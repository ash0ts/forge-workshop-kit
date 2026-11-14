# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "forge-workshop-kit[routing] @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.5.0/forge_workshop_kit-0.5.0-py3-none-any.whl",
#   "abnf==2.2.0",
#   "annotated-types==0.8.0",
#   "anyio==4.16.0",
#   "attrs==26.1.0",
#   "cachetools==8.0.0",
#   "certifi==2026.10.23",
#   "cffi==2.1.1 ; (implementation_name == 'pypy' and sys_platform != 'emscripten') or platform_python_implementation != 'PyPy'",
#   "chardet==7.7.0",
#   "charset-normalizer==3.5.2",
#   "cint==1.0.0",
#   "click==8.5.1",
#   "cloudpickle==3.1.2",
#   "contourpy==1.3.3 ; python_full_version < '3.12'",
#   "contourpy==1.4.0 ; python_full_version >= '3.12'",
#   "coreweave==0.1.0b0",
#   "cryptography==50.0.2",
#   "cwevals==0.0.1b1",
#   "cycler==0.12.1",
#   "diskcache-weave==5.6.3.post1",
#   "distro==1.9.0",
#   "docutils==0.23",
#   "fickling==0.1.13",
#   "filelock==3.32.7",
#   "fonttools==4.68.0",
#   "googleapis-common-protos==1.76.0",
#   "gql==4.4.0",
#   "graphql-core==3.3.2",
#   "graphviz==0.21",
#   "h11==0.16.0",
#   "httpcore==1.0.9",
#   "httpx==0.28.1",
#   "idna==3.20",
#   "intervaltree==3.2.1",
#   "itsdangerous==2.2.0",
#   "jedi==0.20.1",
#   "jinja2==3.1.6",
#   "joblib==1.6.0",
#   "jsonschema==4.26.0",
#   "jsonschema-specifications==2025.9.1",
#   "kaitaistruct==0.11",
#   "kiwisolver==1.5.1",
#   "loro==1.17.1 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "marimo==0.25.2",
#   "markdown==3.11.3",
#   "markupsafe==3.0.4",
#   "matplotlib==3.11.2",
#   "msgspec==0.22.0",
#   "multidict==7.2.1",
#   "narwhals==2.28.0",
#   "networkx==3.6.1 ; python_full_version < '3.12'",
#   "networkx==3.7 ; python_full_version >= '3.12'",
#   "numpy==2.4.6 ; python_full_version < '3.12'",
#   "numpy==2.5.4 ; python_full_version >= '3.12'",
#   "opentelemetry-api==1.45.2",
#   "opentelemetry-exporter-http-transport==0.66b2",
#   "opentelemetry-exporter-otlp-common==0.66b2",
#   "opentelemetry-exporter-otlp-proto-common==1.45.2",
#   "opentelemetry-exporter-otlp-proto-http==1.45.2",
#   "opentelemetry-proto==1.45.2",
#   "opentelemetry-sdk==1.45.2",
#   "opentelemetry-semantic-conventions==0.66b2",
#   "packaging==26.3",
#   "parso==0.8.7",
#   "pdfminer-six==20260107",
#   "pillow==12.3.0",
#   "platformdirs==4.14.5",
#   "polyfile-weave==0.5.9",
#   "propcache==0.5.4",
#   "protobuf==6.33.6",
#   "psutil==7.2.2 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "pycparser==3.12 ; (implementation_name != 'PyPy' and platform_python_implementation != 'PyPy') or (implementation_name == 'pypy' and platform_python_implementation == 'PyPy' and sys_platform != 'emscripten')",
#   "pydantic==2.14.3",
#   "pydantic-core==2.50.4",
#   "pygments==2.21.0",
#   "pymdown-extensions==11.0.2",
#   "pyparsing==3.3.3",
#   "pyreadline3==3.5.6 ; sys_platform == 'win32'",
#   "python-dateutil==4.0.0",
#   "python-multipart==0.0.33",
#   "pyyaml==6.0.3",
#   "pyzmq==27.3.0 ; sys_platform != 'emscripten'",
#   "referencing==0.37.0",
#   "requests==2.34.2",
#   "rpds-py==2026.9.1",
#   "scikit-learn==1.9.1",
#   "scipy==1.17.1 ; python_full_version < '3.12'",
#   "scipy==1.18.1 ; python_full_version >= '3.12'",
#   "sentry-sdk==2.75.0",
#   "sniffio==1.3.1",
#   "sortedcontainers==2.4.0",
#   "starlette==1.10.0 ; sys_platform != 'emscripten'",
#   "tenacity==9.2.1",
#   "threadpoolctl==3.8.0",
#   "tomlkit==0.15.2",
#   "typing-extensions==4.16.0",
#   "typing-inspection==0.4.5",
#   "tzdata==2026.6",
#   "urllib3==2.8.0",
#   "uvicorn==0.54.0 ; sys_platform != 'emscripten'",
#   "wandb==0.31.0",
#   "wandb-workspaces==0.4.13",
#   "weave==0.54.0",
#   "websockets==17.4 ; sys_platform != 'emscripten'",
#   "xxhash==4.1.0",
#   "yarl==1.25.1",
# ]
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Route customer requests')


@app.cell(hide_code=True)
def _():
    import json
    import time
    from pathlib import Path
    import joblib
    import marimo as mo
    from forge_workshop_kit import WorkshopSession, setup, ui, routing, routing_teaching as teaching
    from forge_workshop_kit.review import save_review, reviewed_dataset
    from forge_workshop_kit.provider import validated_json, Provider
    from forge_workshop_kit.session import digest
    from forge_workshop_kit.traces import event, export_trace, saved_trace_inputs
    from forge_workshop_kit.publication import publish_comparison, publish_report
    get_context, set_context = mo.state({})
    get_step, set_step = mo.state("setup", allow_self_loops=True)
    get_output, set_output = mo.state({})
    get_revision, set_revision = mo.state(0)
    return (Path, Provider, WorkshopSession, digest, event, export_trace, get_context, get_output, get_revision, get_step, joblib, json, mo, publish_comparison, publish_report, reviewed_dataset, routing, save_review, saved_trace_inputs, set_context, set_output, set_revision, set_step, setup, teaching, time, ui, validated_json,)


@app.cell(hide_code=True)
def _(export_trace, get_context, get_revision, instrument_tool, joblib, routing, saved_trace_inputs, set_output, set_revision, set_step):
    def go_to(step):
        session=get_context().get("session")
        if session: session.set_view(step)
        set_step(step)
    def refresh():
        set_revision(get_revision()+1)
    def show_result(name,result):
        set_output(lambda old:{**old,name:result})
    def trace_saved(stage):
        session=get_context()["session"]
        try:
            receipt=export_trace(session, **saved_trace_inputs(session,stage.id), tool_writer=instrument_tool)
            return {"status":"published","url":receipt["url"]}
        except Exception as error:
            return {"status":"publication pending","error":str(error),"next":"Retry saved publications; do not rerun training."}
    def load_fitted(record):
        session=get_context()["session"]
        path=session.file(record["result"]["model_file"])
        if routing.checksum(path)!=record["result"]["model_sha256"]:
            raise ValueError("Saved classifier checksum differs. Restore its checkpoint before using it.")
        return joblib.load(path)
    return (go_to, load_fitted, refresh, show_result, trace_saved,)


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, go_to, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    routing_navigation=ui.navigation(mo,teaching.STEPS,get_step(),go_to,completed=teaching.completed_steps(_s),label="Workshop steps")
    mo.vstack([mo.Html(ui.STYLE),routing_navigation,mo.Html(ui.context(_s)) if _s else mo.md("Copy this notebook to your own Forge project. Opening it does not send model requests or train a classifier.")])
    return (routing_navigation,)


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, set_revision, setup):
    _s = get_context().get("session")
    _revision = get_revision()
    _view = get_step()
    routing_recovery_refresh = mo.ui.button(label="Check for stopped or failed work", on_click=lambda _: set_revision(get_revision() + 1), disabled=not bool(_s))
    _options = _s.recovery_options() if _s else []
    _choices = {setup.recovery_label(_s.workshop, row) + " · " + row["id"][:6]: row["id"] for row in _options}
    routing_recovery_choice = mo.ui.dropdown(_choices, value=next(iter(_choices), None), label="Execution to review", full_width=True) if _choices else mo.ui.dropdown({"No failed executions": ""}, value="No failed executions", disabled=True)
    mo.vstack([mo.md("**A run stopped?** Check its saved status here. Reviewing it never starts work."), routing_recovery_refresh, routing_recovery_choice]) if _options else mo.accordion({"A run stopped? Review recovery": mo.vstack([mo.md("Click below to read saved execution status. Completed results stay saved. An upload failure uses Retry publication in the final comparison instead."), routing_recovery_refresh])})
    return (routing_recovery_choice, routing_recovery_refresh,)


@app.cell(hide_code=True)
def _(get_context, mo, routing_recovery_choice, ui):
    _s = get_context().get("session")
    _row = next((row for row in _s.recovery_options() if row["id"] == routing_recovery_choice.value), None) if _s else None
    _needs_confirmation = bool(_row and (_row["has_uncertain_requests"] or _row["status"] == "running"))
    routing_recovery_confirm = mo.ui.checkbox(label="I checked that the previous execution has stopped. Keep unresolved requests charged at their reserved maximum.")
    routing_recovery_allow = mo.ui.run_button(label="Allow retry of this failed execution", disabled=not bool(_row), full_width=True)
    mo.vstack([mo.Html(ui.result("Review the saved execution", {"Execution": _row["name"], "Status": _row["status"], "Issue": _row.get("error") or "The execution has not finished.", "Next": "Allow another attempt, then click the normal run button for this step. This control does not run the experiment."}, status="failed")), routing_recovery_confirm if _needs_confirmation else mo.md("The previous attempt has ended. Its result and costs remain in the record."), routing_recovery_allow]) if _row else mo.md("")
    return (routing_recovery_allow, routing_recovery_confirm,)


@app.cell(hide_code=True)
def _(get_context, mo, refresh, routing_recovery_allow, routing_recovery_choice, routing_recovery_confirm, set_output):
    mo.stop(not routing_recovery_allow.value)
    _s = get_context()["session"]
    try:
        _route = _s.retry_stage(routing_recovery_choice.value, confirm_stopped=routing_recovery_confirm.value)
        _message = "Retry allowed. Return to this step’s run button to start attempt " + str(_route["attempt"]) + ". Completed work will be reused."
    except Exception as _error:
        _message = str(_error)
    set_output(lambda current: {**current, "recovery": _message})
    refresh()
    return


@app.cell(hide_code=True)
def _(get_output, mo):
    _message = get_output().get("recovery")
    mo.callout(mo.md(_message), kind="info") if _message else mo.md("")
    return


@app.cell(hide_code=True)
def _(get_context, mo):
    help_message = mo.ui.text_area(label="What do you need help with?", full_width=True)
    help_button = mo.ui.run_button(label="Send a help request", disabled=not bool(get_context().get("session")))
    mo.accordion({"Ask the facilitator": mo.vstack([help_message, help_button, mo.md("Tell the facilitator which step you’re on and what happened. They can read this request in the workshop monitor.")])})
    return (help_button, help_message,)


@app.cell(hide_code=True)
def _(get_context, help_button, help_message, mo):
    mo.stop(not help_button.value)
    get_context()["session"].request_help(help_message.value)
    mo.md("Help request saved. Send an empty message when it is resolved.")
    return


@app.cell(hide_code=True)
def _(get_step, mo, ui):
    mo.stop(get_step()!="setup")
    mo.vstack([mo.Html(ui.heading("Route customer requests and learn from mistakes", "You're joining a fictional bank's support team. A missing card, a broken card, and an unfamiliar payment need different workflows. You'll build a router, inspect its mistakes, review labels, and test a revised classifier.", theme="routing")),mo.md("The messages come from **Banking77**, published by PolyAI's researchers. It contains 10,003 training messages and 3,080 test messages across 77 banking intents. We reserve ten training examples per intent for validation and ten for review. The official test set stays untouched until the final comparison. These are public teaching data, not your customers' records."),mo.md("We'll start with word counts weighted by how distinctive they are, then train the same classifier on frozen sentence embeddings. After that, you decide which uncertain requests need a person. The support queue is fictional. Its enthusiasm for automatically forwarding tickets is familiar."),mo.md("**Today's output:** a selected router, the reviewed examples it learned from, an evaluation on matching requests, and a trace explaining one routing or labeling decision.")])
    return


@app.cell(hide_code=True)
def _(get_step, mo, setup):
    _context=setup.project_context()
    project_input=mo.ui.text(value=_context["project"],label="Your Forge project",disabled=_context["hosted"] and _context["detected"],full_width=True)
    allowance=mo.ui.number(value=8,start=.01,stop=1000,label="Inference allowance in USD; notebook CPU is separate")
    connect=mo.ui.run_button(label="Connect and restore my work")
    mo.vstack([project_input,allowance,connect,mo.md("On a laptop, authenticate with `uv run wandb login`. Use a project you can write to. Classifier training runs on this notebook's CPU; only the explicit routing and judge buttons use billed inference.")]) if get_step()=="setup" else mo.md("")
    return (allowance, connect, project_input,)


@app.cell(hide_code=True)
def _(WorkshopSession, allowance, connect, mo, project_input, refresh, set_context, set_step, setup):
    mo.stop(not connect.value)
    _s=WorkshopSession.from_environment("banking-routing",project=project_input.value,budget_usd=allowance.value)
    _access=_s.check_access()
    _s.restore()
    setup.save_access(_s,_access)
    set_context({"session":_s})
    set_step(_s.get_view("setup"))
    refresh()
    mo.md("Connected. Send the setup trace below, then inspect the messages.")
    return


@app.cell
def _():
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
    return (instrument_tool,)


@app.cell(hide_code=True)
def _(get_context, get_step, mo):
    first_trace=mo.ui.run_button(label="Send my first Agent Lens trace",disabled=not bool(get_context().get("session")))
    mo.vstack([mo.md("Add an attribute in `instrument_tool` above. Send the trace, open its tool span, and find your attribute."),first_trace]) if get_step()=="setup" else mo.md("")
    return (first_trace,)


@app.cell(hide_code=True)
def _(event, first_trace, get_context, mo, refresh, show_result, trace_saved):
    mo.stop(not first_trace.value)
    _s=get_context()["session"]
    with _s.stage("routing/setup",config={"purpose":"check notebook tracing"}) as _stage:
        if _stage.needs_run:
            _result,_event=event("inspect_routing_environment",{},lambda:{"project":_s.project,"training":"CPU","classes":77},on_error=_stage.record_event)
            _stage.record({"events":[_event]})
    show_result("setup",trace_saved(_stage))
    _s.checkpoint("setup")
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    load_data_button=mo.ui.run_button(label="Download and check Banking77",disabled=not bool(_s))
    mo.vstack([mo.Html(ui.step("Inspect the support queue","Download the pinned public messages and cached MiniLM features. The cache avoids encoding 13,083 messages during the workshop; the preparation script records the encoder revision and every file checksum.","Read a request, choose a likely intent, then reveal its published label.")),load_data_button,mo.md("[Data source and CC-BY-4.0 license](https://github.com/PolyAI-LDN/task-specific-datasets) · [Feature preparation code](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_routing.py)")]) if get_step()=="data" else mo.md("")
    return (load_data_button,)


@app.cell(hide_code=True)
def _(get_context, load_data_button, mo, refresh, routing, set_context, teaching):
    mo.stop(not load_data_button.value)
    _s=get_context()["session"]
    _path=teaching.download(_s.root/"datasets/banking77-v1")
    _data=routing.load_data(_path)
    with _s.stage("routing/data",config={"manifest":routing.checksum(_path/"manifest.json")}) as _stage:
        if _stage.needs_run:_stage.record({"counts":_data["manifest"]["counts"],"dataset_manifest":_data["manifest"]},files=list(_path.iterdir()))
    set_context({**get_context(),"data_path":str(_path)})
    _s.checkpoint("data")
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, routing, teaching):
    def get_data():
        session=get_context()["session"]
        record=teaching.saved(session,"routing/data")
        if not record:raise ValueError("Download Banking77 in the data step first.")
        # Restore places the exact dataset files beside this completed stage.
        return routing.load_data(session.file("outputs/"+record["id"]))
    return (get_data,)


@app.cell(hide_code=True)
def _(get_context, get_data, get_revision, get_step, mo, routing, teaching):
    _s=get_context().get("session")
    _revision=get_revision()
    _ready=bool(_s and teaching.saved(_s,"routing/data"))
    _cases=routing.partition(get_data(),"validation")[0][:30] if _ready else []
    request_picker=mo.ui.dropdown({row["text"]:row["id"] for row in _cases},value=_cases[0]["text"] if _cases else None,label="Request to inspect",full_width=True)
    reveal_label=mo.ui.checkbox(label="Show the published label")
    mo.vstack([request_picker,reveal_label]) if get_step()=="data" and _ready else mo.md("")
    return (request_picker, reveal_label,)


@app.cell(hide_code=True)
def _(get_data, get_step, mo, request_picker, reveal_label, routing):
    mo.stop(get_step()!="data" or not request_picker.value)
    _row=next(row for row in routing.partition(get_data(),"validation")[0] if row["id"]==request_picker.value)
    mo.md("Published intent: **"+_row["label"]+"**") if reveal_label.value else mo.md("Explain which workflow this request needs before checking its label.")
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    classifier_editor=mo.ui.code_editor(value=_s.get_draft("routing/classifier",teaching.CLASSIFIER_STARTER) if _s else teaching.CLASSIFIER_STARTER,language="python",on_change=lambda source:_s.save_draft("routing/classifier",source) if _s else None,debounce=False)
    check_classifier=mo.ui.run_button(label="Check my classifier code")
    train_classifiers=mo.ui.run_button(label="Train both classifiers on the same messages",disabled=not bool(_s and teaching.saved(_s,"routing/data")))
    mo.vstack([mo.Html(ui.step("Train two routers","Complete make_classifier. Both models learn from the same 8,463 messages. The first uses word unigrams and bigrams; the second uses fixed 384-number sentence vectors. No encoder weights change.","Compare validation macro-F1 and review coverage. Open the run in Forge to inspect its code and settings.")),classifier_editor,check_classifier,train_classifiers,mo.accordion({"Hint":mo.md("Return a scikit-learn LogisticRegression object with C=10, max_iter=1000, random_state=17."),"Worked answer":mo.md("```python\n"+teaching.CLASSIFIER_SOLUTION+"\n```")})]) if get_step()=="baseline" else mo.md("")
    return (check_classifier, classifier_editor, train_classifiers,)


@app.cell(hide_code=True)
def _(check_classifier, classifier_editor, mo, show_result, teaching):
    mo.stop(not check_classifier.value)
    try:
        show_result("classifier check",teaching.check_classifier(classifier_editor.value))
    except Exception as _error:
        show_result("classifier check",{"status":"needs work","message":str(_error)})
    return


@app.cell
def _(classifier_editor, get_context, get_data, joblib, mo, refresh, routing, show_result, teaching, time, trace_saved, train_classifiers):
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
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching):
    _s=get_context().get("session")
    _revision=get_revision()
    _baselines={name:teaching.saved(_s,"routing/baseline/"+name) for name in ("tfidf","embedding")} if _s else {}
    mo.ui.table(teaching.metrics_table({name:row["result"]["validation"] for name,row in _baselines.items() if row}),selection=None) if get_step()=="baseline" and any(_baselines.values()) else mo.md("")
    return


@app.cell(hide_code=True)
def _(get_context, get_data, get_revision, get_step, mo, routing, teaching, ui):
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
    mo.vstack([mo.Html(ui.step("Review the uncertain requests","Complete needs_review and move the threshold. Coverage is the fraction routed automatically; accuracy among those cases leaves the deferred requests out. Review at least four examples, including a correct route and a mistake.","Save your own labels. The revised classifier can train on them; final-test cases stay out of training.")),policy_editor,check_policy,review_threshold,review_picker,accepted_label,reviewer,save_label,mo.accordion({"Worked answer":mo.md("```python\n"+teaching.POLICY_SOLUTION+"\n```")})]) if get_step()=="review" else mo.md("")
    return (accepted_label, check_policy, policy_editor, review_picker, review_threshold, reviewer, save_label,)


@app.cell(hide_code=True)
def _(check_policy, mo, policy_editor, show_result, teaching):
    mo.stop(not check_policy.value)
    try:
        show_result("review rule",teaching.check_policy(policy_editor.value))
    except Exception as _error:
        show_result("review rule",{"status":"needs work","message":str(_error)})
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, policy_editor, review_threshold, routing, teaching, ui):
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
    return


@app.cell(hide_code=True)
def _(get_context, get_step, mo, review_picker, teaching, ui):
    mo.stop(get_step()!="review" or not review_picker.value)
    _s=get_context()["session"]
    _row=next(row for row in teaching.saved(_s,"routing/baseline/embedding")["result"]["review"] if row["case_id"]==review_picker.value)
    mo.Html(ui.result("Read the request before accepting a label",{"Request":_row["text"],"Classifier choice":_row["prediction"],"Second choice":_row["runner_up"],"Confidence":round(_row["confidence"],3),"Your task":"Choose the intent you think matches and explain it to a partner. The published reference label is not supplied to the judge."}))
    return


@app.cell
def _(accepted_label, get_context, get_data, json, mo, refresh, review_picker, reviewed_dataset, reviewer, routing, save_label, save_review, show_result, teaching):
    mo.stop(not save_label.value)
    _s=get_context()["session"]
    _row=next(r for r in teaching.saved(_s,"routing/baseline/embedding")["result"]["review"] if r["case_id"]==review_picker.value)
    _dataset=routing.checksum(get_data()["root"]/"manifest.json")
    _review=save_review(_s,case_id=_row["case_id"],proposed_label=_row["prediction"],accepted_label=accepted_label.value,reviewer=reviewer.value,dataset_version=_dataset,evidence={"text":_row["text"],"confidence":_row["confidence"]})
    _regression=reviewed_dataset(_s,_dataset)
    with _s.stage("routing/review",config={"dataset":_regression["version"]}) as _stage:
        if _stage.needs_run:
            _path=_stage.output_dir/"reviewed-cases.json"
            _path.write_text(json.dumps(_regression,indent=2)+"\n")
            _stage.record(_regression,files=[_path])
    _s.checkpoint("review")
    show_result("review",{"saved":_review["case_id"],"accepted":accepted_label.value,"reviewed_cases":len(_regression["rows"])})
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    judge_editor=mo.ui.code_editor(value=_s.get_draft("routing/judge-validator",teaching.VALIDATOR_STARTER) if _s else teaching.VALIDATOR_STARTER,language="python",on_change=lambda source:_s.save_draft("routing/judge-validator",source) if _s else None,debounce=False)
    judge_rubric=mo.ui.text_area(value=_s.get_draft("routing/judge-rubric",teaching.JUDGE_RUBRIC) if _s else teaching.JUDGE_RUBRIC,label="Failure-tag instructions",full_width=True,on_change=lambda value:_s.save_draft("routing/judge-rubric",value) if _s else None)
    check_judge=mo.ui.run_button(label="Check my judge validator")
    run_prompted=mo.ui.run_button(label="Route eight development requests with the fixed model",disabled=not bool(_s and teaching.saved(_s,"routing/baseline/embedding")))
    run_judge=mo.ui.run_button(label="Compare the judge with up to eight of my reviews",disabled=not bool(_s and teaching.saved(_s,"routing/review")))
    mo.vstack([mo.Html(ui.step("Check whether the automated judge agrees with you","Complete validate_judge, then inspect the failure-tag instructions. The eight-request routing sample shows the fixed model making typed routing decisions; it is too small to rank it against the full classifiers.","Run the judge on your reviewed cases. Read one false alarm or missed failure, and revise the rubric if needed. A valid JSON response can still be wrong.")),judge_editor,check_judge,judge_rubric,run_prompted,run_judge,mo.accordion({"Worked answer":mo.md("```python\n"+teaching.VALIDATOR_SOLUTION+"\n```")})]) if get_step()=="judge" else mo.md("")
    return (check_judge, judge_editor, judge_rubric, run_judge, run_prompted,)


@app.cell(hide_code=True)
def _(check_judge, judge_editor, mo, show_result, teaching):
    mo.stop(not check_judge.value)
    try:
        show_result("judge validator",teaching.check_validator(judge_editor.value))
    except Exception as _error:
        show_result("judge validator",{"status":"needs work","message":str(_error)})
    return


@app.cell
def _(get_context, get_data, mo, refresh, routing, run_prompted, show_result, teaching, trace_saved, validated_json):
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
    return


@app.cell
def _(get_context, get_data, json, judge_editor, judge_rubric, mo, refresh, reviewed_dataset, routing, run_judge, show_result, teaching, trace_saved, validated_json):
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
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    retrain=mo.ui.run_button(label="Train a classifier with my reviewed examples",disabled=not bool(_s and teaching.saved(_s,"routing/review")))
    mo.vstack([mo.Html(ui.step("Add reviewed examples to the training dataset","The classifier will use your accepted labels, including a label that differs from the published annotation. Inspect disagreements before training. This is a new experiment; extra labels do not guarantee a higher score.","Compare validation results and choose which version to freeze.")),retrain]) if get_step()=="improve" else mo.md("")
    return (retrain,)


@app.cell
def _(classifier_editor, get_context, get_data, joblib, mo, refresh, retrain, review_threshold, reviewed_dataset, routing, show_result, teaching, time, trace_saved):
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
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    freeze_choice=mo.ui.dropdown({"Classifier on frozen MiniLM features":"embedding","Classifier with my reviews":"reviewed"},value="Classifier on frozen MiniLM features",label="Selected version")
    freeze_reason=mo.ui.text_area(label="Why choose this version? Cite a validation case or metric.",full_width=True)
    _freeze_blocked=teaching.freeze_prerequisite(_s)
    freeze=mo.ui.run_button(label="Freeze the classifier and review threshold",disabled=bool(_freeze_blocked))
    final_run=mo.ui.run_button(label="Evaluate the frozen versions on all 3,080 test requests",disabled=not bool(_s and teaching.saved(_s,"routing/freeze")))
    mo.vstack([mo.Html(ui.step("Evaluate requests you have not used for editing","Select your model using validation evidence. Freeze its files and the review threshold, then evaluate the official test set once. The final comparison includes both baselines and your chosen version.","Inspect per-intent errors, coverage, latency, and cost. Save a report that explains one improvement and one remaining mistake.")),freeze_choice,freeze_reason,mo.callout(mo.md(_freeze_blocked),kind="warn") if _freeze_blocked else mo.md("Judge comparison attempt saved. Unavailable judgments remain missing."),freeze,final_run]) if get_step()=="final" else mo.md("")
    return (final_run, freeze, freeze_choice, freeze_reason,)


@app.cell
def _(freeze, freeze_choice, freeze_reason, get_context, mo, policy_editor, refresh, review_threshold, teaching):
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
    return


@app.cell
def _(final_run, get_context, get_data, load_fitted, mo, refresh, routing, teaching):
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
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching):
    _s=get_context().get("session")
    _revision=get_revision()
    _final={label:teaching.saved(_s,"routing/final/"+label) for label in ("tfidf","embedding","selected")} if _s else {}
    _versions={label:row["result"]["predictions"] for label,row in _final.items() if row}
    final_picker=mo.ui.dropdown({r["text"]:r["case_id"] for r in list(_versions.values())[0]} if _versions else {},label="Compare this test request",full_width=True)
    mo.vstack([mo.ui.table(teaching.metrics_table(_versions),selection=None),final_picker]) if get_step()=="final" and _versions else mo.md("")
    return (final_picker,)


@app.cell(hide_code=True)
def _(final_picker, get_context, get_step, mo, teaching, ui):
    mo.stop(get_step()!="final" or not final_picker.value)
    _s=get_context()["session"]
    _comparison=[]
    for _label in ("tfidf","embedding","selected"):
        _record=teaching.saved(_s,"routing/final/"+_label)
        if _record:_comparison.extend([{"version":_label,**r} for r in _record["result"]["predictions"] if r["case_id"]==final_picker.value])
    mo.vstack([mo.Html(ui.result("This customer request",{"Request":_comparison[0]["text"],"Case":final_picker.value})),mo.ui.table([{"Version":r["version"],"Predicted intent":r["prediction"],"Reference intent":r["target"],"Confidence":round(r["confidence"],3),"Needs review":r["abstained"]} for r in _comparison],selection=None)])
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    conclusion=mo.ui.text_area(value=_s.get_draft("routing/conclusion","") if _s else "",label="What changed, what improved, and what should a person still review?",full_width=True,on_change=lambda value:_s.save_draft("routing/conclusion",value) if _s else None)
    publish=mo.ui.run_button(label="Publish saved comparisons and my report",disabled=not bool(_s and teaching.saved(_s,"routing/final/selected")))
    retry_exports=mo.ui.run_button(label="Retry saved trace exports",disabled=not bool(_s))
    mo.vstack([mo.Html(ui.step("Explain what you would put into the support queue","Write down the measured change and one mistake you would send to a person. Publish the selected classifier with its preprocessing, reviewed dataset, and matching evaluation.","Open one EvalTables row and the corresponding Agent Lens request. If native publication is unavailable, use the saved notebook comparison and retry publication later.")),conclusion,publish,retry_exports,mo.md("Optional: ask ARIA to inspect the published runs and suggest a regression case. Verify its cited example before accepting the suggestion.")]) if get_step()=="report" else mo.md("")
    return (conclusion, publish, retry_exports,)


@app.cell(hide_code=True)
def _(export_trace, get_context, instrument_tool, mo, retry_exports, saved_trace_inputs, show_result):
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
    return


@app.cell
def _(conclusion, get_context, mo, publish, publish_comparison, publish_report, refresh, routing, show_result, teaching):
    mo.stop(not publish.value)
    _s=get_context()["session"]
    if not conclusion.value.strip():raise ValueError("Write your conclusion before publishing the report.")
    _versions={label:teaching.saved(_s,"routing/final/"+label)["result"]["predictions"] for label in ("tfidf","embedding","selected")}
    _result=publish_comparison(_s,"banking-routing-final",{label:teaching.publication_rows(rows) for label,rows in _versions.items()},summaries={label:routing.score(rows) for label,rows in _versions.items()})
    _links={label+" evaluation":record["run"] for label,record in _result.items() if record.get("run")}
    _report=publish_report(_s,conclusion.value,_links)
    with _s.stage("routing/report",config={"conclusion":conclusion.value}) as _stage:
        if _stage.needs_run:_stage.record({"comparison":_result,"report":_report})
    _s.checkpoint("report")
    show_result("publication",{"comparison":_result,"report":_report})
    refresh()
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, mo, teaching, ui):
    mo.stop(get_step()!="report")
    _s=get_context().get("session")
    _revision=get_revision()
    _record=teaching.saved(_s,"routing/report") if _s else None
    _report=_record["result"]["report"] if _record else None
    mo.vstack([ui.publication(mo,_s),mo.Html(ui.links({"Open my Report":_report})) if isinstance(_report,str) else mo.md("")]) if _s else mo.md("")
    return


@app.cell(hide_code=True)
def _(get_output, get_step, mo, ui):
    _outputs=get_output()
    _current=get_step()
    mo.accordion({name:mo.ui.table(value,selection=None) if isinstance(value,list) and value else mo.Html(ui.result(name,value if isinstance(value,dict) else {"result":value})) for name,value in _outputs.items()}) if _outputs else mo.md("")
    return


@app.cell(hide_code=True)
def _(get_context, get_revision, get_step, go_to, mo, teaching, ui):
    _s=get_context().get("session")
    _revision=get_revision()
    _records=[r for r in _s.read()["stages"].values() if r["status"]=="complete" and (r["name"].startswith("routing/"+get_step()) or get_step()=="report")] if _s else []
    routing_next=ui.next_step(mo,"Next: "+teaching.STEPS[min([s[0] for s in teaching.STEPS].index(get_step())+1,len(teaching.STEPS)-1)][1],teaching.STEPS[min([s[0] for s in teaching.STEPS].index(get_step())+1,len(teaching.STEPS)-1)][0],go_to)
    mo.vstack([ui.evidence(mo,_s,stage_ids=[r["id"] for r in _records],question="Open one operation. Match its case ID, returned intent, and executed source to the result in this notebook.") if _s and _records else mo.md(""),routing_next])
    return (routing_next,)

if __name__ == "__main__":
    app.run()
