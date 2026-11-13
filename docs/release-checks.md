# Release checks · November 13, 2026

This is a technical preview. The implementation and live rehearsals are complete; a fresh external-attendee check and a human usability rehearsal remain before advertising a classroom-ready release.

| Check | Evidence and outcome |
| --- | --- |
| Local tests | 21 passed, including real CPU training/frozen-weight replay, true MCP timeout recovery, KEEP, budget reservations, interrupted requests, isolation, artifact restore and missing publication. |
| Clean installs | macOS, Windows and Linux clean installs, all 21 tests and marimo checks passed for this release. [CI run](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43377483699). |
| Hosted copy | Native **Copy to project** created a distinct notebook, autofilled its project, verified writes and exported two stored spans using hosted authentication. No host token. [Receipt](../evidence/hosted-copy.json). This used the maintainer account, not a new external account. |
| Recovery | An empty runtime restored all 33 completed Solar stages and verified 51 source, weight and prediction files byte-for-byte, without new training or inference. [Trained restore](../evidence/trained-restore.json). A separate hosted-identity fixture also passed [restore and monitoring checks](../evidence/restore.json). |
| Monitoring | Real public progress runs read through the API. The monitor only reads; missing updates are unknown. No classroom-scale load test or human rehearsal has been performed. |
| Agent Lens | Stored-span readback checked real requests/tools against independent receipts. The copied hosted notebook’s conversation was also inspected in the native UI. [Capture](../evidence/hosted-agent-lens.png). |
| Solar | Six GOES configurations, two manual image architectures, two research rounds, tested composition/KEEP, frozen image and measurement comparisons completed. [Results](../evidence/solar-rehearsal.json). |
| Pending | Two improvement rounds, real local MCP, all 12 final executions and 12 available explanation judgments completed. All versions passed; no quality advantage was demonstrated. [Results](../evidence/pending-rehearsal.json). |
| Evaluations | W&B tables and Weave evaluations published. Native EvalTables returned HTTP 500, including the final comparison; its status is explicitly unavailable. Retry publication alone after the service recovers. |
| Public access | Solar Report rendered signed out. Forge notebook templates require sign-in before copying. The 26.1 MB dataset downloaded anonymously and matched its SHA-256. [Checks](../evidence/public-access.json). |
| Browser | All six chapters inspected on desktop; narrow layout captured. A fresh hosted copy passed setup and trace export. The complete paid path ran through the same runtime via rehearsal scripts; it has not been driven entirely through a fresh external attendee’s browser. |

## Timing and cost

On the rehearsal Mac, solar training took 30.1 seconds summed over all executed training attempts, with a maximum of 2.26 seconds per training subprocess. Research-agent provider requests took 489 seconds summed across seven calls. Pending used 130 requests totaling 650 seconds of provider time. These totals exclude human review, downloads and publication time; they are not end-to-end classroom timings. [Machine-readable measurements](../evidence/timing.json).

Measured inference was **$0.027084 for Solar** and **$0.039720 for Pending**. Unknown usage and in-flight reservations were zero at completion. Costs include the recorded retries and qualification attempts. Notebook compute is separate; local CPU rehearsal incurred no new hosted training charge. A hosted CPU rehearsal and participant pacing check remain necessary before claiming the four-hour schedule is proven.

## What the results mean

The final image error fell from 0.122442 (manual residual model) to 0.120769 (agent-selected masked-L1 model), about 1.37% relative. The agent’s second-round cosine schedule regressed on validation and was rejected. These 199 overlapping windows come from two days and one seed; they do not establish a general forecasting improvement.

The GOES models were undertrained at the 60-step teaching budget: final error 2.469 versus persistence 0.193 in log10 flux units. Keep this failure visible and inspect the learning curve. A longer, equally applied training budget is a possible next exercise, not an unreported repair to these results.

Qualification retained an initial proposal without the complete active config, its ineffective default-value change, a refreshed proposal with config, and all associated costs. The final demonstration uses the later reviewed two-round sequence. This is a runtime rehearsal, not a preregistered treatment comparison.

## Remaining release gates

- An external attendee must copy the final template into a different account, check its own inference entitlement, train, and restore a destroyed runtime.
- A developer and a less technical participant must complete the code exercises and explain their results without facilitator takeover.
- Recheck native EvalTables when its HTTP 500 is repaired. Until then, teach the clearly labeled Weave/notebook comparison path.

Older Pending releases and attendee copies are untouched. No core product code changed.
