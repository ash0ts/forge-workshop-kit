"""Build workshop decks and downloads. Never publish or execute a workshop."""

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src/forge_workshop_kit/workshops.json"
DECKS = {
    row["authoring"]["deck"]["directory"]: {
        "title": row["authoring"]["deck"]["title"],
        "filename": row["authoring"]["deck"]["file_stem"],
    }
    for row in json.loads(MANIFEST.read_text(encoding='utf-8'))["templates"]
    if row.get("authoring", {}).get("deck")
}

SOURCE_ITEMS = (
    "README.md",
    "package.json",
    "slides.md",
    "style.css",
    "global-bottom.vue",
    "components",
    "data",
    "public",
    "scripts",
    "notes",
)


def run(args, cwd, env=None):
    subprocess.run(args, cwd=cwd, env=env, check=True)


def archive(path, source, items):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for item in items:
            for file in sorted(item.rglob("*") if item.is_dir() else [item]):
                if file.is_file() and "__pycache__" not in file.parts:
                    bundle.write(file, file.relative_to(source))


def source_archive(path, deck, slug):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in SOURCE_ITEMS:
            item = deck / name
            for file in sorted(item.rglob("*") if item.is_dir() else [item]):
                if file.is_file() and "__pycache__" not in file.parts:
                    bundle.write(file, Path("decks") / slug / file.relative_to(deck))
        for name in ("build_decks.py", "build_visual_guides.py", "technical_guide_storyboard.py", "scene_storyboard.py", "share_storyboard.py", "build_share_links.py", "render_share_qr.mjs", "validate_deck.mjs", "check_deck_pdf.py", "check_deck_assets.py", "serve_deck.py", "aria_storyboard.py"):
            bundle.write(ROOT / "scripts" / name, Path("scripts") / name)
        for path in sorted((ROOT / "scripts").glob("illustrate_*.py")):
            bundle.write(path, Path("scripts") / path.name)
        for name in ("README.md", "package.json", "package-lock.json", "scripts/deck.mjs", "aria.css", "technical-manual.css", "technical-manual-tokens.css", "workshop-scenes.css", "workshop-sharing.css", "share-packet.css", "components/TechnicalGuide.vue"):
            bundle.write(ROOT / "decks" / name, Path("decks") / name)
        bundle.write(ROOT / "docs/share-links.json", "docs/share-links.json")
        for directory in (ROOT / "skills", ROOT / "visual-guides" / slug, ROOT / "visual-guides/media", ROOT / "visual-guides/scenes"):
            for file in sorted(directory.rglob("*")):
                if file.is_file() and not {"node_modules", "__pycache__", ".DS_Store"}.intersection(file.parts):
                    bundle.write(file, file.relative_to(ROOT))
        guides = json.loads((ROOT / "visual-guides/index.json").read_text(encoding="utf-8"))
        guides["workshops"] = [row for row in guides["workshops"] if row["slug"] == slug]
        bundle.writestr("visual-guides/index.json", json.dumps(guides, indent=2) + "\n")
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        manifest["templates"] = [
            row for row in manifest["templates"]
            if row.get("authoring", {}).get("deck", {}).get("directory") == slug
        ]
        bundle.writestr("src/forge_workshop_kit/workshops.json", json.dumps(manifest, indent=2) + "\n")
        aria_slug = {"pending": "pending_inc", "solar": "solar_autoresearch", "routing": "request_routing", "inspection": "visual_inspection", "transit": "transit_factory", "airline_monitoring": "airline_monitoring"}[slug]
        aria_path = ROOT / "src/forge_workshop_kit/assets/aria" / aria_slug
        if aria_path.exists():
            for file in sorted(aria_path.rglob("*")):
                if file.is_file():
                    bundle.write(file, file.relative_to(ROOT))
        definitions = Path("src/forge_workshop_kit/assets/visuals.json")
        bundle.write(ROOT / definitions, definitions)
        # Storyboards load this stdlib-only renderer without installing the kit.
        aria_visual = Path("src/forge_workshop_kit/aria_visual.py")
        bundle.write(ROOT / aria_visual, aria_visual)
        bundle.writestr(
            "README.md",
            f"# {DECKS[slug]['title']}\n\n"
            "Install Node.js 22.23.2 or later, Python 3.11 or later, and uv.\n\n"
            f"Run `python3 scripts/build_decks.py --only {slug} --install` to build the browser deck.\n"
            "Add `--pdf --validate` with Chrome installed to export and check every page.\n"
            f"Edit `decks/{slug}/scripts/build-storyboard.py`; the build regenerates slides and notes.\n"
            "No workshop, training, or model request runs when building or opening this deck.\n",
        )


def write_routes(directory, layout, base):
    routes = ["presenter", "overview", "notes"] + [
        route for slide in layout["slides"]
        for route in (str(slide["number"]), f"presenter/{slide['number']}")
    ]
    for route in routes:
        destination = directory / route / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(directory / "index.html", destination)
    aliases = []
    for slide in layout["slides"]:
        name = slide.get("name") or slide.get("key")
        if not name:
            continue
        if not all(c.isalnum() or c in "-_" for c in name):
            raise ValueError(f"Unsafe slide alias: {name}")
        for prefix in ("", "presenter/"):
            route = prefix + name
            target = f"{base}{prefix}{slide['number']}"
            destination = directory / route / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                '<!doctype html><html lang="en"><meta charset="utf-8">'
                f'<meta http-equiv="refresh" content="0;url={html.escape(target, quote=True)}">'
                f'<title>{html.escape(slide["title"])}</title>'
                f'<a href="{html.escape(target, quote=True)}">Open this slide</a></html>', encoding='utf-8'
            )
            aliases.append(route)
    shutil.copyfile(directory / "index.html", directory / "404.html")
    (directory / "static-routes.json").write_text(json.dumps({"routes": routes + aliases}, indent=2) + "\n", encoding='utf-8')


def install_toolchain():
    """All decks resolve the same pinned dependencies from their parent directory."""
    run(["npm", "ci"], ROOT / "decks", {**os.environ, "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD": "1"})


def prepare_browser_files(directory, title, *, offline=False, pdf=None):
    """Keep the display self-contained and make double-click failures actionable."""
    favicon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23183334'/%3E%3Cpath d='M8 9h16M8 16h11M8 23h16' stroke='%23faf5df' stroke-width='3'/%3E%3C/svg%3E"
    for index in directory.rglob("index.html"):
        source = index.read_text(encoding="utf-8")
        source = re.sub(r'<link rel="icon" href="[^"]+">', f'<link rel="icon" href="{favicon}">', source)
        if offline and '<div id="app">' in source and 'id="offline-help"' not in source:
            pdf_path = os.path.relpath(directory / "deck.pdf", index.parent)
            pdf_link = f'<p><a href="{pdf_path}">Open the complete PDF now</a>. No server or internet is needed.</p>' if pdf else ''
            help_panel = (
                '<aside id="offline-help" hidden style="font:18px/1.6 system-ui;max-width:760px;margin:64px auto;padding:24px;color:#172d2d;background:#f4f3ed">'
                f'<h1>{html.escape(title)}</h1><h2>Start the downloaded deck</h2>'
                '<p>This interactive presentation needs a local HTTP address. Double-clicking index.html cannot load its modules.</p>'
                '<ol><li>Extract the complete ZIP.</li><li>Open a terminal in the extracted folder.</li>'
                '<li>Run <code>python3 serve.py --open</code> (Windows: <code>py serve.py --open</code>).</li></ol>'
                '<p>No Node installation, package download, or Forge login is needed to present. Keep the terminal open.</p>'
                + pdf_link + '</aside><script>if(location.protocol==="file:")document.getElementById("offline-help").hidden=false;</script>'
            )
            source = source.replace('<div id="app"></div>', '<div id="app"></div>' + help_panel)
        index.write_text(source, encoding="utf-8")
    if offline:
        if pdf:
            shutil.copyfile(pdf, directory / "deck.pdf")
        shutil.copyfile(ROOT / "scripts/serve_deck.py", directory / "serve.py")
        launcher = directory / "start.command"
        launcher.write_text('#!/bin/sh\ncd "$(dirname "$0")" || exit 1\npython3 serve.py --open\n', encoding="utf-8")
        launcher.chmod(0o755)
        (directory / "start.cmd").write_text('@echo off\r\ncd /d "%~dp0"\r\npy serve.py --open\r\npause\r\n', encoding="utf-8")
        (directory / "README.txt").write_text(
            f"{title}\n\nExtract the complete ZIP first.\n"
            "Interactive deck: python3 serve.py --open (Windows: py serve.py --open).\n"
            "The server chooses a free port, binds only to this laptop, and opens slide 1.\n"
            "Keep the terminal open; Ctrl-C stops it. No Node or network connection is required.\n"
            "You can also run start.command on macOS or start.cmd on Windows.\n"
            + ("For a file-only presentation, open deck.pdf.\n" if pdf else "This build has no PDF. Download the separate deck PDF for file-only presentation.\n")
            + "Arrow keys change slides and reveals. Press P for presenter view.\n"
            "External Forge/source links need internet and the viewer's usual access.\n"
            "Opening the deck starts no inference or training.\n", encoding="utf-8")


def write_library_index(directory, available):
    catalog_path = ROOT / "reports/published.json"
    reports = json.loads(catalog_path.read_text(encoding="utf-8"))["reports"] if catalog_path.exists() else {}
    shutil.copytree(ROOT / "skills/teenage-engineering-visualizations/assets/fonts", directory / "fonts", dirs_exist_ok=True)
    tokens = json.loads((ROOT / "skills/teenage-engineering-visualizations/assets/tokens.json").read_text(encoding="utf-8"))["colors"]
    write_walkthrough_page(directory, tokens)
    video_release = "walkthrough/media"
    links = []
    for row in available:
        slug = row["slug"]
        report = reports.get("airline" if slug == "airline_monitoring" else slug)
        actions = f'<a href="{html.escape(slug)}/">Deck</a>'
        actions += f' · <a href="https://ash0ts.github.io/forge-workshop-kit/packet/docs/run-{slug}.html">How to run this workshop</a>'
        if report:
            actions = (f'<a href="{html.escape(report["url"], quote=True)}">Read the learning Report</a> · '
                       + actions + f' · <a href="packet/start/{slug}.html">Start the notebook</a>')
            if hosted_url := report.get("hosted_notebook_url"):
                actions += (f' · <a href="{html.escape(hosted_url, quote=True)}">Forge template</a>'
                            f' (<a href="packet/start/{slug}.html#forge-copy">copy instructions and access status</a>)')
        stem = DECKS[slug]["filename"]
        downloads = [(f'{stem}.pdf', 'Deck PDF'), (f'{stem}-browser.zip', 'Offline deck'), (f'{stem}-source.zip', 'Editable source')]
        deck_downloads = ' · '.join(
            f'<a href="{html.escape(slug)}/{html.escape(filename)}">{label}</a>'
            for filename, label in downloads if (directory / slug / filename).exists()
        )
        poster = json.loads((ROOT / "visual-guides" / slug / "poster.json").read_text(encoding="utf-8"))["poster"]
        poster_png = next((directory / "posters" / slug / "digital").glob("*.png"), None)
        links.append(f'<article id="{html.escape(slug)}"><a class="preview" href="posters/{slug}/digital/index.html">'
                     f'<img loading="lazy" width="1200" height="1500" src="posters/{slug}/digital/final.svg" alt="Overview poster: {html.escape(row["title"], quote=True)}"></a>'
                     f'<div><p class="number">{len(links)+1:02d} / {html.escape(poster["duration"])}</p>'
                     f'<h2>{html.escape(row["title"])}</h2><p>{html.escape(poster["situation"])}</p>'
                     f'<p>{actions}</p><p>{deck_downloads}</p><p><a href="posters/{slug}/digital/index.html">View poster</a> · '
                     f'<a href="posters/{slug}/print/final.svg" download>A2 SVG</a>'
                     + (f' · <a href="posters/{slug}/digital/{poster_png.name}" download>Digital PNG</a>' if poster_png else '')
                     + (f' · <a href="posters/{slug}/print/print.pdf">A2 PDF</a>' if (directory / "posters" / slug / "print/print.pdf").exists() else '')
                     + '</p></div></article>')
    (directory / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Forge Workshop Kit</title><style>'
        '@font-face{font-family:"IBM Plex Sans";src:url("fonts/ibm-plex-sans-latin-400-normal.woff2");font-weight:400}'
        '@font-face{font-family:"IBM Plex Sans";src:url("fonts/ibm-plex-sans-latin-600-normal.woff2");font-weight:600}'
        '@font-face{font-family:"IBM Plex Mono";src:url("fonts/ibm-plex-mono-latin-400-normal.woff2");font-weight:400}'
        f':root{{--paper:{tokens["paper"]};--ink:{tokens["ink"]};--line:{tokens["line"]};--accent:{tokens["accent"]}}}'
        'body{font:19px/1.5 "IBM Plex Sans",system-ui;max-width:1120px;'
        'margin:3rem auto;padding:0 1.5rem;color:var(--ink);background:var(--paper)}'
        'h1{font-size:clamp(36px,6vw,68px);font-weight:500;line-height:1.05;letter-spacing:-.04em}'
        'h2{font-size:28px;line-height:1.15;font-weight:500}a{color:inherit;text-underline-offset:4px}'
        'a:focus-visible,video:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:4px}'
        'article{display:grid;grid-template-columns:minmax(240px,1fr) 1fr;gap:40px;padding:36px 0;border-top:1px solid var(--line);scroll-margin-top:24px}'
        'article img{width:100%;height:auto;display:block}.number{font:14px "IBM Plex Mono",monospace;letter-spacing:.04em}'
        'header{margin-bottom:36px}header>p{max-width:880px}.tour{margin:28px 0 20px}'
        'video{width:100%;height:auto;aspect-ratio:16/9;display:block;background:#202220}'
        'figcaption{font-size:16px;margin-top:10px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}'
        'details{font-size:17px;padding:14px 0}summary{cursor:pointer}'
        'footer{border-top:1px solid var(--line);padding-top:24px}'
        '@media(max-width:650px){article{grid-template-columns:1fr;gap:8px}body{margin:2rem auto}}'
        '</style><header><p class="number">FORGE / WORKSHOP KIT</p>'
        '<h1>Forge Workshop Kit</h1><p>Six Python workshops follow an agent or model through a concrete job: '
        'handling a refund, forecasting solar activity, routing a support request, finding a defective board, '
        'building a departure app, or changing a booking. Each pairs editable code with the Forge records used to check its result.</p>'
        '<p>Read a worked example, try a short demo, or teach a full session.</p>'
        '<figure class="tour"><video controls playsinline preload="metadata" '
        f'poster="{video_release}/poster.png" aria-label="Ten-minute captioned tour of all six workshops">'
        f'<source src="{video_release}/forge-workshops-narrated-captioned.mp4" type="video/mp4">'
        '<a href="walkthrough/">Watch or download the workshop tour</a></video>'
        '<figcaption><span>10 minutes · Narrated · Captioned</span>'
        '<a href="walkthrough/">Full tour, downloads, and transcript</a></figcaption></figure>'
        '<p><a href="packet/docs/setup.html">Set up your notebook</a> · '
        '<a href="packet/workshop-materials.zip" download>Download all workshop materials</a> · '
        '<a href="packet/docs/recorded-results.html">Read the recorded results</a></p>'
        '<p><a href="packet/docs/facilitator-start.html">Facilitate a workshop</a> · '
        '<a href="packet/docs/use-the-workshops.html">Choose a workshop for your team</a> · '
        '<a href="visual-language/">Explore the workshop diagrams</a></p>'
        '<details><summary>Notebook options and session readiness</summary>'
        '<p>Get the current notebook from its start page and run it locally with your own Forge project. '
        'Each workshop also links its Forge template. Those templates remain on v0.11.1; '
        'the latest access check was blocked, so hosted copying is not yet verified. '
        'The start page explains Copy to project and provides the current download with direct ARIA controls. '
        'Read-only examples are free to browse; running exercises uses your own inference and compute access.</p>'
        '<p>The full sessions remain technical previews while external-account and participant rehearsals are completed. '
        '<a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/next-up.md">Read the current checks and limitations</a>.</p>'
        '</details></header>'
        f'<main>{"".join(links)}</main>'
        '<footer><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/setup.md">Setup instructions</a> · '
        '<a href="https://github.com/ash0ts/forge-workshop-kit">Source and contributor guide</a> · '
        '<a href="share/">Share a workshop</a> · '
        '<a href="visual-language/">Workshop diagrams</a></footer></html>',
        encoding="utf-8",
    )


def write_walkthrough_page(directory, tokens):
    """Show the finished edit, its transcript, and reusable production instructions."""
    destination = directory / "walkthrough"
    destination.mkdir(parents=True, exist_ok=True)
    edit = json.loads((ROOT / "media/walkthrough/edit.json").read_text(encoding="utf-8"))
    chapters, at = [], 0
    for chapter in edit["chapters"]:
        paragraphs = "".join(f'<p>{html.escape(text)}</p>' for shot in chapter["shots"] for text in shot["narration"])
        chapters.append(f'<section id="{html.escape(chapter["id"], quote=True)}"><h2><button type="button" data-time="{at}" aria-label="Play {html.escape(chapter["title"], quote=True)}">'
                        f'{at // 60}:{at % 60:02} · {html.escape(chapter["title"])}</button></h2>{paragraphs}</section>')
        at += chapter["duration"]
    (destination / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Watch the workshop tour · Forge Workshop Kit</title><style>'
        '@font-face{font-family:"IBM Plex Sans";src:url("../fonts/ibm-plex-sans-latin-400-normal.woff2");font-weight:400}'
        '@font-face{font-family:"IBM Plex Mono";src:url("../fonts/ibm-plex-mono-latin-400-normal.woff2");font-weight:400}'
        f':root{{--paper:{tokens["paper"]};--ink:{tokens["ink"]};--line:{tokens["line"]};--accent:{tokens["accent"]}}}'
        'body{font:19px/1.5 "IBM Plex Sans",system-ui;max-width:1120px;margin:3rem auto;padding:0 1.5rem;'
        'color:var(--ink);background:var(--paper)}h1{font-size:clamp(32px,5vw,58px);line-height:1.1;font-weight:500}'
        'a{color:inherit;text-underline-offset:4px}a:focus-visible,video:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:4px}'
        '.number{font:14px "IBM Plex Mono",monospace}video{width:100%;height:auto;aspect-ratio:16/9;background:#202220;display:block}'
        '.downloads,section{border-top:1px solid var(--line);padding-top:20px}p{max-width:850px}'
        'button{font:inherit;text-align:left;color:inherit;border:0;background:none;text-decoration:underline;cursor:pointer;padding:0}'
        'h2{font-size:26px;font-weight:500}.note{font-size:16px}'
        '@media(max-width:650px){body{margin:2rem auto}}</style>'
        '<p class="number"><a href="../">FORGE / WORKSHOP KIT</a></p><h1>Watch the workshop tour</h1>'
        '<p>Follow six practical problems through the participant code, the result, and the Forge record used to check it. '
        'The ten-minute tour shows saved executions and controlled teaching examples.</p>'
        '<video controls playsinline preload="metadata" poster="media/poster.png" aria-label="Narrated and captioned workshop tour">'
        '<source src="media/forge-workshops-narrated-captioned.mp4" type="video/mp4">'
        'Your browser cannot play this video. <a href="media/forge-workshops-narrated-captioned.mp4">Download the MP4</a>.'
        '</video><p class="note">AI narration: Adam – Articulate Engineering Professor, generated with ElevenLabs. '
        'Captions follow the spoken words. The original silent edit remains available.</p>'
        '<p class="downloads">'
        '<a href="media/forge-workshops-narrated-captioned.mp4" download>Download narrated video</a> · '
        '<a href="media/forge-workshops-narrated-clean.mp4" download>Video without burned-in captions</a> · '
        '<a href="media/forge-workshops-narrated.srt" download>Timed captions (SRT)</a> · '
        '<a href="media/forge-workshops-narrated.vtt" download>Web captions (VTT)</a> · '
        '<a href="media/forge-workshops-audio-assets.zip" download>Reusable narration and sounds</a> · '
        '<a href="media/forge-workshops-video-edit.zip" download>Editable video package</a> · '
        '<a href="https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-captioned.mp4">Original silent video</a> · '
        '<a href="#transcript">Read the transcript</a></p>'
        '<p>Running a session? Start with the <a href="../packet/docs/facilitator-start.html">facilitator guide</a>. '
        'To record another workshop, follow the <a href="../packet/docs/video-production.html">video and narration workflow</a>. '
        'It covers screen capture, timed voice-over, captions, sound levels, and publishing.</p>'
        '<h2 id="transcript">Transcript and chapters</h2><p>Choose a chapter heading to play from that point.</p>'
        + "".join(chapters) +
        '<p><a href="../">Choose a workshop</a></p><script>'
        'document.querySelectorAll("button[data-time]").forEach(button=>button.addEventListener("click",()=>{'
        'const video=document.querySelector("video");video.currentTime=Number(button.dataset.time);'
        'video.play().catch(()=>{});video.scrollIntoView({block:"center",behavior:"auto"});}));'
        '</script></html>', encoding="utf-8")


def build(slug, output, *, install=False, pdf=False, validate=False):
    deck = ROOT / "decks" / slug
    settings = DECKS[slug]
    cli = ROOT / "decks/node_modules/@slidev/cli/bin/slidev.mjs"
    if install:
        install_toolchain()
    if not cli.exists():
        raise SystemExit("Missing shared Slidev dependencies. Run with --install first.")
    base = f"/forge-workshop-kit/{slug}/"
    site = output / "site" / slug
    local = output / "browser" / slug
    downloads = output / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    generator = deck / "scripts/build-storyboard.py"
    # Only clear generated deck directories, never notebooks, evidence or release assets.
    for directory in (site, local):
        if directory.exists():
            shutil.rmtree(directory)
    try:
        run([sys.executable, str(generator)], deck, {**os.environ, "DECK_BASE": base})
        run(["node", str(cli), "build", "--base", base, "--out", str(site)], deck)
        layout = json.loads((deck / "notes/slide-map.json").read_text(encoding='utf-8'))
        write_routes(site, layout, base)
    finally:
        run([sys.executable, str(generator)], deck, {**os.environ, "DECK_BASE": ""})
    run(["node", str(cli), "build", "--out", str(local)], deck)
    write_routes(local, layout, "/")
    prepare_browser_files(site, settings["title"])
    if validate:
        run(["node", str(ROOT / "scripts/validate_deck.mjs"), str(deck), str(site), base], ROOT)
    if pdf:
        target = downloads / f"{settings['filename']}.pdf"
        args = [
            "node",
            str(cli),
            "export",
            "--output",
            str(target),
            "--with-clicks",
            "--wait",
            "2000",
        ]
        if os.environ.get("CHROME_PATH"):
            args += ["--executable-path", os.environ["CHROME_PATH"]]
        run(args, deck)
        run(
            [
                "uv",
                "run",
                "--no-project",
                "--with",
                "pymupdf==1.26.6",
                "--with",
                "pillow==12.0.0",
                "python",
                str(ROOT / "scripts/check_deck_pdf.py"),
                str(deck),
                str(target),
                base,
            ],
            ROOT,
        )
        shutil.copyfile(target, site / target.name)
    prepare_browser_files(local, settings["title"], offline=True, pdf=target if pdf else None)
    from check_deck_assets import check as check_assets
    for directory, prefix in ((site, base), (local, "/")):
        receipt = check_assets(deck, directory, prefix)
        (directory / "asset-check.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        if receipt["missing"] or receipt["remote_render_dependencies"]:
            raise RuntimeError(f"Deck assets are not self-contained: {receipt}")
    archive(downloads / f"{settings['filename']}-browser.zip", local, [local])
    source_archive(downloads / f"{settings['filename']}-source.zip", deck, slug)
    for file in downloads.glob(f"{settings['filename']}-*.zip"):
        shutil.copyfile(file, site / file.name)
    return {
        "slug": slug,
        "title": settings["title"],
        "slides": layout["total_slides"],
        "base": base,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=DECKS, action="append")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/decks")
    parser.add_argument(
        "--install", action="store_true", help="Install the shared locked Slidev toolchain once"
    )
    parser.add_argument(
        "--pdf", action="store_true", help="Export and render every PDF page; requires Chrome"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Check every slide, route, image and answer link"
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if args.install:
        install_toolchain()
        # Every poster includes a real QR code, including SVG-only builds.
        run(["npm", "ci"], ROOT / "skills/teenage-engineering-visualizations",
            {**os.environ, "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD": "1"})
    from build_share_links import build as build_sharing
    build_sharing(site=output / "site")
    from build_visual_guides import build as build_guides
    build_guides(only=args.only or (), exports=args.pdf, site=output / "site")
    rows = [
        build(slug, output, pdf=args.pdf, validate=args.validate)
        for slug in (args.only or DECKS)
    ]
    available = [
        {"slug": slug, "title": settings["title"]}
        for slug, settings in DECKS.items()
        if (output / "site" / slug / "index.html").exists()
    ]
    write_library_index(output / "site", available)
    # A one-deck source bundle remains self-contained and does not need the
    # complete workshop catalog. The public all-deck build also emits the packet.
    if not args.only:
        from build_share_packet import build as build_packet
        build_packet(output / "site", pdf=args.pdf)
    (output / "site/.nojekyll").touch()
    files = [
        {
            "file": str(file.relative_to(output)),
            "bytes": file.stat().st_size,
            "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
        }
        for file in sorted((output / "downloads").glob("*"))
        if file.is_file()
    ]
    (output / "build-manifest.json").write_text(
        json.dumps(
            {"built_decks": rows, "available_decks": available, "downloads": files}, indent=2
        )
        + "\n", encoding='utf-8'
    )
    print(f"Built {len(rows)} decks in {output}. Nothing was published.")


if __name__ == "__main__":
    main()
