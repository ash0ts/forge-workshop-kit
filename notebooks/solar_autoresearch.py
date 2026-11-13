# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.2.2/forge_workshop_kit-0.2.2-py3-none-any.whl", "torch==2.15.0"]
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
    from forge_workshop_kit import solar, training, research, ui, plots, solar_teaching as teaching
    from forge_workshop_kit.session import digest
    from forge_workshop_kit.download import dataset
    from forge_workshop_kit.publication import publish_comparison, publish_report
    from forge_workshop_kit.traces import export_trace, event, stamp
    get_lab, set_lab = mo.state({})
    get_feedback, set_feedback = mo.state({})
    get_tracing_check, set_tracing_check = mo.state({})
    get_step, set_step = mo.state("setup", allow_self_loops=True)
    return (Path, WorkshopSession, dataset, digest, event, export_trace, get_feedback, get_lab, get_step, get_tracing_check, json, mo, np, os, plots, publish_comparison, publish_report, research, set_feedback, set_lab, set_step, set_tracing_check, solar, stamp, teaching, time, training, ui,)


@app.cell(hide_code=True)
def _(mo, ui):
    mo.Html(ui.heading("Build a research loop, then give it an agent", "We’ll start with a simple solar forecast, train a few models, and keep enough detail to explain each result. Then you’ll give a research agent the code and ask it to try two changes. You’ll test each suggestion before keeping a change.", theme="lab"))
    return


@app.cell(hide_code=True)
def _(get_feedback, get_lab, set_feedback, set_lab, set_step, teaching):
    def go_to(step):
        session = get_lab().get("session")
        if session:
            session.set_view(step)
        set_step(step)

    def refresh_saved():
        context = get_lab()
        set_lab({**context, **teaching.restore_state(context["session"])})

    def checked(name, action):
        try:
            result = action()
            set_feedback({**get_feedback(), name: {"status": "complete", **result}})
        except Exception as error:
            set_feedback({**get_feedback(), name: {"status": "needs work", "message": str(error)}})
    return (checked, go_to, refresh_saved,)


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, ui):
    _s = get_lab().get("session")
    solar_navigation = ui.navigation(mo, teaching.STEPS, get_step(), go_to, completed=teaching.completed_steps(_s) if _s else (), label="Your research loop")
    mo.vstack([solar_navigation, mo.Html(ui.context(_s)) if _s else mo.md("**Start at Connect.** Your code and results stay in your project. Training and model calls run only when you click their Run buttons.")])
    return (solar_navigation,)


@app.cell(hide_code=True)
def _(get_lab, mo):
    help_message = mo.ui.text_area(label="What do you need help with?", full_width=True)
    help_button = mo.ui.run_button(label="Send a help request", disabled=not bool(get_lab().get("session")))
    mo.accordion({"Ask the facilitator": mo.vstack([help_message, help_button, mo.md("Tell the facilitator which step you’re on and what happened. They can read this request in the workshop monitor.")])})
    return (help_button, help_message,)


@app.cell(hide_code=True)
def _(get_lab, help_button, help_message, mo):
    mo.stop(not help_button.value)
    get_lab()["session"].request_help(help_message.value)
    mo.md("Help request saved. Send an empty message when it is resolved.")
    return


@app.cell(hide_code=True)
def _(get_step, mo, os, ui):
    mo.stop(get_step() != "setup")
    _default = os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None, [os.getenv("WANDB_ENTITY"), os.getenv("WANDB_PROJECT")]))
    project_input = mo.ui.text(value=_default, placeholder="your-name/solar-research", label="Your Forge project", full_width=True)
    allowance = mo.ui.number(value=8, start=.01, stop=1000, label="Inference allowance in USD; notebook compute is separate")
    connect_button = mo.ui.run_button(label="Connect and restore my work")
    mo.vstack([mo.Html(ui.step("1. Connect to your own project", "Enter the Forge project where you want your runs and traces saved, then click Connect and restore my work. In Forge, use your signed-in account. On a laptop, run uv run wandb login first.", "Once the connection succeeds, add your first trace in the code below.")), project_input, allowance, connect_button])
    return (allowance, connect_button, project_input,)


@app.cell(hide_code=True)
def _(WorkshopSession, allowance, connect_button, get_feedback, mo, project_input, set_feedback, set_lab, set_step, teaching):
    mo.stop(not connect_button.value)
    try:
        _s = WorkshopSession.from_environment("solar-autoresearch", project=project_input.value, budget_usd=allowance.value)
        _access = _s.check_access()
        _restored = _s.restore()
        set_lab(teaching.restore_state(_s))
        set_step(_s.get_view("setup"))
        set_feedback({**get_feedback(), "setup": {"status": "complete", **_access, "restore": _restored}})
    except Exception as _error:
        set_feedback({**get_feedback(), "setup": {"status": "unavailable", "message": str(_error), "next": "Check that you’re signed in and can write to this project, then try Connect again."}})
    return


@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching):
    _s = get_lab().get("session")
    instrumentation_editor = mo.ui.code_editor(value=_s.get_draft("solar/instrumentation", teaching.INSTRUMENTATION_STARTER) if _s else teaching.INSTRUMENTATION_STARTER, language="python", on_change=lambda value: _s.save_draft("solar/instrumentation", value) if _s else None, debounce=False)
    check_instrumentation = mo.ui.run_button(label="Check my tracing code")
    mo.vstack([mo.md("**Give your first trace a label.** In `instrument_tool`, add `workshop.exercise` with the value `solar-research` inside the Tool scope. Click **Check my tracing code**, then **Send my first Agent Lens trace**. We’ll reuse this function when you train a model."), instrumentation_editor, check_instrumentation, mo.accordion({"Hint": mo.md("Add `tool.set_attributes({'workshop.exercise': 'solar-research'})` inside the `with tracing.Tool(...)` block. Leave the other fields in place so the trace still shows what ran."), "Worked answer": mo.md("```python\n" + teaching.INSTRUMENTATION_SOLUTION + "\n```")})]) if get_step() == "setup" else mo.md("")
    return (check_instrumentation, instrumentation_editor,)


@app.cell
def _(instrumentation_editor, teaching):
    # The edited function below is the writer used by every export in this notebook.
    def instrument_tool(observation):
        return teaching.functions(instrumentation_editor.value)["instrument_tool"](observation)
    return (instrument_tool,)


@app.cell(hide_code=True)
def _(check_instrumentation, digest, instrumentation_editor, mo, set_tracing_check, teaching):
    mo.stop(not check_instrumentation.value)
    try:
        _result = teaching.check_instrumentation(instrumentation_editor.value)
        set_tracing_check({"status": "complete", **_result, "source": digest(instrumentation_editor.value)})
    except Exception as _error:
        set_tracing_check({"status": "needs work", "message": str(_error)})
    return


@app.cell(hide_code=True)
def _(digest, get_feedback, get_lab, get_step, get_tracing_check, go_to, instrumentation_editor, mo, teaching, ui):
    mo.stop(get_step() != "setup")
    _s = get_lab().get("session")
    _checked = get_tracing_check()
    first_trace = mo.ui.run_button(label="Send my first Agent Lens trace", disabled=not bool(_s) or _checked.get("source") != digest(instrumentation_editor.value))
    _setup = get_feedback().get("setup", {})
    solar_next_step_2 = ui.next_step(mo, "Next: inspect the solar data", "data", go_to)
    mo.vstack([mo.Html(ui.result("Connection", _setup, status=_setup.get("status", "not checked"))) if _setup else mo.md("Enter your project above, then click **Connect and restore my work**."), mo.Html(ui.result("Local tracing check", _checked, status=_checked.get("status", "not checked"))) if _checked else mo.md("Add the attribute in the code above, then click **Check my tracing code**."), mo.md("The Send button runs a small environment check and saves its trace. Open the link below when it finishes."), first_trace, ui.evidence(mo, _s, stage_ids=[teaching.saved(_s, "setup/trace")["id"]] if _s and teaching.saved(_s, "setup/trace") else (), question="Open inspect_training_environment in Agent Lens. Find workshop.exercise=solar-research and the NumPy version returned by the tool.") if _s else mo.md("Connect above first."), solar_next_step_2])
    return (first_trace, solar_next_step_2,)


@app.cell(hide_code=True)
def _(event, export_trace, first_trace, get_feedback, get_lab, instrument_tool, instrumentation_editor, mo, np, refresh_saved, set_feedback, teaching):
    mo.stop(not first_trace.value)
    _s = get_lab()["session"]
    teaching.check_instrumentation(instrumentation_editor.value)
    with _s.stage("setup/trace", config={"device": "cpu"}, sources={"instrumentation.py": instrumentation_editor.value}) as _stage:
        if _stage.needs_run:
            _result, _event = event("inspect_training_environment", {}, lambda: {"numpy": np.__version__, "device": "cpu"})
            _stage.record({"events": [_event]})
    try:
        _trace = export_trace(_s, _stage.id, "Inspect my CPU research environment", _stage.result["events"], tool_writer=instrument_tool)
        _s.checkpoint("setup", evidence={"Setup conversation": _trace["url"]})
        set_feedback({**get_feedback(), "setup_trace": {"status": "complete", "stored spans": _trace["stored_spans"]}})
    except Exception as _error:
        set_feedback({**get_feedback(), "setup_trace": {"status": "publication pending", "message": str(_error), "next": "The check is saved. Click Send my first Agent Lens trace again to retry its upload."}})
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, mo, teaching, ui):
    mo.stop(get_step() != "setup")
    _status = get_feedback().get("setup_trace", {})
    _s = get_lab().get("session")
    _saved = teaching.saved(_s, "setup/trace") if _s else None
    _receipt = _s.read()["publications"].get("trace/" + _saved["id"], {}) if _saved else {}
    if not _status and _receipt.get("verified"):
        _status = {"status": "complete", "stored spans": _receipt["stored_spans"], "result": "Your saved trace is available in Agent Lens."}
    mo.Html(ui.result("Your first trace", _status, status=_status.get("status", "not sent"))) if _status else mo.md("Your trace will appear here after you click **Send my first Agent Lens trace**.")
    return


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, ui):
    mo.stop(get_step() != "data")
    _s = get_lab().get("session")
    load_data = mo.ui.run_button(label="Load the solar dataset", disabled=not bool(_s))
    solar_prerequisite_3 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.vstack([mo.Html(ui.step("2. Inspect the observations", "Click Load the solar dataset. We’ll use SunPy to read an image’s FITS metadata, then look at the measurements we want to predict.", "Find the observation date and wavelength below. We train on February 1–10, compare changes on 11–12, and save 13–14 for the final test.")), mo.md("**Real observations, two prediction tasks.** First, use an hour of GOES-15 X-ray measurements to forecast flux 30 minutes ahead. The measurements are in W/m²; we predict log10 XRS-B flux. Later, use AIA 171 Å images of the Sun to predict an image one hour ahead. Both come from the February 2014 archives."), mo.md("[SunPy GOES retrieval](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html) · [AIA archive and calibration](https://jsoc1.stanford.edu/data/aia/synoptic/README.html) · [Our acquisition code](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)"), load_data, solar_prerequisite_3 if not _s else mo.md("The download is about 26 MB. You’ll see the date, wavelength, and number of usable windows below."), mo.accordion({"What is reserved?": mo.md("A window contains the past observations and the future value we want to predict. Windows stay within their date split and are dropped if observations are missing. February 8 is missing from the GOES archive. We fit normalization on training data and keep the final dates out of the research agent’s input."), "Inspect the acquisition code": mo.md("[Source, quality checks and preprocessing](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)")})])
    return (load_data, solar_prerequisite_3,)


@app.cell(hide_code=True)
def _(dataset, get_lab, load_data, mo, set_lab, solar):
    mo.stop(not load_data.value)
    _s = get_lab()["session"]
    _path, _fingerprint = dataset()
    _goes, _normalization = solar.load_goes(_path)
    _images, _image_normalization = solar.load_aia(_path)
    from sunpy.map import Map
    _map = Map(_path / "sample-aia.fits")
    with _s.stage("data/loaded", inputs={"dataset": _fingerprint}) as _stage:
        if _stage.needs_run:
            _stage.record({"dataset": _fingerprint, "development_windows": {k: len(v["ids"]) for k, v in _goes.items() if k != "test"}, "normalization": _normalization, "image_date": str(_map.date), "wavelength": str(_map.wavelength)})
    _s.checkpoint("data")
    set_lab({**get_lab(), "data_path": str(_path), "dataset": _fingerprint, "goes": _goes, "images": _images})
    return (Map,)


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, plots, teaching, ui):
    mo.stop(get_step() != "data")
    _s = get_lab().get("session")
    _record = teaching.saved(_s, "data/loaded") if _s else None
    solar_next_step_4 = ui.next_step(mo, "Next: implement persistence", "baseline", go_to)
    mo.vstack([mo.Html(ui.result("Dataset loaded", _record["result"])) if _record else mo.md("Click Load the solar dataset to see the observations and a first forecast plot."), plots.forecast(get_lab()["goes"]["validation"]["persistence"], get_lab()["goes"]["validation"], title="Validation measurements: the latest observation as a forecast") if get_lab().get("goes") else mo.md("Returning to the notebook? Click Load the solar dataset to put the arrays back in memory. Your completed experiments stay saved."), ui.evidence(mo, _s, stage_ids=[_record["id"]], question="Open data / loaded · files. This W&B Artifact is a versioned collection of saved files. Find the observation date and wavelength in its dataset record; later runs will save code, weights, and predictions the same way.") if _record else mo.md(""), solar_next_step_4])
    return (solar_next_step_4,)


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "baseline")
    _s = get_lab().get("session")
    solar_prerequisite_5 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_5)
    persistence_editor = mo.ui.code_editor(value=_s.get_draft("solar/persistence", teaching.PERSISTENCE_STARTER), language="python", min_height=130, label="Implement persistence_forecast", on_change=lambda value: _s.save_draft("solar/persistence", value))
    check_persistence = mo.ui.run_button(label="Check my persistence function")
    baseline_button = mo.ui.run_button(label="Run my persistence baseline", disabled=not bool(get_lab().get("goes")))
    solar_prerequisite_6 = ui.prerequisite(mo, "Load the dataset before running the baseline.", "data", go_to)
    mo.vstack([mo.Html(ui.step("3. Predict 30 minutes ahead by copying the latest reading", "In persistence_forecast, replace the exception with a copy of the latest measurement. This is persistence: predict that the current value will stay the same. Check the function, then click Run my persistence baseline.", "Read its validation error below. This is the score your trained models will try to beat.")), persistence_editor, check_persistence, mo.accordion({"Hint": mo.md("Use `split['persistence'].copy()`. The latest value is already provided; you don’t need the future target in `split['y']`."), "Worked answer": mo.md("```python\n" + teaching.PERSISTENCE_SOLUTION + "\n```")}), baseline_button, solar_prerequisite_6 if not get_lab().get("goes") else mo.md("After the check passes, run your function and compare its error with the models in the next step.")])
    return (baseline_button, check_persistence, persistence_editor, solar_prerequisite_5, solar_prerequisite_6,)


@app.cell(hide_code=True)
def _(check_persistence, checked, mo, persistence_editor, teaching):
    mo.stop(not check_persistence.value)
    checked("persistence-check", lambda: teaching.check_persistence(persistence_editor.value))
    return


@app.cell(hide_code=True)
def _(baseline_button, export_trace, get_feedback, get_lab, instrument_tool, mo, np, persistence_editor, refresh_saved, set_feedback, solar, teaching, time):
    mo.stop(not baseline_button.value)
    teaching.check_persistence(persistence_editor.value)
    _s = get_lab()["session"]
    _split = get_lab()["goes"]["validation"]
    with _s.stage("goes/persistence", inputs={"dataset": get_lab()["dataset"], "split": "validation"}, sources={"persistence.py": persistence_editor.value}) as _stage:
        if _stage.needs_run:
            _started = time.time()
            _prediction = teaching.functions(persistence_editor.value)["persistence_forecast"](_split)
            np.save(_stage.output_dir / "predictions.npy", _prediction)
            _metrics = solar.score(_prediction, _split)
            _stage.record({"metrics": _metrics, "events": [{"id": _stage.id + "/predict", "name": "persistence_forecast", "arguments": {"split": "validation", "windows": len(_split["ids"])}, "result": _metrics, "started_at": _started, "ended_at": time.time()}]}, files=[_stage.output_dir / "predictions.npy"])
    try:
        export_trace(_s, _stage.id, "Evaluate my persistence forecast on validation dates", _stage.result["events"], tool_writer=instrument_tool)
    except Exception as _error:
        set_feedback({**get_feedback(), "baseline-export": str(_error)})
    _s.checkpoint("baseline")
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, mo, persistence_editor, teaching, ui):
    mo.stop(get_step() != "baseline")
    _s = get_lab().get("session")
    _row = teaching.saved(_s, "goes/persistence") if _s else None
    _check = get_feedback().get("persistence-check", {})
    solar_next_step_7 = ui.next_step(mo, "Next: track six model configurations", "search", go_to)
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/persistence", persistence_editor.value)) if _s else mo.md(""), mo.Html(ui.result("Local function check", _check, status=_check.get("status", "not checked"))), mo.Html(ui.result("Persistence validation result", _row["result"].get("metrics", {}))) if _row else mo.md("Click Run my persistence baseline to calculate its validation error."), ui.evidence(mo, _s, stage_ids=[_row["id"]], question="Open the persistence run. Find its error and validation dates, then open its files and compare persistence.py with the function you wrote.") if _row else mo.md(""), solar_next_step_7])
    return (solar_next_step_7,)


@app.cell(hide_code=True)
def _():
    DEFAULT_SOURCE = '"""Editable research code. The data split and final scorer live elsewhere."""\nimport torch\nfrom torch import nn\n\n\ndef build_model(input_shape, config):\n    width=config.get(\'width\',16)\n    architecture=config.get(\'architecture\',\'mlp\')\n    if len(input_shape)==2:\n        if architecture==\'mlp\':\n            return nn.Sequential(nn.Flatten(),nn.Linear(input_shape[0]*input_shape[1],width),\n                                 nn.ReLU(),nn.Linear(width,1))\n        return nn.Sequential(nn.Conv1d(input_shape[0],width,5,padding=2),nn.ReLU(),\n                             nn.AdaptiveAvgPool1d(1),nn.Flatten(),nn.Linear(width,1))\n    class ImagePredictor(nn.Module):\n        def __init__(self):\n            super().__init__()\n            self.net=nn.Sequential(nn.Conv2d(2,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,1,3,padding=1))\n        def forward(self,x):\n            prediction=self.net(x)\n            return prediction+x[:,1:2] if architecture==\'residual\' else prediction\n    return ImagePredictor()\n\n\ndef training_loss(prediction,target,mask):\n    return ((prediction-target).square()*mask).sum()/mask.sum()\n\n\ndef fit(model,x,y,mask,config):\n    optimizer=torch.optim.Adam(model.parameters(),lr=config.get(\'learning_rate\',.001))\n    generator=torch.Generator().manual_seed(config.get(\'seed\',17))\n    losses=[]\n    model.train()\n    for step in range(config.get(\'steps\',40)):\n        indices=torch.randint(len(x),(min(config.get(\'batch_size\',16),len(x)),),generator=generator)\n        prediction=model(x[indices])\n        loss=training_loss(prediction,y[indices],mask[indices])\n        optimizer.zero_grad()\n        loss.backward()\n        optimizer.step()\n        losses.append(float(loss.detach()))\n    return losses\n'
    return (DEFAULT_SOURCE,)


@app.cell(hide_code=True)
def _(DEFAULT_SOURCE, get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    solar_prerequisite_8 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_8)
    measurement_editor = mo.ui.code_editor(value=_s.get_draft("solar/measurement", teaching.model_starter(DEFAULT_SOURCE, "measurement")), language="python", min_height=320, max_height=650, label="Measurement model source: complete training_loss", on_change=lambda value: _s.save_draft("solar/measurement", value))
    flux_metric_editor = mo.ui.code_editor(value=_s.get_draft("solar/flux-metric", teaching.FLUX_STARTER), language="python", min_height=120, label="Implement my_flux_mae", on_change=lambda value: _s.save_draft("solar/flux-metric", value))
    check_measurement = mo.ui.run_button(label="Check my measurement code")
    run_search = mo.ui.run_button(label="Run six tracked configurations", disabled=not bool(get_lab().get("goes")) or teaching.saved(_s, "images/freeze") is not None)
    solar_prerequisite_9 = ui.prerequisite(mo, "Load the dataset before training.", "data", go_to)
    mo.vstack([mo.Html(ui.step("4. Record the experiment before comparing it", "Complete training_loss and my_flux_mae below. The loss trains the model; mean absolute error (MAE) measures how far its forecasts miss. Check your code, then click Run six tracked configurations.", "You’ll get six runs: three small feed-forward networks (MLPs) and three temporal convolutional networks (CNNs). Compare their validation errors in the Sweep.")), mo.md("Read `run_training` below before you run it. It saves your settings, metrics, code, trained weights, and predictions with each experiment. Open one run afterward and find those files."), measurement_editor, flux_metric_editor, check_measurement, mo.accordion({"Hint": mo.md("For training_loss, square the prediction error, multiply by the mask, sum, and divide by the mask sum. For my_flux_mae, average the absolute errors. A negative miss must not cancel a positive miss."), "Worked answers": mo.md("```python\ndef training_loss(prediction, target, mask):\n    return ((prediction - target).square() * mask).sum() / mask.sum()\n\n" + teaching.FLUX_SOLUTION + "\n```"), "Why this is a search": mo.md("A Sweep tries settings in implementations we already have. Here it tries three width/learning-rate combinations for each architecture. Every run uses seed 17, 60 training steps, and batch size 32. Later, the agent will change the code itself.")}), run_search, solar_prerequisite_9 if not get_lab().get("goes") else mo.md("The six runs train on this notebook’s CPU. If you return later with the same code and settings, the notebook uses the saved runs.")])
    return (check_measurement, flux_metric_editor, measurement_editor, run_search, solar_prerequisite_8, solar_prerequisite_9,)


@app.cell(hide_code=True)
def _(check_measurement, checked, flux_metric_editor, measurement_editor, mo, teaching):
    mo.stop(not check_measurement.value)
    def _check():
        return {"model": teaching.check_model(measurement_editor.value, "measurement"), "metric": teaching.check_flux_metric(flux_metric_editor.value)}
    checked("measurement-check", _check)
    return


@app.cell
def _(export_trace, instrument_tool, np, plots, teaching, time, training):
    def run_training(session, name, source, splits, config, data_fingerprint, metric_source):
        # The learner's source and metric both belong to this execution's identity.
        with session.stage(name, config=config,
            sources={"candidate.py": source, "development_metric.py": metric_source},
            inputs={"dataset": data_fingerprint, "split": "validation"}) as stage:
            if stage.needs_run:
                started = time.time()
                result, prediction = training.train(source, splits["train"], splits["validation"], config, stage.output_dir)
                figure = plots.forecast(prediction, splits["validation"], title=name)
                figure.savefig(stage.output_dir / "predictions.png", dpi=130)
                functions = teaching.functions(metric_source)
                learner_error = functions["my_flux_mae"](prediction, splits["validation"]["y"]) if prediction.ndim == 2 else functions["my_image_mae"](prediction, splits["validation"]["y"], splits["validation"]["mask"])
                result["metrics"]["learner_metric"] = learner_error
                result["metrics"]["learner_metric_matches"] = bool(np.isclose(learner_error, result["metrics"]["error"]))
                result["events"] = [{"id": stage.id + "/train", "name": "train_and_validate", "arguments": {"config": config, "source_fingerprint": stage.source_fingerprint, "split": "validation"}, "result": result["metrics"], "started_at": started, "ended_at": time.time()}]
                # These files, not just the score, make the result reproducible.
                stage.record(result, files=[stage.output_dir / file for file in ("candidate.py", "weights.pt", "predictions.npy", "predictions.png", "losses.json", "stderr.txt")])
        try:
            export_trace(session, stage.id, "Train this exact code and evaluate it on validation dates", stage.result["events"], tool_writer=instrument_tool)
        except Exception as error:
            with session.transaction() as state:
                state["publications"].setdefault("trace/" + stage.id, {}).update(status="unavailable", error=str(error))
            # The execution stays complete. Retry exports from the final step without training.
        session.checkpoint(name)
        return teaching.training_record(session, session.read()["stages"][stage.id])
    return (run_training,)


@app.cell
def _(digest, flux_metric_editor, get_lab, measurement_editor, mo, os, refresh_saved, run_search, run_training, teaching):
    mo.stop(not run_search.value)
    import wandb
    teaching.check_model(measurement_editor.value, "measurement")
    teaching.check_flux_metric(flux_metric_editor.value)
    _s = get_lab()["session"]
    _configurations = [{"architecture": a, "width": w, "learning_rate": lr, "steps": 60, "seed": 17, "batch_size": 32} for a in ("mlp", "cnn") for w, lr in ((16, .001), (32, .001), (16, .003))]
    _source = measurement_editor.value
    _metric = flux_metric_editor.value
    with _s.stage("goes/create-sweep", inputs={"source": _source, "metric": _metric, "configurations": _configurations}) as _sweep_stage:
        if _sweep_stage.needs_run:
            _sweep_id = wandb.sweep({"method": "grid", "metric": {"name": "validation_error", "goal": "minimize"}, "parameters": {"trial": {"values": list(range(6))}}}, entity=_s.project.split('/')[0], project=_s.project.split('/')[1])
            _sweep_stage.record({"sweep_id": _sweep_id})
    _completed = {row["name"] for row in _s.completed() if row["sources"].get("candidate.py") == _source and row["sources"].get("development_metric.py") == _metric}
    _remaining = sum("goes/search-" + str(i) not in _completed for i in range(6))
    def _trial():
        with wandb.init(entity=_s.project.split('/')[0], project=_s.project.split('/')[1], job_type="workshop-sweep") as _run:
            _i = int(_run.config.trial)
            _cfg = _configurations[_i]
            _run.name = f"GOES / {_cfg['architecture'].upper()} / width {_cfg['width']} / lr {_cfg['learning_rate']}"
            _run.config.update({"experiment": _configurations[_i], "dataset": get_lab()["dataset"], "source_fingerprint": digest({"candidate.py": _source, "development_metric.py": _metric})})
            # A Sweep owns its active W&B run. Save local receipts now; publish their
            # separate runs/artifacts after the Sweep finishes to avoid nested run IDs.
            _publisher = _s.publisher
            _s.publisher = None
            try:
                _record = run_training(_s, "goes/search-" + str(_i), _source, get_lab()["goes"], _configurations[_i], get_lab()["dataset"], _metric)
            finally:
                _s.publisher = _publisher
            _run.summary["execution_stage"] = _record["stage_id"]
            _run.log(_record["metrics"])
    if _remaining:
        _sweep_environment = {key: os.environ.get(key) for key in ("WANDB_RUN_ID", "WANDB_SWEEP_ID", "WANDB_SWEEP_PARAM_PATH")}
        try:
            wandb.agent(_sweep_stage.result["sweep_id"], function=_trial, count=_remaining, entity=_s.project.split('/')[0], project=_s.project.split('/')[1])
        finally:
            for _key, _value in _sweep_environment.items():
                if _value is None:
                    os.environ.pop(_key, None)
                else:
                    os.environ[_key] = _value
    _s.checkpoint("search", evidence={"Measurement Sweep": "https://wandb.ai/" + _s.project + "/sweeps/" + _sweep_stage.result["sweep_id"].split('/')[-1]})
    refresh_saved()
    return (wandb,)


@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, measurement_editor, mo, teaching, ui):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    _rows = [] if not _s else [row for row in _s.completed() if row["name"].startswith("goes/search-")]
    _check = get_feedback().get("measurement-check", {})
    solar_next_step_10 = ui.next_step(mo, "Next: predict a solar image", "images", go_to)
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/measurement", measurement_editor.value, stage_prefix="goes/search-")) if _s else mo.md(""), mo.Html(ui.result("Local measurement checks", _check, status=_check.get("status", "not checked"))), mo.ui.table([{"Run": row["name"], "Architecture": row["config"]["architecture"], "Width": row["config"]["width"], "Learning rate": row["config"]["learning_rate"], **row["result"]["metrics"]} for row in _rows], selection=None), ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="Open the Measurement Sweep and choose one MLP and one CNN. Compare validation_error, width, and learning rate. In each run’s files, find candidate.py and losses.json to see which code trained and how its loss changed.") if _s else mo.md(""), solar_next_step_10])
    return (solar_next_step_10,)


@app.cell(hide_code=True)
def _(DEFAULT_SOURCE, get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "images")
    _s = get_lab().get("session")
    solar_prerequisite_11 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_11)
    image_editor = mo.ui.code_editor(value=_s.get_draft("solar/image", teaching.model_starter(DEFAULT_SOURCE, "image")), language="python", min_height=320, max_height=650, label="Image model source: complete ImagePredictor.forward", on_change=lambda value: _s.save_draft("solar/image", value))
    image_metric_editor = mo.ui.code_editor(value=_s.get_draft("solar/image-metric", teaching.IMAGE_METRIC_STARTER), language="python", min_height=140, label="Implement my_image_mae", on_change=lambda value: _s.save_draft("solar/image-metric", value))
    check_images = mo.ui.run_button(label="Check my image code")
    _locked = teaching.saved(_s, "images/round-1/propose") is not None
    run_images = mo.ui.run_button(label="Compare convolutional and residual predictors", disabled=not bool(get_lab().get("images")) or _locked)
    solar_prerequisite_12 = ui.prerequisite(mo, "Load the image arrays before training.", "data", go_to)
    mo.vstack([mo.Html(ui.step("5. Predict the image, or predict its correction", "Complete ImagePredictor.forward: the residual model should add its predicted correction to the current image. Then finish my_image_mae, run the local check, and click Compare convolutional and residual predictors.", "Compare the two error scores and forecast images below. Where did the prediction miss a change on the solar disk?")), mo.md("**What these images represent.** AIA records the Sun in extreme ultraviolet light. We use its 171 Å channel, sampled every 12 minutes and reduced to 64×64 pixels. Each model sees an image from an hour ago and one from now, then predicts an hour ahead. The score averages absolute error over the solar disk; lower is better."), mo.md("[Inspect the source archive](https://jsoc1.stanford.edu/data/aia/synoptic/README.html) · [Inspect the preprocessing](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)"), image_editor, image_metric_editor, check_images, mo.accordion({"How the images are prepared": mo.md("We divide each image by exposure time, then apply log1p and normalize using training dates only. The fixed score uses this normalized intensity and ignores pixels outside the solar disk. The acquisition link above contains the source checks and preprocessing."), "Hint": mo.md("In the residual model, add `x[:, 1:2]` to the network output. For the metric, average each image’s error over pixels where disk_mask is true, then average the images. An error of +1 everywhere on the disk should score 1; an error outside the disk should score 0."), "Worked answers": mo.md("```python\ndef forward(self, x):\n    prediction = self.net(x)\n    return prediction + x[:, 1:2] if architecture == 'residual' else prediction\n\n" + teaching.IMAGE_METRIC_SOLUTION + "\n```")}), run_images, mo.md("The research agent has already started from your selected manual model. That starting version is now fixed for this comparison.") if _locked else solar_prerequisite_12 if not get_lab().get("images") else mo.md("These image edits are saved separately from your measurement model.")])
    return (check_images, image_editor, image_metric_editor, run_images, solar_prerequisite_11, solar_prerequisite_12,)


@app.cell(hide_code=True)
def _(check_images, checked, image_editor, image_metric_editor, mo, teaching):
    mo.stop(not check_images.value)
    def _check():
        return {"model": teaching.check_model(image_editor.value, "image"), "metric": teaching.check_image_metric(image_metric_editor.value)}
    checked("image-check", _check)
    return


@app.cell(hide_code=True)
def _(get_lab, image_editor, image_metric_editor, mo, refresh_saved, run_images, run_training, teaching):
    mo.stop(not run_images.value)
    teaching.check_model(image_editor.value, "image")
    teaching.check_image_metric(image_metric_editor.value)
    _s = get_lab()["session"]
    for _architecture in ("conv", "residual"):
        _config = {"architecture": _architecture, "width": 8, "learning_rate": .001, "steps": 40, "seed": 17, "batch_size": 8}
        run_training(_s, "images/manual-" + _architecture, image_editor.value, get_lab()["images"], _config, get_lab()["dataset"], image_metric_editor.value)
    _s.checkpoint("images")
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, image_editor, mo, teaching, ui):
    mo.stop(get_step() != "images")
    _s = get_lab().get("session")
    _rows = [] if not _s else [row for row in _s.completed() if row["name"].startswith("images/manual-")]
    _check = get_feedback().get("image-check", {})
    _previews = [mo.image(str(_s.file("outputs/" + row["id"] + "/predictions.png"))) for row in _rows if _s.file("outputs/" + row["id"] + "/predictions.png").exists()]
    solar_next_step_13 = ui.next_step(mo, "Next: let the researcher propose code changes", "research", go_to)
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/image", image_editor.value, stage_prefix="images/manual-")) if _s else mo.md(""), mo.Html(ui.result("Local image checks", _check, status=_check.get("status", "not checked"))) if _check else mo.md("**Your image results.** Saved runs appear below. If you change the code, check it before training again."), mo.ui.table(teaching.metric_rows({row["config"]["architecture"]: row["result"]["metrics"] for row in _rows}), selection=None), *_previews, ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="Pick one forecast where the models differ. Open that model’s files to find weights.pt, then its Agent Lens training span to see the settings and elapsed time. Describe the difference you can see in the error image.") if _s else mo.md(""), solar_next_step_13])
    return (solar_next_step_13,)


@app.cell(hide_code=True)
def _(get_step, mo, ui):
    mo.stop(get_step() not in ("images", "research"))
    mo.vstack([
        mo.callout(mo.vstack([
            mo.md("**Recorded example · a completed rehearsal, separate from your results.**"),
            mo.md("| Frozen image model | Mean error |\n|---|---:|\n| Persistence | 0.12576 |\n| Manual model | 0.12244 |\n| Agent-edited model | 0.11001 |"),
            mo.md("**10.15% lower error than the manual model.** The selected edits zero-initialized the residual output layer and changed training loss to masked L1."),
            mo.md("One seed; 199 overlapping windows on February 13–14, 2014. The GOES measurement model performed worse than persistence. Your results appear in your own comparison.")
        ]), kind="info"),
        mo.accordion({"Open the recorded evidence": mo.Html(ui.links({
            "Recorded result and limitations": "https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==",
            "Actual diffs and execution records": "https://github.com/ash0ts/forge-workshop-kit/blob/main/evidence/ux-v020-solar.json",
            "Selected code and weights": "https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f5e5d198bc9479f78d9a4b1c8c8979e3/v0",
        }))})
    ])
    return


@app.cell
def _(teaching):
    def next_research_action(session):
        # This reads saved decisions. It never launches an action by itself.
        return teaching.next_action(session)

    def choose_adoption(parent, executed):
        # Lower validation error wins. Failed or equal candidates retain the parent.
        if executed.get("metrics", {}).get("validation_error", float("inf")) < parent["metrics"]["validation_error"]:
            return executed
        return parent
    return (choose_adoption, next_research_action,)


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "research")
    _s = get_lab().get("session")
    solar_prerequisite_14 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_14)
    evidence_editor = mo.ui.code_editor(value=_s.get_draft("solar/evidence", teaching.EVIDENCE_STARTER), language="python", min_height=180, label="Implement select_validation_evidence", on_change=lambda value: _s.save_draft("solar/evidence", value))
    check_evidence = mo.ui.run_button(label="Check my evidence selection")
    mo.vstack([mo.Html(ui.step("6. Give the researcher evidence, then inspect its edits", "Now let an agent suggest changes to your image model. Complete select_validation_evidence so it receives the settings, scores, losses, and traces from validation. Check the function, then follow the next action below.", "You’ll review and test two suggestions, ask for a combined or selected version, and test that too. We repeat this for two rounds.")), mo.md("The research agent keeps the same model weights throughout. It edits Python code; your small forecasting models learn new weights when you train each candidate. The agent can change the model or loss, but the data splits and final scorer stay fixed."), evidence_editor, check_evidence, mo.accordion({"Hint": mo.md("Return the fields listed in the starter. Keep the check that rejects split='test': the agent must choose its edits before seeing final-test scores."), "Worked answer": mo.md("```python\n" + teaching.EVIDENCE_SOLUTION + "\n```")})])
    return (check_evidence, evidence_editor, solar_prerequisite_14,)


@app.cell(hide_code=True)
def _(check_evidence, checked, digest, evidence_editor, mo, teaching):
    mo.stop(not check_evidence.value)
    checked("evidence-check", lambda: {**teaching.check_evidence(evidence_editor.value), "source_fingerprint": digest(evidence_editor.value)})
    return


@app.cell(hide_code=True)
def _(digest, evidence_editor, get_feedback, get_lab, get_step, go_to, mo, next_research_action, teaching, ui):
    mo.stop(get_step() != "research")
    _s = get_lab().get("session")
    mo.stop(not _s, mo.md("Connect first."))
    _number, _phase, _label = next_research_action(_s)
    _prefix = f"images/round-{_number}/"
    _proposal = teaching.saved(_s, _prefix + "propose")
    _composition = teaching.saved(_s, _prefix + "compose")
    _candidate = None
    if _phase in ("review-0", "probe-result-0") and _proposal:
        _candidate = _proposal["result"]["candidates"][0]
    elif _phase in ("review-1", "probe-result-1") and _proposal:
        _candidate = _proposal["result"]["candidates"][1]
    elif _phase in ("review-composition", "composition-result") and _composition:
        _candidate = _composition["result"]["decision"]
    _prior = teaching.saved(_s, "images/round-1/adopt")
    _parent = get_lab().get("manual") if _number == 1 else _prior["result"]["adopted"] if _prior else None
    research_note = mo.ui.text_area(value=_s.get_draft("solar/review-" + _prefix + _phase, ""), label="My observation or review note", full_width=True, on_change=lambda value: _s.save_draft("solar/review-" + _prefix + _phase, value))
    _evidence_check = get_feedback().get("evidence-check", {})
    _evidence_ready = _evidence_check.get("status") == "complete" and _evidence_check.get("source_fingerprint") == digest(evidence_editor.value)
    research_button = mo.ui.run_button(label=f"Round {_number}: {_label}", disabled=not bool(_parent and get_lab().get("images")) or _phase == "done" or (_phase == "propose" and not _evidence_ready))
    _explain = {"propose": "Ask the research agent for two code changes. It will use your selected model and validation results.", "review-0": "Read Candidate A’s diff. In your note, name the changed line and what you expect it to do.", "probe-result-0": "Run Candidate A with the same training settings as its starting model. Read its validation error or failure below.", "review-1": "Read Candidate B’s diff and write what it tries to change. B is a separate suggestion from the same starting model.", "probe-result-1": "Run Candidate B on the same data as A. Then you can compare the two suggestions.", "probe-done": "Compare A and B below. Write which result you would keep and point to a score, prediction, or failure.", "compose": "Ask the agent to choose, combine, or reject the two suggestions. You’ll review the resulting code next.", "review-composition": "Read the proposed final diff and write what changed. If it retains the previous version, say why that seems reasonable.", "composition-result": "Run the proposed final version on validation data. Even a combination of good edits needs its own test.", "adopt": "Save the tested version and lesson. The notebook keeps the earlier model if the new one fails or does not lower validation error.", "done": "Both rounds are saved. Continue to Final evaluation to test the selected versions on the reserved dates."}[_phase]
    _parts = [mo.Html(ui.result("Evidence-selection check", _evidence_check, status=_evidence_check.get("status", "not checked"))), mo.Html(ui.step(f"Round {_number} · {_label}", _explain, "Read the result below before moving to the next action."))]
    if _phase == "propose" and not _evidence_ready:
        _parts.append(mo.callout(mo.md("Finish select_validation_evidence above and click Check my evidence selection. Then you can request the first two suggestions."), kind="warn"))
    if _candidate:
        _parts += [mo.Html(ui.result(_candidate.get("title", "Proposed change"), {"Decision": "Retain this version" if _candidate["decision"] == "KEEP" else "Change source", "Agent rationale": _candidate["rationale"]}, detail={"Source fingerprint": _candidate.get("fingerprint")})), mo.Html(ui.diff(_parent["source"], _candidate["source"]))]
    _probe_rows = [teaching.saved(_s, _prefix + "probe-result-" + str(index)) for index in (0, 1)]
    if any(_probe_rows):
        _parts.append(mo.ui.table([{"Candidate": "AB"[index], "Status": "failed" if row["result"].get("errors") else "complete", "Validation error": row["result"].get("metrics", {}).get("validation_error"), "Error": "; ".join(row["result"].get("errors", []))} for index, row in enumerate(_probe_rows) if row], selection=None))
    _parts += [research_note, research_button]
    solar_prerequisite_15 = ui.prerequisite(mo, "Compare the two manual image models first.", "images", go_to)
    solar_prerequisite_16 = ui.prerequisite(mo, "Go to Solar data and click Load the solar dataset to put the images back in memory.", "data", go_to)
    if not _parent:
        _parts.append(solar_prerequisite_15)
    elif not get_lab().get("images"):
        _parts.append(solar_prerequisite_16)
    solar_next_step_17 = ui.next_step(mo, "Next: freeze and evaluate", "final", go_to)
    _parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in (_proposal, _composition) if row], question="Open the proposal in Agent Lens. Find the validation score and code sent to the agent, then compare its explanation with the changed lines below. What does the edit try to fix?"), mo.Html(ui.branch_graph(_s)), solar_next_step_17]
    mo.vstack(_parts)
    return (research_button, research_note, solar_next_step_17, solar_prerequisite_15, solar_prerequisite_16,)


@app.cell
def _(choose_adoption, evidence_editor, get_feedback, get_lab, mo, next_research_action, refresh_saved, research, research_button, research_note, run_training, set_feedback, teaching):
    mo.stop(not research_button.value)
    _s = get_lab()["session"]
    _number, _phase, _label = next_research_action(_s)
    _prefix = f"images/round-{_number}/"
    _prior = teaching.saved(_s, "images/round-1/adopt") if _number == 2 else None
    _parent = get_lab()["manual"] if _number == 1 else {**_prior["result"]["adopted"], "lessons": [{"lesson": _prior["result"].get("lesson"), "limits": _prior["result"].get("limits")}]}
    _metric_source = _s.get_draft("solar/image-metric", teaching.IMAGE_METRIC_SOLUTION)
    teaching.check_image_metric(_metric_source)
    if _phase == "propose":
        teaching.check_evidence(evidence_editor.value)
        _evidence = teaching.functions(evidence_editor.value)["select_validation_evidence"](_parent)
        _proposal, _id = research.propose(_s, _number, _parent["source"], _evidence)
        try:
            research.trace_decision(_s, _id)
        except Exception as _error:
            set_feedback({**get_feedback(), "research-export": str(_error)})
    elif _phase.startswith("review-"):
        mo.stop(not research_note.value.strip(), mo.md("In the review note, name the line that changed and what you expect it to do."))
        _candidate = teaching.saved(_s, _prefix + "compose")["result"]["decision"] if _phase == "review-composition" else teaching.saved(_s, _prefix + "propose")["result"]["candidates"][int(_phase[-1])]
        with _s.stage(_prefix + _phase, sources={"candidate.py": _candidate["source"]}, inputs={"fingerprint": _candidate["fingerprint"]}) as _stage:
            if _stage.needs_run:
                _stage.record({"reviewed_fingerprint": _candidate["fingerprint"], "note": research_note.value})
    elif _phase.startswith("probe-result-") or _phase == "composition-result":
        _is_composition = _phase == "composition-result"
        _index = None if _is_composition else int(_phase[-1])
        _candidate = teaching.saved(_s, _prefix + "compose")["result"]["decision"] if _is_composition else teaching.saved(_s, _prefix + "propose")["result"]["candidates"][_index]
        _review = teaching.saved(_s, _prefix + ("review-composition" if _is_composition else "review-" + str(_index)))
        assert _review["result"]["reviewed_fingerprint"] == _candidate["fingerprint"], "The reviewed source must match the code being executed."
        _name = _prefix + ("composition-test" if _is_composition else "probe-" + str(_index))
        try:
            _executed = run_training(_s, _name, _candidate["source"], get_lab()["images"], _parent["config"], get_lab()["dataset"], _metric_source)
        except Exception as _error:
            _failed = [row for row in _s.read()["stages"].values() if row["name"] == _name]
            _executed = {"stage_id": _failed[-1]["id"] if _failed else None, "source": _candidate["source"], "config": _parent["config"], "split": "validation", "errors": [str(_error)], "metrics": {}}
        with _s.stage(_prefix + _phase, inputs={"candidate_fingerprint": _candidate["fingerprint"]}) as _stage:
            if _stage.needs_run:
                _stage.record({**_executed, "title": _candidate["title"], "rationale": _candidate["rationale"]})
    elif _phase == "probe-done":
        mo.stop(not research_note.value.strip(), mo.md("In the review note, compare A and B using their validation errors or recorded failures."))
        _probes = [teaching.saved(_s, _prefix + "probe-result-" + str(index))["result"] for index in (0, 1)]
        with _s.stage(_prefix + "probe-done", inputs={"probes": _probes}) as _stage:
            if _stage.needs_run:
                _stage.record({"probes": _probes, "participant_comparison": research_note.value})
    elif _phase == "compose":
        _probes = teaching.saved(_s, _prefix + "probe-done")["result"]["probes"]
        _decision, _id = research.compose(_s, _number, _parent["source"], _parent, _probes)
        try:
            research.trace_decision(_s, _id)
        except Exception as _error:
            set_feedback({**get_feedback(), "research-export": str(_error)})
    elif _phase == "adopt":
        _decision = research.normalize_composition(teaching.saved(_s, _prefix + "compose")["result"]["decision"])
        _executed = teaching.saved(_s, _prefix + "composition-result")["result"]
        _adopted = choose_adoption(_parent, _executed)
        with _s.stage(_prefix + "adopt", inputs={"tested": _executed["stage_id"]}) as _stage:
            if _stage.needs_run:
                _stage.record({"adopted": _adopted, "decision": _decision, "retained_parent": _adopted is _parent, "lesson": _decision.get("lesson"), "limits": _decision.get("limits"), "participant_note": research_note.value, "execution_error": _executed.get("errors")})
    _s.checkpoint("research" if next_research_action(_s)[1] == "done" else _prefix + _phase)
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, next_research_action, ui):
    mo.stop(get_step() != "final")
    _s = get_lab().get("session")
    _done = bool(_s) and next_research_action(_s)[1] == "done"
    final_button = mo.ui.run_button(label="Freeze versions and evaluate reserved dates", disabled=not (_done and get_lab().get("images") and get_lab().get("goes")))
    conclusion = mo.ui.text_area(value=_s.get_draft("solar/conclusion", "") if _s else "", label="What changed in your forecast? Link one prediction and the code change behind it.", full_width=True, on_change=lambda value: _s.save_draft("solar/conclusion", value) if _s else None)
    report_button = mo.ui.run_button(label="Publish my conclusion", disabled=not bool(get_lab().get("final")))
    retry_publication = mo.ui.run_button(label="Retry saved exports and comparison publication", disabled=not bool(_s))
    solar_prerequisite_18 = ui.prerequisite(mo, "Finish both research rounds before freezing versions.", "research", go_to)
    solar_prerequisite_19 = ui.prerequisite(mo, "Go to Solar data and click Load the solar dataset before evaluating.", "data", go_to)
    mo.vstack([mo.Html(ui.step("7. Stop choosing. Evaluate the frozen versions.", "Click Freeze versions and evaluate reserved dates. We’ll use the saved weights to compare persistence, your manual image model, and the agent-edited model on February 13–14. We’ll also score your selected GOES model separately.", "Pick one forecast and explain what changed. Then write your conclusion below and click Publish my conclusion.")), final_button, solar_prerequisite_18 if not _done else solar_prerequisite_19 if not get_lab().get("images") else mo.md("These two test days were held back while you chose changes. One seed and overlapping forecast windows make this a teaching result, not evidence of reliable solar forecasting."), conclusion, report_button, mo.accordion({"A trace or comparison did not upload": mo.vstack([mo.md("Your executions and predictions are saved locally. Use the retry button to upload them again without training or calling the research agent. If native EvalTables is unavailable, use the notebook comparison and the published Weave links. Unavailable results stay marked unavailable."), retry_publication])})])
    return (conclusion, final_button, report_button, retry_publication, solar_prerequisite_18, solar_prerequisite_19,)


@app.cell
def _(export_trace, final_button, get_feedback, get_lab, instrument_tool, mo, np, plots, publish_comparison, refresh_saved, research, set_feedback, solar, teaching, time, training):
    mo.stop(not final_button.value)
    mo.output.replace(mo.md("**Evaluating your selected models.** Loading the saved weights and predicting the reserved dates."))
    _s = get_lab()["session"]
    _adopted = teaching.saved(_s, "images/round-2/adopt")["result"]["adopted"]
    _versions = {"manual": get_lab()["manual"], "agent": _adopted}
    _freeze, _freeze_id = research.freeze(_s, _versions, get_lab()["dataset"])
    _test = get_lab()["images"]["test"]
    _comparisons = {"persistence": solar.evaluation_rows(_test["persistence"], _test)}
    _results = {"persistence": solar.score(_test["persistence"], _test)}
    for _label, _version in _versions.items():
        _weights = _s.file("outputs/" + _version["stage_id"] + "/weights.pt")
        with _s.stage("images/final-" + _label, config=_version["config"], sources={"candidate.py": _version["source"]}, inputs={"freeze": _freeze_id, "split": "test"}) as _stage:
            if _stage.needs_run:
                _started = time.time()
                _result, _prediction = training.train(_version["source"], None, _test, _version["config"], _stage.output_dir, weights=_weights)
                _result["events"] = [{"id": _stage.id + "/evaluate", "name": "evaluate_frozen_weights", "arguments": {"freeze": _freeze_id, "source_fingerprint": _stage.source_fingerprint, "trained_stage": _version["stage_id"], "split": "test"}, "result": _result["metrics"], "started_at": _started, "ended_at": time.time()}]
                _figure = plots.forecast(_prediction, _test, title="Frozen " + _label + " on reserved dates")
                _figure.savefig(_stage.output_dir / "predictions.png", dpi=130)
                _stage.record(_result, files=[_stage.output_dir / "predictions.npy", _stage.output_dir / "predictions.png"])
            _prediction = np.load(_stage.output_dir / "predictions.npy")
            try:
                _trace = export_trace(_s, _stage.id, "Evaluate frozen " + _label + " weights on reserved image dates", _stage.result.get("events", []), tool_writer=instrument_tool) if _stage.result.get("events") else {}
            except Exception as _error:
                _trace = {"status": "unavailable", "error": str(_error)}
            _results[_label] = _stage.result["metrics"]
            _comparisons[_label] = solar.evaluation_rows(_prediction, _test, evidence={"stage": _stage.id, "source": _stage.source_fingerprint, "trace": _trace, "training_trace": _version.get("trace", {})})
    with _s.stage("images/final-comparison", inputs={"freeze": _freeze_id}) as _stage:
        if _stage.needs_run:
            _stage.record({"metrics_by_version": _results, "rows": _comparisons})
    # Measurement selection and scoring remain separate from image prediction.
    _goes_runs = [row for row in _s.completed() if row["name"].startswith("goes/search-") and row["inputs"].get("dataset") == get_lab()["dataset"]]
    if _goes_runs:
        _best = min(_goes_runs, key=lambda row: row["result"]["metrics"]["validation_error"])
        _test = get_lab()["goes"]["test"]
        with _s.stage("goes/final", config=_best["config"], sources=_best["sources"], inputs={"selected_stage": _best["id"], "split": "test"}) as _g:
            if _g.needs_run:
                _started = time.time()
                _result, _prediction = training.train(_best["sources"]["candidate.py"], None, _test, _best["config"], _g.output_dir, weights=_s.file("outputs/" + _best["id"] + "/weights.pt"))
                _result["events"] = [{"id": _g.id + "/evaluate", "name": "evaluate_frozen_weights", "arguments": {"trained_stage": _best["id"], "source_fingerprint": _g.source_fingerprint, "split": "test"}, "result": _result["metrics"], "started_at": _started, "ended_at": time.time()}]
                _g.record(_result, files=[_g.output_dir / "predictions.npy"])
            _prediction = np.load(_g.output_dir / "predictions.npy")
            try:
                _goes_trace = export_trace(_s, _g.id, "Evaluate the frozen measurement model on reserved dates", _g.result.get("events", []), tool_writer=instrument_tool) if _g.result.get("events") else {}
            except Exception as _error:
                _goes_trace = {"status": "unavailable", "error": str(_error)}
        with _s.stage("goes/final-comparison", inputs={"selected_stage": _best["id"]}) as _comparison:
            if _comparison.needs_run:
                _comparison.record({"rows": {"persistence": solar.evaluation_rows(_test["persistence"], _test), "selected-model": solar.evaluation_rows(_prediction, _test, evidence={"stage": _g.id, "trace": _goes_trace})}, "metrics_by_version": {"persistence": solar.score(_test["persistence"], _test), "selected-model": _g.result["metrics"]}})
    _s.checkpoint("final")
    refresh_saved()
    # Publication uses saved predictions. Failure does not erase the completed evaluation.
    mo.output.replace(mo.md("**Your predictions and scores are saved.** Uploading the comparisons to Weave and EvalTables. This can take a few minutes."))
    for _name, _label in (("images/final-comparison", "solar-images-final"), ("goes/final-comparison", "solar-measurements-final")):
        _saved = teaching.saved(_s, _name)
        if _saved:
            try:
                with mo.status.spinner(title="Publishing " + _label + " from saved predictions"):
                    publish_comparison(_s, _label, _saved["result"]["rows"])
            except Exception as _error:
                set_feedback({**get_feedback(), "publication": str(_error)})
    refresh_saved()
    mo.output.replace(mo.md("**Your comparison is ready below.** Open the published links, or use the notebook table if a service is unavailable."))
    return


@app.cell(hide_code=True)
def _(conclusion, get_lab, mo, publish_report, refresh_saved, report_button, ui):
    mo.stop(not report_button.value)
    _s = get_lab()["session"]
    _links = {**_s.read()["progress"].get("evidence", {}), **ui.stage_links(_s, [row["id"] for row in _s.completed() if row["name"].startswith(("images/final-", "goes/final", "images/round-"))])}
    for _key, _receipt in _s.read()["publications"].items():
        if _key.startswith("comparison/"):
            _links.update({"Comparison " + label: value["run"] for label, value in _receipt.items() if value.get("run")})
    _url = publish_report(_s, conclusion.value, _links)
    _s.checkpoint("report", evidence={"Report": _url})
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(export_trace, get_feedback, get_lab, instrument_tool, mo, publish_comparison, refresh_saved, research, retry_publication, set_feedback, teaching):
    mo.stop(not retry_publication.value)
    _s = get_lab()["session"]
    _status = _s.retry_publication()
    for _row in _s.completed():
        if _row["result"].get("events") and _row["name"] != "images/final-comparison":
            try:
                if _row["result"].get("request_id"):
                    research.trace_decision(_s, _row["id"])
                else:
                    export_trace(_s, _row["id"], "Inspect saved " + _row["name"], _row["result"]["events"], tool_writer=instrument_tool)
            except Exception as _error:
                _status[_row["name"]] = str(_error)
    for _name, _label in (("images/final-comparison", "solar-images-final"), ("goes/final-comparison", "solar-measurements-final")):
        _saved = teaching.saved(_s, _name)
        if _saved:
            try:
                _status[_label] = publish_comparison(_s, _label, _saved["result"]["rows"])
            except Exception as _error:
                _status[_label] = str(_error)
    set_feedback({**get_feedback(), "publication_retry": _status})
    refresh_saved()
    return


@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching, ui):
    mo.stop(get_step() != "final")
    _s = get_lab().get("session")
    mo.stop(not _s, mo.md("Connect first."))
    _image = teaching.saved(_s, "images/final-comparison")
    _measurement = teaching.saved(_s, "goes/final-comparison")
    _parts = [mo.md("### Final image errors")]
    if _image:
        _parts.append(mo.ui.table(teaching.metric_rows(_image["result"]["metrics_by_version"]), selection=None))
        for _row in _s.completed():
            if _row["name"] in ("images/final-manual", "images/final-agent"):
                _path = _s.file("outputs/" + _row["id"] + "/predictions.png")
                if _path.exists():
                    _parts.append(mo.image(str(_path)))
    else:
        _parts.append(mo.md("Run the frozen comparison above to see your final image scores."))
    _parts.append(mo.md("### Final measurement errors"))
    if _measurement:
        _parts.append(mo.ui.table(teaching.metric_rows(_measurement["result"]["metrics_by_version"]), selection=None))
    elif get_lab().get("goes_final"):
        _parts.append(mo.Html(ui.result("Restored measurement evaluation", get_lab()["goes_final"])))
    else:
        _parts.append(mo.md("Your final GOES scores will appear here. We keep them separate because measurement and image errors use different units."))
    _parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in _s.completed() if row["name"] in ("images/final-manual", "images/final-agent", "images/final-comparison", "goes/final", "goes/final-comparison")], extra=_s.read()["progress"].get("evidence", {}), question="Choose the same forecast timestamp in each version. Compare its predicted image and error, then follow the code and trace links. Which visible difference supports your conclusion?"), ui.publication(mo, _s), mo.md("**Optional ARIA investigation:** Review my Report and linked research-agent traces. Identify one supported reason a change helped or hurt, cite the exact event and prediction, and propose one next experiment. Do not launch new runs.")]
    mo.vstack(_parts)
    return

if __name__ == "__main__":
    app.run()
