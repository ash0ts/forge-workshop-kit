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
        for name in ("build_decks.py", "validate_deck.mjs", "check_deck_pdf.py", "serve_deck.py", "aria_storyboard.py"):
            bundle.write(ROOT / "scripts" / name, Path("scripts") / name)
        for name in ("README.md", "package.json", "package-lock.json", "scripts/deck.mjs", "aria.css"):
            bundle.write(ROOT / "decks" / name, Path("decks") / name)
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
    rows = [
        build(slug, output, pdf=args.pdf, validate=args.validate)
        for slug in (args.only or DECKS)
    ]
    available = [
        {"slug": slug, "title": settings["title"]}
        for slug, settings in DECKS.items()
        if (output / "site" / slug / "index.html").exists()
    ]
    links = "".join(f'<li><a href="{row["slug"]}/">{row["title"]}</a></li>' for row in available)
    (output / "site/index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Forge Workshop Kit decks</title><style>body{font:20px system-ui;max-width:48rem;"
        "margin:4rem auto;padding:0 1.5rem;color:#163c43;background:#faf7ee}li{margin:1rem 0}"
        "a{color:#146965}</style><h1>Forge Workshop Kit</h1>"
        f"<p>Choose the deck for your notebook.</p><ul>{links}</ul>"
        '<p><a href="https://github.com/ash0ts/forge-workshop-kit">Notebooks and setup instructions</a></p></html>', encoding='utf-8'
    )
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
