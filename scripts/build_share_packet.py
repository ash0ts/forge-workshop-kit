"""Package participant and facilitator materials. No execution or publication."""

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


def notebook_start_body(row, report):
    """Use a persistent downloaded file while hosted notebook access is unavailable."""
    deck = row["authoring"]["deck"]
    slug = deck["directory"]
    notebook = Path(row["authoring"]["notebook"])
    hosted_url = report.get("hosted_notebook_url")
    if hosted_url is not None and (not isinstance(hosted_url, str)
                                  or not hosted_url.startswith("https://forge.coreweave.com/notebooks/")):
        raise ValueError(f"{slug}: hosted template must name an actual Forge notebook")
    hosted_help = (
        '<details><summary>Optional: use the older hosted template in Forge (v0.11.1)</summary>'
        '<p>These hosted templates have not received the v0.12.0 update because notebook-management access '
        'for the publishing account is blocked. They do not include the new direct ARIA controls.</p>'
        '<p><a href="' + html.escape(hosted_url, quote=True) + '">Open the v0.11.1 Forge template</a></p>'
        '<p>If your account supports notebooks, choose <strong>Copy to project</strong>, select your writable project, '
        'and open the copy in Edit. If the link redirects to Home or Notebooks is unavailable, use the current '
        'download above. A template link cannot grant product or compute access.</p>'
        '<p>If your project supports notebook import, you can import the current downloaded <code>.py</code> file instead.</p></details>'
    ) if hosted_url else (
        '<p>If your Forge project supports notebook import, you can import the downloaded '
        '<code>.py</code> file. The local path above works without hosted notebook access.</p>'
    )
    extras = " ".join(f"--extra {extra}" for extra in row.get("extras", []))
    launch = ("uvx --from wandb==0.31.0 wandb login --host https://api.wandb.ai --verify\n"
              f"uvx --from marimo==0.25.2 marimo edit --sandbox {notebook.name}")
    checkout = ("git clone https://github.com/ash0ts/forge-workshop-kit.git\n"
                "cd forge-workshop-kit\n"
                f"uv sync --frozen {extras}\n"
                f"uv run {extras} wandb login --host https://api.wandb.ai --verify\n"
                f"uv run {extras} marimo edit {notebook}")
    return (
        '<nav><a href="../index.html">All workshop materials</a></nav>'
        f'<h1>Start {html.escape(deck["title"])}</h1>'
        '<p>Read the example before running anything. The notebook is editable Python; '
        'your executions and saved results belong to your own project.</p>'
        '<p><strong>Current notebook: v0.12.0.</strong> Download the file and open it on your laptop. '
        'This version includes the direct ARIA controls and uses your Forge project for saved records. '
        'It does not require hosted notebook or remote Sandbox access.</p>'
        f'<div class="actions"><a href="../notebooks/{notebook.name}" download>Download the current notebook (.py)</a>'
        '<a href="' + html.escape(report["url"], quote=True) + '">Read the worked example</a></div>'
        '<h2>Open the downloaded notebook</h2><ol>'
        '<li>Install <a href="https://docs.astral.sh/uv/getting-started/installation/">uv</a>. '
        'Save the downloaded notebook in a folder you will keep, then open a terminal in that folder.</li>'
        '<li>Sign in to W&amp;B with your own credentials, then open the file with these commands:</li></ol>'
        f'<pre class="setup-commands"><code>{html.escape(launch)}</code></pre>'
        '<p>The first launch installs the notebook’s pinned Python dependencies. Here, '
        '<code>--sandbox</code> means a local dependency environment; it does not create a remote Forge Sandbox.</p>'
        '<p>Click <strong>Run all</strong> once to load the workshop controls. Then use the buttons in each exercise. '
        'This initialization starts no training or model request.</p>'
        '<p>Keep the downloaded <code>.py</code> file and its <code>.workshop/</code> folder. '
        'Reopen the same file with the second command to return to your edits and completed work.</p>'
        '<details><summary>A managed laptop reports an UnknownIssuer certificate error</summary>'
        '<p>Tell uv to use your operating system’s trusted certificates, then rerun the same launch command. '
        'On macOS or Linux:</p><pre><code>export UV_SYSTEM_CERTS=true</code></pre>'
        '<p>In PowerShell:</p><pre><code>$env:UV_SYSTEM_CERTS = "true"</code></pre>'
        '<p>This uses the certificates already trusted by your computer; it keeps HTTPS verification enabled.</p></details>'
        '<h2>Connect your project</h2><p>Create a project you can write to in '
        '<a href="https://forge.coreweave.com">Forge</a>, then enter its <code>entity/project</code> in the notebook setup. '
        'Opening the notebook starts no training or model request; each execution has an explicit run button.</p>'
        '<p>The default $8 inference allowance is adjustable. Compute, ARIA, and native tag judging are separate.</p>'
        + hosted_help +
        '<details><summary>Contributors: run from the complete source checkout</summary>'
        '<p>Install Git, uv, and Python 3.11–3.13, then run:</p>'
        f'<pre class="setup-commands"><code>{html.escape(checkout)}</code></pre></details>'
        '<p><a href="../docs/setup.html">Setup and saved-work recovery</a> · '
        f'<a href="../docs/run-{slug}.html">Facilitator instructions</a></p>'
    )


def build(site, *, pdf=False):
    site = Path(site).resolve()
    target = site / "packet"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("assets", "decks", "docs", "fonts", "notebooks", "start"):
        (target / name).mkdir(exist_ok=True)
    # These communication drafts remain in Git, outside the participant website.
    for name in ("sharing", "loom-walkthrough"):
        for suffix in ("html", "md"):
            (target / "docs" / f"{name}.{suffix}").unlink(missing_ok=True)
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
    documents = ["docs/workshop-overview.md", "docs/use-the-workshops.md", "docs/setup.md",
                 "docs/current-demo-guide.md", "docs/deck-guide.md", "docs/recorded-results.md",
                 "docs/facilitator-start.md", "docs/share-links.md",
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
        notebook_path = Path(row["authoring"]["notebook"])
        copy(ROOT / notebook_path, "notebooks/" + notebook_path.name)
        start_link = f"start/{slug}.html"
        start_body = notebook_start_body(row, report)
        write(start_link, page(f"Start {deck['title']}", start_body, prefix="../"))
        catalog.append({"workshop": row["slug"], "deck": slug, "title": deck["title"],
                        "duration": poster["duration"], "report": report["url"],
                        "notebook": report["notebook_url"], "start": start_link, "pdf": pdf_link,
                        "deck_url": report["deck_url"], "runbook": runbook,
                        "quick_guide": quick_guide, "share_url": share_url,
                        "readiness": "technical preview"})
        links = [
            (report["url"], "Read the example"), (report["deck_url"], "Present the deck"),
            (pdf_link, "Deck PDF"), (start_link, "Start the notebook"),
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
    brief = '<p class="eyebrow">FORGE WORKSHOP KIT · WORKSHOP GUIDE</p>' + bodies["brief"]
    write("brief.html", page("Forge workshop guide", brief))
    body = (
        '<header><p class="eyebrow">FORGE WORKSHOP KIT · LEARN AND BUILD</p>'
        '<h1>See what an AI system did, then test a change</h1>'
        '<p>A support request reaches the wrong queue. An agent changes the wrong part of a booking. '
        'Two coding agents finish their tasks, but the app still fails a check. These six Python '
        'workshops follow problems like these through their code, saved records, and tested changes in Forge.</p>'
        '<p>Choose a problem to work on. Read its example, inspect the diagrams, and run the notebook in your own project or on your laptop.</p>'
        '<p class="status"><strong>Published technical previews.</strong> Recorded demonstrations and reading material '
        'are available now. Fresh-account and participant rehearsals remain open before full classes.</p>'
        '<div class="actions primary"><a href="docs/setup.html">Setup instructions</a>'
        '<a href="workshop-materials.zip" download>Download the materials</a>'
        '<a href="brief.pdf">Workshop guide PDF</a>'
        '<a href="docs/facilitator-start.html">Facilitate a session</a></div></header>'
        '<section class="start"><h2>Start with one example</h2>'
        '<p>Open its Report to see the input, the changed code, and one recorded outcome. The deck and PDF supply a fallback '
        'when a live product page needs access.</p><p>Live exercises use the participant’s own Forge project '
        'and credentials. The $8 notebook inference allowance is adjustable. Compute, ARIA, and native '
        'tag judging have separate billing. <a href="docs/setup.html">Read the setup instructions</a>.</p></section>'
        f'<section aria-labelledby="choices"><h2 id="choices">Choose the project</h2><div class="catalog">{"".join(cards)}</div></section>'
        '<footer><p>Airline’s AI Alignment and prepared Insights activities remain unqualified. '
        'Use its recorded demonstration and keep missing judgments visible. '
        '<a href="docs/next-up.html">Current readiness</a> · '
        '<a href="docs/recorded-results.html">Results and limitations</a></p>'
        f'<p>The download includes the guide, {pdf_count} deck PDFs, editable notebook files, setup, and facilitator notes. '
        'The saved pages and PDFs open offline; Forge records require their usual access. '
        '<a href="https://github.com/ash0ts/forge-workshop-kit">Repository and contribution guide</a>.</p></footer>'
    )
    if not pdf:
        body = body.replace('<a href="brief.pdf">Workshop guide PDF</a>', '<a href="brief.html">Workshop guide</a>')
    write("index.html", page("Forge workshop materials", body))
    write("catalog.json", json.dumps(catalog, indent=2) + "\n")
    write("README.txt",
        "Open index.html to choose a workshop. Open brief.html for the workshop overview; PDF builds also include brief.pdf.\n"
        f"The decks/ folder contains {pdf_count} presentation PDFs, including reveal states. Missing PDFs link to the public website.\n"
        "docs/ contains setup, runbooks, results, and current readiness. start/ explains how to save and open the current notebook files; notebooks/ has the editable Python files.\n"
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
                "source_has_uncommitted_changes": bool(subprocess.run(["git", "status", "--porcelain", "--", "docs", "notebooks", "next-up.md", "scripts/build_share_packet.py", "scripts/render_share_packet.mjs", "decks/share-packet.css", "reports/published.json", "src/forge_workshop_kit/workshops.json", "visual-guides", "skills/teenage-engineering-visualizations/assets/fonts"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()),
                "workshops": catalog, "files": [{"file": str(p.relative_to(target)), "bytes": p.stat().st_size,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in payloads]}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(target / "workshop-materials.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [*payloads, target / "manifest.json"]:
            archive.write(path, path.relative_to(target))
    # Existing distributed links keep working; both names contain attendee materials.
    shutil.copyfile(target / "workshop-materials.zip", target / "workshop-meeting-packet.zip")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "dist/decks/site")
    parser.add_argument("--pdf", action="store_true")
    args = parser.parse_args()
    print(build(args.site, pdf=args.pdf))
