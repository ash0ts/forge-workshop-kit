"""Package existing workshop materials for meetings. No execution or publication."""

import argparse
import hashlib
import html
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = "https://ash0ts.github.io/forge-workshop-kit"
GITHUB = "https://github.com/ash0ts/forge-workshop-kit/blob/main/"
STYLE = ROOT / "decks/share-packet.css"
RENDERER = ROOT / "scripts/render_share_packet.mjs"


def page(title, body, *, prefix=""):
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title><link rel="stylesheet" href="{prefix}packet.css">'
        '</head><body><a class="skip" href="#main">Skip to content</a>'
        f'<main id="main">{body}</main></body></html>'
    )


def build(site, *, pdf=False):
    site = Path(site).resolve()
    target = site / "packet"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("assets", "decks", "docs", "fonts"):
        (target / name).mkdir(exist_ok=True)
    payloads = set()

    def copy(source, relative):
        destination = target / relative
        shutil.copyfile(source, destination)
        payloads.add(destination)

    def write(relative, content):
        destination = target / relative
        destination.write_text(content)
        payloads.add(destination)

    copy(STYLE, "packet.css")
    fonts = ROOT / "skills/teenage-engineering-visualizations/assets/fonts"
    for path in fonts.iterdir():
        if path.is_file():
            copy(path, "fonts/" + path.name)

    templates = json.loads((ROOT / "src/forge_workshop_kit/workshops.json").read_text())["templates"]
    templates = [row for row in templates if row.get("authoring", {}).get("deck")]
    reports = json.loads((ROOT / "reports/published.json").read_text())["reports"]
    sharing = json.loads((ROOT / "docs/share-links.json").read_text())["links"]
    documents = ["docs/sharing.md", "docs/use-the-workshops.md", "docs/setup.md",
                 "docs/current-demo-guide.md", "docs/deck-guide.md", "docs/recorded-results.md",
                 "docs/facilitator-start.md", "docs/share-links.md", "docs/loom-walkthrough.md",
                 *[f'docs/run-{row["authoring"]["deck"]["directory"]}.md' for row in templates],
                 "next-up.md", *[row["authoring"]["runbook"] for row in templates]]
    documents = list(dict.fromkeys(documents))
    bundled = {path: "docs/" + Path(path).stem + ".html" for path in documents}
    render_inputs = [{"path": path, "text": (ROOT / path).read_text(), "base": GITHUB,
                      "output": bundled[path], "bundled": bundled} for path in documents]
    render_inputs.append({**render_inputs[0], "id": "brief", "output": "brief.html"})
    rendered = subprocess.run(
        ["node", str(RENDERER), "markdown"], input=json.dumps(render_inputs), text=True, capture_output=True, check=True,
    )
    bodies = json.loads(rendered.stdout)
    for path in documents:
        body = bodies[path]
        filename = Path(path).stem
        copy(ROOT / path, f"docs/{filename}.md")
        title = (ROOT / path).read_text().splitlines()[0].removeprefix("# ")
        write(f"docs/{filename}.html", page(
            title, '<nav><a href="../index.html">Workshop packet</a></nav>' + body,
            prefix="../",
        ))

    cards, catalog = [], []
    pdf_count = 0
    for row in templates:
        deck = row["authoring"]["deck"]
        slug, stem = deck["directory"], deck["file_stem"]
        report = reports["airline" if slug == "airline_monitoring" else slug]
        poster = json.loads((ROOT / "visual-guides" / slug / "poster.json").read_text())["poster"]
        image = ROOT / "visual-guides/scenes" / slug / "start.svg"
        copy(image, f"assets/{slug}.svg")
        copy(ROOT / "decks" / slug / "public/images/workshop-qr.svg", f"assets/{slug}-qr.svg")
        pdf_source = site / slug / f"{stem}.pdf"
        pdf_link = f"{PUBLIC}/{slug}/{stem}.pdf"
        if pdf_source.exists():
            copy(pdf_source, "decks/" + pdf_source.name)
            pdf_count += 1
            pdf_link = f"decks/{pdf_source.name}"
        elif pdf:
            raise FileNotFoundError(f"Build the deck PDF first: {pdf_source}")
        runbook = "docs/" + Path(row["authoring"]["runbook"]).stem + ".html"
        quick_guide = f"docs/run-{slug}.html"
        share_url = sharing[slug]["short_url"]
        catalog.append({"workshop": row["slug"], "deck": slug, "title": deck["title"],
                        "duration": poster["duration"], "report": report["url"],
                        "notebook": report["notebook_url"], "pdf": pdf_link,
                        "deck_url": report["deck_url"], "runbook": runbook,
                        "quick_guide": quick_guide, "share_url": share_url,
                        "readiness": "technical preview"})
        links = [
            (report["url"], "Read the example"), (report["deck_url"], "Present the deck"),
            (pdf_link, "Deck PDF"), (report["notebook_url"], "Notebook · Forge sign-in"),
            (quick_guide, "How to run this workshop"), (runbook, "Detailed facilitator notes"),
            (f"{PUBLIC}/{slug}/{stem}-source.zip", "Editable deck source"),
        ]
        actions = "".join(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>' for url, label in links)
        cards.append(
            f'<article id="{slug}"><img src="assets/{slug}.svg" '
            f'alt="Illustrated setting for {html.escape(deck["title"], quote=True)}">'
            f'<div class="card-body"><p class="eyebrow">{html.escape(poster["duration"])} · BASIC PYTHON</p>'
            f'<h3>{html.escape(deck["title"])}</h3><p>{html.escape(poster["situation"])}</p>'
            f'<p class="data">Data: {html.escape(poster["dataset"])}</p>'
            f'<div class="actions">{actions}</div>'
            f'<div class="share-code"><a href="{share_url}"><img src="assets/{slug}-qr.svg" '
            f'width="144" height="144" alt="QR code for this workshop’s materials"></a>'
            f'<p>Share this workshop<br><a href="{share_url}">{share_url.removeprefix("https://")}</a></p>'
            '</div></div></article>'
        )
    brief = '<p class="eyebrow">FORGE WORKSHOP KIT · MEETING BRIEF</p>' + bodies["brief"]
    write("brief.html", page("Workshop meeting brief", brief))
    body = (
        '<header><p class="eyebrow">FORGE WORKSHOP KIT · SHARE AND PRESENT</p>'
        '<h1>See what an AI system did, then test a change</h1>'
        '<p>A support request reaches the wrong queue. An agent changes the wrong part of a booking. '
        'Two coding agents finish their tasks, but the app still fails a check. These six Python '
        'workshops follow problems like these through their code, saved records, and tested changes in Forge.</p>'
        '<p>Choose one example for a meeting, or copy its notebook into your own project to try the exercises.</p>'
        '<p class="status"><strong>Published technical previews.</strong> Recorded demonstrations and reading material '
        'are available now. Fresh-account and participant rehearsals remain open before full classes.</p>'
        '<div class="actions primary"><a href="brief.pdf">Meeting brief PDF</a>'
        f'<a href="{PUBLIC}/packet/workshop-meeting-packet.zip">Download the packet</a>'
        '<a href="docs/sharing.html#slack-message">Slack message</a>'
        '<a href="docs/loom-walkthrough.html">Ten-minute Loom script</a>'
        '<a href="docs/current-demo-guide.html">Short demo routes</a>'
        '<a href="docs/facilitator-start.html">Run a workshop</a>'
        f'<a href="{PUBLIC}/share/">QR codes and sharing links</a></div></header>'
        '<section class="start"><h2>Start with one example</h2>'
        '<p>Open its Report before asking anyone to sign in. In a meeting, show the input, '
        'the changed code, and one recorded outcome. The deck and PDF supply a fallback '
        'when a live product page needs access.</p><p>Live exercises use the participant’s own Forge project '
        'and credentials. The $8 notebook inference allowance is adjustable. Compute, ARIA, and native '
        'tag judging have separate billing. <a href="docs/setup.html">Read the setup instructions</a>.</p></section>'
        f'<section aria-labelledby="choices"><h2 id="choices">Choose the project</h2><div class="catalog">{"".join(cards)}</div></section>'
        '<footer><p>Airline’s AI Alignment and prepared Insights activities remain unqualified. '
        'Use its recorded demonstration and keep missing judgments visible. '
        '<a href="docs/next-up.html">Current readiness</a> · '
        '<a href="docs/recorded-results.html">Results and limitations</a></p>'
        f'<p>The download includes the briefing, {pdf_count} deck PDFs, setup, demo routes, and facilitator notes. '
        'The saved pages and PDFs open offline; Forge records require their usual access. '
        '<a href="https://github.com/ash0ts/forge-workshop-kit">Repository and contribution guide</a>.</p></footer>'
    )
    if not pdf:
        body = body.replace('<a href="brief.pdf">Meeting brief PDF</a>', '<a href="brief.html">Meeting brief</a>')
    write("index.html", page("Forge workshop meeting packet", body))
    write("catalog.json", json.dumps(catalog, indent=2) + "\n")
    write("README.txt",
        "Open index.html to choose a workshop. Open brief.html for the meeting script and Slack copy; PDF builds also include brief.pdf.\n"
        f"The decks/ folder contains {pdf_count} presentation PDFs, including reveal states. Missing PDFs link to the public website.\n"
        "docs/ contains setup, the ten-minute Loom script, short demo routes, runbooks, tracking instructions, and current readiness.\n"
        "No setup or credentials are needed to read these saved files. External links need an internet connection; Forge links require their usual access.\n"
        "These remain technical previews; the packet is for recorded demonstrations and pilot preparation.\n"
    )
    if pdf:
        subprocess.run(["node", str(RENDERER), "pdf", str(target / "brief.html"), str(target / "brief.pdf"), PUBLIC + "/packet/brief.html"], check=True)
        payloads.add(target / "brief.pdf")
    # Only files written by this build belong in the archive. An earlier build
    # or unrelated file in the output folder must not become a shared attachment.
    payloads = sorted(payloads)
    manifest = {"source_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip(),
                "source_has_uncommitted_changes": bool(subprocess.run(["git", "status", "--porcelain", "--", "docs", "next-up.md", "scripts/build_share_packet.py", "scripts/render_share_packet.mjs", "decks/share-packet.css", "reports/published.json", "src/forge_workshop_kit/workshops.json", "visual-guides", "skills/teenage-engineering-visualizations/assets/fonts"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()),
                "workshops": catalog, "files": [{"file": str(p.relative_to(target)), "bytes": p.stat().st_size,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in payloads]}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(target / "workshop-meeting-packet.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [*payloads, target / "manifest.json"]:
            archive.write(path, path.relative_to(target))
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "dist/decks/site")
    parser.add_argument("--pdf", action="store_true")
    args = parser.parse_args()
    print(build(args.site, pdf=args.pdf))
