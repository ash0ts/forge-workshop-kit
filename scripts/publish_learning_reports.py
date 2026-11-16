"""Build the six learning Reports; --apply publishes without running a workshop.

Markdown in reports/ is the source. Destination-scoped receipts preserve Report
identities; existing rehearsal Reports and participant conclusions are untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("pending", "solar", "routing", "inspection", "transit", "airline")


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def build_report(slug, project):
    import wandb_workspaces.reports.v2 as wr

    entity, name = project.split("/")
    source = (ROOT / "reports" / f"{slug}.md").read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{slug}: start with one Report title")
    title = lines.pop(0)[2:].strip()
    if len(title) > 128:
        raise ValueError(f"{slug}: Report title exceeds 128 characters")
    blocks, pending = [], []

    def flush():
        if text := "\n".join(pending).strip():
            blocks.append(wr.MarkdownBlock(text=text))
        pending.clear()

    images, links = [], re.findall(r"\]\((https://[^\s)]+)\)", source)
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            flush()
            language = line[3:].strip() or "python"
            code = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError(f"{slug}: unterminated code fence")
            if language not in {"python", "json", "yaml", "javascript", "css", "html", "markdown"}:
                blocks.append(wr.MarkdownBlock(text=f"```{language}\n" + "\n".join(code) + "\n```"))
            else:
                blocks.append(wr.CodeBlock(code="\n".join(code), language=language))
        elif match := re.fullmatch(r"(#{2,3}) (.+)", line):
            flush()
            heading = wr.H2 if len(match[1]) == 2 else wr.H3
            blocks.append(heading(text=match[2]))
        elif match := re.fullmatch(r"!\[([^\]]*)\]\((https://[^\s)]+)\)", line):
            flush()
            images.append(match[2])
            # Native Report images retain their aspect ratio and use the text
            # column. Keep the explanation with the figure, with a usable route
            # to tiny screenshot fields instead of enlarging or cropping them.
            blocks.append(wr.Image(url=match[2], caption=[
                match[1] + " ", wr.Link(text="Open full-size figure", url=match[2]),
            ]))
        else:
            pending.append(line)
        index += 1
    flush()
    if len(images) < 2:
        raise ValueError(f"{slug}: include at least two teaching visuals")
    workshop_slug = "airline_monitoring" if slug == "airline" else slug
    notebook_start = f"https://ash0ts.github.io/forge-workshop-kit/packet/start/{workshop_slug}.html"
    if notebook_start not in links:
        raise ValueError(f"{slug}: missing current notebook start page")
    if not any(link.startswith("https://ash0ts.github.io/forge-workshop-kit/packet/notebooks/")
               and link.endswith(".py") for link in links):
        raise ValueError(f"{slug}: missing current notebook download")
    if not any(link.startswith("https://github.com/ash0ts/forge-workshop-kit/releases/download/")
               and link.endswith(".py") for link in links):
        raise ValueError(f"{slug}: missing versioned notebook download")
    report = wr.Report(
        entity=entity, project=name, title=title, width="fixed",
        description="A worked example with code, recorded results, and a notebook you can run in your own Forge project.",
        blocks=blocks,
    )
    plan = {
        "slug": slug, "title": title, "project": project,
        "source": f"reports/{slug}.md", "source_sha256": digest(source),
        "images": images, "links": list(dict.fromkeys(links)), "blocks": len(blocks),
        "notebook_url": notebook_start,
        "deck_url": "https://ash0ts.github.io/forge-workshop-kit/" + ("airline_monitoring" if slug == "airline" else slug) + "/",
    }
    # A rendering-only revision (for example linked figure captions) must still
    # update the native Report even when its Markdown has not changed.
    plan["render_sha256"] = digest(json.dumps(
        report._to_model().spec.model_dump(mode="json", by_alias=True, exclude_none=True)["blocks"],
        sort_keys=True,
    ))
    return report, plan


def public_query(query, variables):
    import httpx

    # No SDK session, API key, or browser cookies: check the public access path.
    response = httpx.post("https://api.wandb.ai/graphql", json={"query": query, "variables": variables}, timeout=30)
    response.raise_for_status()
    result = response.json()
    if result.get("errors"):
        raise RuntimeError("Anonymous read failed: " + json.dumps(result["errors"]))
    return result["data"]


def public_readback(report, project):
    from wandb_workspaces.reports.v2.gql import view_report

    view = public_query(view_report, {"reportId": report.id}).get("view")
    if not view:
        raise RuntimeError("Report was saved but is not readable without authentication")
    actual_project = view["project"]["entityName"] + "/" + view["project"]["name"]
    if actual_project != project or view["displayName"] != report.title:
        raise RuntimeError("Published Report identity differs from the requested destination")
    spec = json.loads(view["spec"])
    expected = report._to_model().spec.model_dump(mode="json", by_alias=True, exclude_none=True)
    if spec["blocks"] != expected["blocks"]:
        raise RuntimeError("Published Report blocks differ from the built content")
    return {"anonymous_readback": True, "content_sha256": digest(json.dumps(spec["blocks"], sort_keys=True))}


def check_catalog_identities(project, slugs, receipts, catalog):
    """An ignored local receipt must not be the only protection against duplicates."""
    if catalog.get("project") != project:
        return
    for slug in slugs:
        known = catalog.get("reports", {}).get(slug)
        if not known:
            continue
        report_id = unquote(urlparse(known["url"]).path.rsplit("--", 1)[-1])
        saved_id = receipts.get(slug, {}).get("id")
        if not saved_id:
            raise RuntimeError(
                f"{slug}: the public catalog already names a Report in {project}. "
                f"Restore its destination receipt or use --adopt {slug}={report_id}; "
                "do not create a duplicate."
            )
        if saved_id != report_id:
            raise ValueError(f"{slug}: receipt and public catalog name different Reports; reconcile their identities before publishing")


def build_catalog(project, receipts, previous):
    """Reuse verified metadata when an older receipt predates the link fields."""
    rows = dict(previous.get("reports", {})) if previous.get("project") == project else {}
    for slug, value in receipts.items():
        if value.get("status") != "published":
            continue
        if value.get("project") != project:
            raise ValueError("Receipt destination does not match --project")
        metadata = value.copy()
        if not all(metadata.get(key) for key in ("notebook_url", "deck_url")):
            known = previous.get("reports", {}).get(slug, {}) if previous.get("project") == project else {}
            if known.get("source_sha256") == value["source_sha256"] and known.get("url") == value["url"]:
                fallback = known
            else:
                _, fallback = build_report(slug, project)
                if fallback["source_sha256"] != value["source_sha256"]:
                    raise RuntimeError(f"{slug}: cannot reconstruct links for an older published source. Restore its matching catalog or publish this Report too.")
            for key in ("notebook_url", "deck_url"):
                metadata[key] = fallback[key]
        rows[slug] = {key: metadata[key] for key in ("title", "url", "notebook_url", "deck_url", "source", "source_sha256", "anonymous_readback")}
        # The current start page and a previous hosted template serve different
        # purposes. Keep the verified hosted identity when refreshing prose.
        known = previous.get("reports", {}).get(slug, {}) if previous.get("project") == project else {}
        if hosted_url := metadata.get("hosted_notebook_url") or known.get("hosted_notebook_url"):
            rows[slug]["hosted_notebook_url"] = hosted_url
    return {"project": project, "reports": rows}


def publish(report, plan, receipts, receipt_path):
    import wandb_workspaces.reports.v2 as wr

    slug, project = plan["slug"], plan["project"]
    saved = receipts.get(slug, {})
    if saved and saved.get("project") != project:
        raise ValueError("Receipt destination does not match --project")
    if saved.get("status") == "creating" and not saved.get("id"):
        raise RuntimeError(f"{slug}: creation was interrupted. Find the Report and supply --adopt {slug}=REPORT_ID; do not create a duplicate.")
    if saved.get("id"):
        existing = wr.Report.from_url(f"https://wandb.ai/{project}/reports/learning--{saved['id']}")
        if existing.entity + "/" + existing.project != project:
            raise ValueError("Existing Report belongs to another project")
        report.id = existing.id
        if (saved.get("source_sha256") == plan["source_sha256"]
                and saved.get("render_sha256") == plan["render_sha256"]
                and saved.get("status") == "published"):
            verified = public_readback(report, project)
            return {**saved, **plan, **verified}
        if saved.get("content_sha256"):
            from wandb_workspaces.reports.v2.gql import view_report

            remote = public_query(view_report, {"reportId": existing.id})["view"]
            remote_blocks = json.loads(remote["spec"])["blocks"]
            if digest(json.dumps(remote_blocks, sort_keys=True)) != saved["content_sha256"]:
                raise RuntimeError(f"{slug}: Report was edited after publication. Reconcile those edits with the Markdown before publishing.")
        backup = ROOT / ".workshop-deployments" / project / "learning-report-backups" / f"{slug}-{saved.get('source_sha256', 'adopted')}.json"
        if not backup.exists():
            write_json(backup, existing._to_model().model_dump(mode="json", by_alias=True, exclude_none=True))
    receipts[slug] = {**plan, "id": report.id, "status": "updating" if report.id else "creating"}
    write_json(receipt_path, receipts)
    report.save()
    # Save identity before readback so a temporary read failure can never recreate it.
    url = f"https://forge.coreweave.com/wandb/{project}/reports/{quote(report.title, safe='').replace('%20', '-')}--{report.id}"
    receipts[slug].update(id=report.id, url=url, status="saved")
    write_json(receipt_path, receipts)
    verified = public_readback(report, project)
    receipts[slug].update(verified, status="published")
    write_json(receipt_path, receipts)
    return receipts[slug]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing public entity/project")
    parser.add_argument("--only", choices=SLUGS, action="append")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/learning-reports")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--catalog", type=Path, help="Write the public link index after successful publication")
    parser.add_argument("--adopt", action="append", default=[], metavar="SLUG=REPORT_ID")
    args = parser.parse_args()
    if not re.fullmatch(r"[\w-]+/[\w.-]+", args.project):
        parser.error("--project must be entity/project")
    builds = [build_report(slug, args.project) for slug in args.only or SLUGS]
    for report, plan in builds:
        write_json(args.output / f"{plan['slug']}.json", {
            **plan, "report": report._to_model().model_dump(mode="json", by_alias=True, exclude_none=True),
        })
    if not args.apply:
        print(json.dumps({"mode": "local build", "reports": [plan for _, plan in builds]}, indent=2))
        return
    import wandb

    entity, name = args.project.split("/")
    # Resolve the existing destination. Report.save must not create an accidental project.
    _ = wandb.Api(timeout=30).project(name, entity=entity).id
    destination = public_query(
        "query($entity:String!, $name:String!){project(entityName:$entity,name:$name){name}}",
        {"entity": entity, "name": name},
    ).get("project")
    if not destination:
        raise RuntimeError("Choose a project that is already publicly readable")
    receipt_path = ROOT / ".workshop-deployments" / args.project / "learning-reports.json"
    receipts = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    catalog_path = ROOT / "reports/published.json"
    previous_catalog = json.loads(catalog_path.read_text()) if catalog_path.exists() else {}
    for adoption in args.adopt:
        slug, report_id = adoption.split("=", 1)
        if slug not in SLUGS:
            parser.error("Unknown adoption slug")
        if receipts.get(slug, {}).get("id") not in (None, "", report_id):
            raise ValueError("Adoption would replace an existing Report identity")
        receipts[slug] = {**receipts.get(slug, {}), "id": report_id, "project": args.project, "status": "adopted"}
    check_catalog_identities(args.project, [plan["slug"] for _, plan in builds], receipts, previous_catalog)
    for report, plan in builds:
        receipts[plan["slug"]] = publish(report, plan, receipts, receipt_path)
        print(json.dumps({"slug": plan["slug"], "url": receipts[plan["slug"]]["url"], "status": "published"}))
    write_json(receipt_path, receipts)
    write_json(args.output / "published.json", {slug: receipts[slug] for slug in args.only or SLUGS})
    if args.catalog:
        write_json(args.catalog, build_catalog(args.project, receipts, previous_catalog))


if __name__ == "__main__":
    main()
