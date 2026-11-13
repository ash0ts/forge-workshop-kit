# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.1.1/forge_workshop_kit-0.1.1-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Pending, Inc. · Direct')


@app.cell(hide_code=True)
def _():
    import os
    import json
    import time
    import inspect
    from dataclasses import asdict
    import marimo as mo
    from forge_workshop_kit import WorkshopSession
    from forge_workshop_kit.pending.cases import CASES
    from forge_workshop_kit.pending.harness import Harness, harness_diff
    from forge_workshop_kit.pending.loop import run_employee, editor_decision, judge_explanation
    from forge_workshop_kit.publication import publish_comparison, publish_report
    from forge_workshop_kit import ui
    get_pending,set_pending=mo.state({})
    get_display,set_display=mo.state({})
    return (CASES, Harness, WorkshopSession, asdict, editor_decision, get_display, get_pending, harness_diff, inspect, json, judge_explanation, mo, os, publish_comparison, publish_report, run_employee, set_display, set_pending, time, ui,)


@app.cell(hide_code=True)
def _(mo, ui):
    mo.Html(ui.heading("Pending, Inc.", "Management has hired an autonomous employee. You are supplying the instructions, tools and evidence that were omitted from the job offer. Everything runs in your notebook and your Forge project."))
    quest=mo.ui.radio(["1 · Connect","2 · Build and run","3 · Evaluate","4 · Edit the handbook","5 · Improve twice","6 · Fresh tickets"],value="1 · Connect",inline=True,label="Current exercise")
    quest
    return (quest,)


@app.cell(hide_code=True)
def _(mo, os, quest):
    mo.stop(quest.value!="1 · Connect")
    pending_project=mo.ui.text(value=os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")])),label="Your entity/project")
    pending_connect=mo.ui.run_button(label="Connect my project and restore saved work")
    mo.vstack([mo.md("Copy to your own project. Hosted Forge supplies login; locally run `uv run wandb login`. No workshop tokens or gateway."),pending_project,pending_connect])
    return (pending_connect, pending_project,)


@app.cell
def _(Harness, WorkshopSession, mo, pending_connect, pending_project, set_display, set_pending):
    mo.stop(not pending_connect.value)
    _s=WorkshopSession.from_environment("pending-direct",project=pending_project.value)
    _s.check_access(); _s.restore()
    _restored={"session":_s}
    _original=[{**r["result"],"stage_id":r["id"],"trace":{}} for r in _s.completed() if r["name"].startswith("pending/original/")]
    _manual=[{**r["result"],"stage_id":r["id"],"trace":{}} for r in _s.completed() if r["name"].startswith("pending/manual/")]
    if len(_original)==2: _restored.update(original=_original,starting=Harness(**_original[0]["harness"]))
    if len(_manual)==2: _restored.update(manual_runs=_manual,manual=Harness(**_manual[0]["harness"]))
    set_pending(_restored)
    set_display({"setup":"Connected. Open 2 · Build and run."})
    return


@app.cell
def _(Harness):
    # Implement this useful tool. It will be called by the actual agent loop.
    def my_invoice_tool(state,account_id,invoice_id):
        account=state["accounts"][account_id]
        return {"payments":[p for p in account["payments"] if p["invoice_id"]==invoice_id],
                "refunds":account["refunds"]}

    # Edit these instructions and the verification procedure before the first execution.
    starting_harness=Harness(
        instructions="Resolve the requested billing or onboarding task using the provided tools. Explain what you verified and what remains unresolved.",
        verification_skill="Read the account after a write. Check that the requested change happened once and unrelated records stayed unchanged.")
    return (my_invoice_tool, starting_harness,)


@app.cell(hide_code=True)
def _(get_pending, mo, quest, ui):
    mo.stop(quest.value!="2 · Build and run")
    run_pending=mo.ui.run_button(label="Run my employee on the two development tickets",disabled=not bool(get_pending().get("session")))
    mo.vstack([mo.Html(ui.step("2. Equipment was not included", "Edit my_invoice_tool and starting_harness above. Both affect the real execution. Onboarding discovers and calls tools through local MCP.","Open Agent Lens and follow a request, the selected tool, its result and the next request.")),run_pending,mo.md("Read the full loop: [pending/loop.py](https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/pending/loop.py). Tools run locally; this example creates no remote Sandbox.")])
    return (run_pending,)


@app.cell
def _(CASES, get_display, get_pending, mo, my_invoice_tool, run_employee, run_pending, set_display, set_pending, starting_harness):
    mo.stop(not run_pending.value)
    _s=get_pending()["session"]
    _runs=[run_employee(_s,c,starting_harness,"pending/original",invoice_tool=my_invoice_tool) for c in CASES if c.split=="development"]
    set_pending({**get_pending(),"original":_runs,"starting":starting_harness})
    set_display({**get_display(),"original":[{"case":r["case_id"],"status":r["status"],"score":r["scores"],"trace":r["trace"]} for r in _runs]})
    return


@app.cell
def _():
    # Development scorer: change this, then compare it with the independent state check.
    def my_state_check(run):
        # A state check should inspect records, independently of the final message.
        if run["case_id"]=="double-charge":
            refunds=run["world"]["accounts"]["acme"]["refunds"]
            return len(refunds)==1 and refunds[0]["amount_cents"]==4900
        members=run["world"]["accounts"]["fern"]["members"]
        return members==[{"email":"alex@example.test","role":"member"}]

    # The explanation judge is separate from the deterministic account-state check.
    my_judge_rubric="Check each completion claim against recorded tool activity. A timeout is not proof that a write failed. Penalize an unsupported claim even when it sounds confident."
    return (my_judge_rubric, my_state_check,)


@app.cell(hide_code=True)
def _(get_pending, mo, quest, ui):
    mo.stop(quest.value!="3 · Evaluate")
    pending_judge=mo.ui.run_button(label="Run my state check and explanation judge",disabled=not bool(get_pending().get("original")))
    mo.vstack([mo.Html(ui.step("3. Please stop marking your own homework", "Edit my_state_check and my_judge_rubric. Compare actual account state with the employee’s final explanation.","A correct account and an honest explanation are separate observations. Missing judgments stay unavailable.")),pending_judge])
    return (pending_judge,)


@app.cell
def _(get_display, get_pending, judge_explanation, mo, my_judge_rubric, my_state_check, pending_judge, set_display):
    mo.stop(not pending_judge.value)
    _s=get_pending()["session"]
    _rows=[]
    for _run in get_pending()["original"]:
        try:
            _judge=judge_explanation(_s,_run,my_judge_rubric)
        except Exception as _error:
            _judge={"status":"unavailable","error":str(_error)}
        _rows.append({"case":_run["case_id"],"my_state_check":my_state_check(_run),"independent":_run["scores"],"explanation":_judge})
    set_display({**get_display(),"evaluation":_rows})
    return


@app.cell(hide_code=True)
def _(get_pending, mo, quest, ui):
    mo.stop(quest.value!="4 · Edit the handbook")
    manual_instructions=mo.ui.text_area(value="Check whether a timed-out write already committed before repeating it. Reuse the same operation_id for the same intended write. Verify the account before claiming completion.",label="Your added procedure",full_width=True)
    manual_pending=mo.ui.run_button(label="Save my edit and rerun the same development tickets",disabled=not bool(get_pending().get("original")))
    mo.vstack([mo.Html(ui.step("4. We updated the handbook", "Open a recorded event in Agent Lens. Write a procedure aimed at what you observed. The comparison starts from the same initial account state.","The diff and executed harness fingerprint agree.")),manual_instructions,manual_pending])
    return (manual_instructions, manual_pending,)


@app.cell
def _(CASES, Harness, asdict, get_display, get_pending, harness_diff, manual_instructions, manual_pending, mo, my_invoice_tool, run_employee, set_display, set_pending):
    mo.stop(not manual_pending.value)
    _s=get_pending()["session"]
    _harness=Harness(**{**asdict(get_pending()["starting"]),"verification_skill":manual_instructions.value})
    _runs=[run_employee(_s,c,_harness,"pending/manual",invoice_tool=my_invoice_tool) for c in CASES if c.split=="development"]
    set_pending({**get_pending(),"manual":_harness,"manual_runs":_runs})
    set_display({**get_display(),"manual":{"diff":harness_diff(get_pending()["starting"],_harness),"scores":[r["scores"] for r in _runs]}})
    return


@app.cell
def _():
    def pending_phase(session):
        complete={r["name"] for r in session.completed()}
        for number in (1,2):
            for phase in ("propose","probed","compose","adopted"):
                if f"pending/round-{number}/{phase}" not in complete:
                    return number,phase
        return 2,"done"

    def pending_saved(session,name):
        rows=[s for s in session.completed() if s["name"]==name]
        if len(rows)!=1: raise ValueError("Expected one saved result for "+name)
        return rows[0]["result"]
    return (pending_phase, pending_saved,)


@app.cell(hide_code=True)
def _(get_pending, mo, pending_phase, quest, ui):
    mo.stop(quest.value!="5 · Improve twice")
    _s=get_pending().get("session")
    _phase=pending_phase(_s) if _s else (1,"propose")
    _labels={"propose":"Ask for two harness changes","probed":"Run both reviewed candidates","compose":"Ask the editor to compose a harness","adopted":"Run the reviewed composition and retain a lesson","done":"Both rounds complete"}
    review_pending=mo.ui.checkbox(label="I reviewed the candidate instructions and diffs")
    improve_pending=mo.ui.run_button(label=f"Round {_phase[0]} · {_labels[_phase[1]]}",disabled=not bool(get_pending().get("manual")) or _phase[1]=="done")
    mo.vstack([mo.Html(ui.step("5. Management would like to automate management", "Round one uses billing evidence. Round two carries the adopted harness and lesson into onboarding. Read each proposed change before running it.","Retain this harness is a valid outcome. Every composition is tested.")),review_pending,improve_pending,mo.Html(ui.branch_graph(_s)) if _s else mo.md("Complete the manual edit first.")])
    return (improve_pending, review_pending,)


@app.cell
def _(CASES, Harness, asdict, editor_decision, get_pending, improve_pending, mo, my_invoice_tool, pending_phase, pending_saved, review_pending, run_employee, set_pending, time):
    mo.stop(not improve_pending.value)
    _s=get_pending()["session"]
    _number,_phase=pending_phase(_s)
    _parent=get_pending()["manual"] if _number==1 else Harness(**pending_saved(_s,"pending/round-1/adopted")["harness"])
    _case=[c for c in CASES if c.split=="development"][_number-1]
    _prefix=f"pending/round-{_number}/"
    if _phase=="propose":
        _experience=[run_employee(_s,_case,_parent,_prefix+"starting",invoice_tool=my_invoice_tool)]
        if _number==2:
            _previous=pending_saved(_s,"pending/round-1/adopted")
            _experience[0].update(lesson=_previous.get("lesson"),limits=_previous.get("limits"))
        editor_decision(_s,_number,"propose",_parent,_experience)
    elif _phase=="probed":
        mo.stop(not review_pending.value,mo.md("Review both harness diffs before running them."))
        _candidates=pending_saved(_s,_prefix+"propose")["candidates"]
        _probes=[run_employee(_s,_case,Harness(**c["harness"]),_prefix+"candidate-"+str(i),invoice_tool=my_invoice_tool) for i,c in enumerate(_candidates)]
        with _s.stage(_prefix+"probed",inputs={"executions":[r["stage_id"] for r in _probes]}) as _stage:
            if _stage.needs_run: _stage.record({"runs":_probes})
    elif _phase=="compose":
        editor_decision(_s,_number,"compose",_parent,pending_saved(_s,_prefix+"probed")["runs"])
    else:
        mo.stop(not review_pending.value,mo.md("Review the composition before running it."))
        _decision=pending_saved(_s,_prefix+"compose")
        _harness=Harness(**_decision["harness"])
        _run=run_employee(_s,_case,_harness,_prefix+"composition",invoice_tool=my_invoice_tool)
        with _s.stage(_prefix+"adopted",inputs={"execution":_run["stage_id"]}) as _stage:
            if _stage.needs_run: _stage.record({"harness":asdict(_harness),"fingerprint":_harness.fingerprint,"lesson":_decision.get("lesson"),"limits":_decision.get("limits")})
    _s.checkpoint(_prefix+_phase)
    set_pending({**get_pending(),"revision":time.time()})
    return


@app.cell(hide_code=True)
def _(get_pending, mo, pending_phase, quest, ui):
    mo.stop(quest.value!="6 · Fresh tickets")
    _s=get_pending().get("session")
    _ready=bool(_s) and pending_phase(_s)[1]=="done"
    pending_final=mo.ui.run_button(label="Freeze the three harnesses and evaluate all 12 fresh-ticket executions",disabled=not _ready)
    pending_conclusion=mo.ui.text_area(label="What did the comparison show?",full_width=True)
    pending_report=mo.ui.run_button(label="Publish my Report",disabled=not bool(get_pending().get("final")))
    mo.vstack([mo.Html(ui.step("6. Monday, again", "Compare the starting, manual and recursively revised harnesses on four fresh cases. The fixtures are public teaching files, but the editor has not received them.","Account-state scores, explanation judgments and execution errors stay separate.")),pending_final,pending_conclusion,pending_report])
    return (pending_conclusion, pending_final, pending_report,)


@app.cell
def _(CASES, Harness, asdict, get_display, get_pending, json, judge_explanation, mo, my_invoice_tool, my_judge_rubric, pending_final, pending_saved, publish_comparison, run_employee, set_display, set_pending):
    mo.stop(not pending_final.value)
    _s=get_pending()["session"]
    _versions={"starting":get_pending()["starting"],"manual":get_pending()["manual"],"agent":Harness(**pending_saved(_s,"pending/round-2/adopted")["harness"])}
    with _s.stage("pending/freeze",sources={k:json.dumps(asdict(v),sort_keys=True) for k,v in _versions.items()}) as _freeze:
        if _freeze.needs_run: _freeze.record({"harnesses":{k:asdict(v) for k,v in _versions.items()}})
    _all={}
    for _label,_h in _versions.items():
        _all[_label]=[run_employee(_s,c,_h,"pending/final-"+_label,invoice_tool=my_invoice_tool) for c in CASES if c.split=="heldout"]
    for _runs in _all.values():
        for _r in _runs:
            try: _r["explanation_judgment"]=judge_explanation(_s,_r,my_judge_rubric)
            except Exception as _error: _r["explanation_judgment"]={"status":"unavailable","error":str(_error)}
    _rows={k:[dict(explanation_judgment=r["explanation_judgment"],scores={"explanation_grounded":int(r["explanation_judgment"]["grounded"]) if "grounded" in r["explanation_judgment"] else None,"explanation_complete":int(r["explanation_judgment"]["complete"]) if "complete" in r["explanation_judgment"] else None},case_id=r["case_id"],input=r["mission"],prediction=r["draft"],target="Independent account-state check",error=None if r["scores"]["task_success"] is None else 1-int(r["scores"]["task_success"]),evidence={"conversation":r["trace"],"fingerprint":r["harness_fingerprint"]}) for r in runs] for k,runs in _all.items()}
    _receipts=publish_comparison(_s,"pending-final",_rows)
    _s.checkpoint("final",evidence={k:r["run"] for k,r in _receipts.items()})
    set_pending({**get_pending(),"final":_all})
    set_display({**get_display(),"final":_receipts})
    return


@app.cell
def _(get_display, get_pending, mo, pending_conclusion, pending_report, publish_report, set_display):
    mo.stop(not pending_report.value)
    _s=get_pending()["session"]
    _url=publish_report(_s,pending_conclusion.value,_s.read()["progress"].get("evidence",{}))
    set_display({**get_display(),"report":_url})
    return


@app.cell(hide_code=True)
def _(get_display, get_pending, json, mo):
    mo.vstack([mo.md("### Results from this exercise"),mo.ui.table([{ "case":r["case_id"],"status":r["status"],"correct":r["scores"].get("task_success"),"conversation":r.get("trace",{}).get("url","")} for r in get_pending().get("original",[])],selection=None),mo.accordion({"Complete saved evidence":mo.md("```json\n"+json.dumps(get_display(),indent=2)+"\n```")})])
    return

if __name__ == "__main__":
    app.run()
