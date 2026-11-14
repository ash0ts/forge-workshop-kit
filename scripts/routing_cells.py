"""Authored request-routing workshop. Keep training and evaluation calls visible."""
from notebook_builder import Cell
cells=[]
def add(code,hide=False,cell_id=None): cells.append(Cell(code,hide=hide,cell_id=cell_id))

add('''
import json
import time
from pathlib import Path
import joblib
import marimo as mo
from forge_workshop_kit import WorkshopSession, setup, ui, routing, routing_teaching as teaching
from forge_workshop_kit import routing_release as release_lab
from forge_workshop_kit.review import save_review, reviewed_dataset
from forge_workshop_kit.provider import validated_json, Provider
from forge_workshop_kit.session import digest
from forge_workshop_kit.traces import event, export_trace, saved_trace_inputs
from forge_workshop_kit.publication import publish_comparison, publish_report
get_context, set_context = mo.state({})
get_step, set_step = mo.state("setup", allow_self_loops=True)
get_output, set_output = mo.state({})
get_revision, set_revision = mo.state(0)
''',True)
add('''
def go_to(step):
    session=get_context().get("session")
    if session: session.set_view(step)
    set_step(step)
def refresh():
    set_revision(lambda previous: previous+1)
def show_result(name,result):
    set_output(lambda old:{**old,name:result})
def trace_saved(stage):
    session=get_context()["session"]
    try:
        receipt=export_trace(session, **saved_trace_inputs(session,stage["id"] if isinstance(stage,dict) else stage.id), tool_writer=instrument_tool)
        return {"status":"published","url":receipt["url"]}
    except Exception as error:
        return {"status":"publication pending","error":str(error),"next":"Retry saved publications; do not rerun training."}
def publish_routing_results(session, *, include_judge=True, include_final=True):
    # This function reads completed records only. It never asks a model or classifier to run.
    status={}
    if include_judge:
        summary=teaching.saved(session,"routing/judge/summary")
        if summary:
            state=session.read()
            reviews={state["reviews"][identity]["case_id"]:state["reviews"][identity] for identity in summary["config"].get("reviews",[]) if identity in state.get("reviews",{})}
            attempts={row["case_id"]:row for row in summary["result"].get("attempts",[])}
            rows=[]
            for human in summary["result"]["human_reviews"]:
                case_id=human["case_id"]
                review=reviews.get(case_id,{})
                judgment=summary["result"]["predictions"].get(case_id)
                agreed=judgment["failed"]==human["failed"] if judgment is not None else None
                attempt=attempts.get(case_id,{})
                trace=state["publications"].get("trace/"+attempt.get("stage_id",""),{})
                rows.append({"case_id":case_id,"input":{"request":review.get("evidence",{}).get("text"),"proposed_intent":review.get("proposed_label")},
                    "prediction":{"failed":judgment["failed"] if judgment is not None else None,"reason":judgment.get("reason") if judgment is not None else None,"status":"available" if judgment is not None else "unavailable"},
                    "target":{"failed":human["failed"],"accepted_intent":review.get("accepted_label")},"error":float(not agreed) if agreed is not None else None,
                    "scores":{"agrees_with_review":agreed},"evidence":{"review_id":review.get("id"),"dataset_version":review.get("dataset_version"),"judge_stage":attempt.get("stage_id"),"agent_lens":trace.get("url") if trace.get("verified") else None}})
            try:
                status["judge"]=publish_comparison(session,"banking-routing-judge-alignment",{"automated-judge":rows})
            except Exception as error:
                status["judge"]={"status":"publication pending","error":str(error)}
    if include_final:
        records={label:teaching.saved(session,"routing/final/"+label) for label in ("tfidf","embedding","selected")}
        if all(records.values()):
            versions={label:record["result"]["predictions"] for label,record in records.items()}
            try:
                status["final"]=publish_comparison(session,"banking-routing-final",{label:teaching.publication_rows(rows) for label,rows in versions.items()},summaries={label:routing.score(rows) for label,rows in versions.items()})
            except Exception as error:
                status["final"]={"status":"publication pending","error":str(error)}
    records=release_lab.comparisons(session)
    if records:
        try:
            versions={label:release_lab.comparison_rows(session,record) for label,record in records.items()}
            status["release"]=publish_comparison(session,"banking-routing-release-drill",versions,summaries={label:record["result"]["metrics"] for label,record in records.items()})
        except Exception as error:status["release"]={"status":"publication pending","error":str(error)}
    return status

def load_fitted(record):
    session=get_context()["session"]
    path=session.file(record["result"]["model_file"])
    if routing.checksum(path)!=record["result"]["model_sha256"]:
        raise ValueError("Saved classifier checksum differs. Restore its checkpoint before using it.")
    return joblib.load(path)
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
routing_navigation=ui.navigation(mo,teaching.STEPS,get_step(),go_to,completed=teaching.completed_steps(_s),label="Workshop steps")
mo.vstack([mo.Html(ui.STYLE),routing_navigation,mo.Html(ui.context(_s)) if _s else mo.md("Copy this notebook to your own Forge project. Opening it does not send model requests or train a classifier.")])
''',True)
add('''
_s = get_context().get("session")
_revision = get_revision()
_view = get_step()
routing_recovery_refresh = mo.ui.button(label="Check for stopped or failed work", on_click=lambda _: set_revision(lambda previous: previous + 1), disabled=not bool(_s))
_options = _s.recovery_options() if _s else []
_choices = {setup.recovery_label(_s.workshop, row) + " · " + row["id"][:6]: row["id"] for row in _options}
routing_recovery_choice = mo.ui.dropdown(_choices, value=next(iter(_choices), None), label="Execution to review", full_width=True) if _choices else mo.ui.dropdown({"No failed executions": ""}, value="No failed executions", disabled=True)
mo.vstack([mo.md("**A run stopped?** Check its saved status here. Reviewing it never starts work."), routing_recovery_refresh, routing_recovery_choice]) if _options else mo.accordion({"A run stopped? Review recovery": mo.vstack([mo.md("Click below to read saved execution status. Completed results stay saved. An upload failure uses Retry publication in the final comparison instead."), routing_recovery_refresh])})
''', True)
add('''
_s = get_context().get("session")
_row = next((row for row in _s.recovery_options() if row["id"] == routing_recovery_choice.value), None) if _s else None
_needs_confirmation = bool(_row and (_row["has_uncertain_requests"] or _row["status"] == "running"))
routing_recovery_confirm = mo.ui.checkbox(label="I checked that the previous execution has stopped. Keep unresolved requests charged at their reserved maximum.")
routing_recovery_allow = mo.ui.run_button(label="Allow retry of this failed execution", disabled=not bool(_row), full_width=True)
mo.vstack([mo.Html(ui.result("Review the saved execution", {"Execution": _row["name"], "Status": _row["status"], "Issue": _row.get("error") or "The execution has not finished.", "Next": "Allow another attempt, then click the normal run button for this step. This control does not run the experiment."}, status="failed")), routing_recovery_confirm if _needs_confirmation else mo.md("The previous attempt has ended. Its result and costs remain in the record."), routing_recovery_allow]) if _row else mo.md("")
''', True)
add('''
mo.stop(not routing_recovery_allow.value)
_s = get_context()["session"]
try:
    _route = _s.retry_stage(routing_recovery_choice.value, confirm_stopped=routing_recovery_confirm.value)
    _message = "Retry allowed. Return to this step’s run button to start attempt " + str(_route["attempt"]) + ". Completed work will be reused."
except Exception as _error:
    _message = str(_error)
set_output(lambda current: {**current, "recovery": _message})
refresh()
''', True)
add('''
_message = get_output().get("recovery")
mo.callout(mo.md(_message), kind="info") if _message else mo.md("")
''', True)
add('''
help_message = mo.ui.text_area(label="What do you need help with?", full_width=True)
help_button = mo.ui.run_button(label="Send a help request", disabled=not bool(get_context().get("session")))
mo.accordion({"Ask the facilitator": mo.vstack([help_message, help_button, mo.md("Tell the facilitator which step you’re on and what happened. They can read this request in the workshop monitor.")])})
''', True)
add('''
mo.stop(not help_button.value)
get_context()["session"].request_help(help_message.value)
mo.md("Help request saved. Send an empty message when it is resolved.")
''', True)
add('''
mo.stop(get_step()!="setup")
mo.vstack([mo.md("**5½-hour workshop, including breaks and exercises.** [Open the companion deck](https://ash0ts.github.io/forge-workshop-kit/routing/). Its worked examples explain the code you will edit below."),mo.Html(ui.heading("Route customer requests and learn from mistakes", "You're joining a fictional bank's support team. A missing card, a broken card, and an unfamiliar payment need different workflows. You'll build a router, inspect its mistakes, review labels, and test a revised classifier.", theme="routing")),mo.md("The messages come from **Banking77**, published by PolyAI's researchers. It contains 10,003 training messages and 3,080 test messages across 77 banking intents. We reserve ten training examples per intent for validation and ten for review. The official test set stays untouched until the final comparison. These are public teaching data, not your customers' records."),mo.md("We'll start with word counts weighted by how distinctive they are, then train the same classifier on frozen sentence embeddings. After that, you decide which uncertain requests need a person. The support queue is fictional. Its enthusiasm for automatically forwarding tickets is familiar."),mo.md("**Today's output:** a selected router, the reviewed examples it learned from, an evaluation on matching requests, and a trace explaining one routing or labeling decision.")])
''',True)
add('''
_context=setup.project_context()
project_input=mo.ui.text(value=_context["project"],label="Your Forge project",disabled=_context["hosted"] and _context["detected"],full_width=True)
allowance=mo.ui.number(value=8,start=.01,stop=1000,label="Inference allowance in USD; notebook CPU is separate")
connect=mo.ui.run_button(label="Connect and restore my work")
mo.vstack([project_input,allowance,connect,mo.md("On a laptop, authenticate with `uv run wandb login`. Use a project you can write to. Classifier training runs on this notebook's CPU; only the explicit routing and judge buttons use billed inference.")]) if get_step()=="setup" else mo.md("")
''',True)
add('''
mo.stop(not connect.value)
_s=WorkshopSession.from_environment("banking-routing",project=project_input.value,budget_usd=allowance.value)
_access=_s.check_access()
_s.restore()
setup.save_access(_s,_access)
set_context({"session":_s})
set_step(_s.get_view("setup"))
refresh()
mo.md("Connected. Send the setup trace below, then inspect the messages.")
''',True)
add('''
# This scope writes the tool spans used in every export below.
# Add another descriptive attribute, then find it in Agent Lens.
def instrument_tool(observation):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=observation["name"],arguments=observation["arguments"],
        result=observation["result"],tool_call_id=observation["id"],
        started_at=stamp(observation["started_at"]),ended_at=stamp(observation["ended_at"])) as span:
        span.set_attributes({"workshop.exercise":"request-routing"})
        if observation.get("error"):span.record_error(RuntimeError(observation["error"]))
        return format(trace.get_current_span().get_span_context().span_id,"016x")
''')
add('''
first_trace=mo.ui.run_button(label="Send my first Agent Lens trace",disabled=not bool(get_context().get("session")))
mo.vstack([mo.md("Add an attribute in `instrument_tool` above. Send the trace, open its tool span, and find your attribute."),first_trace]) if get_step()=="setup" else mo.md("")
''',True)
add('''
mo.stop(not first_trace.value)
_s=get_context()["session"]
with _s.stage("routing/setup",config={"purpose":"check notebook tracing"}) as _stage:
    if _stage.needs_run:
        _result,_event=event("inspect_routing_environment",{},lambda:{"project":_s.project,"training":"CPU","classes":77},on_error=_stage.record_event)
        _stage.record({"events":[_event]})
show_result("setup",trace_saved(_stage))
_s.checkpoint("setup")
refresh()
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
load_data_button=mo.ui.run_button(label="Download and check Banking77",disabled=not bool(_s))
mo.vstack([mo.Html(ui.step("Inspect the support queue","Download the pinned public messages and cached MiniLM features. The cache avoids encoding 13,083 messages during the workshop; the preparation script records the encoder revision and every file checksum.","Read a request, choose a likely intent, then reveal its published label.")),load_data_button,mo.md("[Data source and CC-BY-4.0 license](https://github.com/PolyAI-LDN/task-specific-datasets) · [Feature preparation code](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_routing.py)")]) if get_step()=="data" else mo.md("")
''',True)
add('''
mo.stop(not load_data_button.value)
_s=get_context()["session"]
_path=teaching.download(_s.root/"datasets/banking77-v1")
_data=routing.load_data(_path)
with _s.stage("routing/data",config={"manifest":routing.checksum(_path/"manifest.json")}) as _stage:
    if _stage.needs_run:_stage.record({"counts":_data["manifest"]["counts"],"dataset_manifest":_data["manifest"]},files=list(_path.iterdir()))
set_context({**get_context(),"data_path":str(_path)})
_s.checkpoint("data")
refresh()
''',True)
add('''
def get_data():
    session=get_context()["session"]
    record=teaching.saved(session,"routing/data")
    if not record:raise ValueError("Download Banking77 in the data step first.")
    # Restore places the exact dataset files beside this completed stage.
    return routing.load_data(session.file("outputs/"+record["id"]))
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
_ready=bool(_s and teaching.saved(_s,"routing/data"))
_cases=routing.partition(get_data(),"validation")[0][:30] if _ready else []
request_picker=mo.ui.dropdown({row["text"]:row["id"] for row in _cases},value=_cases[0]["text"] if _cases else None,label="Request to inspect",full_width=True)
reveal_label=mo.ui.checkbox(label="Show the published label")
mo.vstack([request_picker,reveal_label]) if get_step()=="data" and _ready else mo.md("")
''',True)
add('''
mo.stop(get_step()!="data" or not request_picker.value)
_row=next(row for row in routing.partition(get_data(),"validation")[0] if row["id"]==request_picker.value)
mo.md("Published intent: **"+_row["label"]+"**") if reveal_label.value else mo.md("Explain which workflow this request needs before checking its label.")
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
classifier_editor=mo.ui.code_editor(value=_s.get_draft("routing/classifier",teaching.CLASSIFIER_STARTER) if _s else teaching.CLASSIFIER_STARTER,language="python",on_change=lambda source:_s.save_draft("routing/classifier",source) if _s else None,debounce=False)
check_classifier=mo.ui.run_button(label="Check my classifier code")
train_classifiers=mo.ui.run_button(label="Train both classifiers on the same messages",disabled=not bool(_s and teaching.saved(_s,"routing/data")))
mo.vstack([mo.Html(ui.step("Train two routers","Complete make_classifier. Both models learn from the same 8,463 messages. The first uses word unigrams and bigrams; the second uses fixed 384-number sentence vectors. No encoder weights change.","Compare validation macro-F1 and review coverage. Open the run in Forge to inspect its code and settings.")),classifier_editor,check_classifier,train_classifiers,mo.accordion({"Hint":mo.md("Return a scikit-learn LogisticRegression object with C=10, max_iter=1000, random_state=17."),"Worked answer":mo.md("```python\\n"+teaching.CLASSIFIER_SOLUTION+"\\n```")})]) if get_step()=="baseline" else mo.md("")
''',True)
add('''
mo.stop(not check_classifier.value)
try:
    show_result("classifier check",teaching.check_classifier(classifier_editor.value))
except Exception as _error:
    show_result("classifier check",{"status":"needs work","message":str(_error)})
''',True)
add('''
mo.stop(not train_classifiers.value)
teaching.check_classifier(classifier_editor.value)
_s=get_context()["session"]
_data=get_data()
_factory=teaching.functions(classifier_editor.value)["make_classifier"]
for _kind in ("tfidf","embedding"):
    with _s.stage("routing/baseline/"+_kind,config={"kind":_kind,"seed":17,"dataset":routing.checksum(_data["root"]/"manifest.json")},sources={"classifier.py":classifier_editor.value}) as _stage:
        if _stage.needs_run:
            _started=time.time()
            _fitted=routing.fit_classifier(_data,_kind,factory=_factory)
            _rows=routing.predict(_fitted,_data,"validation")
            _review=routing.predict(_fitted,_data,"review")
            _model_path=_stage.output_dir/"classifier.joblib"
            joblib.dump(_fitted,_model_path)
            _event={"id":_stage.id+"/train","name":"train_routing_classifier","arguments":{"kind":_kind,"training_examples":len(_fitted["training_ids"])},"result":routing.score(_rows),"started_at":_started,"ended_at":time.time(),"status":"complete"}
            _stage.record({"model_file":str(_model_path.relative_to(_s.root)),"model_sha256":routing.checksum(_model_path),"validation":_rows,"review":_review,"metrics":routing.score(_rows),"events":[_event]},files=[_model_path])
    show_result(_kind,trace_saved(_stage))
_s.checkpoint("baseline")
refresh()
''')
add('''
_s=get_context().get("session")
_revision=get_revision()
_baselines={name:teaching.saved(_s,"routing/baseline/"+name) for name in ("tfidf","embedding")} if _s else {}
mo.ui.table(teaching.metrics_table({name:row["result"]["validation"] for name,row in _baselines.items() if row}),selection=None) if get_step()=="baseline" and any(_baselines.values()) else mo.md("")
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
policy_editor=mo.ui.code_editor(value=_s.get_draft("routing/policy",teaching.POLICY_STARTER) if _s else teaching.POLICY_STARTER,language="python",on_change=lambda source:_s.save_draft("routing/policy",source) if _s else None,debounce=False)
check_policy=mo.ui.run_button(label="Check my review rule")
review_threshold=mo.ui.slider(start=0,stop=1,step=.05,value=.5,label="Send to a person below this confidence")
_embedding=teaching.saved(_s,"routing/baseline/embedding") if _s else None
_review_rows=routing.select_review(_embedding["result"]["review"],50) if _embedding else []
review_picker=mo.ui.dropdown({r["text"]:r["case_id"] for r in _review_rows},value=_review_rows[0]["text"] if _review_rows else None,label="Request to review",full_width=True)
_intents=sorted({r["label"] for r in get_data()["rows"]}) if _embedding else []
accepted_label=mo.ui.dropdown(_intents,value=None,label="Your accepted intent",full_width=True)
reviewer=mo.ui.text(label="Reviewer name or workshop alias",full_width=True)
save_label=mo.ui.run_button(label="Save my reviewed label",disabled=not bool(_embedding))
mo.vstack([mo.Html(ui.step("Review the uncertain requests","Complete needs_review and move the threshold. Coverage is the fraction routed automatically; accuracy among those cases leaves the deferred requests out. Review at least four examples, including a correct route and a mistake.","Save your own labels. The revised classifier can train on them; final-test cases stay out of training.")),policy_editor,check_policy,review_threshold,review_picker,accepted_label,reviewer,save_label,mo.accordion({"Worked answer":mo.md("```python\\n"+teaching.POLICY_SOLUTION+"\\n```")})]) if get_step()=="review" else mo.md("")
''',True)
add('''
mo.stop(not check_policy.value)
try:
    show_result("review rule",teaching.check_policy(policy_editor.value))
except Exception as _error:
    show_result("review rule",{"status":"needs work","message":str(_error)})
''',True)
add('''
mo.stop(get_step()!="review")
_s=get_context().get("session")
_revision=get_revision()
_record=teaching.saved(_s,"routing/baseline/embedding") if _s else None
if _record:
    try:
        _fn=teaching.functions(policy_editor.value)["needs_review"]
        _rows=[{**r,"abstained":bool(_fn(r["confidence"],review_threshold.value))} for r in _record["result"]["validation"]]
        mo.output.replace(mo.Html(ui.result("What the review threshold changes",routing.score(_rows))))
    except Exception as _error:mo.output.replace(mo.md("Complete needs_review above: "+str(_error)))
''',True)
add('''
mo.stop(get_step()!="review" or not review_picker.value)
_s=get_context()["session"]
_row=next(row for row in teaching.saved(_s,"routing/baseline/embedding")["result"]["review"] if row["case_id"]==review_picker.value)
mo.Html(ui.result("Read the request before accepting a label",{"Request":_row["text"],"Classifier choice":_row["prediction"],"Second choice":_row["runner_up"],"Confidence":round(_row["confidence"],3),"Your task":"Choose the intent you think matches and explain it to a partner. The published reference label is not supplied to the judge."}))
''',True)
add('''
mo.stop(not save_label.value)
_s=get_context()["session"]
_row=next(r for r in teaching.saved(_s,"routing/baseline/embedding")["result"]["review"] if r["case_id"]==review_picker.value)
_dataset=routing.checksum(get_data()["root"]/"manifest.json")
_review=save_review(_s,case_id=_row["case_id"],proposed_label=_row["prediction"],accepted_label=accepted_label.value,reviewer=reviewer.value,dataset_version=_dataset,evidence={"text":_row["text"],"confidence":_row["confidence"]})
_regression=reviewed_dataset(_s,_dataset)
with _s.stage("routing/review",config={"dataset":_regression["version"]}) as _stage:
    if _stage.needs_run:
        _path=_stage.output_dir/"reviewed-cases.json"
        _path.write_text(json.dumps(_regression,indent=2)+"\\n")
        _stage.record(_regression,files=[_path])
_s.checkpoint("review")
show_result("review",{"saved":_review["case_id"],"accepted":accepted_label.value,"reviewed_cases":len(_regression["rows"])})
refresh()
''')
add('''
_s=get_context().get("session")
_revision=get_revision()
judge_editor=mo.ui.code_editor(value=_s.get_draft("routing/judge-validator",teaching.VALIDATOR_STARTER) if _s else teaching.VALIDATOR_STARTER,language="python",on_change=lambda source:_s.save_draft("routing/judge-validator",source) if _s else None,debounce=False)
judge_rubric=mo.ui.text_area(value=_s.get_draft("routing/judge-rubric",teaching.JUDGE_RUBRIC) if _s else teaching.JUDGE_RUBRIC,label="Failure-tag instructions",full_width=True,on_change=lambda value:_s.save_draft("routing/judge-rubric",value) if _s else None)
check_judge=mo.ui.run_button(label="Check my judge validator")
run_prompted=mo.ui.run_button(label="Route eight development requests with the fixed model",disabled=not bool(_s and teaching.saved(_s,"routing/baseline/embedding")))
run_judge=mo.ui.run_button(label="Compare the judge with up to eight of my reviews",disabled=not bool(_s and teaching.saved(_s,"routing/review")))
retry_judge_publication=mo.ui.run_button(label="Retry publishing my saved judge comparison",disabled=not bool(_s and teaching.saved(_s,"routing/judge/summary")))
mo.vstack([mo.Html(ui.step("Check whether the automated judge agrees with you","Complete validate_judge, then inspect the failure-tag instructions. The eight-request routing sample shows the fixed model making typed routing decisions; it is too small to rank it against the full classifiers.","Run the judge on your reviewed cases. Read one false alarm or missed failure, and revise the rubric if needed. A valid JSON response can still be wrong.")),judge_editor,check_judge,judge_rubric,run_prompted,run_judge,retry_judge_publication,ui.publication(mo,_s,names=("banking-routing-judge-alignment",)) if _s else mo.md(""),mo.accordion({"Worked answer":mo.md("```python\\n"+teaching.VALIDATOR_SOLUTION+"\\n```")})]) if get_step()=="judge" else mo.md("")
''',True)
add('''
mo.stop(not check_judge.value)
try:
    show_result("judge validator",teaching.check_validator(judge_editor.value))
except Exception as _error:
    show_result("judge validator",{"status":"needs work","message":str(_error)})
''',True)
add('''
mo.stop(not retry_judge_publication.value)
show_result("judge publication",publish_routing_results(get_context()["session"],include_final=False))
refresh()
''')
add('''
mo.stop(not run_prompted.value)
_s=get_context()["session"]
_data=get_data()
_intents=sorted({r["label"] for r in _data["rows"] if r["split"]=="train"})
_rows=sorted(teaching.saved(_s,"routing/baseline/embedding")["result"]["validation"],key=lambda r:r["case_id"])[:8]
_results=[]
for _row in _rows:
    with _s.stage("routing/judge/prompted/"+_row["case_id"],config={"case_id":_row["case_id"]}) as _stage:
        if _stage.needs_run:
            _value,_request=validated_json(_s,_stage.id,routing.route_messages(_row["text"],_intents),lambda value:routing.validate_route(value,_intents),max_tokens=512)
            _stage.record({"case_id":_row["case_id"],"request":_row["text"],"output":_value,"reference":_row["target"]})
    _results.append(_stage.result)
    show_result("prompted trace",trace_saved(_stage))
show_result("prompted routes",_results)
_s.checkpoint("routing-sample")
refresh()
''')
add('''
mo.stop(not run_judge.value)
teaching.check_validator(judge_editor.value)
_s=get_context()["session"]
_dataset=routing.checksum(get_data()["root"]/"manifest.json")
_reviews=reviewed_dataset(_s,_dataset)["rows"][:8]
_validator=teaching.functions(judge_editor.value)["validate_judge"]
if not _reviews:raise ValueError("Save a human review before comparing the judge.")
_predictions={}
_human=[]
_attempts=[]
for _review in _reviews:
    _human.append({"case_id":_review["case_id"],"failed":_review["proposed_label"]!=_review["accepted_label"]})
    _stage=_s.stage("routing/judge/alignment/"+_review["case_id"],config={"review":_review["id"]},sources={"validator.py":judge_editor.value,"rubric.txt":judge_rubric.value})
    try:
        with _stage:
            if _stage.needs_run:
                _messages=[{"role":"system","content":judge_rubric.value},{"role":"user","content":json.dumps({"request":_review["evidence"]["text"],"proposed_intent":_review["proposed_label"],"needs_review":False})}]
                _value,_request=validated_json(_s,_stage.id,_messages,_validator,max_tokens=512)
                _stage.record({"case_id":_review["case_id"],"judgment":_value})
        _predictions[_review["case_id"]]=_stage.result["judgment"]
        _attempts.append({"case_id":_review["case_id"],"stage_id":_stage.id,"status":"available"})
        show_result("judge trace",trace_saved(_stage))
    except Exception as _error:
        _predictions[_review["case_id"]]=None
        _attempts.append({"case_id":_review["case_id"],"stage_id":_stage.id,"status":"unavailable","error":str(_error)})
_summary={"human_reviews":_human,"predictions":_predictions,"attempts":_attempts,"metrics":routing.judge_alignment(_human,_predictions)}
with _s.stage("routing/judge/summary",config={"reviews":[r["id"] for r in _reviews],"attempts":_attempts},sources={"validator.py":judge_editor.value,"rubric.txt":judge_rubric.value}) as _summary_stage:
    if _summary_stage.needs_run:_summary_stage.record(_summary)
show_result("judge agreement",_summary_stage.result)
if _summary["metrics"]["unavailable"]:
    show_result("Missing judgments",{"message":"The comparison attempt is saved. Missing judgments are not failures of your router and count toward no agreement score. You can continue, or repair access and explicitly retry the failed judge steps."})
_s.checkpoint("judge")
show_result("judge publication",publish_routing_results(_s,include_final=False))
refresh()
''')
add('''
_s=get_context().get("session")
_revision=get_revision()
retrain=mo.ui.run_button(label="Train a classifier with my reviewed examples",disabled=not bool(_s and teaching.saved(_s,"routing/review")))
mo.vstack([mo.Html(ui.step("Add reviewed examples to the training dataset","The classifier will use your accepted labels, including a label that differs from the published annotation. Inspect disagreements before training. This is a new experiment; extra labels do not guarantee a higher score.","Compare validation results and choose which version to freeze.")),retrain]) if get_step()=="improve" else mo.md("")
''',True)
add('''
mo.stop(not retrain.value)
_s=get_context()["session"]
_data=get_data()
_reviewed=reviewed_dataset(_s,routing.checksum(_data["root"]/"manifest.json"))
if not _reviewed["rows"]:raise ValueError("Save at least one reviewed label first.")
teaching.check_classifier(classifier_editor.value)
with _s.stage("routing/improve",config={"reviewed_dataset":_reviewed["version"]},sources={"classifier.py":classifier_editor.value}) as _stage:
    if _stage.needs_run:
        _started=time.time()
        _fitted=routing.fit_classifier(_data,"embedding",reviewed=_reviewed["rows"],factory=teaching.functions(classifier_editor.value)["make_classifier"])
        _rows=routing.predict(_fitted,_data,"validation",threshold=review_threshold.value)
        _path=_stage.output_dir/"classifier.joblib"
        joblib.dump(_fitted,_path)
        _event={"id":_stage.id+"/train","name":"train_with_reviewed_labels","arguments":{"reviewed_dataset":_reviewed["version"],"added_labels":len(_reviewed["rows"])},"result":routing.score(_rows),"started_at":_started,"ended_at":time.time(),"status":"complete"}
        _stage.record({"model_file":str(_path.relative_to(_s.root)),"model_sha256":routing.checksum(_path),"validation":_rows,"metrics":routing.score(_rows),"events":[_event]},files=[_path])
show_result("revised classifier",{"validation":_stage.result["metrics"],"trace":trace_saved(_stage)})
_s.checkpoint("improve")
refresh()
''')
add('''
_s=get_context().get("session")
_revision=get_revision()
freeze_choice=mo.ui.dropdown({"Classifier on frozen MiniLM features":"embedding","Classifier with my reviews":"reviewed"},value="Classifier on frozen MiniLM features",label="Selected version")
freeze_reason=mo.ui.text_area(label="Why choose this version? Cite a validation case or metric.",full_width=True)
_freeze_blocked=teaching.freeze_prerequisite(_s)
freeze=mo.ui.run_button(label="Freeze the classifier and review threshold",disabled=bool(_freeze_blocked))
final_run=mo.ui.run_button(label="Evaluate the frozen versions on all 3,080 test requests",disabled=not bool(_s and teaching.saved(_s,"routing/freeze")))
publish_final_comparison=mo.ui.run_button(label="Publish or retry my saved test comparison",disabled=not bool(_s and teaching.saved(_s,"routing/final/selected")))
mo.vstack([mo.Html(ui.step("Evaluate requests you have not used for editing","Select your model using validation evidence. Freeze its files and the review threshold, then evaluate the official test set once. The final comparison includes both baselines and your chosen version.","Inspect per-intent errors, coverage, latency, and cost. Save a report that explains one improvement and one remaining mistake.")),freeze_choice,freeze_reason,mo.callout(mo.md(_freeze_blocked),kind="warn") if _freeze_blocked else mo.md("Judge comparison attempt saved. Unavailable judgments remain missing."),freeze,final_run,publish_final_comparison,ui.publication(mo,_s,names=("banking-routing-final",)) if _s else mo.md("")]) if get_step()=="final" else mo.md("")
''',True)
add('''
mo.stop(not freeze.value)
_s=get_context()["session"]
if teaching.freeze_prerequisite(_s):raise ValueError(teaching.freeze_prerequisite(_s))
if not freeze_reason.value.strip():raise ValueError("Explain your selection before final evaluation.")
if teaching.saved(_s,"routing/final/selected"):raise ValueError("This workspace has already used the final test set. Keep its frozen selection; start a separately labeled teaching retest for another choice.")
_selected=teaching.saved(_s,"routing/improve" if freeze_choice.value=="reviewed" else "routing/baseline/embedding")
if not _selected:raise ValueError("Train the selected version before freezing it.")
teaching.check_policy(policy_editor.value)
with _s.stage("routing/freeze",config={"selected_stage":_selected["id"],"threshold":review_threshold.value},sources={"review-policy.py":policy_editor.value}) as _stage:
    if _stage.needs_run:_stage.record({"selected_stage":_selected["id"],"threshold":review_threshold.value,"reason":freeze_reason.value,"model_sha256":_selected["result"]["model_sha256"],"policy_source":policy_editor.value})
_s.checkpoint("final")
refresh()
''')
add('''
mo.stop(not final_run.value)
_s=get_context()["session"]
_frozen=teaching.saved(_s,"routing/freeze")
_data=get_data()
_models={"tfidf":teaching.saved(_s,"routing/baseline/tfidf"),"embedding":teaching.saved(_s,"routing/baseline/embedding"),"selected":_s.read()["stages"][_frozen["result"]["selected_stage"]]}
_policy=teaching.functions(_frozen["result"]["policy_source"])["needs_review"]
for _label,_record in _models.items():
    with _s.stage("routing/final/"+_label,config={"freeze":_frozen["id"],"model_sha256":_record["result"]["model_sha256"]}) as _stage:
        if _stage.needs_run:
            _fitted=load_fitted(_record)
            _rows=routing.predict(_fitted,_data,"test",threshold=_frozen["result"]["threshold"])
            _rows=[{**row,"abstained":bool(_policy(row["confidence"],_frozen["result"]["threshold"]))} for row in _rows]
            _stage.record({"predictions":_rows,"metrics":routing.score(_rows),"per_intent":routing.per_intent(_rows),"model_stage":_record["id"]})
_s.checkpoint("final")
show_result("final publication",publish_routing_results(_s,include_judge=False))
refresh()
''')
add('''
mo.stop(not publish_final_comparison.value)
show_result("final publication",publish_routing_results(get_context()["session"],include_judge=False))
refresh()
''')
add('''
_s=get_context().get("session")
_revision=get_revision()
_final={label:teaching.saved(_s,"routing/final/"+label) for label in ("tfidf","embedding","selected")} if _s else {}
_versions={label:row["result"]["predictions"] for label,row in _final.items() if row}
final_picker=mo.ui.dropdown({r["text"]:r["case_id"] for r in list(_versions.values())[0]} if _versions else {},label="Compare this test request",full_width=True)
mo.vstack([mo.ui.table(teaching.metrics_table(_versions),selection=None),final_picker]) if get_step()=="final" and _versions else mo.md("")
''',True)
add('''
mo.stop(get_step()!="final" or not final_picker.value)
_s=get_context()["session"]
_comparison=[]
for _label in ("tfidf","embedding","selected"):
    _record=teaching.saved(_s,"routing/final/"+_label)
    if _record:_comparison.extend([{"version":_label,**r} for r in _record["result"]["predictions"] if r["case_id"]==final_picker.value])
mo.vstack([mo.Html(ui.result("This customer request",{"Request":_comparison[0]["text"],"Case":final_picker.value})),mo.ui.table([{"Version":r["version"],"Predicted intent":r["prediction"],"Reference intent":r["target"],"Confidence":round(r["confidence"],3),"Needs review":r["abstained"]} for r in _comparison],selection=None)])
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
_release_records={name:teaching.saved(_s,"routing/release/"+name) for name in ("prepare","reproduce","incident","repair","decision","rollback")} if _s else {}
_release_ready=bool(_s and teaching.saved(_s,"routing/final/selected"))
_phase=next((name for name in ("prepare","reproduce","incident","repair","decision","rollback") if not _release_records.get(name)),"complete")
if _release_records.get("decision") and _release_records["decision"]["result"]["release"]["decision"]=="reject":_phase="complete"
release_prepare=mo.ui.run_button(label="Prepare the selected router for release",disabled=not _release_ready)
release_reload=mo.ui.run_button(label="Publish and reload the exact release artifact",disabled=not bool(_release_records.get("prepare")))
release_incident=mo.ui.run_button(label="Run the deliberately faulty release",disabled=not bool(_release_records.get("reproduce")))
release_check=mo.ui.run_button(label="Check my release and repair code")
release_repair=mo.ui.run_button(label="Run my repaired loader on the same requests",disabled=not bool(_release_records.get("incident")))
release_loader_editor=mo.ui.code_editor(value=_s.get_draft("routing/release-loader",release_lab.LOADER_STARTER) if _s else release_lab.LOADER_STARTER,language="python",on_change=lambda value:_s.save_draft("routing/release-loader",value) if _s else None,debounce=False)
release_check_editor=mo.ui.code_editor(value=_s.get_draft("routing/release-check",release_lab.CHECK_STARTER) if _s else release_lab.CHECK_STARTER,language="python",on_change=lambda value:_s.save_draft("routing/release-check",value) if _s else None,debounce=False)
release_choice=mo.ui.radio({"Release the tested repair":"release","Reject the repair and keep the previous release":"reject"},value="Release the tested repair",label="Release decision")
release_reason=mo.ui.text_area(value=_s.get_draft("routing/release-reason","") if _s else "",label="Which checks support this decision?",full_width=True,on_change=lambda value:_s.save_draft("routing/release-reason",value) if _s else None)
release_decide=mo.ui.run_button(label="Save my release decision",disabled=not bool(_release_records.get("repair")))
release_rollback=mo.ui.run_button(label="Restore the previous release and verify its predictions",disabled=not bool(_release_records.get("decision")))
release_retry=mo.ui.run_button(label="Retry release publication only",disabled=not bool(_release_records.get("prepare")))
_phase_ui={
    "prepare":mo.vstack([mo.md("**1. Package the selected router.** Save its classifier, preprocessing identity, label order, review policy, and source. Freeze one review-pool request per intent before computing any release predictions."),release_prepare]),
    "reproduce":mo.vstack([mo.md("**2. Reload the published version.** Upload the saved package, download its exact `:vN` version, and predict the fixed request batch. This uses cached features and CPU classifier inference. It makes no model API calls."),release_reload]),
    "incident":mo.vstack([mo.md("**3. Run a controlled incident.** The faulty loader rotates the intent names while leaving the probabilities unchanged. This defect is deliberately introduced for the drill. Open its Agent Lens tool result and compare one destination with the healthy version."),mo.md("```python\\n"+release_lab.FAULTY_LOADER+"\\n```"),release_incident]),
    "repair":mo.vstack([mo.md("**4. Write the check and repair.** Compare one request below and save your reviewed regression case. Complete `check_release` so names in the wrong order fail. Complete `label_names` to preserve the classifier's probability-column order. Your functions are saved in the actual repaired package and used by the batch below."),release_check_editor,release_loader_editor,release_check,release_repair,mo.accordion({"Hint":mo.md("Compare sets to check membership, and lists to check order. Do not sort the model's class list."),"Worked answer":mo.md("```python\\n"+release_lab.CHECK_SOLUTION+"\\n"+release_lab.LOADER_SOLUTION+"\\n```")})]),
    "decision":mo.vstack([mo.md("**5. Decide whether to release.** Read the checks and matching requests below. The repair should reproduce the healthy classifier, including its remaining mistakes. Saving this decision uploads the saved repaired package; it does not run it again."),release_choice,release_reason,release_decide]),
    "rollback":mo.vstack([mo.md("**6. Practice rollback.** Download the previous exact artifact and compare its outputs with the healthy batch. A saved pointer alone is not a verified rollback."),release_rollback]),
    "complete":mo.md("**Release drill saved.** Explain the defect, your repair, and the rollback result in the conclusion. The official test comparison above is unchanged.")}
mo.vstack([mo.Html(ui.heading("The classifier passed. The release did not.","Your support team has selected a router. Now check that the released files preserve the same decisions. This is a controlled release drill, not a new claim about model quality.",theme="routing")),mo.md("**Regression set:** one lexical-first review-pool request per intent. Some may have been used for review or retraining. These are reproduction checks, not independent test results."),_phase_ui[_phase] if _release_ready else mo.callout(mo.md("Complete the final classifier comparison first. [Go to the final comparison](#final)."),kind="warn"),mo.accordion({"Publication failed?":mo.vstack([mo.md("Saved executions remain available. Retry uploads here, then use the current step's button. Completed batches are reused."),release_retry]),"Optional Registry and ARIA":mo.md("The required release is this notebook's batch predictor. If you have Registry access, link the exact artifact version after the checks pass. Registry does not deploy it. Where ARIA is enabled, ask it to investigate the saved incident; verify its cited request before accepting a suggestion.")})]) if get_step()=="release" else mo.md("")
''',True,cell_id="routing.release.controls")
add('''
mo.stop(not release_prepare.value)
_s=get_context()["session"]
_record=release_lab.prepare(_s,get_data())
show_result("release package",{"Cases":_record["result"]["case_count"],"Files":list(_record["result"]["metadata"]["files"]),"Next":"Publish and reload the exact release artifact."})
_s.checkpoint("release")
refresh()
''',True,cell_id="routing.release.prepare")
add('''
mo.stop(not release_reload.value)
_s=get_context()["session"]
_record=release_lab.reproduce_selected(_s,get_data())
show_result("reloaded release",{"Artifact":_record["result"]["artifact"],**_record["result"]["metrics"]})
show_result("release trace",trace_saved(_record))
_s.checkpoint("release")
refresh()
''',True,cell_id="routing.release.reproduce")
add('''
mo.stop(not release_incident.value)
_s=get_context()["session"]
_record=release_lab.run_variant(_s,get_data(),variant="incident")
show_result("controlled release incident",{"Checks":_record["result"]["checks"],"Meaning":"The names still match, but their order does not. Confidence alone does not reveal this defect."})
show_result("incident trace",trace_saved(_record))
_s.checkpoint("release")
refresh()
''',True,cell_id="routing.release.incident")
add('''
mo.stop(not release_check.value)
try:show_result("release code check",release_lab.check_exercises(release_loader_editor.value,release_check_editor.value))
except Exception as _error:show_result("release code check",{"status":"needs work","message":str(_error)})
''',True,cell_id="routing.release.check")
add('''
mo.stop(not release_repair.value)
_s=get_context()["session"]
_record=release_lab.run_variant(_s,get_data(),variant="repair",loader_source=release_loader_editor.value,check_source=release_check_editor.value)
show_result("repair checks",_record["result"]["checks"])
show_result("repair trace",trace_saved(_record))
_s.checkpoint("release")
show_result("release comparison",publish_routing_results(_s,include_judge=False,include_final=False))
refresh()
''',True,cell_id="routing.release.repair")
add('''
mo.stop(not release_decide.value)
_s=get_context()["session"]
_record=release_lab.decide(_s,decision=release_choice.value,reason=release_reason.value)
show_result("release decision",_record)
_s.checkpoint("release")
refresh()
''',True,cell_id="routing.release.decision")
add('''
mo.stop(not release_rollback.value)
_s=get_context()["session"]
_record=release_lab.rollback(_s,get_data())
show_result("rollback",_record["result"]["release"])
show_result("rollback trace",trace_saved(_record))
_s.checkpoint("release")
show_result("release comparison",publish_routing_results(_s,include_judge=False,include_final=False))
refresh()
''',True,cell_id="routing.release.rollback")
add('''
mo.stop(not release_retry.value)
_s=get_context()["session"]
_status={}
for _name in ("prepare","incident","repair"):
    _record=teaching.saved(_s,"routing/release/"+_name)
    if _record:
        try:_status[_name]=release_lab.publish_bundle(_s,_record)
        except Exception as _error:_status[_name]={"status":"publication pending","error":str(_error)}
for _record in release_lab.comparisons(_s).values():
    _status["trace/"+_record["id"]]=trace_saved(_record)
show_result("release artifact publication",_status)
show_result("release comparison",publish_routing_results(_s,include_judge=False,include_final=False))
refresh()
''',True,cell_id="routing.release.retry")
add('''
_s=get_context().get("session")
_revision=get_revision()
_release_versions=release_lab.comparisons(_s) if _s else {}
_release_rows={label:record["result"]["predictions"] for label,record in _release_versions.items()}
_release_cases=list(_release_rows.values())[0] if _release_rows else []
release_case=mo.ui.dropdown({r["text"]:r["case_id"] for r in _release_cases},value=_release_cases[0]["text"] if _release_cases else None,label="Follow one request across releases",full_width=True)
mo.vstack([mo.ui.table(teaching.metrics_table(_release_rows),selection=None),release_case]) if get_step()=="release" and _release_rows else mo.md("")
''',True,cell_id="routing.release.compare")
add('''
mo.stop(get_step()!="release" or not release_case.value)
_s=get_context()["session"]
_versions=release_lab.comparisons(_s)
_rows=[{"Version":label,"Destination":row["prediction"],"Reference":row["target"],"Confidence":round(row["confidence"],3),"Needs review":row["abstained"]} for label,record in _versions.items() for row in record["result"]["predictions"] if row["case_id"]==release_case.value]
_faulty=next((row for row in _versions.get("faulty",{}).get("result",{}).get("predictions",[]) if row["case_id"]==release_case.value),None)
release_accept_label=mo.ui.dropdown({name:name for name in sorted({r["target"] for r in _versions["healthy"]["result"]["predictions"]})},label="Your reviewed intent",full_width=True)
release_review_reason=mo.ui.text_area(value=_s.get_draft("routing/release-review-reason","") if _s else "",label="Why should this request go to that workflow?",full_width=True,on_change=lambda value:_s.save_draft("routing/release-review-reason",value))
release_save_case=mo.ui.run_button(label="Save this reviewed regression case",disabled=not bool(_faulty))
mo.vstack([mo.ui.table(_rows,selection=None),mo.md("Choose the intended support workflow after reading the request. Saving this case records your review; it does not retrain the frozen classifier."),release_accept_label,release_review_reason,release_save_case])
''',True,cell_id="routing.release.review.controls")
add('''
mo.stop(not release_save_case.value)
if not release_accept_label.value:raise ValueError("Choose an intent after reviewing the request.")
if not release_review_reason.value.strip():raise ValueError("Explain why this request belongs in that workflow.")
_s=get_context()["session"]
_incident=teaching.saved(_s,"routing/release/incident")
_row=next(row for row in _incident["result"]["predictions"] if row["case_id"]==release_case.value)
_review=save_review(_s,case_id=_row["case_id"],proposed_label=_row["prediction"],accepted_label=release_accept_label.value,reviewer=_s.workspace_id,dataset_version="routing-release-regression/"+_incident["result"]["metadata"]["dataset"],evidence={"text":_row["text"],"controlled_drill":True,"incident_stage":_incident["id"],"reason":release_review_reason.value})
with _s.stage("routing/release/regression",config={"review":_review["id"]}) as _stage:
    if _stage.needs_run:_stage.record({"review":_review,"expected_behavior":"Preserve the classifier probability-column mapping. Human acceptance does not change the frozen model."})
_s.checkpoint("release")
show_result("saved regression case",{"Request":_row["text"],"Accepted intent":release_accept_label.value,"Review":_review["id"]})
refresh()
''',True,cell_id="routing.release.review")

add('''
_s=get_context().get("session")
_revision=get_revision()
conclusion=mo.ui.text_area(value=_s.get_draft("routing/conclusion","") if _s else "",label="What changed, what improved, and what should a person still review?",full_width=True,on_change=lambda value:_s.save_draft("routing/conclusion",value) if _s else None)
publish=mo.ui.run_button(label="Publish my conclusion with the saved comparisons",disabled=not bool(_s and teaching.saved(_s,"routing/final/selected")))
retry_exports=mo.ui.run_button(label="Retry saved traces and comparison uploads",disabled=not bool(_s))
mo.vstack([mo.Html(ui.step("Explain what you would put into the support queue","Write down the measured change and one mistake you would send to a person. Publish the selected classifier with its preprocessing, reviewed dataset, and matching evaluation.","Open one EvalTables row and the corresponding Agent Lens request. If native publication is unavailable, use the saved notebook comparison and retry publication later.")),conclusion,publish,retry_exports,mo.md("Optional: ask ARIA to inspect the published runs and suggest a regression case. Verify its cited example before accepting the suggestion.")]) if get_step()=="report" else mo.md("")
''',True)
add('''
mo.stop(not retry_exports.value)
_s=get_context()["session"]
_status=[]
for _record in _s.read()["stages"].values():
    if _record["status"]=="complete" and (_record.get("result",{}).get("events") or _record["name"].startswith("routing/judge/")):
        try:
            _receipt=export_trace(_s,**saved_trace_inputs(_s,_record),tool_writer=instrument_tool)
            _status.append({"stage":_record["name"],"status":"published","url":_receipt["url"]})
        except Exception as _error:_status.append({"stage":_record["name"],"status":"unavailable","error":str(_error)})
show_result("trace publication",_status)
show_result("comparison publication",publish_routing_results(_s))
refresh()
''',True)
add('''
mo.stop(not publish.value)
_s=get_context()["session"]
if not conclusion.value.strip():raise ValueError("Write your conclusion before publishing the report.")
_result=publish_routing_results(_s)
_links=release_lab.evidence_links(_s)
for _key,_receipt in _s.read()["publications"].items():
    if _key.startswith("comparison/"):
        _links.update(ui.comparison_links(_receipt,suffix=_key.rsplit("/",1)[-1][:6]))
_report=publish_report(_s,conclusion.value+release_lab.report_text(_s),_links)
with _s.stage("routing/report",config={"conclusion":conclusion.value,"release_summary":release_lab.report_text(_s)}) as _stage:
    if _stage.needs_run:_stage.record({"comparison":_result,"report":_report})
_s.checkpoint("report")
show_result("publication",{"comparison":_result,"report":_report})
refresh()
''')
add('''
mo.stop(get_step()!="report")
_s=get_context().get("session")
_revision=get_revision()
_record=teaching.saved(_s,"routing/report") if _s else None
_report=_record["result"]["report"] if _record else None
mo.vstack([ui.publication(mo,_s),mo.Html(ui.links({"Open my Report":_report})) if isinstance(_report,str) else mo.md("")]) if _s else mo.md("")
''',True)
add('''
_outputs=get_output()
_current=get_step()
mo.accordion({name:mo.ui.table(value,selection=None) if isinstance(value,list) and value else mo.Html(ui.result(name,value if isinstance(value,dict) else {"result":value})) for name,value in _outputs.items()}) if _outputs else mo.md("")
''',True)
add('''
_s=get_context().get("session")
_revision=get_revision()
_records=[r for r in _s.read()["stages"].values() if r["status"]=="complete" and (r["name"].startswith("routing/"+get_step()) or get_step()=="report")] if _s else []
routing_next=ui.next_step(mo,"Next: "+teaching.STEPS[min([s[0] for s in teaching.STEPS].index(get_step())+1,len(teaching.STEPS)-1)][1],teaching.STEPS[min([s[0] for s in teaching.STEPS].index(get_step())+1,len(teaching.STEPS)-1)][0],go_to)
mo.vstack([ui.evidence(mo,_s,stage_ids=[r["id"] for r in _records],question="Open one operation. Match its case ID, returned intent, and executed source to the result in this notebook.") if _s and _records else mo.md(""),routing_next])
''',True)
