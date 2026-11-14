# Run a candidate outside the notebook

The core workshops execute reviewed Python in the notebook. A Sandbox gives the candidate a separate environment. It requires organization enablement and is billed independently.

Install the optional client with `uv sync --frozen --extra remote`. Inspect `examples/advanced/sandbox_candidate.py` before running it. It copies only the chosen Python source into a one-CPU environment, records its output, and saves a filesystem snapshot. It does not copy your environment variables or API credentials into the candidate process.

Write a short candidate that reads a small public fixture, computes a prediction, and writes it under `/work`. Use a cost forecast and the script's explicit `--approve-usd` option. The current example image contains Python only; add and pin the packages your candidate needs before changing the image. A missing dependency is an execution failure, not a bad model score.

Inspect the saved Sandbox ID, stdout, return code and snapshot ID. Run again with `--restore SNAPSHOT_ID`, then verify the saved prediction. A snapshot preserves files, not a running Python process. If snapshot saving fails after the command finishes, the completed output remains saved with `snapshot_status: unavailable`. Repeating the same command reads that result rather than running the candidate again. A missing snapshot cannot be restored; inspect its Sandbox ID before deciding whether another execution is necessary.

For ARIA, use a prepared Launch queue with an active worker. Ask it to investigate a completed comparison first:

```python
from forge_workshop_kit.advanced import aria_prompt
print(aria_prompt(session.project, run_url, exact_artifact, evaluation_url, queue_name))
```

Paste that prompt into ARIA. Verify one cited event yourself. Its instructions ask for a proposed change and cost estimate before submission. ARIA cannot provide your durable Launch worker; that environment must already exist. Neither a queue name nor an ARIA conversation establishes that an experiment ran.

[Sandbox setup](https://docs.coreweave.com/products/sandboxes/get-started) · [Snapshot behavior](https://docs.coreweave.com/products/sandboxes/file-system-snapshots) · [ARIA and Launch](https://docs.coreweave.com/products/aria/autoresearch)
