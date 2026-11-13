"""Copy only the public evidence used in this deck from a completed journal.

This reads records. It never initializes a session or repeats an execution.
"""
from pathlib import Path
import argparse
import json

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("journal", type=Path)
args = parser.parse_args()
journal = json.loads(args.journal.read_text())
rows = []
for saved in journal["stages"].values():
    if not saved["name"].startswith(("goes/", "images/")):
        continue
    row = {key: saved[key] for key in (
        "id", "name", "config", "sources", "inputs", "attempt", "status",
        "started_at", "ended_at", "source_fingerprint", "artifact_url",
    ) if key in saved}
    result = saved.get("result", {})
    row["result"] = {key: result[key] for key in (
        "metrics", "losses", "exit_code", "candidates", "decision",
        "selected", "adopted", "parent", "lesson", "lessons", "versions",
        "metrics_by_version", "rows",
    ) if key in result}
    trace = journal.get("publications", {}).get("trace/" + saved["id"])
    if trace:
        row["trace"] = {key: trace[key] for key in (
            "trace_id", "conversation_id", "verified", "expected", "url",
            "span_ids", "stored_spans",
        ) if key in trace}
    rows.append(row)
output = {
    "label": "Recorded revised-notebook browser rehearsal, November 13, 2026",
    "project": "wandb/forge-workshop-kit",
    "scope": "One seed, two reserved dates. Overlapping windows are not independent trials.",
    "stages": rows,
}
(root / "public/recorded-study.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps({"stages": len(rows), "output": "public/recorded-study.json"}))

# Module data and the downloadable copy come from the same saved rows.
runs = []
for name in ("goes/search-0", "goes/search-2"):
    row = next(row for row in rows if row["name"] == name)
    runs.append({"name": name, "id": row["id"], "source_fingerprint": row["source_fingerprint"],
                 "config": row["config"], "validation_error": row["result"]["metrics"]["validation_error"],
                 "dataset": row["inputs"]["dataset"], "split": row["inputs"]["split"],
                 "run_url": "https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/" + row["id"]})
(root / "data").mkdir(exist_ok=True)
for output in (root / "data/recorded-runs.json", root / "public/recorded-runs.json"):
    output.write_text(json.dumps(runs, indent=2) + "\n")
