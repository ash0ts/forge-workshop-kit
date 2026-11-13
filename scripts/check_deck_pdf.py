"""Check and render each PDF page; repair local slide links for the downloadable PDF."""

import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import pymupdf
from PIL import Image, ImageDraw

deck, target = (Path(value).resolve() for value in sys.argv[1:3])
prefix = sys.argv[3]
layout = json.loads((deck / "notes/slide-map.json").read_text())
document = pymupdf.open(target)
assert len(document) == layout["total_slides"], (len(document), layout["total_slides"])
converted = 0
for page in document:
    assert page.get_text().strip(), "Empty PDF page"
    for link in page.get_links():
        parsed = urlparse(link.get("uri", ""))
        if parsed.hostname not in ("localhost", "127.0.0.1"):
            continue
        route = parsed.path.strip("/")
        page.delete_link(link)
        if route.isdigit() and 1 <= int(route) <= len(document):
            page.insert_link(
                {
                    "kind": pymupdf.LINK_GOTO,
                    "from": link["from"],
                    "page": int(route) - 1,
                    "to": pymupdf.Point(0, 0),
                }
            )
        elif route.startswith(("images/", "recorded-")):
            page.insert_link(
                {
                    "kind": pymupdf.LINK_URI,
                    "from": link["from"],
                    "uri": "https://ash0ts.github.io" + prefix + route,
                }
            )
        else:
            raise ValueError(f"Unexpected local link: {link['uri']}")
        converted += 1
if converted:
    replacement = target.with_suffix(".linked.pdf")
    document.save(replacement)
    document.close()
    replacement.replace(target)
    document = pymupdf.open(target)
screens = deck / ".screenshots"
screens.mkdir(exist_ok=True)
for number, page in enumerate(document, 1):
    assert not any(
        urlparse(link.get("uri", "")).hostname in ("localhost", "127.0.0.1")
        for link in page.get_links()
    )
    page.get_pixmap().save(screens / f"pdf-{number:03}.png")
for offset in range(0, len(document), 12):
    sheet = Image.new("RGB", (1280, 795), "#f4efe5")
    text = ImageDraw.Draw(sheet)
    for slot, index in enumerate(range(offset, min(offset + 12, len(document)))):
        image = Image.open(screens / f"pdf-{index + 1:03}.png")
        image.thumbnail((310, 230))
        x, y = slot % 4 * 320, slot // 4 * 265
        sheet.paste(image, (x, y + 25))
        text.text((x + 10, y + 6), str(index + 1), fill="#163c43")
    sheet.save(screens / f"pdf-contact-{offset // 12 + 1:02}.png")
result = {
    "pages": len(document),
    "empty_pages": 0,
    "all_pages_rendered": True,
    "converted_links": converted,
    "source_sha256": hashlib.sha256((deck / "slides.md").read_bytes()).hexdigest(),
    "pdf_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
}
(deck / "notes/pdf-checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
