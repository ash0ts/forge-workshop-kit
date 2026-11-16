import json
from pathlib import Path

import marimo as mo
import pytest

from forge_workshop_kit import technical_guides as guides


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    index = {"workshops": [{"slug": "demo", "notebook_slug": "demo_workshop", "title": "Example",
                            "overview": "demo/overview.json", "sequences": [
                                {"id": "observe", "title": "Follow the returned value", "spec": "demo/observe.json", "notebook_step": "tools"},
                                {"id": "compare", "title": "Compare outputs", "spec": "demo/compare.json", "notebook_step": "tools"}]}]}
    (tmp_path / "index.json").write_text(json.dumps(index))
    (tmp_path / "tokens.json").write_text(json.dumps({"colors": {"paper": "#f4f3ef", "ink": "#242522", "muted": "#60625d", "line": "#b6b7af", "accent": "#ec5b28"}}))
    for identity in ("overview", "observe", "compare"):
        folder = tmp_path / "demo" / identity
        (folder / "notebook").mkdir(parents=True)
        (folder / "spec.json").write_text(json.dumps({"steps": [{"title": "Returned record", "body": "The lookup returned 49.", "input": "invoice", "output": "49", "code": "return 49"}],
                                                     "source_links": [{"label": "Code", "url": "https://example.test/source"}]}))
        (folder / "notebook/index.json").write_text(json.dumps({"states": [{"id": "input", "label": "Read input", "svg": "01.svg"}, {"id": "result", "label": "Read result", "svg": "02.svg", "caption": "The returned value enters the next request."}]}))
        for frame in ("01.svg", "02.svg"):
            (folder / "notebook" / frame).write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>49</text></svg>')
    monkeypatch.setattr(guides, "_assets", lambda: tmp_path)
    guides.catalog.cache_clear()
    guides.theme_style.cache_clear()
    yield tmp_path
    guides.catalog.cache_clear()
    guides.theme_style.cache_clear()


def test_sequences_are_scoped_to_the_open_lesson_and_have_an_offline_opening(bundle):
    assert [row["id"] for row in guides.sequences("demo_workshop", "setup")] == ["overview"]
    assert [row["id"] for row in guides.sequences("demo", "tools")] == ["observe", "compare"]
    assert guides.sequences("demo", "final") == []


def test_frame_contains_same_value_code_and_source_as_the_text_alternative(bundle):
    sequence = guides.sequences("demo", "tools")[0]
    html, position, count = guides.frame_html(sequence, 99)
    assert (position, count) == (1, 2)
    assert "data:image/svg+xml;base64," in html
    assert "return 49" in html
    assert "https://example.test/source" in html
    assert "The returned value enters the next request." in html


def test_native_controls_are_bound_without_a_session_or_provider(bundle):
    changes = []
    buttons = guides.controls(mo, "demo", changes.append)
    result = guides.panel(mo, "demo", "tools", {}, buttons)
    assert isinstance(result, mo.Html)
    assert "Follow the returned value" in result.text
    assert "Compare outputs" in result.text
    assert "Text description and sources" in result.text
    assert changes == []


def test_navigation_changes_only_its_own_display_state_and_back_restores(bundle):
    view = {"other": {"sequence": "unchanged"}}

    def update(fn):
        nonlocal view
        view = fn(view)

    buttons = guides.controls(mo, "demo", update)
    guides.panel(mo, "demo", "tools", view, buttons)
    next_button = buttons[("tools", "observe", 0, "next")]
    next_button._on_change(None)
    assert view["tools"]["frames"] == {"observe": 1}
    # Rebuilding the panel retains the controls and does not replay the click.
    guides.panel(mo, "demo", "tools", view, buttons)
    assert buttons[("tools", "observe", 0, "next")] is next_button
    assert view["tools"]["frames"] == {"observe": 1}
    # A retried callback is idempotent: it selects an absolute frame.
    next_button._on_change(None)
    assert view["tools"]["frames"] == {"observe": 1}
    buttons[("tools", "observe", 1, "back")]._on_change(None)
    assert view["tools"]["frames"] == {"observe": 0}
    buttons[("tools", "compare", "select")]._on_change(None)
    assert view["tools"]["sequence"] == "compare"
    assert view["other"] == {"sequence": "unchanged"}


def test_paths_cannot_escape_the_bundled_directory(bundle):
    with pytest.raises(ValueError, match="bundled directory"):
        guides.read_guide({"spec": "../secret.json"})
    index = bundle / "demo/observe/notebook/index.json"
    index.write_text(json.dumps({"states": [{"id": "x", "label": "x", "svg": "../../secret.svg"}]}))
    with pytest.raises(ValueError, match="bundled directory"):
        guides.frame_html(guides.sequences("demo", "tools")[0])


def test_descriptions_escape_content_and_do_not_activate_unsafe_links():
    html = guides._description({"steps": [{"title": "<script>bad</script>", "code": "a < b"}],
                                "source_links": [{"label": "Example", "url": "javascript:alert(1)"}]})
    assert "<script>" not in html
    assert "a &lt; b" in html
    assert "javascript:" not in html


def test_all_authored_notebooks_bind_only_a_display_panel():
    root = Path(__file__).resolve().parents[1]
    for name in ("pending", "solar", "routing", "inspection", "transit", "airline_monitoring"):
        source = (root / "scripts" / f"{name}_cells.py").read_text()
        assert "technical_guide_view = technical_guides.panel(" in source
        assert "get_technical_guide_view, set_technical_guide_view = mo.state(" in source
        assert "technical_guides.theme_style()" in source
