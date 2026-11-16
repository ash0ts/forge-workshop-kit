"""Put the managed workshop link beside setup and the take-home handoff."""
from __future__ import annotations

from copy import deepcopy
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "pending": ("copy", "end", True),
    "solar": ("copy", "close", True),
    "routing": ("connect", "close", False),
    "inspection": ("connect", "conclusion", False),
    "transit": ("connect-and-inspect-the-source-data", "take-the-coordination-code-to-your-own-project", False),
    "airline_monitoring": ("setup", "end", True),
}


def _key(row):
    return row.get("key") or row.get("name") or re.sub(
        r"[^a-z0-9]+", "-", row["title"].replace("<br>", " ").lower()
    ).strip("-")


def _body(url, *, closing, workshop):
    label = escape(url.removeprefix("https://"))
    url = escape(url, quote=True)
    if closing:
        instructions = (
            "<p>Return to your saved notebook copy to continue your work.</p>"
            "<ol><li><strong>Revisit the example.</strong> The Report links its claims to recorded results.</li>"
            "<li><strong>Keep the materials.</strong> Open the deck, download the PDF, or get the source.</li>"
            "<li><strong>Run a session.</strong> Use the short run guide and facilitator notes.</li></ol>"
        )
        footer = "The shared page has the template and references. Your executions remain in your own project."
    else:
        instructions = (
            "<ol><li><strong>Open this workshop’s page.</strong> Scan the code or type the short link.</li>"
            "<li><strong>Choose the notebook.</strong> Sign in to Forge, then choose <strong>Copy to project</strong>.</li>"
            "<li><strong>Open your copy in Edit.</strong> Run all stale cells once to initialize the controls.</li>"
            "<li><strong>Check the destination.</strong> Use your own writable project and account.</li></ol>"
        )
        footer = (
            "The first exercise follows. Opening the copy does not start training or inference."
            if workshop == "inspection" else
            "The $8 adjustable allowance covers notebook inference. Notebook compute is billed separately."
        )
        if workshop == "airline_monitoring":
            footer += " Native tag judging has separate charges."
    return (
        '<div class="workshop-share-layout"><div class="workshop-share-instructions">'
        + instructions
        + '</div><div class="workshop-share-code"><a href="' + url
        + '" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" '
        + 'width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a>'
        + '<a class="workshop-share-url" href="' + url + '">' + label + '</a>'
        + '<p>Notebook · Report · Deck · Run guide</p></div></div>'
        + '<p class="workshop-share-footer">' + footer + '</p>'
    )


def _new_slide(source, key):
    row = deepcopy(source)
    row.update(key=key, name=key, answer=None, concept=key,
               exercise=None, exercise_id=None, clicks=0)
    for field in ("technical_guide", "workshop_scene"):
        row.pop(field, None)
    row["cls" if "cls" in row else "kind"] = "workshop-sharing"
    return row


def enrich(slides, deck_root, workshop):
    """Keep setup exercises and return links unchanged while adding share access."""
    manifest = json.loads((ROOT / "docs/share-links.json").read_text(encoding="utf-8"))
    record = manifest["links"][workshop]
    url = record["short_url"]
    if urlsplit(url).scheme != "https" or urlsplit(url).netloc not in {"utm.io", "www.utm.io"}:
        raise ValueError(f"Expected a managed HTTPS UTM.io link for {workshop}")
    setup_key, closing_key, replace_setup = TARGETS[workshop]
    by_key = {_key(row): row for row in slides}
    setup = by_key[setup_key] if replace_setup else _new_slide(by_key[setup_key], "workshop-start")
    if not replace_setup:
        slides.insert(slides.index(by_key[setup_key]), setup)
    setup.update(title="Open the materials and copy the notebook",
                 body=_body(url, closing=False, workshop=workshop), source=url,
                 notes="Leave this QR code visible while participants open the workshop page. "
                 "It links the current notebook, Report, deck, and run guide. Choose Notebook, "
                 "sign in, then copy into a writable project. Continue to the existing setup exercise. "
                 "The short link is managed in docs/share-links.json; do not reuse a historical event QR.")
    setup["cls" if "cls" in setup else "kind"] = "workshop-sharing"
    closing = _new_slide(by_key[closing_key], "workshop-take-home")
    closing.update(title="Keep the notebook and workshop materials",
                   body=_body(url, closing=True, workshop=workshop), source=url,
                   notes="Keep this slide up during questions. Participants resume their saved notebook copy. "
                   "The QR page provides the template, Report, downloads, and short facilitator run guide. "
                   "Use recorded examples for a demo; check the current readiness notes before scheduling live delivery.")
    slides.insert(slides.index(by_key[closing_key]) + 1, closing)
    (deck_root / "notes/share-links.json").write_text(json.dumps({
        "workshop": workshop, "short_url": url, "destination": record["url"],
        "setup_key": _key(setup), "closing_key": _key(closing),
        "qr_asset": "public/images/workshop-qr.svg",
    }, indent=2) + "\n", encoding="utf-8")
    return slides
