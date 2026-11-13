"""Rehearse the authored Solar cells, stopping for source review before execution.

This checks the execution path, not browser interactions. Every action is explicit;
restarts use the same durable stage records. Use a new state directory per release.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "action", choices=("status", "prepare", "next", "review", "evaluate", "publish", "audit")
    )
    result.add_argument("--project", required=True)
    result.add_argument("--state", type=Path, required=True)
    result.add_argument("--data", type=Path, default=ROOT / "data/solar-v1")
    result.add_argument("--budget-usd", type=float, default=8)
    result.add_argument("--note", default="")
    result.add_argument("--reviewed-fingerprint")
    result.add_argument(
        "--evidence", type=Path, default=ROOT / "evidence/solar-rehearsal-v030.json"
    )
    return result


class ConsoleUI:
    """Only replace rendering; execute the original cell bodies and run controls."""

    output = SimpleNamespace(replace=lambda text: print(text, flush=True))
    status = SimpleNamespace(spinner=lambda **kwargs: nullcontext())

    @staticmethod
    def stop(condition, message="A prerequisite is missing"):
        if condition:
            raise RuntimeError(str(message))

    @staticmethod
    def md(value):
        return value


def main():
    args = parser().parse_args()
    args.state = args.state.resolve()
    for key, directory in (("MPLCONFIGDIR", "matplotlib"), ("SUNPY_CONFIGDIR", "sunpy")):
        path = args.state / "cache" / directory
        path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(key, str(path))
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("WANDB_SILENT", "true")
    import time

    import numpy as np
    from solar_cells import DEFAULT, cells

    from forge_workshop_kit import WorkshopSession, plots, research, solar, training, ui
    from forge_workshop_kit import solar_teaching as teaching
    from forge_workshop_kit.download import dataset
    from forge_workshop_kit.provider import Provider
    from forge_workshop_kit.publication import publish_comparison, publish_report
    from forge_workshop_kit.session import digest, write_json
    from forge_workshop_kit.traces import event, export_trace, stamp

    session = WorkshopSession(
        args.project, "solar-autoresearch", state_dir=args.state, budget_usd=args.budget_usd
    )
    if args.action not in ("status", "audit"):
        paths = [
            ROOT / "scripts/solar_cells.py",
            *sorted((ROOT / "src/forge_workshop_kit").rglob("*.py")),
        ]
        invocation = {
            "action": args.action,
            "started_at": time.time(),
            "installed_kit_version": session.kit_version,
            "source_sha256": {
                str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in paths
            },
        }
        write_json(session.file(f"rehearsal-invocations/{time.time_ns()}.json"), invocation)
    lab = {"session": session, **teaching.restore_state(session)}
    feedback = {}
    solutions = {
        "solar/instrumentation": teaching.INSTRUMENTATION_SOLUTION,
        "solar/persistence": teaching.PERSISTENCE_SOLUTION,
        "solar/measurement": DEFAULT,
        "solar/flux-metric": teaching.FLUX_SOLUTION,
        "solar/image": DEFAULT,
        "solar/image-metric": teaching.IMAGE_METRIC_SOLUTION,
        "solar/evidence": teaching.EVIDENCE_SOLUTION,
    }
    scope = {
        "os": os,
        "json": json,
        "time": time,
        "Path": Path,
        "np": np,
        "solar": solar,
        "training": training,
        "research": research,
        "plots": plots,
        "teaching": teaching,
        "ui": ui,
        "digest": digest,
        "event": event,
        "export_trace": export_trace,
        "stamp": stamp,
        "publish_comparison": publish_comparison,
        "publish_report": publish_report,
        "dataset": lambda: dataset(args.data),
        "mo": ConsoleUI(),
    }
    scope.update(
        get_lab=lambda: lab,
        set_lab=lambda value: lab.update(value),
        get_feedback=lambda: feedback,
        set_feedback=lambda value: feedback.update(value),
        refresh_saved=lambda: lab.update(teaching.restore_state(session)),
    )
    for name, key in (
        ("instrumentation_editor", "solar/instrumentation"),
        ("persistence_editor", "solar/persistence"),
        ("measurement_editor", "solar/measurement"),
        ("flux_metric_editor", "solar/flux-metric"),
        ("image_editor", "solar/image"),
        ("image_metric_editor", "solar/image-metric"),
        ("evidence_editor", "solar/evidence"),
    ):
        scope[name] = SimpleNamespace(value=session.get_draft(key, solutions[key]))
    for name in (
        "first_trace",
        "load_data",
        "baseline_button",
        "run_search",
        "run_images",
        "research_button",
        "final_button",
        "report_button",
    ):
        scope[name] = SimpleNamespace(value=True)
    scope["research_note"] = SimpleNamespace(value=args.note)
    scope["conclusion"] = SimpleNamespace(value=args.note)

    def run_cell(start):
        matches = [cell.code for cell in cells if cell.code.startswith(start)]
        if len(matches) != 1:
            raise RuntimeError(
                f"Expected one authored cell beginning {start!r}; found {len(matches)}"
            )
        # Execute repository-authored cells; agent code still waits for the review action.
        exec(compile(matches[0], str(ROOT / "scripts/solar_cells.py") + ":" + start, "exec"), scope)  # noqa: S102
        import matplotlib.pyplot as plt

        plt.close("all")

    run_cell("# The edited function below")
    run_cell("def run_training(")
    run_cell("def next_research_action(")

    def hydrate():
        # Loading arrays is free; only explicit run cells train or request inference.
        path, fingerprint = dataset(args.data)
        goes, _ = solar.load_goes(path)
        images, _ = solar.load_aia(path)
        lab.update(data_path=str(path), dataset=fingerprint, goes=goes, images=images)
        scope["refresh_saved"]()

    def candidate():
        number, phase, _ = teaching.next_action(session)
        prefix = f"images/round-{number}/"
        if phase == "review-composition":
            return teaching.saved(session, prefix + "compose")["result"]["decision"]
        if phase.startswith("review-"):
            return teaching.saved(session, prefix + "propose")["result"]["candidates"][
                int(phase[-1])
            ]
        return None

    def status():
        number, phase, label = teaching.next_action(session)
        value = {
            "project": session.project,
            "workspace": session.workspace_id,
            "state": str(session.root),
            "next_action": {"round": number, "phase": phase, "label": label},
            "completed_stages": len(session.completed()),
            "cost": Provider(session).summary(),
            "failed": [
                {"id": row["id"], "name": row["name"], "error": row.get("error")}
                for row in session.read()["stages"].values()
                if row["status"] != "complete"
            ],
            "feedback": feedback,
        }
        selected = candidate()
        if selected:
            value["review_required"] = {
                key: selected.get(key)
                for key in ("title", "decision", "rationale", "fingerprint", "diff")
            }
            value["review_command"] = (
                "Inspect the saved complete source, then run review with --note and --reviewed-fingerprint."
            )
        print(json.dumps(value, indent=2), flush=True)
        return value

    if args.action == "status":
        status()
        return
    if args.action == "audit":
        value = status()
        value["kind"] = "Fresh v0.3.0 authored-cell rehearsal; not a browser usability test"
        value["authored_cells_sha256"] = hashlib.sha256(
            (ROOT / "scripts/solar_cells.py").read_bytes()
        ).hexdigest()
        value["dataset_fingerprint"] = solar.verify_data(args.data)
        value["stages"] = [
            {
                key: row.get(key)
                for key in (
                    "id",
                    "name",
                    "status",
                    "config",
                    "source_fingerprint",
                    "inputs",
                    "published",
                )
            }
            for row in session.read()["stages"].values()
        ]
        value["publication"] = session.read()["publications"]
        value["invocations"] = [
            json.loads(path.read_text())
            for path in sorted(session.file("rehearsal-invocations").glob("*.json"))
        ]
        for name in ("images/final-comparison", "goes/final-comparison"):
            row = teaching.saved(session, name)
            if row:
                value[name] = row["result"]["metrics_by_version"]
        value["adoptions"] = [
            teaching.saved(session, f"images/round-{number}/adopt")["result"]
            for number in (1, 2)
            if teaching.saved(session, f"images/round-{number}/adopt")
        ]
        write_json(args.evidence, value)
        print("Saved audit:", args.evidence)
        return
    if args.action == "prepare":
        session.check_access()
    else:
        session.connect()
    if args.action == "prepare":
        for name, value in solutions.items():
            if session.get_draft(name) is None:
                session.save_draft(name, value)
        teaching.check_instrumentation(scope["instrumentation_editor"].value)
        teaching.check_persistence(scope["persistence_editor"].value)
        teaching.check_flux_metric(scope["flux_metric_editor"].value)
        teaching.check_image_metric(scope["image_metric_editor"].value)
        teaching.check_evidence(scope["evidence_editor"].value)
        for start in (
            "mo.stop(not first_trace.value)",
            "mo.stop(not load_data.value)",
            "mo.stop(not baseline_button.value)",
            "mo.stop(not run_search.value)",
            "mo.stop(not run_images.value)",
        ):
            print("Executing authored cell:", start, flush=True)
            run_cell(start)
    elif args.action in ("next", "review"):
        hydrate()
        if not lab.get("manual"):
            raise RuntimeError("Run prepare before the research rounds.")
        number, phase, _ = teaching.next_action(session)
        if phase == "done":
            status()
            return
        if phase.startswith("review-"):
            selected = candidate()
            if (
                args.action != "review"
                or not args.note.strip()
                or args.reviewed_fingerprint != selected["fingerprint"]
            ):
                status()
                raise SystemExit("Source review is required; no candidate was executed.")
        elif args.action == "review":
            raise SystemExit("The next action is not a source review; nothing executed.")
        if phase == "probe-done" and not args.note.strip():
            raise SystemExit("Read both saved probe results and supply --note before composing.")
        print(f"Executing authored research action: round {number} / {phase}", flush=True)
        run_cell("mo.stop(not research_button.value)")
    elif args.action == "evaluate":
        if teaching.next_action(session)[1] != "done":
            raise SystemExit("Both rounds must finish before final evaluation.")
        hydrate()
        run_cell("mo.stop(not final_button.value)")
    elif args.action == "publish":
        if not teaching.saved(session, "images/final-comparison") or not args.note.strip():
            raise SystemExit("Save the final comparison and supply an evidence-based --note first.")
        run_cell("mo.stop(not report_button.value)")
    status()


if __name__ == "__main__":
    main()
