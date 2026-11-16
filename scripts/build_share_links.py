"""Build QR codes from registered UTM.io links, without network calls."""

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = "https://ash0ts.github.io/forge-workshop-kit"
MANIFEST = ROOT / "docs/share-links.json"
WORKSHOPS = ("pending", "solar", "routing", "inspection", "transit", "airline_monitoring")
COLLECTION_LINKS = {
    "packet": {"source": "slack", "medium": "social", "content": "workshop-library",
               "title": "All six workshops · Community Slack",
               "placement": "Use when sharing with prospective participants in an external Slack community. For coworkers, use the untracked library address."},
    "loom": {"source": "loom", "medium": "video", "content": "kit-walkthrough",
             "title": "All six workshops · Loom",
             "placement": "Use in the Loom description and closing screen."},
}


def load_links(path=MANIFEST):
    """Reject inconsistent destinations before replacing any shared QR assets."""
    manifest = json.loads(Path(path).read_text())
    campaign = manifest.get("campaign")
    if not isinstance(campaign, str) or not campaign.strip():
        raise ValueError("share-links.json must name the registered UTM.io campaign")
    links = manifest.get("links", {})
    expected = {*WORKSHOPS, *COLLECTION_LINKS}
    if set(links) != expected:
        raise ValueError(f"Expected exactly these share links: {sorted(expected)}")
    short_urls = set()
    for slug, row in links.items():
        short = urlsplit(row["short_url"])
        if (short.scheme != "https" or short.netloc != "utm.io" or
                not short.path.strip("/") or short.query or short.fragment):
            raise ValueError(f"{slug}: short_url must be a registered HTTPS utm.io link without added parameters")
        if row["short_url"] in short_urls:
            raise ValueError(f"{slug}: each resource needs its own registered short URL")
        short_urls.add(row["short_url"])
        destination = urlsplit(row["url"])
        collection = COLLECTION_LINKS.get(slug)
        expected_path = "/forge-workshop-kit/" if collection else f"/forge-workshop-kit/packet/start/{slug}.html"
        if (destination.scheme, destination.netloc, destination.path) != (
            "https", "ash0ts.github.io", expected_path
        ):
            raise ValueError(f"{slug}: destination must be its public library or notebook start page")
        parameters = {
            "utm_source": [collection["source"] if collection else "forge-workshop-kit"],
            "utm_medium": [collection["medium"] if collection else "workshop"],
            "utm_campaign": [campaign],
            "utm_content": [collection["content"] if collection else f"{slug}-start"],
        }
        if parse_qs(destination.query, keep_blank_values=True) != parameters:
            raise ValueError(f"{slug}: UTM values differ from the sharing convention")
        if destination.fragment:
            raise ValueError(f"{slug}: start pages do not use workshop fragments")
    return manifest


def build(site=None):
    manifest = load_links(ROOT / "docs/share-links.json")
    links = manifest["links"]
    templates = json.loads((ROOT / "src/forge_workshop_kit/workshops.json").read_text())["templates"]
    titles = {row["authoring"]["deck"]["directory"]: row["authoring"]["deck"]["title"]
              for row in templates if row.get("authoring", {}).get("deck")}
    titles.update({slug: row["title"] for slug, row in COLLECTION_LINKS.items()})
    available = [slug for slug in WORKSHOPS if slug in titles]
    requests = []
    for slug in available:
        requests.append({"url": links[slug]["short_url"], "title": f"Open {titles[slug]}",
                         "svg": str(ROOT / "decks" / slug / "public/images/workshop-qr.svg")})
    target = Path(site).resolve() / "share" if site else None
    if target:
        for slug in (*available, *COLLECTION_LINKS):
            row = links[slug]
            requests.append({"url": row["short_url"], "title": f"Open {titles[slug]}",
                             "svg": str(target / f"{slug}.svg"), "png": str(target / f"{slug}.png")})
    subprocess.run(["node", str(ROOT / "scripts/render_share_qr.mjs")],
                   input=json.dumps(requests), text=True, check=True)
    for slug in available:
        path = ROOT / "visual-guides" / slug / "poster.json"
        poster = json.loads(path.read_text())
        poster["poster"]["cta"].update({"url": links[slug]["short_url"],
                                           "display_url": links[slug]["short_url"].removeprefix("https://")})
        path.write_text(json.dumps(poster, indent=2, ensure_ascii=False) + "\n")
    if target:
        write_page(target, manifest, titles)
    return manifest


def write_page(target, manifest, titles):
    shutil.copyfile(ROOT / "decks/share-packet.css", target / "packet.css")
    fonts = target / "fonts"
    fonts.mkdir(exist_ok=True)
    for source in (ROOT / "skills/teenage-engineering-visualizations/assets/fonts").iterdir():
        if source.is_file():
            shutil.copyfile(source, fonts / source.name)
    cards = []
    for slug in (*COLLECTION_LINKS, *[slug for slug in WORKSHOPS if slug in titles]):
        row = manifest["links"][slug]
        short = html.escape(row["short_url"], quote=True)
        placement = COLLECTION_LINKS.get(slug, {}).get("placement", "Use in this workshop’s deck, poster, or invitation.")
        cards.append(
            f'<article id="{slug}"><div class="card-body"><h2>{html.escape(titles[slug])}</h2>'
            f'<p>{html.escape(placement)}</p>'
            f'<a href="{short}"><img class="qr" src="{slug}.svg" width="240" height="240" '
            f'alt="QR code opening {html.escape(titles[slug], quote=True)}"></a>'
            f'<p><a href="{short}">{short}</a></p><div class="actions">'
            f'<a href="{slug}.png" download>Download PNG</a>'
            f'<a href="{slug}.svg" download>Download editable SVG</a></div></div></article>'
        )
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Share a Forge workshop</title><link rel="stylesheet" href="packet.css">'
        '<style>.qr{width:240px;max-width:100%;height:auto;margin:20px 0;border:0}'
        '.card-body h2{font-size:26px;margin:0}</style></head><body>'
        '<a class="skip" href="#main">Skip to content</a><main id="main">'
        '<nav><a href="../">Workshop library</a> · '
        '<a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/share-links.md">Sharing instructions</a></nav>'
        '<header><p class="eyebrow">FORGE WORKSHOP KIT · SHARING LINKS</p>'
        '<h1>Choose a workshop and share its link</h1>'
        '<p>Choose the community Slack or video link for an introduction to the collection. '
        'Use a workshop link when inviting people to a specific session. Each opens its '
        'public introduction, deck, setup instructions, and notebook start page. '
        'For internal discussions, use the <a href="../">untracked library address</a>.</p>'
        '<p>Download the PNG for a message or the SVG for a slide or printed handout. '
        'Keep the white border around the QR code and include the written link.</p></header>'
        f'<section class="catalog" aria-label="Workshop sharing codes">{"".join(cards)}</section>'
        '<footer><p>These links are registered in UTM.io. A workshop uses the same link in '
        'its deck and poster, so the counts do not distinguish those surfaces. Verification '
        'clicks, link previews, and repeat visits are not attendee counts. UTM parameters '
        'identify the incoming link; they do not record notebook copies or completed exercises.</p>'
        '<p>Opening the introduction needs no Forge account. Copying and running a notebook '
        'requires the participant’s own project and access. '
        '<a href="../packet/docs/next-up.html">Read the current readiness notes</a>.</p></footer>'
        '</main></body></html>'
    )
    (target / "index.html").write_text(document)
    (target / "links.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, help="Also write share/ HTML, SVGs, and PNGs below this site root")
    parser.add_argument("--check", action="store_true", help="Validate the manifest without writing files")
    args = parser.parse_args()
    result = load_links() if args.check else build(args.site)
    print(f"{'Validated' if args.check else 'Built'} {len(result['links'])} registered sharing links")
