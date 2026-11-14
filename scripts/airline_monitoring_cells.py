"""Authored airline-monitoring lesson. Execution stays behind explicit controls."""
from notebook_builder import Cell

cells = []
def add(code, hide=True, cell_id=None):
    # Durable-record helpers are ordinary Python reads. Make their presentation
    # consumers reactive without making the execution cells depend on refreshes.
    is_action = bool(cell_id and "/action/" in cell_id)
    if not is_action and ("mo.ui." in code or "mo.vstack" in code) and "get_revision()" not in code:
        code = "_revision = get_revision()\n" + code
    cells.append(Cell(code, hide=hide, cell_id=cell_id))

add('''
import json
import time
import marimo as mo
from forge_workshop_kit import WorkshopSession, setup, ui, airline, airline_teaching as teaching
from forge_workshop_kit import agent_lens, airline_calibration, airline_regression
from forge_workshop_kit.manifest import get_workshop
from forge_workshop_kit.session import digest
from forge_workshop_kit.traces import event, export_trace, saved_trace_inputs
from forge_workshop_kit.publication import publish_comparison, publish_report as write_report
get_context, set_context = mo.state({})
get_step, set_step = mo.state("setup", allow_self_loops=True)
get_revision, set_revision = mo.state(0)
get_output, set_output = mo.state({})
STEPS = tuple(tuple(row) for row in get_workshop("airline-monitoring")["steps"])
''', cell_id="airline_monitoring/imports")

add('''
def refresh():
    set_revision(lambda value: value + 1)
def go_to(step):
    session = get_context().get("session")
    if session: session.set_view(step)
    set_step(step)
def show(name, result):
    set_output(lambda old: {**old, name: result})
def saved(name):
    session = get_context().get("session")
    rows = [] if not session else [r for r in session.read()["stages"].values() if r["name"] == name and r["status"] == "complete"]
    return max(rows, key=lambda row: row["ended_at"]) if rows else None
def save_local(name, result, *, config=None, sources=None):
    session = get_context()["session"]
    with session.stage(name, config=config or {"content": digest(result)}, sources=sources) as stage:
        if stage.needs_run: stage.record(result)
    refresh()
    return stage.result

def source_for(name):
    session = get_context().get("session")
    starter = teaching.STARTERS[name]
    return session.get_draft("airline/" + name, starter) if session else starter

def save_source(name, source):
    session = get_context().get("session")
    if session: session.save_draft("airline/" + name, source)

def check_source(name, checker):
    source = source_for(name)
    values = teaching.compile_code(source)
    function_names = {"monitor": "my_monitor", "curation": "case_from_reviewed_turn", "state_scorer": "my_state_scorer", "judge_validation": "my_judge_validation", "itinerary_builder": "my_itinerary_builder"}
    result = checker(values if name == "instrumentation" else values[function_names[name]])
    session = get_context()["session"]
    with session.transaction() as state:
        state.setdefault("airline_checks", {})[name] = {"source": digest(source), "result": result}
    show("check/" + name, result)
    refresh()
    return result

def checked(name):
    session = get_context().get("session")
    check = session.read().get("airline_checks", {}).get(name) if session else None
    return bool(check and check["source"] == digest(source_for(name)))

def hooks(source=None):
    values = teaching.compile_code(source or source_for("instrumentation"))
    return {"tool_writer": values["my_tool_span"], "model_writer": values["my_model_span"]}

def runs_for(partition, label=None):
    session = get_context().get("session")
    if not session: return []
    rows = []
    for record in sorted(session.read()["stages"].values(), key=lambda row: row.get("ended_at", 0)):
        result = record.get("result") or {}
        if record["status"] == "complete" and result.get("split") == partition and result.get("case_id") and (label is None or result.get("label") == label):
            rows.append({**result, "stage_id": record["id"], "trace": session.read()["publications"].get("trace/" + record["id"], {})})
    # A successful explicit retry supersedes a prior completed display entry.
    unique = {}
    for row in rows: unique[(row["case_id"], row.get("label"))] = row
    return list(unique.values())

def trace_url(run):
    session = get_context().get("session")
    receipt = session.read()["publications"].get("trace/" + run["stage_id"], {}) if session else {}
    return receipt.get("url") if receipt.get("verified") else None

def review_for(stage_id, trace_id=None):
    session = get_context().get("session")
    if not session: return None
    matches = [row for row in session.read()["stages"].values()
        if row["status"] == "complete" and row["name"].startswith("airline/review/" + stage_id + "/")
        and (trace_id is None or row["result"].get("trace_id") == trace_id)]
    return max(matches, key=lambda row: row["ended_at"]) if matches else None

def native_scope():
    session = get_context()["session"]
    return "airline-" + session.workspace_id

def batch(partition, label="baseline", builder=None):
    session = get_context()["session"]
    if partition in ("final", "subsequent"):
        tracing_source = saved("airline/frozen")["result"]["instrumentation"]
    else:
        if not checked("instrumentation"):
            raise ValueError("The tracing draft changed. Run Check my tracing code before this execution.")
        tracing_source = source_for("instrumentation")
    scorer = None
    if partition == "development":
        scorer = teaching.compile_code(saved("airline/evaluation-code")["result"]["sources"]["state_scorer.py"])["my_state_scorer"]
    return airline.run_batch(session, partition, label=label, itinerary_builder=builder, state_scorer=scorer, **hooks(tracing_source))

def saved_ids(partitions):
    return [run["stage_id"] for phase in partitions for run in runs_for(phase)]
''', cell_id="airline_monitoring/helpers")

add('''
_s = get_context().get("session")
_revision = get_revision()
_done = _s.read().get("progress", {}).get("completed", []) if _s else []
airline_navigation = ui.navigation(mo, STEPS, get_step(), go_to, completed=_done, label="Your monitoring shift")
mo.vstack([mo.Html(ui.STYLE), airline_navigation, mo.Html(ui.context(_s)) if _s else mo.md("Copy this notebook into a project you can write to. Your traces and results will belong to that project.")])
''')

add('''
_s = get_context().get("session")
_current = get_step()
_missing = None
if _current != "setup" and not _s:
    _missing = ("Connect to your project and restore your work first.", "setup")
elif _current == "discovery" and not saved("airline/booking"):
    _missing = ("Save your expected booking before running the agent.", "booking")
elif _current == "discovery" and not checked("instrumentation"):
    _missing = ("Complete and check your tracing functions before sending requests.", "setup")
elif _current == "investigate" and not runs_for("discovery"):
    _missing = ("Run the discovery requests so there is an execution to investigate.", "discovery")
elif _current == "align" and not saved("airline/investigation"):
    _missing = ("Save one evidence-linked investigation before defining the tag.", "investigate")
elif _current == "monitor" and not saved("airline/tag-context"):
    _missing = ("Read back your saved native tag and agent scope first.", "align")
elif _current == "curate" and not any(review_for(run["stage_id"]) for run in runs_for("discovery") + runs_for("monitoring") + runs_for("calibration")):
    _missing = ("Save a turn review, including its expected behavior and supporting event.", "monitor")
elif _current == "repair" and not (saved("airline/regression") and saved("airline/evaluation-code")):
    _missing = ("Save your regression cases and development evaluation code before testing a repair.", "curate")
elif _current == "final" and not saved("airline/development-complete"):
    _missing = ("Compare the repair on all four development bookings before freezing it.", "repair")
elif _current == "traffic" and len(runs_for("final")) != 12:
    _missing = ("Complete both versions on all six reserved bookings first.", "final")
elif _current == "report" and len(runs_for("subsequent")) != 8:
    _missing = ("Run both versions on the subsequent batch before drawing the final conclusion.", "traffic")
missing_prerequisite = ui.prerequisite(mo, _missing[0], _missing[1], go_to) if _missing else mo.md("")
missing_prerequisite
''')

add('''
mo.stop(get_step() != "setup")
mo.vstack([mo.Html(ui.heading("Monitor an airline service agent and build better evaluations", "A passenger asks to change the outbound leg of a round trip. The booking API accepts a complete replacement itinerary. If the agent leaves out the return flight, a successful API call can still produce the wrong booking.", theme="neutral", eyebrow="Airline service desk · Six-hour Forge workshop")), mo.md("You will run a working agent, inspect its behavior in Agent Lens, review a monitoring rule, and turn incidents into regression tests. Then you will repair the itinerary code and compare both versions on reserved requests. The passenger should still have a flight home."), mo.md("**Data:** simulated bookings, requests, and airline policy from a pinned MIT-licensed revision of [τ-bench](https://github.com/sierra-research/tau2-bench/tree/989d3285ae669e49503324bdb9981bf14fccedeb). This workshop adapts those records; it is not a benchmark replication or real passenger traffic. Related bookings stay in the same partition. Reserved cases remain outside the repair and tag-tuning steps."), mo.md("The notebook runs tools locally. Model calls use your fixed inference model and your account. The $8 allowance covers notebook inference; native tag judging and notebook compute are billed separately. Opening a step or editing code starts no paid work."), mo.md("[Companion deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) · [Source and dataset provenance](https://github.com/ash0ts/forge-workshop-kit/tree/main/docs/airline_monitoring-runbook.md)")])
''')

add('''
_context = setup.project_context()
project_input = mo.ui.text(value=_context["project"], label="Your Forge project", disabled=_context["hosted"] and _context["detected"], full_width=True)
allowance = mo.ui.number(value=8, start=.01, stop=1000, label="Notebook inference allowance · USD")
connect = mo.ui.run_button(label="Connect and restore my work")
mo.vstack([project_input, allowance, connect, mo.md("On a laptop, run `uv run wandb login` first. Your project must allow traces, artifacts, and evaluations. The connection check does not send a model request.")]) if get_step() == "setup" else mo.md("")
''')
add('''
mo.stop(not connect.value)
_s = WorkshopSession.from_environment("airline-monitoring", project=project_input.value, budget_usd=allowance.value)
_access = _s.check_access()
_s.restore()
setup.save_access(_s, _access)
set_context({"session": _s})
set_step(_s.get_view("setup"))
refresh()
show("setup", {"status": "Connected", "next": "Complete the tracing code and send the free setup trace."})
''', cell_id="airline_monitoring/action/connect")

add('''
_s = get_context().get("session")
instrumentation_editor = mo.ui.code_editor(value=source_for("instrumentation"), language="python", on_change=lambda text: save_source("instrumentation", text), debounce=False)
check_instrumentation = mo.ui.run_button(label="Check my tracing code", disabled=not bool(_s))
first_trace = mo.ui.run_button(label="Send my first Agent Lens trace", disabled=not checked("instrumentation"))
mo.vstack([mo.Html(ui.step("Record what the agent actually did", "Complete my_tool_span and my_model_span. The tool span needs its original arguments, result, timestamps, and any error. The model span needs the real request, response, and available usage.", "Open your setup trace and find the attribute you added. These same functions export every request batch later.")), instrumentation_editor, mo.accordion({"Hint": mo.md("Use the Forge SDK context managers shown in the starter. Preserve actual timestamps; exporting happens after the operation."), "Worked tracing code": mo.md("```python" + chr(10) + teaching.ANSWERS["instrumentation"] + chr(10) + "```")}), check_instrumentation, first_trace]) if get_step() == "setup" else mo.md("")
''')
add('''
mo.stop(not check_instrumentation.value)
try: show("check/instrumentation", check_source("instrumentation", teaching.check_instrumentation))
except Exception as _error: show("check/instrumentation", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_instrumentation")
add('''
mo.stop(not first_trace.value)
_s = get_context()["session"]
with _s.stage("airline/setup", config={"purpose": "instrumentation check"}, sources={"instrumentation.py": source_for("instrumentation")}) as _stage:
    if _stage.needs_run:
        _result, _event = event("inspect_booking_environment", {}, lambda: {"project": _s.project, "booking_state": "isolated fictional copies"}, on_error=_stage.record_event)
        _stage.record({"events": [_event]})
try:
    _trace = export_trace(_s, **saved_trace_inputs(_s, _stage.id), agent_name=native_scope(), **hooks())
    show("setup", {"status": "Stored spans verified", "url": _trace["url"]})
except Exception as _error:
    show("setup", {"status": "Execution saved; trace publication pending", "error": str(_error)})
_s.checkpoint("setup")
refresh()
''', cell_id="airline_monitoring/action/first_trace")

add('''
mo.stop(get_step() != "booking")
_examples = airline.load_cases("discovery")
mo.vstack([mo.Html(ui.step("Read the passenger's request before inspecting the agent", "Choose one discovery booking. Write down which flights the passenger wants to change and which must remain. The update tool replaces its full flight list; it does not append a partial patch.", "You can explain the expected booking without relying on the agent's final message.")), mo.md("The cases cover flight changes, restricted requests, and itinerary questions. A shorter itinerary can be valid: two connections may become a nonstop flight. Count-based monitoring alone will flag the wrong things.")])
_s = get_context().get("session")
_remembered = _s.get_draft("airline/booking-case", _examples[0]["id"]) if _s else _examples[0]["id"]
booking_picker = mo.ui.dropdown({row["id"]: row["id"] for row in _examples}, value=_remembered if _remembered in {row["id"] for row in _examples} else _examples[0]["id"], on_change=lambda value: _s.save_draft("airline/booking-case", value) if _s else None, label="Discovery booking", full_width=True)
booking_picker
''')
add('''
mo.stop(get_step() != "booking")
_case = next(row for row in airline.load_cases("discovery") if row["id"] == booking_picker.value)
mo.vstack([mo.md("**Passenger request**"), mo.md(_case.get("request", _case.get("mission", ""))), mo.ui.table([{"Segment": index + 1, "Flight": flight["flight_number"], "Date": flight["date"], "From": flight.get("origin"), "To": flight.get("destination")} for index, flight in enumerate(_case["initial"]["reservation"]["flights"])], selection=None), mo.accordion({"Starting booking, policy, and allowed tools": mo.json({"request": _case["mission"], "initial_state": _case["initial"], "policy": airline.public_case(_case)["policy"], "tools": airline.TOOLS})}), mo.md("Do not reveal final or subsequent requests while changing your code or monitoring criteria.")])
''')
add('''
_s = get_context().get("session")
_booking_key = "airline/booking-explanation/" + booking_picker.value
booking_explanation = mo.ui.text_area(value=_s.get_draft(_booking_key, "") if _s else "", on_change=lambda text: _s.save_draft(_booking_key, text) if _s else None, label="What should change, and what must remain untouched?", full_width=True)
save_booking = mo.ui.run_button(label="Save my expected booking", disabled=not bool(get_context().get("session")))
mo.vstack([booking_explanation, save_booking]) if get_step() == "booking" else mo.md("")
''')
add('''
mo.stop(not save_booking.value)
mo.stop(not booking_explanation.value.strip(), mo.md("Name the requested change and at least one thing to preserve."))
save_local("airline/booking", {"case_id": booking_picker.value, "explanation": booking_explanation.value})
get_context()["session"].checkpoint("booking")
''', cell_id="airline_monitoring/action/save_booking")

add('''
_s = get_context().get("session")
_ready = bool(_s and saved("airline/booking") and checked("instrumentation"))
run_discovery = mo.ui.run_button(label="Run eight discovery requests", disabled=not _ready)
mo.vstack([mo.Html(ui.step("Let the service agent handle eight requests", "This is the starting agent using the complete-itinerary API. It is allowed to succeed. Each booking starts in an isolated copy; the passenger confirms only an offer that respects their request.", "For one request, compare the starting booking, actual tool arguments, resulting booking, and final response.")), mo.md("At most ten model requests per conversation, including transport retries. Completed cases are reused if a later case fails. This is the first paid exercise."), run_discovery, mo.md("Complete the booking explanation and tracing check first.") if not _ready else mo.md("Your tracing functions will record this batch.")]) if get_step() == "discovery" else mo.md("")
''')
add('''
mo.stop(not run_discovery.value)
show("discovery", batch("discovery"))
get_context()["session"].checkpoint("discovery")
refresh()
''', cell_id="airline_monitoring/action/run_discovery")

add('''
mo.stop(get_step() != "investigate")
_s = get_context().get("session")
mo.vstack([mo.Html(ui.step("Find the operation behind one outcome", "In Agent Lens, filter to the workshop agent shown in the next step. Use the custom attributes airline.version and airline.partition for version and batch; the standard Agent version field is not populated by this workshop. Save the view. Open a conversation, then compare Thread, Spans, and Timeline. Check a tool's arguments and returned booking before accepting the final completion message.", "Save one claim with a conversation and event that supports it. A tool error followed by recovery is different from a wrong booking.")), mo.Html(ui.links({"Open my Agent Lens project": "https://forge.coreweave.com/agent-lens/" + _s.project}) if _s else ""), mo.md("**Prepared Insights:** [open the workshop project](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/insights/failure). The last verification found no completed clustering run, so a prepared cluster investigation is not yet available. Read the current status below. When clusters exist, inspect a representative member and a counterexample. An empty view does not show that the agent had no problems. Until then, investigate individual conversations and record the Insights exercise as incomplete.")])
''')
add('''
read_insights = mo.ui.run_button(label="Read native Insights availability", disabled=not bool(get_context().get("session")))
mo.vstack([read_insights, mo.md("This reads current status from the prepared project. It does not launch clustering or model work.")]) if get_step() == "investigate" else mo.md("")
''')
add('''
mo.stop(not read_insights.value)
_client = agent_lens.LensClient("wandb/forge-workshop-kit")
try:
    _result = _client.insights_status()
    save_local("airline/insights-status", {"project": "wandb/forge-workshop-kit", "url": "https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/insights/failure", "status": _result})
    show("insights", {"project": "wandb/forge-workshop-kit", "native_status": _result, "next": "Open the native view to check whether a completed cluster exists before claiming this exercise is available."})
except Exception as _error:
    show("insights", {"status": "unavailable", "error": str(_error), "next": "Continue with individual conversations. Prepared Insights remains an incomplete access check."})
finally: _client.close()
refresh()
''', cell_id="airline_monitoring/action/read_insights")

add('''
_cases = runs_for("discovery")
investigation_case = mo.ui.dropdown({r["case_id"]: r["stage_id"] for r in _cases}, value=_cases[0]["case_id"] if _cases else None, label="Completed discovery request", full_width=True)
investigation_claim = mo.ui.text_area(label="What happened, and which operation supports your claim?", full_width=True)
investigation_span = mo.ui.text(label="Exact Agent Lens span URL", full_width=True)
save_investigation = mo.ui.run_button(label="Save this trace investigation", disabled=not bool(_cases))
mo.vstack([investigation_case, investigation_claim, investigation_span, save_investigation]) if get_step() == "investigate" else mo.md("")
''')
add('''
mo.stop(not save_investigation.value)
mo.stop(not investigation_claim.value.strip(), mo.md("Describe the operation and the observed outcome."))
_s = get_context()["session"]
_run = next(row for row in runs_for("discovery") if row["stage_id"] == investigation_case.value)
_url = trace_url(_run)
mo.stop(not _url or not investigation_span.value.startswith(_url + "/"), mo.md("Use a span URL from this run's verified conversation. Retry its trace publication if no link is available yet."))
save_local("airline/investigation", {"stage_id": _run["stage_id"], "case_id": _run["case_id"], "claim": investigation_claim.value, "span_url": investigation_span.value, "conversation_url": _url})
_s.checkpoint("investigate")
''', cell_id="airline_monitoring/action/save_investigation")

add('''
run_calibration = mo.ui.run_button(label="Create six controlled calibration traces", disabled=not bool(get_context().get("session")))
mo.vstack([mo.md("### If the live agent made no relevant mistake"), mo.md("Create six local simulator incidents for tag calibration: an omitted return flight, a valid one-way trip, a connection-to-nonstop change, an explicitly requested whole-itinerary change, recovery, and a request awaiting confirmation. These are controlled tool-only drills with no model calls. Their labels are teaching examples, not measured agent failures."), run_calibration]) if get_step() in ("investigate", "align") else mo.md("")
''')
add('''
mo.stop(not run_calibration.value)
_runs = airline_calibration.run_calibration_pack(get_context()["session"])
show("calibration", {"status": "Controlled simulator incidents saved", "count": len(_runs), "model_calls": 0, "next": "Open these labeled conversations in Agent Lens, inspect their actual tools, and add relevant turns to Alignment."})
refresh()
''', cell_id="airline_monitoring/action/run_calibration")

add('''
_s = get_context().get("session")
tag_id = mo.ui.text(value=_s.get_draft("airline/tag-id", "") if _s else "", label="Native tag ID", on_change=lambda value: _s.save_draft("airline/tag-id", value) if _s else None, full_width=True)
read_native_tag = mo.ui.run_button(label="Read back my tag and alignment", disabled=not bool(saved("airline/investigation")))
mo.vstack([mo.Html(ui.step("Review an Unrequested itinerary change rule", "In Tags, choose New tag, Create manually, then turn on Apply with AI to reveal the criteria and agent filter. Create one tag scoped to the exact agent name below, then stop sending new traffic while you calibrate it. In Alignment, label both suspect and ordinary turns, test criteria, and inspect the judge's reasons. Alignment tests do not update live criteria: save your chosen criteria and read them back before the next traffic batch.", "You can explain a false positive, a missed issue, and a turn with insufficient evidence.")), mo.md("**Agent scope:** `" + (native_scope() if _s else "Connect first") + "`"), mo.md("Start with the request and what changed, not a count of remaining flights. Include a one-way booking, a valid connection-to-nonstop change, a requested full-itinerary change, recovery, and a request waiting for confirmation. Native judges see turn-level evidence; missing context is not a negative finding."), mo.Html(ui.links({"Open native Agent Lens": "https://forge.coreweave.com/agent-lens/" + _s.project, "How to create and align tags": "https://docs.coreweave.com/products/agent-lens/tags/create-tag"}) if _s else ""), tag_id, read_native_tag, mo.md("This readback checks saved native configuration. During release qualification, native Alignment test requests returned HTTP 500. The test control preserves those judgments as unavailable; it does not replace them with a local judge or report a failed booking. Tag configuration and manual labels remained accessible. Native tag calls are billed outside the notebook allowance.")]) if get_step() == "align" else mo.md("")
''')
add('''
mo.stop(not read_native_tag.value)
_s = get_context()["session"]
try:
    _snapshot = agent_lens.save_tag_snapshot(_s, tag_id.value.strip(), native_scope())
    _client = agent_lens.LensClient(_s.project)
    try: _alignment = _client.alignment(tag_id.value.strip())
    finally: _client.close()
    save_local("airline/tag-context", {"tag_id": tag_id.value.strip(), "agent_name": native_scope(), "snapshot": _snapshot, "alignment": _alignment})
    show("align", {"status": "Native configuration saved", "snapshot": _snapshot, "alignment": _alignment})
    _s.checkpoint("align")
except Exception as _error:
    show("align", {"status": "Native readback unavailable", "error": str(_error), "next": "Check tag scope, saved criteria, enabled status, and project permissions. Do not substitute a missing label with false."})
refresh()
''', cell_id="airline_monitoring/action/read_native_tag")

add('''
_s = get_context().get("session")
monitor_editor = mo.ui.code_editor(value=source_for("monitor"), language="python", on_change=lambda text: save_source("monitor", text), debounce=False)
check_monitor = mo.ui.run_button(label="Check my monitoring calculations", disabled=not bool(_s))
run_monitoring = mo.ui.run_button(label="Run four new requests", disabled=not bool(saved("airline/tag-context")))
read_monitoring = mo.ui.run_button(label="Read tag results", disabled=not bool(runs_for("monitoring")))
mo.vstack([mo.Html(ui.step("Count the turns the monitor has actually judged", "Implement my_monitor to report judged coverage, pending or unavailable rows, and precision and recall against human reviews. A turn with no completed judgment must not become a negative prediction. Live assignments alone do not reveal processing coverage; use explicit Alignment test results to calculate agreement.", "You can name the denominator for each number and point to at least one flagged and one unflagged control.")), monitor_editor, mo.accordion({"Hint": mo.md("First separate completed boolean labels from pending and unavailable rows. Precision divides true positives by predicted positives; recall divides true positives by reviewed positives."), "Worked monitoring calculation": mo.md("```python" + chr(10) + teaching.ANSWERS["monitor"] + chr(10) + "```")}), check_monitor, run_monitoring, read_monitoring, mo.md("Run the new requests once. Reading results afterward checks server processing; it does not repeat agent work.")]) if get_step() == "monitor" else mo.md("")
''')
add('''
mo.stop(not check_monitor.value)
try: show("check/monitor", check_source("monitor", teaching.check_monitor))
except Exception as _error: show("check/monitor", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_monitor")
add('''
mo.stop(not run_monitoring.value)
_s = get_context()["session"]
_tag = saved("airline/tag-context")["result"]
_snapshot = agent_lens.save_tag_snapshot(_s, _tag["tag_id"], _tag["agent_name"], require_enabled=True)
save_local("airline/tag-context", {**_tag, "snapshot": _snapshot})
show("monitoring", batch("monitoring"))
refresh()
''', cell_id="airline_monitoring/action/run_monitoring")
add('''
mo.stop(not read_monitoring.value)
_s = get_context()["session"]
_tag = saved("airline/tag-context")["result"]
_runs = runs_for("monitoring")
try:
    _native = agent_lens.read_monitoring(_s, _tag["tag_id"], [r["stage_id"] for r in _runs], _tag["agent_name"])
    save_local("airline/monitor-readback", _native)
    show("monitoring-native", _native)
except Exception as _error: show("monitoring-native", {"status": "unavailable", "error": str(_error)})
refresh()
''', cell_id="airline_monitoring/action/read_monitoring")

add('''
_s = get_context().get("session")
_reviewable = runs_for("discovery") + runs_for("monitoring") + runs_for("calibration")
review_case = mo.ui.dropdown({r["case_id"]: r["stage_id"] for r in _reviewable}, value=_reviewable[0]["case_id"] if _reviewable else None, label="Turn to review", full_width=True)
mo.vstack([mo.md("Choose a completed request, then review its evidence below."), review_case]) if get_step() == "monitor" else mo.md("")
''')
add('''
_reviewable = runs_for("discovery") + runs_for("monitoring") + runs_for("calibration")
review_label = mo.ui.radio({"Unrequested change": True, "No unrequested change": False, "Insufficient evidence": None}, value="Insufficient evidence", label="Your label")
review_expected = mo.ui.text_area(label="What behavior should a corrected agent produce from this starting booking?", full_width=True)
review_reason = mo.ui.text_area(label="Which request and booking details support your label?", full_width=True)
review_span = mo.ui.text(label="Supporting native span URL", full_width=True)
_selected_review = next((r for r in _reviewable if r["stage_id"] == review_case.value), None)
_events = (_selected_review or {}).get("events", [])
review_event = mo.ui.dropdown({str(index + 1) + " · " + e["name"]: e["id"] for index, e in enumerate(_events)}, value="1 · " + _events[0]["name"] if _events else None, label="Operation supporting your review", full_width=True)
save_review = mo.ui.run_button(label="Save my turn review", disabled=not bool(_reviewable))
mo.vstack([mo.md("**Review before counting.** Include unflagged controls. Read the passenger's request and the whole booking; the native tag is the claim you are checking."), review_label, review_reason, review_expected, review_span, review_event, save_review]) if get_step() == "monitor" else mo.md("")
''')
add('''
mo.stop(not save_review.value)
_s = get_context()["session"]
_run = next(r for r in runs_for("discovery") + runs_for("monitoring") + runs_for("calibration") if r["stage_id"] == review_case.value)
_link = trace_url(_run)
mo.stop(not review_reason.value.strip() or not review_expected.value.strip(), mo.md("Explain the evidence and the expected behavior before saving the review."))
mo.stop(not _link or not review_span.value.startswith(_link + "/"), mo.md("Use a span in this selected run's verified Agent Lens conversation."))
_receipt = _s.read()["publications"].get("trace/" + _run["stage_id"], {})
_span_id = _receipt.get("span_ids", {}).get(review_event.value)
mo.stop(not _span_id or not review_span.value.rstrip("/").endswith("/" + _span_id), mo.md("The span URL must point to the selected operation. Open its link in the saved execution details."))
_turn_receipt = next((turn for turn in _receipt.get("turns", [_receipt]) if review_event.value in turn.get("span_ids", {})), None)
mo.stop(not _turn_receipt or ("/turns/" + _turn_receipt["trace_id"] + "/") not in review_span.value, mo.md("The selected operation belongs to another turn. Use its exact turn-and-span link."))
save_local("airline/review/" + _run["stage_id"] + "/" + _turn_receipt["trace_id"], {"stage_id": _run["stage_id"], "trace_id": _turn_receipt["trace_id"], "case_id": _run["case_id"], "human_label": review_label.value, "reason": review_reason.value, "span_url": review_span.value, "conversation_url": _link, "reviewer": _s.workspace_id, "expected_behavior": review_expected.value, "supporting_event_id": review_event.value, "decision": "accepted" if review_label.value is not None else "insufficient_evidence"})
_s.checkpoint("monitor")
''', cell_id="airline_monitoring/action/save_review")

add('''
_s = get_context().get("session")
_tag = saved("airline/tag-context")
_examples = (_tag or {}).get("result", {}).get("alignment", [])
alignment_picker = mo.ui.dropdown({row["id"] + " · " + row["conversation_id"][:10]: row["id"] for row in _examples}, value=_examples[0]["id"] + " · " + _examples[0]["conversation_id"][:10] if _examples else None, label="Native Alignment example", full_width=True)
refresh_alignment = mo.ui.run_button(label="Refresh native Alignment examples", disabled=not bool(_tag))
mo.vstack([mo.md("### Check the judge against your reviewed turn"), mo.md("Add the turn to this tag's Alignment set in Agent Lens, then refresh the examples. Choose a turn you also reviewed above. Running this explicit native test can incur a tag-judge charge outside the notebook allowance."), refresh_alignment, alignment_picker]) if get_step() == "monitor" else mo.md("")
''')
add('''
mo.stop(not refresh_alignment.value)
_s = get_context()["session"]
_tag = saved("airline/tag-context")["result"]
_client = agent_lens.LensClient(_s.project)
try: _examples = _client.alignment(_tag["tag_id"])
finally: _client.close()
save_local("airline/tag-context", {**_tag, "alignment": _examples})
''', cell_id="airline_monitoring/action/refresh_alignment")
add('''
_tag = saved("airline/tag-context")
_examples = (_tag or {}).get("result", {}).get("alignment", [])
_example = next((row for row in _examples if row["id"] == alignment_picker.value), None)
_review = review_for(_example["conversation_id"], _example["trace_id"]) if _example else None
run_alignment_test = mo.ui.run_button(label="Test the saved criteria on this reviewed turn", disabled=not bool(_review and _review["result"]["human_label"] is not None))
calculate_monitor = mo.ui.run_button(label="Calculate agreement with my reviews", disabled=not checked("monitor"))
mo.vstack([run_alignment_test, calculate_monitor, mo.md("An explicit completed test with an empty result list is a negative result. An absent live assignment still has unknown processing status. These are different observations.")]) if get_step() == "monitor" else mo.md("")
''')
add('''
mo.stop(not run_alignment_test.value)
_s = get_context()["session"]
_tag = saved("airline/tag-context")["result"]
_result = agent_lens.test_alignment(_s, _tag["tag_id"], alignment_picker.value, _tag["snapshot"]["criteria"])
show("alignment-test", _result)
refresh()
''', cell_id="airline_monitoring/action/run_alignment_test")
add('''
mo.stop(not calculate_monitor.value)
_s = get_context()["session"]
_fn = teaching.compile_code(source_for("monitor"))["my_monitor"]
_rows = []
_tag = saved("airline/tag-context")["result"]
for _test in _s.read().get("native_alignment", {}).values():
    if _test["tag_id"] != _tag["tag_id"] or _test["criteria_fingerprint"] != digest(_tag["snapshot"]["criteria"]):
        continue
    _review = review_for(_test["example"]["conversation_id"], _test["example"]["trace_id"])
    if _review:
        _rows.append({"prediction": _test.get("prediction"), "human_label": _review["result"]["human_label"], "status": _test["status"], "test_id": _test["id"]})
_result = _fn(_rows)
save_local("airline/monitor-agreement", {"metrics": _result, "rows": _rows}, sources={"monitor.py": source_for("monitor")})
show("monitor-agreement", {**_result, "scope": "Explicit native tests paired with reviews of the same turn; live requests and labeled calibration drills may both be represented"})
''', cell_id="airline_monitoring/action/calculate_monitor")

add('''
_s = get_context().get("session")
curation_editor = mo.ui.code_editor(value=source_for("curation"), language="python", on_change=lambda text: save_source("curation", text), debounce=False)
check_curation = mo.ui.run_button(label="Check my regression-case builder", disabled=not bool(_s))
save_regression = mo.ui.run_button(label="Save reviewed regression cases", disabled=not checked("curation"))
mo.vstack([mo.Html(ui.step("Turn a reviewed incident into a repeatable case", "Complete case_from_reviewed_turn. Keep the original request, starting booking, policy, expected behavior, and source links. Preserve an unflagged control as well as the incident.", "The case can be replayed from its starting booking. It contains a reviewed expectation, not just a transcript or a tag name.")), curation_editor, mo.accordion({"Hint": mo.md("A final booking alone cannot recreate the mistake. Save the state before the first tool call and the participant's reviewed expectation."), "Worked regression-case builder": mo.md("```python" + chr(10) + teaching.ANSWERS["curation"] + chr(10) + "```")}), check_curation, save_regression, mo.md("Discovery and monitor-check reviews can enter this dataset. Controlled calibration cases retain their drill label and stay separate from live traffic. Reserved evaluation and subsequent traffic stay out of repair inputs.")]) if get_step() == "curate" else mo.md("")
''')
add('''
mo.stop(not check_curation.value)
try: show("check/curation", check_source("curation", teaching.check_curation))
except Exception as _error: show("check/curation", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_curation")
add('''
mo.stop(not save_regression.value)
_s = get_context()["session"]
_fn = teaching.compile_code(source_for("curation"))["case_from_reviewed_turn"]
_rows = []
for _run in runs_for("discovery") + runs_for("monitoring") + runs_for("calibration"):
    _review = review_for(_run["stage_id"])
    if _review and _review["result"]["human_label"] is not None:
        _rows.append(_fn(_review["result"], _run))
mo.stop(not _rows, mo.md("Save at least one reviewed turn in Check new traffic first. Include an unflagged control before treating this as a balanced regression set."))
save_local("airline/regression", {"cases": _rows, "dataset_version": digest(_rows), "source": "Reviewed development traffic and explicitly labeled controlled calibration incidents"}, sources={"curation.py": source_for("curation")})
_s.checkpoint("curate")
show("curation", {"reviewed_cases": len(_rows), "dataset_version": digest(_rows)})
''', cell_id="airline_monitoring/action/save_regression")

add('''
_s = get_context().get("session")
scorer_editor = mo.ui.code_editor(value=source_for("state_scorer"), language="python", on_change=lambda text: save_source("state_scorer", text), debounce=False)
judge_editor = mo.ui.code_editor(value=source_for("judge_validation"), language="python", on_change=lambda text: save_source("judge_validation", text), debounce=False)
judge_rubric = mo.ui.text_area(value=_s.get_draft("airline/judge-rubric", "Judge whether the explanation agrees with the actual booking operations, distinguishes pending confirmation from completion, and describes unresolved issues accurately. Return the structured fields required by my_judge_validation. A valid response format does not establish that the judgment is correct.") if _s else "", label="Explanation-judge rubric", on_change=lambda text: _s.save_draft("airline/judge-rubric", text) if _s else None, full_width=True)
check_state_scorer = mo.ui.run_button(label="Check my booking scorer", disabled=not bool(_s))
check_judge_validation = mo.ui.run_button(label="Check my judge-response validator", disabled=not bool(_s))
save_evaluation_code = mo.ui.run_button(label="Save my development evaluation code", disabled=not (checked("state_scorer") and checked("judge_validation")))
mo.vstack([mo.Html(ui.step("Compare the booking and the explanation separately", "Implement my_state_scorer and my_judge_validation. The state scorer checks requested changes and untouched flights. The judge examines whether the explanation matches recorded work; it cannot replace a booking check.", "A well-formed but incorrect judgment and an unavailable judgment remain different outcomes.")), scorer_editor, check_state_scorer, judge_editor, judge_rubric, check_judge_validation, mo.accordion({"Worked booking scorer": mo.md("```python" + chr(10) + teaching.ANSWERS["state_scorer"] + chr(10) + "```"), "Worked judge validator": mo.md("```python" + chr(10) + teaching.ANSWERS["judge_validation"] + chr(10) + "```")}), save_evaluation_code]) if get_step() == "curate" else mo.md("")
''')
add('''
mo.stop(not check_state_scorer.value)
try: show("check/state_scorer", check_source("state_scorer", teaching.check_state_scorer))
except Exception as _error: show("check/state_scorer", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_state_scorer")
add('''
mo.stop(not check_judge_validation.value)
try: show("check/judge_validation", check_source("judge_validation", teaching.check_judge_validation))
except Exception as _error: show("check/judge_validation", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_judge_validation")
add('''
mo.stop(not save_evaluation_code.value)
_sources = {"state_scorer.py": source_for("state_scorer"), "judge_validation.py": source_for("judge_validation")}
save_local("airline/evaluation-code", {"sources": _sources, "rubric": judge_rubric.value, "source_fingerprint": digest(_sources)}, sources=_sources)
show("evaluation-code", {"status": "Development evaluation saved", "next": "Use this code on matched development bookings. Final booking checks remain independently fixed."})
''', cell_id="airline_monitoring/action/save_evaluation_code")

add('''
_s = get_context().get("session")
itinerary_editor = mo.ui.code_editor(value=source_for("itinerary_builder"), language="python", on_change=lambda text: save_source("itinerary_builder", text), debounce=False)
check_repair = mo.ui.run_button(label="Check my itinerary repair", disabled=not bool(_s))
run_regression = mo.ui.run_button(label="Run my curated regression cases", disabled=not (checked("itinerary_builder") and bool(saved("airline/evaluation-code")) and bool(saved("airline/regression"))))
_regression = saved("airline/regression-check")
_regression_ready = bool(_regression and _regression["result"].get("passed") and _regression["result"].get("notebook_builder_source") == digest(source_for("itinerary_builder")) and _regression["result"].get("dataset_fingerprint") == digest(saved("airline/regression")["result"]["cases"]))
run_development = mo.ui.run_button(label="Compare on four development bookings", disabled=not _regression_ready)
mo.vstack([mo.Html(ui.step("Preserve the flights the passenger did not ask to change", "Complete my_itinerary_builder(current_flights, replace_start, replace_stop, replacement_flights). Return the untouched prefix, the requested replacement, and the untouched suffix. The repaired agent can call this helper before submitting the full itinerary.", "The free check replaces a connecting outbound trip with a nonstop flight while keeping the return trip. Then inspect what the real agent chooses to do.")), itinerary_editor, mo.accordion({"Hint": mo.md("The replacement interval is half-open: include replace_start, exclude replace_stop. Validate its bounds and avoid mutating the original list."), "Worked itinerary builder": mo.md("```python" + chr(10) + teaching.ANSWERS["itinerary_builder"] + chr(10) + "```")}), check_repair, mo.md("Run the cases you curated against the deliberately incomplete adapter and your repair. This local test executes tools and booking checks without a model. It must pass before comparing the live agents."), run_regression, run_development, mo.md("The free legacy-adapter example is a labeled implementation drill. The live starting agent uses the real complete-itinerary API and may already succeed. Keep ties and regressions in the comparison.")]) if get_step() == "repair" else mo.md("")
''')
add('''
mo.stop(not check_repair.value)
try: show("check/itinerary_builder", check_source("itinerary_builder", teaching.check_itinerary_builder))
except Exception as _error: show("check/itinerary_builder", {"error": str(_error)})
''', cell_id="airline_monitoring/action/check_repair")
add('''
mo.stop(not run_regression.value)
_s = get_context()["session"]
_cases = saved("airline/regression")["result"]["cases"]
_builder = teaching.compile_code(source_for("itinerary_builder"))["my_itinerary_builder"]
_scorer_source = saved("airline/evaluation-code")["result"]["sources"]["state_scorer.py"]
_scorer = teaching.compile_code(_scorer_source)["my_state_scorer"]
_result = airline_regression.run_regressions(_s, _cases, itinerary_builder=_builder, state_scorer=_scorer)
save_local("airline/regression-check", {**_result, "notebook_builder_source": digest(source_for("itinerary_builder"))})
show("regression-check", _result)
refresh()
''', cell_id="airline_monitoring/action/run_regression")
add('''
mo.stop(not run_development.value)
_builder = teaching.compile_code(source_for("itinerary_builder"))["my_itinerary_builder"]
show("development", {"baseline": batch("development"), "repaired": batch("development", "repaired", _builder)})
save_local("airline/development-complete", {"source": source_for("itinerary_builder"), "fingerprint": digest(source_for("itinerary_builder")), "instrumentation": source_for("instrumentation"), "regression_fingerprint": saved("airline/regression-check")["result"]["dataset_fingerprint"], "stage_ids": saved_ids(["development"])})
get_context()["session"].checkpoint("repair")
refresh()
''', cell_id="airline_monitoring/action/run_development")

add('''
_dev = runs_for("development")
judge_case = mo.ui.dropdown({r["label"] + " · " + r["case_id"]: r["stage_id"] for r in _dev}, value=_dev[0]["label"] + " · " + _dev[0]["case_id"] if _dev else None, label="Development explanation to judge", full_width=True)
run_explanation_judge = mo.ui.run_button(label="Judge this saved explanation", disabled=not bool(_dev and saved("airline/evaluation-code")))
mo.vstack([mo.md("### Does the explanation match the booking?"), mo.md("Use your saved rubric and validator on one completed development request. This explicit button makes a billed model call; repeating it with the same evidence and rubric reuses the saved judgment. Compare its reason with the independent booking checks."), judge_case, run_explanation_judge]) if get_step() == "repair" else mo.md("")
''')
add('''
mo.stop(not run_explanation_judge.value)
_s = get_context()["session"]
_code = saved("airline/evaluation-code")["result"]
_run = next(r for r in runs_for("development") if r["stage_id"] == judge_case.value)
_validator = teaching.compile_code(_code["sources"]["judge_validation.py"])["my_judge_validation"]
try:
    _result = airline.judge_explanation(_s, _run, rubric=_code["rubric"], validator=_validator, **hooks())
    show("explanation-judge", _result)
except Exception as _error:
    show("explanation-judge", {"status": "unavailable", "error": str(_error), "judgment": None, "next": "Review the saved attempt before retrying. A missing judgment is not a failed booking."})
refresh()
''', cell_id="airline_monitoring/action/run_explanation_judge")

add('''
_s = get_context().get("session")
freeze_version = mo.ui.run_button(label="Freeze the tested repair", disabled=not bool(saved("airline/development-complete")))
run_final = mo.ui.run_button(label="Evaluate six reserved bookings", disabled=not bool(saved("airline/frozen")))
mo.vstack([mo.Html(ui.step("Stop editing and evaluate on reserved requests", "Freeze the tested itinerary builder and the monitoring criteria. Run both versions on six reserved bookings from the same starting states. The independent final scorer and the booking targets stay fixed.", "Open one aligned case in EvalTables and explain the booking change behind its score. A higher aggregate number is not enough.")), freeze_version, run_final, mo.md("This comparison adds twelve conversations. Reopening the notebook or retrying publication reuses their saved results. Reserved outcomes must not enter further repair or tag tuning in this workshop run.")]) if get_step() == "final" else mo.md("")
''')
add('''
mo.stop(not freeze_version.value)
_s = get_context()["session"]
_development = saved("airline/development-complete")["result"]
mo.stop(_development["fingerprint"] != digest(source_for("itinerary_builder")) or _development["instrumentation"] != source_for("instrumentation") or _development["regression_fingerprint"] != digest(saved("airline/regression")["result"]["cases"]), mo.md("The itinerary code, tracing code, or curated regression dataset changed after the development comparison. Test this version before freezing it."))
_tag = saved("airline/tag-context")["result"]
_snapshot = agent_lens.save_tag_snapshot(_s, _tag["tag_id"], _tag["agent_name"], require_enabled=True)
save_local("airline/frozen", {"source": _development["source"], "fingerprint": _development["fingerprint"], "instrumentation": _development["instrumentation"], "regression_fingerprint": _development["regression_fingerprint"], "tag": _snapshot, "tag_id": _tag["tag_id"], "agent_name": _tag["agent_name"], "development_ids": _development["stage_ids"]}, sources={"itinerary_builder.py": _development["source"]})
show("freeze", {"status": "Frozen", "fingerprint": _development["fingerprint"]})
''', cell_id="airline_monitoring/action/freeze_version")
add('''
mo.stop(not run_final.value)
_frozen = saved("airline/frozen")["result"]
_builder = teaching.compile_code(_frozen["source"])["my_itinerary_builder"]
show("final", {"baseline": batch("final"), "repaired": batch("final", "repaired", _builder)})
get_context()["session"].checkpoint("final")
refresh()
''', cell_id="airline_monitoring/action/run_final")

add('''
run_subsequent = mo.ui.run_button(label="Monitor four subsequent requests", disabled=len(runs_for("final")) != 12)
read_subsequent = mo.ui.run_button(label="Read the subsequent batch's tag results", disabled=len(runs_for("subsequent")) != 8)
mo.vstack([mo.Html(ui.step("Check the same monitor on the next batch", "Run both frozen versions on four new requests. Keep the saved monitoring criteria unchanged and inspect remaining problems, including requests that received no tag assignment.", "Explain what happened to agent quality and what the monitor can actually observe.")), run_subsequent, read_subsequent, mo.md("A native tag assignment is positive evidence. No assignment is ambiguous: processing may be pending or the rule may not have matched. Do not report it as a completed negative or infer processing coverage.")]) if get_step() == "traffic" else mo.md("")
''')
add('''
mo.stop(not run_subsequent.value)
_s = get_context()["session"]
_frozen = saved("airline/frozen")["result"]
_current = agent_lens.save_tag_snapshot(_s, _frozen["tag_id"], _frozen["agent_name"], require_enabled=True)
# Native adapter checks the criteria identity before the comparison; do not silently retune it.
mo.stop(_current.get("criteria") != _frozen["tag"].get("criteria"), mo.md("The live criteria changed after freezing. Restore the saved criteria before running this comparison."))
_builder = teaching.compile_code(_frozen["source"])["my_itinerary_builder"]
show("subsequent", {"baseline": batch("subsequent"), "repaired": batch("subsequent", "repaired", _builder)})
_s.checkpoint("traffic")
refresh()
''', cell_id="airline_monitoring/action/run_subsequent")
add('''
mo.stop(not read_subsequent.value)
_s = get_context()["session"]
_frozen = saved("airline/frozen")["result"]
try:
    _native = agent_lens.read_monitoring(_s, _frozen["tag_id"], [r["stage_id"] for r in runs_for("subsequent")], _frozen["agent_name"])
    save_local("airline/subsequent-readback", _native)
    show("subsequent-native", _native)
except Exception as _error: show("subsequent-native", {"status": "unavailable", "error": str(_error)})
refresh()
''', cell_id="airline_monitoring/action/read_subsequent")

add('''
def publish_saved_comparisons():
    session = get_context()["session"]
    statuses = {}
    for phase in ("development", "final", "subsequent"):
        versions = {label: runs_for(phase, label) for label in ("baseline", "repaired")}
        expected = {"development": 4, "final": 6, "subsequent": 4}[phase]
        if any(len(rows) != expected for rows in versions.values()):
            statuses[phase] = {"status": "not complete", "counts": {key: len(value) for key, value in versions.items()}}
            continue
        try:
            statuses[phase] = publish_comparison(session, "airline-" + phase, {label: airline.comparison_rows(rows) for label, rows in versions.items()})
        except Exception as error:
            statuses[phase] = {"status": "publication pending", "error": str(error), "next": "Retry from saved results. Do not repeat agent execution."}
    return statuses
''', cell_id="airline_monitoring/publication")
add('''
_s = get_context().get("session")
publish_results = mo.ui.run_button(label="Publish saved comparisons", disabled=not bool(_s and runs_for("development")))
conclusion = mo.ui.text_area(value=_s.get_draft("airline/conclusion", "") if _s else "", label="What changed in the agent, the monitor, and the evaluation suite? Include one remaining problem and the next test.", on_change=lambda text: _s.save_draft("airline/conclusion", text) if _s else None, full_width=True)
publish_report = mo.ui.run_button(label="Publish my conclusion", disabled=len(runs_for("subsequent")) != 8)
confirm_tag_off = mo.ui.run_button(label="Verify automatic tagging is off", disabled=not bool(saved("airline/tag-context")))
mo.vstack([mo.Html(ui.step("Write down what the comparison supports", "Separate booking quality from monitoring agreement and tool errors. Link one claim to its trace and matching case. Name what remains unresolved rather than describing every valid judge response as correct.", "Your Report links back to the saved code and results. Turn off Apply with AI for this workshop tag and verify the change below.")), publish_results, conclusion, publish_report, mo.md("**Stop automatic judging:** open your native tag, disable Apply with AI, save it, then click the verification button. Closing the notebook does not disable the tag."), confirm_tag_off]) if get_step() == "report" else mo.vstack([mo.md("Publish the saved predictions to compare matching requests in Forge. This button never sends another passenger request."), publish_results]) if get_step() in ("final", "traffic") else mo.md("")
''')
add('''
mo.stop(not publish_results.value)
show("publication", publish_saved_comparisons())
refresh()
''', cell_id="airline_monitoring/action/publish_results")
add('''
mo.stop(not publish_report.value)
mo.stop(not conclusion.value.strip(), mo.md("Explain one observed outcome and one remaining limitation first."))
_s = get_context()["session"]
save_local("airline/conclusion", {"text": conclusion.value})
_statuses = publish_saved_comparisons()
_links = ui.stage_links(_s, saved_ids(["development", "final", "subsequent"]))
_links.update({"Agent Lens": "https://forge.coreweave.com/agent-lens/" + _s.project})
try:
    _report = write_report(_s, conclusion.value, _links)
    save_local("airline/report-receipt", {"status": "Published", "url": _report})
    show("report", {"status": "Published", "url": _report})
    _s.checkpoint("report", evidence=_links)
except Exception as _error:
    show("report", {"status": "Conclusion saved; publication pending", "error": str(_error)})
refresh()
''', cell_id="airline_monitoring/action/publish_report")
add('''
mo.stop(not confirm_tag_off.value)
_s = get_context()["session"]
_tag = saved("airline/tag-context")["result"]
try:
    _snapshot = agent_lens.save_tag_snapshot(_s, _tag["tag_id"], _tag["agent_name"])
    mo.stop(_snapshot.get("llm_judge_enabled") is not False, mo.md("Automatic judging is still enabled or its state is unknown. Disable Apply with AI in the native tag, save, and read it again."))
    save_local("airline/tag-disabled", _snapshot)
    show("tag-off", {"status": "Native readback confirms automatic judging is off"})
except Exception as _error:
    show("tag-off", {"status": "Not verified", "error": str(_error)})
refresh()
''', cell_id="airline_monitoring/action/confirm_tag_off")

add('''
_s = get_context().get("session")
_revision = get_revision()
_phase = {"discovery": "discovery", "investigate": "discovery", "monitor": "monitoring", "repair": "development", "final": "final", "traffic": "subsequent"}.get(get_step())
_current_runs = (runs_for(_phase) if _phase else []) + (runs_for("calibration") if get_step() in ("investigate", "align") else [])
run_picker = mo.ui.dropdown({r["label"] + " · " + r["case_id"]: r["stage_id"] for r in _current_runs}, value=_current_runs[0]["label"] + " · " + _current_runs[0]["case_id"] if _current_runs else None, label="Saved execution to inspect", full_width=True)
mo.vstack([mo.md("### Compare the booking with the request"), mo.ui.table([{"Request": r["case_id"], "Version": r["label"], "Completed": r["status"], "Booking checks": r.get("scores", {}).get("task_success"), "Origin": r.get("scenario_origin", "Live simulator agent"), "Model attempts": r.get("model_attempts"), "Time (s)": r.get("elapsed_seconds"), "Measured cost (USD)": r.get("cost_usd"), "Unresolved cost bound (USD)": r.get("bounded_unknown_usd")} for r in _current_runs], selection=None), run_picker]) if _current_runs else mo.md("")
''')
add('''
_s = get_context().get("session")
mo.stop(not _s or not run_picker.value)
_run = next((r for phase in ("discovery", "monitoring", "development", "final", "subsequent", "calibration") for r in runs_for(phase) if r["stage_id"] == run_picker.value), None)
mo.stop(not _run)
_before = _run["initial_state"]["reservation"]["flights"]
_after = _run["world"]["reservation"]["flights"]
_flights = [{"When": when, "Flight": f["flight_number"], "Date": f["date"], "From": f.get("origin"), "To": f.get("destination")} for when, flights in (("Before", _before), ("After", _after)) for f in flights]
mo.vstack([mo.md("**Passenger request:** " + _run["mission"]), mo.ui.table(_flights, selection=None), mo.md("**Agent's explanation:** " + ((_run.get("draft") or {}).get("summary", "No final explanation saved.") if isinstance(_run.get("draft"), dict) else str(_run.get("draft") or "No final explanation saved."))), mo.Html(ui.result("Independent booking checks", _run.get("scores", {}))), ui.evidence(mo, _s, [_run["stage_id"]], "Find update_reservation_flights. Compare its complete flight list with the unchanged flights above."), mo.accordion({"Arguments, observations, messages, and execution receipt": mo.json(_run)})])
''')

add('''
_revision = get_revision()
_prefixes = {"setup": ("setup", "check/instrumentation"), "investigate": ("insights", "calibration"), "align": ("align", "calibration"), "monitor": ("check/monitor", "monitoring-native", "alignment-test", "monitor-agreement"), "curate": ("check/curation", "check/state_scorer", "check/judge_validation", "curation", "evaluation-code"), "repair": ("check/itinerary_builder", "regression-check", "explanation-judge"), "final": ("freeze", "publication"), "traffic": ("subsequent-native", "publication"), "report": ("publication", "report", "tag-off")}
_items = []
for _key in _prefixes.get(get_step(), ()):
    _value = get_output().get(_key)
    if _value is None and _key.startswith("check/") and get_context().get("session"):
        _value = get_context()["session"].read().get("airline_checks", {}).get(_key.split("/", 1)[1], {}).get("result")
    if _value is None:
        _saved_names = {"insights": "airline/insights-status", "align": "airline/tag-context", "monitoring-native": "airline/monitor-readback", "monitor-agreement": "airline/monitor-agreement", "curation": "airline/regression", "evaluation-code": "airline/evaluation-code", "regression-check": "airline/regression-check", "freeze": "airline/frozen", "subsequent-native": "airline/subsequent-readback", "tag-off": "airline/tag-disabled", "report": "airline/report-receipt"}
        _record = saved(_saved_names[_key]) if _key in _saved_names else None
        _value = _record["result"] if _record else None
    if _value:
        if isinstance(_value, dict) and isinstance(_value.get("url"), str): _items.append(mo.Html(ui.links({"Open saved result": _value["url"]})))
        if _key == "regression-check" and _value.get("rows"):
            _items.extend([mo.md("### Replay your curated cases\\nThese are controlled local adapter comparisons on the saved original bookings. They use no model calls. A tie is valid when both adapters preserve the requested itinerary."), mo.ui.table([{"Case": row["case_id"], "Source": row.get("origin"), "Omission adapter passes": row["legacy"]["scores"]["task_success"], "My repair passes": row["repaired"]["scores"]["task_success"], "Omission adapter flights": [f["flight_number"] for f in row["legacy"].get("planned_flights", [])], "My repair flights": [f["flight_number"] for f in row["repaired"].get("planned_flights", [])]} for row in _value["rows"]], selection=None)])
        if _key in ("monitoring-native", "subsequent-native") and _value.get("rows"):
            _items.extend([mo.md("### Native tag readback\\nAn observed assignment is a match. No assignment observed does not establish a negative judgment: the turn may be unprocessed or may not match. Processing coverage is unavailable from this response."), mo.ui.table([{"Conversation": row["conversation_id"], "Native status": row["status"], "Finding": row.get("explanation", ""), "Open conversation": row.get("url", "")} for row in _value["rows"]], selection=None)])
        if _key != "publication":
            _items.append(mo.Html(ui.result(_key.replace("check/", "Free check · ").replace("-", " ").title(), {k: v for k, v in _value.items() if not isinstance(v, (list, dict))} if isinstance(_value, dict) else {"Result": _value}, detail=_value)))
if get_step() in ("repair", "final", "traffic", "report") and get_context().get("session"):
    _items.append(ui.publication(mo, get_context()["session"], names=("airline-development", "airline-final", "airline-subsequent")))
mo.vstack(_items) if _items else mo.md("")
''')

add('''
_s = get_context().get("session")
_revision = get_revision()
_failed = _s.recovery_options() if _s else []
recovery_choice = mo.ui.dropdown({setup.recovery_label(_s.workshop, row) + " · " + row["id"][:6]: row["id"] for row in _failed}, value=setup.recovery_label(_s.workshop, _failed[0]) + " · " + _failed[0]["id"][:6] if _failed else None, label="Saved attempt to review", full_width=True)
confirm_stopped = mo.ui.checkbox(label="I checked that this execution has stopped; keep unresolved requests charged at their reserved maximum.")
retry_execution = mo.ui.run_button(label="Allow retry of this failed execution", disabled=not bool(_failed))
retry_publications = mo.ui.run_button(label="Retry saved trace and result publications", disabled=not bool(_s))
mo.accordion({"A request or upload stopped?": mo.vstack([mo.md("A saved result does not need another model call. Retry publications for missing traces or comparisons. For a stopped execution, review its status, allow another attempt, then use its normal run button. Successful sibling requests are reused."), recovery_choice, confirm_stopped, retry_execution, retry_publications])})
''')
add('''
mo.stop(not retry_execution.value)
_s = get_context()["session"]
try:
    _retry = _s.retry_stage(recovery_choice.value, confirm_stopped=confirm_stopped.value)
    show("recovery", {"status": "Retry allowed", "attempt": _retry["attempt"], "next": "Use the original run control. This action did not execute a request."})
except Exception as _error: show("recovery", {"error": str(_error)})
refresh()
''', cell_id="airline_monitoring/action/retry_execution")
add('''
mo.stop(not retry_publications.value)
_s = get_context()["session"]
_statuses = {}
for _record in _s.read()["stages"].values():
    _has_requests = any(key.startswith(_record["id"] + "/") for key in _s.read()["requests"])
    if _record["name"].startswith(("airline/", "airline-calibration/")) and (_has_requests or _record.get("events") or (_record.get("result") or {}).get("events")):
        try:
            _inputs = saved_trace_inputs(_s, _record["id"])
            _result = _record.get("result") or {}
            _judge = _record["name"].startswith("airline/judge/")
            _inputs.setdefault("agent_name", "airline-judge-" + _s.workspace_id if _judge else native_scope())
            if _result.get("case_id"):
                _inputs.setdefault("attributes", {"airline.version": _result.get("label"), "airline.partition": _result.get("split"), "airline.case_id": _result["case_id"]})
                _inputs.setdefault("conversation_name", ("CONTROLLED CALIBRATION / " if _result.get("split") == "calibration" else "Airline / " + _result.get("label", "") + " / ") + _result["case_id"])
            _source = _record.get("sources", {})
            _writers = hooks(_source["tool_writer.py"] + chr(10) + _source["model_writer.py"]) if "tool_writer.py" in _source and "model_writer.py" in _source else {}
            _statuses[_record["id"]] = export_trace(_s, **_inputs, **_writers)
        except Exception as _error: _statuses[_record["id"]] = {"status": "unavailable", "error": str(_error)}
_statuses["comparisons"] = publish_saved_comparisons()
show("recovery", _statuses)
refresh()
''', cell_id="airline_monitoring/action/retry_publications")
add('''
_recovery = get_output().get("recovery")
mo.Html(ui.result("Recovery status", {key: value for key, value in _recovery.items() if not isinstance(value, (list, dict))}, detail=_recovery)) if _recovery else mo.md("")
''')

add('''
_s = get_context().get("session")
help_text = mo.ui.text_area(label="Tell the facilitator which step is confusing or blocked", full_width=True)
request_help = mo.ui.run_button(label="Send a help request", disabled=not bool(_s))
mo.accordion({"Ask the facilitator": mo.vstack([help_text, request_help])})
''')
add('''
mo.stop(not request_help.value)
get_context()["session"].request_help(help_text.value)
show("help", {"status": "Help request saved"})
''', cell_id="airline_monitoring/action/request_help")
add('''
airline_current_step = get_step()
''', cell_id="airline_monitoring/current_step")
add('''
_index = [key for key, label in STEPS].index(airline_current_step)
_next = STEPS[min(_index + 1, len(STEPS) - 1)]
next_step = ui.next_step(mo, _next[1], _next[0], go_to)
next_step if _index < len(STEPS) - 1 else mo.md("Keep the exact code, case, and result behind one conclusion. You can return to this notebook without contacting the facilitator.")
''')
