# Demo the two workshop flows

Use these saved rehearsals when introducing the workshops or showing a result while a participant's run finishes. Opening these pages does not run an experiment. Tell the audience when you switch from their work to the recorded example.

| Workshop | Participant notebook | Companion deck | Results and walkthrough links |
| --- | --- | --- | --- |
| Pending, Inc. | [Copy the office notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | [Pending deck](https://ash0ts.github.io/forge-workshop-kit/pending/) | [November 13 Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==) |
| Solar Forecasting Lab | [Copy the research notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | [Solar deck](https://ash0ts.github.io/forge-workshop-kit/solar/) | [November 13 Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==) |

These links follow one November 13 rehearsal per workshop. The project's default workspace also includes template uploads, setup checks and earlier rehearsals. Use the linked records rather than combining events from different sessions.

Participants copy a template into their own project, check access, and work through its steps. They use their own Forge authentication, inference access and notebook compute. There is no shared gateway or facilitator token. The [setup instructions](../README.md#start-in-forge) cover hosted and laptop use.

## Pending, Inc. in eight minutes

The office and customer accounts are fictional. The model requests, tool calls, edited instructions and evaluations are real executions of that simulator.

1. **Show the task and the code.** In the notebook, open **Build an invoice tool** and show `my_invoice_tool`. Then open **Pass observations to the agent** and point to `my_dispatch` and `my_observation`. Explain that a returned tool result must enter the next model request for the employee to use it.
2. **Follow one actual ticket.** Open the [verification-gate candidate](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46). Find the rejected `finish`, the `check_work` call, and the accepted completion afterward. Ask: “What did the added rule make the employee do?”
3. **Inspect a recovery.** Open the [original onboarding conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/319b6f367f8f69026d7e37aff42e3bc7). Find `provision_member` and the `onboarding_status` read afterward. The write had already committed before its response timed out. The status read established what happened before the employee decided how to continue.
4. **Show the editor's decision.** In **Improve twice**, open the actual diff. The first candidate set `verify_before_finish` to true. The [round-one composition](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c04f575608c6f43d99e1b7b428a23791) retained the previous harness because the extra gate added work without improving the probes. The [round-two composition](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a39aede201a0fe7320092976c0501e42) instead revised the verification skill. Follow it into its [subsequent execution](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/d641da20ff5e553866a93a3c12bee913).
5. **Compare the fresh tickets.** Open the November 13 Pending Report. All 12 state checks and explanation judgments pass. The changed skill did not improve these already-passing final scores. Retaining a version and testing a changed version are both visible in the branch history.
6. **Ask for an interpretation.** “Did this show a better agent, or a working way to test changes?” This rehearsal shows the latter. Ask which additional billing or access case would challenge the retained procedure.

For the full session, use the notebook's eight steps and the [current control reference](deck-guide.md#current-pending-exercise-references). Keep the account state and explanation judgment separate when discussing results.

## Solar Forecasting Lab in ten minutes

The lab's failed handoff is fictional. The GOES-15 measurements and AIA 171 Å images are observations from February 2014. Use the [data and evidence review](solar-evidence.md) for acquisition, processing and result details.

1. **Start with a forecast people can read.** Open the image result in the notebook: previous image, current image, predicted future, observed future and error. Point to the timestamp shared by the versions. Explain that persistence copies the current observation into the future.
2. **Show how the experiment is recorded.** Open the [measurement Sweep](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pzigourv). Compare two configurations and their learning curves. This search changes settings within existing implementations; it does not write a new model.
3. **Show what the research agent receives.** Open the [first proposal conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7). Inspect `read_validation_evidence` and the model request. The agent sees training and validation evidence, not reserved-date results. This request also shows an output-limit interruption and the recorded retry.
4. **Follow one code change into training.** Round one changes the training loss to masked absolute error. In [round two](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f67b35115662dea4c433dcd112ad6d68), the agent proposes a zero-initialized residual head. That makes its initial forecast equal persistence before training learns a correction. Open the [adopted training conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289) and [its saved files](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0) to connect the source, weights and predictions.
5. **Compare the reserved dates.** In the November 13 Solar Report, show image error separately from GOES error. Image error falls from 0.122442 for the manual model to 0.110011 for the agent-selected model, a 10.15% relative reduction. These are 199 overlapping windows from two days and one seed. The GOES model loses to persistence: 2.468975 versus 0.192706 log-flux MAE.
6. **Ask for the next experiment.** “Would this edit still help with another seed and another date range?” The observed image improvement is a reason to test that question. The GOES failure needs its own investigation; averaging the two tasks together would hide it.

Keep the two kinds of model change explicit: the research agent stays fixed while it edits code; the forecasting model trains new weights. Follow the [four-hour runbook](facilitator.md) for the hands-on session.

## When a product view is unavailable

- **The hosted notebook preview is blank:** the current browser check hit a public-page-to-local-network error in the embedded preview. The **Copy to project** dialog opened, but that does not verify a copied notebook can run. Try copying the template into your project; if the copied notebook cannot start, use the [laptop setup](../README.md#start-on-your-laptop). The downloadable HTML is a saved preview, not a running notebook. Its initial Solar and Pending screens render directly at desktop and phone widths. [Preview checks](../evidence/ux-v023-static-exports.json).
- **Agent Lens asks for sign-in:** use the saved notebook view or clearly labeled capture while the participant signs in. A Report link does not grant access to someone else's project.
- **Native EvalTables is unavailable:** our recorded publications returned HTTP 500. Show the actual notebook comparison, Weave evaluation or W&B Table and name it correctly. Publication can be retried from saved results without repeating training or model calls.
- **A judgment is missing:** show the execution and the failure separately. A missing explanation judgment is not an incorrect account state and is not a zero score.
- **A participant is still running:** demonstrate the recorded result, then return to their own project. Their unexecuted edits did not produce the rehearsal's outcome.

The saved rehearsal records are [Pending](../evidence/v030-pending-rehearsal.json) and [Solar](../evidence/solar-rehearsal-v030-audit.json). These results are teaching rehearsals, not a repeated benchmark.
