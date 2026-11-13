"""Authored Solar notebook cells. Generated notebook files are not edited by hand."""
from pathlib import Path
from notebook_builder import Cell
ROOT = Path(__file__).resolve().parents[1]
DEFAULT = (ROOT / "examples/solar/candidate.py").read_text()
cells = []

def add(code, hide=False):
    cells.append(Cell(code, hide=hide))

add('''
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
get_step, set_step = mo.state("setup")
''', True)
add('''
mo.Html(ui.heading("Build a research loop, then give it an agent", "Pending, Inc. has requested a solar forecast. Management would also like to know which experiment produced it. Build the forecast, preserve the evidence, then let an agent propose changes to your research code."))
''', True)
add('''
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
''', True)
add('''
_s = get_lab().get("session")
solar_navigation = ui.navigation(mo, teaching.STEPS, get_step(), go_to, completed=teaching.completed_steps(_s) if _s else ())
mo.vstack([solar_navigation, mo.Html(ui.context(_s)) if _s else mo.md("**Your notebook, your project.** Start with the access check. Opening this notebook does not train models or call inference.")])
''', True)
add('''
help_message = mo.ui.text_area(label="What do you need help with?", full_width=True)
help_button = mo.ui.run_button(label="Send a help request", disabled=not bool(get_lab().get("session")))
mo.accordion({"Ask the facilitator": mo.vstack([help_message, help_button, mo.md("This saves a request to your project. It does not give anyone control of your notebook.")])})
''', True)
add('''
mo.stop(not help_button.value)
get_lab()["session"].request_help(help_message.value)
mo.md("Help request saved. Send an empty message when it is resolved.")
''', True)
add('''
mo.stop(get_step() != "setup")
_default = os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None, [os.getenv("WANDB_ENTITY"), os.getenv("WANDB_PROJECT")]))
project_input = mo.ui.text(value=_default, placeholder="your-name/solar-research", label="Your Forge project", full_width=True)
allowance = mo.ui.number(value=8, start=.01, stop=1000, label="Inference allowance in USD; notebook compute is separate")
connect_button = mo.ui.run_button(label="Connect and restore my work")
mo.vstack([mo.Html(ui.step("1. Connect to your own project", "Copy this notebook into your writable Forge project. Hosted Forge supplies authentication. On a laptop, run uv run wandb login first.", "Your project passes a write check. No training or model request runs during setup.")), project_input, allowance, connect_button])
''', True)
add('''
mo.stop(not connect_button.value)
try:
    _s = WorkshopSession.from_environment("solar-autoresearch", project=project_input.value, budget_usd=allowance.value)
    _access = _s.check_access()
    _restored = _s.restore()
    set_lab(teaching.restore_state(_s))
    set_step(_s.get_view("setup"))
    set_feedback({**get_feedback(), "setup": {"status": "complete", **_access, "restore": _restored}})
except Exception as _error:
    set_feedback({**get_feedback(), "setup": {"status": "unavailable", "message": str(_error), "next": "Check project write access and account login. No training has run."}})
''', True)
add('''
_s = get_lab().get("session")
instrumentation_editor = mo.ui.code_editor(value=_s.get_draft("solar/instrumentation", teaching.INSTRUMENTATION_STARTER) if _s else teaching.INSTRUMENTATION_STARTER, language="python", on_change=lambda value: _s.save_draft("solar/instrumentation", value) if _s else None, debounce=False)
check_instrumentation = mo.ui.run_button(label="Check my tracing code")
mo.vstack([mo.md("**Instrument the operation.** Add a `workshop.exercise` attribute with value `solar-research` inside the Tool scope. This writer will also instrument your training calls. The local check exports nothing."), instrumentation_editor, check_instrumentation, mo.accordion({"Hint": mo.md("Call `tool.set_attributes` inside the `with tracing.Tool(...)` block. Keep the arguments, result, timestamps, and error handling."), "Worked answer": mo.md("```python\\n" + teaching.INSTRUMENTATION_SOLUTION + "\\n```")})]) if get_step() == "setup" else mo.md("")
''', True)
add('''
# The edited function below is the writer used by every export in this notebook.
def instrument_tool(observation):
    return teaching.functions(instrumentation_editor.value)["instrument_tool"](observation)
''')
add('''
mo.stop(not check_instrumentation.value)
try:
    _result = teaching.check_instrumentation(instrumentation_editor.value)
    set_tracing_check({"status": "complete", **_result, "source": digest(instrumentation_editor.value)})
except Exception as _error:
    set_tracing_check({"status": "needs work", "message": str(_error)})
''', True)
add('''
mo.stop(get_step() != "setup")
_s = get_lab().get("session")
_checked = get_tracing_check()
first_trace = mo.ui.run_button(label="Send my first Agent Lens trace", disabled=not bool(_s) or _checked.get("source") != digest(instrumentation_editor.value))
_setup = get_feedback().get("setup", {})
solar_next_step_2 = ui.next_step(mo, "Next: inspect the solar data", "data", go_to)
mo.vstack([mo.Html(ui.result("Connection", _setup, status=_setup.get("status", "not checked"))) if _setup else mo.md("**Connection: not checked yet.** Enter your project and click Connect above."), mo.Html(ui.result("Local tracing check", _checked, status=_checked.get("status", "not checked"))) if _checked else mo.md("**Next:** edit the tracing function, then click **Check my tracing code**."), mo.md("Send the checked operation, then open Agent Lens and inspect the actual arguments, result, timing, and your attribute."), first_trace, ui.evidence(mo, _s, stage_ids=[teaching.saved(_s, "setup/trace")["id"]] if _s and teaching.saved(_s, "setup/trace") else (), question="Does the environment tool's result match the receipt? Find your workshop.exercise attribute.") if _s else mo.md("Connect above first."), solar_next_step_2])
''', True)
add('''
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
    set_feedback({**get_feedback(), "setup_trace": {"status": "publication pending", "message": str(_error), "next": "Click the trace button again to retry export of the saved operation. It sends no model request."}})
refresh_saved()
''', True)
add('''
mo.stop(get_step() != "setup")
_status = get_feedback().get("setup_trace", {})
_s = get_lab().get("session")
_saved = teaching.saved(_s, "setup/trace") if _s else None
_receipt = _s.read()["publications"].get("trace/" + _saved["id"], {}) if _saved else {}
if not _status and _receipt.get("verified"):
    _status = {"status": "complete", "stored spans": _receipt["stored_spans"], "result": "Restored verified trace; no operation repeated."}
mo.Html(ui.result("Trace readback", _status, status=_status.get("status", "not sent"))) if _status else mo.md("**Trace: not sent yet.** Check your code, then send the operation above.")
''', True)
add('''
mo.stop(get_step() != "data")
_s = get_lab().get("session")
load_data = mo.ui.run_button(label="Load the solar dataset", disabled=not bool(_s))
solar_prerequisite_3 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
mo.vstack([mo.Html(ui.step("2. Inspect the observations", "Load the pinned GOES-15 measurements and AIA 171 Å images. Read one SunPy FITS record and the date partitions before building a model.", "Train: February 1–10, 2014. Validation: 11–12. Final evaluation: 13–14. Gaps remain gaps; the future is not a feature.")), load_data, solar_prerequisite_3 if not _s else mo.md("The combined teaching data is about 26 MB. Loading it trains nothing."), mo.accordion({"What is reserved?": mo.md("We construct windows inside date partitions, reject gaps, and fit normalization only on training dates. February 8 is absent from the GOES source archive. The researcher sees training and validation evidence. Final dates are used only after versions are frozen."), "Inspect the acquisition code": mo.md("[Source, quality checks and preprocessing](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)")})])
''', True)
add('''
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
''', True)
add('''
mo.stop(get_step() != "data")
_s = get_lab().get("session")
_record = teaching.saved(_s, "data/loaded") if _s else None
solar_next_step_4 = ui.next_step(mo, "Next: implement persistence", "baseline", go_to)
mo.vstack([mo.Html(ui.result("Dataset loaded", _record["result"])) if _record else mo.md("Load the data to see its fingerprint, dates, and development-window counts."), plots.forecast(get_lab()["goes"]["validation"]["persistence"], get_lab()["goes"]["validation"], title="Validation measurements: the latest observation as a forecast") if get_lab().get("goes") else mo.md("Reopening restores receipts. Click Load the solar dataset to restore arrays; this does not repeat training."), ui.evidence(mo, _s, stage_ids=[_record["id"]], question="Find the exact dataset fingerprint recorded with this workspace.") if _record else mo.md(""), solar_next_step_4])
''', True)
add('''
mo.stop(get_step() != "baseline")
_s = get_lab().get("session")
solar_prerequisite_5 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
mo.stop(not _s, solar_prerequisite_5)
persistence_editor = mo.ui.code_editor(value=_s.get_draft("solar/persistence", teaching.PERSISTENCE_STARTER), language="python", min_height=130, label="Implement persistence_forecast", on_change=lambda value: _s.save_draft("solar/persistence", value))
check_persistence = mo.ui.run_button(label="Check my persistence function")
baseline_button = mo.ui.run_button(label="Run my persistence baseline", disabled=not bool(get_lab().get("goes")))
solar_prerequisite_6 = ui.prerequisite(mo, "Load the dataset before running the baseline.", "data", go_to)
mo.vstack([mo.Html(ui.step("3. Predict the current measurement again", "Replace the exception in persistence_forecast. Return the latest observation for each window without reading its future target.", "The local check passes, then the validation forecast appears below. This baseline makes no inference call.")), persistence_editor, check_persistence, mo.accordion({"Hint": mo.md("The loader supplies the latest observation in split['persistence']. Return a copy so predictions cannot overwrite the data."), "Worked answer": mo.md("```python\\n" + teaching.PERSISTENCE_SOLUTION + "\\n```")}), baseline_button, solar_prerequisite_6 if not get_lab().get("goes") else mo.md("Draft edits save locally. The Run button executes the code currently shown.")])
''', True)
add('''
mo.stop(not check_persistence.value)
checked("persistence-check", lambda: teaching.check_persistence(persistence_editor.value))
''', True)
add('''
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
''', True)
add('''
mo.stop(get_step() != "baseline")
_s = get_lab().get("session")
_row = teaching.saved(_s, "goes/persistence") if _s else None
_check = get_feedback().get("persistence-check", {})
solar_next_step_7 = ui.next_step(mo, "Next: track six model configurations", "search", go_to)
mo.vstack([mo.md(teaching.draft_status(_s, "solar/persistence", persistence_editor.value)) if _s else mo.md(""), mo.Html(ui.result("Local function check", _check, status=_check.get("status", "not checked"))), mo.Html(ui.result("Persistence validation result", _row["result"].get("metrics", {}))) if _row else mo.md("Run your checked function to save the baseline."), ui.evidence(mo, _s, stage_ids=[_row["id"]], question="Find the exact function source and validation score. Which dates did it use?") if _row else mo.md(""), solar_next_step_7])
''', True)
add('''
DEFAULT_SOURCE = ''' + repr(DEFAULT) + '''
''', True)
add('''
mo.stop(get_step() != "search")
_s = get_lab().get("session")
solar_prerequisite_8 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
mo.stop(not _s, solar_prerequisite_8)
measurement_editor = mo.ui.code_editor(value=_s.get_draft("solar/measurement", teaching.model_starter(DEFAULT_SOURCE, "measurement")), language="python", min_height=320, max_height=650, label="Measurement model source: complete training_loss", on_change=lambda value: _s.save_draft("solar/measurement", value))
flux_metric_editor = mo.ui.code_editor(value=_s.get_draft("solar/flux-metric", teaching.FLUX_STARTER), language="python", min_height=120, label="Implement my_flux_mae", on_change=lambda value: _s.save_draft("solar/flux-metric", value))
check_measurement = mo.ui.run_button(label="Check my measurement code")
run_search = mo.ui.run_button(label="Run six tracked configurations", disabled=not bool(get_lab().get("goes")) or teaching.saved(_s, "images/freeze") is not None)
solar_prerequisite_9 = ui.prerequisite(mo, "Load the dataset before training.", "data", go_to)
mo.vstack([mo.Html(ui.step("4. Record the experiment before comparing it", "Implement masked mean squared training loss and log-flux MAE. Read run_training below: your source, configuration, dataset and predictions identify each experiment.", "Two free local checks pass. The search produces three MLP and three temporal-CNN runs with the same date partitions.")), measurement_editor, flux_metric_editor, check_measurement, mo.accordion({"Hint": mo.md("Training loss: square the residual, multiply by the mask, sum, and divide by the mask sum. The evaluation metric uses absolute error instead."), "Worked answers": mo.md("```python\\ndef training_loss(prediction, target, mask):\\n    return ((prediction - target).square() * mask).sum() / mask.sum()\\n\\n" + teaching.FLUX_SOLUTION + "\\n```"), "Why this is a search": mo.md("Six fixed configurations choose mlp/cnn, width, and learning rate. They do not write new model code. All use seed 17, 60 steps, and batch size 32.")}), run_search, solar_prerequisite_9 if not get_lab().get("goes") else mo.md("This trains on notebook CPU. Reusing an identical configuration returns its saved execution.")])
''', True)
add('''
mo.stop(not check_measurement.value)
def _check():
    return {"model": teaching.check_model(measurement_editor.value, "measurement"), "metric": teaching.check_flux_metric(flux_metric_editor.value)}
checked("measurement-check", _check)
''', True)
add('''
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
''')
add('''
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
''')
add('''
mo.stop(get_step() != "search")
_s = get_lab().get("session")
_rows = [] if not _s else [row for row in _s.completed() if row["name"].startswith("goes/search-")]
_check = get_feedback().get("measurement-check", {})
solar_next_step_10 = ui.next_step(mo, "Next: predict a solar image", "images", go_to)
mo.vstack([mo.md(teaching.draft_status(_s, "solar/measurement", measurement_editor.value, stage_prefix="goes/search-")) if _s else mo.md(""), mo.Html(ui.result("Local measurement checks", _check, status=_check.get("status", "not checked"))), mo.ui.table([{"Run": row["name"], "Architecture": row["config"]["architecture"], "Width": row["config"]["width"], "Learning rate": row["config"]["learning_rate"], **row["result"]["metrics"]} for row in _rows], selection=None), ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="In the Sweep, compare one MLP and one CNN. Can you recover the data version, learning curve and source behind each score?") if _s else mo.md(""), solar_next_step_10])
''', True)
add('''
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
mo.vstack([mo.Html(ui.step("5. Predict the image, or predict its correction", "Complete ImagePredictor.forward and the disk-masked image metric. The two input channels are the image from an hour ago and the current image.", "A constant +1 valid-pixel error scores 1; an off-disk error scores 0. Both architectures return one future image.")), image_editor, image_metric_editor, check_images, mo.accordion({"Hint": mo.md("For the residual architecture, add x[:, 1:2], the current image, to the network output. Average the metric over valid pixels per image, then over images."), "Worked answers": mo.md("```python\\ndef forward(self, x):\\n    prediction = self.net(x)\\n    return prediction + x[:, 1:2] if architecture == 'residual' else prediction\\n\\n" + teaching.IMAGE_METRIC_SOLUTION + "\\n```")}), run_images, mo.md("The manual parent is fixed once the first research proposal exists. Your draft remains editable; it will not replace that parent.") if _locked else solar_prerequisite_12 if not get_lab().get("images") else mo.md("Image and measurement drafts are independent. Changes here do not overwrite the earlier model.")])
''', True)
add('''
mo.stop(not check_images.value)
def _check():
    return {"model": teaching.check_model(image_editor.value, "image"), "metric": teaching.check_image_metric(image_metric_editor.value)}
checked("image-check", _check)
''', True)
add('''
mo.stop(not run_images.value)
teaching.check_model(image_editor.value, "image")
teaching.check_image_metric(image_metric_editor.value)
_s = get_lab()["session"]
for _architecture in ("conv", "residual"):
    _config = {"architecture": _architecture, "width": 8, "learning_rate": .001, "steps": 40, "seed": 17, "batch_size": 8}
    run_training(_s, "images/manual-" + _architecture, image_editor.value, get_lab()["images"], _config, get_lab()["dataset"], image_metric_editor.value)
_s.checkpoint("images")
refresh_saved()
''', True)
add('''
mo.stop(get_step() != "images")
_s = get_lab().get("session")
_rows = [] if not _s else [row for row in _s.completed() if row["name"].startswith("images/manual-")]
_check = get_feedback().get("image-check", {})
_previews = [mo.image(str(_s.file("outputs/" + row["id"] + "/predictions.png"))) for row in _rows if _s.file("outputs/" + row["id"] + "/predictions.png").exists()]
solar_next_step_13 = ui.next_step(mo, "Next: let the researcher propose code changes", "research", go_to)
mo.vstack([mo.md(teaching.draft_status(_s, "solar/image", image_editor.value, stage_prefix="images/manual-")) if _s else mo.md(""), mo.Html(ui.result("Local image checks", _check, status=_check.get("status", "not checked"))) if _check else mo.md("**Image validation results.** Saved runs are restored below. Check your code again before running an edited version."), mo.ui.table(teaching.metric_rows({row["config"]["architecture"]: row["result"]["metrics"] for row in _rows}), selection=None), *_previews, ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="Open the weights artifact and its training trace. Inspect a prediction's error image before calling either model better.") if _s else mo.md(""), solar_next_step_13])
''', True)
add('''
def next_research_action(session):
    # This reads saved decisions. It never launches an action by itself.
    return teaching.next_action(session)

def choose_adoption(parent, executed):
    # Lower validation error wins. Failed or equal candidates retain the parent.
    if executed.get("metrics", {}).get("validation_error", float("inf")) < parent["metrics"]["validation_error"]:
        return executed
    return parent
''')
add('''
mo.stop(get_step() != "research")
_s = get_lab().get("session")
solar_prerequisite_14 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
mo.stop(not _s, solar_prerequisite_14)
evidence_editor = mo.ui.code_editor(value=_s.get_draft("solar/evidence", teaching.EVIDENCE_STARTER), language="python", min_height=180, label="Implement select_validation_evidence", on_change=lambda value: _s.save_draft("solar/evidence", value))
check_evidence = mo.ui.run_button(label="Check my evidence selection")
mo.vstack([mo.Html(ui.step("6. Give the researcher evidence, then inspect its edits", "Implement select_validation_evidence. The fixed research agent writes code; the forecasting models still train normally. Review and test each branch before composing.", "Two candidates per round, two rounds. The adopted source must match a completed execution. A longer procedure is allowed to lose.")), evidence_editor, check_evidence, mo.accordion({"Hint": mo.md("Use an explicit field allowlist. Keep validation metrics, settings, losses, the trace, and the supporting stage identity. Reject split='test'."), "Worked answer": mo.md("```python\\n" + teaching.EVIDENCE_SOLUTION + "\\n```")})])
''', True)
add('''
mo.stop(not check_evidence.value)
checked("evidence-check", lambda: {**teaching.check_evidence(evidence_editor.value), "source_fingerprint": digest(evidence_editor.value)})
''', True)
add('''
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
_explain = {"propose": "Ask for two competing code changes using the selected manual model and validation evidence.", "review-0": "Read Candidate A's actual diff. Record what behavior it intends to change before confirming.", "probe-result-0": "Train the reviewed Candidate A with the parent's settings. Its failure remains evidence.", "review-1": "Read Candidate B's actual diff. It is an independent alternative to A.", "probe-result-1": "Train the reviewed Candidate B on the same training and validation partitions.", "probe-done": "Compare the probes below. Record which evidence supports your recommendation.", "compose": "Ask the researcher to retain, select, or combine the tested changes.", "review-composition": "Inspect the composition's diff. A composed source has not won until it is tested.", "composition-result": "Train the reviewed composition. This does not use final-test dates.", "adopt": "Save the tested winner and the researcher's lesson. Equal or worse validation error retains the parent.", "done": "Both rounds are saved. Freeze the versions before inspecting final dates."}[_phase]
_parts = [mo.Html(ui.result("Evidence-selection check", _evidence_check, status=_evidence_check.get("status", "not checked"))), mo.Html(ui.step(f"Round {_number} · {_label}", _explain, "Only this button performs the named action. Navigation and code edits run nothing."))]
if _phase == "propose" and not _evidence_ready:
    _parts.append(mo.callout(mo.md("Complete select_validation_evidence above, then click Check my evidence selection. No inference can run until that check passes for this code."), kind="warn"))
if _candidate:
    _parts += [mo.Html(ui.result(_candidate.get("title", "Proposed change"), {"Decision": "Retain this version" if _candidate["decision"] == "KEEP" else "Change source", "Agent rationale": _candidate["rationale"], "Source fingerprint": _candidate.get("fingerprint")})), mo.Html(ui.diff(_parent["source"], _candidate["source"]))]
_probe_rows = [teaching.saved(_s, _prefix + "probe-result-" + str(index)) for index in (0, 1)]
if any(_probe_rows):
    _parts.append(mo.ui.table([{"Candidate": "AB"[index], "Status": "failed" if row["result"].get("errors") else "complete", "Validation error": row["result"].get("metrics", {}).get("validation_error"), "Error": "; ".join(row["result"].get("errors", []))} for index, row in enumerate(_probe_rows) if row], selection=None))
_parts += [research_note, research_button]
solar_prerequisite_15 = ui.prerequisite(mo, "Compare the two manual image models first.", "images", go_to)
solar_prerequisite_16 = ui.prerequisite(mo, "Restore the image arrays with Load the solar dataset. Saved work will be reused.", "data", go_to)
if not _parent:
    _parts.append(solar_prerequisite_15)
elif not get_lab().get("images"):
    _parts.append(solar_prerequisite_16)
solar_next_step_17 = ui.next_step(mo, "Next: freeze and evaluate", "final", go_to)
_parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in (_proposal, _composition) if row], question="What evidence did the researcher read? Does the proposed diff address that evidence?"), mo.Html(ui.branch_graph(_s)), solar_next_step_17]
mo.vstack(_parts)
''', True)
add('''
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
    mo.stop(not research_note.value.strip(), mo.md("Write one sentence about the diff before confirming this review."))
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
    mo.stop(not research_note.value.strip(), mo.md("Record one comparison of the two probes before continuing."))
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
''')
add('''
mo.stop(get_step() != "final")
_s = get_lab().get("session")
_done = bool(_s) and next_research_action(_s)[1] == "done"
final_button = mo.ui.run_button(label="Freeze versions and evaluate reserved dates", disabled=not (_done and get_lab().get("images") and get_lab().get("goes")))
conclusion = mo.ui.text_area(value=_s.get_draft("solar/conclusion", "") if _s else "", label="What did your changes do? Cite one prediction, run, and code change.", full_width=True, on_change=lambda value: _s.save_draft("solar/conclusion", value) if _s else None)
report_button = mo.ui.run_button(label="Publish my conclusion", disabled=not bool(get_lab().get("final")))
retry_publication = mo.ui.run_button(label="Retry saved exports and comparison publication", disabled=not bool(_s))
solar_prerequisite_18 = ui.prerequisite(mo, "Finish both research rounds before freezing versions.", "research", go_to)
solar_prerequisite_19 = ui.prerequisite(mo, "Load the dataset to restore arrays. Completed training will not repeat.", "data", go_to)
mo.vstack([mo.Html(ui.step("7. Stop choosing. Evaluate the frozen versions.", "Compare persistence, the selected manual model, and the adopted agent model on reserved dates. Source and trained weights are frozen before this comparison.", "Keep image and measurement metrics separate. Inspect an error image. A failed or worse model still belongs in the result.")), final_button, solar_prerequisite_18 if not _done else solar_prerequisite_19 if not get_lab().get("images") else mo.md("Final evaluation loads saved weights. It does not retrain them."), conclusion, report_button, retry_publication])
''', True)
add('''
mo.stop(not final_button.value)
mo.output.replace(mo.md("**Evaluating the frozen versions.** Loading saved weights; no model is being retrained."))
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
mo.output.replace(mo.md("**Evaluation complete and saved.** Publishing matching predictions to Weave and EvalTables. This may take a few minutes; it sends no inference requests."))
for _name, _label in (("images/final-comparison", "solar-images-final"), ("goes/final-comparison", "solar-measurements-final")):
    _saved = teaching.saved(_s, _name)
    if _saved:
        try:
            with mo.status.spinner(title="Publishing " + _label + " from saved predictions"):
                publish_comparison(_s, _label, _saved["result"]["rows"])
        except Exception as _error:
            set_feedback({**get_feedback(), "publication": str(_error)})
refresh_saved()
mo.output.replace(mo.md("**Evaluation saved. Publication finished.** The tables below distinguish available Weave results from any unavailable native comparison. Publication retries reuse these saved predictions."))
''')
add('''
mo.stop(not report_button.value)
_s = get_lab()["session"]
_links = {**_s.read()["progress"].get("evidence", {}), **ui.stage_links(_s, [row["id"] for row in _s.completed() if row["name"].startswith(("images/final-", "goes/final", "images/round-"))])}
for _key, _receipt in _s.read()["publications"].items():
    if _key.startswith("comparison/"):
        _links.update({"Comparison " + label: value["run"] for label, value in _receipt.items() if value.get("run")})
_url = publish_report(_s, conclusion.value, _links)
_s.checkpoint("report", evidence={"Report": _url})
refresh_saved()
''', True)
add('''
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
''', True)
add('''
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
    _parts.append(mo.md("No final image evaluation has run."))
_parts.append(mo.md("### Final measurement errors"))
if _measurement:
    _parts.append(mo.ui.table(teaching.metric_rows(_measurement["result"]["metrics_by_version"]), selection=None))
elif get_lab().get("goes_final"):
    _parts.append(mo.Html(ui.result("Restored measurement evaluation", get_lab()["goes_final"])))
else:
    _parts.append(mo.md("No final measurement evaluation has run. Measurement error is not averaged with image error."))
_parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in _s.completed() if row["name"] in ("images/final-manual", "images/final-agent", "images/final-comparison", "goes/final", "goes/final-comparison")], extra=_s.read()["progress"].get("evidence", {}), question="Align one prediction across versions. Follow its source and trace, then state what the image actually changed."), ui.publication(mo, _s), mo.md("**Optional ARIA investigation:** Review my Report and linked research-agent traces. Identify one supported reason a change helped or hurt, cite the exact event and prediction, and propose one next experiment. Do not launch new runs.")]
mo.vstack(_parts)
''', True)
