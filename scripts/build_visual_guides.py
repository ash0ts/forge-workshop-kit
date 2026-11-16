"""Render shared technical guides and posters. No workshop execution or publication."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/teenage-engineering-visualizations"
SOURCE = ROOT / "visual-guides"
BUNDLED = ROOT / "src/forge_workshop_kit/assets/technical-guides"
EXCLUDED = {"node_modules", "__pycache__", ".DS_Store", ".git", ".venv", "dist"}


def archive(destination, folders):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for folder, prefix in folders:
            for path in sorted(folder.rglob("*")):
                relative = path.relative_to(folder)
                if path.is_file() and not EXCLUDED.intersection(relative.parts) and path.suffix != ".pyc":
                    entry = zipfile.ZipInfo(str(Path(prefix) / relative), date_time=(2026, 1, 1, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.external_attr = 0o644 << 16
                    bundle.writestr(entry, path.read_bytes())


def render(spec, destination, layout, exports=False):
    # These are generated figure directories, not source or participant work.
    # A reduced reveal count or SVG-only build must not retain stale exports.
    if destination.exists():
        shutil.rmtree(destination)
    subprocess.run([sys.executable, str(SKILL / "scripts/render.py"), str(spec),
                    "--output", str(destination), "--layout", layout,
                    "--formats", "svg,html,png,pdf" if exports else "svg,html"], check=True)


def build(*, only=(), exports=False, output=None, site=None):
    index = json.loads((SOURCE / "index.json").read_text(encoding="utf-8"))
    selected = [row for row in index["workshops"] if not only or row["slug"] in only]
    output = Path(output or ROOT / "dist/visual-guides").resolve()
    site = Path(site or ROOT / "dist/decks/site").resolve()
    BUNDLED.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / "index.json", BUNDLED / "index.json")
    shutil.copyfile(SKILL / "assets/tokens.json", BUNDLED / "tokens.json")
    receipts = []
    for workshop in selected:
        slug = workshop["slug"]
        for relative in [workshop["overview"], *[s["spec"] for s in workshop["sequences"]]]:
            spec = SOURCE / relative
            record = json.loads(spec.read_text(encoding="utf-8"))
            identifier = record["id"]
            if Path(identifier).name != identifier or identifier in {".", ".."}:
                raise ValueError(f"Invalid figure identity: {identifier}")
            destination = BUNDLED / slug / identifier
            for layout in ("notebook", "slide"):
                render(spec, destination / layout, layout)
            shutil.copyfile(spec, destination / "spec.json")
            deck = ROOT / "decks" / slug / "public/guides" / slug / identifier
            if deck.exists():
                shutil.rmtree(deck)
            shutil.copytree(destination / "slide", deck / "slide")
            shutil.copyfile(destination / "spec.json", deck / "spec.json")
            receipts.append({"workshop": slug, "id": identifier, "spec": relative,
                             "sha256": hashlib.sha256(spec.read_bytes()).hexdigest()})
        poster = SOURCE / workshop["poster"]
        for layout in ("digital", "print"):
            destination = output / "posters" / slug / layout
            render(poster, destination, layout, exports=exports)
            delivered = site / "posters" / slug / layout
            if delivered.exists():
                shutil.rmtree(delivered)
            shutil.copytree(destination, delivered)
        # Self-contained HTML guides make all reveal frames available without Forge.
        for row in receipts:
            if row["workshop"] == slug:
                source = BUNDLED / slug / row["id"] / "notebook"
                delivered = site / "guides" / slug / row["id"]
                if delivered.exists():
                    shutil.rmtree(delivered)
                shutil.copytree(source, delivered)
    examples = []
    for spec in sorted((SKILL / "examples").glob("*.json")):
        record = json.loads(spec.read_text(encoding="utf-8"))
        layout = "digital" if record["kind"] == "poster" else "slide"
        destination = output / "reference-gallery" / spec.stem
        render(spec, destination, layout, exports=exports)
        delivered = site / "visual-language" / spec.stem
        if delivered.exists():
            shutil.rmtree(delivered)
        shutil.copytree(destination, delivered)
        examples.append({"id": spec.stem, "title": record["title"]})
    cards = "".join(f'<li><a href="{html.escape(row["id"])}/index.html">'
                    f'<img src="{html.escape(row["id"])}/final.svg" alt="">'
                    f'{html.escape(row["title"])}</a></li>' for row in examples)
    gallery = site / "visual-language"
    gallery.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL / "assets/fonts", gallery / "fonts", dirs_exist_ok=True)
    colors = json.loads((SKILL / "assets/tokens.json").read_text(encoding="utf-8"))["colors"]
    (gallery / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Technical visual language</title><style>'
        '@font-face{font-family:Plex;src:url("fonts/ibm-plex-sans-latin-400-normal.woff2")}'
        f'body{{font:18px/1.5 Plex,sans-serif;background:{colors["paper"]};color:{colors["ink"]};'
        'max-width:1100px;margin:3rem auto;padding:0 1rem}ul{list-style:none;padding:0;'
        'display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}img{width:100%}'
        'a{color:inherit}a:focus-visible{outline:3px solid #d65321}</style>'
        '<h1>Technical visual language</h1><p>Six reusable compositions. These examples are illustrative; '
        'they are not workshop experiment results.</p><ul>' + cards + '</ul>'
        '<p><a href="../downloads/teenage-engineering-visualizations.zip">Download the standalone skill</a> · '
        '<a href="../">Workshop library</a></p></html>', encoding="utf-8")
    downloads = output / "downloads"
    archive(downloads / "teenage-engineering-visualizations.zip", [(SKILL, SKILL.name)])
    archive(downloads / "workshop-visual-source.zip", [(SOURCE, "visual-guides"), (SKILL, "skill")])
    archive(downloads / "workshop-posters.zip", [(output / "posters", "posters")])
    shutil.copytree(downloads, site / "downloads", dirs_exist_ok=True)
    receipt = {"schema_version": 1, "figures": receipts, "exports_requested": exports,
               "examples": examples, "training_requests": 0, "inference_requests": 0}
    output.mkdir(parents=True, exist_ok=True)
    (output / "build-manifest.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(receipts)} workshop figures, {len(selected)} posters, and {len(examples)} reference examples.")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--exports", action="store_true", help="Also render PNG and vector PDF outputs")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    build(only=args.only, exports=args.exports, output=args.output, site=args.site)


if __name__ == "__main__":
    main()
