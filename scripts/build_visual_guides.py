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
ILLUSTRATORS = {"pending": "pending", "solar": "solar", "routing": "routing",
                "inspection": "inspection", "transit": "transit", "airline_monitoring": "airline"}

# Each preview follows an object from the corresponding workshop. The full
# sequence supplies intermediate states, code, and source links.
GUIDE_LEADS = {
    "pending": ("dispatch", "Pending, Inc.",
                "How does an agent use the result of a tool call?",
                "Follow the account and invoice IDs into Python, then find the returned payments in the next model request."),
    "solar": ("window", "Solar forecasting",
              "What can the forecast know at this timestamp?",
              "Locate the observed hour, the latest reading, and the target 30 minutes ahead. Then follow the values into the model."),
    "routing": ("release", "Customer request routing",
                "How can the same scores send a request to the wrong queue?",
                "Keep the probability columns fixed and watch what happens when a release loads the intent names in a different order."),
    "inspection": ("patch-distance", "Circuit-board inspection",
                   "What does one image patch contribute to the detector?",
                   "Compare a patch with normal reference patches, calculate its distance, and locate that value in the classifier input."),
    "transit": ("claims", "Coding agents building a departure board",
                "What stops two workers from taking the same task?",
                "Follow both claim attempts into one task record. The ownership check must happen together with the write."),
    "airline_monitoring": ("itinerary", "Airline service monitoring",
                           "Why can changing an outbound flight erase the return trip?",
                           "The API replaces the whole itinerary. Compare a payload containing only the new flight with one that preserves the untouched segments."),
}


def write_guide_index(site: Path, index: dict):
    """Publish lesson explanations, keeping renderer examples out of the learner path."""
    gallery = Path(site) / "visual-language"
    gallery.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL / "assets/fonts", gallery / "fonts", dirs_exist_ok=True)
    colors = json.loads((SKILL / "assets/tokens.json").read_text(encoding="utf-8"))["colors"]
    public_site = "https://ash0ts.github.io/forge-workshop-kit/"
    library = "../" if (site / "index.html").is_file() else public_site
    tour = "../walkthrough/" if (site / "walkthrough/index.html").is_file() else public_site + "walkthrough/"
    navigation, sections = [], []
    for workshop in index["workshops"]:
        slug = workshop["slug"]
        lead, name, question, explanation = GUIDE_LEADS[slug]
        url = f"../guides/{slug}/{lead}/index.html"
        start = f"../packet/start/{slug}.html" if (site / "packet/start" / f"{slug}.html").is_file() else f"https://ash0ts.github.io/forge-workshop-kit/packet/start/{slug}.html"
        deck = f"../{slug}/" if (site / slug / "index.html").is_file() else f"https://ash0ts.github.io/forge-workshop-kit/{slug}/"
        navigation.append(f'<a href="#{slug}">{html.escape(name)}</a>')
        lessons = "".join(
            f'<li><a href="../guides/{slug}/{row["id"]}/index.html">{html.escape(row["title"])}</a></li>'
            for row in workshop["sequences"]
        )
        sections.append(
            f'<section id="{slug}" aria-labelledby="{slug}-title">'
            f'<p class="eyebrow">{len(sections)+1:02d} / {html.escape(name)}</p>'
            f'<h2 id="{slug}-title">{html.escape(question)}</h2><p>{html.escape(explanation)}</p>'
            f'<figure><a href="{url}" aria-label="Open the step-by-step explanation: {html.escape(question, quote=True)}">'
            f'<img loading="lazy" width="1200" height="675" src="../guides/{slug}/{lead}/final.svg" '
            f'alt="{html.escape(explanation, quote=True)}"></a>'
            '<figcaption>Follow the inputs, operation, and resulting state. '
            f'<a href="{url}">Open the steps and code</a></figcaption></figure>'
            f'<h3>Explore this workshop</h3><ul class="lessons">{lessons}</ul>'
            f'<p class="actions"><a href="{start}">Get the notebook</a> · '
            f'<a href="{deck}">Open the deck</a> · '
            f'<a href="{library}#{slug}">Report and recorded results</a></p></section>'
        )
    (gallery / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Workshop diagrams · Forge Workshop Kit</title><style>'
        '@font-face{font-family:Plex;src:url("fonts/ibm-plex-sans-latin-400-normal.woff2");font-weight:400}'
        '@font-face{font-family:Plex;src:url("fonts/ibm-plex-sans-latin-600-normal.woff2");font-weight:600}'
        '@font-face{font-family:PlexMono;src:url("fonts/ibm-plex-mono-latin-400-normal.woff2")}'
        f':root{{--paper:{colors["paper"]};--ink:{colors["ink"]};--line:{colors["line"]};--accent:{colors["accent"]}}}'
        'html{scroll-behavior:smooth}body{font:20px/1.5 Plex,sans-serif;background:var(--paper);color:var(--ink);'
        'max-width:1120px;margin:40px auto;padding:0 24px}a{color:inherit;text-underline-offset:4px}'
        'a:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:5px}'
        'h1{font-size:clamp(36px,5vw,58px);line-height:1.1;font-weight:600;letter-spacing:-.03em}'
        'h2{font-size:clamp(27px,3.2vw,38px);line-height:1.2;max-width:900px}h3{font-size:21px}'
        'header>p,section>p{max-width:870px}.eyebrow{font:14px/1.5 PlexMono,monospace}'
        'nav{display:flex;flex-wrap:wrap;gap:8px 24px;padding:20px 0 28px;font-size:17px}'
        'section{padding:40px 0;border-top:1px solid var(--line);scroll-margin-top:24px}'
        'figure{margin:28px 0}figure>a{display:block;border:1px solid var(--line)}img{display:block;width:100%;height:auto}'
        'figcaption{font-size:16px;margin-top:10px}.lessons{display:grid;grid-template-columns:1fr 1fr;gap:12px 32px;padding-left:24px}'
        '.actions{font-size:17px;margin-top:28px}footer{border-top:1px solid var(--line);padding:24px 0;font-size:17px}'
        'summary{cursor:pointer}.skip{position:absolute;left:-10000px}.skip:focus{position:static}'
        '@media(max-width:650px){body{margin:24px auto;padding:0 18px;font-size:18px}.lessons{grid-template-columns:1fr}section{padding:28px 0}}'
        '@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style></head><body>'
        '<a class="skip" href="#examples">Skip to the diagrams</a>'
        f'<header><p class="eyebrow"><a href="{library}">FORGE / WORKSHOP KIT</a></p>'
        '<h1>See what the code changes</h1>'
        '<p>Follow an invoice through an agent, a measurement into a forecast, or a flight into an updated booking. '
        'These diagrams explain the operations you implement in the workshops, one step at a time.</p>'
        '<p>Open an example and use Next and Back to compare its states. The accompanying code and source links '
        'show where each operation comes from. You can read every guide without signing in.</p>'
        f'<nav aria-label="Choose a workshop">{"".join(navigation)}</nav></header>'
        f'<main id="examples">{"".join(sections)}</main>'
        '<footer><details><summary>Use these drawings in your own teaching</summary>'
        '<p>The diagrams are shared by the notebooks and decks. '
        '<a href="../downloads/workshop-visual-source.zip">Download their editable sources</a>, or '
        '<a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/technical-visuals.md">read the authoring guide</a>. '
        'The <a href="../downloads/teenage-engineering-visualizations.zip">standalone visual skill</a> includes the renderer and reference examples.</p>'
        f'</details><p><a href="{library}">Workshop library</a> · <a href="{tour}">Watch the ten-minute tour</a></p></footer>'
        '</body></html>', encoding="utf-8")


def archive(destination, folders):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for folder, prefix in folders:
            if folder.is_file():
                entry = zipfile.ZipInfo(str(prefix), date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o644 << 16
                bundle.writestr(entry, folder.read_bytes())
                continue
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
    subprocess.run([sys.executable, str(ROOT / "scripts/illustrate_workshop_scenes.py")], check=True)
    receipts = []
    for workshop in selected:
        slug = workshop["slug"]
        # Illustrators consume checked-in observations and fixtures only. They
        # author SVG geometry; no workshop runtime or provider is imported.
        subprocess.run([sys.executable, str(ROOT / "scripts" / f"illustrate_{ILLUSTRATORS[slug]}.py")], check=True)
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
    # A partial build should not advertise guides it has not delivered. Keep
    # earlier workshops when building incrementally into an existing site.
    delivered_index = {**index, "workshops": [row for row in index["workshops"]
        if (site / "guides" / row["slug"] / GUIDE_LEADS[row["slug"]][0] / "index.html").is_file()]}
    write_guide_index(site, delivered_index)
    downloads = output / "downloads"
    archive(downloads / "teenage-engineering-visualizations.zip", [(SKILL, SKILL.name)])
    archive(downloads / "workshop-visual-source.zip", [(SOURCE, "visual-guides"),
        (SKILL, "skills/teenage-engineering-visualizations"),
        *[(path, Path("scripts") / path.name) for path in sorted((ROOT / "scripts").glob("illustrate_*.py"))]])
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
