"""Rehearse current authored cells, or inspect saved records without execution.

Replay deliberately uses only JSON and pathlib. Live mode imports marimo only
when requested. It is an interactive action adapter, not a claim that a complete
workshop or a browser session has been tested.
"""

from __future__ import annotations

import ast
import hashlib
import html
import json
import os
import re
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

from .authoring import cell_info, load_cells, metadata, script_imports

COVERAGE = {
    "free_checks": "not run",
    "authored_notebook_execution": "not run",
    "browser": "not run",
    "external_account": "unknown",
    "human_rehearsal": "unknown",
}


def replay(state, *, expected_workshop=None):
    """Read exactly one existing journal; never create a session or publish it."""
    root = Path(state)
    journal = root if root.is_file() else root / "journal.json"
    record = json.loads(journal.read_text(encoding="utf-8"))
    identity_path = journal.parent / "identity.json"
    identity = (
        json.loads(identity_path.read_text(encoding="utf-8")) if identity_path.exists() else {}
    )
    if expected_workshop and identity.get("workshop") != expected_workshop:
        raise ValueError(
            "The saved workspace belongs to another workshop or has no identity record."
        )
    rows = [
        {
            "id": key,
            "name": value.get("name"),
            "status": value.get("status"),
            "attempt": value.get("attempt"),
            "result_available": value.get("result") is not None,
        }
        for key, value in record.get("stages", {}).items()
    ]
    return {
        "mode": "replay",
        "identity": identity,
        "stages": rows,
        "progress": record.get("progress", {}),
        "publication_count": len(record.get("publications", {})),
        "requests": dict(
            Counter(row.get("status", "unknown") for row in record.get("requests", {}).values())
        ),
        "coverage": {**COVERAGE, "saved_evidence": "read only; no execution or publication"},
    }


@contextmanager
def live_environment(project, state, budget):
    if not project or len(project.split("/")) != 2:
        raise ValueError("Live rehearsal requires --project entity/project.")
    if not 0 < float(budget) < float("inf"):
        raise ValueError("The inference allowance must be positive and finite.")
    values = {"WORKSHOP_PROJECT": project, "WORKSHOP_STATE_DIR": str(Path(state).resolve())}
    # Local rehearsal must never inherit another hosted notebook's identity.
    keys = set(values) | {
        "WANDB_NOTEBOOK_ANCHOR_RUN",
        "WANDB_NOTEBOOK_COLLECTION",
        "WANDB_ENTITY",
        "WANDB_PROJECT",
    }
    previous = {key: os.environ.get(key) for key in keys}
    try:
        for key in keys:
            os.environ.pop(key, None)
        os.environ.update(values)
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


class AuthoredAdapter:
    """Execute selected action bodies with current widgets, hooks, and gates.

    The adapter only replaces output rendering. It never fills in worked
    answers, accepts a diff, or chooses a release for the operator.
    """

    def __init__(self, root, slug, *, project, state, budget_usd=8, output=print):
        self.root, self.slug = Path(root), slug
        self.cells = load_cells(root, slug)
        self.project, self.state, self.budget = project, Path(state), budget_usd
        self.output = output
        self.scope = {"__name__": "__workshop_rehearsal__"}
        self.initialized = set()
        self.inputs = {}
        self.history = []
        self.refresh_errors = {}
        self.blocked_cells = {}
        with script_imports(root):
            from notebook_builder import analyze

            definitions, references, _ = analyze(self.cells)
        self.definitions = dict(zip((c.cell_id for c in self.cells), definitions))
        self.references = dict(zip((c.cell_id for c in self.cells), references))
        self.source_hash = hashlib.sha256(
            "\n".join(c.code for c in self.cells).encode()
        ).hexdigest()
        self.controls = {name for cell in self.cells for name in cell_info(cell)["controls"]}
        self.actions = {cell.cell_id: cell for cell in self.cells if cell_info(cell)["actions"]}

    def _render(self, value):
        # HTML and markdown output are useful for reading candidate diffs. The
        # browser remains the appropriate place to validate visual readability.
        text = str(getattr(value, "text", value))
        text = re.sub(
            r"<(style|script|svg)\b[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE
        )
        text = re.sub(
            r"</(?:p|div|section|h[1-6]|pre|tr|li)>|<br\s*/?>", "\n", text, flags=re.IGNORECASE
        )
        text = html.unescape(re.sub(r"<[^>]*>", "", text))
        text = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())
        if text:
            self.output(text)

    def _execute(self, cell):
        local_scope = dict(self.scope)
        tree = ast.parse(cell.code, filename=cell.cell_id)
        # Display the final expression, as marimo does, rather than discarding
        # the candidate diff or the prerequisite message in a console runner.
        expression = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        exec(compile(tree, cell.cell_id, "exec"), local_scope)  # noqa: S102 — reviewed local notebook source, not a sandbox.
        if expression is not None:
            value = eval(
                compile(ast.Expression(expression.value), cell.cell_id, "eval"), local_scope
            )
            if value is not None:
                self._render(value)
        if "mo" in local_scope:
            import marimo

            local_scope["mo"] = _display_proxy(marimo, self._render)
        for name in self.definitions[cell.cell_id]:
            if name in local_scope:
                self.scope[name] = local_scope[name]

    def _set_widget(self, name, value):
        widget = self.scope.get(name)
        if widget is None or not hasattr(widget, "_update"):
            raise ValueError(f"{name!r} is not a currently available notebook input.")
        if name in self.controls:
            raise ValueError("Run controls are invoked with run CELL_ID, not set.")
        widget._update(value)

    def refresh(self):
        """Refresh passive cells only; never revisit a completed action cell."""
        from marimo._runtime.control_flow import MarimoStopError

        errors, blocked = {}, {}
        pending = []
        for cell in self.cells:
            info = cell_info(cell)
            if info["actions"] or (info["state"] and cell.cell_id in self.initialized):
                continue
            pending.append(cell)
            # A hidden section must not leave yesterday's widgets available.
            for name in self.definitions[cell.cell_id]:
                self.scope.pop(name, None)
        while pending:
            ready = [
                cell
                for cell in pending
                if all(name in self.scope for name in self.references[cell.cell_id])
            ]
            if not ready:
                for cell in pending:
                    blocked[cell.cell_id] = "Unavailable inputs: " + ", ".join(
                        name for name in self.references[cell.cell_id] if name not in self.scope
                    )
                break
            for cell in ready:
                pending.remove(cell)
                info = cell_info(cell)
                try:
                    self._execute(cell)
                    if info["state"]:
                        self.initialized.add(cell.cell_id)
                    for name in self.definitions[cell.cell_id]:
                        if name in self.inputs:
                            self._set_widget(name, self.inputs[name])
                        elif name in ("allowance", "pending_allowance", "inspection_allowance"):
                            self._set_widget(name, self.budget)
                except MarimoStopError:
                    blocked[cell.cell_id] = "Hidden or waiting for its notebook prerequisite"
                except Exception as error:  # noqa: BLE001 — report the boundary failure without retrying execution.
                    errors[cell.cell_id] = f"{type(error).__name__}: {error}"
        self.refresh_errors, self.blocked_cells = errors, blocked
        return errors

    def set_input(self, name, value):
        if (
            name in ("project", "project_input", "pending_project", "inspection_project")
            and value != self.project
        ):
            raise ValueError(
                "The rehearsal project is fixed by --project. Use a separate state directory for another project."
            )
        if name in ("allowance", "pending_allowance", "inspection_allowance") and float(
            value
        ) != float(self.budget):
            raise ValueError("Change the rehearsal allowance with --budget-usd before starting.")
        if getattr(self.scope.get(name), "_component_args", {}).get("disabled", False):
            raise ValueError("This input is disabled; complete its prerequisite first.")
        self._set_widget(name, value)
        self.inputs[name] = value
        # Editing is not a request to run an action, including checks.

    def navigate(self, step):
        row = metadata(self.root, self.slug)
        if step not in dict(row["steps"]):
            raise ValueError("Unknown step. Choose one from the workshop manifest.")
        setter = self.scope.get("set_step")
        if setter is None:
            raise ValueError("This notebook has no supported step navigation adapter.")
        setter(step)
        self.refresh()

    def available_actions(self):
        rows = []
        for identity, cell in self.actions.items():
            control = cell_info(cell)["actions"][0]
            widget = self.scope.get(control)
            args = getattr(widget, "_component_args", {})
            rows.append(
                {
                    "cell_id": identity,
                    "control": control,
                    "label": getattr(getattr(widget, "_args", None), "label", None) or control,
                    "available": widget is not None and not args.get("disabled", False),
                }
            )
        return rows

    def run(self, identity):
        from marimo._runtime.control_flow import MarimoStopError

        cell = self.actions.get(identity)
        if cell is None:
            raise ValueError("Select an exact action cell ID from list.")
        control = cell_info(cell)["actions"][0]
        widget = self.scope.get(control)
        if widget is None:
            raise ValueError(f"{control} is not available. Navigate to its step first.")
        if getattr(widget, "_component_args", {}).get("disabled", False):
            raise ValueError(
                "This control is disabled. Read and complete the notebook prerequisite first."
            )
        start = time.time()
        record = {
            "cell_id": identity,
            "source_sha256": hashlib.sha256(cell.code.encode()).hexdigest(),
            "started_at": start,
            "status": "started",
        }
        self.history.append(record)
        try:
            widget._update(1)
            self._execute(cell)
            record["status"] = "returned"
        except MarimoStopError as error:
            record.update(status="blocked", error=str(error))
            self._render(error)
        except Exception as error:
            record.update(status="raised", error=f"{type(error).__name__}: {error}")
            raise
        finally:
            widget._update(0)
            # Review acknowledgments apply to one action, never to the next diff.
            for name in list(self.inputs):
                if type(self.scope.get(name)).__name__ == "checkbox":
                    self.inputs.pop(name)
                    self.scope[name]._update(False)
            record["ended_at"] = time.time()
            self.save_receipt()
        self.refresh()
        return record

    def receipt(self):
        return {
            "schema_version": 1,
            "mode": "live",
            "workshop": self.slug,
            "project": self.project,
            "allowance_usd": self.budget,
            "authored_source_sha256": self.source_hash,
            "actions": self.history,
            "coverage": {
                **COVERAGE,
                "authored_notebook_execution": "selected action cells only"
                if self.history
                else "not run",
            },
            "limitations": [
                "A returned cell may contain a handled error; inspect its saved stage and displayed result.",
                "Console execution does not verify browser interaction, an external account, or a participant's understanding.",
                "Worked answers and review decisions must be supplied explicitly by the operator.",
            ],
        }

    def save_receipt(self):
        # Execution and accounting remain in WorkshopSession's durable records.
        # This receipt records coverage, never credentials or widget values.
        self.state.mkdir(parents=True, exist_ok=True)
        target = self.state / "authored-rehearsal.json"
        from filelock import FileLock

        with FileLock(str(self.state / ".rehearsal.lock")):
            previous = json.loads(target.read_text()) if target.exists() else {}
            old = previous.get("sessions", [])
            current = self.receipt()
            identity = self.history[0]["started_at"] if self.history else 0
            sessions = [row for row in old if row.get("session_id") != identity]
            sessions.append({**current, "session_id": identity})
            temporary = target.with_suffix(".tmp")
            temporary.write_text(
                json.dumps({"schema_version": 1, "sessions": sessions}, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary.replace(target)


def _display_proxy(marimo, render):
    class DisplayProxy:
        output = SimpleNamespace(replace=render)

        def __getattr__(self, name):
            return getattr(marimo, name)

    return DisplayProxy()


def interactive(root, slug, *, project, state, budget_usd=8):
    with live_environment(project, state, budget_usd):
        adapter = AuthoredAdapter(root, slug, project=project, state=state, budget_usd=budget_usd)
        adapter.refresh()
        print(
            "Commands: list; inputs; show INPUT; step STEP; set INPUT JSON_VALUE; run EXACT_CELL_ID; status; quit.\nNo action runs until you type run. Read diffs before setting review controls.\nUse the browser notebook for visual rehearsal."
        )
        while True:
            try:
                command = input("workshop> ").strip()
                if command in ("quit", "exit"):
                    adapter.save_receipt()
                    return adapter.receipt()
                if command == "list":
                    print(json.dumps(adapter.available_actions(), indent=2))
                elif command == "inputs":
                    print(
                        json.dumps(
                            [
                                {
                                    "input": name,
                                    "label": getattr(getattr(widget, "_args", None), "label", None),
                                    "type": type(widget).__name__,
                                }
                                for name, widget in adapter.scope.items()
                                if hasattr(widget, "_update") and name not in adapter.controls
                            ],
                            indent=2,
                        )
                    )
                elif command.startswith("show "):
                    name = command[5:].strip()
                    widget = adapter.scope.get(name)
                    if widget is None or not hasattr(widget, "value"):
                        raise ValueError("Choose a current input from inputs.")
                    print(widget.value)
                elif command == "status":
                    print(
                        json.dumps(
                            {
                                "receipt": adapter.receipt(),
                                "display_errors": adapter.refresh_errors,
                                "blocked_cells": adapter.blocked_cells,
                            },
                            indent=2,
                        )
                    )
                elif command.startswith("step "):
                    adapter.navigate(command[5:].strip())
                elif command.startswith("set "):
                    name, value = command[4:].split(" ", 1)
                    adapter.set_input(name, json.loads(value))
                    adapter.refresh()
                elif command.startswith("run "):
                    adapter.run(command[4:].strip())
                elif command:
                    print("Use list, inputs, show, step, set, run, status, or quit.")
            except (EOFError, KeyboardInterrupt):
                adapter.save_receipt()
                return adapter.receipt()
            except Exception as error:  # noqa: BLE001 — report the boundary failure without retrying execution.
                print(f"{type(error).__name__}: {error}")
