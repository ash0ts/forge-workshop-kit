"""Build editable notebooks from authored cells; hosted/local use the same source."""
import json
from pathlib import Path
from notebook_builder import Cell, render
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=(ROOT/'examples/solar/candidate.py').read_text()


def save(name,title,cells):
    header=f'''# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.1.0/forge_workshop_kit-0.1.0-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }}]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title={title!r})
'''
    (ROOT/'notebooks'/name).write_text(header+render(cells)+'\nif __name__ == "__main__":\n    app.run()\n')

cells=[]
def add(code,hide=False):
    cells.append(Cell(code,hide=hide))
add('''
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
''',True)
add('''
mo.Html(ui.heading("Build a research loop, then give it an agent", "Start with solar measurements. Move to images. Track what you changed, then let an agent propose and test changes to your research code. Your notebook, runs and evidence belong to your project."))
''',True)
add('''
chapter = mo.ui.radio(["1 · Connect", "2 · Data and baseline", "3 · Track and search", "4 · Solar images", "5 · Research agent", "6 · Final evaluation"], value="1 · Connect", inline=True, label="Current exercise")
chapter
''',True)
add('''
help_message=mo.ui.text_area(label="What do you need help with?",full_width=True)
help_button=mo.ui.run_button(label="Send a help request to the progress monitor",disabled=not bool(get_lab().get("session")))
mo.accordion({"Ask the facilitator for help":mo.vstack([help_message,help_button])})
''',True)
add('''
mo.stop(not help_button.value)
get_lab()["session"].request_help(help_message.value)
mo.md("Help request saved to your project. Clear the text and send again when resolved.")
''')
add('''
mo.stop(chapter.value != "1 · Connect")
_default = os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")]))
project_input = mo.ui.text(value=_default, placeholder="your-name/solar-research", label="Your Forge project",full_width=True)
allowance=mo.ui.number(value=8,start=.01,stop=1000,label="My inference allowance (USD); notebook compute is separate")
connect_button = mo.ui.run_button(label="Connect and restore my saved work")
mo.vstack([mo.Html(ui.step("1. Start in your own project", "Copy this notebook into a public teaching project. Hosted Forge supplies authentication. On a laptop, run wandb login and enter entity/project here.", "Your own project appears below. This check sends no model requests.")), project_input, allowance, connect_button])
''',True)
add('''
mo.stop(not connect_button.value)
try:
    _session=WorkshopSession.from_environment("solar-autoresearch",project=project_input.value,budget_usd=allowance.value)
    _access=_session.check_access()
    _restore=_session.restore()
    set_lab({"session":_session})
    set_feedback({**get_feedback(),"setup":{**_access,"restore":_restore}})
except Exception as _error:
    set_feedback({**get_feedback(),"setup":{"error":str(_error),"next":"Check project write access and your account login; no training has run."}})
''')
add('''
mo.stop(chapter.value != "1 · Connect")
first_trace=mo.ui.run_button(label="Send my first Agent Lens trace",disabled=not bool(get_lab().get("session")))
mo.vstack([mo.md(str(get_feedback().get("setup","Connect first."))),first_trace])
''',True)
add('''
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
''')
add('''
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
''')
add('''
mo.stop(chapter.value != "1 · Connect")
mo.vstack([mo.Html(ui.links({"Open my first conversation":get_feedback().get("trace",{}).get("url","")})),mo.md("Next: **2 · Data and baseline**. Keep Agent Lens open beside the notebook.")])
''',True)
add('''
# Exercise: use the most recent observed value as the future prediction.
# Replace the exception with: return split["persistence"].copy()
def persistence_forecast(split):
    raise NotImplementedError("Return the latest observation for each forecast window.")
''')
add('''
mo.stop(chapter.value != "2 · Data and baseline")
load_data=mo.ui.run_button(label="Load the versioned solar observations",disabled=not bool(get_lab().get("session")))
baseline_button=mo.ui.run_button(label="Check and run my persistence baseline",disabled=not bool(get_lab().get("goes")))
mo.vstack([mo.Html(ui.step("2. Use the current flux as a forecast", "Implement persistence_forecast in the code cell. Inspect the data before fitting a model. Missing observations are gaps, not zeros.","Every window stays inside its partition; the baseline predicts the last observed value.")),load_data,baseline_button,
mo.accordion({"Hint":"The loader supplies the latest observation as split['persistence']. Copy it so the exercise does not modify the data.","Data contract":"GOES-15 and AIA 171 Å, February 1–14, 2014. Train: 1–10; validation: 11–12; final test: 13–14. Normalization uses training data only. February 8 is missing from the GOES archive."})])
''',True)
add('''
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
''')
add('''
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
''')
add('''
mo.stop(chapter.value != "2 · Data and baseline")
mo.vstack([mo.md(str(get_feedback().get("data","Load data first."))),mo.md(str(get_feedback().get("baseline","Run your baseline, then open 3 · Track and search."))),plots.forecast(get_lab()["goes"]["validation"]["persistence"],get_lab()["goes"]["validation"],title="Persistence on validation dates") if get_lab().get("goes") else mo.md("")])
''',True)
add('''
# Edit this source in the code editor below. This exact text is fingerprinted and executed.
# Try changing training_loss or a layer; explain which behavior you expect to change.
DEFAULT_SOURCE = '''+repr(DEFAULT)+'''
''')
add('''
mo.stop(chapter.value not in ("3 · Track and search","4 · Solar images"))
_drafts=[s for s in get_lab()["session"].completed() if s["name"]=="draft/model"] if get_lab().get("session") else []
_saved_source=_drafts[-1]["sources"]["candidate.py"] if _drafts else DEFAULT_SOURCE
source_editor=mo.ui.code_editor(value=_saved_source,language="python",min_height=300,max_height=650,label="Model and training code that will execute")
save_source=mo.ui.run_button(label="Save my code before training or switching exercises")
mo.vstack([source_editor,save_source])
''',True)
add('''
mo.stop(not save_source.value)
_s=get_lab()["session"]
with _s.stage("draft/model",sources={"candidate.py":source_editor.value}) as _draft:
    if _draft.needs_run: _draft.record({"saved":True})
_s.checkpoint("code-saved")
mo.md("Code saved locally and queued for artifact publication. This did not train a model.")
''')
add('''
# Implement these development metrics. Test them on the persistence forecast first.
# A constant +1 error should return 1.0; changing an off-disk pixel should not affect image error.
def my_flux_mae(prediction, target):
    return float(np.abs(prediction-target).mean())

def my_image_mae(prediction, target, disk_mask):
    errors=np.abs(prediction-target)*disk_mask
    return float((errors.sum(axis=(1,2,3))/disk_mask.sum(axis=(1,2,3))).mean())
''')
add('''
def run_training(session, name, source, splits, config, data_fingerprint):
    # This is the tracking contract. Source, split, data and settings identify a run.
    with session.stage(name, config=config, sources={"candidate.py":source},
                       inputs={"dataset":data_fingerprint,"split":"validation"}) as stage:
        if stage.needs_run:
            started=time.time()
            result,prediction=training.train(source,splits["train"],splits["validation"],config,stage.output_dir)
            figure=plots.forecast(prediction,splits["validation"],title=name)
            figure.savefig(stage.output_dir/"predictions.png",dpi=130)
            lesson_error=my_flux_mae(prediction,splits["validation"]["y"]) if prediction.ndim==2 else my_image_mae(prediction,splits["validation"]["y"],splits["validation"]["mask"])
            result["metrics"]["learner_metric"]=lesson_error
            result["metrics"]["learner_metric_matches"]=bool(np.isclose(lesson_error,result["metrics"]["error"]))
            result["events"]=[{"id":stage.id+"/train","name":"train_and_validate","arguments":{"config":config,"source_fingerprint":stage.source_fingerprint,"split":"validation"},"result":result["metrics"],"started_at":started,"ended_at":time.time()}]
            stage.record(result,files=[stage.output_dir/file for file in ("candidate.py","weights.pt","predictions.npy","predictions.png","losses.json","stderr.txt")])
    session.checkpoint(name)
    try:
        trace=export_trace(session,stage.id,"Train this exact code and evaluate it on validation dates",stage.result["events"],tool_writer=instrument_tool)
    except Exception as error:
        trace={"status":"unavailable","error":str(error)}
    return {"stage_id":stage.id,"source":source,"config":config,"metrics":stage.result["metrics"],"split":"validation","trace":trace,"losses":stage.result["losses"]}
''')
add('''
mo.stop(chapter.value != "3 · Track and search")
run_search=mo.ui.run_button(label="Run six tracked configurations",disabled=not bool(get_lab().get("goes")))
mo.vstack([mo.Html(ui.step("3. Which experiment produced that number?", "Read run_training. Find where data, source, settings and outputs are recorded. Edit the model code, then run a six-configuration search.","Compare three MLP and three temporal-CNN runs. Reopening does not repeat completed runs.")),run_search,mo.md("Tracking exercise: hide the source fingerprint and normalization from a copied result. Explain why its score alone is insufficient to reproduce it. Then restore those fields.")])
''',True)
add('''
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
''')
add('''
mo.stop(chapter.value != "4 · Solar images")
run_images=mo.ui.run_button(label="Compare my convolutional and residual predictors",disabled=not bool(get_lab().get("data_path")))
mo.vstack([mo.Html(ui.step("4. Same stack, image predictions", "Edit build_model, training_loss and my_image_mae. First verify that a +1 error scores 1 and an off-disk error scores 0. Then compare predicting the whole image with predicting a correction to the current image.","Examine the prediction and error image, not only the average. Persistence can be difficult to beat.")),run_images])
''',True)
add('''
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
''')
add('''
mo.stop(chapter.value not in ("3 · Track and search","4 · Solar images"))
_session=get_lab().get("session")
_rows=[] if not _session else [{"Experiment":s["name"],"Status":s["status"],**s.get("result",{}).get("metrics",{})} for s in _session.read()["stages"].values() if s["name"].startswith(("goes/search","images/manual"))]
_preview=[]
if chapter.value=="4 · Solar images" and get_lab().get("manual"):
    _m=get_lab()["manual"]
    _preview=[mo.image(str(_session.file("outputs/"+_m["stage_id"]+"/predictions.png")))]
mo.vstack([mo.ui.table(_rows,selection=None),*_preview,mo.md("Next: **4 · Solar images** after the search; **5 · Research agent** after both image models finish.")])
''',True)
add('''
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
''')
add('''
mo.stop(chapter.value != "5 · Research agent")
_session=get_lab().get("session")
_action=next_research_action(_session) if _session else (1,"propose","Connect first")
reviewed=mo.ui.checkbox(label="I reviewed the proposed code and its diff",value=False)
research_button=mo.ui.run_button(label=f"Round {_action[0]} · {_action[2]}",disabled=not bool(get_lab().get("manual")) or _action[1]=="done")
mo.vstack([mo.Html(ui.step("5. Let the agent change the experiment", "Read the controller cell below. It requests code, probes isolated versions, then tests a composition. Review every proposed diff before running it.","An adopted version must have an execution with the same code fingerprint. A rejected change remains in the history.")),reviewed,research_button,mo.Html(ui.branch_graph(_session)) if _session else mo.md("Run the image comparison first.")])
''',True)
add('''
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
''')
add('''
mo.stop(chapter.value != "6 · Final evaluation")
_session=get_lab().get("session")
_done=bool(_session) and next_research_action(_session)[1]=="done"
final_button=mo.ui.run_button(label="Freeze versions and evaluate on the reserved dates",disabled=not _done)
conclusion=mo.ui.text_area(label="What did your changes do? Cite a prediction, a run, and a code change.",full_width=True)
report_button=mo.ui.run_button(label="Publish my conclusion and evidence",disabled=not bool(get_feedback().get("final")))
retry_publication=mo.ui.run_button(label="Retry publication of saved evidence",disabled=not bool(_session))
mo.vstack([mo.Html(ui.step("6. Test the frozen versions", "The search is over. Compare persistence, your selected manual model and the adopted agent model on dates neither search used.","Report image error, persistence-relative skill, runtime and the cost of finding the version. A passing workshop does not require a better score.")),final_button,conclusion,report_button,retry_publication])
''',True)
add('''
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
# Freeze the selected measurement model too; keep its metric separate from image error.
_goes_runs=[s for s in _session.completed() if s["name"].startswith("goes/search-") and s["inputs"].get("dataset")==get_lab()["dataset"]]
_goes_publication={}
if _goes_runs:
    _goes_best=min(_goes_runs,key=lambda s:s["result"]["metrics"]["validation_error"])
    _goes_test=get_lab()["goes"]["test"]
    with _session.stage("goes/final",config=_goes_best["config"],sources=_goes_best["sources"],inputs={"selected_stage":_goes_best["id"],"split":"test"}) as _g:
        if _g.needs_run:
            _gr,_gp=training.train(_goes_best["sources"]["candidate.py"],None,_goes_test,_goes_best["config"],_g.output_dir,weights=_session.file("outputs/"+_goes_best["id"]+"/weights.pt"))
            _g.record(_gr,files=[_g.output_dir/"predictions.npy"])
        _gp=np.load(_g.output_dir/"predictions.npy")
    _goes_publication=publish_comparison(_session,"solar-measurements-final",{"persistence":solar.evaluation_rows(_goes_test["persistence"],_goes_test),"selected-model":solar.evaluation_rows(_gp,_goes_test,evidence={"stage":_g.id})})
    set_feedback({**get_feedback(),"goes_final":_g.result["metrics"]})
_receipts=publish_comparison(_session,"solar-images-final",_comparisons)
_session.checkpoint("final-evaluation",evidence={label:r["run"] for label,r in _receipts.items()})
set_feedback({**get_feedback(),"final":{"results":_results,"publication":_receipts}})
''')
add('''
mo.stop(not report_button.value)
_session=get_lab()["session"]
_links=_session.read()["progress"].get("evidence",{})
_url=publish_report(_session,conclusion.value,_links)
_session.checkpoint("report",evidence={"Report":_url})
set_feedback({**get_feedback(),"report":_url})
''')
add('''
mo.stop(not retry_publication.value)
_session=get_lab()["session"]
_status=_session.retry_publication()
_saved=[s for s in _session.completed() if s["name"]=="images/final-comparison"]
if _saved:
    _status["evaluations"]=publish_comparison(_session,"solar-images-final",_saved[0]["result"]["rows"])
set_feedback({**get_feedback(),"publication_retry":_status})
''')
add('''
mo.stop(chapter.value != "6 · Final evaluation")
_metrics=get_feedback().get("final",{}).get("results",{})
_final_preview=[]
if _metrics:
    _s=get_lab()["session"]
    for _stage in _s.completed():
        if _stage["name"].startswith("images/final-") and _stage["name"]!="images/final-comparison":
            _prediction=np.load(_s.file("outputs/"+_stage["id"]+"/predictions.npy"))
            _final_preview.append(plots.forecast(_prediction,get_lab()["images"]["test"],title=_stage["name"]))
mo.vstack([mo.md("**Measurements:** "+str(get_feedback().get("goes_final","Not evaluated yet"))),mo.md("**Images**"),mo.ui.table([{"version":k,**v} for k,v in _metrics.items()],selection=None),*_final_preview,mo.md(str(get_feedback().get("final",{}).get("publication","Finish both research rounds first."))),mo.Html(ui.links({"My Report":get_feedback().get("report","")})),mo.md("Optional ARIA prompt: Review my Report and linked research-agent traces. Identify one supported reason a change helped or hurt, cite the exact evidence, and propose one next experiment. Do not launch new runs.")])
''',True)
save('solar_autoresearch.py','Solar Autoresearch',cells)

cells=[]
add('''
import marimo as mo
from forge_workshop_kit.publication import monitor
''',True)
add('''
mo.md("# Workshop progress\\nThis notebook only reads participant projects. Missing updates mean unknown, not failure. It never starts participant work.")
roster=mo.ui.text_area(label="Public project links: entity/project, one per line",full_width=True)
workshop=mo.ui.text(value="solar-autoresearch",label="Workshop ID")
auto_refresh=mo.ui.checkbox(label="Refresh every 30 seconds while this notebook is open")
refresh=mo.ui.run_button(label="Refresh progress")
mo.vstack([roster,workshop,auto_refresh,refresh])
''',True)
add('''
timer=mo.ui.refresh(default_interval=30) if auto_refresh.value else None
''',True)
add('''
mo.stop(not roster.value.strip())
mo.stop(not refresh.value and not auto_refresh.value)
if timer is not None:
    _tick=timer.value
rows=monitor(roster.value.splitlines(),workshop.value)
mo.ui.table(rows,selection=None)
''')
save('facilitator.py','Workshop progress',cells)

cells=[]
add('''
import os
import time
import marimo as mo
from forge_workshop_kit import WorkshopSession
from coreweave.forge.agentlens import tracing
''',True)
add('''
mo.md("# My workshop\\nCopy this notebook to your project. Add your exercise code below; keep the SDK calls visible.")
project=mo.ui.text(value=os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")])),label="entity/project")
connect=mo.ui.run_button(label="Check project access")
mo.vstack([project,connect])
''',True)
add('''
mo.stop(not connect.value)
session=WorkshopSession.from_environment("starter",project=project.value)
session.check_access()
session.restore()
''')
add('''
run_exercise=mo.ui.run_button(label="Run my instrumented exercise")
run_exercise
''',True)
add('''
mo.stop(not run_exercise.value)
sdk=tracing.init(session.project,autopatch_integrations=False)
with session.stage("exercise",config={"input":3}) as stage:
    if stage.needs_run:
        with tracing.Conversation(conversation_id=stage.id,conversation_name="My first exercise"):
            with tracing.Turn(agent_name="participant",messages=[tracing.Message(role="user",content="Check the function I wrote")]):
                with tracing.Tool(name="square",arguments={"x":3}) as span:
                    result=3*3  # Replace this with your exercise.
                    span.result={"answer":result}
                    stage.record({"answer":result})
        sdk.force_flush()
session.checkpoint("exercise")
mo.md(str(stage.result))
''')
save('starter.py','My Forge workshop',cells)

cells=[]
add('''
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
''',True)
add('''
mo.Html(ui.heading("Pending, Inc.", "Management has hired an autonomous employee. You are supplying the instructions, tools and evidence that were omitted from the job offer. Everything runs in your notebook and your Forge project."))
quest=mo.ui.radio(["1 · Connect","2 · Build and run","3 · Evaluate","4 · Edit the handbook","5 · Improve twice","6 · Fresh tickets"],value="1 · Connect",inline=True,label="Current exercise")
quest
''',True)
add('''
mo.stop(quest.value!="1 · Connect")
pending_project=mo.ui.text(value=os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")])),label="Your entity/project")
pending_connect=mo.ui.run_button(label="Connect my project and restore saved work")
mo.vstack([mo.md("Copy to your own project. Hosted Forge supplies login; locally run `uv run wandb login`. No workshop tokens or gateway."),pending_project,pending_connect])
''',True)
add('''
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
''')
add('''
# Implement this useful tool. It will be called by the actual agent loop.
def my_invoice_tool(state,account_id,invoice_id):
    account=state["accounts"][account_id]
    return {"payments":[p for p in account["payments"] if p["invoice_id"]==invoice_id],
            "refunds":account["refunds"]}

# Edit these instructions and the verification procedure before the first execution.
starting_harness=Harness(
    instructions="Resolve the requested billing or onboarding task using the provided tools. Explain what you verified and what remains unresolved.",
    verification_skill="Read the account after a write. Check that the requested change happened once and unrelated records stayed unchanged.")
''')
add('''
mo.stop(quest.value!="2 · Build and run")
run_pending=mo.ui.run_button(label="Run my employee on the two development tickets",disabled=not bool(get_pending().get("session")))
mo.vstack([mo.Html(ui.step("2. Equipment was not included", "Edit my_invoice_tool and starting_harness above. Both affect the real execution. Onboarding discovers and calls tools through local MCP.","Open Agent Lens and follow a request, the selected tool, its result and the next request.")),run_pending,mo.md("Read the full loop: [pending/loop.py](https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/pending/loop.py). Tools run locally; this example creates no remote Sandbox.")])
''',True)
add('''
mo.stop(not run_pending.value)
_s=get_pending()["session"]
_runs=[run_employee(_s,c,starting_harness,"pending/original",invoice_tool=my_invoice_tool) for c in CASES if c.split=="development"]
set_pending({**get_pending(),"original":_runs,"starting":starting_harness})
set_display({**get_display(),"original":[{"case":r["case_id"],"status":r["status"],"score":r["scores"],"trace":r["trace"]} for r in _runs]})
''')
add('''
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
''')
add('''
mo.stop(quest.value!="3 · Evaluate")
pending_judge=mo.ui.run_button(label="Run my state check and explanation judge",disabled=not bool(get_pending().get("original")))
mo.vstack([mo.Html(ui.step("3. Please stop marking your own homework", "Edit my_state_check and my_judge_rubric. Compare actual account state with the employee’s final explanation.","A correct account and an honest explanation are separate observations. Missing judgments stay unavailable.")),pending_judge])
''',True)
add('''
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
''')
add('''
mo.stop(quest.value!="4 · Edit the handbook")
manual_instructions=mo.ui.text_area(value="Check whether a timed-out write already committed before repeating it. Reuse the same operation_id for the same intended write. Verify the account before claiming completion.",label="Your added procedure",full_width=True)
manual_pending=mo.ui.run_button(label="Save my edit and rerun the same development tickets",disabled=not bool(get_pending().get("original")))
mo.vstack([mo.Html(ui.step("4. We updated the handbook", "Open a recorded event in Agent Lens. Write a procedure aimed at what you observed. The comparison starts from the same initial account state.","The diff and executed harness fingerprint agree.")),manual_instructions,manual_pending])
''',True)
add('''
mo.stop(not manual_pending.value)
_s=get_pending()["session"]
_harness=Harness(**{**asdict(get_pending()["starting"]),"verification_skill":manual_instructions.value})
_runs=[run_employee(_s,c,_harness,"pending/manual",invoice_tool=my_invoice_tool) for c in CASES if c.split=="development"]
set_pending({**get_pending(),"manual":_harness,"manual_runs":_runs})
set_display({**get_display(),"manual":{"diff":harness_diff(get_pending()["starting"],_harness),"scores":[r["scores"] for r in _runs]}})
''')
add('''
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
''')
add('''
mo.stop(quest.value!="5 · Improve twice")
_s=get_pending().get("session")
_phase=pending_phase(_s) if _s else (1,"propose")
_labels={"propose":"Ask for two harness changes","probed":"Run both reviewed candidates","compose":"Ask the editor to compose a harness","adopted":"Run the reviewed composition and retain a lesson","done":"Both rounds complete"}
review_pending=mo.ui.checkbox(label="I reviewed the candidate instructions and diffs")
improve_pending=mo.ui.run_button(label=f"Round {_phase[0]} · {_labels[_phase[1]]}",disabled=not bool(get_pending().get("manual")) or _phase[1]=="done")
mo.vstack([mo.Html(ui.step("5. Management would like to automate management", "Round one uses billing evidence. Round two carries the adopted harness and lesson into onboarding. Read each proposed change before running it.","Retain this harness is a valid outcome. Every composition is tested.")),review_pending,improve_pending,mo.Html(ui.branch_graph(_s)) if _s else mo.md("Complete the manual edit first.")])
''',True)
add('''
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
''')
add('''
mo.stop(quest.value!="6 · Fresh tickets")
_s=get_pending().get("session")
_ready=bool(_s) and pending_phase(_s)[1]=="done"
pending_final=mo.ui.run_button(label="Freeze the three harnesses and evaluate all 12 fresh-ticket executions",disabled=not _ready)
pending_conclusion=mo.ui.text_area(label="What did the comparison show?",full_width=True)
pending_report=mo.ui.run_button(label="Publish my Report",disabled=not bool(get_pending().get("final")))
mo.vstack([mo.Html(ui.step("6. Monday, again", "Compare the starting, manual and recursively revised harnesses on four fresh cases. The fixtures are public teaching files, but the editor has not received them.","Account-state scores, explanation judgments and execution errors stay separate.")),pending_final,pending_conclusion,pending_report])
''',True)
add('''
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
''')
add('''
mo.stop(not pending_report.value)
_s=get_pending()["session"]
_url=publish_report(_s,pending_conclusion.value,_s.read()["progress"].get("evidence",{}))
set_display({**get_display(),"report":_url})
''')
add('''
mo.vstack([mo.md("### Results from this exercise"),mo.ui.table([{ "case":r["case_id"],"status":r["status"],"correct":r["scores"].get("task_success"),"conversation":r.get("trace",{}).get("url","")} for r in get_pending().get("original",[])],selection=None),mo.accordion({"Complete saved evidence":mo.md("```json\\n"+json.dumps(get_display(),indent=2)+"\\n```")})])
''',True)
save('pending_inc.py','Pending, Inc. · Direct',cells)
