import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("technical_guide_storyboard", ROOT / "scripts/technical_guide_storyboard.py")
storyboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(storyboard)


def test_enrichment_replaces_explanations_without_changing_exercises(tmp_path, monkeypatch):
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "tokens.json").write_text(json.dumps({"colors": {"paper": "#ffffff", "candidate_a": "#246cac"}}))
    (assets / "index.json").write_text(json.dumps({"workshops": [{"slug": "demo", "overview": "demo/overview.json", "sequences": [
        {"id": "operation", "title": "Follow the input", "notebook_step": "practice", "deck_keys": ["operation-slide"]}]}]}))
    for identity in ("overview", "operation"):
        folder = assets / "demo" / identity / "slide"
        folder.mkdir(parents=True)
        (folder / "index.json").write_text(json.dumps({"states": [{"id": "input", "label": "Input", "svg": "01-input.svg"}, {"id": "output", "label": "Output", "svg": "02-output.svg"}]}))
    monkeypatch.setattr(storyboard, "ASSETS", assets)
    monkeypatch.setenv("DECK_BASE", "/forge-workshop-kit/demo/")
    deck = tmp_path / "decks/demo"
    (deck / "notes").mkdir(parents=True)
    slides = [
        {"key": "cover", "title": "Cover", "body": "Situation", "notes": "", "kind": "cover", "time": "0:00"},
        {"key": "operation-slide", "title": "Operation", "body": "Old diagram", "notes": "Explain the operation", "kind": "", "time": "0:10"},
        {"key": "exercise", "title": "Change the function", "body": "Run the free check", "notes": "Run explicitly", "kind": "exercise", "time": "0:15"},
    ]
    exercise = copy.deepcopy(slides[-1])
    storyboard.enrich(slides, deck, "demo")
    assert slides[-1] == exercise
    assert slides[1]["key"] == "technical-overview"
    assert slides[2]["technical_guide"] == "demo/operation"
    assert slides[2]["clicks"] == 1
    assert "/forge-workshop-kit/demo/guides/demo/operation/slide/01-input.svg" in slides[2]["body"]
    assert slides[2]["time"] == "0:10"
    receipt = json.loads((deck / "notes/technical-guide-coverage.json").read_text())
    assert receipt["runtime_changes"] is False
    assert receipt["sequences"][0]["notebook_step"] == "practice"


def test_every_storyboard_calls_shared_enrichment_and_keeps_click_metadata():
    for deck in ("pending", "solar", "routing", "inspection", "transit", "airline_monitoring"):
        source = (ROOT / "decks" / deck / "scripts/build-storyboard.py").read_text(encoding="utf-8")
        assert "technical_guide_storyboard.py" in source
        assert "clicks:" in source
        wrapper = (ROOT / "decks" / deck / "components/TechnicalGuide.vue").read_text(encoding="utf-8")
        assert wrapper.count("../../components/TechnicalGuide.vue") == 1
        # Slidev injects setup into each SFC. A re-export-only wrapper gets an
        # empty render function, overriding the shared component's setup.
        assert '<SharedTechnicalGuide :frames="frames" :step="step" />' in wrapper
        assert "export { default }" not in wrapper
