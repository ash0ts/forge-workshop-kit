"""Check schedule, teaching references and exact notebook controls; no execution."""
import hashlib
import json
from pathlib import Path

DECK = Path(__file__).resolve().parents[1]
ROOT = DECK.parents[1]
layout = json.loads((DECK / "notes/slide-map.json").read_text())
slides = layout["slides"]
notebook = (ROOT / "scripts/transit_cells.py").read_text()
teaching = (ROOT / "src/forge_workshop_kit/factory_teaching.py").read_text()
errors = []
keys = [slide["key"] for slide in slides]
if len(set(keys)) != len(keys):
    errors.append("Slide keys are not unique")

def minutes(clock):
    hour, minute = map(int, clock.split(":"))
    return hour * 60 + minute

cursor = 0
for block in layout["schedule"]:
    start, end = minutes(block["start"]), minutes(block["end"])
    if start != cursor or end <= start:
        errors.append(f"Schedule gap/overlap: {block}")
    cursor = end
if cursor != layout["duration_minutes"] or cursor != 360:
    errors.append("Schedule must cover one six-hour session")
ordered = [slide["timing"]["minutes"] for slide in slides if slide["timing"]["minutes"] is not None]
if ordered != sorted(ordered):
    errors.append("Timed slides are out of order")
controls = []
for slide in slides:
    if not slide["concept"] or not slide["source"]:
        errors.append(f"Missing concept or source: {slide['key']}")
    exercise = slide.get("exercise")
    if not exercise:
        continue
    for field in ("step", "functions", "prerequisites", "run"):
        if not exercise.get(field):
            errors.append(f"Missing exercise {field}: {slide['key']}")
    for field in ("run", "inspect", "optional", "review", "integrate", "recovery"):
        value = exercise.get(field)
        if not value:
            continue
        if value.startswith("Check my ") and value.endswith(" code"):
            name = value[len("Check my "):-len(" code")]
            found = f"def {name}(" in teaching and 'label="Check my "+_spec["function"]+" code"' in notebook
        else:
            found = value in notebook
        controls.append({"slide": slide["number"], "field": field, "label": value, "found": found})
        if not found:
            errors.append(f"Notebook control absent: {value}")
receipt = {
    "source_sha256": hashlib.sha256((DECK / "slides.md").read_bytes()).hexdigest(),
    "duration_minutes": cursor,
    "slides": len(slides),
    "schedule": layout["schedule"],
    "ordered_slides": [{"key": s["key"], "minutes": s["timing"]["minutes"]} for s in slides],
    "controls": controls,
    "errors": errors,
}
(DECK / "notes/schedule-checks.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"slides":len(slides),"duration_minutes":cursor,"controls_checked":len(controls),"errors":errors}))
raise SystemExit(bool(errors))
