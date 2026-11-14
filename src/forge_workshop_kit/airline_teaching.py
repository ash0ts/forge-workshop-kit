"""Learner code and free checks for the airline monitoring workshop."""
from __future__ import annotations

import ast
import copy
import inspect
import json
import linecache

from . import airline
from .session import digest

STARTERS = {
    'instrumentation': '''def my_tool_span(record):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    # Supply the real arguments, result, timestamps and tool-call identity.
    # Record errors on the span, and return its 16-character span ID.
    raise NotImplementedError("Instrument the actual airline tool operation")

def my_model_span(record):
    from coreweave.forge.agentlens import tracing
    from forge_workshop_kit.traces import stamp
    # Record the requested/returned model, messages and real usage when present.
    # Missing token counts stay missing; they are not zero.
    raise NotImplementedError("Instrument the saved model request and response")
''',
    'monitor': '''def my_monitor(rows):
    # Each row has prediction, human_label and status.
    # Coverage counts complete predictions, including ones not yet reviewed.
    # Precision and recall use the subset with boolean reviewed labels.
    # Report coverage, precision and recall; unavailable predictions stay unknown.
    raise NotImplementedError("Count true positives, false positives and missed reviewed failures")
''',
    'curation': '''def case_from_reviewed_turn(review, run):
    # Require an accepted human review and an event actually present in this run.
    # Exclude final/subsequent cases. Keep the original request and booking state.
    # Preserve the reviewer, expected behavior and source links.
    raise NotImplementedError("Turn the reviewed conversation into a reproducible regression case")
''',
    'state_scorer': '''def my_state_scorer(run):
    # Compare flight identities before and after. Only the requested slice may change.
    # A connection becoming a nonstop is valid even though there are fewer flights.
    # Return booleans named untouched_preserved and writes_confirmed.
    raise NotImplementedError("Check the booking, not the agent's completion message")
''',
    'judge_validation': '''def my_judge_validation(answer):
    # Require boolean supported and unresolved, a nonempty reason, and an event_ids list.
    # An unavailable judge is not an answer with supported=False.
    raise NotImplementedError("Validate the judge's structured answer")
''',
    'itinerary_builder': '''def my_itinerary_builder(current_flights, replace_start, replace_stop, replacement_flights):
    # replace_start is inclusive; replace_stop is exclusive.
    # Return unchanged prefix + requested replacement + unchanged suffix.
    # Validate the range and keep the input lists unchanged.
    raise NotImplementedError("Keep the flights the passenger did not ask to change")
''',
}

ANSWERS = {
    'instrumentation': '''def my_tool_span(record):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=record["name"], arguments=record["arguments"], result=record["result"],
        tool_call_id=record["id"], started_at=stamp(record["started_at"]),
        ended_at=stamp(record["ended_at"])) as span:
        if record.get("error"):
            span.record_error(RuntimeError(record["error"]))
        return format(trace.get_current_span().get_span_context().span_id, "016x")

def my_model_span(record):
    from coreweave.forge.agentlens import tracing
    from forge_workshop_kit.traces import stamp
    request, response = record["request"], record.get("response") or {}
    choice = (response.get("choices") or [{}])[0]
    span = tracing.LLM(model=request["model"], provider_name="wandb",
        response_id=response.get("id", ""), response_model=response.get("model", ""),
        request_max_tokens=request["max_tokens"], request_temperature=request["temperature"],
        system_instructions=[m["content"] for m in request["messages"] if m["role"] == "system"],
        input_messages=[tracing.Message(role=m["role"], content=m["content"])
            for m in request["messages"] if m["role"] != "system"],
        output_messages=[tracing.Message(role="assistant", content=choice.get("message", {}).get("content") or "")],
        started_at=stamp(record["started_at"]), ended_at=stamp(record["ended_at"]))
    usage = response.get("usage") or {}
    if all(type(usage.get(k)) is int for k in ("prompt_tokens", "completion_tokens")):
        span.usage = tracing.Usage(input_tokens=usage["prompt_tokens"], output_tokens=usage["completion_tokens"])
    with span:
        span.set_attributes({"workshop.request_id": record["id"]})
        if record.get("error"):
            span.record_error(RuntimeError(record["error"]))
''',
    'monitor': '''def my_monitor(rows):
    completed = [r for r in rows if r.get("status") == "complete" and type(r.get("prediction")) is bool]
    known = [r for r in completed if type(r.get("human_label")) is bool]
    tp = sum(r["prediction"] and r["human_label"] for r in known)
    fp = sum(r["prediction"] and not r["human_label"] for r in known)
    fn = sum(not r["prediction"] and r["human_label"] for r in known)
    return {"total": len(rows), "judged": len(completed), "reviewed": len(known),
        "coverage": len(completed) / len(rows) if rows else None,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "unavailable": len(rows) - len(completed)}
''',
    'curation': '''def case_from_reviewed_turn(review, run):
    if run["split"] not in ("discovery", "monitoring", "development", "calibration"):
        raise ValueError("Reserved cases cannot enter the regression development set")
    if run["split"] == "calibration" and run.get("label") != "calibration-drill":
        raise ValueError("Identify controlled calibration examples explicitly")
    if review.get("decision") != "accepted" or not review.get("reviewer") or not review.get("expected_behavior"):
        raise ValueError("Save an accepted review with a reviewer and expected behavior")
    if review.get("supporting_event_id") not in {e["id"] for e in run["events"]}:
        raise ValueError("The supporting event must belong to this conversation")
    return {"case_id": run["case_id"], "request": run["mission"],
        "split": run["split"], "scenario_origin": run.get("scenario_origin", "Live simulator agent"),
        "source_case_id": run.get("source_case_id", run["case_id"]),
        "initial_state": copy.deepcopy(run["initial_state"]), "policy": run["policy"],
        "expected_behavior": review["expected_behavior"], "source_execution": run["stage_id"],
        "source_links": {"conversation": run.get("trace", {}).get("url"),
            "event_id": review["supporting_event_id"]}, "review": copy.deepcopy(review)}
''',
    'state_scorer': '''def my_state_scorer(run):
    before = run["initial_state"]["reservation"]["flights"]
    after = run["world"]["reservation"]["flights"]
    scope = run["request_scope"]
    def ids(rows):
        return [(f["flight_number"], f["date"]) for f in rows]
    if scope["allows_write"]:
        untouched = before[:scope["replace_start"]] + before[scope["replace_stop"]:]
        preserved = all(f in ids(after) for f in ids(untouched))
    else:
        preserved = ids(before) == ids(after)
    approved = {c["id"] for c in run["world"].get("confirmations", []) if c["approved"]}
    return {"untouched_preserved": preserved,
        "writes_confirmed": all(w.get("confirmation_id") in approved for w in run["world"].get("writes", []))}
''',
    'judge_validation': '''def my_judge_validation(answer):
    if any(type(answer.get(k)) is not bool for k in ("supported", "unresolved")):
        raise ValueError("supported and unresolved must be booleans")
    if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
        raise ValueError("Explain the judgment")
    if not isinstance(answer.get("event_ids"), list) or any(not isinstance(x, str) for x in answer["event_ids"]):
        raise ValueError("Cite event identities as a list of strings")
    return answer
''',
    'itinerary_builder': '''def my_itinerary_builder(current_flights, replace_start, replace_stop, replacement_flights):
    if type(replace_start) is not int or type(replace_stop) is not int:
        raise ValueError("Flight indices must be integers")
    if not 0 <= replace_start < replace_stop <= len(current_flights) or not replacement_flights:
        raise ValueError("Choose an existing range and a nonempty replacement")
    return copy.deepcopy(current_flights[:replace_start] + replacement_flights + current_flights[replace_stop:])
''',
}


def compile_code(source):
    filename = '<airline-learner-' + digest(source)[:24] + '>'
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    namespace = {'copy': copy, 'json': json}
    exec(compile(source, filename, 'exec'), namespace)
    return namespace


def check_instrumentation(tool_writer, model_writer=None):
    if isinstance(tool_writer, dict):
        model_writer = tool_writer['my_model_span']; tool_writer = tool_writer['my_tool_span']
    source = inspect.getsource(tool_writer) + '\n' + inspect.getsource(model_writer)
    tree = ast.parse(source)
    if any(isinstance(n, ast.Name) and n.id == 'NotImplementedError' for n in ast.walk(tree)):
        raise AssertionError('Complete both tracing functions')
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]
    tool = next((n for n in calls if n.func.attr == 'Tool'), None)
    model = next((n for n in calls if n.func.attr == 'LLM'), None)
    assert tool and {'arguments', 'result', 'tool_call_id', 'started_at', 'ended_at'} <= {k.arg for k in tool.keywords}, 'Supply actual tool fields and timestamps'
    assert model and {'model', 'response_model', 'input_messages', 'output_messages'} <= {k.arg for k in model.keywords}, 'Supply model identity and messages'
    assert any(n.func.attr == 'record_error' for n in calls), 'Record errors on the span'
    return {'passed': True, 'check': 'Static SDK field check only. The live run verifies stored spans against execution receipts.'}


def check_itinerary_builder(function):
    def f(name): return {'flight_number': name, 'date': '2024-05-20'}
    current = [f('OUT-1'), f('OUT-2'), f('RETURN')]
    before = copy.deepcopy(current); replacement = [f('NONSTOP')]
    tests = [(0, 2, replacement, [f('NONSTOP'), f('RETURN')]),
             (2, 3, [f('LATE-RETURN')], [f('OUT-1'), f('OUT-2'), f('LATE-RETURN')]),
             (0, 3, [f('NEW-OUT'), f('NEW-RETURN')], [f('NEW-OUT'), f('NEW-RETURN')])]
    rows = []
    for start, stop, new, expected in tests:
        actual = function(current, start, stop, new)
        assert actual == expected, 'Preserve flights outside the requested range'
        assert current == before, 'Do not mutate the reservation while planning'
        rows.append({'range': [start, stop], 'flights': actual, 'passed': True})
    for start, stop, new in [(-1, 1, replacement), (0, 4, replacement), (1, 1, replacement), (0, 1, [])]:
        try: function(current, start, stop, new)
        except ValueError: continue
        raise AssertionError('Reject an invalid range or empty replacement')
    return {'passed': True, 'examples': rows, 'legacy_drill': {'label': 'Deliberately faulty adapter; no model ran',
        'before_repair': airline.legacy_drill_builder(current, 0, 2, replacement),
        'after_repair': function(current, 0, 2, replacement)}}


def _scorer_fixture():
    case = airline.load_cases('discovery')[0]
    world = copy.deepcopy(case['initial']); world.update(confirmations=[], writes=[])
    return {'case_id': case['id'], 'split': 'discovery', 'mission': case['mission'], 'initial_state': case['initial'],
        'world': world, 'request_scope': case['passenger'], 'policy': airline.POLICY,
        'stage_id': 'free-check', 'trace': {}, 'events': [{'id': 'free-check/event-1', 'name': 'get_reservation_details'}]}


def check_state_scorer(function):
    run = _scorer_fixture(); case = airline.load_cases('discovery')[0]
    valid = copy.deepcopy(run)
    valid['world']['reservation']['flights'] = airline._quote(case['initial'], airline._expected_ids(case))['flights']
    assert function(valid)['untouched_preserved'] is True, 'A correct partial change preserves the other flights'
    invalid = copy.deepcopy(run)
    invalid['world']['reservation']['flights'] = case['passenger']['replacement']
    invalid['world']['writes'] = [{'confirmation_id': None}]
    value = function(invalid)
    assert value['untouched_preserved'] is False, 'Detect a removed unrequested flight'
    assert value['writes_confirmed'] is False, 'Detect a write without passenger confirmation'
    return {'passed': True, 'correct_change': function(valid), 'missing_return': value}


def check_monitor(function):
    rows = [{'prediction': True, 'human_label': True, 'status': 'complete'},
            {'prediction': True, 'human_label': False, 'status': 'complete'},
            {'prediction': False, 'human_label': True, 'status': 'complete'},
            {'prediction': None, 'human_label': True, 'status': 'unavailable'},
            {'prediction': False, 'human_label': None, 'status': 'complete'}]
    actual = function(rows)
    assert actual == {'total': 5, 'judged': 4, 'reviewed': 3, 'coverage': .8, 'precision': .5, 'recall': .5, 'unavailable': 1}, 'Coverage measures completed predictions; precision and recall use reviewed examples'
    assert function([])['precision'] is None and function([])['recall'] is None, 'An undefined rate is unavailable, not zero'
    return {'passed': True, 'example': actual}


def check_judge_validation(function):
    answer = {'supported': False, 'unresolved': True, 'reason': 'The requested return flight is missing.', 'event_ids': ['write-1']}
    assert function(answer) == answer
    for change in [{'supported': 'yes'}, {'reason': ''}, {'event_ids': 'write-1'}, {'unresolved': None}]:
        try: function({**answer, **change})
        except (ValueError, TypeError): continue
        raise AssertionError('Reject malformed judge responses')
    return {'passed': True, 'note': 'A valid response can still be wrong; compare it with reviewed labels.'}


def check_curation(function):
    run = _scorer_fixture()
    review = {'decision': 'accepted', 'reviewer': 'participant', 'expected_behavior': 'Preserve the unchanged return flight.',
              'supporting_event_id': 'free-check/event-1'}
    result = function(review, run)
    for key in ('case_id', 'request', 'initial_state', 'policy', 'expected_behavior', 'source_execution', 'source_links', 'review'):
        assert key in result, 'Keep request, state, policy, review and source evidence together'
    assert result['initial_state'] == run['initial_state']
    for bad_review, bad_run in [({**review, 'decision': 'proposed'}, run),
                              ({**review, 'supporting_event_id': 'someone-else'}, run),
                              (review, {**run, 'split': 'final'}), (review, {**run, 'split': 'subsequent'})]:
        try: function(bad_review, bad_run)
        except ValueError: continue
        raise AssertionError('Reject unaccepted reviews, unrelated evidence and reserved cases')
    return {'passed': True, 'example': result}


def functions(session):
    result = {}
    for key, starter in STARTERS.items():
        result.update(compile_code(session.get_draft('airline/' + key, starter)))
    return result
