import copy
import json

from forge_workshop_kit.pending import teaching, visuals


def test_handoff_uses_checked_learner_result_and_preserves_it():
    functions = {}
    for name in ("tool", "loop"):
        functions.update(teaching.compile_code(teaching.ANSWERS[name]))
    checked = teaching.check_loop(functions["my_dispatch"], functions["my_observation"], functions["my_invoice_tool"])
    before = copy.deepcopy(checked)
    frames = visuals.handoff_frames(checked)
    assert len(frames) == 4
    assert "pay-2" in frames["3 · Returned records"]
    assert "Tool observation" in frames["4 · Next request"]
    assert checked == before
    assert visuals.handoff_frames({}) == {}


def test_timeout_alternatives_are_local_isolated_and_have_real_effects():
    initial = visuals.new_timeout_practice()
    before = copy.deepcopy(initial)
    timed_out = visuals.timeout_action(initial, "commit")
    assert initial == before
    assert timed_out["events"][-1]["result"]["error"] == "timeout"
    assert len(timed_out["world"]["accounts"]["fern"]["members"]) == 1
    inspected = visuals.timeout_action(timed_out, "inspect")
    retried = visuals.timeout_action(timed_out, "same")
    duplicate = visuals.timeout_action(timed_out, "new")
    assert len(inspected["events"][-1]["result"]["members"]) == 1
    assert retried["events"][-1]["result"]["replayed"] is True
    assert len(retried["world"]["accounts"]["fern"]["members"]) == 1
    assert len(duplicate["world"]["accounts"]["fern"]["members"]) == 2
    assert visuals.new_timeout_practice() == before


def test_skill_read_requires_actual_return_and_later_request():
    text = 'Check the account.\nDo not trust "done".'
    read = {"name": "read_skill", "arguments": {"name": "verify-operation"}, "result": {"text": text}, "id": "read-1", "ended_at": 10}
    run = {"events": [read, {"name": "onboarding_status"}]}
    request = {"id": "run/2", "started_at": 11, "request": {"messages": [{"role": "user", "content": "Tool observation: " + json.dumps({"text": text})}]}}
    result = visuals.skill_inspection(run, [request])
    assert result[0]["request"]["id"] == "run/2"
    assert result[0]["following"] == ["onboarding_status"]
    assert visuals.skill_inspection(run, [{**request, "started_at": 9}])[0]["request"] is None
    assert visuals.skill_inspection({"events": [{"name": "get_account"}]}) == []
    assert "No successful" in visuals.skill_view({"events": []})
    assert not visuals.skill_inspection({"events": [{**read, "error": "failed"}]})[0]["read"]


def test_comparison_preserves_missing_rows_judgments_and_escapes_outputs():
    run = {"case_id": "fresh-case", "scores": {"task_success": True}, "events": [], "draft": {"summary": "<script>alert(1)</script>"}, "world": {"accounts": {}}, "explanation_judgment": {"status": "unavailable"}, "trace": {"url": "javascript:bad"}}
    records = {"starting": [run], "manual": [], "agent": []}
    before = copy.deepcopy(records)
    html = visuals.comparison_view(records, "fresh-case")
    assert "Unavailable" in html and "No saved execution" in html
    assert "<script>" not in html and "javascript:bad" not in html
    assert records == before
    assert visuals.aligned_cases(records) == ["fresh-case"]
