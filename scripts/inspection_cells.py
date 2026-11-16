"""Authored PCB1 workshop cells. The generator writes the editable notebook."""
from notebook_builder import Cell
cells = []
def add(code, hide=False, cell_id=None):
    cells.append(Cell(code, hide=hide, cell_id=cell_id))

add('''
import json
from pathlib import Path
import numpy as np
import marimo as mo
from forge_workshop_kit import WorkshopSession, setup, ui, inspection
from forge_workshop_kit import aria, technical_guides
from forge_workshop_kit import inspection_teaching as teaching
from forge_workshop_kit.session import digest
from forge_workshop_kit.traces import event, export_trace
from forge_workshop_kit.review import save_review
from forge_workshop_kit.publication import publish_comparison, publish_report
get_lab, set_lab = mo.state({})
get_technical_guide_view, set_technical_guide_view = mo.state({}, allow_self_loops=True)
technical_guide_controls = technical_guides.controls(mo, 'visual_inspection', set_technical_guide_view)
get_step, set_step = mo.state("setup", allow_self_loops=True)
get_feedback, set_feedback = mo.state({})
''', True)
add('''
def go_to(step):
    if get_lab().get("session"):
        get_lab()["session"].set_view(step)
    set_step(step)

def feedback(name, value):
    set_feedback(lambda current: {**current, name: value})

def refresh_inspection():
    set_lab(dict(get_lab()))
''', True)
add('''
_s = get_lab().get("session")
inspection_nav = ui.navigation(mo, teaching.STEPS, get_step(), go_to, completed=teaching.completed_steps(_s), label="Workshop steps")
mo.vstack([mo.Html(ui.STYLE + technical_guides.theme_style()), inspection_nav, mo.Html(ui.context(_s)) if _s else mo.md("Inspect the opening board, then connect. Looking at images and editing code does not train or publish.")])
''', True)
add('''
technical_guide_view = technical_guides.panel(mo, 'visual_inspection', get_step(), get_technical_guide_view(), technical_guide_controls)
technical_guide_view
''', True, cell_id='visual_inspection/visual_guide')
add('''
mo.stop(get_step() != "setup")
mo.vstack([mo.md("**4-hour workshop, including breaks and exercises.** [Open the companion deck](https://ash0ts.github.io/forge-workshop-kit/inspection/). Its worked examples explain the code you will edit below."),mo.Html(ui.heading("Find defective parts before they ship", "You’re joining a fictional circuit-board inspection team. A missed defect can leave the factory; a false alarm sends a usable board for another inspection. Your job is to compare both outcomes before choosing a detector.", theme="inspection")),
mo.md("The photographs are real **VisA PCB1** observations, released by the SPot-the-Difference authors under CC BY 4.0. They show one circuit-board family, with normal and defective examples and pixel masks identifying annotated defects. We’ll use the authors’ supervised split. The final 442 boards stay outside training and threshold selection."),
mo.md("We’ll first compress each photograph into one feature vector. Then we’ll keep local patch information to see whether small defects become easier to detect. You’ll choose a review batch, train again, freeze a threshold, and check missed defects, false alarms, and review workload separately. A factory pilot would need more products and operating conditions than this teaching set."),
mo.md("The recorded follow-up improved average precision from **0.8729 to 0.8857**, with misses falling from 4 to 3 and false alarms from 23 to 18. It was a teaching retest of images already inspected during a failed first recipe. Your own run may differ; don’t select a model by looking at its final-test result.")])
''', True)
add('''
opening_board_choice = mo.ui.radio(["Pass", "Send for inspection"], label="Would you pass this board?")
opening_board_reveal = mo.ui.checkbox(label="Reveal the supplied defect annotation")
''', True, cell_id='visual_inspection/controls/opening_example')
add('''
_board=teaching.opening_board()
_opening=[mo.md("### Inspect one board before connecting"),mo.image(_board["image"],alt="A VisA PCB1 circuit board photographed from above, with components and copper traces visible.",width=320),opening_board_choice,opening_board_reveal]
if opening_board_reveal.value:
    from PIL import Image as _Image
    _mask=np.asarray(_Image.open(_board["mask"]))
    _opening.extend([mo.image(_Image.fromarray((_mask>0).astype("uint8")*255),alt="Supplied defect mask for the displayed board: white pixels mark annotated defects; black pixels are unmarked.",width=320),mo.md("Published label: **defective**. White pixels show the supplied annotation, not a model explanation."),mo.accordion({"Source and checksums":mo.md(f"Case: `{_board['case_id']}` · partition: `{_board['partition']}`\\n\\nSource image: `{_board['source_image']}`\\n\\nSource SHA-256: `{_board['source_sha256']}`\\n\\nBundled image SHA-256: `{_board['image_sha256']}`\\n\\nBundled mask SHA-256: `{_board['mask_sha256']}`")})])
_opening.append(mo.md("VisA PCB1 fitting example · CC BY 4.0. This bundled example needs no account or download. [Dataset source](https://github.com/amazon-science/spot-diff)"))
mo.vstack(_opening) if get_step()=="setup" else mo.md("")
''', True, cell_id='visual_inspection/opening_example')
add('''
mo.stop(get_step() != "setup")
_context = setup.project_context()
inspection_project = mo.ui.text(value=_context["project"], label="Your Forge entity/project", disabled=_context["hosted"] and _context["detected"], full_width=True)
inspection_allowance = mo.ui.number(value=8, start=.01, stop=1000, label="Optional inference allowance in USD; this core classifier path uses no model API")
connect_inspection = mo.ui.run_button(label="Connect and restore my inspection work")
mo.vstack([inspection_project, inspection_allowance, mo.md("Use your own writable project. Locally, run uv run wandb login first. CPU feature and classifier work uses notebook compute; it is separate from inference billing."), connect_inspection])
''', True)
add('''
mo.stop(not connect_inspection.value)
try:
    _session = WorkshopSession.from_environment("visual-inspection", project=inspection_project.value, budget_usd=inspection_allowance.value)
    _access = _session.check_access()
    _restored = _session.restore()
    setup.save_access(_session, _access)
    set_lab({"session": _session})
    set_step(_session.get_view("setup"))
    feedback("setup", {"project": _session.project, "restore": _restored, "status": "complete"})
except Exception as _error:
    feedback("setup", {"status": "unavailable", "message": str(_error), "next": "Check project write access and sign in again, then retry Connect."})
''', True)
add('''
def instrument_inspection_tool(observation):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=observation["name"], arguments=observation["arguments"], result=observation["result"],
        tool_call_id=observation["id"], started_at=stamp(observation["started_at"]), ended_at=stamp(observation["ended_at"])) as tool:
        tool.set_attributes({"workshop.exercise": "pcb-inspection"})
        # Add an attribute that describes the feature representation being tested.
        if observation.get("error"):
            tool.record_error(RuntimeError(observation["error"]))
        return format(trace.get_current_span().get_span_context().span_id, "016x")
''')
add('''
mo.stop(get_step() != "setup")
first_inspection_trace = mo.ui.run_button(label="Send my first inspection trace", disabled=not bool(get_lab().get("session")))
mo.vstack([mo.md("**Read the tracing function above.** The Tool scope records actual arguments, result and timing. Add an attribute of your own, then send an environment trace. The same writer will record your classifier training calls."), first_inspection_trace, mo.Html(ui.result("Connection", get_feedback().get("setup", {}))), ui.next_step(mo, "Next: inspect the boards", "data", go_to)])
''', True)
add('''
mo.stop(not first_inspection_trace.value)
_s = get_lab()["session"]
with _s.stage("setup/trace", config={"device": "cpu"}) as _stage:
    if _stage.needs_run:
        _result, _event = event("inspect_classifier_environment", {}, lambda: {"numpy": np.__version__, "device": "cpu"}, on_error=_stage.record_event)
        _stage.record({"events": [_event]})
try:
    _trace = export_trace(_s, _stage.id, "Inspect my circuit-board experiment", _stage.result["events"], tool_writer=instrument_inspection_tool)
    _s.checkpoint("setup", evidence={"Environment trace": _trace["url"]})
    feedback("trace", {"status": "complete", "url": _trace["url"]})
except Exception as _error:
    feedback("trace", {"status": "publication pending", "message": str(_error), "next": "Click the same button to retry export. The saved environment check will not rerun."})
''', True)
add('''
mo.stop(get_step() != "setup")
_s = get_lab().get("session")
mo.vstack([mo.Html(ui.result("Trace publication", get_feedback().get("trace", {}))), ui.evidence(mo, _s, stage_ids=teaching.stage_ids(_s, "setup/trace"), question="Open inspect_classifier_environment in Agent Lens. Find your attribute and the NumPy version returned by the operation.") if _s else mo.md("")])
''', True)
add('''
mo.stop(get_step() != "data")
load_inspection = mo.ui.run_button(label="Download and verify the PCB1 teaching data", disabled=not bool(get_lab().get("session")))
mo.vstack([mo.Html(ui.step("Inspect the parts before training", "Look at a board and decide whether it needs review before revealing the supplied label. The mask is an annotation for inspection, never a classifier input.", "Click Download, then choose a training board.")), load_inspection, mo.md("The download contains 1,104 real photos, defect masks, cached features, source checksums and the license. Of the official training partition, 397 boards fit models, 133 form the review pool, and 132 set validation choices. The authors’ 442 test boards remain untouched until your freeze step.")])
''', True)
add('''
mo.stop(not load_inspection.value)
_root = teaching.download()
_data = inspection.load_data(_root)
set_lab({**get_lab(), "data": _data})
get_lab()["session"].checkpoint("data", evidence={"Dataset source": "https://github.com/amazon-science/spot-diff"})
''', True)
add('''
mo.stop(get_step() != "data")
_data = get_lab().get("data")
_options = {r["case_id"]: i for i, r in enumerate(_data["records"]) if r["partition"] == "fit"} if _data else {}
board_choice = mo.ui.dropdown(_options, value=next(iter(_options), None), label="Training board", disabled=not bool(_options))
show_board_label = mo.ui.checkbox(label="Reveal the published defect label and mask")
mo.vstack([board_choice, show_board_label, ui.next_step(mo, "Next: train the whole-image baseline", "baseline", go_to)])
''', True)
add('''
mo.stop(get_step() != "data" or not get_lab().get("data"))
inspection.render_case(get_lab()["data"], board_choice.value, reveal_label=show_board_label.value)
''', True)
add('''
_s = get_lab().get("session")
feature_editor = mo.ui.code_editor(value=_s.get_draft("inspection/features", teaching.FEATURE_STARTER) if _s else teaching.FEATURE_STARTER, language="python", on_change=lambda value: _s.save_draft("inspection/features", value) if _s else None, debounce=False)
check_inspection_features = mo.ui.run_button(label="Check my patch-feature function")
mo.vstack([mo.md("### Keep the local information\\nThe fixed ImageNet encoder gives us a 512-value whole-image vector and a 14 × 14 grid of patch vectors. In `build_features`, turn the patch-error map into a row and append it to the whole-image features. The trained classifier will actually use your function."), feature_editor, check_inspection_features, mo.accordion({"Hint": mo.md("Use `inspection.nearest_patch_errors(data, rows, reference)` for nearest-patch. Apply np.log1p, reshape to `(len(rows), -1)`, then concatenate along axis 1."), "Worked answer": mo.md("```python\\n" + teaching.FEATURE_SOLUTION + "\\n```"), "What is cached?": mo.md("ResNet-18’s ImageNet weights stay fixed. We resize each board to 224 × 224, normalize channels, and extract whole-image and local features. The prepared cache preserves exact source and weight hashes. Fitting a classifier changes its weights, not the image encoder.")}), ui.next_step(mo, "Next: train and compare", "compare", go_to)]) if get_step() == "features" else mo.md("")
''', True)
add('''
patch_distance_check = mo.ui.run_button(label="Calculate one patch distance",disabled=not bool(get_lab().get("data")))
mo.vstack([mo.md("### Work through one position before flattening the map"),mo.md("The calculation below uses position (7, 7) of fitting board pcb1-anomaly-005 and normal fitting boards only. Find the smallest distance, then compare it with nearest_patch_errors."),patch_distance_check]) if get_step()=="features" else mo.md("")
''', True, cell_id='visual_inspection/controls/patch_distance')
add('''
mo.stop(not patch_distance_check.value)
_data=get_lab()["data"]
_query=next(i for i,row in enumerate(_data["records"]) if row["case_id"]=="pcb1-anomaly-005" and row["partition"]=="fit")
_fit=inspection.indices(_data,"fit")
_normals=_fit[inspection.labels(_data,_fit)==0]
_reference={"bank":_data["patches"][_normals],"case_ids":[_data["records"][int(i)]["case_id"] for i in _normals]}
_bank=_reference["bank"][:,7,7,:]
_query_vector=_data["patches"][_query,7,7,:]
_scale=np.maximum(_bank.std(axis=0),.1)
_distances=np.mean((_query_vector/_scale-_bank/_scale)**2,axis=1)
_closest=int(np.argmin(_distances))
_expected=float(inspection.nearest_patch_errors(_data,np.array([_query]),_reference)[0,7,7])
assert np.isclose(_distances[_closest],_expected,atol=1e-5)
mo.ui.table([{"Query":"pcb1-anomaly-005","Position":"(7, 7)","Channels":len(_query_vector),"Normal fitting boards":len(_normals),"Closest board":_reference["case_ids"][_closest],"Mean squared scaled distance":float(_distances[_closest]),"log1p feature":float(np.log1p(_distances[_closest]))}],selection=None)
''', False, cell_id='visual_inspection/action/patch_distance')
add('''
def build_features(data, rows, method, reference=None):
    return teaching.functions(feature_editor.value)["build_features"](data, rows, method, reference)
''')
add('''
mo.stop(not check_inspection_features.value)
try:
    feedback("features", teaching.check_features(feature_editor.value))
    if get_lab().get("session"):
        get_lab()["session"].checkpoint("features", publish=False)
except Exception as _error:
    feedback("features", {"status": "needs work", "message": str(_error)})
''', True)
add('''
_s = get_lab().get("session")
threshold_editor = mo.ui.code_editor(value=_s.get_draft("inspection/threshold", teaching.THRESHOLD_STARTER) if _s else teaching.THRESHOLD_STARTER, language="python", on_change=lambda value: _s.save_draft("inspection/threshold", value) if _s else None, debounce=False)
check_inspection_threshold = mo.ui.run_button(label="Check my threshold function")
train_whole = mo.ui.run_button(label="Train the whole-image baseline", disabled=not bool(get_lab().get("data")))
_seen=bool(_s and (_s.get_draft("inspection/baseline-observation",None) or teaching.saved(_s,"compare/nearest-patch")))
train_inspection = mo.ui.run_button(label="Train the patch-feature alternative", disabled=not bool(_s and teaching.saved(_s,"compare/whole")))
mo.vstack([mo.md("### Choose an operating rule for the baseline"),mo.md("The baseline uses the 512 whole-image values already returned by build_features. Complete choose_threshold so at least 90% of validation defects score at or above the cutoff. Then fit the baseline and inspect a miss or false alarm. We will keep this rule and classifier settings fixed when adding patches."),threshold_editor,check_inspection_threshold,mo.accordion({"Worked answer":mo.md("```python"+chr(10)+teaching.THRESHOLD_SOLUTION+chr(10)+"```")}),train_whole]) if get_step()=="baseline" else mo.vstack([mo.md("### Test the added patch information"),mo.md("The patch model uses the same fitting boards, C=0.03, and threshold rule. Only the feature representation changes. The whole-image result stays saved."),train_inspection,mo.md("Inspect a validation board before testing patches. Saving a note is optional.") if not _seen else mo.md("The baseline observation is saved."),ui.next_step(mo,"Next: choose a review batch","review",go_to)]) if get_step()=="compare" else mo.md("")
''', True, cell_id='visual_inspection/controls/check_inspection_threshold')
add('''
_s=get_lab().get("session")
_data=get_lab().get("data")
_base=teaching.saved(_s,"compare/whole") if _s else None
_choices={}
if _base and _data:
    _rows=inspection.indices(_data,"validation")
    _model=teaching.model_from_stage(_s,"compare/whole")
    _scores=inspection.score(_data,_rows,_model,build_features=teaching.functions(_base["sources"]["features.py"])["build_features"])
    _mistakes=[int(i) for i,score in zip(_rows,_scores) if bool(score>=_model["threshold"])!=bool(_data["records"][int(i)]["label"])]
    _choices={_data["records"][i]["case_id"]:i for i in (_mistakes or list(_rows))}
validation_board=mo.ui.dropdown(_choices,value=next(iter(_choices),None),label="Validation board to investigate",disabled=not bool(_choices))
inspection_baseline_note=mo.ui.text_area(value=_s.get_draft("inspection/baseline-note","") if _s else "",label="Optional note: what did the baseline miss or flag, and what might patches change?",on_change=lambda value:_s.save_draft("inspection/baseline-note",value) if _s else None,full_width=True)
save_inspection_observation=mo.ui.run_button(label="Save my baseline observation",disabled=not bool(_choices))
mo.vstack([mo.md("### Inspect a baseline decision"),validation_board,inspection_baseline_note,save_inspection_observation]) if get_step()=="baseline" else mo.md("")
''', True, cell_id='visual_inspection/controls/baseline_observation')
add('''
mo.stop(get_step()!="baseline" or validation_board.value is None or not get_lab().get("data"))
_s=get_lab()["session"]
_data=get_lab()["data"]
_base=teaching.saved(_s,"compare/whole")
_model=teaching.model_from_stage(_s,"compare/whole")
_score=float(inspection.score(_data,[validation_board.value],_model,build_features=teaching.functions(_base["sources"]["features.py"])["build_features"])[0])
mo.vstack([inspection.render_case(_data,validation_board.value,reveal_label=True),mo.md("Saved whole-image model: score **"+str(round(_score,3))+"**, cutoff **"+str(round(_model["threshold"],3))+"**. Scores at or above the cutoff are flagged. This is a validation board, not a final-test example.")])
''', True, cell_id='visual_inspection/display/baseline_board')
add('''
mo.stop(get_step()!="baseline")
_s=get_lab().get("session")
_baseline=teaching.saved(_s,"compare/whole") if _s else None
_selected_case=get_lab()["data"]["records"][validation_board.value]["case_id"] if get_lab().get("data") and validation_board.value is not None else None
inspection_aria_investigate=aria.investigation(mo,_s,"investigate",record_ids=[_baseline["id"]] if _baseline else [],case_ids=[_selected_case] if _selected_case else [],interpretation=inspection_baseline_note.value,workshop="visual-inspection")
inspection_after_aria=ui.next_step(mo,"Next: add patch features","features",go_to)
mo.vstack([inspection_aria_investigate,inspection_after_aria])
''', True, cell_id='visual_inspection/aria/investigate')
add('''
mo.stop(not save_inspection_observation.value)
mo.stop(not inspection_baseline_note.value.strip(),mo.md("Write a note to save it, or continue without one."))
_s=get_lab()["session"]
_s.save_draft("inspection/baseline-observation",{"row":validation_board.value,"note":inspection_baseline_note.value})
''', True, cell_id='visual_inspection/action/baseline_observation')
add('''
mo.stop(get_step() != "features")
mo.Html(ui.result("Local check", get_feedback().get("features", {})))
''', True)
add('''
def choose_threshold(target, scores, recall=.90):
    return teaching.functions(threshold_editor.value)["choose_threshold"](target, scores, recall)
''')
add('''
mo.stop(not check_inspection_threshold.value)
try:
    feedback("threshold", teaching.check_threshold(threshold_editor.value))
except Exception as _error:
    feedback("threshold", {"status": "needs work", "message": str(_error)})
''', True)
add('''
mo.stop(not train_whole.value)
teaching.check_whole_features(feature_editor.value)
teaching.check_threshold(threshold_editor.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_fit, _val = inspection.indices(_data, "fit"), inspection.indices(_data, "validation")
_method='whole'
teaching.check_matched_settings(_s,_method,feature_editor.value,threshold_editor.value,_data)
with _s.stage("compare/" + _method, config={"method": _method, "C": .03, "threshold_recall": .90}, sources={"features.py": feature_editor.value, "threshold.py": threshold_editor.value}) as _stage:
    if _stage.needs_run:
        def _train_and_validate():
            _model = inspection.fit_classifier(_data, _fit, _method, build_features=build_features, C=.03)
            _values = inspection.score(_data, _val, _model, build_features=build_features)
            _threshold = choose_threshold(inspection.labels(_data, _val), _values)
            _metrics = inspection.metrics(inspection.labels(_data, _val), _values, _threshold)
            _path = _stage.output_dir / "classifier.npz"
            _sha = inspection.save_classifier(_path, _model, _threshold)
            return {"metrics": _metrics, "model_file": _path.relative_to(_s.root).as_posix(), "model_sha256": _sha, "seconds": _model["seconds"]}
        _result, _event = event("train_and_validate_classifier", {"method": _method, "training_boards": len(_fit), "C": .03}, _train_and_validate, on_error=_stage.record_event)
        _stage.record({**_result, "events": [_event]}, files=[_s.file(_result["model_file"])])
try:
    export_trace(_s, _stage.id, "Compare " + _method + " board features", _stage.result["events"], tool_writer=instrument_inspection_tool)
except Exception as _error:
    feedback("publication", {"status": "trace pending", "message": str(_error)})

_s.checkpoint("baseline")
if teaching.saved(_s,"compare/whole") and teaching.saved(_s,"compare/nearest-patch"):
    _s.checkpoint("compare")
feedback("compare", {"status": "saved", "representation": _method})
''', False, cell_id='visual_inspection/action/train_whole')
add('''
mo.stop(not train_inspection.value)
teaching.check_features(feature_editor.value)
teaching.check_threshold(threshold_editor.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_fit, _val = inspection.indices(_data, "fit"), inspection.indices(_data, "validation")
_method='nearest-patch'
teaching.check_matched_settings(_s,_method,feature_editor.value,threshold_editor.value,_data)
with _s.stage("compare/" + _method, config={"method": _method, "C": .03, "threshold_recall": .90}, sources={"features.py": feature_editor.value, "threshold.py": threshold_editor.value}) as _stage:
    if _stage.needs_run:
        def _train_and_validate():
            _model = inspection.fit_classifier(_data, _fit, _method, build_features=build_features, C=.03)
            _values = inspection.score(_data, _val, _model, build_features=build_features)
            _threshold = choose_threshold(inspection.labels(_data, _val), _values)
            _metrics = inspection.metrics(inspection.labels(_data, _val), _values, _threshold)
            _path = _stage.output_dir / "classifier.npz"
            _sha = inspection.save_classifier(_path, _model, _threshold)
            return {"metrics": _metrics, "model_file": _path.relative_to(_s.root).as_posix(), "model_sha256": _sha, "seconds": _model["seconds"]}
        _result, _event = event("train_and_validate_classifier", {"method": _method, "training_boards": len(_fit), "C": .03}, _train_and_validate, on_error=_stage.record_event)
        _stage.record({**_result, "events": [_event]}, files=[_s.file(_result["model_file"])])
try:
    export_trace(_s, _stage.id, "Compare " + _method + " board features", _stage.result["events"], tool_writer=instrument_inspection_tool)
except Exception as _error:
    feedback("publication", {"status": "trace pending", "message": str(_error)})

if teaching.saved(_s,"compare/whole") and teaching.saved(_s,"compare/nearest-patch"):
    _s.checkpoint("compare")
feedback("compare", {"status": "saved", "representation": _method})
''', False, cell_id='visual_inspection/action/train_inspection')
add('''
mo.stop(get_step() not in ("baseline", "compare"))
_s = get_lab().get("session")
_rows = []
if _s:
    for _name in ["whole", "nearest-patch"]:
        _row = teaching.saved(_s, "compare/" + _name)
        if _row:
            _rows.append({"Representation": _name, **_row["result"]["metrics"], "Seconds": _row["result"]["seconds"]})
mo.vstack([mo.Html(ui.result("Threshold check", get_feedback().get("threshold", {}))), mo.ui.table(_rows, selection=None), ui.evidence(mo, _s, stage_ids=teaching.stage_ids(_s, "compare"), question="Open each classifier run. Compare validation recall and false alarms, then open the saved classifier artifact.") if _s else mo.md("")])
''', True)
add('''
_s = get_lab().get("session")
review_editor = mo.ui.code_editor(value=_s.get_draft("inspection/review", teaching.REVIEW_STARTER) if _s else teaching.REVIEW_STARTER, language="python", on_change=lambda value: _s.save_draft("inspection/review", value) if _s else None, debounce=False)
check_inspection_review = mo.ui.run_button(label="Check my review selector")
select_inspection_review = mo.ui.run_button(label="Select 24 boards for each review method", disabled=not bool(_s and teaching.saved(_s, "compare/nearest-patch")))
mo.vstack([mo.md("### Spend the same review effort\\nSelect 24 cases closest to the decision threshold without reading their labels. Compare that choice with 24 uniformly sampled cases from the same review pool, using seed 17. Both methods get the same number of new labels. A larger training set alone does not prove that active selection helped."), review_editor, check_inspection_review, mo.accordion({"Worked answer": mo.md("```python\\n" + teaching.REVIEW_SOLUTION + "\\n```")}), select_inspection_review]) if get_step() == "review" else mo.md("")
''', True)
add('''
mo.stop(not check_inspection_review.value)
try:
    feedback("review_check", teaching.check_review(review_editor.value))
except Exception as _error:
    feedback("review_check", {"status": "needs work", "message": str(_error)})
''', True)
add('''
mo.stop(not select_inspection_review.value)
teaching.check_review(review_editor.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_parent = teaching.saved(_s, "compare/nearest-patch")
if feature_editor.value != _parent["sources"]["features.py"]:
    raise ValueError("Your feature code changed. Train both representations before choosing a review batch.")
_model = teaching.model_from_stage(_s, "compare/nearest-patch")
_parent_features = teaching.functions(_parent["sources"]["features.py"])["build_features"]
_pool = inspection.indices(_data, "review")
_values = inspection.score(_data, _pool, _model, build_features=_parent_features)
_active = teaching.functions(review_editor.value)["choose_review"](_values, _pool, _model["threshold"], 24, 17)
_random = inspection.select_review(_values, _pool, _model["threshold"], 24, "random", 17)
if len(set(_active)) != 24 or not set(_active).issubset(set(_pool)):
    raise ValueError("Select 24 different cases from the review pool.")
with _s.stage("review/selection", config={"budget": 24, "seed": 17, "parent_stage": _parent["id"], "parent_model_sha256": _parent["result"]["model_sha256"]}, sources={"review.py": review_editor.value, "features.py": _parent["sources"]["features.py"]}) as _stage:
    if _stage.needs_run:
        _stage.record({"active": [int(i) for i in _active], "random": [int(i) for i in _random], "labels_revealed": False})
feedback("review", {"status": "selected", "active_cases": [str(_data["records"][i]["case_id"]) for i in _active]})
''', True)
add('''
mo.stop(get_step() != "review")
_s, _data = get_lab().get("session"), get_lab().get("data")
_selection = teaching.saved(_s, "review/selection") if _s else None
_options = {_data["records"][i]["case_id"]: i for i in _selection["result"]["active"]} if _selection and _data else {}
review_board = mo.ui.dropdown(_options, value=next(iter(_options), None), label="Board selected for review", disabled=not bool(_options))
review_guess = mo.ui.radio(["normal", "defective", "needs another reviewer"], value="needs another reviewer", label="Your assessment before revealing the label")
reveal_review = mo.ui.checkbox(label="Reveal the dataset annotation")
save_inspection_review = mo.ui.run_button(label="Save my assessment", disabled=not bool(_options))
train_reviewed = mo.ui.run_button(label="Reveal batch labels and train the two reviewed classifiers", disabled=not bool(_options))
mo.vstack([mo.Html(ui.result("Selector check", get_feedback().get("review_check", {}))), review_board, review_guess, reveal_review, save_inspection_review, mo.md("Inspect a few selected boards and save your assessments. The batch step uses the authors’ supplied labels for all 24 selected cases. It is a simulation of label acquisition, not a claim that a human reviewed the entire batch. Your own assessment remains a separate record."), train_reviewed, ui.next_step(mo, "Next: freeze a detector", "freeze", go_to)])
''', True)
add('''
mo.stop(get_step() != "review" or review_board.value is None or not get_lab().get("data"))
inspection.render_case(get_lab()["data"], review_board.value, reveal_label=reveal_review.value, reference=teaching.model_from_stage(get_lab()["session"], "compare/nearest-patch")["reference"])
''', True)
add('''
mo.stop(not save_inspection_review.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_row = _data["records"][review_board.value]
_review_record = save_review(_s, case_id=_row["case_id"], proposed_label=None, accepted_label=None if review_guess.value == "needs another reviewer" else review_guess.value, reviewer=_s.workspace_id, dataset_version=_data["manifest"]["version"], verified=review_guess.value != "needs another reviewer", evidence={"annotation_visible": reveal_review.value, "source_image": _row["source_image"]})
with _s.stage("review/assessment/" + _row["case_id"], config={"assessment": review_guess.value, "annotation_visible": reveal_review.value}) as _stage:
    if _stage.needs_run:
        _stage.record({"case_id": _row["case_id"], "human_assessment": review_guess.value, "review_record_id": _review_record["id"], "reviewer": _s.workspace_id, "annotation_visible": reveal_review.value, "dataset_version": _data["manifest"]["version"]})
feedback("assessment", {"status": "saved", "case": _row["case_id"]})
''', True)
add('''
mo.stop(not train_reviewed.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_selection_record = teaching.saved(_s, "review/selection")
_parent = teaching.saved(_s, "compare/nearest-patch")
if _selection_record["config"].get("parent_stage") != _parent["id"] or feature_editor.value != _parent["sources"]["features.py"] or review_editor.value != _selection_record["sources"]["review.py"]:
    raise ValueError("The detector or review code changed. Train the current detector and select its review batch again before using those labels.")
_selection = _selection_record["result"]
_fit, _val = inspection.indices(_data, "fit"), inspection.indices(_data, "validation")
for _selection_name in ["active", "random"]:
    _chosen = np.array(_selection[_selection_name], dtype=int)
    with _s.stage("review/" + _selection_name, config={"budget": 24, "seed": 17, "label_source": "VisA published annotation", "method": "nearest-patch", "C": .03, "selection_stage": _selection_record["id"], "selected_cases": [_data["records"][i]["case_id"] for i in _chosen]}, sources={"features.py": feature_editor.value, "threshold.py": threshold_editor.value, "review.py": _selection_record["sources"]["review.py"]}) as _stage:
        if _stage.needs_run:
            def _train_reviewed_classifier():
                _model = inspection.fit_classifier(_data, np.concatenate([_fit, _chosen]), "nearest-patch", build_features=build_features, C=.03)
                _values = inspection.score(_data, _val, _model, build_features=build_features)
                _threshold = choose_threshold(inspection.labels(_data, _val), _values)
                _metrics = inspection.metrics(inspection.labels(_data, _val), _values, _threshold)
                _path = _stage.output_dir / "classifier.npz"
                _sha = inspection.save_classifier(_path, _model, _threshold)
                return {"metrics": _metrics, "model_file": _path.relative_to(_s.root).as_posix(), "model_sha256": _sha, "acquired_labels": [{"case_id": _data["records"][i]["case_id"], "label": _data["records"][i]["label"], "source": "dataset annotation, simulated review"} for i in _chosen]}
            _result, _event = event("train_reviewed_classifier", {"selection": _selection_name, "new_labels": len(_chosen), "C": .03}, _train_reviewed_classifier, on_error=_stage.record_event)
            _stage.record({**_result, "events": [_event]}, files=[_s.file(_result["model_file"])])
    try:
        export_trace(_s, _stage.id, "Train using " + _selection_name + " review labels", _stage.result.get("events", []), tool_writer=instrument_inspection_tool)
    except Exception as _error:
        feedback("publication", {"status": "trace pending", "message": str(_error)})
_s.checkpoint("review")
feedback("review_training", {"status": "complete"})
''')
add('''
mo.stop(get_step() != "review")
_s = get_lab().get("session")
mo.vstack([mo.Html(ui.result("Saved assessment", get_feedback().get("assessment", {}))), mo.Html(ui.result("Reviewed classifiers", get_feedback().get("review_training", {}))), ui.evidence(mo, _s, stage_ids=teaching.stage_ids(_s, "review/active", "review/random"), question="Open the active and random training calls. Check that each received 24 new labels and compare their validation mistakes.") if _s else mo.md("")])
''', True)
add('''
mo.stop(get_step() != "freeze")
_s = get_lab().get("session")
_rows = []
if _s:
    for _name in ["compare/whole", "compare/nearest-patch", "review/active", "review/random"]:
        _r = teaching.saved(_s, _name)
        if _r:
            _rows.append({"Version": _name, **_r["result"]["metrics"]})
freeze_choice = mo.ui.dropdown({r["Version"]: r["Version"] for r in _rows}, value=_rows[0]["Version"] if _rows else None, label="Version to take into final evaluation", disabled=not bool(_rows))
freeze_reason = mo.ui.text_area(value=_s.get_draft("inspection/freeze-reason", "") if _s else "", on_change=lambda value: _s.save_draft("inspection/freeze-reason", value) if _s else None, label="Why this detector and threshold? Include validation mistakes and review cost.", full_width=True)
freeze_inspection = mo.ui.run_button(label="Freeze models and thresholds before testing", disabled=len(_rows) != 4)
mo.vstack([mo.md("### Make the choice before seeing test results\\nCompare validation average precision, misses and false alarms below. Choose a detector and save your reason. We will evaluate all four frozen versions so the selected example remains part of the full comparison."), mo.ui.table(_rows, selection=None), freeze_choice, freeze_reason, freeze_inspection, mo.Html(ui.result("Frozen selection", get_feedback().get("freeze", {}))), ui.next_step(mo, "Next: test the frozen versions", "evaluate", go_to)])
''', True)
add('''
mo.stop(not freeze_inspection.value)
_s = get_lab()["session"]
if not freeze_reason.value.strip():
    raise ValueError("Save a short reason for your selection.")
_names = ["compare/whole", "compare/nearest-patch", "review/active", "review/random"]
_missing=[name for name in _names if not teaching.saved(_s,name)]
if _missing:
    raise ValueError("Complete both representations and both reviewed classifiers before freezing. Missing: " + ", ".join(_missing))
_versions = {name: {"stage_id": teaching.saved(_s, name)["id"], "model_file": teaching.saved(_s, name)["result"]["model_file"], "sha256": teaching.saved(_s, name)["result"]["model_sha256"], "feature_source": teaching.saved(_s, name)["sources"]["features.py"]} for name in _names}
_evaluated = teaching.saved(_s, "evaluate")
if _evaluated:
    _tested = _s.read()["stages"][_evaluated["config"]["freeze"]]
    if _tested["result"]["selected"] != freeze_choice.value or _tested["result"]["versions"] != _versions:
        raise ValueError("This workspace has already evaluated the final test boards. Keep the tested selection; use a new teaching-retest workspace for different models or choices.")
    feedback("freeze", {"status": "retained", "message": "The identical frozen version is already evaluated. Its saved results remain available; no new freeze or evaluation ran."})
else:
    with _s.stage("freeze", config={"selected": freeze_choice.value, "rationale": freeze_reason.value, "versions": _versions}) as _stage:
        if _stage.needs_run:
            _stage.record({"selected": freeze_choice.value, "rationale": freeze_reason.value, "versions": _versions})
    feedback("freeze", {"status": "complete", "selected": freeze_choice.value})
_s.checkpoint("freeze")
''', True)
add('''
mo.stop(get_step() != "evaluate")
_s = get_lab().get("session")
run_inspection_final = mo.ui.run_button(label="Evaluate all four frozen detectors on 442 test boards", disabled=not bool(_s and teaching.saved(_s, "freeze")))
retry_inspection_publication = mo.ui.run_button(label="Publish saved comparisons to Forge", disabled=not bool(_s and teaching.saved(_s, "evaluate")))
mo.vstack([mo.md("### Check boards you did not use to choose the detector\\nThis runs the frozen files and thresholds, not the current editor contents. Average precision summarizes ranking across thresholds. The operating results count missed defects and false alarms at the threshold you froze. Adding a review queue changes routing; it does not change detection quality."), run_inspection_final, retry_inspection_publication, ui.next_step(mo, "Next: reproduce and write the conclusion", "reproduce", go_to)])
''', True)
add('''
mo.stop(not run_inspection_final.value)
import hashlib as _hashlib
_s, _data = get_lab()["session"], get_lab()["data"]
_frozen = teaching.saved(_s, "freeze")
_test = inspection.indices(_data, "test")
with _s.stage("evaluate", config={"freeze": _frozen["id"]}) as _stage:
    if _stage.needs_run:
        _summaries, _versions = {}, {}
        for _name, _entry in _frozen["result"]["versions"].items():
            _path = _s.file(_entry["model_file"])
            if _hashlib.sha256(_path.read_bytes()).hexdigest() != _entry["sha256"]:
                raise ValueError("A frozen classifier file changed.")
            _model = inspection.load_classifier(_path)
            _frozen_features = teaching.functions(_entry["feature_source"])["build_features"]
            _values = inspection.score(_data, _test, _model, build_features=_frozen_features)
            _summaries[_name] = inspection.metrics(inspection.labels(_data, _test), _values, _model["threshold"], review_margin=.5)
            _versions[_name] = inspection.prediction_rows(_data, _test, _model, _model["threshold"], build_features=_frozen_features, destination=_stage.output_dir / "media", root=_s.root)
        _stage.record({"summaries": _summaries, "versions": _versions, "selected": _frozen["result"]["selected"]}, files=list((_stage.output_dir / "media").glob("*")))
_s.checkpoint("evaluate")
feedback("evaluation", {"status": "complete"})
''')
add('''
mo.stop(not retry_inspection_publication.value)
_s = get_lab()["session"]
_result = teaching.saved(_s, "evaluate")["result"]
try:
    _receipt = publish_comparison(_s, "visual-inspection-final", _result["versions"], summaries=_result["summaries"])
    feedback("publication", {"status": "published", "receipt": _receipt})
except Exception as _error:
    feedback("publication", {"status": "publication unavailable", "message": str(_error), "next": "The final results remain saved. Retry this publication button without rerunning the classifiers."})
''', True)
add('''
mo.stop(get_step() != "evaluate")
_s, _data = get_lab().get("session"), get_lab().get("data")
_final = teaching.saved(_s, "evaluate") if _s else None
_summaries = _final["result"]["summaries"] if _final else {}
_options = {r["case_id"]: i for i, r in enumerate(_data["records"]) if r["partition"] == "test"} if _final and _data else {}
final_board = mo.ui.dropdown(_options, value=next(iter(_options), None), label="Compare the same test board", disabled=not bool(_options))
mo.vstack([mo.ui.table([{"Version": name, **values} for name, values in _summaries.items()], selection=None), final_board, mo.Html(ui.result("Publication", get_feedback().get("publication", {}))), ui.publication(mo, _s), ui.evidence(mo, _s, stage_ids=teaching.stage_ids(_s, "evaluate", "freeze"), question="In the saved comparison, find a false alarm and a missed defect. Open each photo and its mask. Check that the classifier artifact matches your frozen version.") if _s else mo.md("")])
''', True)
add('''
mo.stop(get_step() != "evaluate" or final_board.value is None or not get_lab().get("data"))
_s, _data = get_lab()["session"], get_lab()["data"]
_result = teaching.saved(_s, "evaluate")["result"]
_case = _data["records"][final_board.value]["case_id"]
_scores = {name: next(row for row in rows if row["case_id"] == _case)["prediction"]["score"] for name, rows in _result["versions"].items()}
inspection.render_case(_data, final_board.value, _scores)
''', True)
add('''
mo.stop(get_step() != "reproduce")
_s = get_lab().get("session")
inspection_conclusion = mo.ui.text_area(value=_s.get_draft("inspection/conclusion", "") if _s else "", on_change=lambda value: _s.save_draft("inspection/conclusion", value) if _s else None, label="What changed, whether it helped, and what you would test next", full_width=True)
reproduce_inspection = mo.ui.run_button(label="Reload the selected classifier and reproduce one prediction", disabled=not bool(get_lab().get("session") and teaching.saved(get_lab()["session"], "evaluate")))
report_inspection = mo.ui.run_button(label="Publish my inspection Report", disabled=not bool(get_lab().get("session") and teaching.saved(get_lab()["session"], "evaluate")))
mo.vstack([mo.md("### Leave the next engineer a reproducible result\\nReload the selected file and reproduce a saved prediction. In your conclusion, separate the feature change, the extra labeled examples and the review policy. State which comparison improved and which did not. A lower missed-defect count is not a deployment guarantee."), inspection_conclusion, reproduce_inspection, mo.accordion({"Optional extension": mo.md("Link the evaluated classifier artifact to Registry if you have access. Load that exact version in a batch predictor, fail a release check, and return to the previous version. Registry tracks the selected artifact; it does not deploy this Python classifier for you.")})])
''', True)
add('''
mo.stop(get_step()!="reproduce")
_s=get_lab().get("session")
inspection_aria_conclusion=aria.investigation(mo,_s,"conclusion",interpretation=inspection_conclusion.value,workshop="visual-inspection")
mo.vstack([inspection_aria_conclusion,report_inspection])
''', True, cell_id='visual_inspection/aria/conclusion')
add('''
mo.stop(not reproduce_inspection.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_final = teaching.saved(_s, "evaluate")["result"]
_selected = _final["selected"]
_frozen = teaching.saved(_s, "freeze")["result"]["versions"][_selected]
_model = inspection.load_classifier(_s.file(_frozen["model_file"]))
_index = inspection.indices(_data, "test")[0]
_frozen_features = teaching.functions(_frozen["feature_source"])["build_features"]
_value = float(inspection.score(_data, np.array([_index]), _model, build_features=_frozen_features)[0])
_expected = _final["versions"][_selected][0]["prediction"]["score"]
np.testing.assert_allclose(_value, _expected, rtol=1e-6, atol=1e-6)
_s.checkpoint("reproduce")
feedback("reproduction", {"status": "complete", "case": _data["records"][_index]["case_id"], "saved_score": _expected, "reloaded_score": _value})
''')
add('''
mo.stop(not report_inspection.value)
_s = get_lab()["session"]
if not inspection_conclusion.value.strip():
    raise ValueError("Write your conclusion before publishing the Report.")
_s.save_draft("inspection/conclusion", inspection_conclusion.value)
try:
    _links=ui.stage_links(_s,teaching.stage_ids(_s))
    for _key,_receipt in _s.read()["publications"].items():
        if _key.startswith("comparison/"):
            _links.update(ui.comparison_links(_receipt,suffix=_key.rsplit("/",1)[-1][:6]))
    _report = publish_report(_s, inspection_conclusion.value, _links)
    feedback("report", {"status": "published", "result": _report})
except Exception as _error:
    feedback("report", {"status": "publication unavailable", "message": str(_error)})
''', True)
add('''
mo.stop(get_step() != "reproduce")
mo.vstack([mo.Html(ui.result("Reproduction check", get_feedback().get("reproduction", {}))), mo.Html(ui.result("Report", get_feedback().get("report", {})))])
''', True)
add('''
mo.stop(get_step() != "features")
recompute_encoder = mo.ui.run_button(label="Recompute four cached board features", disabled=not bool(get_lab().get("data")))
mo.accordion({"See how photographs become feature vectors": mo.vstack([mo.md("This optional CPU check downloads the pinned 45 MB ImageNet checkpoint, then recomputes four training-board feature rows. It compares the arrays with the cache; it does not train an encoder or call a model provider."), recompute_encoder])})
''', True)
add('''
mo.stop(not recompute_encoder.value)
_s, _data = get_lab()["session"], get_lab()["data"]
_weights = teaching.fetch_weights(Path("data/inspection-encoder/resnet18-f37072fd.pth"))
with _s.stage("features/recompute", config={"encoder": _data["manifest"]["encoder"], "weights_sha256": _data["manifest"]["weights_sha256"]}) as _stage:
    if _stage.needs_run:
        _result, _event = event("recompute_encoder_features", {"boards": 4}, lambda: teaching.recompute_batch(_data["root"], _weights), on_error=_stage.record_event)
        _stage.record({**_result, "events": [_event]})
try:
    _trace = export_trace(_s, _stage.id, "Recompute four cached PCB1 features", _stage.result["events"], tool_writer=instrument_inspection_tool)
    feedback("recompute", {"status": "complete", **_stage.result, "trace": _trace["url"]})
except Exception as _error:
    feedback("recompute", {"status": "export pending", "message": str(_error), "next": "Click Recompute again to retry export from the saved feature check."})
''', True)
add('''
mo.stop(get_step() != "features")
mo.Html(ui.result("Encoder cache check", get_feedback().get("recompute", {})))
''', True)
add('''
_s = get_lab().get("session")
inspection_help = mo.ui.text_area(label="What would you like help with?", full_width=True)
send_inspection_help = mo.ui.run_button(label="Send a help request", disabled=not bool(_s))
mo.accordion({"Ask the facilitator": mo.vstack([inspection_help, send_inspection_help, mo.md("This writes to your progress run. The facilitator can read the request but cannot run your notebook.")])})
''', True)
add('''
mo.stop(not send_inspection_help.value)
get_lab()["session"].request_help(inspection_help.value)
mo.md("Help request saved. Send an empty message when it is resolved.")
''', True)
add('''
_s = get_lab().get("session")
_options = _s.recovery_options() if _s else []
_choices = {r["name"] + " · " + r["id"][:6]: r["id"] for r in _options}
inspection_recovery = mo.ui.dropdown(_choices or {"No stopped executions": ""}, value=next(iter(_choices), "No stopped executions"), label="Stopped execution", disabled=not bool(_choices))
inspection_confirm_stopped = mo.ui.checkbox(label="I checked that this execution has stopped; keep uncertain requests charged at their reserved maximum")
allow_inspection_retry = mo.ui.run_button(label="Allow another attempt of this stopped execution", disabled=not bool(_choices))
mo.accordion({"Recover a stopped execution": mo.vstack([inspection_recovery, inspection_confirm_stopped, allow_inspection_retry, mo.md("This permits a retry; it does not start one. Then return to the normal run button. For a publication error, use the publication button instead. Completed sibling runs stay saved.")])})
''', True)
add('''
mo.stop(not allow_inspection_retry.value)
_s = get_lab()["session"]
_route = _s.retry_stage(inspection_recovery.value, confirm_stopped=inspection_confirm_stopped.value)
feedback("recovery", {"status": "retry allowed", "next": "Return to that step and click its run button.", "attempt": _route["attempt"]})
''', True)

# Refresh saved status after explicit actions so the next control unlocks in place.
for _cell in cells:
    if _cell.code.startswith("mo.stop(not ") and not _cell.code.startswith(("mo.stop(not connect_inspection.value)", "mo.stop(not load_inspection.value)")):
        _cell.code += "\nrefresh_inspection()"

# marimo retains callbacks for named UI objects across reactive renders.
import re as _re
for _cell in cells:
    _buttons = _re.findall(r'ui\.next_step\(mo, "[^"\n]+", "([^"\n]+)", go_to\)', _cell.code)
    for _target in _buttons:
        _pattern = r'ui\.next_step\(mo, "[^"\n]+", "' + _target + r'", go_to\)'
        _expression = _re.search(_pattern, _cell.code).group()
        _name = 'continue_inspection_' + _target
        _cell.code = _re.sub(_pattern, _name, _cell.code)
        _cell.code = _name + ' = ' + _expression + '\n' + _cell.code
