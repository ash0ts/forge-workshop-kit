# Demonstrate the workshops

Use these saved rehearsals to show how an instruction or code change affects an agent's work. Participants can follow the same sequence in their own notebook: run the starting version, inspect a failure or limitation, edit the code, and compare the results. Tell the audience when you switch to the recorded example. Opening its pages does not run an experiment.

| Workshop | Participant notebook | Companion deck | Results and walkthrough links |
| --- | --- | --- | --- |
| Pending, Inc. | [Copy the office notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | [Pending deck](https://ash0ts.github.io/forge-workshop-kit/pending/) | [November 13 Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==) |
| Solar forecasting with agent-assisted experiments | [Copy the research notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | [Solar deck](https://ash0ts.github.io/forge-workshop-kit/solar/) | [November 13 Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==) |

The Pending and Solar links above follow the November 13 rehearsals. The qualification follow-ups below preserve those results and explain what changed afterward. The project's default workspace also includes template uploads, setup checks and earlier rehearsals. Use the linked records rather than combining events from different sessions.

Open the [native evaluation comparisons](evaluations.md#open-the-recorded-comparisons) when comparing individual cases. These named workspaces select the relevant versions and leave the project default unchanged.

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

Explain which model is changing. We use the same language model for the research agent throughout the workshop. It edits Python code; running that code trains the small forecasting model's weights. Follow the [six-hour runbook](facilitator.md) for the hands-on session.

## Show the qualified repairs

In Pending's **Pass observations to the agent** step, edit `recover_access` and click **Compare the two retry procedures**. A new operation ID adds Alex twice; reusing the original ID and reading the account leaves one membership. This is a code repair against actual simulator state. It does not turn the separate 4/4 harness tie into a gain. [Saved repair and native trace links](../evidence/v050-publication-check.json).

For Solar, open the [three-seed qualification](solar-qualification.md). The repaired GOES model has 15.15% lower mean error than persistence and improves all three seeds. The image edit improves two seeds and slightly regresses on the third. Explain why the average image gain does not meet the stricter all-seed teaching gate. These use previously inspected dates and are teaching retests.

## Request routing in six minutes

1. Open the [routing deck](https://ash0ts.github.io/forge-workshop-kit/routing/) and compare a missing card with a card that does not work. Ask which support workflow each needs.
2. Show the TF–IDF and frozen-embedding classifiers. The recorded official-test macro-F1 rises from 0.879385 to 0.920229. Explain that the encoder stays fixed while the classifier is fitted.
3. Open the [recorded judge disagreement](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01). The request says “Can I activate a card in the app?” The judge accepts `activate_my_card`; the dataset says `card_linking`. Ask what else a reviewer would need before accepting a label.
4. In the notebook, save a review, show its dataset version, and follow it into retraining. The participant's later improvement is measured separately from the qualified classifier comparison. [Four-hour instructions](routing-workshop.md).

## Circuit-board inspection in six minutes

1. Open the [inspection deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) and show one actual board before revealing its mask.
2. Compare a whole-image feature vector with the patch-distance grid. The latter can expose small local differences; it is not a defect-segmentation model.
3. Show `pcb1-anomaly-048`, where the patch version catches a defect the whole-image model misses, then `pcb1-anomaly-015`, where the result reverses. Keep the counterexample visible.
4. Open the [recorded Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-defective-parts-before-they-ship:-5ec44d92--VmlldzoxODMwNzU3Nw==). Compare AP, misses, false alarms and review volume. Both active and random selection receive 24 additional labels.
5. Reload a frozen classifier file and reproduce its prediction. The first patch recipe failed; the revised 1.284-point AP gain is a teaching retest. [Protocol and all outcomes](inspection-workshop.md).

## Airline monitoring in ten minutes

Use the [airline notebook source](../notebooks/airline_monitoring.py), [deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/), and [qualification record](airline-monitoring-qualification.md). The airline records are fictional, adapted from a pinned Sierra tau-bench release. Scripted passengers confirm or reject exact itinerary changes; there is no live booking service.

1. **Read the request and starting booking.** Identify the flights the passenger wants changed and the flights that should remain. The update tool replaces the whole itinerary. A successful API call alone does not establish that the change was correct.
2. **Follow the actual operations in Agent Lens.** Find the reservation read, quoted itinerary, passenger confirmation, and saved update. Contrast a recovered timeout with an unresolved request. A tool error and a bad passenger outcome are different observations.
3. **Show the controlled example separately.** Open the labeled omitted-return calibration incident and a valid connection-to-nonstop control. Both shorten an itinerary, but only one removes an unrequested flight. No model generated the calibration mistake.
4. **Review the native tag.** Show its criteria, exact agent scope, and manually labeled Alignment examples. Be explicit: the six tested AI Alignment requests returned HTTP 500, and this new session had no Insights clusters. Do not demonstrate calculated monitor accuracy as if either feature produced results.
5. **Turn the review into a test.** Save the original request, booking, reviewed expectation, and source event. Run the free regression comparison with the participant's itinerary builder. It uses those saved cases and shows the proposed flights, confirmation, resulting booking, and independent checks.
6. **Finish with the live comparison.** All 40 live conversations passed. Starting and repaired agents each passed 6/6 reserved and 4/4 subsequent requests. The controlled adapter repair works; this small live comparison did not show a quality gain. Ask which additional request would test its value.

This is a technical-preview walkthrough. Native service recovery, external-account access, and human rehearsal are still required before presenting the six-hour workshop as ready for attendees. Native automatic tagging is separately billed; verify **Apply with AI** is off when the demonstration ends.

## When a product view is unavailable

- **The hosted notebook preview is blank:** the current browser check hit a public-page-to-local-network error in the embedded preview. The **Copy to project** dialog opened, but that does not verify a copied notebook can run. Try copying the template into your project; if the copied notebook cannot start, use the [laptop setup](../README.md#start-on-your-laptop). The downloadable HTML is a saved preview, not a running notebook. Its initial Solar and Pending screens render directly at desktop and phone widths. [Preview checks](../evidence/ux-v023-static-exports.json).
- **Agent Lens asks for sign-in:** use the saved notebook view or clearly labeled capture while the participant signs in. A Report link does not grant access to someone else's project.
- **A comparison is unavailable:** use the saved notebook result and choose **Retry publication**. Native EvalTables uses the Weave backend; the CES service remains unavailable. Publication retries do not repeat training or model calls. See [evaluation setup](evaluations.md).
- **A judgment is missing:** show the execution and the failure separately. A missing explanation judgment is not an incorrect account state and is not a zero score.
- **A participant is still running:** demonstrate the recorded result, then return to their own project. Their unexecuted edits did not produce the rehearsal's outcome.

The saved rehearsal records are [Pending](../evidence/v030-pending-rehearsal.json) and [Solar](../evidence/solar-rehearsal-v030-audit.json). These results are teaching rehearsals, not a repeated benchmark.
