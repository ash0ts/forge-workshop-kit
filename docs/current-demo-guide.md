# Demo the two workshop flows

Use these saved rehearsals when introducing the workshops or showing a result while a participant's run finishes. Opening these pages does not run an experiment. Tell the audience when you switch from their work to the recorded example.

| Workshop | Participant notebook | Recorded runs | Results and walkthrough links |
| --- | --- | --- | --- |
| Pending, Inc. | [Copy the office notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | [Pending dashboard](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=nkyxiy1o6wn) | [Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-51a0006f--VmlldzoxODMwMjcxMA==) |
| Solar Forecasting Lab | [Copy the research notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | [Solar dashboard](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=ogpa6vhy8db) | [Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==) |

The named dashboards select each rehearsal's runs. The project's default workspace includes template uploads, setup checks and other workshop sessions. Use the links above for the demonstration.

Participants copy a template into their own project, check access, and work through its steps. They use their own Forge authentication, inference access and notebook compute. There is no shared gateway or facilitator token. The [setup instructions](../README.md#start-in-forge) cover hosted and laptop use.

## Pending, Inc. in eight minutes

The office and customer accounts are fictional. The model requests, tool calls, edited instructions and evaluations are real executions of that simulator.

1. **Show the task and the code.** In the notebook, open **Build an invoice tool** and show `my_invoice_tool`. Then open **Pass observations to the agent** and point to `my_dispatch` and `my_observation`. Explain that a returned tool result must enter the next model request for the employee to use it.
2. **Follow one actual ticket.** Open the [billing conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a5e6d591a1e0a977954efd67bae60ecc). Select `get_account`, read its arguments, and inspect the returned payments. Ask: “Which account did this call actually read, and which payment did the employee refund?”
3. **Inspect a recovery.** Open the [onboarding conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/911e3062cf37ac66f5b9944464a27fae). Find the write that timed out and the state read afterward. The write had already committed. A repeated write could have caused another change; the state read established what happened.
4. **Show the editor's alternatives.** In **Improve twice**, open the saved branch view and a candidate's actual diff. The [first proposal conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/e59f98a0cc5d76c8e5939212b2ec009b) shows the editor's response. The [composition conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ab8601f17816d231b44cac6f77f33f6c) explains its choice to retain the current harness. That is a decision, followed by a test, rather than a new executable version.
5. **Compare the fresh tickets.** Open the Pending dashboard or Report. All 12 state checks pass. The three comparison labels represent two distinct harnesses because both rounds retained the manual revision. Eleven explanation judgments are available and pass; one remains unavailable after its output limit and a judge-only retry.
6. **Ask for an interpretation.** “Did this show a better agent, or a working way to test changes?” This rehearsal shows the latter. Ask which additional billing or access case would challenge the retained procedure.

For the full session, use the notebook's eight steps and the [current control reference](deck-guide.md#current-pending-exercise-references). Keep the account state and explanation judgment separate when discussing results.

## Solar Forecasting Lab in ten minutes

The lab's failed handoff is fictional. The GOES-15 measurements and AIA 171 Å images are observations from February 2014. Use the [data and evidence review](solar-evidence.md) for acquisition, processing and result details.

1. **Start with a forecast people can read.** Open the image result in the notebook: previous image, current image, predicted future, observed future and error. Point to the timestamp shared by the versions. Explain that persistence copies the current observation into the future.
2. **Show how the experiment is recorded.** Open the [measurement Sweep](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pr1xsoaw). Compare two configurations and their learning curves. This search changes settings within existing implementations; it does not write a new model.
3. **Show what the research agent receives.** Open the [first proposal conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4). Inspect `read_validation_evidence` and the model request. The agent sees training and validation evidence, not reserved-date results.
4. **Follow one code change into training.** Open the [zero-initialized residual model run](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/c07c5d78722ad00dd3c397a69a497d3e). Compare its saved source with the manual model. Zero initialization makes its initial forecast equal persistence before training learns a correction. The second round adds masked absolute-error training loss. Open the [tested second-round files](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f5e5d198bc9479f78d9a4b1c8c8979e3/v0) to connect the code, weights and predictions.
5. **Compare the reserved dates.** In the Solar dashboard or Report, show image error separately from GOES error. Image error falls from 0.122442 for the manual model to 0.110011 for the agent-selected model, a 10.15% relative reduction. These are 199 overlapping windows from two days and one seed. The GOES model loses to persistence: 2.468975 versus 0.192706 log-flux MAE.
6. **Ask for the next experiment.** “Would this edit still help with another seed and another date range?” The observed image improvement is a reason to test that question. The GOES failure needs its own investigation; averaging the two tasks together would hide it.

Keep the two kinds of model change explicit: the research agent stays fixed while it edits code; the forecasting model trains new weights. Follow the [four-hour runbook](facilitator.md) for the hands-on session.

## When a product view is unavailable

- **The hosted notebook preview is blank:** the current browser check hit a public-page-to-local-network error in the embedded preview. The **Copy to project** dialog opened, but that does not verify a copied notebook can run. Try copying the template into your project; if the copied notebook cannot start, use the [laptop setup](../README.md#start-on-your-laptop). The downloadable HTML is a saved preview, not a running notebook. Its initial Solar and Pending screens render directly at desktop and phone widths. [Preview checks](../evidence/ux-v023-static-exports.json).
- **Agent Lens asks for sign-in:** use the saved notebook view or clearly labeled capture while the participant signs in. A Report link does not grant access to someone else's project.
- **Native EvalTables is unavailable:** our recorded publications returned HTTP 500. Show the actual notebook comparison, Weave evaluation or W&B Table and name it correctly. Publication can be retried from saved results without repeating training or model calls.
- **A judgment is missing:** show the execution and the failure separately. A missing explanation judgment is not an incorrect account state and is not a zero score.
- **A participant is still running:** demonstrate the recorded result, then return to their own project. Their unexecuted edits did not produce the rehearsal's outcome.

The complete saved records are [Pending](../evidence/ux-v020-pending.json) and [Solar](../evidence/ux-v020-solar.json). These results are teaching rehearsals, not a repeated benchmark.
