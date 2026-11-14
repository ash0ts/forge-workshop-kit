"""Maintainer commands for the Workshop Kit checkout. No command runs on import."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from .authoring import action_catalog, exercise_reference, metadata, source_root, validate_authored


def parser():
    top = argparse.ArgumentParser(description=__doc__)
    top.add_argument(
        "--root",
        type=Path,
        help="Workshop Kit source checkout (default: find from current directory)",
    )
    subs = top.add_subparsers(dest="command", required=True)
    for name in ("new", "open", "check", "doctor", "build", "rehearse", "publish"):
        sub = subs.add_parser(name)
        sub.add_argument("slug")
        if name == "new":
            sub.add_argument("--title", required=True)
        if name in ("doctor", "rehearse", "publish"):
            sub.add_argument("--project", required=name == "publish")
        if name == "doctor":
            sub.add_argument(
                "--services",
                action="store_true",
                help="Explicit read-only project lookup; no inference, trace, or evaluation writes",
            )
        if name == "build":
            sub.add_argument("--install", action="store_true")
            sub.add_argument("--pdf", action="store_true")
            sub.add_argument("--validate", action="store_true")
        if name == "check":
            sub.add_argument(
                "--source-only",
                action="store_true",
                help="Skip local exercise checks; validate source and references only",
            )
            sub.add_argument(
                "--write-reference",
                action="store_true",
                help="Write generated exercise references in dist/references",
            )
        if name == "rehearse":
            sub.add_argument("--mode", choices=("replay", "live"))
            sub.add_argument("--state", type=Path)
            sub.add_argument("--budget-usd", type=float, default=8)
            sub.add_argument(
                "--list-actions",
                action="store_true",
                help="List current authored action IDs without executing cells",
            )
        if name == "publish":
            sub.add_argument("--build", type=Path)
    return top


def run(root, args):
    subprocess.run(args, cwd=root, check=True)


def scaffold(root, slug, title):
    if not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
        raise ValueError("Use a lowercase Python-style slug, for example my_workshop.")
    manifest_path = root / "src/forge_workshop_kit/workshops.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if any(row["slug"] == slug for row in manifest["templates"]):
        raise ValueError("That workshop already exists. No files were changed.")
    paths = [
        root / f"scripts/{slug}_cells.py",
        root / f"decks/{slug}/scripts/build-storyboard.py",
        root / f"docs/{slug}-runbook.md",
    ]
    if any(path.exists() for path in paths) or (root / f"decks/{slug}").exists():
        raise ValueError("A scaffold destination exists. No files were changed.")
    intro = (
        "mo.md("
        + repr("# " + title + "\nReplace this paragraph with the actual problem and dataset.")
        + ")"
    )
    code = f'''"""Authored cells for {title.replace(chr(34), "")}."""
from notebook_builder import Cell
cells = [
    Cell("import marimo as mo", cell_id="{slug}/imports"),
    Cell({intro!r}, cell_id="{slug}/introduction"),
    Cell("def transform(value):\\n    # Replace this bounded exercise with the participant's task.\\n    return value * 2", hide=False, cell_id="{slug}/transform"),
    Cell('run_example = mo.ui.run_button(label="Run my example")\\nrun_example', cell_id="{slug}/controls"),
    Cell('mo.stop(not run_example.value)\\nanswer = transform(3)\\nmo.md(str(answer))', hide=False, cell_id="{slug}/action/run_example"),
]
'''
    # Keep scaffolding small; the maintainer supplies a dataset and meaningful
    # checks before advertising a runnable workshop.
    deck_slug = slug
    row = {
        "slug": slug,
        "id": slug.replace("_", "-"),
        "kind": "workshop",
        "title": title,
        "workflow_version": "1",
        "extras": [],
        "steps": [["example", "Implement the example"]],
        "checkpoint_prefixes": [],
        "comparison_labels": {},
        "release_status": "draft",
        "authoring": {
            "cells_module": f"{slug}_cells",
            "notebook": f"notebooks/{slug}.py",
            "deck": {
                "directory": deck_slug,
                "title": title,
                "file_stem": slug.replace("_", "-"),
                "storyboard": f"decks/{slug}/scripts/build-storyboard.py",
            },
            "runbook": f"docs/{slug}-runbook.md",
            "exercises": [
                {
                    "id": "example",
                    "step": "example",
                    "cell_id": f"{slug}/action/run_example",
                    "function": "transform",
                    "check_control": None,
                    "run_control": "run_example",
                    "prerequisites": [],
                    "expected_output": "The transformed input. Replace with the actual completion check.",
                    "forge_investigation": "Add a specific record and field to inspect before release.",
                }
            ],
        },
    }
    slides = f"---\ntitle: {json.dumps(title)}\n---\n\n# {title}\n\nReplace this slide with the problem, data, and first concrete example.\n"
    layout = {
        "title": title,
        "total_slides": 1,
        "slides": [{"number": 1, "title": title, "name": "introduction", "clicks": 0}],
    }
    storyboard = (
        "from pathlib import Path\nimport json\nROOT = Path(__file__).resolve().parents[1]\n"
        + 'ROOT.joinpath("slides.md").write_text('
        + repr(slides)
        + ', encoding="utf-8")\n'
        + 'ROOT.joinpath("notes").mkdir(exist_ok=True)\n'
        + 'ROOT.joinpath("notes/slide-map.json").write_text(json.dumps('
        + repr(layout)
        + ', indent=2) + "\\n", encoding="utf-8")\n'
    )
    contents = [
        code,
        storyboard,
        f"# {title}\n\nStatus: draft.\n\nSpecify the audience, duration, dataset and license, intervention, comparison, metric, budget, and rehearsal evidence before publishing.\n",
    ]
    for path, content in zip(paths, contents):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest["templates"].append(row)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {
        "status": "scaffolded",
        "slug": slug,
        "release_status": "draft",
        "files": [str(path.relative_to(root)) for path in paths],
        "next": "Replace the example and define its checks; then run forge-workshop check.",
    }


def doctor(root, row, *, services=False, project=None):
    import tomllib

    config = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    requirements = list(config["project"]["dependencies"])
    for extra in row["extras"]:
        requirements.extend(config["project"].get("optional-dependencies", {}).get(extra, []))
    packages = []
    for requirement in requirements:
        name = re.split(r"[<>=!~;\[]", requirement, 1)[0].strip()
        try:
            packages.append({"package": name, "version": importlib.metadata.version(name)})
        except importlib.metadata.PackageNotFoundError:
            packages.append({"package": name, "status": "missing"})
    receipt = {
        "workshop": row["slug"],
        "python": sys.version.split()[0],
        "dependencies": packages,
        "project": project or os.getenv("WORKSHOP_PROJECT"),
        "credentials": "present in environment"
        if os.getenv("WANDB_API_KEY")
        else "not inspected; wandb login may already be available",
        "inference": "not called; entitlement and billing unverified",
        "tracing": "not checked",
        "publication": "not checked",
    }
    if services:
        if not project or not re.fullmatch(r"[\w.-]+/[\w.-]+", project):
            raise ValueError("--services requires --project entity/project.")
        import wandb

        entity, name = project.split("/")
        try:
            found = wandb.Api(timeout=20).project(name, entity=entity)
            receipt["project_read"] = "verified" if found else "unavailable"
        except Exception as error:  # noqa: BLE001 — report the boundary failure without retrying execution.
            receipt["project_read"] = f"{type(error).__name__}: {error}"
        receipt["project_write"] = "not checked; use the notebook's explicit access check"
    return receipt


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        root = source_root(args.root)
        if args.command == "new":
            result = scaffold(root, args.slug, args.title)
        else:
            row = metadata(root, args.slug)
            slug = row["slug"]
            if args.command == "open":
                path = root / row.get("authoring", {}).get("notebook", f"notebooks/{slug}.py")
                if not path.exists():
                    raise ValueError(
                        "The notebook has not been generated. Run forge-workshop build first."
                    )
                run(root, [sys.executable, "-m", "marimo", "edit", str(path)])
                return 0
            if args.command == "check":
                result = validate_authored(root, slug)
                tests = row.get("authoring", {}).get("free_check_tests", [])
                if result["status"] == "passed" and not args.source_only and tests:
                    checked = subprocess.run(
                        [sys.executable, "-m", "pytest", "-q", *tests],
                        cwd=root,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    result["exercise_checks"] = {
                        "status": "passed" if checked.returncode == 0 else "failed",
                        "tests": tests,
                        "output": checked.stdout + checked.stderr,
                    }
                    result["coverage"]["free_checks"] += (
                        "; local exercise fixtures " + result["exercise_checks"]["status"]
                    )
                    if checked.returncode:
                        result["status"] = "failed"
                if args.write_reference:
                    path = root / "dist/references" / f"{slug}.md"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(exercise_reference(root, slug), encoding="utf-8")
                    result["reference"] = str(path)
            elif args.command == "doctor":
                result = doctor(root, row, services=args.services, project=args.project)
            elif args.command == "build":
                run(root, [sys.executable, "scripts/build_release.py", "--only", slug])
                deck = row.get("authoring", {}).get("deck")
                if deck:
                    flags = [
                        "--" + key for key in ("install", "pdf", "validate") if getattr(args, key)
                    ]
                    run(
                        root,
                        [
                            sys.executable,
                            "scripts/build_decks.py",
                            "--only",
                            deck["directory"],
                            *flags,
                        ],
                    )
                result = {"status": "built", "workshop": slug, "publication": "not requested"}
            elif args.command == "publish":
                if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.project):
                    raise ValueError("Use --project entity/project.")
                command = [
                    sys.executable,
                    "scripts/publish_templates.py",
                    "--only",
                    slug,
                    "--project",
                    args.project,
                ]
                if args.build:
                    command += ["--build", str(args.build.resolve())]
                run(root, command)
                result = {"status": "publisher finished", "project": args.project, "workshop": slug}
            elif args.command == "rehearse":
                if args.list_actions:
                    result = [
                        {k: v for k, v in row.items() if k != "code"}
                        for row in action_catalog(root, slug)
                    ]
                else:
                    if not args.mode or not args.state:
                        raise ValueError(
                            "Choose --mode replay|live and --state PATH. No rehearsal ran."
                        )
                    from .rehearsal import interactive, replay

                    if args.mode == "replay":
                        result = replay(args.state, expected_workshop=row["id"])
                    else:
                        if not args.project:
                            raise ValueError("Live rehearsal requires --project entity/project.")
                        result = interactive(
                            root,
                            slug,
                            project=args.project,
                            state=args.state,
                            budget_usd=args.budget_usd,
                        )
            else:
                raise ValueError("Unknown command")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return int(isinstance(result, dict) and result.get("status") == "failed")
    except (ValueError, FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"forge-workshop: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
