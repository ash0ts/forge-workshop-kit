"""Build workshop decks and downloads. Never publish or execute a workshop."""

import argparse
import hashlib
import html
import json
import os
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
        for name in ("build_decks.py", "build_visual_guides.py", "technical_guide_storyboard.py", "scene_storyboard.py", "share_storyboard.py", "build_share_links.py", "render_share_qr.mjs", "validate_deck.mjs", "check_deck_pdf.py", "serve_deck.py", "aria_storyboard.py"):
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


def write_library_index(directory, available):
    catalog_path = ROOT / "reports/published.json"
    reports = json.loads(catalog_path.read_text(encoding="utf-8"))["reports"] if catalog_path.exists() else {}
    shutil.copytree(ROOT / "skills/teenage-engineering-visualizations/assets/fonts", directory / "fonts", dirs_exist_ok=True)
    tokens = json.loads((ROOT / "skills/teenage-engineering-visualizations/assets/tokens.json").read_text(encoding="utf-8"))["colors"]
    links = []
    for row in available:
        slug = row["slug"]
        report = reports.get("airline" if slug == "airline_monitoring" else slug)
        actions = f'<a href="{html.escape(slug)}/">Deck</a>'
        actions += f' · <a href="https://ash0ts.github.io/forge-workshop-kit/packet/docs/run-{slug}.html">How to run this workshop</a>'
        if report:
            actions = (f'<a href="{html.escape(report["url"], quote=True)}">Read the learning Report</a> · '
                       + actions + f' · <a href="{html.escape(report["notebook_url"], quote=True)}">Notebook · Forge sign-in</a>')
        stem = DECKS[slug]["filename"]
        downloads = [(f'{stem}.pdf', 'Deck PDF'), (f'{stem}-browser.zip', 'Offline deck'), (f'{stem}-source.zip', 'Editable source')]
        deck_downloads = ' · '.join(
            f'<a href="{html.escape(slug)}/{html.escape(filename)}">{label}</a>'
            for filename, label in downloads if (directory / slug / filename).exists()
        )
        poster = json.loads((ROOT / "visual-guides" / slug / "poster.json").read_text(encoding="utf-8"))["poster"]
        poster_png = next((directory / "posters" / slug / "digital").glob("*.png"), None)
        links.append(f'<article id="{html.escape(slug)}"><a class="preview" href="posters/{slug}/digital/index.html">'
                     f'<img loading="lazy" src="posters/{slug}/digital/final.svg" alt="Overview poster: {html.escape(row["title"], quote=True)}"></a>'
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
        'a:focus-visible{outline:3px solid var(--accent);outline-offset:4px}'
        'article{display:grid;grid-template-columns:minmax(240px,1fr) 1fr;gap:40px;padding:36px 0;border-top:1px solid var(--line);scroll-margin-top:24px}'
        'article img{width:100%;display:block}.number{font:14px "IBM Plex Mono",monospace;letter-spacing:.04em}'
        'header{max-width:850px;margin-bottom:48px}footer{border-top:1px solid var(--line);padding-top:24px}'
        '@media(max-width:650px){article{grid-template-columns:1fr;gap:8px}body{margin:2rem auto}}'
        '</style><header><p class="number">FORGE / WORKSHOP KIT</p>'
        '<h1>Forge Workshop Kit</h1><p>Six Python workshops for building and testing agents, models, and software. '
        'Start with a worked example in the Report, '
        'then copy its notebook into your own Forge project to change the code and run the exercises.</p>'
        '<p>These are technical previews. You can read the recorded results without running an experiment. '
        'Notebook execution uses your own project access and billing.</p>'
        '<p><a href="https://ash0ts.github.io/forge-workshop-kit/packet/">Meeting packet, demo routes, and Slack copy</a> · '
        '<a href="https://ash0ts.github.io/forge-workshop-kit/packet/workshop-meeting-packet.zip">Download the packet</a></p>'
        '<p><a href="https://ash0ts.github.io/forge-workshop-kit/packet/docs/facilitator-start.html">Facilitator start guide</a> · '
        '<a href="https://ash0ts.github.io/forge-workshop-kit/share/">QR codes and tracked sharing links</a></p>'
        '<p><a href="visual-language/">Explore the visual guide templates</a> · '
        '<a href="downloads/workshop-posters.zip">Download all six posters</a></p></header>'
        f'<main>{"".join(links)}</main>'
        '<footer><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/setup.md">Setup instructions</a> · '
        '<a href="https://github.com/ash0ts/forge-workshop-kit">Source and contributor guide</a> · '
        '<a href="downloads/teenage-engineering-visualizations.zip">Standalone visualization skill</a></footer></html>',
        encoding="utf-8",
    )


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
    shutil.copyfile(ROOT / "scripts/serve_deck.py", local / "serve.py")
    (local / "README.txt").write_text(
        f"{settings['title']}\n\nRun python3 serve.py (Windows: py serve.py).\n"
        "Open the local address printed by the server. Presenter notes: /presenter/1.\n"
        "Arrow keys change slides. Worked-answer links return to the exercise.\n\n"
        "Opening this deck sends no inference or training requests. Forge links use your account.\n", encoding='utf-8'
    )
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
