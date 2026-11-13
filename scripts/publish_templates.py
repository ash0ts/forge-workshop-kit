"""Explicitly publish a verified release to one project. No exercises are executed."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import httpx
from release_support import REPOSITORY, ROOT, project_metadata, templates

NOTEBOOK_QUERY = """query($id:ID!){notebook(id:$id){id name project{name entity{name}} currentVersion{artifactCollectionName versionIndex sourceFileName} viewerPermissions}}"""


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_receipt(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def load_receipt(path, project):
    if not path.exists():
        return {"schema_version": 1, "project": project, "templates": {}}
    saved = json.loads(path.read_text())
    if saved.get("project") != project or saved.get("schema_version") != 1:
        raise ValueError(
            "Deployment receipt belongs to another project or has the old unscoped format. Use --adopt-ids to verify and import old IDs."
        )
    return saved


def verify_destination(notebook, project):
    actual = notebook["project"]["entity"]["name"] + "/" + notebook["project"]["name"]
    if actual != project:
        raise ValueError(
            f"Notebook {notebook['id']} belongs to {actual}, not {project}. Nothing was changed."
        )
    return notebook


def load_build(folder, only=None):
    manifest = json.loads((folder / "release-manifest.json").read_text())
    if manifest["release"] != project_metadata()["version"]:
        raise ValueError("Build release does not match pyproject.toml. Rebuild before publishing.")
    rows = {slug: row for slug, row in manifest["templates"].items() if not only or slug in only}
    if only and set(only) - set(rows):
        raise ValueError("A selected notebook is absent from this build.")
    for item in [
        manifest["wheel"],
        *[part for row in rows.values() for part in (row["source"], row["html"])],
    ]:
        path = (folder / item["file"]).resolve()
        if not path.is_relative_to(folder.resolve()) or sha256(path) != item["sha256"]:
            raise ValueError(f"Build file changed after validation: {item['file']}")
    return manifest, rows


def verify_released_wheel(manifest):
    url = f"{REPOSITORY}/releases/download/v{manifest['release']}/{manifest['wheel']['file']}"
    digest = hashlib.sha256()
    with httpx.stream("GET", url, timeout=30, follow_redirects=True) as response:
        response.raise_for_status()
        for chunk in response.iter_bytes():
            digest.update(chunk)
    if digest.hexdigest() != manifest["wheel"]["sha256"]:
        raise ValueError(
            "The public wheel differs from this build. Publish the matching release asset first."
        )


def read_notebook(query, notebook_id, project):
    notebook = query(NOTEBOOK_QUERY, {"id": notebook_id})["notebook"]
    if not notebook:
        raise ValueError(f"Notebook {notebook_id} is unavailable.")
    return verify_destination(notebook, project)


def remote_matches(api, notebook, project, row):
    version = notebook.get("currentVersion")
    if not version:
        return False
    artifact = api.artifact(
        f"{project}/{version['artifactCollectionName']}:v{version['versionIndex']}", type="notebook"
    )
    with tempfile.TemporaryDirectory(prefix="workshop-readback-") as directory:
        for item, name in (
            (row["source"], "notebook.py"),
            (row["html"], "__marimo__/notebook.html"),
        ):
            try:
                downloaded = artifact.get_entry(name).download(root=directory)
            except KeyError:
                return False
            if sha256(downloaded) != item["sha256"]:
                return False
    return True


def publish_one(project, folder, receipt_path, slug, *, api=None):
    import wandb

    manifest, rows = load_build(folder, [slug])
    row = rows[slug]
    api = api or wandb.Api(timeout=30)
    query = api._service_api.execute_graphql
    saved = load_receipt(receipt_path, project)
    record = saved["templates"].get(slug, {})
    if record.get("status") == "create_pending" and not record.get("id"):
        raise RuntimeError(
            "Creation may have succeeded before an interruption. Find the notebook in the project and supply --notebook-id SLUG=ID; do not create a duplicate."
        )
    entity, project_name = project.split("/")
    if not record.get("id"):
        saved["templates"][slug] = {"status": "create_pending"}
        write_receipt(receipt_path, saved)
        notebook = query(
            "mutation($e:String!,$p:String!){createNotebook(input:{entityName:$e,projectName:$p,template:BASIC}){notebook{id}}}",
            {"e": entity, "p": project_name},
        )["createNotebook"]["notebook"]
        record = {"id": notebook["id"], "status": "created"}
        saved["templates"][slug] = record
        write_receipt(receipt_path, saved)
    notebook = read_notebook(query, record["id"], project)
    if not remote_matches(api, notebook, project, row):
        saved["templates"][slug] = {
            **record,
            "status": "publishing",
            "release": manifest["release"],
        }
        write_receipt(receipt_path, saved)
        query(
            "mutation($id:ID!,$n:String!){renameNotebook(input:{id:$id,name:$n}){notebook{id}}}",
            {"id": record["id"], "n": row["title"]},
        )
        # Destination was read back before either rename or artifact publication.
        with wandb.init(
            entity=entity,
            project=project_name,
            job_type="workshop-template",
            name=row["title"],
            settings=wandb.Settings(disable_git=True, init_timeout=45),
        ) as run:
            artifact = wandb.Artifact(
                notebook["currentVersion"]["artifactCollectionName"],
                type="notebook",
                metadata={
                    "release": manifest["release"],
                    "workflow_version": row["workflow_version"],
                    "source_sha256": row["source"]["sha256"],
                    "html_sha256": row["html"]["sha256"],
                },
            )
            artifact.add_file(str(folder / row["source"]["file"]), name="notebook.py")
            artifact.add_file(str(folder / row["html"]["file"]), name="__marimo__/notebook.html")
            run.log_artifact(artifact).wait(timeout=120)
        notebook = read_notebook(query, record["id"], project)
        if not remote_matches(api, notebook, project, row):
            raise RuntimeError(
                "Published source/preview readback differs from the built files. Rerun publication to inspect and resume."
            )
    saved["templates"][slug] = {
        **record,
        "status": "verified",
        "release": manifest["release"],
        "source_sha256": row["source"]["sha256"],
        "html_sha256": row["html"]["sha256"],
        "currentVersion": notebook["currentVersion"],
        "url": f"https://forge.coreweave.com/notebooks/{record['id']}/view",
    }
    write_receipt(receipt_path, saved)
    print(slug, saved["templates"][slug]["url"], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--only", action="append", choices=[row["slug"] for row in templates()])
    parser.add_argument("--build", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument(
        "--adopt-ids",
        type=Path,
        help="Verify and import IDs from a prior receipt; never infer its project.",
    )
    parser.add_argument("--notebook-id", action="append", default=[], metavar="SLUG=ID")
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Maximum seconds per notebook; interrupted publication can resume.",
    )
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.project):
        parser.error("Use entity/project.")
    folder = (args.build or ROOT / "dist" / ("v" + project_metadata()["version"])).resolve()
    receipt = (
        args.receipt or ROOT / ".workshop-deployments" / args.project / "templates.json"
    ).resolve()
    manifest, rows = load_build(folder, [args.worker] if args.worker else args.only)
    if args.worker:
        publish_one(args.project, folder, receipt, args.worker)
        return
    verify_released_wheel(manifest)
    saved = load_receipt(receipt, args.project)
    adopt = {}
    if args.adopt_ids:
        old = json.loads(args.adopt_ids.read_text())
        adopt.update(old.get("templates", old))
    for value in args.notebook_id:
        slug, notebook_id = value.split("=", 1)
        if slug not in rows:
            parser.error(f"Notebook ID supplied for unselected template {slug}.")
        adopt[slug] = {"id": notebook_id}
    if adopt:
        import wandb

        query = wandb.Api(timeout=30)._service_api.execute_graphql
        # Validate every imported destination before saving any ID or changing any notebook.
        verified = {
            slug: read_notebook(query, record["id"], args.project)
            for slug, record in adopt.items()
            if slug in rows
        }
        for slug, notebook in verified.items():
            saved["templates"][slug] = {"id": notebook["id"], "status": "adopted"}
        write_receipt(receipt, saved)
    for slug in rows:
        subprocess.run(
            [
                sys.executable,
                __file__,
                "--project",
                args.project,
                "--build",
                str(folder),
                "--receipt",
                str(receipt),
                "--worker",
                slug,
            ],
            check=True,
            timeout=args.timeout,
        )


if __name__ == "__main__":
    main()
