"""Authored transit workshop: participant functions control the builders."""
from notebook_builder import Cell
cells=[]
def add(code, hide=False): cells.append(Cell(code,hide=hide))

add('''
import json
from pathlib import Path
import marimo as mo
from forge_workshop_kit import WorkshopSession, setup, ui
from forge_workshop_kit import factory, transit, factory_teaching as teaching
from forge_workshop_kit import transit_workshop as lab
from forge_workshop_kit.traces import event, export_trace, saved_trace_inputs
from forge_workshop_kit.session import digest
get_context, set_context = mo.state({})
get_step, set_step = mo.state("setup", allow_self_loops=True)
get_revision, set_revision = mo.state(0)
get_output, set_output = mo.state({})
draft_cache = {}
''', True)
add('''
def refresh():
    set_revision(get_revision()+1)
def go_to(step):
    session=get_context().get("session")
    if session: session.set_view(step)
    set_step(step)
def show(name, result):
    set_output(lambda values:{**values,name:result})
def current_session():
    return get_context().get("session")
def read_draft(name, default):
    session=current_session()
    return session.get_draft("factory/"+name,draft_cache.get(name,default)) if session else draft_cache.get(name,default)
def save_draft(name, text):
    draft_cache[name]=text
    session=current_session()
    if session: session.save_draft("factory/"+name,text)
def active_sources():
    session=current_session()
    return teaching.capture_sources(session, ["worker","tasks","memory","evaluate","release"])
def export_saved_traces():
    return lab.publish_traces(current_session(),tool_writer=instrument_tool)
''', True)
add('''
_s=current_session()
_revision=get_revision()
step_navigation=ui.navigation(mo,teaching.STEPS,get_step(),go_to,completed=teaching.complete_steps(_s),label="Build and release")
mo.vstack([mo.Html(ui.STYLE),step_navigation,mo.Html(ui.context(_s)) if _s else mo.md("Copy this notebook into your Forge project. You will write the code that gives agents work and checks what they produce.")])
''', True)
add('''
mo.stop(get_step()!="setup")
mo.vstack([mo.md("**6-hour workshop, including breaks and exercises.** [Open the companion deck](https://ash0ts.github.io/forge-workshop-kit/transit/). Its worked examples explain the code you will edit below."),mo.Html(ui.heading("Build a transit app with a team of coding agents","People leaving an evening event need the next departures and the last service home. Your team is building the departure board. You'll give two coding agents separate tasks, test their combined work, and decide what the next builders should remember.",theme="neutral",eyebrow="Six-hour software factory workshop")),mo.md("The schedule is real: a frozen MBTA GTFS feed for **November 28 to December 4, 2024**. GTFS joins routes, trips, stops, service calendars, and stop times. You'll inspect those records before asking agents to change code. The app displays historical scheduled departures, not live arrival predictions."),mo.md("**Your output:** a departure board you can run, the coordinator you wrote, and a release linked to its tests and Agent Lens conversations. The first work order adds next departures. The second adds the last departure tonight and an itinerary download."),mo.md("A software factory connects a request to assignments, code, integration tests, and a release decision. The builder agents write the app's query and display modules. You write the task selection, handoffs, memory retrieval, and checks around them."),mo.md("[GTFS source and terms](https://github.com/mbta/gtfs-documentation) · [Software-factory background](https://factory.strongdm.ai/) · [Workshop source](https://github.com/ash0ts/forge-workshop-kit/blob/main/notebooks/transit_factory.py)")])
''',True)
add('''
_env=setup.project_context()
project=mo.ui.text(value=_env["project"],label="Your Forge project",disabled=_env["hosted"] and _env["detected"],full_width=True)
allowance=mo.ui.number(value=8,start=.01,stop=1000,label="Inference allowance in USD; notebook compute is separate")
connect=mo.ui.run_button(label="Connect and restore my work")
mo.vstack([project,allowance,connect,mo.md("On your laptop: `uv sync --frozen`, `uv run wandb login`, then `uv run marimo edit notebooks/transit_factory.py`. In Forge, copy the template into a project you can write to. Setup and the local checks make no model calls.")]) if get_step()=="setup" else mo.md("")
''',True)
add('''
mo.stop(not connect.value)
_s=WorkshopSession.from_environment("transit-factory",project=project.value,budget_usd=allowance.value)
_access=_s.check_access()
_s.restore()
setup.save_access(_s,_access)
set_context({"session":_s})
set_step(_s.get_view("setup"))
refresh()
''',True)
add('''
# This function is used for the setup trace and every builder's tool span.
# Add the task ID attribute below, then find it on a real span in Agent Lens.
def instrument_tool(observation):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=observation["name"], arguments=observation["arguments"],
        result=observation["result"], tool_call_id=observation["id"],
        started_at=stamp(observation["started_at"]), ended_at=stamp(observation["ended_at"])) as span:
        span.set_attributes({"workshop.exercise":"transit-factory",
            "factory.task_id":observation.get("task_id",observation.get("arguments",{}).get("task_id","setup"))})
        if observation.get("error"): span.record_error(RuntimeError(observation["error"]))
        return format(trace.get_current_span().get_span_context().span_id,"016x")
''')
add('''
setup_trace=mo.ui.run_button(label="Send my first Agent Lens trace",disabled=not bool(current_session()))
mo.vstack([mo.md("Edit an attribute in `instrument_tool` above. This is the same function used to export the builders' recorded tool calls."),setup_trace]) if get_step()=="setup" else mo.md("")
''',True)
add('''
mo.stop(not setup_trace.value)
_s=current_session()
with _s.stage("factory/setup",config={"data":transit.data_manifest()}) as _stage:
    if _stage.needs_run:
        _data,_receipt=event("inspect_transit_source",{},lambda:lab.data_preview(),on_error=_stage.record_event)
        _stage.record({"data":_data,"events":[_receipt],"mission":"Inspect the historical MBTA schedule used for the departures board."})
try:
    _trace=export_trace(_s,**saved_trace_inputs(_s,_stage.id),tool_writer=instrument_tool)
    show("setup",_trace)
except Exception as _error:
    show("setup",{"status":"Trace publication pending","error":str(_error)})
_s.checkpoint("setup")
refresh()
''',True)
add('''
mo.stop(get_step()!="setup")
_data=lab.data_preview()
mo.vstack([mo.md("### Read one departure before writing code\\nA trip references a service calendar. Its stop times belong to that service day. After-midnight values can exceed 24:00:00. The feed date is part of the input, not the computer's current date."),mo.ui.table([{"Trip":row["trip_id"],"Platform":row["stop_id"],"GTFS departure":row["departure_time"],"Service calendar":row["service_id"]} for row in _data["departures"]],selection=None),mo.accordion({"Source, checksum, and extraction":mo.json(_data["manifest"])}),mo.md("Trip **63926435** has a **24:08:00** departure at Park Street on Thanksgiving's service calendar. That means **00:08 on November 29**, with **November 28** retained as its service date. At 00:05, a useful board must still include it. Write that requirement below before building the app.")])
''',True)
add('''
_s=current_session()
acceptance_code=mo.ui.code_editor(value=read_draft("acceptance",teaching.ACCEPTANCE_STARTER),language="python",on_change=lambda text:save_draft("acceptance",text),debounce=False)
acceptance_check=mo.ui.run_button(label="Check my after-midnight scenario")
mo.vstack([mo.md("### Write one acceptance scenario\\nComplete `check_departures(rows)`. Return True when the train above appears with both dates correct. Your check will also run on the combined app. The free check below uses the real public example, then removes the train and changes its service date to make sure your condition catches both errors."),acceptance_code,acceptance_check,mo.accordion({"Hint":mo.md("Use `any(...)` over the rows. Check `trip_id`, `service_date`, and `departure_time` together."),"Worked answer":mo.md("```python\\n"+teaching.ACCEPTANCE_SOLUTION+"\\n```")})]) if get_step()=="setup" else mo.md("")
''',True)
add('''
mo.stop(not acceptance_check.value)
save_draft("acceptance",acceptance_code.value)
try:
    _result=teaching.check_acceptance(acceptance_code.value)
    if current_session():
        current_session().save_draft("factory/acceptance",acceptance_code.value)
        lab.save_check(current_session(),"acceptance",acceptance_code.value,_result)
    show("acceptance check",_result)
except Exception as _error:
    show("acceptance check",{"status":"Needs a change","message":str(_error)})
refresh()
''',True)
add('''
mo.stop(get_step()!="setup")
_session=current_session()
_result=get_output().get("acceptance check") or (_session.read().get("factory_checks",{}).get("acceptance") if _session else None)
if _result and _result.get("source_fingerprint") != digest(acceptance_code.value): _result=None
mo.callout(mo.md("**Scenario passed.** The real departure passes; the missing train and wrong service day fail." if _result and _result.get("passed") else (_result or {}).get("message","Run your scenario check above. No model or training call is involved.")),kind="success" if _result and _result.get("passed") else "info")
''',True)

# One editor appears at the relevant step; drafts are saved independently.
for name in ('worker','tasks','memory','evaluate','release'):
    add(f'''
_s=current_session()
_revision=get_revision()
_spec=teaching.EXERCISES[{name!r}]
{name}_code=mo.ui.code_editor(value=read_draft("{name}",_spec["starter"]),language="python",on_change=lambda text:save_draft("{name}",text),debounce=False)
{name}_check=mo.ui.run_button(label="Check my "+_spec["function"]+" code")
mo.vstack([mo.Html(ui.step(_spec["function"],_spec["task"],"Run the free check before using this function in the workshop.")),{name}_code,{name}_check,mo.accordion({{"Hint":mo.md(_spec["hint"]),"Worked answer":mo.md("```python\\n"+_spec["solution"]+"\\n```")}})]) if get_step()=={name!r} else mo.md("")
''',True)
    add(f'''
mo.stop(not {name}_check.value)
save_draft("{name}",{name}_code.value)
try:
    _result=teaching.check_exercise({name!r},{name}_code.value)
    if current_session():
        current_session().save_draft("factory/{name}",{name}_code.value)
        lab.save_check(current_session(),{name!r},{name}_code.value,_result)
    show("{name} check",_result)
except Exception as _error:
    show("{name} check",{{"status":"Needs a change","message":str(_error)}})
refresh()
''',True)
    add(f'''
mo.stop(get_step()!={name!r})
_session=current_session()
_check=get_output().get("{name} check") or (_session.read().get("factory_checks",{{}}).get({name!r}) if _session else None)
mo.callout(mo.md("**Free check passed.** Your function handled the supplied examples." if _check and _check.get("status")=="passed" else (_check or {{}}).get("message","Complete the function above, then run its free check.")),kind="success" if _check and _check.get("status")=="passed" else "info")
''',True)

add('''
_s=current_session()
_revision=get_revision()
_ready=lab.can_run(_s,"solo")
run_solo=mo.ui.run_button(label="Run one worker on the first feature",disabled=not _ready)
mo.vstack([mo.md("The builder will edit `query.py` and `presentation.py` in separate tasks. One worker handles them sequentially. Its budget is the same as the two-worker build. Read the contract and the exact messages before running."),mo.accordion({"Approved work order and interface":mo.json(lab.work_order(1))}),run_solo,mo.md(lab.blocked(_s,"solo")) if not _ready else mo.md("Model calls start only when you click Run. Completed work is reused on restart.")]) if get_step()=="worker" else mo.md("")
''',True)
add('''
mo.stop(not run_solo.value)
_s=current_session()
_result=lab.run_initial(_s,"solo",worker_code.value,workers=1)
show("solo",_result)
show("traces",export_saved_traces())
_s.checkpoint("worker")
refresh()
''',True)
add('''
mo.stop(get_step()!="tasks")
_session=current_session()
_result=get_output().get("tasks check") or (_session.read().get("factory_checks",{}).get("tasks",{}) if _session else {})
_repair=_result.get("coordination_repair")
mo.vstack([mo.md("### Give each task an owner\\nThe two builders receive the same interface contract and starting files. One owns the departure query; one owns its display. If both threads check that a task is free before either writes its name, both can start the same work. `board.claim(...)` checks readiness and saves the owner in one short locked transaction. The lock is released before the model runs."),mo.md("```python\\n# Broken: another worker can claim between these operations.\\nif task[\\\"status\\\"] == \\\"pending\\\":\\n    task[\\\"owner\\\"] = worker_id\\n\\n# Repaired: check and write happen together inside the board.\\nclaim = board.claim(task_id, worker_id)\\n```"),mo.Html(teaching.task_board(lab.example_task_board())),mo.callout(mo.md("**Two real threads tried the same task.** The separate check/write allowed **"+str(_repair["before"]["successful_claims"])+" owners**. The atomic claim allowed **"+str(_repair["after"]["successful_claims"])+" owner**. This is a local implementation check; it says nothing yet about model quality or speed."),kind="success") if _repair else mo.md("Run **Check my ready_tasks code** above. It tests your functions and runs the two-thread claim race locally."),mo.md("**Explain:** a submitted patch is waiting for review. Only an integrated patch should unblock a task that depends on its code.")])
''',True)
add('''
_s=current_session()
_revision=get_revision()
_ready=lab.can_run(_s,"team")
run_team=mo.ui.run_button(label="Run the ready tasks with two workers",disabled=not _ready)
mo.vstack([mo.Html(ui.step("Run both builders","Use your ready_tasks and claim_task functions to start two independent builders from the same code as the one-worker run.","Open each worker's conversation in Agent Lens. Compare its assigned files and inspect the task claim before the first edit.")),run_team,mo.md(lab.blocked(_s,"team")) if not _ready else mo.md("The builders have separate files and contexts. They can send a message or propose follow-up work; they cannot silently change the approved assignment.")]) if get_step()=="team" else mo.md("")
''',True)
add('''
mo.stop(not run_team.value)
_s=current_session()
_result=lab.run_initial(_s,"team",worker_code.value,workers=2,task_code=tasks_code.value)
show("team",_result)
show("traces",export_saved_traces())
_s.checkpoint("team")
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
reviewed_patches=mo.ui.checkbox(label="I reviewed both builds' patches below and their development checks")
run_integration=mo.ui.run_button(label="Test the combined departures board",disabled=not lab.can_run(_s,"integrate"))
mo.vstack([mo.Html(ui.step("Review the patches together","Read the query and display diffs below. Both modules can pass their own checks while disagreeing about the interface.","The integration action applies reviewed patches and runs development scenarios. Final reserved scenarios remain separate.")),mo.Html(lab.patch_review(_s)),reviewed_patches,run_integration,mo.md(lab.blocked(_s,"integrate"))]) if get_step()=="integrate" else mo.md("")
''',True)
add('''
mo.stop(not run_integration.value)
mo.stop(not reviewed_patches.value,mo.md("Read the actual diffs and confirm the review above first."))
_result=lab.integrate_initial(current_session())
show("integrate",_result)
show("traces",export_saved_traces())
current_session().checkpoint("integrate")
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
_available=lab.can_run(_s,"prepared-reference")
continue_reference=mo.ui.run_button(label="Continue from the prepared reference app",disabled=not _available)
mo.vstack([mo.callout(mo.md("**The live builds did not produce a usable starting release.** Keep their failures in the comparison. You can continue the lesson exercise using the instructor's tested app. This does not repair, replace, or improve the recorded live builds."),kind="warn"),continue_reference]) if get_step()=="integrate" and _available else mo.md("")
''',True)
add('''
mo.stop(not continue_reference.value)
show("prepared reference",lab.use_prepared_reference(current_session()))
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
preview_stop=mo.ui.dropdown(lab.stop_choices(),value=next(iter(lab.stop_choices())),label="Stop")
preview_time=mo.ui.text(value="2024-11-29T00:05:00-05:00",label="Historical local time")
preview_version=mo.ui.dropdown({"One builder":"solo","Two builders":"team"},value="Two builders",label="Integrated version")
preview_app=mo.ui.run_button(label="Preview this saved app",disabled=not lab.can_run(_s,"preview"))
mo.vstack([mo.md("### Try the app\\nChoose a stop and time from the saved week. Previewing runs the reviewed Python locally; it makes no model requests."),mo.hstack([preview_stop,preview_version]),preview_time,preview_app]) if get_step()=="integrate" else mo.md("")
''',True)
add('''
mo.stop(not preview_app.value)
try:
    show("app",lab.preview(current_session(),preview_version.value,preview_stop.value,preview_time.value))
except Exception as _error:
    show("app",{"error":str(_error)})
''',True)
add('''
_s=current_session()
_revision=get_revision()
lesson_text=mo.ui.text_area(value=_s.get_draft("factory/lesson-text","") if _s else "",label="The rule you checked and where it applies",full_width=True,on_change=lambda text:_s.save_draft("factory/lesson-text",text) if _s else None)
lesson_evidence=mo.ui.dropdown(lab.lesson_evidence_options(_s),value=next(iter(lab.lesson_evidence_options(_s)),None),label="Supporting development result",full_width=True)
propose_lesson=mo.ui.run_button(label="Ask the agent to propose a lesson",disabled=not lab.can_run(_s,"memory"))
save_lesson=mo.ui.run_button(label="Save a checked lesson",disabled=not lab.can_run(_s,"memory"))
mo.vstack([mo.md("### Decide what the next builders should remember\\nAsk for a proposed lesson, then check it against a development result. Edit the rule in your own words. A proposed note is not automatically accepted. Final evaluation answers are excluded."),propose_lesson,lesson_evidence,lesson_text,save_lesson,mo.md(lab.blocked(_s,"memory"))]) if get_step()=="memory" else mo.md("")
''',True)
add('''
mo.stop(not propose_lesson.value)
show("lesson proposal",lab.propose_lesson(current_session()))
show("traces",export_saved_traces())
refresh()
''',True)
add('''
mo.stop(not save_lesson.value)
teaching.check_exercise("memory",memory_code.value)
_result=lab.accept_lesson(current_session(),lesson_text.value,lesson_evidence.value)
show("memory",_result)
current_session().checkpoint("memory")
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
run_followup=mo.ui.run_button(label="Run both versions of the follow-up feature",disabled=not lab.can_run(_s,"followup"))
mo.vstack([mo.Html(ui.step("Add the last departure and itinerary","Start fresh builders from the same tested release. Both receive the specification and interface. Only one receives your accepted lesson.","Find the read_memory operation in Agent Lens. Inspect the returned note and the code that subsequently ran.")),mo.accordion({"Second work order":mo.json(lab.work_order(2))}),run_followup,mo.md(lab.blocked(_s,"followup"))]) if get_step()=="followup" else mo.md("")
''',True)
add('''
mo.stop(not run_followup.value)
_result=lab.run_followups(current_session(),worker_code.value,tasks_code.value,memory_code.value)
show("followup",_result)
show("traces",export_saved_traces())
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
reviewed_followup=mo.ui.checkbox(label="I reviewed the no-lesson and shared-lesson patches")
integrate_followup=mo.ui.run_button(label="Integrate the reviewed follow-up patches",disabled=not lab.can_run(_s,"integrate-followup"))
mo.vstack([mo.Html(lab.patch_review(_s,followup=True)),reviewed_followup,integrate_followup]) if get_step()=="followup" else mo.md("")
''',True)
add('''
mo.stop(not integrate_followup.value)
mo.stop(not reviewed_followup.value,mo.md("Review the two diffs and confirm above."))
show("followup integration",lab.integrate_followups(current_session()))
current_session().checkpoint("followup")
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
run_evaluation=mo.ui.run_button(label="Compare the frozen builds",disabled=not lab.can_run(_s,"evaluate"))
retry_publication=mo.ui.run_button(label="Retry saved Forge publications",disabled=not bool(_s))
mo.vstack([mo.Html(ui.step("Check the same journeys across builds","Run your development scorer check, then freeze each build and run the reserved scenarios with the independent scorer.","Open native EvalTables in the Forge workspace. Compare the same departure case across versions, then follow its trace and source links.")),run_evaluation,retry_publication,mo.md(lab.blocked(_s,"evaluate")),mo.md("A passing scenario measures the delivered app. Wall-clock time and total inference cost describe the factory. These are separate comparisons. A single run cannot establish a general advantage for teams or memory.")]) if get_step()=="evaluate" else mo.md("")
''',True)
add('''
mo.stop(not run_evaluation.value)
teaching.check_exercise("evaluate",evaluate_code.value)
_s=current_session()
show("evaluation",lab.evaluate_builds(_s))
show("publications",lab.publish_results(_s))
_s.checkpoint("evaluate")
refresh()
''',True)
add('''
mo.stop(not retry_publication.value)
show("traces",export_saved_traces())
show("publications",lab.publish_results(current_session()))
current_session().retry_publication()
refresh()
''',True)
add('''
_s=current_session()
_revision=get_revision()
release_version=mo.ui.dropdown(lab.release_choices(_s),value=next(iter(lab.release_choices(_s)),None),label="Tested version to release",full_width=True)
conclusion=mo.ui.text_area(value=_s.get_draft("factory/conclusion","") if _s else "",label="What shipped, what failed, and what you would test next",full_width=True,on_change=lambda text:_s.save_draft("factory/conclusion",text) if _s else None)
release_button=mo.ui.run_button(label="Publish this release and its evidence",disabled=not lab.can_run(_s,"release"))
mo.vstack([mo.md("### Reproduce the version you selected\\nThe release contains the exact app code, data, contract, memory version, and checked results. Your release_decision runs before publication. If no build passes, retain the previous version and explain what is blocked."),release_version,conclusion,release_button,mo.md(lab.blocked(_s,"release"))]) if get_step()=="release" else mo.md("")
''',True)
add('''
mo.stop(not release_button.value)
teaching.check_exercise("release",release_code.value)
mo.stop(not conclusion.value.strip(),mo.md("Write what the comparison showed before publishing."))
show("release",lab.release(current_session(),release_version.value,release_code.value,conclusion.value))
current_session().checkpoint("release")
refresh()
''',True)

add('''
_s=current_session()
_revision=get_revision()
mo.stop(_s is None)
_view=get_step()
mo.vstack(lab.result_views(mo,_s,_view,get_output()))
''',True)
add('''
_index=next(i for i,step in enumerate(teaching.STEPS) if step[0]==get_step())
_next=teaching.STEPS[_index+1] if _index+1<len(teaching.STEPS) else None
next_step_control=ui.next_step(mo,_next[1],_next[0],go_to) if _next else None
mo.vstack([next_step_control,mo.md("Continue opens the next exercise. It does not run agents or publish results.")]) if _next else mo.md("You have reached the last step. Keep the saved app and Report so you can reproduce the release later.")
''',True)
add('''
_s=current_session()
_revision=get_revision()
mo.stop(_s is None)
mo.vstack([ui.evidence(mo,_s,stage_ids=teaching.stages_for_step(_s,get_step()),question=lab.investigation(get_step())),ui.publication(mo,_s)])
''',True)
add('''
_s=current_session()
_revision=get_revision()
_help=mo.ui.text_area(label="Which step needs help?",full_width=True)
help_form=mo.Html("<div>{message}</div>").batch(message=_help).form(submit_button_label="Send a help request")
mo.accordion({"Ask the facilitator":help_form}) if _s else mo.md("")
''',True)
add('''
mo.stop(help_form.value is None or not current_session())
current_session().request_help(help_form.value["message"])
mo.md("Request saved. The facilitator can read it in the workshop monitor.")
''',True)
add('''
_s=current_session()
_revision=get_revision()
_options=_s.recovery_options() if _s else []
recovery=mo.ui.dropdown({row["name"]+" · "+row["id"][:6]:row["id"] for row in _options},value=next((row["name"]+" · "+row["id"][:6] for row in _options),None),label="Stopped execution")
confirm_stopped=mo.ui.checkbox(label="The previous execution has stopped; keep uncertain requests charged at their reserved maximum")
retry_execution=mo.ui.run_button(label="Allow another attempt",disabled=not bool(_options))
mo.accordion({"Recover stopped work":mo.vstack([recovery,confirm_stopped,retry_execution,mo.md("Completed sibling tasks remain saved. This control authorizes recovery; use the step's normal run button afterward. Publication retries never require another build.")])}) if _options else mo.md("")
''',True)
add('''
mo.stop(not retry_execution.value)
try:
    show("recovery",lab.allow_retry(current_session(),recovery.value,confirm_stopped.value))
except Exception as _error:
    show("recovery",{"error":str(_error)})
refresh()
''',True)
