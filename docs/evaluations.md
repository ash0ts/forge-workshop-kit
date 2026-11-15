# Compare saved results in Forge

Each workshop publishes an **Evaluation Tables (Preview)** panel in its Forge W&B workspace. Click **Compare in EvalTables** beside the notebook result. The first version is the reference; other versions are aligned against the same cases. Select a row to inspect its output, individual scores and execution links.

Agent Lens answers a different question: what happened while the agent was working? Follow the selected result’s conversation link to inspect its model requests and tool calls. The evaluation table compares the work those executions produced.

| Workshop step | What to compare | What to inspect |
| --- | --- | --- |
| Pending: retry practice | New-operation retry and the repaired procedure | Two memberships versus one after a committed write times out |
| Pending: development and final tickets | Starting, manually edited and agent-selected harnesses | Account checks and explanation judgments separately; all four final cases remain represented |
| Solar: reserved dates | Persistence, manual and agent-selected image forecasts | Matching timestamps, actual images and disk-masked error; measurement forecasts use a separate table |
| Routing: judge review | The automated judge and the saved human review | Agreement, the reason for disagreement and unavailable judgments |
| Routing: final requests | Frozen classifiers on the same requests | Intent, correctness, abstention, latency and cost; macro-F1 remains a run-level metric |
| Inspection: final boards | Whole-image, patch, active-review and random-review models | Actual photographs, reference masks, misses, false alarms and review decisions |
| Routing: release drill | Healthy, faulty, and repaired loaders | Matching review-pool requests and probability-to-intent mapping; this is not a new test set |
| Transit: initial and follow-up builds | Solo/team, then without/with accepted lessons | Actual departure outputs, application checks, incomplete builds, and trace links |
| Airline: development, reserved, and subsequent requests | Original and repaired agents | Requested itinerary change, preserved flights, resulting booking, and independent checks; monitor agreement is separate |

## Open the recorded comparisons

These views reuse saved rehearsal outputs. Their publication checks did not retrain models or request new judgments. [Recorded results](recorded-results.md) links each workshop’s protocol and qualification.

| Comparison | Saved predictions |
| --- | ---: |
| [Pending retry repair](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=yw6s55oucu4) | 2 |
| [Pending final tickets](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=qeo6ytk9yxz) | 12 |
| [Solar images](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=91ypk2or045) | 597 |
| [Solar measurements](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=dtm5k18fpo4) | 5,388 |
| [Routing classifiers](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=fthby6owcpo) | 6,160 |
| [Board inspection](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=h43oxpf30iu) | 1,768 |
| [Transit first release](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=dg2ogm6wp3z) | 20 |
| [Transit memory comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=f9jpm0yjsxy) | 36 |
| [Airline development](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1) | 8 |
| [Airline reserved requests](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=m6e4y19blu9) | 12 |
| [Airline subsequent requests](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=8woi2lgyt5c) | 8 |

Prediction counts include each version of the same case. They are not counts of independent tasks. The Routing judge-alignment exercise requires the participant's saved human reviews; the recorded four-judgment check used dataset labels and is not presented as human alignment.

## The code participants use

The notebook retains the scorer and prediction code. Publication reads its saved rows:

```python
rows = [{
    "case_id": "ticket-17",
    "input": {"request": "My card has not arrived"},
    "prediction": {"intent": "card_arrival"},
    "target": {"intent": "card_arrival"},
    "scores": {"correct": True, "abstained": False},
    "evidence": {"agent_lens": conversation_url},
}]
```

Across versions, `case_id` and the input contents must match. Put the version name, prediction and trace link outside the inputs. Otherwise the table treats them as different examples. Keep an unavailable score as `None`; it is not a wrong answer.

The shared publisher uses the pinned SDK’s public API:

```python
table = wandb.EvalTable(
    input_columns=["case_id", "request"],
    output_columns=["prediction", "target", "agent_lens"],
    score_columns=["correct"],
    data=saved_examples,
    backend="weave",
    unsupported_media_mode="raise",
)
run.log({"final_cases": table})
```

Images are real media cells, not file-path strings. The publisher retains the SDK’s evaluation identity, reads back every case and score, and checks the run’s logged table before calling the export complete. Image readback checks the stored media type and file references; it does not download and compare every pixel. A saved comparison view selects only the relevant runs; it does not change the project’s default workspace.

## If an upload fails

Your completed experiment remains saved. Choose **Retry publication** to retry the incomplete destination. This does not repeat training, inference or judging. Completed W&B and Weave exports are reused.

An interrupted export with a saved evaluation identity can resume readback. If the upload was interrupted before that identity was saved, the notebook reports an uncertain export. Check the run history before attempting another upload; do not rerun the experiment to solve a publication problem.

The separate CES EvalTables backend returned HTTP 500 in the November 14 check. This release uses **Weave-backed native EvalTables Preview**. It does not claim that CES recovered or that a proposed Evaluation Studio is available to attendees. The [pinned SDK source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/sdk/data_types/eval_table/eval_table.py) documents the supported backend and comparison inputs.

Native comparison publication and execution have separate statuses. If the comparison service is unavailable, inspect the saved notebook results or Weave evaluation while publication is repaired.
