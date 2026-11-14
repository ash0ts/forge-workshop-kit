from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from forge_workshop_kit import solar_views as views


def test_window_toggle_preserves_target_and_latest_reading():
    split = {"x": np.ones((1, 2, 60)), "y": np.array([[-5.5]]),
             "persistence": np.array([[-6.0]]), "ids": np.array(["2014-02-01T00:59"])}
    normalization = {"mean": [[[-8], [-7]]], "std": [[[.5], [1.0]]]}
    raw = views.window_values(split, normalization)
    normalized = views.window_values(split, normalization, standardized=True)
    assert raw["inputs"][1, -1] == -6
    assert normalized["inputs"][1, -1] == 1
    assert raw["target"] == normalized["target"] == -5.5
    assert raw["persistence"] == normalized["persistence"] == -6


def test_public_fixture_weights_images_equally_and_ignores_excluded_pixels():
    inside = views.scorer_fixture(-2, inside=True)
    assert [row["Included pixels"] for row in inside["rows"]] == [1, 4]
    assert [row["Per-image MAE"] for row in inside["rows"]] == [2, 4]
    assert inside["expected"] == 3  # Not the pixel-weighted 18/5.
    assert views.scorer_fixture(3, inside=False)["expected"] == 0


def test_actual_forward_shapes_use_authored_code_without_fitting_or_changing_rng():
    import torch
    source = (Path(__file__).resolve().parents[1] / "examples/solar/candidate.py").read_text()
    source = source[:source.index("def fit(")] + 'def fit(*args):\n    raise AssertionError("Must not train")\n'
    before = torch.get_rng_state().clone()
    mlp = views.forward_shapes(source, "mlp")
    cnn = views.forward_shapes(source, "cnn")
    assert torch.equal(before, torch.get_rng_state())
    assert mlp[0]["Output shape"] == [2, 120]
    assert cnn[0]["Output shape"] == [2, 4, 60]
    assert mlp[-1]["Output shape"] == cnn[-1]["Output shape"] == [2, 1]


def test_aligned_images_share_scales_and_keep_case_score_separate_from_mean():
    split = {"y": np.zeros((2, 1, 3, 3)), "mask": np.ones((2, 1, 3, 3)),
             "ids": np.array(["2014-02-13T01:00", "2014-02-13T01:12"])}
    predictions = {"Manual": np.stack([np.ones((1, 3, 3)), 3*np.ones((1, 3, 3))]),
                   "Agent": np.zeros((2, 1, 3, 3))}
    figure, rows = views.aligned_images(predictions, split)
    assert rows[0]["This image MAE"] == 1
    assert rows[0]["All images MAE"] == 2
    assert len({axis.images[0].get_clim() for axis in figure.axes[:3]}) == 1
    assert figure.axes[4].images[0].get_clim() == figure.axes[5].images[0].get_clim()
    plt.close(figure)


def test_saved_prediction_missing_file_stays_unavailable(tmp_path):
    row = {"id": "test", "name": "images/final-agent", "ended_at": 1}
    class Session:
        def completed(self):
            return [row]
        def file(self, name):
            return tmp_path / name
    predictions, records, missing = views.saved_predictions(Session(), {"Agent": row["name"]}, {"y": np.zeros((2, 1, 3, 3))})
    assert not predictions and not records
    assert "unavailable" in missing["Agent"]


def test_figures_render_without_any_provider_or_training(tmp_path):
    fixture = views.scorer_fixture()
    figure = views.fixture_figure(fixture)
    figure.savefig(tmp_path / "fixture.png")
    plt.close(figure)

    split = {"y": np.array([[-6.0], [-5.5]]), "persistence": np.array([[-6.2], [-6.0]]),
             "ids": np.array(["2014-02-13T01:00", "2014-02-13T01:01"])}
    figure = views.goes_investigation(np.array([[-3.0], [-2.5]]), split, losses=[3, 2, 1])
    figure.savefig(tmp_path / "goes.png")
    assert len(figure.axes[1].lines) == 3
    plt.close(figure)


def test_check_feedback_does_not_redefine_or_retrigger_its_writer():
    import sys
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "scripts"))
    from solar_cells import cells
    from notebook_builder import analyze
    definitions, references, owners = analyze(cells)
    owner = owners["checked"]
    assert definitions[owner] == {"checked"}
    assert "get_feedback" not in references[owner]
    assert "get_lab" not in references[owner]
    assert "set_feedback(lambda current:" in cells[owner].code


def test_failed_authored_scorer_keeps_error_and_current_check_identity():
    import ast
    import hashlib
    import sys
    from types import SimpleNamespace
    from forge_workshop_kit import solar_teaching as teaching
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "scripts"))
    from solar_cells import cells
    cell = next(cell for cell in cells if 'checked("fixture-score", _try)' in cell.code)
    function = next(node for node in ast.parse(cell.code).body if isinstance(node, ast.FunctionDef))
    source = 'def my_image_mae(prediction, target, disk_mask):\n    raise ValueError("Finish the per-image average before checking this example.")\n'
    digest = lambda value: hashlib.sha256(value.encode()).hexdigest()
    namespace = dict(views=views, teaching=teaching, np=np, digest=digest,
                     fixture_error=SimpleNamespace(value=1), fixture_inside=SimpleNamespace(value=True),
                     image_metric_editor=SimpleNamespace(value=source))
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<scorer-check>", "exec"), namespace)
    result = namespace["_try"]()
    assert result["status"] == "needs work"
    assert result["message"] == "Finish the per-image average before checking this example."
    assert result["source"] == digest(source)
    assert result["fixture"] == [1, True]
    assert result["Expected"] == 1.5


def test_aligned_comparison_exposes_actual_timestamp_and_readable_width():
    split = {"y": np.zeros((2, 1, 3, 3)), "mask": np.ones((2, 1, 3, 3)),
             "ids": np.array(["2014-02-13T02:48", "2014-02-13T03:00"])}
    figure, rows = views.aligned_images({"Manual": np.ones_like(split["y"])}, split, index=1)
    html = views.comparison_html(figure, split["ids"][1])
    assert 'data-forecast-origin="2014-02-13T03:00"' in html
    assert 'min-width:720px' in html and 'width:100%' in html
    assert rows[0]["Forecast origin UTC"] == "2014-02-13T03:00"
    assert figure.axes[3].get_title() == "Absolute error"
    plt.close(figure)


def test_final_goes_curve_uses_exact_selected_training_execution():
    import sys
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "scripts"))
    from solar_cells import cells
    cell = next(cell for cell in cells if '"Frozen GOES model"' in cell.code)
    assert '_row.get("inputs", {}).get("selected_stage")' in cell.code
    assert 'row["id"] == _selected_training_id' in cell.code
    assert 'max(_training_rows' not in cell.code
    assert 'no other run is substituted' in cell.code


def test_completed_comparison_does_not_mix_in_a_later_partial_final_attempt(tmp_path):
    shape = (2, 1, 3, 3)
    rows = [
        {"id": "manual-old", "name": "images/final-manual", "ended_at": 1},
        {"id": "agent-old", "name": "images/final-agent", "ended_at": 2},
        # A retry completed only manual before interruption; no new comparison exists.
        {"id": "manual-retry", "name": "images/final-manual", "ended_at": 10},
        {"id": "goes-old", "name": "goes/final", "ended_at": 3,
         "inputs": {"selected_stage": "training-old"}},
        {"id": "goes-retry", "name": "goes/final", "ended_at": 11,
         "inputs": {"selected_stage": "training-retry"}},
    ]
    class Session:
        def completed(self):
            return rows
        def file(self, name):
            return tmp_path / name
    session = Session()
    for identity, value in (("manual-old", 1), ("agent-old", 2), ("manual-retry", 9)):
        path = session.file(f"outputs/{identity}/predictions.npy")
        path.parent.mkdir(parents=True)
        np.save(path, np.full(shape, value))
    comparison = {"result": {"rows": {
        "manual": [{"evidence": {"stage": "manual-old"}}],
        "agent": [{"evidence": {"stage": "agent-old"}}],
        "selected-model": [{"evidence": {"stage": "goes-old"}}],
    }}}
    versions = {"Manual": "manual", "Agent": "agent"}
    executions = {label: views.comparison_execution(session, comparison, version)
                  for label, version in versions.items()}
    names = {"Manual": "images/final-manual", "Agent": "images/final-agent"}
    predictions, records, missing = views.saved_predictions(session, names, {"y": np.zeros(shape)}, executions=executions)
    assert not missing
    assert predictions["Manual"].mean() == 1 and predictions["Agent"].mean() == 2
    assert records["Manual"]["id"] == "manual-old"
    goes = views.comparison_execution(session, comparison, "selected-model")
    assert goes["inputs"]["selected_stage"] == "training-old"
    # Latest-per-name remains available for the validation-run inspector.
    latest, _, _ = views.saved_predictions(session, {"Manual": names["Manual"]}, {"y": np.zeros(shape)})
    assert latest["Manual"].mean() == 9
    # Missing selected files never substitute newer predictions.
    session.file("outputs/manual-old/predictions.npy").unlink()
    predictions, _, missing = views.saved_predictions(session, names, {"y": np.zeros(shape)}, executions=executions)
    assert "Manual" not in predictions and "unavailable" in missing["Manual"]
    # Missing referenced execution remains missing even if another final run exists.
    rows[:] = [row for row in rows if row["id"] != "agent-old"]
    assert views.comparison_execution(session, comparison, "agent") is None
    executions["Agent"] = None
    _, _, missing = views.saved_predictions(session, names, {"y": np.zeros(shape)}, executions=executions)
    assert "referenced by the saved comparison" in missing["Agent"]
    # A completed retry comparison can explicitly select the newer execution.
    comparison["result"]["rows"]["manual"][0]["evidence"]["stage"] = "manual-retry"
    assert views.comparison_execution(session, comparison, "manual")["id"] == "manual-retry"


def test_timestamp_choice_survives_control_reconstruction_and_is_split_specific():
    import sys
    from types import SimpleNamespace
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "scripts"))
    from solar_cells import cells
    cell = next(cell for cell in cells if 'comparison_timestamp = mo.ui.dropdown' in cell.code)
    class Session:
        drafts = {}
        def get_draft(self, key, default=None):
            return self.drafts.get(key, default)
        def save_draft(self, key, value):
            self.drafts[key] = value
    session = Session()
    ids = np.array(["2014-02-13T02:48", "2014-02-13T03:00"])
    state = {"step": "final"}
    context = {"session": session, "dataset": "data-v1",
               "images": {"test": {"ids": ids}, "validation": {"ids": ids}}}
    def stop(condition, *args):
        assert not condition
    fake_mo = SimpleNamespace(stop=stop, md=lambda value: value, vstack=lambda value: value,
                              ui=SimpleNamespace(dropdown=lambda options, **kwargs: kwargs))
    namespace = dict(mo=fake_mo, get_step=lambda: state["step"], get_lab=lambda: context,
                     teaching=SimpleNamespace(saved=lambda *args: {"id": "comparison"}))
    exec(cell.code, namespace)
    control = namespace["comparison_timestamp"]
    assert control["value"] == ids[0] + " UTC"
    control["on_change"](1)
    exec(cell.code, namespace)  # A late parent update recreates the control.
    assert namespace["comparison_timestamp"]["value"] == ids[1] + " UTC"
    state["step"] = "images"
    exec(cell.code, namespace)
    assert namespace["comparison_timestamp"]["value"] == ids[0] + " UTC"
    state["step"] = "final"
    exec(cell.code, namespace)
    assert namespace["comparison_timestamp"]["value"] == ids[1] + " UTC"
