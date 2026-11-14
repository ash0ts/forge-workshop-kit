import json
import shutil
import sys
from pathlib import Path

import pytest

from forge_workshop_kit.authoring import (
    action_catalog,
    bind_cells,
    exercise_reference,
    validate_authored,
)
from forge_workshop_kit.cli import main, scaffold
from forge_workshop_kit.rehearsal import AuthoredAdapter, live_environment, replay

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from notebook_builder import Cell, render


def checkout(tmp_path):
    (tmp_path / "scripts").mkdir(parents=True)
    (tmp_path / "src/forge_workshop_kit").mkdir(parents=True)
    shutil.copy(ROOT / "scripts/notebook_builder.py", tmp_path / "scripts/notebook_builder.py")
    (tmp_path / "src/forge_workshop_kit/workshops.json").write_text(
        '{"schema_version":2,"templates":[]}'
    )
    (tmp_path / "pyproject.toml").write_text("[project]\ndependencies=[]\n")
    return tmp_path


def test_action_identity_survives_rewording_source_edit_and_insert():
    original = bind_cells(
        "demo",
        [
            Cell('run = mo.ui.run_button(label="Old")'),
            Cell("mo.stop(not run.value)\nresult = my_hook(1)"),
        ],
    )
    changed = bind_cells(
        "demo",
        [
            Cell('mo.md("Introduction")'),
            Cell('run = mo.ui.run_button(label="Better wording")'),
            Cell("mo.stop(not run.value)\nresult = my_hook(2)"),
        ],
    )
    assert original[-1].cell_id == changed[-1].cell_id == "demo/action/run"
    assert "# workshop-cell: demo/action/run" in render(changed)
    custom = bind_cells("demo", [Cell("result = 1", cell_id="release.verify")])
    assert custom[0].cell_id == "release.verify"


def test_all_workshops_bind_current_cells_and_match_exercise_refs():
    for slug in (
        "pending_inc",
        "solar_autoresearch",
        "request_routing",
        "visual_inspection",
        "transit_factory",
    ):
        result = validate_authored(ROOT, slug)
        assert result["status"] == "passed", result
        assert result["actions"] > 15
        assert result["coverage"]["authored_notebook_execution"] == "not run"
        assert not any("rehearse_pending.py" in row["code"] for row in action_catalog(ROOT, slug))


def test_new_is_small_valid_scaffold_and_never_overwrites(tmp_path):
    root = checkout(tmp_path)
    result = scaffold(root, "example_lab", 'Example "lab"')
    assert result["release_status"] == "draft"
    assert validate_authored(root, "example_lab")["status"] == "passed"
    import runpy

    runpy.run_path(str(root / "decks/example_lab/scripts/build-storyboard.py"))
    layout = json.loads((root / "decks/example_lab/notes/slide-map.json").read_text())
    assert layout["total_slides"] == 1
    assert layout["slides"][0]["title"] == 'Example "lab"'
    before = (root / "scripts/example_lab_cells.py").read_bytes()
    with pytest.raises(ValueError, match="already exists"):
        scaffold(root, "example_lab", "Replacement")
    assert (root / "scripts/example_lab_cells.py").read_bytes() == before
    with pytest.raises(ValueError):
        scaffold(root, "../bad", "Bad")


def test_replay_reads_only_and_rejects_other_identity(tmp_path, monkeypatch):
    state = {
        "stages": {"a": {"name": "baseline", "status": "complete", "result": {"answer": 4}}},
        "requests": {"r": {"status": "unknown"}},
        "publications": {},
    }
    (tmp_path / "journal.json").write_text(json.dumps(state))
    (tmp_path / "identity.json").write_text(
        json.dumps({"workshop": "example", "project": "attendee/project"})
    )
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    # Replay must not instantiate WorkshopSession, initialize SDKs, or load cells.
    monkeypatch.setattr(
        "forge_workshop_kit.rehearsal.load_cells",
        lambda *a: pytest.fail("replay imported authored cells"),
    )
    result = replay(tmp_path, expected_workshop="example")
    assert result["stages"][0]["result_available"] is True
    assert result["requests"]["unknown"] == 1
    assert result["coverage"]["external_account"] == "unknown"
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before
    with pytest.raises(ValueError, match="another workshop"):
        replay(tmp_path, expected_workshop="other")


def fixture_adapter(tmp_path):
    root = checkout(tmp_path / "repo")
    scaffold(root, "fixture", "Fixture")
    source = """from notebook_builder import Cell
cells = [
Cell("import marimo as mo\\nfrom forge_workshop_kit.session import WorkshopSession\\nget_step,set_step=mo.state('example')\\nget_count,set_count=mo.state(0)"),
Cell("editor=mo.ui.code_editor(value='def hook(x):\\\\n    return x * 2')\\nreview=mo.ui.checkbox(label='I read this diff')\\nrun=mo.ui.run_button(label='Run reviewed code')"),
Cell("mo.stop(not run.value)\\nmo.stop(not review.value, mo.md('Read the diff first'))\\nnamespace={}\\nexec(editor.value,namespace)\\nsession=WorkshopSession.from_environment('fixture')\\nwith session.stage('example',sources={'hook.py':editor.value},config={'x':3}) as stage:\\n    if stage.needs_run:\\n        set_count(get_count()+1)\\n        stage.record({'answer':namespace['hook'](3)})\\nmo.md(str(stage.result))", cell_id='fixture/action/run'),
]
"""
    (root / "scripts/fixture_cells.py").write_text(source)
    return root


def test_authored_adapter_preserves_review_hook_result_and_resume(tmp_path):
    root = fixture_adapter(tmp_path)
    state = tmp_path / "state"
    with live_environment("attendee/project", state, 8):
        adapter = AuthoredAdapter(
            root, "fixture", project="attendee/project", state=state, output=lambda x: None
        )
        assert adapter.refresh() == {}
        assert not state.exists(), "Opening and rendering must not create paid or execution records"
        assert adapter.run("fixture/action/run")["status"] == "blocked"
        assert not (state / "journal.json").exists()
        adapter.set_input("review", True)
        adapter.run("fixture/action/run")
        assert adapter.scope["get_count"]() == 1
        assert adapter.scope["stage"].result == {"answer": 6}
        adapter.refresh()
        assert adapter.scope["get_count"]() == 1
        adapter.set_input("review", True)
        adapter.run("fixture/action/run")
        assert adapter.scope["get_count"]() == 1, "The authored stage must reuse its saved result"
        adapter.set_input("editor", "def hook(x):\n    return x + 10")
        adapter.set_input("review", True)
        adapter.run("fixture/action/run")
        assert adapter.scope["stage"].result == {"answer": 13}
        assert adapter.scope["get_count"]() == 2
        receipt = adapter.receipt()
        assert receipt["actions"][0]["status"] == "blocked"
        assert receipt["coverage"]["browser"] == "not run"
        assert receipt["coverage"]["human_rehearsal"] == "unknown"
        second = AuthoredAdapter(
            root, "fixture", project="attendee/project", state=state, output=lambda x: None
        )
        second.refresh()
        second.set_input("review", True)
        second.run("fixture/action/run")
        assert second.scope["get_count"]() == 0
        assert second.scope["stage"].result == {"answer": 6}


def test_environment_restored_and_no_hosted_identity_leaks(tmp_path, monkeypatch):
    monkeypatch.setenv("WANDB_NOTEBOOK_ANCHOR_RUN", "host-copy")
    monkeypatch.setenv("WORKSHOP_PROJECT", "host/project")
    import os

    with live_environment("learner/project", tmp_path, 3):
        assert "WANDB_NOTEBOOK_ANCHOR_RUN" not in os.environ
        assert os.environ["WORKSHOP_PROJECT"] == "learner/project"
    assert os.environ["WANDB_NOTEBOOK_ANCHOR_RUN"] == "host-copy"
    assert os.environ["WORKSHOP_PROJECT"] == "host/project"


def test_cli_requires_explicit_rehearsal_mode_and_publish_project(tmp_path, capsys):
    root = checkout(tmp_path)
    scaffold(root, "fixture", "Fixture")
    assert main(["--root", str(root), "rehearse", "fixture"]) == 2
    assert "No rehearsal ran" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        main(["--root", str(root), "publish", "fixture"])
    assert main(["--root", str(root), "doctor", "fixture"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["inference"].startswith("not called")


def test_adapter_keeps_private_callbacks_local_and_blocks_hidden_dependencies(tmp_path):
    root = fixture_adapter(tmp_path)
    path = root / "scripts/fixture_cells.py"
    path.write_text(
        path.read_text()
        + """
cells.extend([
Cell("_s='first cell'\\ndef callback():\\n    return _s"),
Cell("_s='another cell'"),
Cell("mo.stop(get_step() != 'example')\\nvisible_input=mo.ui.text(value='present')"),
Cell("dependent_value=visible_input.value"),
])
"""
    )
    with live_environment("attendee/project", tmp_path / "state", 8):
        adapter = AuthoredAdapter(
            root,
            "fixture",
            project="attendee/project",
            state=tmp_path / "state",
            output=lambda value: None,
        )
        assert adapter.refresh() == {}
        assert adapter.scope["callback"]() == "first cell"
        assert adapter.scope["dependent_value"] == "present"
        assert "_s" not in adapter.scope
        adapter.scope["set_step"]("hidden")
        assert adapter.refresh() == {}
        assert "visible_input" not in adapter.scope
        assert "dependent_value" not in adapter.scope
        assert any("visible_input" in why for why in adapter.blocked_cells.values())
        with pytest.raises(ValueError, match="fixed by --project"):
            adapter.set_input("project", "another/project")
        with pytest.raises(ValueError, match="budget-usd"):
            adapter.set_input("allowance", 20)


def test_new_cli_modules_remain_python_311_compatible():
    import ast

    for name in ("authoring", "cli", "rehearsal"):
        ast.parse((ROOT / f"src/forge_workshop_kit/{name}.py").read_text(), feature_version=(3, 11))


def test_exercise_reference_uses_actual_labels_and_accurate_activity(tmp_path):
    root = checkout(tmp_path)
    scaffold(root, "reference", "Reference")
    manifest = root / "src/forge_workshop_kit/workshops.json"
    data = json.loads(manifest.read_text())
    row = data["templates"][0]
    row["steps"] = [["setup", "Connect"], ["example", "Try the example"]]
    row["authoring"]["exercises"] = [
        {
            "id": "inspect",
            "step": "example",
            "function": "run_training",
            "activity": "inspect",
            "prerequisites": ["setup"],
            "check_control": "dynamic_check",
            "check_label": "Check this function",
            "run_control": "run_example",
            "run_label": "Stale run label",
            "expected_output": "One saved result.",
            "forge_investigation": "Open the run.",
        }
    ]
    manifest.write_text(json.dumps(data))
    text = exercise_reference(root, "reference")
    assert "Inspect `run_training`" in text
    assert "Try the example" in text and "Before this exercise: Connect" in text
    assert "Check this function" in text
    assert "Stale run label" not in text
    row["authoring"]["exercises"][0]["task"] = "Read the branch that chooses the training source."
    manifest.write_text(json.dumps(data))
    assert "Read the branch" in exercise_reference(root, "reference")
