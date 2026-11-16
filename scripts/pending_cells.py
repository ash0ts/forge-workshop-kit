"""Authored Pending cells. Training, inference and tools require explicit run controls."""
from notebook_builder import Cell

cells=[]
def add(code,hide=False,cell_id=None):
    cells.append(Cell(code,hide=hide,cell_id=cell_id))

add('''
import os
import json
import time
from dataclasses import asdict
import copy
import marimo as mo
from forge_workshop_kit import WorkshopSession, ui, setup
from forge_workshop_kit import aria, technical_guides
from forge_workshop_kit.pending import teaching, recovery, visuals as pending_visuals
from forge_workshop_kit.pending.cases import CASES
from forge_workshop_kit.pending.harness import Harness, harness_diff
from forge_workshop_kit.pending.loop import run_employee, editor_decision, judge_explanation, reflect_execution
from forge_workshop_kit.traces import event, export_trace, saved_trace_inputs
from forge_workshop_kit.publication import publish_comparison, publish_report
get_pending,set_pending=mo.state({})
get_display,set_display=mo.state({})
get_technical_guide_view, set_technical_guide_view = mo.state({}, allow_self_loops=True)
technical_guide_controls = technical_guides.controls(mo, 'pending_inc', set_technical_guide_view)
get_step,set_step=mo.state("setup",allow_self_loops=True)
get_recovery_revision,set_recovery_revision=mo.state(0)
get_timeout_practice,set_timeout_practice=mo.state(pending_visuals.new_timeout_practice(),allow_self_loops=True)
''',True)
add('''
mo.stop(get_step()!="setup")
mo.vstack([mo.md("**4-hour workshop, including breaks and exercises.** [Open the companion deck](https://ash0ts.github.io/forge-workshop-kit/pending/). Its worked examples explain the code you will edit below."),mo.Html(ui.heading("Pending, Inc.", "You're on the operations team at a fictional software company. Customers are waiting for refunds and account access. Management has assigned those tickets to an AI employee and given you the job of making it reliable. Its onboarding so far consists of a motivational paragraph.")),
mo.md("**Today's assignment:** get the employee through two customer requests. It needs to look up the right account, decide whether a change is needed, make that change once, and explain what happened. A confident reply won't help a customer who still can't sign in."),
mo.Html(pending_visuals.office_brief()),
mo.md("**What's in a case.** Our dataset pairs each customer request with a starting account snapshot: the subscription, payments, refunds, and members. Python tools read and change a separate copy of that snapshot. These are fictional records; no real money moves and no real access is granted."),
mo.md("**What counts as success.** We check the account after the employee finishes: was the right payment refunded, does the requested access exist, and were unrelated records left alone? A separate judge checks whether the reply matches the recorded work. You'll use two development tickets while building and debugging, then compare the starting, manually edited, and agent-edited harnesses on four fresh cases."),
mo.md("You'll first write the invoice tool, connect its results to the model, and trace the work in Agent Lens. Then you'll change the employee's instructions yourself and ask another agent to propose and test further edits. The model stays fixed. We're testing whether changing how it works helps it handle the next ticket.")])
''',True)
add('''
mo.stop(get_step()!="setup")
pending_preview_account=mo.ui.radio({"Acme's account":"acme","Unrelated account":"other-account"},value="Acme's account",inline=True,label="Which account should the lookup read?")
pending_preview_reveal=mo.ui.checkbox(label="Show the invoice records for this account")
mo.vstack([mo.md("### Inspect a ticket before signing in"),mo.md("Acme reports two charges for invoice inv-1. Before seeing the lookup, name the payment that should be refunded and the records that should stay unchanged. This free example reads the bundled development snapshot. It does not call a model or publish anything."),mo.md("```python\\nmy_invoice_tool(state, account_id, 'inv-1')\\n```"),pending_preview_account,pending_preview_reveal])
''',True)
add('''
mo.stop(get_step()!="setup")
mo.vstack([mo.Html(ui.result("Requested account",{"account_id":pending_preview_account.value,"invoice_id":"inv-1"})),mo.ui.table(teaching.invoice_preview(pending_preview_account.value)["payments"],selection=None),mo.md("These fictional accounts reuse the same invoice and payment IDs. The customer named Acme: matching an invoice number alone is not enough to authorize a refund in another account.")]) if pending_preview_reveal.value else mo.md("Connect below when you are ready to save your own tool, traces and results.")
''',True)
add('''
def move_pending(step):
    if get_pending().get("session"):
        get_pending()["session"].set_view(step)
    set_step(step)

def pending_refresh(session):
    set_pending(teaching.restore(session))

def pending_checkpoint(session,step,**kwargs):
    with mo.status.spinner(title="Saving your results to Forge"):
        return session.checkpoint(step,**kwargs)

def pending_execution_table(rows):
    return mo.ui.table(rows,selection=None,pagination=False,hidden_columns=["Harness"],
        format_mapping={"Conversation":lambda url:mo.md("[Open trace]("+url+")") if url.startswith("https://") else url},
        column_widths={"Conversation":110},label="Execution comparison")

def pending_publish(session,name,rows):
    try:
        with mo.status.spinner(title="Uploading the saved comparison"):
            result=publish_comparison(session,name,rows)
        set_display({key:value for key,value in get_display().items() if key!="publication_error"})
        return result
    except Exception as error:
        set_display({**get_display(),"publication_error":str(error)})
        return {}

_s=get_pending().get("session")
mo.vstack([mo.Html(ui.STYLE + technical_guides.theme_style()),ui.navigation(mo,teaching.STEPS,get_step(),move_pending,completed=_s.read()["progress"].get("completed",[]) if _s else ()),mo.Html(ui.context(_s)) if _s else mo.md("Start by connecting your own Forge project. Your code, traces and results will be saved there."),mo.Html(ui.result("Some results have not uploaded",{"Issue":get_display()["publication_error"],"Next":"Your run is saved. Use Retry publication in the final comparison to upload it again."},status="unavailable")) if get_display().get("publication_error") else mo.md("")])
''',True)
add('''
technical_guide_view = technical_guides.panel(mo, 'pending_inc', get_step(), get_technical_guide_view(), technical_guide_controls)
technical_guide_view
''', True, cell_id='pending_inc/visual_guide')
add('''
_s = get_pending().get("session")
_revision = get_recovery_revision()
_view = get_step()
pending_recovery_refresh = mo.ui.button(label="Check for stopped or failed work", on_click=lambda _: set_recovery_revision(lambda previous: previous + 1), disabled=not bool(_s))
_options = _s.recovery_options() if _s else []
_choices = {setup.recovery_label(_s.workshop, row) + " · " + row["id"][:6]: row["id"] for row in _options}
pending_recovery_choice = mo.ui.dropdown(_choices, value=next(iter(_choices), None), label="Execution to review", full_width=True) if _choices else mo.ui.dropdown({"No failed executions": ""}, value="No failed executions", disabled=True)
mo.vstack([mo.md("**A run stopped?** Check its saved status here. Reviewing it never starts work."), pending_recovery_refresh, pending_recovery_choice]) if _options else mo.accordion({"A run stopped? Review recovery": mo.vstack([mo.md("Click below to read saved execution status. Completed results stay saved. An upload failure uses Retry publication in the final comparison instead."), pending_recovery_refresh])})
''', True)
add('''
_s = get_pending().get("session")
_row = next((row for row in _s.recovery_options() if row["id"] == pending_recovery_choice.value), None) if _s else None
_needs_confirmation = bool(_row and (_row["has_uncertain_requests"] or _row["status"] == "running"))
pending_recovery_confirm = mo.ui.checkbox(label="I checked that the previous execution has stopped. Keep unresolved requests charged at their reserved maximum.")
pending_recovery_allow = mo.ui.run_button(label="Allow retry of this failed execution", disabled=not bool(_row), full_width=True)
mo.vstack([mo.Html(ui.result("Review the saved execution", {"Execution": _row["name"], "Status": _row["status"], "Issue": _row.get("error") or "The execution has not finished.", "Next": "Allow another attempt, then click the normal run button for this step. This control does not run the experiment."}, status="failed")), pending_recovery_confirm if _needs_confirmation else mo.md("The previous attempt has ended. Its result and costs remain in the record."), pending_recovery_allow]) if _row else mo.md("")
''', True)
add('''
mo.stop(not pending_recovery_allow.value)
_s = get_pending()["session"]
try:
    _route = _s.retry_stage(pending_recovery_choice.value, confirm_stopped=pending_recovery_confirm.value)
    _message = "Retry allowed. Return to this step’s run button to start attempt " + str(_route["attempt"]) + ". Completed work will be reused."
except Exception as _error:
    _message = str(_error)
set_display({**get_display(), "recovery": _message})
pending_refresh(_s)
set_recovery_revision(lambda previous: previous + 1)
''', True)
add('''
_message = get_display().get("recovery")
mo.callout(mo.md(_message), kind="info") if _message else mo.md("")
''', True)
add('''
mo.stop(get_step()!="setup")
_context=setup.project_context()
pending_project=mo.ui.text(value=_context["project"],label="Your Forge entity/project",disabled=_context["hosted"] and _context["detected"],full_width=True)
pending_allowance=mo.ui.number(value=8,start=.01,stop=1000,label="Inference limit in USD; notebook compute is separate")
pending_connect=mo.ui.run_button(label="Check my project and restore saved work",full_width=True)
mo.vstack([mo.Html(ui.step("1. Connect your project and send a trace", "Copy this notebook into your own Forge project. We use that project and your existing Forge login. On a laptop, enter entity/project and run uv run wandb login first.","Click Check my project and restore saved work. You should see your project name and a successful connection. This check makes no model calls.")),mo.Html(ui.result("Copied notebook project",{"Project":_context["project"],"Access":"Uses your Forge login"})) if _context["hosted"] and _context["detected"] else pending_project,pending_allowance,pending_connect])
''',True)
add('''
mo.stop(not pending_connect.value)
_s = None
_access = None
try:
    _s=WorkshopSession.from_environment("pending-direct-teaching",project=pending_project.value,budget_usd=pending_allowance.value)
    _access=_s.check_access()
    _restore=_s.restore()
    setup.save_access(_s,_access)
    pending_refresh(_s)
    set_step(_s.get_view("setup"))
    set_display({**get_display(),"setup":{**_access,"restore":_restore["status"]}})
except Exception as _error:
    if _s is not None and _access is None:
        setup.save_access(_s, {"write_access": False, "error": str(_error)})
    set_display({**get_display(),"setup":{"error":str(_error)}})
''')
add('''
pending_help=mo.ui.text_area(label="What do you need help with?",full_width=True)
pending_help_button=mo.ui.run_button(label="Send this help request",disabled=not bool(get_pending().get("session")))
mo.accordion({"Ask the facilitator":mo.vstack([pending_help,pending_help_button,mo.md("The facilitator can see this message in the workshop monitor. Include the step you are on and what happened.")])})
''',True)
add('''
mo.stop(not pending_help_button.value)
get_pending()["session"].request_help(pending_help.value)
mo.md("Help request sent. Clear the message and send it again when you no longer need help.")
''')
add('''
pending_prerequisite_1=ui.prerequisite(mo,"Connect to a writable project first.","setup",move_pending)
mo.stop(get_step()!="setup")
_s=get_pending().get("session")
instrumentation_editor=mo.ui.code_editor(value=_s.get_draft("pending/instrumentation",teaching.STARTERS["instrumentation"]) if _s else teaching.STARTERS["instrumentation"],language="python",min_height=260,max_height=500,label="Your Forge tool and model scopes",on_change=lambda value:_s.save_draft("pending/instrumentation",value) if _s else None)
pending_trace=mo.ui.run_button(label="Run this check and verify my Agent Lens trace",disabled=not bool(_s),full_width=True)
mo.vstack([mo.Html(ui.result("Project connection",get_display().get("setup",{"Project":_s.project} if _s else {"Next":"Connect above."}))),mo.ui.table(setup.capabilities(_s),selection=None,pagination=False) if _s else mo.md(""),mo.md("**Send your first trace.** In the code cell below this button, find inspect_notebook and add an environment field to the returned dictionary, such as the operating system name. Run the check, open Agent Lens, and find that field. The functions here record tool activity and model calls; you'll use them again when the employee starts work."),instrumentation_editor,pending_trace,pending_prerequisite_1 if not _s else mo.md("")])
''',True)
add('''
mo.stop(not pending_trace.value)
_s=get_pending()["session"]
_s.save_draft("pending/instrumentation",instrumentation_editor.value)
_writers=teaching.compile_code(instrumentation_editor.value)
with _s.stage("pending/setup-trace",sources={"instrumentation.py":instrumentation_editor.value}) as _stage:
    if _stage.needs_run:
        # Add another measured field here. This is a real operation, without a model call.
        _result,_receipt=event("inspect_notebook",{},lambda:{"python":__import__("platform").python_version(),"tools":"local Python and MCP"},on_error=_stage.record_event)
        _stage.record({"events":[_receipt]})
_trace=export_trace(_s,_stage.id,"Check my notebook before running an agent",_stage.result["events"],tool_writer=_writers["my_tool_span"],model_writer=_writers["my_model_span"])
pending_checkpoint(_s,"setup",evidence={"My first Agent Lens conversation":_trace["url"]})
set_display({**get_display(),"trace":_trace})
pending_refresh(_s)
''')
add('''
pending_next_step_1=ui.next_step(mo,"Build the invoice lookup","tools",move_pending)
mo.stop(get_step()!="setup")
_s=get_pending().get("session")
_row=teaching.latest(_s,"pending/setup-trace") if _s else None
mo.stop(not _row)
mo.vstack([ui.evidence(mo,_s,[_row["id"]],question="Open inspect_notebook in Agent Lens. Find the field you added and compare its value with the dictionary your code returned."),pending_next_step_1])
''',True)
add('''
pending_prerequisite_2=ui.prerequisite(mo,"Connect to your project so the notebook can save your code and test results.","setup",move_pending)
mo.stop(get_step()!="tools")
_s=get_pending().get("session")
tool_editor=mo.ui.code_editor(value=_s.get_draft("pending/tool",teaching.STARTERS["tool"]) if _s else teaching.STARTERS["tool"],language="python",min_height=170,max_height=350,label="Write my_invoice_tool",on_change=lambda value:_s.save_draft("pending/tool",value) if _s else None)
check_pending_tool=mo.ui.run_button(label="Test my invoice lookup",disabled=not bool(_s),full_width=True)
mo.vstack([mo.Html(ui.step("2. Build the invoice lookup tool", "Complete my_invoice_tool. Find the requested account, filter its payments by invoice_id, and return those payments with the account's refunds. A lookup reads the account; it should not change it.","Click Test my invoice lookup. All three checks should pass: the requested invoice, a missing invoice, and another customer's account.")),mo.md("The employee needs to see the payments before it can decide whether a refund is needed. Equipment was not included in the offer letter."),tool_editor,check_pending_tool,mo.accordion({"Hint":"Filter account['payments'] by invoice_id. Return the selected account's refunds.","Worked answer":mo.md("```python\\n"+teaching.ANSWERS["tool"]+"\\n```")}),pending_prerequisite_2 if not _s else mo.md("")])
''',True)
add('''
mo.stop(not check_pending_tool.value)
_s=get_pending()["session"]
_s.save_draft("pending/tool",tool_editor.value)
try:
    _fn=teaching.compile_code(tool_editor.value)["my_invoice_tool"]
    _writers=teaching.functions(_s)
    with _s.stage("pending/check-tool",sources={"lookup_invoice.py":tool_editor.value},config={"trace_version":1}) as _stage:
        if _stage.needs_run:
            _events=[]
            def _checked_tool(state,account_id,invoice_id):
                _result,_event=event("lookup_invoice",{"account_id":account_id,"invoice_id":invoice_id},lambda:_fn(state,account_id,invoice_id),on_error=_stage.record_event)
                _events.append(_event)
                return _result
            _rows=teaching.check_tool(_checked_tool)
            _stage.record({"rows":_rows,"events":_events})
    _rows=_stage.result["rows"]
    _trace=export_trace(_s,_stage.id,"Check my invoice tool on three public examples",_stage.result["events"],tool_writer=_writers["my_tool_span"],model_writer=_writers["my_model_span"])
    pending_checkpoint(_s,"tools",evidence={"My invoice-tool checks":_trace["url"]})
    set_display({**get_display(),"tool":{"rows":_rows,"passed":True}})
except Exception as _error:
    set_display({**get_display(),"tool":{"error":str(_error)}})
pending_refresh(_s)
''')
add('''
pending_next_step_2=ui.next_step(mo,"Wire the tool into an agent request","loop",move_pending)
mo.stop(get_step()!="tools")
_s=get_pending().get("session")
_result=teaching.check_status(_s,"tool",{"lookup_invoice.py":tool_editor.value})
_error=get_display().get("tool",{}).get("error")
mo.vstack([mo.ui.table(_result.get("rows",[]),selection=None),mo.Html(ui.result("Invoice checks",{"Status":_result["state"],"Issue":_error or ""},status="failed" if _error else "complete" if _result["passed"] else "not started")),ui.evidence(mo,_s,[teaching.latest(_s,"pending/check-tool")["id"]],question="Open one lookup_invoice call. Check which account and invoice you requested, then look at the returned payments. Later, the employee can choose this tool or another registered account-reading tool.") if _s and teaching.latest(_s,"pending/check-tool") else mo.md(""),pending_next_step_2])
''',True)
add('''
mo.stop(get_step() != 'loop')
mo.md('### Keep the action and its result together\\nDispatch changes the outside world or reads it. The observation handoff changes what the model knows about that operation.\\n```python\\n# Execute the named tool with the arguments selected by the model.\\nresult = my_dispatch(action["action"], action["arguments"], ...)\\n# Preserve the action, then append the actual return value to history.\\nmessages = my_observation(messages, action, result)\\n# The next request receives that longer history.\\n```\\nThis is an abbreviated call-site sketch; the editable functions below have the full signatures. A refund can happen even if the model never receives its result. Retrying before checking the account can therefore change an already-changed account.')
''', True, cell_id='pending_inc/explanation/handoff')
add('''
mo.stop(get_step()!="loop")
_s=get_pending().get("session")
loop_editor=mo.ui.code_editor(value=_s.get_draft("pending/loop",teaching.STARTERS["loop"]) if _s else teaching.STARTERS["loop"],language="python",min_height=230,max_height=450,label="Dispatch an action and append its observation",on_change=lambda value:_s.save_draft("pending/loop",value) if _s else None)
starting_instructions=mo.ui.text_area(value=_s.get_draft("pending/instructions",Harness().instructions) if _s else Harness().instructions,label="Employee instructions",full_width=True,on_change=lambda value:_s.save_draft("pending/instructions",value) if _s else None)
mo.vstack([mo.Html(ui.step("3. Give the tool result back to the model", "Complete my_dispatch so lookup_invoice calls your function and other actions call their registered tools. Then complete my_observation to add the action and tool result to the next model request.","Pass the handoff check, then run the two starting tickets. Open the four handoff tabs and find the tool result in the next request. We'll keep the model, tools and these Python functions unchanged while we compare employee instructions.")),mo.md("Calling a tool is only half the job. The model also needs the returned data before it chooses its next action."),loop_editor,starting_instructions,mo.accordion({"Hint":"lookup_invoice calls your function. Other names call call_tool. Append the action as assistant content and the returned observation as user content.","Worked answer":mo.md("```python\\n"+teaching.ANSWERS["loop"]+"\\n```")})])
''',True)
add('''
pending_prerequisite_3=ui.prerequisite(mo,"Verify your setup trace before starting model calls.","setup",move_pending)
mo.stop(get_step()!="loop")
_s=get_pending().get("session")
_checked=teaching.check_status(_s,"loop",{"lookup_invoice.py":_s.get_draft("pending/tool",teaching.STARTERS["tool"]) if _s else "","loop.py":loop_editor.value})
check_pending_loop=mo.ui.run_button(label="Test my tool-to-model handoff",disabled=not bool(_s),full_width=True)
_failures=[row for row in _s.read()["stages"].values() if row["name"].startswith("pending/original/") and row["status"]=="failed"] if _s else []
run_pending=mo.ui.run_button(label="Starting tickets complete" if get_pending().get("starting") else "Resume the starting tickets" if _failures else "Freeze this executor and run the two starting tickets",disabled=not bool(_s) or not _checked["passed"] or not teaching.setup_verified(_s) or bool(get_pending().get("starting")),full_width=True)
mo.vstack([mo.Html(ui.result("Saved execution failed",{"Issue":_failures[-1]["error"],"Retry":"Review the failed execution in the recovery controls above, then use the run button. Completed tickets remain saved."},status="failed")) if _failures and not get_pending().get("starting") else mo.md(""),mo.Html(ui.result("Executor check",{"Status":_checked["state"]},status="complete" if _checked["passed"] else "not started")),check_pending_loop,run_pending,pending_prerequisite_3 if _s and not teaching.setup_verified(_s) else mo.md("Pass the handoff check above. If you edit the code afterward, run the check again.")])
''',True)
add('''
mo.stop(not check_pending_loop.value)
_s=get_pending()["session"]
_s.save_draft("pending/loop",loop_editor.value)
try:
    _f=teaching.functions(_s)
    teaching.check_tool(_f["my_invoice_tool"])
    _result=teaching.check_loop(_f["my_dispatch"],_f["my_observation"],_f["my_invoice_tool"])
    with _s.stage("pending/check-loop",sources={"lookup_invoice.py":_s.get_draft("pending/tool",teaching.STARTERS["tool"]),"loop.py":loop_editor.value}) as _stage:
        if _stage.needs_run: _stage.record(_result)
    pending_checkpoint(_s,"loop-check")
    set_display({**get_display(),"loop":{"passed":True,**_result}})
    pending_refresh(_s)
except Exception as _error:
    set_display({**get_display(),"loop":{"error":str(_error)}})
''')
add('''
mo.stop(not run_pending.value)
_s=get_pending()["session"]
_s.save_draft("pending/loop",loop_editor.value)
_s.save_draft("pending/instructions",starting_instructions.value)
_f=teaching.functions(_s)
_runtime=teaching.freeze_runtime(_s,_f)
_harness=Harness(instructions=starting_instructions.value)
try:
    _runs=[run_employee(_s,c,_harness,"pending/original",**teaching.hooks(_f)) for c in CASES if c.split=="development"]
finally:
    pending_refresh(_s)
pending_checkpoint(_s,"loop")
pending_refresh(_s)
''')
add('''
pending_next_step_3=ui.next_step(mo,"Check the account and judge the explanation","evals",move_pending)
mo.stop(get_step()!="loop")
_s=get_pending().get("session")
_runs=get_pending().get("original",[])
_preview=teaching.check_status(_s,"loop",{"lookup_invoice.py":_s.get_draft("pending/tool",teaching.STARTERS["tool"]) if _s else "","loop.py":loop_editor.value})
_preview["error"]=get_display().get("loop",{}).get("error","")
_views=[mo.Html(ui.result("Local handoff check",{"Status":_preview["state"],"Issue":_preview.get("error","")},status="failed" if _preview.get("error") else "complete" if _preview["passed"] else "not started"))]
if _preview.get("next_request"):
    _views.append(mo.ui.tabs({name:mo.Html(frame) for name,frame in pending_visuals.handoff_frames(_preview).items()}))
if _runs:
    _views.append(pending_execution_table(teaching.summary_rows(_runs)))
    for _run in _runs:
        _views.extend([mo.md("**"+_run["case_id"]+": actual tool sequence**"),mo.ui.table(teaching.tool_rows(_run),selection=None),mo.accordion({"Exact arguments and returned observations":mo.ui.table([{"Step":i+1,"Arguments":e["arguments"],"Result":e["result"]} for i,e in enumerate(_run["events"])],selection=None)})])
    _views.extend([ui.evidence(mo,_s,[r["stage_id"] for r in _runs],question="Open a starting ticket in Agent Lens. Find an account lookup and the model call that used its result. In onboarding, find the timeout and inspect what the employee did next. Did it check whether access had already been granted?"),pending_next_step_3])
mo.vstack(_views)
''',True)
add('''
mo.stop(get_step()!="loop")
_practice=get_timeout_practice()
_started=bool(_practice["events"])
timeout_start=mo.ui.button(label="Send the request and trigger a timeout",on_click=lambda _:set_timeout_practice(pending_visuals.timeout_action(pending_visuals.new_timeout_practice(),"commit")),disabled=_started)
timeout_read=mo.ui.button(label="Read the account's access",on_click=lambda _:set_timeout_practice(pending_visuals.timeout_action(get_timeout_practice(),"inspect")),disabled=not _started)
timeout_same=mo.ui.button(label="Retry with the same operation ID",on_click=lambda _:set_timeout_practice(pending_visuals.timeout_action(get_timeout_practice(),"same")),disabled=not _started)
timeout_new=mo.ui.button(label="Retry with a new operation ID",on_click=lambda _:set_timeout_practice(pending_visuals.timeout_action(get_timeout_practice(),"new")),disabled=not _started)
timeout_reset=mo.ui.button(label="Reset this practice account",on_click=lambda _:set_timeout_practice(pending_visuals.new_timeout_practice()),disabled=not _started)
mo.vstack([mo.Html(pending_visuals.timeout_view(_practice)),timeout_start,mo.md("**Choose a recovery action.** Predict the membership count before clicking. Reset between alternatives to compare each with the same timed-out request."),mo.hstack([timeout_read,timeout_same,timeout_new],wrap=True),timeout_reset])
''',True)
add('''
mo.stop(get_step()!="loop")
_s=get_pending().get("session")
recovery_editor=mo.ui.code_editor(value=_s.get_draft("pending/recovery",recovery.STARTER) if _s else recovery.STARTER,language="python",min_height=190,label="Repair recover_access",on_change=lambda value:_s.save_draft("pending/recovery",value) if _s else None,debounce=False)
check_recovery=mo.ui.run_button(label="Compare the two retry procedures",disabled=not bool(_s))
mo.vstack([mo.md("### Repair the retry in Python\\nThe timed-out request already added Alex. The starter below retries with a new operation ID and adds Alex twice. Keep the original ID, then read onboarding_status to check the account. Run both procedures from the same starting state. This free exercise changes actual simulator state; it does not ask a model to follow your instructions."),recovery_editor,check_recovery,mo.accordion({"Hint":"Call provision_member with the original arguments. Then call onboarding_status with the account_id.","Worked answer":mo.md("```python\\n"+recovery.ANSWER+"\\n```")})])
''')
add('''
mo.stop(not check_recovery.value)
_s=get_pending().get("session")
mo.stop(not _s)
_s.save_draft("pending/recovery",recovery_editor.value)
with _s.stage("pending/timeout-repair",sources={"recovery.py":recovery_editor.value}) as _stage:
    if _stage.needs_run:
        _before=recovery.run_recovery(recovery.STARTER)
        _after=recovery.run_recovery(recovery_editor.value)
        _stage.record({"before":_before,"after":_after,"rows":recovery.comparison_rows(_before,_after)})
_result=_stage.result
for _label in ("before","after"):
    try:
        _trace=export_trace(_s,_stage.id+"-"+_label,"Compare recovery after a committed membership write times out",_result[_label]["events"])
        _result[_label]["trace"]=_trace
    except Exception as _error:
        _result[_label]["trace_error"]=str(_error)
for _condition,_label in (("new-id-retry","before"),("your-recovery","after")):
    if _result[_label].get("trace"):
        _result["rows"][_condition][0]["evidence"]["agent_lens"]=_result[_label]["trace"]["url"]
try:
    _result["publication"]=pending_publish(_s,"pending-timeout-repair",_result["rows"])
except Exception as _error:
    _result["publication_error"]=str(_error)
set_display({**get_display(),"timeout-repair":_result})
_checkpoint=pending_checkpoint(_s,"loop")
''')
add('''
mo.stop(get_step()!="loop")
_s=get_pending().get("session")
_saved=[s for s in _s.read()["stages"].values() if s["name"]=="pending/timeout-repair" and s["status"]=="complete"] if _s else []
_result=get_display().get("timeout-repair") or (_saved[-1]["result"] if _saved else None)
mo.stop(not _result)
if not _result["after"].get("trace") and _saved:
    _result["after"]["trace"]=_s.read()["publications"].get("trace/"+_saved[-1]["id"]+"-after")
_rows=[{"Procedure":label,"Memberships":r["membership_count"],"Checked account":r["verified_account"],"Check passed":r["passed"],"Function error":r["error"]} for label,r in [("New ID retry",_result["before"]),("Your recovery",_result["after"])]]
mo.vstack([mo.ui.table(_rows,selection=None,pagination=False),mo.md("**Your repair keeps one membership and checks the account.** Now distinguish this code repair from the later harness experiment: that experiment asks a fixed model to use revised instructions. Its recorded final comparison was a tie, with all three versions passing four cases." if _result["after"]["passed"] else "**Revise recover_access and run the check again.** Success means one membership and an account read after recovery."),mo.md("[Inspect your recovery in Agent Lens]("+_result["after"]["trace"]["url"]+"). Find the reused operation_id and the following account read.") if _result["after"].get("trace") else mo.md("Trace publication is pending. The account comparison remains saved."),mo.accordion({"Actual tool calls":mo.ui.table(_result["after"]["events"],selection=None)})])
''')
add('''
pending_prerequisite_4=ui.prerequisite(mo,"Finish the two starting tickets, then pass the scorer checks above.","loop",move_pending)
mo.stop(get_step()!="evals")
_s=get_pending().get("session")
scorer_editor=mo.ui.code_editor(value=_s.get_draft("pending/scorer",teaching.STARTERS["scorer"]) if _s else teaching.STARTERS["scorer"],language="python",min_height=250,max_height=480,label="Write a state check and validate the judge response",on_change=lambda value:_s.save_draft("pending/scorer",value) if _s else None)
judge_rubric=mo.ui.text_area(value=_s.get_draft("pending/rubric","Check each completion claim against recorded tool activity. A timeout is not proof that a write failed. Separate an accurate explanation from a correct account.") if _s else "Check completion claims against recorded work.",label="Explanation judge rubric",full_width=True,on_change=lambda value:_s.save_draft("pending/rubric",value) if _s else None)
mo.vstack([mo.Html(ui.step("4. Check the work, then judge the explanation", "Complete my_state_check: a correct refund means exactly one refund for 4,900 cents. Then complete my_judge_validation to reject malformed judge answers. Test the four examples before asking the judge to assess the employee's saved replies.","Compare the account check with the explanation judge. A confident reply can describe a refund that never happened. If the judge fails to return an answer, its score stays blank.")),mo.md("Accounting would prefer that we check the account before declaring the ticket resolved."),mo.Html(pending_visuals.checks_view()),scorer_editor,judge_rubric,mo.accordion({"Worked answer":mo.md("```python\\n"+teaching.ANSWERS["scorer"]+"\\n```")}),pending_prerequisite_4 if not get_pending().get("starting") else mo.md("")])
''',True)
add('''
mo.stop(get_step()!="evals")
_s=get_pending().get("session")
_checked=teaching.check_status(_s,"scorer",{"scorer.py":scorer_editor.value})
check_pending_scorer=mo.ui.run_button(label="Test my scorer against four known examples",disabled=not bool(_s),full_width=True)
pending_judge=mo.ui.run_button(label="Judge and publish the starting development comparison",disabled=not bool(get_pending().get("starting")) or not _checked["passed"],full_width=True)
mo.vstack([mo.Html(ui.result("Scorer check",{"Status":_checked["state"]},status="complete" if _checked["passed"] else "not started")),check_pending_scorer,pending_judge])
''',True)
add('''
mo.stop(not check_pending_scorer.value)
_s=get_pending()["session"]
_s.save_draft("pending/scorer",scorer_editor.value)
try:
    _f=teaching.functions(_s)
    _rows=teaching.check_scorer(_f["my_state_check"],_f["my_judge_validation"])
    with _s.stage("pending/check-scorer",sources={"scorer.py":scorer_editor.value}) as _stage:
        if _stage.needs_run: _stage.record({"rows":_rows})
    pending_checkpoint(_s,"scorer-check")
    set_display({**get_display(),"scorer":{"passed":True,"rows":_rows}})
    pending_refresh(_s)
except Exception as _error:
    set_display({**get_display(),"scorer":{"error":str(_error)}})
''')
add('''
mo.stop(not pending_judge.value)
_s=get_pending()["session"]
_s.save_draft("pending/scorer",scorer_editor.value)
_s.save_draft("pending/rubric",judge_rubric.value)
_f=teaching.functions(_s)
teaching.check_scorer(_f["my_state_check"],_f["my_judge_validation"])
_rows=[]
_runs=[]
for _run in get_pending()["original"]:
    try:
        _judgment=judge_explanation(_s,_run,judge_rubric.value,validate=_f["my_judge_validation"],tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
    except Exception as _error:
        _judgment={"status":"unavailable","error":str(_error)}
    _runs.append({**_run,"explanation_judgment":_judgment})
    _rows.append({"Case":_run["case_id"],"My state check":_f["my_state_check"](_run),"Independent state check":_run["scores"]["task_success"],"Grounded explanation":_judgment.get("grounded"),"Judge reason":_judgment.get("reason",_judgment.get("error"))})
with _s.stage("pending/development-evaluation",sources={"scorer.py":scorer_editor.value},inputs={"executions":[r["stage_id"] for r in _runs],"rubric":judge_rubric.value}) as _stage:
    if _stage.needs_run: _stage.record({"rows":_rows,"runs":_runs,"comparison":teaching.comparison_rows({"starting":_runs})})
_published=pending_publish(_s,"pending-development",_stage.result["comparison"])
pending_checkpoint(_s,"evals",evidence={"Development "+k:r["run"] for k,r in _published.items()})
pending_refresh(_s)
''')
add('''
pending_next_step_4=ui.next_step(mo,"Change one procedure using that evidence","manual",move_pending)
mo.stop(get_step()!="evals")
_s=get_pending().get("session")
_check=teaching.check_status(_s,"scorer",{"scorer.py":scorer_editor.value})
_check["error"]=get_display().get("scorer",{}).get("error","")
_evaluation=get_pending().get("evaluation",{})
mo.vstack([mo.ui.table(_check.get("rows",[]),selection=None),mo.md(_check.get("error","")),mo.ui.table(_evaluation.get("rows",[]),selection=None),ui.publication(mo,_s) if _s else mo.md(""),ui.evidence(mo,_s,[r["stage_id"] for r in _evaluation.get("runs",[])],question="Choose a ticket and compare its account check with its explanation score. Open the trace: did the refund happen, and did the reply describe it accurately?") if _s else mo.md("")])
''',True)
add('''
mo.stop(get_step()!="evals")
_s=get_pending().get("session")
_evaluation=teaching.latest(_s,"pending/development-evaluation") if _s else None
_ids=([_evaluation["id"]]+[r["stage_id"] for r in _evaluation["result"].get("runs",[])]) if _evaluation else []
pending_aria_investigate=aria.investigation(mo,_s,"investigate",record_ids=_ids,workshop="pending-direct-teaching")
pending_aria_investigate
''', True, cell_id='pending_inc/aria/investigate')
add('''
mo.vstack([aria.response(mo,pending_aria_investigate),pending_next_step_4])
''', True, cell_id='pending_inc/aria_response/investigate')
add('''
mo.stop(get_step()!="manual")
_s=get_pending().get("session")
_requests=list(_s.read()["requests"].values()) if _s else []
_skill_views={run["case_id"]:mo.Html(pending_visuals.skill_view(run,[request for request in _requests if request.get("id","").startswith(run["stage_id"]+"/")])) for run in get_pending().get("original",[])}
pending_skill_example=mo.ui.checkbox(label="Show a free example of read_skill and the next request")
mo.vstack([mo.md("### Check whether the starting employee read a skill"),mo.md("Before editing, inspect the starting tickets below. A skill file and a successful read are different observations. If no read is recorded, say so. The optional local example shows how returned text reaches the next request; it does not claim your employee read it."),mo.ui.tabs(_skill_views) if _skill_views else mo.md("Run the starting tickets to inspect their actual skill reads."),pending_skill_example])
''',True)
add('''
mo.stop(get_step()!="manual" or not pending_skill_example.value)
_example=teaching.skill_handoff_example()
mo.vstack([mo.md("**Free local example. No model chose this action.** The initial message names the skill. The read returns its text. The observation function appends that text to the next request."),mo.Html(ui.result("Installed file",{"skills/verify-operation.md":_example["file"]})),mo.ui.tabs({"Before read":mo.json(_example["before"]),"Action":mo.json(_example["action"]),"Returned text":mo.json(_example["result"]),"Next request":mo.json(_example["after"])})])
''',True)
add('''
pending_prerequisite_5=ui.prerequisite(mo,"Check and publish the starting development result first.","evals",move_pending)
mo.stop(get_step()!="manual")
_s=get_pending().get("session")
_events={f"{r['case_id']} · {i+1}. {e['name']} · {'error' if e.get('error') else 'returned'}":e["id"] for r in get_pending().get("original",[]) for i,e in enumerate(r["events"])}
manual_event=mo.ui.dropdown(_events,label="Which recorded action prompted your edit?",value=next(iter(_events),None))
manual_instructions=mo.ui.text_area(value=_s.get_draft("pending/manual","") if _s else "",label="Write the procedure the employee should follow",full_width=True,on_change=lambda value:_s.save_draft("pending/manual",value) if _s else None)
manual_pending=mo.ui.run_button(label="Save this procedure and rerun both development tickets",disabled=not bool(get_pending().get("evaluation")),full_width=True)
mo.vstack([mo.Html(ui.step("5. Change an instruction and rerun both tickets", "Choose an action from a starting ticket. Write a short instruction for what the employee should do differently next time, such as checking the account after a timeout. This text becomes an installed verification skill. The employee sees its name and must call read_skill to load its contents.","Rerun both tickets, then compare the tool calls and account checks with the starting runs. Each run starts from the same account data; only your instruction changes.")),mo.md("Write the procedure you'd want a new colleague to follow. Then see whether the employee reads and follows it."),manual_event,manual_instructions,manual_pending,pending_prerequisite_5 if not get_pending().get("evaluation") else mo.md("")])
''',True)
add('''
mo.stop(not manual_pending.value)
_s=get_pending()["session"]
mo.stop(not manual_instructions.value.strip(),mo.md("Write a specific procedure before running it."))
_s.save_draft("pending/manual",manual_instructions.value)
_f=teaching.functions(_s)
_harness=Harness(**{**asdict(get_pending()["starting"]),"verification_skill":manual_instructions.value})
with _s.stage("pending/manual-decision",sources=_harness.files(),inputs={"event":manual_event.value}) as _decision:
    if _decision.needs_run: _decision.record({"diff":harness_diff(get_pending()["starting"],_harness),"harness":asdict(_harness),"fingerprint":_harness.fingerprint,"authorship":"participant"})
_runs=[run_employee(_s,c,_harness,"pending/manual",**teaching.hooks(_f)) for c in CASES if c.split=="development"]
with _s.stage("pending/development-manual-comparison",inputs={"starting":[r["stage_id"] for r in get_pending()["original"]],"manual":[r["stage_id"] for r in _runs]}) as _comparison:
    if _comparison.needs_run: _comparison.record({"rows":teaching.comparison_rows({"starting":get_pending().get("evaluation",{}).get("runs",get_pending()["original"]),"manual":_runs})})
pending_publish(_s,"pending-development",_comparison.result["rows"])
pending_checkpoint(_s,"manual")
pending_refresh(_s)
''')
add('''
pending_next_step_5=ui.next_step(mo,"Ask an agent for two alternative procedures","improve",move_pending)
mo.stop(get_step()!="manual")
_s=get_pending().get("session")
_runs=get_pending().get("manual_runs",[])
mo.stop(not _runs)
_before=json.dumps(asdict(get_pending()["starting"]),indent=2)
_after=json.dumps(asdict(get_pending()["manual"]),indent=2)
_requests=list(_s.read()["requests"].values())
_skill_views={run["case_id"]:mo.Html(pending_visuals.skill_view(run,[request for request in _requests if request.get("id","").startswith(run["stage_id"]+"/")])) for run in _runs}
mo.vstack([mo.Html(ui.diff(_before,_after)),pending_execution_table(teaching.summary_rows(get_pending()["original"])+teaching.summary_rows(_runs,"My procedure")),mo.ui.tabs(_skill_views),ui.publication(mo,_s,names=("pending-development",)),ui.evidence(mo,_s,[r["stage_id"] for r in _runs],question="Look for a successful read_skill call. If one is present, check the next model request and later tools. If no read is recorded, do not assume the employee used the skill."),pending_next_step_5])
''',True)
add('''
pending_prerequisite_6=ui.prerequisite(mo,"Run your manual procedure first.","manual",move_pending)
pending_next_step_6=ui.next_step(mo,"Freeze and compare on fresh tickets","final",move_pending)
mo.stop(get_step()!="improve")
_s=get_pending().get("session")
_number,_phase,_label=teaching.next_phase(_s) if _s else (1,"propose","Connect first")
_decision=teaching.active_decision(_s,_number,_phase) if _s else None
review_pending=mo.ui.checkbox(label="I reviewed this version's files and rationale")
_reason_key=f"pending/round-{_number}/my-comparison"
_choice_key=f"pending/round-{_number}/my-choice"
_choice_options={"Not decided":"undecided","Candidate A":"a","Candidate B":"b","Retain the parent":"keep","Combine parts":"combine"}
_saved_choice=_s.get_draft(_choice_key,"undecided") if _s else "undecided"
pending_my_choice=mo.ui.radio(_choice_options,value=next(label for label,value in _choice_options.items() if value==_saved_choice),label="Which version would you choose?",on_change=lambda value:_s.save_draft(_choice_key,value) if _s else None)
pending_my_reason=mo.ui.text_area(value=_s.get_draft(_reason_key,"") if _s else "",label="Which probe result supports your choice?",full_width=True,on_change=lambda value:_s.save_draft(_reason_key,value) if _s else None)

improve_pending=mo.ui.run_button(label=f"Round {_number} · {_label}",disabled=not bool(get_pending().get("manual")) or _phase=="done",full_width=True)
_views=[mo.Html(ui.step("6. Ask an agent to revise the instructions", "The editor agent reads a billing run and proposes two changes to the instructions. Read each diff and test both on the billing ticket. Then repeat with onboarding, using the version you kept and what you learned from billing.","After both tests, ask the editor to choose or combine the changes. Test that version too. It can keep the current instructions if neither change is worth using.")),mo.md("Management would like to automate management. Please review its changes.")]
if _s:
    _views.append(mo.ui.table([{"Phase":label,"State":"Done" if teaching.latest(_s,f'pending/round-{_number}/'+phase) else "Now" if phase==_phase else "Later"} for phase,label in teaching.PHASES],selection=None))
if _decision:
    _parent=get_pending()["manual"] if _number==1 else Harness(**teaching.saved(_s,"pending/round-1/adopted")["harness"])
    _views.extend([mo.md("**"+_decision["title"]+"**\\n\\n**Editor rationale:** "+_decision["rationale"]),mo.Html(ui.diff(json.dumps(asdict(_parent),indent=2),json.dumps(_decision["harness"],indent=2))),mo.md("The editor chose to keep the current instructions. The next button tests those same instructions again." if _decision["decision"]=="KEEP" else ""),review_pending])
if _s and _phase in ("compose","composition-test","adopted","done"):
    _probes=[teaching.latest(_s,f"pending/round-{_number}/probe-"+letter) for letter in ("a","b")]
    _views.append(pending_execution_table([row for letter,saved in zip(("A","B"),_probes) if saved for row in teaching.summary_rows([saved["result"]["run"]],"Candidate "+letter)]))
    if _phase=="compose":
        _views.extend([mo.md("**Before asking the editor:** choose A, B, the parent, or a combination, and cite a probe result. These optional notes are saved for you; the editor does not receive them. You can request composition without filling them in."),pending_my_choice,pending_my_reason])
    elif _s.get_draft(_reason_key,"") or _saved_choice!="undecided":
        _views.append(mo.Html(ui.result("Your reasoning before composition",{"Choice":_saved_choice,"Evidence":_s.get_draft(_reason_key,"")})))

_views.extend([improve_pending,pending_prerequisite_6 if not get_pending().get("manual") else mo.md("")])
if _s: _views.append(ui.branch_workbench(mo,_s,key="pending-improvement"))
if _phase=="done": _views.append(pending_next_step_6)
mo.vstack(_views)
''',True)
add('''
mo.stop(not improve_pending.value)
_s=get_pending()["session"]
_f=teaching.functions(_s)
_number,_phase,_label=teaching.next_phase(_s)
_prefix=f"pending/round-{_number}/"
_parent=get_pending()["manual"] if _number==1 else Harness(**teaching.saved(_s,"pending/round-1/adopted")["harness"])
_case=[c for c in CASES if c.split=="development"][_number-1]
if _phase=="propose":
    # Evidence comes from this parent's actual execution, never the fresh-case grades.
    _experience=[run_employee(_s,_case,_parent,_prefix+"starting",**teaching.hooks(_f))]
    if _number==2:
        _previous=teaching.saved(_s,"pending/round-1/adopted")
        _experience[0]["prior_experience"]={"source_execution":_previous["execution"],"case_id":"double-charge","lesson":_previous["lesson"],"limits":_previous["limits"]}
    editor_decision(_s,_number,"propose",_parent,_experience,tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
elif _phase in ("probe-a","probe-b","composition-test"):
    _decision=teaching.active_decision(_s,_number,_phase)
    mo.stop(not review_pending.value,mo.md("Read this version's diff and rationale, then check the review box."))
    _review=teaching.review_decision(_s,_decision)
    _harness=Harness(**_decision["harness"])
    _run=run_employee(_s,_case,_harness,_prefix+_phase+"-execution",**teaching.hooks(_f))
    assert _run["harness_fingerprint"]==_decision["fingerprint"]
    with _s.stage(_prefix+_phase,inputs={"execution":_run["stage_id"],"review":_review}) as _stage:
        if _stage.needs_run: _stage.record({"run":_run,"decision_fingerprint":_decision["fingerprint"]})
elif _phase=="compose":
    _probes=[teaching.saved(_s,_prefix+"probe-"+letter)["run"] for letter in ("a","b")]
    editor_decision(_s,_number,"compose",_parent,_probes,tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
elif _phase=="adopted":
    _decision=teaching.saved(_s,_prefix+"compose")
    _run=teaching.saved(_s,_prefix+"composition-test")["run"]
    assert _run["harness_fingerprint"]==_decision["fingerprint"]
    _reflection=reflect_execution(_s,_number,_run,tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
    _selected=Harness(**_decision["harness"]) if _run["status"]=="complete" else _parent
    with _s.stage(_prefix+"adopted",inputs={"execution":_run["stage_id"]}) as _stage:
        if _stage.needs_run: _stage.record({"harness":asdict(_selected),"fingerprint":_selected.fingerprint,"lesson":_reflection["lesson"],"limits":_reflection["limits"],"execution":_run["stage_id"],"retained_parent":_selected.fingerprint==_parent.fingerprint,"failure_fallback":_run["status"]!="complete"})
pending_checkpoint(_s,"improve/"+str(_number)+"/"+_phase)
if _number==2 and _phase=="adopted": pending_checkpoint(_s,"improve")
pending_refresh(_s)
''')
add('''
mo.stop(get_step()!="improve")
_s=get_pending().get("session")
mo.stop(not _s)
_stages=[s["id"] for s in _s.completed() if s["name"].startswith("pending/round-") and (s["result"].get("events") is not None or s["name"].endswith(("/propose","/compose")))]
mo.vstack([ui.evidence(mo,_s,_stages,question="Pick one proposed change. Read its diff, open its test run, and check whether the employee did what the editor expected. Was that change kept?"),ui.publication(mo,_s)])
''',True)
add('''
pending_prerequisite_7=ui.prerequisite(mo,"Finish both improvement rounds before freezing versions.","improve",move_pending)
mo.stop(get_step()!="final")
_s=get_pending().get("session")
_ready=bool(_s) and teaching.next_phase(_s)[1]=="done"
pending_final=mo.ui.run_button(label="All 12 executions are saved" if get_pending().get("final") else "Freeze versions and run 12 evaluations",disabled=not _ready or bool(get_pending().get("final")),full_width=True)
pending_retry=mo.ui.run_button(label="Retry publication only; reuse all saved executions",disabled=not bool(_s),full_width=True)
_missing=sum(r.get("explanation_judgment",{}).get("status")=="unavailable" for runs in get_pending().get("final",{}).get("runs",{}).values() for r in runs)
_judge_failures=[r["name"] for r in _s.read()["stages"].values() if r["status"]=="failed"] if _s else []
_retryable=sum(r.get("explanation_judgment",{}).get("status")=="unavailable" and _judge_failures.count("pending/judge/"+r["stage_id"])<2 for runs in get_pending().get("final",{}).get("runs",{}).values() for r in runs)
pending_retry_judges=mo.ui.run_button(label=f"Retry {_retryable} unavailable explanation judgment(s) only" if _retryable else "No further explanation-judge retries needed or available",disabled=not bool(_retryable),full_width=True)
mo.vstack([mo.Html(ui.step("7. Test the three instruction sets on new tickets", "Run three versions on four new tickets: the starting instructions, your edit, and the instructions kept after two editor rounds. The editor has not seen these tickets or their scores.","Compare the same ticket across all three versions. Check what happened to the account and what the employee said happened. Keep errors and missing judge answers visible.")),mo.md("These tickets are new to the employee. This is where we find out whether the revised handbook helps beyond the cases we used to write it."),pending_final,pending_retry,mo.md("**Some explanation scores are missing.** Review each failed judge execution in the recovery controls above and allow a retry, then use the button below. The employee’s work will not run again. If the judge fails twice, leave its score unavailable.") if _missing else mo.md(""),pending_retry_judges,pending_prerequisite_7 if not _ready else mo.md("")])
''',True)
add('''
mo.stop(not pending_final.value)
_s=get_pending()["session"]
_f=teaching.functions(_s)
_versions={"starting":get_pending()["starting"],"manual":get_pending()["manual"],"agent":Harness(**teaching.saved(_s,"pending/round-2/adopted")["harness"])}
with _s.stage("pending/freeze",sources={k:json.dumps(asdict(v),sort_keys=True) for k,v in _versions.items()}) as _freeze:
    if _freeze.needs_run: _freeze.record({"harnesses":{k:asdict(v) for k,v in _versions.items()}})
_all={}
for _label,_harness in _versions.items():
    _all[_label]=[run_employee(_s,c,_harness,"pending/final-"+_label,**teaching.hooks(_f)) for c in CASES if c.split=="heldout"]
for _runs in _all.values():
    for _run in _runs:
        try:
            _run["explanation_judgment"]=judge_explanation(_s,_run,_s.get_draft("pending/rubric","Check claims against recorded work."),validate=_f["my_judge_validation"],tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
        except Exception as _error:
            _run["explanation_judgment"]={"status":"unavailable","error":str(_error)}
with _s.stage("pending/final-comparison",inputs={"freeze":_freeze.id}) as _comparison:
    if _comparison.needs_run: _comparison.record({"runs":_all,"rows":teaching.comparison_rows(_all)})
_published=pending_publish(_s,"pending-final",_comparison.result["rows"])
pending_checkpoint(_s,"final",evidence={"Final "+k:r["run"] for k,r in _published.items()})
pending_refresh(_s)
''')
add('''
mo.stop(not pending_retry_judges.value)
_s=get_pending()["session"]
_f=teaching.functions(_s)
_all=copy.deepcopy(get_pending()["final"]["runs"])
with mo.status.spinner(title="Retrying unavailable explanation judgments only; employee executions stay saved"):
    for _runs in _all.values():
        for _run in _runs:
            if _run.get("explanation_judgment",{}).get("status")!="unavailable": continue
            try:
                _run["explanation_judgment"]=judge_explanation(_s,_run,_s.get_draft("pending/rubric","Check claims against recorded work."),validate=_f["my_judge_validation"],tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
            except Exception as _error:
                _run["explanation_judgment"]={"status":"unavailable","error":str(_error)}
_retry_records=[r["id"] for r in _s.read()["stages"].values() if r["name"].startswith("pending/judge/")]
with _s.stage("pending/final-comparison",inputs={"freeze":teaching.latest(_s,"pending/freeze")["id"],"judge_attempts":_retry_records}) as _comparison:
    if _comparison.needs_run: _comparison.record({"runs":_all,"rows":teaching.comparison_rows(_all)})
pending_publish(_s,"pending-final",_comparison.result["rows"])
pending_checkpoint(_s,"final")
pending_refresh(_s)
''')
add('''
mo.stop(not pending_retry.value)
_s=get_pending()["session"]
_s.retry_publication()
_f=teaching.functions(_s)
for _row in _s.read()["stages"].values():
    try:
        _trace_inputs=saved_trace_inputs(_s,_row)
        if _trace_inputs["events"] or _trace_inputs["requests"]:
            export_trace(_s,**_trace_inputs,tool_writer=_f["my_tool_span"],model_writer=_f["my_model_span"])
    except Exception as _error:
        set_display({**get_display(),"export_error":str(_error)})
_restored=teaching.restore(_s)
_manual=teaching.latest(_s,"pending/development-manual-comparison")
if _manual:
    pending_publish(_s,"pending-development",_manual["result"]["rows"])
elif _restored.get("manual_runs"):
    pending_publish(_s,"pending-development",teaching.comparison_rows({"starting":_restored.get("evaluation",{}).get("runs",_restored.get("original",[])),"manual":_restored["manual_runs"]}))
else:
    _development=teaching.latest(_s,"pending/development-evaluation")
    if _development: pending_publish(_s,"pending-development",_development["result"]["comparison"])
for _name,_label in (("pending/timeout-repair","pending-timeout-repair"),("pending/final-comparison","pending-final")):
    _row=teaching.latest(_s,_name)
    if _row: pending_publish(_s,_label,_row["result"]["rows"])
pending_refresh(_s)
''')
add('''
mo.stop(get_step()!="final")
_s=get_pending().get("session")
_final=get_pending().get("final",{})
mo.stop(not _final)
_rows=[row for label,runs in _final["runs"].items() for row in teaching.summary_rows(runs,label)]
_stages=[r["stage_id"] for runs in _final["runs"].values() for r in runs]
_cases=pending_visuals.aligned_cases(_final["runs"])
pending_final_case=mo.ui.dropdown({case_id:case_id for case_id in _cases},value=_cases[0],label="Compare one saved ticket across all three versions",full_width=True)
mo.vstack([pending_final_case,mo.accordion({"All saved evaluation rows":pending_execution_table(_rows)}),ui.evidence(mo,_s,_stages,question="Choose a ticket whose score changed, or a tie if none changed. Compare the final accounts and trace the actions that produced them. Which instruction do you think mattered?"),ui.publication(mo,_s)])
''',True)
add('''
pending_next_step_7=ui.next_step(mo,"Write up your comparison","report",move_pending)
mo.stop(get_step()!="final")
_final=get_pending().get("final",{})
mo.stop(not _final)
mo.vstack([mo.Html(pending_visuals.comparison_view(_final["runs"],pending_final_case.value)),pending_next_step_7])
''',True)
add('''
pending_prerequisite_8=ui.prerequisite(mo,"Complete the fresh-ticket comparison first.","final",move_pending)
mo.stop(get_step()!="report")
_s=get_pending().get("session")
pending_conclusion=mo.ui.text_area(value=_s.get_draft("pending/conclusion","") if _s else "",label="What changed, what happened, and what would you test next?",full_width=True,on_change=lambda value:_s.save_draft("pending/conclusion",value) if _s else None)
pending_report=mo.ui.run_button(label="Publish my conclusion with the comparison and evidence",disabled=not bool(get_pending().get("final")),full_width=True)
mo.vstack([mo.Html(ui.step("8. Explain what changed", "Choose one fresh ticket. Explain what you changed, what the employee did, and what the account check and judge found. Link to the trace and instructions you used. If the edit did not help, say so.","Publish your Report, then follow its links to the comparison and ticket. The saved code and result files are W&B Artifacts: versioned files you or a teammate can reopen later.")),pending_conclusion,pending_prerequisite_8 if not get_pending().get("final") else mo.md("")])
''',True)
add('''
mo.stop(get_step()!="report")
_s=get_pending().get("session")
pending_aria_conclusion=aria.investigation(mo,_s,"conclusion",interpretation=pending_conclusion.value,workshop="pending-direct-teaching")
pending_aria_conclusion
''', True, cell_id='pending_inc/aria/conclusion')
add('''
mo.vstack([aria.response(mo,pending_aria_conclusion),pending_report])
''', True, cell_id='pending_inc/aria_response/conclusion')
add('''
mo.stop(not pending_report.value)
_s=get_pending()["session"]
mo.stop(not pending_conclusion.value.strip(),mo.md("Write a conclusion before publishing."))
_s.save_draft("pending/conclusion",pending_conclusion.value)
_links=dict(_s.read()["progress"].get("evidence",{}))
for _key,_receipt in _s.read()["publications"].items():
    if _key.startswith("comparison/"):
        _links.update(ui.comparison_links(_receipt,suffix=_key.rsplit("/",1)[-1][:6]))
with _s.stage("pending/report",inputs={"conclusion":pending_conclusion.value,"links":_links}) as _stage:
    if _stage.needs_run:
        _url=publish_report(_s,pending_conclusion.value,_links)
        _stage.record({"url":_url,"conclusion":pending_conclusion.value})
pending_checkpoint(_s,"report",evidence={"Report":_stage.result["url"]})
pending_refresh(_s)
''')
add('''
mo.stop(get_step()!="report")
_report=get_pending().get("report",{})
mo.stop(not _report)
mo.Html(ui.links({"Open my Report":_report["url"]}))
''',True)

# Marimo only registers UI callbacks held in cell globals. Give navigation
# widgets explicit names in the generated notebook, including buttons embedded
# in stacks or conditional displays. This transformation never executes a cell.
def _bind_navigation_controls():
    import ast
    for index, cell in enumerate(cells):
        tree = ast.parse(cell.code)
        source = cell.code.splitlines(True)
        offsets = [0]
        for line in source:
            offsets.append(offsets[-1] + len(line))
        changes = []
        count = 0
        for statement in tree.body:
            calls = [node for node in ast.walk(statement)
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                     and isinstance(node.func.value, ast.Name) and node.func.value.id == 'ui'
                     and node.func.attr in {'navigation', 'next_step', 'prerequisite'}]
            assignments = []
            for call in calls:
                count += 1
                name = f'pending_navigation_{index}_{count}'
                start = offsets[call.lineno-1] + len(source[call.lineno-1].encode()[:call.col_offset].decode())
                end = offsets[call.end_lineno-1] + len(source[call.end_lineno-1].encode()[:call.end_col_offset].decode())
                assignments.append(name + ' = ' + cell.code[start:end] + '\n')
                changes.append((start, end, name))
            if assignments:
                position = offsets[statement.lineno-1]
                changes.append((position, position, ''.join(assignments)))
        for start, end, replacement in sorted(changes, reverse=True):
            cell.code = cell.code[:start] + replacement + cell.code[end:]

_bind_navigation_controls()
