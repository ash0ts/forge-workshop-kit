"""Present the saved workshop rehearsals in their existing Reports.

The default is a read-only plan: check the saved rows against published summary
metrics and serialize the proposed panels. --apply changes only Report content.
It does not create runs, change scores, train, or call an inference provider.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import wandb
import wandb_workspaces.reports.v2 as wr


ROOT = Path(__file__).resolve().parents[1]
PROJECT = "wandb/forge-workshop-kit"
FORGE = "https://forge.coreweave.com/wandb/" + PROJECT
REPO = "https://github.com/ash0ts/forge-workshop-kit"
REPORTS = {
    "pending": "pending-direct-teaching:-51a0006f--VmlldzoxODMwMjcxMA==",
    "solar": "solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==",
}


def load(name):
    return json.loads((ROOT / name).read_text())


def comparison(journal, name):
    # Labels repeat between tasks, so select the dataset before indexing labels.
    matches = [value for key, value in journal["publications"].items()
               if key.startswith("comparison/") and value
               and all(name + "-" in row.get("evaluation", "") for row in value.values())]
    if len(matches) != 1:
        raise ValueError(f"Expected one saved {name} comparison, found {len(matches)}")
    return matches[0]


def link(label, url):
    return wr.P(text=[wr.Link(text=label, url=url)])


def table(headers, rows):
    def clean(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(clean, headers)) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(map(clean, row)) + " |" for row in rows)
    return wr.MarkdownBlock(text="\n".join(lines))


def panel(journal, receipts, name, metric, title):
    ids = [r["run"].rsplit("/", 1)[-1] for r in receipts.values()]
    workspace = journal["workspace_id"]
    filters = f'Config("workspace_id") == "{workspace}" and ID in {json.dumps(ids)}'
    labels, axis = {
        "available_scores": ({"starting": "Starting instructions", "manual": "Manual revision",
            "agent": "Agent-selected version"}, "Completed state checks (four tickets per version)"),
        "solar-images-final/error_mean": ({"persistence": "Copy the latest image", "manual": "Manual image model",
            "agent": "Agent-selected image model"}, "Mean disk-masked absolute error (standardized log1p image units)"),
        "solar-measurements-final/error_mean": ({"persistence": "Copy the latest GOES reading",
            "selected-model": "Selected GOES model"}, "Mean absolute error in log10 XRS-B flux"),
    }[metric]
    line_titles = {f"{rid}:{metric}": labels[label] for rid, label in zip(ids, receipts)}
    grid = wr.PanelGrid(runsets=[wr.Runset(entity="wandb", project="forge-workshop-kit",
        name=name, filters=filters, visible_columns=["Name", "config.condition", "summary." + metric])],
        panels=[wr.BarPlot(title=title, metrics=[metric], orientation="h", aggregate=False,
            title_x=axis, range_x=(0, 4 if metric == "available_scores" else None),
            max_runs_to_show=len(ids), max_bars_to_show=len(ids), line_titles=line_titles,
            font_size="large", layout=wr.Layout(w=24, h=8))])
    return grid, {"name": name, "ids": ids, "metric": metric, "filters": filters,
                  "chart": "BarPlot", "run_labels": line_titles}


def verify_runs(api, spec, expected, workspace):
    verified = []
    for rid, value in zip(spec["ids"], expected):
        run = api.run(PROJECT + "/" + rid)
        actual = run.summary.get(spec["metric"])
        if run.config.get("workspace_id") != workspace:
            raise ValueError(f"Wrong rehearsal in {rid}")
        if actual is None or not math.isclose(actual, value, rel_tol=1e-11, abs_tol=1e-12):
            raise ValueError(f"Saved score differs from published score in {rid}: {value} != {actual}")
        verified.append({"id": rid, "score": actual, "planned": run.summary.get("planned_scores"),
                         "available": run.summary.get("available_scores")})
    spec["verified_runs"] = verified


def pending_blocks(journal, evidence, api):
    receipts = comparison(journal, "pending-final")
    grid, spec = panel(journal, receipts, "Four fresh tickets · final comparison",
        "available_scores", "Completed state checks · four tickets per version")
    verify_runs(api, spec, [4] * 3, journal["workspace_id"])
    state_error = {"ids": spec["ids"], "metric": "pending-final/error_mean"}
    verify_runs(api, state_error, [0.0] * 3, journal["workspace_id"])
    spec["state_error_readback"] = state_error["verified_runs"]
    rows = evidence["final_comparison"]["rows"]
    labels = {"starting": "Starting instructions", "manual": "Manual revision", "agent": "Agent-selected version"}
    coverage = []
    for condition, title in labels.items():
        group = [row for row in rows if row["condition"] == condition]
        available = [row for row in group if row["judge_status"] == "available"]
        coverage.append([title, f'{sum(row["state_correct"] for row in group)}/{len(group)}',
            f'{sum(not row["state_correct"] for row in group) / len(group):.1f}',
            f'{sum(row["grounded"] and row["explanation_complete"] for row in available)}/{len(available)} available',
            len(group) - len(available)])
    blocks = [
        wr.P(text="An operations agent handles fictional billing and account-access tickets. We built its tools, traced its actions, changed its instructions by hand, then let an editor agent propose and test alternatives."),
        wr.H2(text="All three versions got the account state right"),
        wr.P(text="All 12 final executions passed the state checks. Both improvement rounds retained the manual revision, so the three labels represent two distinct harnesses. This rehearsal demonstrates the loop; it shows no task-quality gain."),
        grid,
        wr.P(text="The bars count completed state checks, not explanation judgments. Every completed state check passed; mean state error is zero for each version."),
        table(["Version", "Correct state", "Mean state error", "Explanation checks", "Unavailable judgments"], coverage),
        wr.P(text="The starting version's two-invoices explanation hit its output limit twice, including one judge-only retry. Its judgment stays missing. Passing state checks does not fill in that missing score."),
        wr.H2(text="Follow a ticket through the tools and the revision"),
        wr.P(text="Open the onboarding trace and find the write that timed out. Then inspect the state read that established what had already happened. A tool error can be followed by successful recovery."),
        link("1. Inspect the timed-out onboarding write and recovery in Agent Lens", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/911e3062cf37ac66f5b9944464a27fae"),
        link("2. Read the editor's two proposed billing procedures", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/e59f98a0cc5d76c8e5939212b2ec009b"),
        link("3. See why composition retained the current harness", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/ab8601f17816d231b44cac6f77f33f6c"),
        link("4. Open the saved decision and exact harness files", FORGE + "/artifacts/workshop-execution/execution-32e300cbba317080d5c345eb3aab0b6d/v0"),
        link("5. Inspect the manual version on the two-invoices final case", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/370ae4263372ca1de91d7308e66d0d3d"),
        wr.H2(text="Inspect matching cases"),
        wr.P(text="These runs contain the saved case tables, scores, and conversation links. Native EvalTables publication returned HTTP 500; the notebook comparison and Weave evaluations remain available. These are W&B Tables, not native EvalTables screenshots."),
        *[link(labels[label] + " · final case table", value["run"]) for label, value in receipts.items()],
        wr.H2(text="What to try next"),
        wr.P(text="Use harder billing and access cases, then test whether explicitly loading the verification skill changes behavior. The retained version already passes these four cases; more elaborate instructions alone would not establish a benefit."),
        wr.P(text=f'Measured inference: ${evidence["accounting"]["observed_usd"]:.8f}. This includes the saved attempts and retries. Notebook compute is separate.'),
    ]
    return blocks, [spec]


def solar_blocks(journal, evidence, api):
    image = comparison(journal, "solar-images-final")
    goes = comparison(journal, "solar-measurements-final")
    igrid, ispec = panel(journal, image, "AIA images · reserved dates",
        "solar-images-final/error_mean", "Future-image error · lower is better")
    ggrid, gspec = panel(journal, goes, "GOES measurements · reserved dates",
        "solar-measurements-final/error_mean", "Log-flux forecast error · lower is better")
    verify_runs(api, ispec, [evidence["final_images"][k]["error"] for k in image], journal["workspace_id"])
    verify_runs(api, gspec, [evidence["final_measurements"][k]["error"] for k in goes], journal["workspace_id"])
    gain = 100 * (1 - evidence["final_images"]["agent"]["error"] / evidence["final_images"]["manual"]["error"])
    blocks = [
        wr.P(text="A research lab starts with real GOES X-ray measurements and AIA solar images. We record the data, code and training settings, compare existing models, then let a fixed research agent propose changes to the image-model code."),
        wr.H2(text="The image model improved in this rehearsal"),
        wr.P(text=f'The agent-selected image model reduced final error by {gain:.2f}% relative to the manual model. It first zero-initialized the residual output head, then trained with a disk-masked absolute-error loss. The final comparison uses 199 overlapping forecast windows from February 13–14, 2014, with one seed. It does not establish repeatability across dates or seeds.'),
        igrid,
        table(["Image forecast", "Disk-masked absolute error", "Forecast windows"],
            [[label, f'{evidence["final_images"][label]["error"]:.6f}', evidence["final_images"][label]["examples"]] for label in image]),
        wr.H2(text="The measurement model lost to persistence"),
        wr.P(text="On the separate GOES task, the selected neural model did much worse than carrying the current flux forward. Keep this failed forecast beside the image result. The two tasks use different metrics and cannot be combined into one score."),
        ggrid,
        table(["Measurement forecast", "Log-flux MAE", "Forecast windows"],
            [[label, f'{evidence["final_measurements"][label]["error"]:.6f}', evidence["final_measurements"][label]["examples"]] for label in goes]),
        wr.H2(text="Follow the research agent's changes"),
        wr.P(text="Start with the validation evidence the agent read. Compare its proposed source with the files used by the training run, then open the final predictions. The forecasting weights train normally; the research agent's model stays fixed."),
        link("1. Compare the six measurement configurations in the Sweep", FORGE + "/sweeps/pr1xsoaw"),
        link("2. Inspect the agent reading validation evidence and proposing code", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/ef590522f1af377a0bc04bd63eea23e4"),
        link("3. Inspect the zero-initialized model's training run", FORGE + "/runs/c07c5d78722ad00dd3c397a69a497d3e"),
        link("4. Read the second-round composition decision", "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/1c8586a9e445da02a96803d435192200"),
        link("5. Open the tested source, weights and predictions", FORGE + "/artifacts/workshop-execution/execution-f5e5d198bc9479f78d9a4b1c8c8979e3/v0"),
        wr.H2(text="Inspect matching forecasts"),
        wr.P(text="Each run below contains a saved prediction table and source links. Native EvalTables publication returned HTTP 500. Use the Weave evaluations and notebook comparison, and retry publication without retraining."),
        *[link("AIA images · " + label, value["run"]) for label, value in image.items()],
        *[link("GOES measurements · " + label, value["run"]) for label, value in goes.items()],
        wr.H2(text="What to try next"),
        wr.P(text="Repeat the zero-initialization and loss comparisons with new seeds and additional reserved dates. For GOES, investigate target scaling, model capacity and optimization as separate hypotheses. Do not choose those changes using the final dates already inspected here."),
        wr.P(text=f'Four research-agent requests cost ${evidence["accounting"]["observed_usd"]:.8f} in measured inference, with no bounded unknown usage. Notebook compute is separate.'),
    ]
    return blocks, [ispec, gspec]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Update the same two Report IDs after checking source scores")
    parser.add_argument("--env-file", type=Path, help="Optional local credentials file; never copied into the plan")
    parser.add_argument("--workspaces", type=Path, help="Optional JSON mapping pending/solar to named workspace URLs")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.env_file:
        from dotenv import load_dotenv
        load_dotenv(args.env_file, override=True)
    workspace_urls = json.loads(args.workspaces.read_text()) if args.workspaces else {}
    workspace_urls = {key: value["url"] if isinstance(value, dict) else value
                      for key, value in workspace_urls.items()}
    api = wandb.Api(timeout=30)
    plans = {}
    for stem, suffix in REPORTS.items():
        report_url = "https://wandb.ai/" + PROJECT + "/reports/" + suffix
        # The SDK expects entity/project directly after the host. The Forge /wandb
        # route has an additional segment, so use its equivalent W&B URL here.
        report = wr.Report.from_url(report_url)
        original_id = report.id
        original = report._to_model().model_dump(mode="json", by_alias=True, exclude_none=True)
        previous_conclusion = next(b.text for b in report.blocks if isinstance(b, wr.P))
        journal = load(f".workshop/ux-v020-{stem}/journal.json")
        journal["workspace_id"] = load(f".workshop/ux-v020-{stem}/identity.json")["workspace_id"]
        evidence = load(f"evidence/ux-v020-{stem}.json")
        blocks, panels = (pending_blocks if stem == "pending" else solar_blocks)(journal, evidence, api)
        notebook_id = "Tm90ZWJvb2s6MTU3NzQ=" if stem == "pending" else "Tm90ZWJvb2s6MTU3NzU="
        blocks.extend([wr.H2(text="Run the workshop in your project"),
            link("Open the participant notebook and copy it into your project", "https://forge.coreweave.com/notebooks/" + notebook_id + "/view"),
            link("Get the source and setup instructions", REPO),
            link("Read the complete recorded rehearsal", REPO + f"/blob/main/evidence/ux-v020-{stem}.json")])
        if stem in workspace_urls:
            blocks.insert(1, link("Open this rehearsal's run dashboard", workspace_urls[stem]))
        # Keep the participant's actual words available without placing a long
        # unstructured result paragraph in front of the charts.
        if not any(isinstance(b, wr.H2) and b.text == "Original rehearsal conclusion" for b in report.blocks):
            saved_conclusion = previous_conclusion
        else:
            old = next(b for b in report.blocks if isinstance(b, wr.H2) and b.text == "Original rehearsal conclusion")
            saved_conclusion = old.collapsed_blocks[0].text
        blocks.append(wr.H2(text="Original rehearsal conclusion", collapsed_blocks=[wr.P(text=saved_conclusion)]))
        report.title = ("Pending, Inc. | Build and test an agent harness" if stem == "pending"
                        else "Solar Autoresearch | Build a research loop, then give it an agent")
        report.description = "Recorded workshop results, code changes, predictions and Agent Lens traces."
        # Wide page is capped at 1072px in Forge and still uses the responsive
        # mobile layout. It leaves room for full model names and metric units.
        report.width = "fixed"
        report.blocks = blocks
        proposed = report._to_model().model_dump(mode="json", by_alias=True, exclude_none=True)
        if report.id != original_id:
            raise ValueError("Presentation update must retain the existing Report ID")
        plan = {"title": report.title, "id": original_id, "url": FORGE + "/reports/" + suffix,
                "workspace_id": journal["workspace_id"], "panels": panels,
                "blocks": len(blocks), "outcomes_changed": False,
                "original_conclusion_sha256": hashlib.sha256(str(saved_conclusion).encode()).hexdigest(),
                "presentation_sha256": hashlib.sha256(json.dumps(proposed, sort_keys=True).encode()).hexdigest(),
                "mode": "read-only plan"}
        if args.apply:
            backup = ROOT / ".workshop/report-presentation-backups" / f"{stem}-before-v023.json"
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_text(json.dumps(original, indent=2))
            report.save()
            readback = wr.Report.from_url(report_url)
            if readback.id != original_id or readback.title != report.title or len(readback.blocks) != len(blocks):
                raise ValueError("Report presentation readback did not match")
            plan.update(mode="updated", readback=True)
        plans[stem] = plan
    text = json.dumps(plans, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
