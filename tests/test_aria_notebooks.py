"""Notebook ARIA stops select saved work without executing the experiment."""
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def authored(module, stop):
    cells = importlib.import_module(module + "_cells").cells
    return next(cell for cell in cells if cell.cell_id and cell.cell_id.endswith("/aria/" + stop))


class FakeMo:
    def stop(self, condition, *args):
        if condition:
            raise RuntimeError("stopped")

    def md(self, value):
        return value

    def vstack(self, values):
        return values


class CaptureAria:
    def __init__(self):
        self.calls = []

    def investigation(self, mo, session, stop, **kwargs):
        self.calls.append((session, stop, kwargs))
        return "investigation card"


def run_stop(module, stop, scope):
    capture = CaptureAria()
    scope.update({"mo": FakeMo(), "aria": capture})
    exec(compile(authored(module, stop).code, "<authored ARIA stop>", "exec"), scope)  # noqa: S102 — exercise the checked-in cell with fake services.
    return capture.calls[-1]


def test_routing_uses_tfidf_without_waiting_for_embedding():
    session = object()
    def saved(current, name):
        assert current is session
        assert name == "routing/baseline/tfidf"
        return {"id": "word-features"}

    _, stop, context = run_stop("routing", "investigate", {
        "get_step": lambda: "baseline",
        "get_context": lambda: {"session": session},
        "get_revision": lambda: 1,
        "teaching": SimpleNamespace(saved=saved),
        "baseline_case": SimpleNamespace(value="validation-request"),
        "baseline_observation": SimpleNamespace(value="Inspect the unusual wording."),
    })
    assert stop == "investigate"
    assert context["record_ids"] == ["word-features"]
    assert context["interpretation"] == "Inspect the unusual wording."


def test_solar_uses_selected_validation_run_and_persistence():
    session = object()
    def saved(current, name):
        assert current is session
        assert name == "goes/persistence"
        return {"id": "persistence-validation"}

    _, _, context = run_stop("solar", "investigate", {
        "get_step": lambda: "search",
        "get_lab": lambda: {"session": session},
        "teaching": SimpleNamespace(saved=saved),
        "inspect_goes_run": SimpleNamespace(value="selected-validation-run"),
        "goes_diagnosis": SimpleNamespace(value="Check the output units."),
        "show_goes_repair": "closed worked answer",
    })
    assert context["record_ids"] == ["selected-validation-run", "persistence-validation"]
    assert context["interpretation"] == "Check the output units."


@pytest.mark.parametrize("review,expected", [
    (None, []),
    ({"id": "human-review", "result": {"stage_id": "reviewed-run", "reason": "The return flight remains."}}, ["human-review", "reviewed-run"]),
])
def test_airline_selects_only_the_saved_human_review(review, expected):
    _, _, context = run_stop("airline_monitoring", "investigate", {
        "get_step": lambda: "review",
        "get_context": lambda: {"session": object()},
        "get_revision": lambda: 1,
        "review_for": lambda identity: review,
        "review_case": SimpleNamespace(value="reviewed-run"),
    })
    assert context["record_ids"] == expected
    assert context["interpretation"] == ("The return flight remains." if review else "")


def test_pending_resolves_the_saved_evaluation_and_its_executions():
    _, _, context = run_stop("pending", "investigate", {
        "get_step": lambda: "evals",
        "get_pending": lambda: {"session": object()},
        "teaching": SimpleNamespace(latest=lambda *args: {
            "id": "development-evaluation", "result": {"runs": [{"stage_id": "billing"}, {"stage_id": "access"}]},
        }),
        "pending_next_step_4": "manual edit",
    })
    assert context["record_ids"] == ["development-evaluation", "billing", "access"]


@pytest.mark.parametrize("module", ["pending", "solar", "routing", "inspection", "transit", "airline_monitoring"])
def test_each_workshop_has_two_explicit_presentation_cells(module):
    import ast
    cells = importlib.import_module(module + "_cells").cells
    selected = [cell for cell in cells if cell.cell_id and "/aria/" in cell.cell_id]
    assert len(selected) == 2
    for cell in selected:
        tree = ast.parse(cell.code)
        # These are display-only stops. The shared helper owns an explicit local save.
        called = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        assert not called.intersection({"stage", "checkpoint", "publish", "run", "send", "retry_publication"})
        assert "investigation" in called
        assert any(isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and "aria_" in target.id for target in node.targets) for node in tree.body)
