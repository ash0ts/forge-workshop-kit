"""Qualify fixed Solar teaching recipes without inference or network calls.

Run freeze, validate, evaluate, then summarize. Each step is explicit. Completed
executions are read from disk; an interrupted execution is never rerun implicitly.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from forge_workshop_kit import solar, training

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = "solar-fixed-recipes-2026-11-14"
SEEDS = (17, 29, 43)


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(path.suffix + ".tmp")
    pending.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    pending.replace(path)


def image_recipes():
    return [
        {"name": name, "source": f"examples/solar/qualification/{source}.py",
         "config": {"architecture": "residual", "width": 8, "learning_rate": .001,
                    "steps": 40, "batch_size": 8}}
        for name, source in (("manual", "image_manual"), ("mae", "image_mae"),
                             ("zero_residual", "image_zero_residual"))
    ]


def goes_recipes():
    rows = [{"name": "historical", "source": "examples/solar/qualification/goes_historical.py",
             "config": {"architecture": "mlp", "width": 16, "learning_rate": .003,
                        "steps": 60, "batch_size": 32}}]
    for architecture in ("mlp", "cnn"):
        for residual in (False, True):
            for steps in (400, 1200):
                rows.append({"name": f"{architecture}-{'residual' if residual else 'direct'}-{steps}",
                             "source": "examples/solar/qualification/goes_scaled.py",
                             "config": {"architecture": architecture, "residual": residual,
                                        "width": 16, "learning_rate": .001,
                                        "steps": steps, "batch_size": 64}})
    return rows


def freeze(data, evidence):
    path = evidence / "protocol.json"
    if path.exists():
        raise ValueError("This protocol already exists. Reuse it; do not overwrite a frozen experiment.")
    recipes = {"images": image_recipes(), "goes": goes_recipes()}
    sources = {r["source"]: checksum(ROOT / r["source"]) for rows in recipes.values() for r in rows}
    value = {
        "identity": IDENTITY, "frozen_at": datetime.now(UTC).isoformat(),
        "question": "Do fixed image edits repeat across seeds, and can a bounded scaled GOES recipe beat persistence?",
        "seeds": list(SEEDS), "dataset_sha256": solar.verify_data(data),
        "recipes": recipes, "source_sha256": sources,
        "scorer_sha256": checksum(ROOT / "src/forge_workshop_kit/solar.py"),
        "worker_sha256": checksum(ROOT / "src/forge_workshop_kit/worker.py"),
        "partitions": solar.SPLITS,
        "selection": "Images: evaluate all three fixed arms. GOES: select one scaled recipe by mean validation MAE across all three seeds; break ties by recipe name. Evaluate selected recipe and historical control on all seeds.",
        "acceptance": {"images": "zero_residual has lower final mean masked MAE than manual for every seed",
                       "goes": "selected scaled recipe has lower final log-flux MAE than persistence for every seed"},
        "units": {"images": "mean absolute standardized log1p intensity error on target disk",
                  "goes": "mean absolute log10 XRS-B flux error"},
        "aggregation": "Average windows within each seed, report every seed and their arithmetic mean. Windows overlap; seeds repeat the same dates and are not additional datasets.",
        "scope": "Training and validation dates choose GOES recipe. February 13-14 were inspected in the earlier rehearsal; this is a teaching retest, not a new unseen benchmark. No agent calls or new agent adaptations.",
        "failure_policy": "Retain every failed attempt. Do not replace it automatically or omit its outcome. Fail qualification if a required run is unavailable.",
        "timeout_seconds": 180, "cpu_threads": 2, "provider_cost_usd": 0,
        "compute": "Existing local CPU; no newly billed compute requested.",
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        **{name: importlib.metadata.version(name) for name in ("torch", "numpy", "pandas")}},
        "reproduction": "uv run python scripts/qualify_solar.py freeze|validate|evaluate|summarize",
    }
    save(path, value)
    return value


def load_protocol(data, evidence):
    value = json.loads((evidence / "protocol.json").read_text())
    if solar.verify_data(data) != value["dataset_sha256"]:
        raise ValueError("Dataset changed after protocol freeze.")
    for path, expected in value["source_sha256"].items():
        if checksum(ROOT / path) != expected:
            raise ValueError("Candidate source changed after protocol freeze: " + path)
    for key, path in (("scorer_sha256", "solar.py"), ("worker_sha256", "worker.py")):
        if checksum(ROOT / "src/forge_workshop_kit" / path) != value[key]:
            raise ValueError("Scoring or execution changed after protocol freeze.")
    return value


def selection(validation, recipes, seeds):
    """Choose the GOES recipe only from complete validation records."""
    candidates = []
    for recipe in recipes:
        if recipe["name"] == "historical":
            continue
        rows = [validation[f"goes/{recipe['name']}/{seed}"] for seed in seeds]
        if any(row["status"] != "complete" or row["split"] != "validation" for row in rows):
            raise ValueError("Every planned validation run must finish before selecting a recipe.")
        candidates.append((float(np.mean([row["metrics"]["error"] for row in rows])), recipe["name"]))
    return min(candidates)[1]


def run_one(protocol, state, task, recipe, seed, split, splits, normalization, weights=None):
    key = f"{task}/{recipe['name']}/{seed}"
    folder = state / split / key
    result_path = folder / "result.json"
    config = {**recipe["config"], "seed": seed}
    if task == "goes" and recipe["name"] != "historical":
        config.update(target_center=normalization["mean"][0][1][0],
                      target_scale=normalization["std"][0][1][0])
    request = {"key": key, "split": split, "config": config,
               "source_sha256": protocol["source_sha256"][recipe["source"]],
               "dataset_sha256": protocol["dataset_sha256"],
               "weights_sha256": checksum(weights) if weights else None}
    if result_path.exists():
        result = json.loads(result_path.read_text())
        if result["request"] != request:
            raise ValueError("Saved request differs. Use a new experiment identity.")
        if result["status"] == "running":
            raise ValueError("Interrupted work retained. Inspect it before an explicit new attempt: " + str(folder))
        if result["status"] == "complete":
            for name, expected in result["files"].items():
                if checksum(folder / name) != expected:
                    raise ValueError("Saved execution file changed: " + str(folder / name))
        return result
    record = {"request": request, "key": key, "split": split, "status": "running",
              "started_at": datetime.now(UTC).isoformat()}
    save(result_path, record)
    started = time.perf_counter()
    try:
        output, prediction = training.train(
            (ROOT / recipe["source"]).read_text(), splits["train"], splits[split], config,
            folder, timeout=protocol["timeout_seconds"], weights=weights,
        )
        errors = solar.errors(prediction, splits[split]["y"], splits[split]["mask"])
        record.update(status="complete", metrics=output["metrics"], losses=output["losses"],
                      errors=[{"case_id": str(case), "error": float(error)}
                              for case, error in zip(splits[split]["ids"], errors, strict=True)],
                      files={name: checksum(folder / name) for name in (
                          "candidate.py", "weights.pt", "predictions.npy", "losses.json", "request.json")})
    except Exception as error:  # noqa: BLE001 - retain failures from participant candidate code.
        record.update(status="failed", error=type(error).__name__ + ": " + str(error))
    record.update(elapsed_seconds=time.perf_counter() - started,
                  ended_at=datetime.now(UTC).isoformat())
    save(result_path, record)
    print(key, split, record["status"], record.get("metrics", {}).get("error"), flush=True)
    return record


def execute(action, data, state, evidence, protocol):
    loaded = {"images": solar.load_aia(data), "goes": solar.load_goes(data)}
    validation_path = evidence / "validation.json"
    if action == "validate":
        records = {}
        for task, recipes in protocol["recipes"].items():
            for recipe in recipes:
                for seed in protocol["seeds"]:
                    result = run_one(protocol, state, task, recipe, seed, "validation", *loaded[task])
                    records[result["key"]] = result
                    save(validation_path, records)
        return
    validation = json.loads(validation_path.read_text())
    expected = sum(len(rows) for rows in protocol["recipes"].values()) * len(protocol["seeds"])
    if len(validation) != expected or any(row["status"] != "complete" for row in validation.values()):
        raise ValueError("Final evaluation requires every planned validation run, including controls.")
    chosen = selection(validation, protocol["recipes"]["goes"], protocol["seeds"])
    frozen = {"validation_sha256": checksum(validation_path), "goes_recipe": chosen,
              "source_and_weights": {key: {"source": row["request"]["source_sha256"],
                                            "weights": row["files"]["weights.pt"]}
                                     for key, row in validation.items()},
              "evaluation_kind": "Known final dates: teaching retest"}
    freeze_path = evidence / "evaluation-freeze.json"
    if freeze_path.exists() and json.loads(freeze_path.read_text()) != frozen:
        raise ValueError("The selected sources or weights changed after the evaluation freeze.")
    if not freeze_path.exists():
        save(freeze_path, frozen)
    records = {}
    for task, recipes in protocol["recipes"].items():
        for recipe in recipes:
            if task == "goes" and recipe["name"] not in ("historical", chosen):
                continue
            for seed in protocol["seeds"]:
                key = f"{task}/{recipe['name']}/{seed}"
                weights = state / "validation" / key / "weights.pt"
                if checksum(weights) != frozen["source_and_weights"][key]["weights"]:
                    raise ValueError("Frozen training weights changed before evaluation.")
                result = run_one(protocol, state, task, recipe, seed, "test", *loaded[task], weights=weights)
                records[key] = result
                save(evidence / "evaluation.json", records)


def summarize(evidence, protocol):
    validation = json.loads((evidence / "validation.json").read_text())
    evaluation = json.loads((evidence / "evaluation.json").read_text())
    frozen = json.loads((evidence / "evaluation-freeze.json").read_text())
    rows = []
    image_pass, goes_pass = [], []
    for seed in protocol["seeds"]:
        image = {name: evaluation[f"images/{name}/{seed}"] for name in ("manual", "mae", "zero_residual")}
        selected = evaluation[f"goes/{frozen['goes_recipe']}/{seed}"]
        historical = evaluation[f"goes/historical/{seed}"]
        for task, arms in (("images", image), ("goes", {"historical": historical, frozen["goes_recipe"]: selected})):
            for name, result in arms.items():
                rows.append({"task": task, "recipe": name, "seed": seed, "status": result["status"],
                             "error": result.get("metrics", {}).get("error"),
                             "persistence_error": result.get("metrics", {}).get("persistence_error"),
                             "examples": result.get("metrics", {}).get("examples")})
        image_pass.append(all(r["status"] == "complete" for r in image.values()) and
                          image["zero_residual"]["metrics"]["error"] < image["manual"]["metrics"]["error"])
        goes_pass.append(selected["status"] == "complete" and
                         selected["metrics"]["error"] < selected["metrics"]["persistence_error"])
    result = {"identity": protocol["identity"], "seeds": protocol["seeds"], "rows": rows,
              "image_qualified": all(image_pass), "goes_qualified": all(goes_pass),
              "selected_goes_recipe": frozen["goes_recipe"],
              "completed_training_executions": sum(r["status"] == "complete" for r in validation.values()),
              "completed_final_executions": sum(r["status"] == "complete" for r in evaluation.values()),
              "elapsed_training_seconds": sum(r["elapsed_seconds"] for r in validation.values()),
              "elapsed_evaluation_seconds": sum(r["elapsed_seconds"] for r in evaluation.values()),
              "inference_calls": 0, "provider_cost_usd": 0,
              "scope": protocol["scope"], "aggregation": protocol["aggregation"]}
    save(evidence / "summary.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "validate", "evaluate", "summarize"))
    parser.add_argument("--data", type=Path, default=ROOT / "data/solar-v1")
    parser.add_argument("--state", type=Path, default=ROOT / ".workshop/solar-fixed-recipes-2026-11-14")
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence/solar-fixed-recipes-2026-11-14")
    args = parser.parse_args()
    if args.action == "freeze":
        print(json.dumps(freeze(args.data, args.evidence), indent=2))
        return
    protocol = load_protocol(args.data, args.evidence)
    if args.action == "summarize":
        print(json.dumps(summarize(args.evidence, protocol), indent=2))
    else:
        execute(args.action, args.data, args.state, args.evidence, protocol)


if __name__ == "__main__":
    main()
