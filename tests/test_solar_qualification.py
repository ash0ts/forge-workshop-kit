import importlib.util
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qualification = load(ROOT / "scripts/qualify_solar.py")
candidate = load(ROOT / "examples/solar/qualification/goes_scaled.py")


def test_residual_starts_at_persistence_in_original_units():
    import torch

    config = {"architecture": "mlp", "width": 4, "residual": True,
              "target_center": -6.1, "target_scale": .7}
    model = candidate.build_model((2, 60), config)
    x = torch.randn((5, 2, 60))
    expected = x[:, 1, -1:] * .7 - 6.1
    torch.testing.assert_close(model(x), expected)
    # The offset is a stored model buffer, so checkpoint loading retains the scale.
    assert set(model.state_dict()) >= {"center", "scale"}


def test_selection_uses_all_seeds_and_refuses_final_results():
    recipes = [{"name": "historical"}, {"name": "a"}, {"name": "b"}]
    validation = {}
    for seed, a, b in ((17, .1, .2), (29, .4, .2), (43, .4, .2)):
        for name, error in (("a", a), ("b", b)):
            validation[f"goes/{name}/{seed}"] = {
                "status": "complete", "split": "validation", "metrics": {"error": error}}
    assert qualification.selection(validation, recipes, (17, 29, 43)) == "b"
    validation["goes/b/29"]["split"] = "test"
    with pytest.raises(ValueError, match="validation"):
        qualification.selection(validation, recipes, (17, 29, 43))


def test_training_checkpoint_reproduces_scaled_predictions(tmp_path):
    from forge_workshop_kit import training

    rng = np.random.default_rng(17)
    x = rng.normal(size=(12, 2, 60)).astype("float32")
    y = x[:, 1, -1:] * .7 - 6.1 + .02
    split = {"x": x, "y": y, "mask": np.ones_like(y, dtype=bool),
             "persistence": x[:, 1, -1:] * .7 - 6.1}
    config = {"architecture": "mlp", "width": 4, "residual": True,
              "target_center": -6.1, "target_scale": .7, "seed": 17,
              "steps": 3, "learning_rate": .001, "batch_size": 4}
    source = (ROOT / "examples/solar/qualification/goes_scaled.py").read_text()
    _, initial = training.train(source, split, split, config, tmp_path / "train")
    _, restored = training.train(source, split, split, config, tmp_path / "test",
                                 weights=tmp_path / "train/weights.pt")
    np.testing.assert_array_equal(initial, restored)
    saved_inputs = np.load(tmp_path / "test/inputs.npz")
    assert saved_inputs.files == ["predict_x"]


def test_saved_complete_run_is_reused_and_request_drift_rejected(tmp_path, monkeypatch):
    protocol = {"source_sha256": {"example.py": "source"}, "dataset_sha256": "data"}
    recipe = {"name": "manual", "source": "example.py", "config": {"steps": 40}}
    request = {"key": "images/manual/17", "split": "validation", "config": {"steps": 40, "seed": 17},
               "source_sha256": "source", "dataset_sha256": "data", "weights_sha256": None}
    record = {"request": request, "status": "complete", "files": {}}
    qualification.save(tmp_path / "validation/images/manual/17/result.json", record)
    monkeypatch.setattr(qualification.training, "train", lambda *args, **kwargs: pytest.fail("Duplicate training"))
    assert qualification.run_one(protocol, tmp_path, "images", recipe, 17, "validation", {}, {}) == record
    recipe["config"]["steps"] = 41
    with pytest.raises(ValueError, match="differs"):
        qualification.run_one(protocol, tmp_path, "images", recipe, 17, "validation", {}, {})


def test_worked_notebook_config_matches_qualified_recipe():
    from forge_workshop_kit.solar_teaching import measurement_repair_config

    normalization = {"mean": [[[-7.0], [-6.1]]], "std": [[[.8], [.7]]]}
    config = measurement_repair_config(normalization)
    qualified = next(r for r in qualification.goes_recipes() if r["name"] == "mlp-residual-1200")
    assert config == {**qualified["config"], "seed": 17, "target_center": -6.1, "target_scale": .7}
