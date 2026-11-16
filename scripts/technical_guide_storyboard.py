"""Use the notebook's technical guide frames in the existing deck sequence.

Only explanation slides change. Exercise controls, measured results, and source
captures remain authored in their workshop storyboard.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
import json
import os
from pathlib import Path
import re

KIT = Path(__file__).resolve().parents[1]
ASSETS = KIT / "src/forge_workshop_kit/assets/technical-guides"
TARGETS = {
    "pending": {"harness": "harness-inputs", "dispatch": "loop-3", "skills": "manual-interpret",
                "retry": "retry-identity", "checks": "checks", "changes": "branch-3"},
    "solar": {"window": "goes-window", "model-shapes": "batch-shapes", "learning": "training-step",
              "images": "residual", "run-record": "stage", "research": "compose"},
    "routing": {"features": "word-vector", "decision": "threshold-policy", "labels": "review-provenance",
                "metrics": "intent-counts", "judge": "judge-purpose", "release": "release-columns"},
    "inspection": {"representations": "patch-grid", "patch-distance": "one-patch-distance", "threshold": "threshold",
                   "review": "active-selection", "case-changes": "improved-case", "reproduce": "reload-detector"},
    "transit": {"service-time": "the-last-train-can-belong-to-yesterday-s-service",
                "worker": "one-worker-still-needs-a-complete-loop", "claims": "both-workers-can-see-a-pending-task",
                "integration": "integration-checks-the-patches-against-their-base",
                "memory": "a-saved-note-is-not-automatically-accepted",
                "comparison": "evaluate-the-product-and-the-process-separately"},
    "airline_monitoring": {"itinerary": "replace-semantics", "traces": "trace-shape", "alignment": "tag-lifecycle",
                           "coverage": "coverage", "regression": "case-fields", "comparison": "aligned-comparison"},
}


def _key(row):
    return row.get("key") or row.get("name") or re.sub(r"[^a-z0-9]+", "-", row["title"].replace("<br>", " ").lower()).strip("-")


def _body(deck, identity):
    path = ASSETS / deck / identity / "slide"
    record = json.loads((path / "index.json").read_text(encoding="utf-8"))
    base = os.environ.get("DECK_BASE", "").rstrip("/")
    frames = [{**state, "src": f"{base}/guides/{deck}/{identity}/slide/{state['svg']}"} for state in record["states"]]
    body = ('<TechnicalGuide :frames="' + escape(json.dumps(frames, ensure_ascii=False), quote=True)
            + '" :step="$clicks" />')
    return body, len(frames) - 1


def _replace(row, deck, identity, title):
    row["body"], row["clicks"] = _body(deck, identity)
    row["title"] = title
    row["technical_guide"] = f"{deck}/{identity}"
    row["cls" if "cls" in row else "kind"] = "technical-manual"
    row["notes"] += ("\nVisual guide: " + deck + "/" + identity + ". Advance one state at a time; Back restores the preceding state. "
                     "The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. "
                     "These are explanatory frames; they do not execute an experiment or imply a learner result.")


def enrich(slides, deck_root, deck):
    tokens = json.loads((ASSETS / "tokens.json").read_text(encoding="utf-8"))
    variables = ";".join("--te-" + key.replace("_", "-") + ":" + value for key, value in tokens["colors"].items())
    (deck_root.parent / "technical-manual-tokens.css").write_text(
        "/* Generated from teenage-engineering-visualizations/assets/tokens.json. */\n:root{" + variables + "}\n",
        encoding="utf-8")
    catalog = json.loads((ASSETS / "index.json").read_text(encoding="utf-8"))
    workshop = next(row for row in catalog["workshops"] if Path(row["overview"]).parts[0] == deck)
    by_key = {_key(row): row for row in slides}
    coverage = []
    for sequence in workshop["sequences"]:
        keys = sequence.get("deck_keys") or [TARGETS[deck][sequence["id"]]]
        key = next((key for key in keys if key in by_key), None)
        if key is None:
            raise ValueError(f"No current storyboard target for {deck}/{sequence['id']}: {keys}")
        _replace(by_key[key], deck, sequence["id"], sequence["title"])
        coverage.append({"sequence": sequence["id"], "slide_key": key, "notebook_step": sequence["notebook_step"],
                         "reveal_count": by_key[key]["clicks"] + 1})

    # One overview follows the existing cover. It inherits the opening time so
    # adding a diagram does not allocate extra workshop time or move exercises.
    overview = deepcopy(slides[1])
    overview.update(key="technical-overview", name="technical-overview", answer=None)
    if "exercise" in overview:
        overview["exercise"] = None
    if "exercise_id" in overview:
        overview["exercise_id"] = None
    overview["notes"] = "Introduce the real task, the data available, and the outcome participants will check. Point to each Forge product at the operation it helps investigate."
    _replace(overview, deck, "overview", "What you will build and inspect")
    slides.insert(1, overview)
    (deck_root / "notes/technical-guide-coverage.json").write_text(json.dumps({
        "schema_version": 1, "workshop": workshop["slug"], "overview": "technical-overview",
        "sequences": coverage, "source": "visual-guides/index.json", "runtime_changes": False,
    }, indent=2) + "\n", encoding="utf-8")
    return slides
