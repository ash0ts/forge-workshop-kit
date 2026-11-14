"""Inspect authored notebook cells without executing the participant's code.

Control symbols are durable identities. Text and whitespace can change without
changing an action ID. Authors may give a Cell an explicit ID before renaming a
control. This module does not import any workshop runtime or provider.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import sys
from contextlib import contextmanager
from pathlib import Path


def source_root(path=None):
    start = Path(path or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "scripts/notebook_builder.py").is_file() and (
            candidate / "src/forge_workshop_kit/workshops.json"
        ).is_file():
            return candidate
    raise ValueError(
        "This command needs a Workshop Kit source checkout. Clone https://github.com/ash0ts/forge-workshop-kit and run it there, or pass --root PATH."
    )


def metadata(root, slug):
    rows = json.loads(
        (Path(root) / "src/forge_workshop_kit/workshops.json").read_text(encoding="utf-8")
    )["templates"]
    return next(
        (row for row in rows if row["slug"] == slug or row["id"] == slug), None
    ) or _unknown(slug)


def _unknown(slug):
    raise ValueError(f"Unknown workshop {slug!r}. Use a slug from workshops.json.")


@contextmanager
def script_imports(root):
    path = str(Path(root) / "scripts")
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)


def load_cells(root, slug):
    row = metadata(root, slug)
    module_name = row.get("authoring", {}).get("cells_module")
    if not module_name:
        raise ValueError(
            f"{slug} has no authored exercise adapter. Build/open its notebook directly."
        )
    if not re.fullmatch(r"[a-z][a-z0-9_]*", module_name):
        raise ValueError("cells_module must be a Python module in scripts/.")
    filename = Path(root) / "scripts" / f"{module_name}.py"
    with script_imports(root):
        spec = importlib.util.spec_from_file_location(f"workshop_authored_{slug}", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return bind_cells(row["slug"], module.cells)


def _call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _call_name(node.value) + "." + node.attr
    return ""


def cell_info(cell):
    tree = ast.parse(cell.code)
    definitions, controls, actions, state = [], {}, [], False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node.func) == "mo.state":
            state = True
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append(node.name)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call = node.value
            kind = _call_name(call.func)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if not target.id.startswith("_"):
                        definitions.append(target.id)
                    if kind == "mo.ui.run_button":
                        label = next(
                            (
                                kw.value.value
                                for kw in call.keywords
                                if kw.arg == "label" and isinstance(kw.value, ast.Constant)
                            ),
                            None,
                        )
                        controls[target.id] = label
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and _call_name(node.value.func) == "mo.stop"
        ):
            args = node.value.args
            if args and isinstance(args[0], ast.UnaryOp) and isinstance(args[0].op, ast.Not):
                value = args[0].operand
                if (
                    isinstance(value, ast.Attribute)
                    and value.attr == "value"
                    and isinstance(value.value, ast.Name)
                ):
                    actions.append(value.value.id)
    return {"definitions": definitions, "controls": controls, "actions": actions, "state": state}


def bind_cells(slug, cells):
    seen = set()
    for index, cell in enumerate(cells):
        info = cell_info(cell)
        if not cell.cell_id:
            # Action IDs survive wording, source, and cell-order changes. Display
            # cells are not rehearsal entry points; their positional IDs are only
            # used to show diagnostics and generated source locations.
            stem = (
                "action/" + info["actions"][0]
                if info["actions"]
                else "controls/" + next(iter(info["controls"]))
                if info["controls"]
                else "definitions/" + info["definitions"][0]
                if info["definitions"]
                else f"display/{index + 1}"
            )
            cell.cell_id = f"{slug}/{stem}"
        if cell.cell_id in seen:
            raise ValueError(
                f"Duplicate authored cell ID: {cell.cell_id}. Set an explicit Cell(cell_id=...)."
            )
        seen.add(cell.cell_id)
    return cells


def action_catalog(root, slug):
    cells = load_cells(root, slug)
    labels = {name: label for cell in cells for name, label in cell_info(cell)["controls"].items()}
    return [
        {
            "cell_id": cell.cell_id,
            "control": info["actions"][0],
            "label": labels.get(info["actions"][0]),
            "code": cell.code,
        }
        for cell in cells
        if (info := cell_info(cell))["actions"]
    ]


def validate_authored(root, slug):
    row = metadata(root, slug)
    cells = load_cells(root, slug)
    with script_imports(root):
        from notebook_builder import analyze

        analyze(cells)
    by_id = {cell.cell_id: cell for cell in cells}
    controls = {
        name: label for cell in cells for name, label in cell_info(cell)["controls"].items()
    }
    functions = {
        node.name
        for cell in cells
        for node in ast.walk(ast.parse(cell.code))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    errors = []
    for exercise in row.get("authoring", {}).get("exercises", []):
        if exercise["cell_id"] not in by_id:
            errors.append(f"{exercise['id']}: missing cell {exercise['cell_id']}")
        for field in ("check_control", "run_control"):
            name = exercise.get(field)
            if name and name not in controls:
                errors.append(f"{exercise['id']}: missing {field} {name}")
        if exercise.get("function") and exercise["function"] not in functions:
            # Many exercise functions are editable code strings. Parse them too.
            strings = [
                n.value
                for c in cells
                for n in ast.walk(ast.parse(c.code))
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
            ]
            if exercise.get("function_source"):
                source_path = (Path(root) / exercise["function_source"]).resolve()
                if not source_path.is_relative_to(Path(root).resolve()):
                    raise ValueError("Exercise source must stay inside the checkout.")
                strings.append(source_path.read_text(encoding="utf-8"))
            if not any(f"def {exercise['function']}(" in text for text in strings):
                errors.append(
                    f"{exercise['id']}: function {exercise['function']} is not introduced in its notebook"
                )
    return {
        "workshop": row["slug"],
        "status": "failed" if errors else "passed",
        "cells": len(cells),
        "actions": len(action_catalog(root, slug)),
        "exercise_references": len(row.get("authoring", {}).get("exercises", [])),
        "errors": errors,
        "coverage": {
            "free_checks": "source, compilation, cell dependencies, exercise references",
            "authored_notebook_execution": "not run",
            "browser": "not run",
            "external_account": "unknown",
            "human_rehearsal": "unknown",
        },
    }


def exercise_reference(root, slug):
    row = metadata(root, slug)
    controls = {
        name: label
        for cell in load_cells(root, slug)
        for name, label in cell_info(cell)["controls"].items()
    }
    lines = [
        f"# {row['title']}: exercise reference",
        "",
        "Generated from the workshop manifest and current authored controls.",
        "",
    ]
    steps = dict(row.get("steps", []))
    for exercise in row.get("authoring", {}).get("exercises", []):
        lines += [f"## {exercise['id']}", ""]
        if exercise.get("step"):
            lines.append(f"Notebook step: **{steps.get(exercise['step'], exercise['step'])}**.")
        if exercise.get("task"):
            lines.append(exercise["task"])
        elif exercise.get("function"):
            verb = {"inspect": "Inspect", "revise": "Revise"}.get(exercise.get("activity"), "Edit")
            lines.append(f"{verb} `{exercise['function']}`.")
        else:
            lines.append("Use the code shown in this exercise.")
        if exercise.get("prerequisites"):
            prerequisites = ", ".join(steps.get(item, item) for item in exercise["prerequisites"])
            lines.append(f"Before this exercise: {prerequisites}.")
        for field, label, fallback in (
            ("check_control", "Free check", "check_label"),
            ("run_control", "Run", "run_label"),
        ):
            if exercise.get(field):
                control_label = (
                    controls.get(exercise[field]) or exercise.get(fallback) or exercise[field]
                )
                lines.append(f"{label}: **{control_label}**.")
        lines += [
            f"Expected output: {exercise['expected_output']}",
            f"In Forge: {exercise['forge_investigation']}",
            "",
        ]
    return "\n".join(lines)
