# Demonstrate the two workshops

Use these saved rehearsals to show how an instruction or code change affects an agent's work. Participants can follow the same sequence in their own notebook: run the starting version, inspect a failure or limitation, edit the code, and compare the results. Tell the audience when you switch to the recorded example. Opening its pages does not run an experiment.

| Workshop | Participant notebook | Companion deck | Results and walkthrough links |
| --- | --- | --- | --- |
| Pending, Inc. | [Copy the office notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | [Pending deck](https://ash0ts.github.io/forge-workshop-kit/pending/) | [November 13 Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==) |
| Solar forecasting with agent-assisted experiments | [Copy the research notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | [Solar deck](https://ash0ts.github.io/forge-workshop-kit/solar/) | [November 13 Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==) |

These links follow one November 13 rehearsal per workshop. The project's default workspace also includes template uploads, setup checks and earlier rehearsals. Use the linked records rather than combining events from different sessions.

Participants copy a template into their own project, check access, and work through its steps. They use their own Forge authentication, inference access and notebook compute. There is no shared gateway or facilitator token. The [setup instructions](../README.md#start-in-forge) cover hosted and laptop use.

## Pending, Inc. in eight minutes

The agent handles a duplicate charge and an account-access request for a fictional company. Participants write its tools and the code that passes tool results back to the model. They then test changes to its instructions and procedures. The customer accounts are fictional; the saved model requests, tool calls and evaluations came from actual executions of that simulator.

1. **Show the task and the code.** In the notebook, open **Build an invoice tool** and show `my_invoice_tool`. Then open **Pass observations to the agent** and point to `my_dispatch` and `my_observation`. Explain that a returned tool result must enter the next model request for the employee to use it.
2. **Follow one actual ticket.** Open the [candidate that requires a check before completion](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46). Find the rejected `finish`, the `check_work` call, and the accepted completion afterward. Ask: “What did the added rule make the employee do?”
3. **Inspect a recovery.** Open the [original onboarding conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/319b6f367f8f69026d7e37aff42e3bc7). Find `provision_member` and the `onboarding_status` read afterward. The write had already committed before its response timed out. The status read established what happened before the employee decided how to continue.
4. **Show the editor's decision.** In **Improve twice**, open the actual diff. The first candidate set `verify_before_finish` to true. The editor's [round-one composition decision](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c04f575608c6f43d99e1b7b428a23791) kept the previous harness because the extra check added work without improving the candidate tests. Its [round-two decision](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a39aede201a0fe7320092976c0501e42) revised the verification skill. Follow that file change into the [execution that used it](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/d641da20ff5e553866a93a3c12bee913).
5. **Compare the fresh tickets.** Open the November 13 Pending Report. All 12 state checks and explanation judgments pass. The changed skill did not improve these already-passing final scores. Retaining a version and testing a changed version are both visible in the branch history.
6. **Discuss what changed.** Ask: “Which edit changed the tool sequence? Did that change improve either score?” The added checks changed behavior without raising the final scores. Ask participants to suggest a billing or access case that would test whether those checks are useful.

For the full session, use the notebook's eight steps and the [current control reference](deck-guide.md#current-pending-exercise-references). Keep the account state and explanation judgment separate when discussing results.

## Solar forecasting in ten minutes

Participants predict future solar measurements and images, then ask an agent to modify the image model's training code. They compare every change using the same data partitions and scoring rule. The lab setting is fictional. The GOES-15 measurements and AIA 171 Å images are real observations from February 2014; the [data and evidence review](solar-evidence.md) explains their acquisition, processing and results.

1. **Start with a forecast people can read.** Open the image result in the notebook: previous image, current image, predicted future, observed future and error. Point to the timestamp shared by the versions. Explain that persistence copies the current observation into the future.
2. **Show how the experiment is recorded.** Open the [measurement Sweep](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pzigourv). Compare two configurations and their learning curves. This search changes settings within existing implementations; it does not write a new model.
3. **Show what the research agent receives.** Open the [first proposal conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7). Inspect `read_validation_evidence` and the model request. The agent sees training and validation evidence, not reserved-date results. This request also shows an output-limit interruption and the recorded retry.
4. **Follow one code change into training.** Round one changes the training loss to absolute error within the solar-disk mask. In [round two](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f67b35115662dea4c433dcd112ad6d68), the agent initializes the residual model's output layer to zero. The model initially predicts no change from the current image, then training learns a correction. Open the [selected version's training call](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289) and [its saved files](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0). Find those two edits in the source and the weights produced by that run.
5. **Compare the reserved dates.** In the November 13 Solar Report, show image error separately from GOES error. Image error falls from 0.122442 for the manual model to 0.110011 for the agent-selected model, a 10.15% relative reduction. These are 199 overlapping windows from two days and one seed. The GOES model loses to persistence: 2.468975 versus 0.192706 log-flux MAE.
6. **Ask for the next experiment.** “Would this edit still help with another seed and another date range?” The observed image improvement is a reason to test that question. The GOES failure needs its own investigation; averaging the two tasks together would hide it.

Explain which model is changing. We use the same language model for the research agent throughout the workshop. It edits Python code; running that code trains the small forecasting model's weights. Follow the [four-hour runbook](facilitator.md) for the hands-on session.

## When a product view is unavailable

- **The hosted notebook preview is blank:** the current browser check hit a public-page-to-local-network error in the embedded preview. The **Copy to project** dialog opened, but that does not verify a copied notebook can run. Try copying the template into your project; if the copied notebook cannot start, use the [laptop setup](../README.md#start-on-your-laptop). The downloadable HTML is a saved preview, not a running notebook. Its initial Solar and Pending screens render directly at desktop and phone widths. [Preview checks](../evidence/ux-v023-static-exports.json).
- **Agent Lens asks for sign-in:** use the saved notebook view or clearly labeled capture while the participant signs in. A Report link does not grant access to someone else's project.
- **Native EvalTables is unavailable:** our recorded publications returned HTTP 500. Show the actual notebook comparison, Weave evaluation or W&B Table and name it correctly. Publication can be retried from saved results without repeating training or model calls.
- **A judgment is missing:** show the execution and the failure separately. A missing explanation judgment is not an incorrect account state and is not a zero score.
- **A participant is still running:** demonstrate the recorded result, then return to their own project. Their unexecuted edits did not produce the rehearsal's outcome.

The saved rehearsal records are [Pending](../evidence/v030-pending-rehearsal.json) and [Solar](../evidence/solar-rehearsal-v030-audit.json). These results are teaching rehearsals, not a repeated benchmark.
