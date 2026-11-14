"""Current authored cells, learner functions, and publication-only recovery."""
from pathlib import Path
from unittest.mock import Mock

import pytest

from forge_workshop_kit import airline, airline_teaching
from forge_workshop_kit.authoring import action_catalog, validate_authored
from forge_workshop_kit.rehearsal import AuthoredAdapter
from forge_workshop_kit.session import WorkshopSession

ROOT = Path(__file__).resolve().parents[1]
SLUG = "airline_monitoring"


def adapter(tmp_path):
    runner = AuthoredAdapter(ROOT, SLUG, project="attendee/airline", state=tmp_path, output=lambda _: None)
    assert runner.refresh() == {}
    session = WorkshopSession("attendee/airline", "airline-monitoring", state_dir=tmp_path)
    runner.scope["set_context"]({"session": session})
    assert runner.refresh() == {}
    return runner, session


def test_current_exercises_resolve_and_no_legacy_gateway():
    result = validate_authored(ROOT, SLUG)
    assert result["status"] == "passed", result
    assert result["actions"] >= 30
    actions = action_catalog(ROOT, SLUG)
    assert all("gateway" not in row["code"] for row in actions)
    assert any(row["control"] == "run_alignment_test" for row in actions)
    assert any(row["control"] == "confirm_tag_off" for row in actions)


def test_all_steps_open_without_account_or_execution(tmp_path, monkeypatch):
    monkeypatch.setattr("forge_workshop_kit.provider.Provider.complete", Mock(side_effect=AssertionError("Navigation cannot call a model")))
    runner = AuthoredAdapter(ROOT, SLUG, project="attendee/airline", state=tmp_path, output=lambda _: None)
    assert runner.refresh() == {}
    for step in ("booking", "discovery", "investigate", "align", "monitor", "curate", "repair", "final", "traffic", "report"):
        runner.navigate(step)
        assert runner.refresh_errors == {}, (step, runner.refresh_errors)
    assert not (tmp_path / "journal.json").exists()


def test_checks_execute_current_drafts_and_edits_invalidate_them(tmp_path):
    runner, session = adapter(tmp_path)
    for key in ("instrumentation", "monitor", "curation", "state_scorer", "judge_validation", "itinerary_builder"):
        session.save_draft("airline/" + key, airline_teaching.ANSWERS[key])
    runner.refresh()
    for step, control, key in (
        ("setup", "check_instrumentation", "instrumentation"),
        ("monitor", "check_monitor", "monitor"),
        ("curate", "check_curation", "curation"),
        ("curate", "check_state_scorer", "state_scorer"),
        ("curate", "check_judge_validation", "judge_validation"),
        ("repair", "check_repair", "itinerary_builder"),
    ):
        runner.navigate(step)
        runner.run(SLUG + "/action/" + control)
        assert runner.scope["checked"](key), key
    session.save_draft("airline/itinerary_builder", airline_teaching.STARTERS["itinerary_builder"])
    assert runner.scope["checked"]("itinerary_builder") is False
    assert session.read()["requests"] == {}


def test_development_uses_learner_scorer_and_tracing(tmp_path, monkeypatch):
    runner, session = adapter(tmp_path)
    for key in ("instrumentation", "state_scorer"):
        session.save_draft("airline/" + key, airline_teaching.ANSWERS[key])
    with session.stage("airline/evaluation-code", config={}) as stage:
        stage.record({"sources": {"state_scorer.py": airline_teaching.ANSWERS["state_scorer"]}})
    runner.scope["check_source"]("instrumentation", airline_teaching.check_instrumentation)
    calls = []
    monkeypatch.setattr(airline, "run_batch", lambda *args, **kwargs: calls.append((args, kwargs)))
    runner.scope["batch"]("development")
    assert callable(calls[0][1]["state_scorer"])
    assert callable(calls[0][1]["tool_writer"])
    assert callable(calls[0][1]["model_writer"])
    with session.stage("airline/frozen", config={}) as stage:
        stage.record({"instrumentation": airline_teaching.ANSWERS["instrumentation"]})
    runner.scope["batch"]("final")
    assert calls[1][1]["state_scorer"] is None
    assert session.read()["requests"] == {}


def test_restored_completed_runs_supply_the_current_view(tmp_path):
    runner, session = adapter(tmp_path)
    case = airline.load_cases("discovery")[0]
    result = {"case_id": case["id"], "split": "discovery", "label": "baseline", "mission": case["mission"], "initial_state": case["initial"], "world": case["initial"], "events": [], "scores": {}, "status": "complete", "draft": {"summary": "A saved answer"}}
    with session.stage("airline/baseline/" + case["id"], config={}) as stage:
        stage.record(result)
    runner.navigate("discovery")
    assert runner.refresh_errors == {}
    rows = runner.scope["runs_for"]("discovery")
    assert len(rows) == 1
    assert rows[0]["stage_id"] == stage.id
    assert runner.scope["run_picker"].value == stage.id
    # A newly opened authored runner gets the same saved result without execution.
    other, restored = adapter(tmp_path)
    other.navigate("discovery")
    assert other.scope["runs_for"]("discovery")[0]["stage_id"] == stage.id
    assert restored.read()["requests"] == {}


def test_publication_retry_has_no_passenger_execution(tmp_path, monkeypatch):
    runner, session = adapter(tmp_path)
    session.save_draft("airline/instrumentation", airline_teaching.ANSWERS["instrumentation"])
    monkeypatch.setattr(airline, "run_batch", Mock(side_effect=AssertionError("Publication cannot execute passengers")))
    runner.navigate("report")
    runner.run(SLUG + "/action/retry_publications")
    assert session.read()["requests"] == {}


def test_curated_case_drives_the_authored_regression_action(tmp_path, monkeypatch):
    from forge_workshop_kit import airline_calibration

    runner, session = adapter(tmp_path)
    monkeypatch.setattr("forge_workshop_kit.provider.Provider.complete", Mock(side_effect=AssertionError("A local regression must not call a model")))
    controlled = airline_calibration.run_calibration_pack(session, export=False)[0]
    review = {"decision": "accepted", "reviewer": "participant", "expected_behavior": "Keep the unrequested return flight.", "supporting_event_id": controlled["events"][-1]["id"]}
    curate = airline_teaching.compile_code(airline_teaching.ANSWERS["curation"])["case_from_reviewed_turn"]
    cases = [curate(review, controlled)]
    for key in ("instrumentation", "state_scorer", "itinerary_builder"):
        session.save_draft("airline/" + key, airline_teaching.ANSWERS[key])
    with session.stage("airline/regression", config={}) as stage:
        stage.record({"cases": cases})
    with session.stage("airline/evaluation-code", config={}) as stage:
        stage.record({"sources": {"state_scorer.py": airline_teaching.ANSWERS["state_scorer"]}})
    runner.scope["check_source"]("itinerary_builder", airline_teaching.check_itinerary_builder)
    runner.navigate("repair")
    runner.run(SLUG + "/action/run_regression")
    record = runner.scope["saved"]("airline/regression-check")
    assert record["result"]["passed"] is True
    assert record["result"]["model_calls"] == 0
    assert record["result"]["rows"][0]["source_execution"] == controlled["stage_id"]
    assert record["result"]["rows"][0]["legacy"]["scores"]["task_success"] is False
    assert record["result"]["rows"][0]["repaired"]["scores"]["task_success"] is True
    assert session.read()["requests"] == {}
    assert not runner.scope["run_development"]._component_args["disabled"]


def test_continue_follows_current_step_without_running_work(tmp_path, monkeypatch):
    monkeypatch.setattr("forge_workshop_kit.provider.Provider.complete", Mock(side_effect=AssertionError("Navigation cannot call a model")))
    runner = AuthoredAdapter(ROOT, SLUG, project="attendee/airline", state=tmp_path, output=lambda _: None)
    runner.refresh()
    steps = runner.scope["STEPS"]
    for index, (step, label) in enumerate(steps[:-1]):
        runner.navigate(step)
        assert runner.scope["airline_current_step"] == step
        button = runner.scope["next_step"]
        assert "Continue: " + steps[index + 1][1] in button.text
        button._convert_value(1)
        runner.refresh()
        assert runner.scope["get_step"]() == steps[index + 1][0]
    assert not (tmp_path / "journal.json").exists()


def test_comparisons_use_declared_booking_metrics(tmp_path):
    from forge_workshop_kit.publication import comparison_metrics

    session = WorkshopSession("attendee/airline", "airline-monitoring", state_dir=tmp_path)
    rows = [{"error": 0, "scores": {"task_success": True, "untouched_flights_preserved": True,
             "write_confirmed": True, "execution_errors": 0}}]
    for phase in ("development", "final", "subsequent"):
        name = "airline-" + phase
        result = comparison_metrics(session, name, rows)
        assert result[name + "/task_success"] == 1
        assert result[name + "/untouched_flights_preserved"] == 1
        assert result[name + "/write_confirmed"] == 1
        assert result[name + "/execution_errors"] == 0
        assert name + "/error_mean" not in result


def test_controls_react_to_saved_work_without_repeating_actions():
    from forge_workshop_kit.authoring import load_cells, cell_info

    for cell in load_cells(ROOT, SLUG):
        info = cell_info(cell)
        if info["actions"]:
            assert "get_revision()" not in cell.code, cell.cell_id
        elif info["controls"]:
            assert "get_revision()" in cell.code, cell.cell_id


def test_publication_retry_includes_model_only_judge(tmp_path, monkeypatch):
    runner, session = adapter(tmp_path)
    with session.stage("airline/judge/development-case", config={}) as stage:
        stage.record({"judgment": {"supported": True}, "source_execution": "development-case", "status": "complete"})
    with session.transaction() as state:
        state["requests"][stage.id + "/judge"] = {"id": stage.id + "/judge", "started_at": 1, "ended_at": 2,
            "request": {"messages": [{"role": "user", "content": "Inspect the saved explanation"}]}}
    calls = []
    runner.scope["export_trace"] = lambda *args, **kwargs: calls.append(kwargs) or {"status": "published"}
    monkeypatch.setattr(airline, "run_batch", Mock(side_effect=AssertionError("Export cannot rerun passengers")))
    runner.navigate("report")
    runner.run(SLUG + "/action/retry_publications")
    assert len(calls) == 1
    assert calls[0]["identity"] == stage.id
    assert calls[0]["agent_name"] == "airline-judge-" + session.workspace_id
    assert len(calls[0]["requests"]) == 1


def test_monitoring_uses_frozen_native_criteria_in_following_tests(tmp_path, monkeypatch):
    from forge_workshop_kit import agent_lens

    runner, session = adapter(tmp_path)
    session.save_draft("airline/instrumentation", airline_teaching.ANSWERS["instrumentation"])
    runner.scope["check_source"]("instrumentation", airline_teaching.check_instrumentation)
    with session.stage("airline/tag-context", config={}) as stage:
        stage.record({"tag_id": "tag", "agent_name": "airline-" + session.workspace_id,
                      "snapshot": {"criteria": "Earlier draft"}, "alignment": []})
    monkeypatch.setattr(agent_lens, "save_tag_snapshot", lambda *args, **kwargs: {"criteria": "Current saved criteria"})
    monkeypatch.setattr(airline, "run_batch", lambda *args, **kwargs: [])
    runner.navigate("monitor")
    runner.run(SLUG + "/action/run_monitoring")
    assert runner.scope["saved"]("airline/tag-context")["result"]["snapshot"]["criteria"] == "Current saved criteria"


def test_booking_choice_and_explanation_survive_save_and_restart(tmp_path):
    runner, session = adapter(tmp_path)
    runner.navigate("booking")
    case_id = airline.load_cases("discovery")[1]["id"]
    runner.scope["booking_picker"]._update([case_id])
    runner.refresh()
    assert runner.scope["booking_picker"].value == case_id
    explanation = "Change the outbound flight and preserve the return journey."
    runner.scope["booking_explanation"]._update(explanation)
    runner.run(SLUG + "/action/save_booking")
    assert runner.scope["booking_picker"].value == case_id
    assert runner.scope["booking_explanation"].value == explanation
    other, restored = adapter(tmp_path)
    other.navigate("booking")
    assert other.scope["booking_picker"].value == case_id
    assert other.scope["booking_explanation"].value == explanation
    assert not restored.read()["requests"]
