"""Place the workshop setting beside its existing explanation, without new slides."""
from __future__ import annotations

from html import escape
import json
import os
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("start", "inspect", "build", "compare", "release")
TARGETS = {
    "pending": ("cover", "arrival", "editor", "freeze", "end"),
    "solar": ("cover", "research-question", "agent-need", "freeze", "close"),
    "routing": ("cover", "manager", "review-dataset", "freeze", "close"),
    "inspection": ("opening", "assignment", "human", "regression", "conclusion"),
    "transit": (
        "build-a-transit-app-with-a-team-of-coding-agents",
        "your-team-needs-a-departures-board",
        "add-the-task-board-and-two-workers",
        "more-workers-can-still-produce-more-waiting",
        "take-the-coordination-code-to-your-own-project",
    ),
    "airline_monitoring": ("introduction", "three-questions", "curation", "report-measures", "end"),
}


def _key(row):
    return row.get("key") or row.get("name") or re.sub(
        r"[^a-z0-9]+", "-", row["title"].replace("<br>", " ").lower()
    ).strip("-")


def enrich(slides, deck_root, deck):
    """Add a setting frame before an existing slide's complete authored content.

    Existing reveals retain their relative index. Source code, result tables,
    captures, notes, exercise names, and the schedule are not replaced.
    """
    if deck not in TARGETS:
        return slides
    source = ROOT / "visual-guides/scenes" / deck
    if not source.exists():
        raise ValueError("Build workshop scene artwork before generating the deck.")
    destination = deck_root / "public/scenes" / deck
    destination.mkdir(parents=True, exist_ok=True)
    by_key = {_key(row): row for row in slides}
    base = os.environ.get("DECK_BASE", "").rstrip("/")
    catalog = json.loads((ROOT / "visual-guides/scenes/index.json").read_text(encoding="utf-8"))
    scene = next(row for row in catalog["scenes"] if row["slug"] == deck)
    descriptions = {stage["id"]: stage["alt"] for stage in scene["stages"]}
    coverage = []
    for stage, key in zip(STAGES, TARGETS[deck]):
        if key not in by_key:
            raise ValueError(f"Missing scene placement: {deck}/{key}")
        row = by_key[key]
        original = row["body"]
        if "v-click" in original:
            raise ValueError(f"Scene placement requires explicit reveal indices: {deck}/{key}")
        filename = f"{stage}.svg"
        shutil.copyfile(source / filename, destination / filename)
        # These transitions use explicit $clicks expressions, not automatic
        # v-click registration. The extra frame must not skip their first state.
        details = original.replace("$clicks", "(Math.max(0, $clicks - 1))")
        title = re.sub(r"<[^>]+>", " ", row["title"]).strip()
        row["body"] = (
            f'<figure v-if="$clicks === 0" class="workshop-setting-frame" '
            f'data-workshop-scene="{deck}/{stage}">'
            f'<img :src="{escape(json.dumps(f"{base}/scenes/{deck}/{filename}"), quote=True)}" alt="{escape(descriptions[stage], quote=True)}" />'
            '<figcaption><span>Next → explanation and evidence</span></figcaption>'
            '</figure>\n'
            f'<div v-else class="workshop-setting-detail">{details}</div>'
        )
        field = "cls" if "cls" in row else "kind"
        row[field] = (row.get(field, "") + " workshop-setting-slide").strip()
        old_clicks = row.get("clicks") or 0
        row["clicks"] = old_clicks + 1
        row["workshop_scene"] = f"{deck}/{stage}"
        row["notes"] += (
            "\nSetting frame: point to the active work object, then advance to the complete "
            "explanation. This is an illustrated situation, not an execution screenshot. "
            "Back restores the scene; the following diagram reveals keep their original order."
        )
        coverage.append({"stage": stage, "slide_key": key, "title": title,
                         "original_reveals": old_clicks + 1,
                         "content_preserved": True, "asset": f"scenes/{deck}/{filename}"})
    (deck_root / "notes/scene-coverage.json").write_text(
        json.dumps({"workshop": deck, "placements": coverage,
                    "new_slides": 0, "source": "scripts/illustrate_workshop_scenes.py"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return slides
