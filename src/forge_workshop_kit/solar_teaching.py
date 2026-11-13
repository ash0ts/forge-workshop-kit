"""Local exercise checks and read-only reconstruction for the Solar notebook.

Training, logging and the research controller stay in the authored notebook.
These helpers never call a model, train, download data, or publish records.
"""
from __future__ import annotations

from copy import deepcopy

import numpy as np

from forge_workshop_kit.manifest import get_workshop
STEPS = tuple(tuple(step) for step in get_workshop("solar-autoresearch")["steps"])

INSTRUMENTATION_STARTER = '''def instrument_tool(observation):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=observation["name"], arguments=observation["arguments"],
        result=observation["result"], tool_call_id=observation["id"],
        started_at=stamp(observation["started_at"]), ended_at=stamp(observation["ended_at"])) as tool:
        # Add a workshop.exercise attribute with the value solar-research.
        if observation.get("error"):
            tool.record_error(RuntimeError(observation["error"]))
        return format(trace.get_current_span().get_span_context().span_id, "016x")
'''
INSTRUMENTATION_SOLUTION = INSTRUMENTATION_STARTER.replace(
    '# Add a workshop.exercise attribute with the value solar-research.',
    'tool.set_attributes({"workshop.exercise": "solar-research"})',
)

PERSISTENCE_STARTER = '''def persistence_forecast(split):
    # One latest observation is available for every forecast window.
    raise NotImplementedError("Return a copy of the latest observation.")
'''
PERSISTENCE_SOLUTION = '''def persistence_forecast(split):
    return split["persistence"].copy()
'''
FLUX_STARTER = '''def my_flux_mae(prediction, target):
    # Mean absolute error in log10 XRS-B flux units (W/m² before log10).
    raise NotImplementedError("Return the mean absolute difference.")
'''
FLUX_SOLUTION = '''def my_flux_mae(prediction, target):
    return float(np.abs(prediction - target).mean())
'''
IMAGE_METRIC_STARTER = '''def my_image_mae(prediction, target, disk_mask):
    # Average each image over its valid pixels, then average images.
    raise NotImplementedError("Ignore off-disk pixels.")
'''
IMAGE_METRIC_SOLUTION = '''def my_image_mae(prediction, target, disk_mask):
    errors = np.abs(prediction - target) * disk_mask
    per_image = errors.sum(axis=(1, 2, 3)) / disk_mask.sum(axis=(1, 2, 3))
    return float(per_image.mean())
'''
EVIDENCE_STARTER = '''def select_validation_evidence(record):
    if record.get("split") != "validation":
        raise ValueError("The researcher can only inspect validation evidence.")
    # Return the recorded fields the research agent needs. Never add test results.
    raise NotImplementedError("Select config, metrics, losses, trace and stage_id.")
'''
EVIDENCE_SOLUTION = '''def select_validation_evidence(record):
    if record.get("split") != "validation":
        raise ValueError("The researcher can only inspect validation evidence.")
    fields = ("split", "config", "metrics", "losses", "errors", "trace", "stage_id", "lessons")
    return {name: record[name] for name in fields if name in record}
'''


def functions(source):
    """Compile learner code in the notebook process; this is not a security sandbox."""
    scope = {"np": np}
    exec(compile(source, "<participant-exercise>", "exec"), scope)
    return scope


def metric_rows(versions):
    """Readable display only; full-precision metrics remain in execution records."""
    return [{"Version": name,
             "Mean error": round(values["error"], 6) if values.get("error") is not None else None,
             "Skill vs persistence": f"{values['skill_vs_persistence']:.1%}" if values.get("skill_vs_persistence") is not None else None,
             "Forecast windows": values.get("examples"),
             "Seconds": round(values["seconds"], 2) if values.get("seconds") is not None else None}
            for name, values in versions.items()]


def check_instrumentation(source):
    """Exercise the writer against an in-memory scope; no export or model call."""
    import builtins
    from datetime import datetime, timezone
    from types import SimpleNamespace

    calls = []

    class ToolReceipt:
        def __init__(self, **values):
            self.values, self.attributes, self.errors = values, {}, []
            calls.append(self)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def set_attributes(self, values):
            self.attributes.update(values)

        def record_error(self, error):
            self.errors.append(str(error))

    current = SimpleNamespace(get_span_context=lambda: SimpleNamespace(span_id=123))
    # The notebook itself uses OpenTelemetry. Override imports only inside this
    # learner function; process-wide monkeypatches can corrupt marimo's spans.
    fake_modules = {
        "coreweave.forge.agentlens": SimpleNamespace(tracing=SimpleNamespace(Tool=ToolReceipt)),
        "opentelemetry": SimpleNamespace(trace=SimpleNamespace(get_current_span=lambda: current)),
        "forge_workshop_kit.traces": SimpleNamespace(stamp=lambda value: datetime.fromtimestamp(value, tz=timezone.utc)),
    }

    def local_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in fake_modules and level == 0:
            return fake_modules[name]
        return builtins.__import__(name, globals, locals, fromlist, level)

    scope = {"__builtins__": {**vars(builtins), "__import__": local_import}}
    exec(compile(source, "<local-tracing-exercise>", "exec"), scope)
    writer = scope["instrument_tool"]
    observation = dict(name="check_example", arguments={"value": 3}, result={"answer": 6},
                       id="local-check", started_at=1.0, ended_at=2.0)
    identity = writer(observation)
    writer({**observation, "error": "Example operation failed"})
    if len(calls) != 2 or identity != "000000000000007b":
        raise ValueError("Open one Tool scope per observation and return its actual span ID.")
    for call in calls:
        if call.attributes.get("workshop.exercise") != "solar-research":
            raise ValueError('Inside the Tool scope, add tool.set_attributes({"workshop.exercise": "solar-research"}).')
        for key in ("name", "arguments", "result"):
            if call.values.get(key) != observation[key]:
                raise ValueError(f"Record the actual observation's {key}.")
        if call.values.get("tool_call_id") != observation["id"] or call.values.get("ended_at") <= call.values.get("started_at"):
            raise ValueError("Preserve the observation identity and actual start/end times.")
    if calls[0].errors or calls[1].errors != ["Example operation failed"]:
        raise ValueError("Record a supplied error, but do not invent an error for successful work.")
    return {"checks": 4, "result": "Attributes, arguments/results, timing/identity, and errors preserved. Nothing was exported."}


def check_persistence(source):
    predict = functions(source)["persistence_forecast"]
    last = np.array([[1.0], [3.0]], dtype=np.float32)
    result = predict({"persistence": last, "y": np.array([[9.0], [12.0]])})
    if not np.array_equal(result, last):
        raise ValueError("Predict the most recent observation, not the future target or their mean.")
    if np.shares_memory(result, last):
        raise ValueError("Return a copy so changing a prediction cannot edit the input observations.")
    return {"checks": 2, "result": "Latest observations copied; future targets ignored."}


def check_flux_metric(source):
    metric = functions(source)["my_flux_mae"]
    target = np.array([[2.0], [4.0]])
    if not np.isclose(metric(target + 1, target), 1):
        raise ValueError("A +1 error at every value must score 1.")
    if not np.isclose(metric(target + np.array([[-2.0], [0.0]]), target), 1):
        raise ValueError("Use absolute differences before averaging; signed errors can cancel.")
    return {"checks": 2, "result": "Absolute error and averaging match the public examples."}


def check_image_metric(source):
    metric = functions(source)["my_image_mae"]
    target = np.zeros((2, 1, 3, 3), dtype=np.float32)
    mask = np.zeros_like(target)
    mask[:, :, 1, 1] = 1
    if not np.isclose(metric(target + 1, target, mask), 1):
        raise ValueError("A +1 error on every valid pixel must score 1.")
    prediction = target.copy()
    prediction[:, :, 0, 0] = 100
    if not np.isclose(metric(prediction, target, mask), 0):
        raise ValueError("Off-disk pixels must contribute zero error.")
    return {"checks": 2, "result": "Valid pixels count; off-disk pixels do not."}


def check_evidence(source):
    select = functions(source)["select_validation_evidence"]
    example = dict(split="validation", metrics={"validation_error": 0.2}, config={"steps": 40},
                   losses=[0.4, 0.2], stage_id="example", trace={"url": "https://example.test/trace"},
                   final_test={"error": 0.01})
    result = select(deepcopy(example))
    allowed = {"split", "config", "metrics", "losses", "errors", "trace", "stage_id", "lessons"}
    if not isinstance(result, dict) or not {"split", "metrics", "stage_id"} <= result.keys():
        raise ValueError("Keep the split, metrics and exact supporting execution identity.")
    if result.keys() - allowed:
        raise ValueError("Only training/validation fields may enter the improvement prompt.")
    if any(result[key] != example[key] for key in result):
        raise ValueError("Evidence must match the recorded values; do not rewrite the scores.")
    try:
        select({**example, "split": "test"})
    except ValueError:
        return {"checks": 3, "result": "Validation evidence retained; final-test evidence rejected."}
    raise ValueError("Reject a record whose split is test.")


def model_starter(source, task):
    if task == "measurement":
        return source.replace(
            "return ((prediction-target).square()*mask).sum()/mask.sum()",
            'raise NotImplementedError("Implement masked mean squared error for training.")',
        )
    return source.replace(
        "return prediction+x[:,1:2] if architecture=='residual' else prediction",
        'raise NotImplementedError("For residual, add the current image to the predicted correction.")',
    )


def check_model(source, task):
    import torch
    from .research import validate_source
    validate_source(source)
    scope = functions(source)
    shape = (2, 60) if task == "measurement" else (2, 8, 8)
    for architecture in (("mlp", "cnn") if task == "measurement" else ("conv", "residual")):
        model = scope["build_model"](shape, {"architecture": architecture, "width": 4})
        x = torch.zeros((2, *shape))
        prediction = model(x)
        expected = (2, 1) if task == "measurement" else (2, 1, 8, 8)
        if tuple(prediction.shape) != expected:
            raise ValueError(f"{architecture} returned {tuple(prediction.shape)}; expected {expected}.")
        target = torch.zeros_like(prediction)
        loss = scope["training_loss"](prediction, target, torch.ones_like(target))
        if not torch.isfinite(loss) or loss.ndim:
            raise ValueError("training_loss must return one finite scalar.")
    return {"checks": 4, "result": "Both architectures return the required shape and a finite training loss. No training ran."}


def saved(session, name):
    rows = [row for row in session.completed() if row["name"] == name]
    return max(rows, key=lambda row: (row.get("ended_at", 0), row["id"])) if rows else None


def training_record(session, row):
    result = row["result"]
    trace = session.read()["publications"].get("trace/" + row["id"], {})
    return dict(stage_id=row["id"], source=row["sources"]["candidate.py"], config=row["config"],
                metrics=result.get("metrics", {}), losses=result.get("losses", []),
                split=row["inputs"].get("split", "validation"), trace=trace)


def restore_state(session):
    """Rebuild display state from receipts, without loading data or repeating work."""
    stages = session.completed()
    manual = [row for row in stages if row["name"].startswith("images/manual-")
              and "validation_error" in row["result"].get("metrics", {})]
    # Once research begins, its parent source is fixed even if another draft exists.
    proposal = saved(session, "images/round-1/propose")
    if proposal:
        manual = [row for row in manual if row["sources"]["candidate.py"] == proposal["sources"]["candidate.py"]]
    result = {"session": session}
    if manual:
        best = min(manual, key=lambda row: row["result"]["metrics"]["validation_error"])
        result["manual"] = training_record(session, best)
    final = saved(session, "images/final-comparison")
    if final:
        result["final"] = final["result"]
    measurement = saved(session, "goes/final")
    if measurement:
        result["goes_final"] = measurement["result"]["metrics"]
    return result


def completed_steps(session):
    names = {row["name"] for row in session.completed()}
    complete = set()
    if "setup/trace" in names and any(value.get("verified") for key, value in session.read()["publications"].items() if key.startswith("trace/")):
        complete.add("setup")
    if "data/loaded" in names:
        complete.add("data")
    if "goes/persistence" in names:
        complete.add("baseline")
    if all(f"goes/search-{number}" in names for number in range(6)):
        complete.add("search")
    if {"images/manual-conv", "images/manual-residual"} <= names:
        complete.add("images")
    if "images/round-2/adopt" in names:
        complete.add("research")
    if "images/final-comparison" in names:
        complete.add("final")
    return complete


def next_action(session):
    names = {row["name"] for row in session.completed()}
    phases = (
        ("propose", "Propose two code changes"),
        ("review-0", "Confirm review of Candidate A"),
        ("probe-result-0", "Test Candidate A"),
        ("review-1", "Confirm review of Candidate B"),
        ("probe-result-1", "Test Candidate B"),
        ("probe-done", "Record my comparison"),
        ("compose", "Request a composition"),
        ("review-composition", "Confirm review of composition"),
        ("composition-result", "Test the composition"),
        ("adopt", "Save the adopted version and lesson"),
    )
    for number in (1, 2):
        prefix = f"images/round-{number}/"
        # Previous releases already have complete rounds and need no new work.
        if prefix + "adopt" in names:
            continue
        for phase, label in phases:
            if prefix + phase not in names:
                return number, phase, label
    return 2, "done", "Both research rounds are complete"


def draft_status(session, name, current, *, stage_prefix=None):
    saved_value = session.get_draft(name)
    saved_text = "Saved in this workspace" if saved_value == current else "Not saved yet"
    if stage_prefix:
        rows = [row for row in session.completed() if row["name"].startswith(stage_prefix)]
        if rows:
            last = max(rows, key=lambda row: row.get("ended_at", 0))
            matches = last["sources"].get("candidate.py") == current
            saved_text += " · " + ("matches the last executed source" if matches else "differs from the last executed source")
    return saved_text
