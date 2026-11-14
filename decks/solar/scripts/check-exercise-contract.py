"""Reconcile the deck's actionable instructions with the authored notebook.

This checks labels and function names, not whether the live product works. The
browser rehearsal and stored execution receipts provide that separate evidence.
"""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
repo = root.parents[1]
authored = (repo / "scripts/solar_cells.py").read_text()
teaching = (repo / "src/forge_workshop_kit/solar_teaching.py").read_text()
slides = json.loads((root / "notes/slide-map.json").read_text())["slides"]
by = {slide["key"]: slide for slide in slides}
contracts = [
    ("setup-turn", "Connect", ["instrument_tool"], ["Connect and restore my work", "Check my tracing code", "Send my first Agent Lens trace"]),
    ("data-turn", "Solar data", [], ["Load the solar dataset"]),
    ("persistence-turn", "Persistence", ["persistence_forecast"], ["Check my persistence function", "Run my persistence baseline"]),
    ("tracking-turn", "Track and search", ["training_loss", "my_flux_mae", "run_training"], ["Check my measurement code"]),
    ("search-turn", "Track and search", [], ["Run six tracked configurations"]),
    ("goes-repair-turn", "Track and search", ["forward", "fit"], ["Check the GOES repair code", "Train the worked GOES repair"]),
    ("image-turn", "Solar images", ["ImagePredictor.forward", "my_image_mae"], ["Check my image code", "Compare convolutional and residual predictors"]),
    ("evidence-turn", "Research agent", ["select_validation_evidence"], ["Check my evidence selection"]),
    ("round1-turn", "Research agent", ["next_research_action"], []),
    ("final-turn", "Final evaluation", [], ["Freeze versions and evaluate reserved dates"]),
    ("conclusion-turn", "Final evaluation", [], ["Publish my conclusion"]),
]
checks = []
for key, step, functions, buttons in contracts:
    assert key in by, f"Missing slide: {key}"
    slide = by[key]
    text = slide["body"]
    for function in functions:
        parts = function.split(".")
        assert all(part in authored for part in parts), f"Notebook function missing: {function}"
        assert function in text, f"Exercise does not name function: {key}/{function}"
    for button in buttons:
        assert button in authored, f"Notebook control missing: {button}"
        assert button in text, f"Deck control missing: {key}/{button}"
    checks.append({"slide": slide["number"], "key": key, "notebook_step": step, "functions": functions, "controls": buttons})

# The research button is a single state-dependent action, not a phase selector.
research_labels = [
    "Propose two code changes", "Confirm review of Candidate A", "Test Candidate A",
    "Confirm review of Candidate B", "Test Candidate B", "Record my comparison",
    "Request a composition", "Confirm review of composition", "Test the composition",
    "Save the adopted version and lesson",
]
for label in research_labels:
    assert label in teaching, f"Guided-action label missing: {label}"
    assert any(label in slide["body"] for slide in slides), f"Deck omits action: {label}"

result = {
    "notebook_source": "scripts/solar_cells.py",
    "guided_action_source": "src/forge_workshop_kit/solar_teaching.py",
    "status": "passed",
    "exercise_checks": checks,
    "guided_actions": research_labels,
    "scope": "Exact teaching function and control names. Live execution is checked separately in the browser rehearsal.",
    "paid_requests": 0,
}
(root / "notes/exercise-contract-checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "exercises": len(checks), "guided_actions": len(research_labels)}))
