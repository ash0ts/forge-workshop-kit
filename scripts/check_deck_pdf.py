"""Check and render each PDF page; repair local slide links for the downloadable PDF."""

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pymupdf
from PIL import Image, ImageDraw

deck, target = (Path(value).resolve() for value in sys.argv[1:3])
prefix = sys.argv[3]
layout = json.loads((deck / "notes/slide-map.json").read_text(encoding='utf-8'))
coverage_path = deck / "notes/technical-guide-coverage.json"
coverage = json.loads(coverage_path.read_text()) if coverage_path.exists() else None
guide_keys = {coverage["overview"], *(row["slide_key"] for row in coverage["sequences"])} if coverage else set()
document = pymupdf.open(target)
# Click builds add physical pages. Resolve the printed slide number rather than
# assuming that slide 20 is physical PDF page 20.
page_map = []
for index, page in enumerate(document):
    labels = re.findall(r"\b(\d+)\s*/\s*" + str(layout["total_slides"]) + r"\b", page.get_text())
    assert labels, f"PDF page {index + 1} has no slide-number footer"
    slide = int(labels[-1])
    click = sum(entry["slide"] == slide for entry in page_map)
    page_map.append({"page": index, "slide": slide, "click": click})
assert sorted(set(row["slide"] for row in page_map)) == list(range(1, layout["total_slides"] + 1))
assert [row["slide"] for row in page_map] == sorted(row["slide"] for row in page_map)
checks_path = deck / "notes/delivery-checks.json"
checked_guides = {}
checked_scenes = {}
if checks_path.exists():
    checked = json.loads(checks_path.read_text(encoding='utf-8'))
    source_hash = hashlib.sha256((deck / "slides.md").read_bytes()).hexdigest()
    if checked.get("source_sha256") == source_hash and checked.get("click_states"):
        assert [{"slide": row["slide"], "click": row["click"]} for row in page_map] == [{"slide": row["slide"], "click": row["click"]} for row in checked["click_states"]], "PDF builds differ from checked browser click states"
        checked_scenes = {(row["slide"], row["click"]): row["workshop_scene"] for row in checked["click_states"] if row.get("workshop_scene")}
        checked_guides = {(row["slide"], row["click"]): row["technical_guide"] for row in checked["click_states"] if row.get("technical_guide")}
first_page = {slide: next(row["page"] for row in page_map if row["slide"] == slide) for slide in range(1, layout["total_slides"] + 1)}
converted = 0
for page in document:
    assert page.get_text().strip(), "Empty PDF page"
    for link in page.get_links():
        parsed = urlparse(link.get("uri", ""))
        if parsed.hostname not in ("localhost", "127.0.0.1"):
            continue
        route = parsed.path.strip("/")
        page.delete_link(link)
        if route.isdigit() and int(route) in first_page:
            page.insert_link(
                {
                    "kind": pymupdf.LINK_GOTO,
                    "from": link["from"],
                    "page": next((row["page"] for row in page_map if row["slide"] == int(route) and row["click"] == int(parse_qs(parsed.query).get("clicks", [0])[0])), first_page[int(route)]),
                    "to": pymupdf.Point(0, 0),
                }
            )
        elif route.startswith(("images/", "recorded-", "aria/")):
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
guide_pages = []
scene_pages = []
for number, page in enumerate(document, 1):
    assert not any(
        urlparse(link.get("uri", "")).hostname in ("localhost", "127.0.0.1")
        for link in page.get_links()
    )
    pixmap = page.get_pixmap()
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    row = page_map[number - 1]
    guide = checked_guides.get((row["slide"], row["click"]))
    slide_entry = layout["slides"][row["slide"] - 1]
    is_guide = guide or slide_entry.get("technical_guide") or slide_entry.get("key", slide_entry.get("name")) in guide_keys
    scene = checked_scenes.get((row["slide"], row["click"]))
    if is_guide or scene:
        # Footers and a frame counter do not establish a rendered diagram.
        # Inspect the drawing area above both, independently of PDF text.
        crop = image.crop((int(image.width * .02), int(image.height * .03), int(image.width * .98), int(image.height * .84)))
        background = image.getpixel((10, 10))
        pixels = list(crop.resize((240, 120)).getdata())
        ink = sum(max(abs(channel - base) for channel, base in zip(pixel, background)) > 20 for pixel in pixels) / len(pixels)
        assert ink > .01, f"PDF page {number} has a blank technical guide (drawing coverage {ink:.3%})"
        if guide:
            expected_counter = f"{guide['frameIndex'] + 1} / {guide['frameCount']}"
            assert expected_counter in page.get_text(), f"PDF page {number} is missing technical-guide reveal {expected_counter}"
        (scene_pages if scene else guide_pages).append({"page": number, "slide": row["slide"], "click": row["click"], "drawing_coverage": round(ink, 4)})
    pixmap.save(screens / f"pdf-{number:03}.png")
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
    "slides": layout["total_slides"],
    "page_map": page_map,
    "empty_pages": 0,
    "all_pages_rendered": True,
    "technical_guide_pages": guide_pages,
    "workshop_scene_pages": scene_pages,
    "converted_links": converted,
    "source_sha256": hashlib.sha256((deck / "slides.md").read_bytes()).hexdigest(),
    "pdf_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
}
(deck / "notes/pdf-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding='utf-8')
print(json.dumps(result))
