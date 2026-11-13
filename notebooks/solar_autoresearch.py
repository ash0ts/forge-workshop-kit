# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.1.0/forge_workshop_kit-0.1.0-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Solar Autoresearch')


@app.cell(hide_code=True)
def _():
    import os
    import json
    import time
    from pathlib import Path
    import numpy as np
    import marimo as mo
    from forge_workshop_kit import WorkshopSession
    from forge_workshop_kit import solar, training, research, ui, plots
    from forge_workshop_kit.session import digest
    from forge_workshop_kit.download import dataset
    from forge_workshop_kit.publication import publish_comparison, publish_report
    from forge_workshop_kit.traces import export_trace, event, stamp
    get_lab, set_lab = mo.state({})
    get_feedback, set_feedback = mo.state({})
    return (Path, WorkshopSession, dataset, digest, event, export_trace, get_feedback, get_lab, json, mo, np, os, plots, publish_comparison, publish_report, research, set_feedback, set_lab, solar, stamp, time, training, ui,)


@app.cell(hide_code=True)
def _(mo, ui):
    mo.Html(ui.heading("Build a research loop, then give it an agent", "Start with solar measurements. Move to images. Track what you changed, then let an agent propose and test changes to your research code. Your notebook, runs and evidence belong to your project."))
    return


@app.cell(hide_code=True)
def _(mo):
    chapter = mo.ui.radio(["1 · Connect", "2 · Data and baseline", "3 · Track and search", "4 · Solar images", "5 · Research agent", "6 · Final evaluation"], value="1 · Connect", inline=True, label="Current exercise")
    chapter
    return (chapter,)


@app.cell(hide_code=True)
def _(get_lab, mo):
    help_message=mo.ui.text_area(label="What do you need help with?",full_width=True)
    help_button=mo.ui.run_button(label="Send a help request to the progress monitor",disabled=not bool(get_lab().get("session")))
    mo.accordion({"Ask the facilitator for help":mo.vstack([help_message,help_button])})
    return (help_button, help_message,)


@app.cell
def _(get_lab, help_button, help_message, mo):
    mo.stop(not help_button.value)
    get_lab()["session"].request_help(help_message.value)
    mo.md("Help request saved to your project. Clear the text and send again when resolved.")
    return


@app.cell(hide_code=True)
def _(chapter, mo, os, ui):
    mo.stop(chapter.value != "1 · Connect")
    _default = os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")]))
    project_input = mo.ui.text(value=_default, placeholder="your-name/solar-research", label="Your Forge project",full_width=True)
    allowance=mo.ui.number(value=8,start=.01,stop=1000,label="My inference allowance (USD); notebook compute is separate")
    connect_button = mo.ui.run_button(label="Connect and restore my saved work")
    mo.vstack([mo.Html(ui.step("1. Start in your own project", "Copy this notebook into a public teaching project. Hosted Forge supplies authentication. On a laptop, run wandb login and enter entity/project here.", "Your own project appears below. This check sends no model requests.")), project_input, allowance, connect_button])
    return (allowance, connect_button, project_input,)


@app.cell
def _(WorkshopSession, allowance, connect_button, get_feedback, mo, project_input, set_feedback, set_lab):
    mo.stop(not connect_button.value)
    try:
        _session=WorkshopSession.from_environment("solar-autoresearch",project=project_input.value,budget_usd=allowance.value)
        _access=_session.check_access()
        _restore=_session.restore()
        set_lab({"session":_session})
        set_feedback({**get_feedback(),"setup":{**_access,"restore":_restore}})
    except Exception as _error:
        set_feedback({**get_feedback(),"setup":{"error":str(_error),"next":"Check project write access and your account login; no training has run."}})
    return


@app.cell(hide_code=True)
def _(chapter, get_feedback, get_lab, mo):
    mo.stop(chapter.value != "1 · Connect")
    first_trace=mo.ui.run_button(label="Send my first Agent Lens trace",disabled=not bool(get_lab().get("session")))
    mo.vstack([mo.md(str(get_feedback().get("setup","Connect first."))),first_trace])
    return (first_trace,)


@app.cell
def _(stamp):
    # These scopes are your instrumentation. Their fields must match the independent event.
    def instrument_tool(observation):
        from coreweave.forge.agentlens import tracing
        from opentelemetry import trace
        with tracing.Tool(name=observation["name"], arguments=observation["arguments"],
            result=observation["result"], tool_call_id=observation["id"],
            started_at=stamp(observation["started_at"]), ended_at=stamp(observation["ended_at"])) as tool:
            if observation.get("error"):
                tool.record_error(RuntimeError(observation["error"]))
            return format(trace.get_current_span().get_span_context().span_id,"016x")
    return (instrument_tool,)


@app.cell
def _(event, export_trace, first_trace, get_feedback, get_lab, instrument_tool, mo, np, set_feedback):
    mo.stop(not first_trace.value)
    _session=get_lab()["session"]
    # This is the independent operation receipt. Add another measured setup check here.
    _result,_event=event("inspect_training_environment",{},lambda:{"numpy":np.__version__,"device":"cpu"})
    with _session.stage("setup/trace",config={"device":"cpu"}) as _stage:
        if _stage.needs_run:
            _stage.record({"events":[_event]})
    _trace=export_trace(_session,_stage.id,"Inspect my CPU research environment",_stage.result["events"],tool_writer=instrument_tool)
    _session.checkpoint("setup",evidence={"Agent Lens":_trace["url"]})
    set_feedback({**get_feedback(),"trace":_trace})
    return


@app.cell(hide_code=True)
def _(chapter, get_feedback, mo, ui):
    mo.stop(chapter.value != "1 · Connect")
    mo.vstack([mo.Html(ui.links({"Open my first conversation":get_feedback().get("trace",{}).get("url","")})),mo.md("Next: **2 · Data and baseline**. Keep Agent Lens open beside the notebook.")])
    return


@app.cell
def _():
    # Exercise: use the most recent observed value as the future prediction.
    # Replace the exception with: return split["persistence"].copy()
    def persistence_forecast(split):
        raise NotImplementedError("Return the latest observation for each forecast window.")
    return (persistence_forecast,)


@app.cell(hide_code=True)
def _(chapter, get_lab, mo, ui):
    mo.stop(chapter.value != "2 · Data and baseline")
    load_data=mo.ui.run_button(label="Load the versioned solar observations",disabled=not bool(get_lab().get("session")))
    baseline_button=mo.ui.run_button(label="Check and run my persistence baseline",disabled=not bool(get_lab().get("goes")))
    mo.vstack([mo.Html(ui.step("2. Use the current flux as a forecast", "Implement persistence_forecast in the code cell. Inspect the data before fitting a model. Missing observations are gaps, not zeros.","Every window stays inside its partition; the baseline predicts the last observed value.")),load_data,baseline_button,
    mo.accordion({"Hint":"The loader supplies the latest observation as split['persistence']. Copy it so the exercise does not modify the data.","Data contract":"GOES-15 and AIA 171 Å, February 1–14, 2014. Train: 1–10; validation: 11–12; final test: 13–14. Normalization uses training data only. February 8 is missing from the GOES archive."})])
    return (baseline_button, load_data,)


@app.cell
def _(dataset, get_feedback, get_lab, load_data, mo, set_feedback, set_lab, solar):
    mo.stop(not load_data.value)
    _path,_fingerprint=dataset()
    _goes,_normalization=solar.load_goes(_path)
    # Open a real FITS image with SunPy, not a decorative screenshot.
    from sunpy.map import Map
    _map=Map(_path/"sample-aia.fits")
    _restored={"data_path":str(_path),"dataset":_fingerprint,"goes":_goes}
    _session=get_lab()["session"]
    _manual=[s for s in _session.completed() if s["name"].startswith("images/manual-") and s["inputs"].get("dataset")==_fingerprint]
    if len(_manual)>=2:
        _best=min(_manual,key=lambda s:s["result"]["metrics"]["validation_error"])
        _images,_norm=solar.load_aia(_path)
        _restored.update(images=_images,manual={"stage_id":_best["id"],"source":_best["sources"]["candidate.py"],"config":_best["config"],"metrics":_best["result"]["metrics"],"losses":_best["result"]["losses"],"split":"validation"})
    set_lab({**get_lab(),**_restored})
    set_feedback({**get_feedback(),"data":{"dataset":_fingerprint,"development_windows":{k:len(v["ids"]) for k,v in _goes.items() if k!="test"},"normalization":_normalization,"image_date":str(_map.date),"wavelength":str(_map.wavelength)}})
    return (Map,)


@app.cell
def _(baseline_button, get_feedback, get_lab, mo, np, persistence_forecast, set_feedback, solar):
    mo.stop(not baseline_button.value)
    _session=get_lab()["session"]
    _split=get_lab()["goes"]["validation"]
    _prediction=persistence_forecast(_split)
    assert np.array_equal(_prediction,_split["persistence"]), "Persistence should return the current observation unchanged."
    with _session.stage("goes/persistence",inputs={"dataset":get_lab()["dataset"]}) as _stage:
        if _stage.needs_run:
            _stage.record({"metrics":solar.score(_prediction,_split)})
    _session.checkpoint("goes/baseline")
    set_feedback({**get_feedback(),"baseline":_stage.result})
    return


@app.cell(hide_code=True)
def _(chapter, get_feedback, get_lab, mo, plots):
    mo.stop(chapter.value != "2 · Data and baseline")
    mo.vstack([mo.md(str(get_feedback().get("data","Load data first."))),mo.md(str(get_feedback().get("baseline","Run your baseline, then open 3 · Track and search."))),plots.forecast(get_lab()["goes"]["validation"]["persistence"],get_lab()["goes"]["validation"],title="Persistence on validation dates") if get_lab().get("goes") else mo.md("")])
    return


@app.cell
def _():
    # Edit this source in the code editor below. This exact text is fingerprinted and executed.
    # Try changing training_loss or a layer; explain which behavior you expect to change.
    DEFAULT_SOURCE = '"""Editable research code. The data split and final scorer live elsewhere."""\nimport torch\nfrom torch import nn\n\n\ndef build_model(input_shape, config):\n    width=config.get(\'width\',16)\n    architecture=config.get(\'architecture\',\'mlp\')\n    if len(input_shape)==2:\n        if architecture==\'mlp\':\n            return nn.Sequential(nn.Flatten(),nn.Linear(input_shape[0]*input_shape[1],width),\n                                 nn.ReLU(),nn.Linear(width,1))\n        return nn.Sequential(nn.Conv1d(input_shape[0],width,5,padding=2),nn.ReLU(),\n                             nn.AdaptiveAvgPool1d(1),nn.Flatten(),nn.Linear(width,1))\n    class ImagePredictor(nn.Module):\n        def __init__(self):\n            super().__init__()\n            self.net=nn.Sequential(nn.Conv2d(2,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,1,3,padding=1))\n        def forward(self,x):\n            prediction=self.net(x)\n            return prediction+x[:,1:2] if architecture==\'residual\' else prediction\n    return ImagePredictor()\n\n\ndef training_loss(prediction,target,mask):\n    return ((prediction-target).square()*mask).sum()/mask.sum()\n\n\ndef fit(model,x,y,mask,config):\n    optimizer=torch.optim.Adam(model.parameters(),lr=config.get(\'learning_rate\',.001))\n    generator=torch.Generator().manual_seed(config.get(\'seed\',17))\n    losses=[]\n    model.train()\n    for step in range(config.get(\'steps\',40)):\n        indices=torch.randint(len(x),(min(config.get(\'batch_size\',16),len(x)),),generator=generator)\n        prediction=model(x[indices])\n        loss=training_loss(prediction,y[indices],mask[indices])\n        optimizer.zero_grad()\n        loss.backward()\n        optimizer.step()\n        losses.append(float(loss.detach()))\n    return losses\n'
    return (DEFAULT_SOURCE,)


@app.cell(hide_code=True)
def _(DEFAULT_SOURCE, chapter, get_lab, mo):
    mo.stop(chapter.value not in ("3 · Track and search","4 · Solar images"))
    _drafts=[s for s in get_lab()["session"].completed() if s["name"]=="draft/model"] if get_lab().get("session") else []
    _saved_source=_drafts[-1]["sources"]["candidate.py"] if _drafts else DEFAULT_SOURCE
    source_editor=mo.ui.code_editor(value=_saved_source,language="python",min_height=300,max_height=650,label="Model and training code that will execute")
    save_source=mo.ui.run_button(label="Save my code before training or switching exercises")
    mo.vstack([source_editor,save_source])
    return (save_source, source_editor,)


@app.cell
def _(get_lab, mo, save_source, source_editor):
    mo.stop(not save_source.value)
    _s=get_lab()["session"]
    with _s.stage("draft/model",sources={"candidate.py":source_editor.value}) as _draft:
        if _draft.needs_run: _draft.record({"saved":True})
    _s.checkpoint("code-saved")
    mo.md("Code saved locally and queued for artifact publication. This did not train a model.")
    return


@app.cell
def _(export_trace, instrument_tool, plots, time, training):
    def run_training(session, name, source, splits, config, data_fingerprint):
        # This is the tracking contract. Source, split, data and settings identify a run.
        with session.stage(name, config=config, sources={"candidate.py":source},
                           inputs={"dataset":data_fingerprint,"split":"validation"}) as stage:
            if stage.needs_run:
                started=time.time()
                result,prediction=training.train(source,splits["train"],splits["validation"],config,stage.output_dir)
                figure=plots.forecast(prediction,splits["validation"],title=name)
                figure.savefig(stage.output_dir/"predictions.png",dpi=130)
                result["events"]=[{"id":stage.id+"/train","name":"train_and_validate","arguments":{"config":config,"source_fingerprint":stage.source_fingerprint,"split":"validation"},"result":result["metrics"],"started_at":started,"ended_at":time.time()}]
                stage.record(result,files=[stage.output_dir/file for file in ("candidate.py","weights.pt","predictions.npy","predictions.png","losses.json","stderr.txt")])
        session.checkpoint(name)
        try:
            trace=export_trace(session,stage.id,"Train this exact code and evaluate it on validation dates",stage.result["events"],tool_writer=instrument_tool)
        except Exception as error:
            trace={"status":"unavailable","error":str(error)}
        return {"stage_id":stage.id,"source":source,"config":config,"metrics":stage.result["metrics"],"split":"validation","trace":trace,"losses":stage.result["losses"]}
    return (run_training,)


@app.cell(hide_code=True)
def _(chapter, get_lab, mo, ui):
    mo.stop(chapter.value != "3 · Track and search")
    run_search=mo.ui.run_button(label="Run six tracked configurations",disabled=not bool(get_lab().get("goes")))
    mo.vstack([mo.Html(ui.step("3. Which experiment produced that number?", "Read run_training. Find where data, source, settings and outputs are recorded. Edit the model code, then run a six-configuration search.","Compare three MLP and three temporal-CNN runs. Reopening does not repeat completed runs.")),run_search,mo.md("Tracking exercise: hide the source fingerprint and normalization from a copied result. Explain why its score alone is insufficient to reproduce it. Then restore those fields.")])
    return (run_search,)


@app.cell
def _(get_feedback, get_lab, mo, run_search, run_training, set_feedback, source_editor):
    mo.stop(not run_search.value)
    import wandb
    _session=get_lab()["session"]
    _configurations=[{"architecture":a,"width":w,"learning_rate":lr,"steps":60,"seed":17,"batch_size":32}
                     for a in ("mlp","cnn") for w,lr in ((16,.001),(32,.001),(16,.003))]
    # W&B Sweeps owns the configuration search. The stage journal owns execution reuse.
    with _session.stage("goes/create-sweep",inputs={"source":source_editor.value,"configurations":_configurations}) as _stage:
        if _stage.needs_run:
            _sweep=wandb.sweep({"method":"grid","metric":{"name":"validation_error","goal":"minimize"},"parameters":{"trial":{"values":list(range(6))}}},entity=_session.project.split('/')[0],project=_session.project.split('/')[1])
            _stage.record({"sweep_id":_sweep})
    def _trial():
        with wandb.init(entity=_session.project.split('/')[0],project=_session.project.split('/')[1],job_type="workshop-sweep") as _run:
            _i=int(_run.config.trial)
            _record=run_training(_session,"goes/search-"+str(_i),source_editor.value,get_lab()["goes"],_configurations[_i],get_lab()["dataset"])
            _run.log(_record["metrics"])
    wandb.agent(_stage.result["sweep_id"],function=_trial,count=6,entity=_session.project.split('/')[0],project=_session.project.split('/')[1])
    set_feedback({**get_feedback(),"search":"Search finished. Open the runs in your project; completed executions were reused."})
    return (wandb,)


@app.cell(hide_code=True)
def _(chapter, get_lab, mo, ui):
    mo.stop(chapter.value != "4 · Solar images")
    run_images=mo.ui.run_button(label="Compare my convolutional and residual predictors",disabled=not bool(get_lab().get("data_path")))
    mo.vstack([mo.Html(ui.step("4. Same stack, image predictions", "Inspect build_model and training_loss. Compare predicting the whole future image with predicting a correction to the current image.","Examine the prediction and error image, not only the average. Persistence can be difficult to beat.")),run_images])
    return (run_images,)


@app.cell
def _(get_feedback, get_lab, mo, run_images, run_training, set_feedback, set_lab, solar, source_editor):
    mo.stop(not run_images.value)
    _session=get_lab()["session"]
    _splits,_normalization=solar.load_aia(get_lab()["data_path"])
    _records=[]
    for _architecture in ("conv","residual"):
        _config={"architecture":_architecture,"width":8,"learning_rate":.001,"steps":40,"seed":17,"batch_size":8}
        _records.append(run_training(_session,"images/manual-"+_architecture,source_editor.value,_splits,_config,get_lab()["dataset"]))
    _best=min(_records,key=lambda r:r["metrics"]["validation_error"])
    set_lab({**get_lab(),"images":_splits,"manual":_best,"adopted":_best})
    set_feedback({**get_feedback(),"images":_records})
    return


@app.cell(hide_code=True)
def _(chapter, get_lab, mo):
    mo.stop(chapter.value not in ("3 · Track and search","4 · Solar images"))
    _session=get_lab().get("session")
    _rows=[] if not _session else [{"Experiment":s["name"],"Status":s["status"],**s.get("result",{}).get("metrics",{})} for s in _session.read()["stages"].values() if s["name"].startswith(("goes/search","images/manual"))]
    _preview=[]
    if chapter.value=="4 · Solar images" and get_lab().get("manual"):
        _m=get_lab()["manual"]
        _preview=[mo.image(str(_session.file("outputs/"+_m["stage_id"]+"/predictions.png")))]
    mo.vstack([mo.ui.table(_rows,selection=None),*_preview,mo.md("Next: **4 · Solar images** after the search; **5 · Research agent** after both image models finish.")])
    return


@app.cell
def _():
    def next_research_action(session):
        complete={s["name"] for s in session.completed()}
        for number in (1,2):
            prefix=f"images/round-{number}/"
            for phase,label in (("propose","Ask for two code changes"),("probe-done","Run the two reviewed candidates"),("compose","Ask the agent to compose a version"),("adopt","Run the reviewed composition and save the decision")):
                if prefix+phase not in complete:
                    return number,phase,label
        return 2,"done","Both rounds are complete"

    def saved_result(session,name):
        rows=[s for s in session.completed() if s["name"]==name]
        if len(rows)!=1:
            raise ValueError("Expected exactly one completed stage: "+name)
        return rows[0]["result"]
    return (next_research_action, saved_result,)


@app.cell(hide_code=True)
def _(chapter, get_lab, mo, next_research_action, ui):
    mo.stop(chapter.value != "5 · Research agent")
    _session=get_lab().get("session")
    _action=next_research_action(_session) if _session else (1,"propose","Connect first")
    reviewed=mo.ui.checkbox(label="I reviewed the proposed code and its diff",value=False)
    research_button=mo.ui.run_button(label=f"Round {_action[0]} · {_action[2]}",disabled=not bool(get_lab().get("manual")) or _action[1]=="done")
    mo.vstack([mo.Html(ui.step("5. Let the agent change the experiment", "Read the controller cell below. It requests code, probes isolated versions, then tests a composition. Review every proposed diff before running it.","An adopted version must have an execution with the same code fingerprint. A rejected change remains in the history.")),reviewed,research_button,mo.Html(ui.branch_graph(_session)) if _session else mo.md("Run the image comparison first.")])
    return (research_button, reviewed,)


@app.cell
def _(get_feedback, get_lab, mo, next_research_action, research, research_button, reviewed, run_training, saved_result, set_feedback, set_lab, time):
    mo.stop(not research_button.value)
    _session=get_lab()["session"]
    _number,_phase,_label=next_research_action(_session)
    _prior=saved_result(_session,"images/round-1/adopt") if _number==2 else None
    _parent=get_lab()["manual"] if _number==1 else {**_prior["adopted"],"lessons":[{"lesson":_prior.get("lesson"),"limits":_prior.get("limits")}]}
    _prefix=f"images/round-{_number}/"
    if _phase=="propose":
        _proposal,_id=research.propose(_session,_number,_parent["source"],{**_parent,"split":"validation"})
        try:
            research.trace_decision(_session,_id)
        except Exception as _error:
            set_feedback({**get_feedback(),"export":str(_error)})
    elif _phase=="probe-done":
        mo.stop(not reviewed.value,mo.md("Read both proposed diffs, then tick the review box."))
        _proposal=saved_result(_session,_prefix+"propose")
        _probes=[]
        for _i,_candidate in enumerate(_proposal["candidates"]):
            try:
                _probe=run_training(_session,_prefix+"probe-"+str(_i),_candidate["source"],get_lab()["images"],_parent["config"],get_lab()["dataset"])
            except Exception as _error:
                _probe={"source":_candidate["source"],"config":_parent["config"],"split":"validation","errors":[str(_error)],"metrics":{}}
            _probes.append({**_probe,"title":_candidate["title"],"rationale":_candidate["rationale"]})
        with _session.stage(_prefix+"probe-done",inputs={"probes":_probes}) as _stage:
            if _stage.needs_run:
                _stage.record({"probes":_probes})
    elif _phase=="compose":
        _probes=saved_result(_session,_prefix+"probe-done")["probes"]
        _decision,_id=research.compose(_session,_number,_parent["source"],_parent,_probes)
        try:
            research.trace_decision(_session,_id)
        except Exception as _error:
            set_feedback({**get_feedback(),"export":str(_error)})
    elif _phase=="adopt":
        mo.stop(not reviewed.value,mo.md("Review the composition diff before running it."))
        _decision=saved_result(_session,_prefix+"compose")["decision"]
        try:
            _executed=run_training(_session,_prefix+"composition-test",_decision["source"],get_lab()["images"],_parent["config"],get_lab()["dataset"])
        except Exception as _error:
            _executed={"stage_id":None,"errors":[str(_error)],"metrics":{}}
        # This policy is explicit. Keep the parent when the composition is worse on validation.
        _adopted=_executed if _executed["metrics"].get("validation_error",float("inf"))<_parent["metrics"]["validation_error"] else _parent
        with _session.stage(_prefix+"adopt",inputs={"tested":_executed["stage_id"]}) as _stage:
            if _stage.needs_run:
                _stage.record({"adopted":_adopted,"decision":_decision,"retained_parent":_adopted is _parent,"lesson":_decision.get("lesson"),"limits":_decision.get("limits"),"execution_error":_executed.get("errors")})
    _session.checkpoint(_prefix+_phase)
    set_lab({**get_lab(),"revision":time.time()})
    return


@app.cell(hide_code=True)
def _(chapter, get_feedback, get_lab, mo, next_research_action, ui):
    mo.stop(chapter.value != "6 · Final evaluation")
    _session=get_lab().get("session")
    _done=bool(_session) and next_research_action(_session)[1]=="done"
    final_button=mo.ui.run_button(label="Freeze versions and evaluate on the reserved dates",disabled=not _done)
    conclusion=mo.ui.text_area(label="What did your changes do? Cite a prediction, a run, and a code change.",full_width=True)
    report_button=mo.ui.run_button(label="Publish my conclusion and evidence",disabled=not bool(get_feedback().get("final")))
    retry_publication=mo.ui.run_button(label="Retry publication of saved evidence",disabled=not bool(_session))
    mo.vstack([mo.Html(ui.step("6. Test the frozen versions", "The search is over. Compare persistence, your selected manual model and the adopted agent model on dates neither search used.","Report image error, persistence-relative skill, runtime and the cost of finding the version. A passing workshop does not require a better score.")),final_button,conclusion,report_button,retry_publication])
    return (conclusion, final_button, report_button, retry_publication,)


@app.cell
def _(final_button, get_feedback, get_lab, mo, np, publish_comparison, research, saved_result, set_feedback, solar, training):
    mo.stop(not final_button.value)
    _session=get_lab()["session"]
    _adopted=saved_result(_session,"images/round-2/adopt")["adopted"]
    _versions={"manual":get_lab()["manual"],"agent":_adopted}
    _freeze,_freeze_id=research.freeze(_session,_versions,get_lab()["dataset"])
    _test=get_lab()["images"]["test"]
    _comparisons={"persistence":solar.evaluation_rows(_test["persistence"],_test)}
    _results={"persistence":solar.score(_test["persistence"],_test)}
    for _label,_version in _versions.items():
        _weights=_session.file("outputs/"+_version["stage_id"]+"/weights.pt")
        with _session.stage("images/final-"+_label,config=_version["config"],sources={"candidate.py":_version["source"]},inputs={"freeze":_freeze_id,"split":"test"}) as _stage:
            if _stage.needs_run:
                _result,_prediction=training.train(_version["source"],None,_test,_version["config"],_stage.output_dir,weights=_weights)
                _stage.record(_result,files=[_stage.output_dir/"predictions.npy"])
            _prediction=np.load(_stage.output_dir/"predictions.npy")
            _results[_label]=_stage.result["metrics"]
            _comparisons[_label]=solar.evaluation_rows(_prediction,_test,evidence={"stage":_stage.id,"source":_stage.source_fingerprint,"trace":_version.get("trace",{})})
    with _session.stage("images/final-comparison",inputs={"freeze":_freeze_id}) as _stage:
        if _stage.needs_run:
            _stage.record({"metrics_by_version":_results,"rows":_comparisons})
    _receipts=publish_comparison(_session,"solar-images-final",_comparisons)
    _session.checkpoint("final-evaluation",evidence={label:r["run"] for label,r in _receipts.items()})
    set_feedback({**get_feedback(),"final":{"results":_results,"publication":_receipts}})
    return


@app.cell
def _(conclusion, get_feedback, get_lab, mo, publish_report, report_button, set_feedback):
    mo.stop(not report_button.value)
    _session=get_lab()["session"]
    _links=_session.read()["progress"].get("evidence",{})
    _url=publish_report(_session,conclusion.value,_links)
    _session.checkpoint("report",evidence={"Report":_url})
    set_feedback({**get_feedback(),"report":_url})
    return


@app.cell
def _(get_feedback, get_lab, mo, publish_comparison, retry_publication, set_feedback):
    mo.stop(not retry_publication.value)
    _session=get_lab()["session"]
    _status=_session.retry_publication()
    _saved=[s for s in _session.completed() if s["name"]=="images/final-comparison"]
    if _saved:
        _status["evaluations"]=publish_comparison(_session,"solar-images-final",_saved[0]["result"]["rows"])
    set_feedback({**get_feedback(),"publication_retry":_status})
    return


@app.cell(hide_code=True)
def _(chapter, get_feedback, get_lab, mo, np, plots, ui):
    mo.stop(chapter.value != "6 · Final evaluation")
    _metrics=get_feedback().get("final",{}).get("results",{})
    _final_preview=[]
    if _metrics:
        _s=get_lab()["session"]
        for _stage in _s.completed():
            if _stage["name"].startswith("images/final-") and _stage["name"]!="images/final-comparison":
                _prediction=np.load(_s.file("outputs/"+_stage["id"]+"/predictions.npy"))
                _final_preview.append(plots.forecast(_prediction,get_lab()["images"]["test"],title=_stage["name"]))
    mo.vstack([mo.ui.table([{"version":k,**v} for k,v in _metrics.items()],selection=None),*_final_preview,mo.md(str(get_feedback().get("final",{}).get("publication","Finish both research rounds first."))),mo.Html(ui.links({"My Report":get_feedback().get("report","")})),mo.md("Optional ARIA prompt: Review my Report and linked research-agent traces. Identify one supported reason a change helped or hurt, cite the exact evidence, and propose one next experiment. Do not launch new runs.")])
    return

if __name__ == "__main__":
    app.run()
