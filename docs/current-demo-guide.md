# Demonstrate the workshops

Use these saved rehearsals to show how an instruction or code change affects an agent's work. Participants can follow the same sequence in their own notebook: run the starting version, inspect a failure or limitation, edit the code, and compare the results. Tell the audience when you switch to the recorded example. Opening its pages does not run an experiment.

Begin with the notebook's bundled development example before connecting an account. Ask what should change and what should remain intact. Show one result before a batch, and ask for a diagnosis before opening a worked answer. For a candidate comparison, let someone choose a version and explain their choice before revealing the editor's decision. These prompts are discussion, not additional approval forms.

Choose a template and deck from the [workshop catalog](../README.md#choose-your-workshop). This guide gives short walkthroughs for all six; the [recorded results](recorded-results.md) collects their outcomes and qualifications.

The Pending and Solar walkthroughs below follow the November 13 rehearsals. The qualification follow-ups below preserve those results and explain what changed afterward. The project's default workspace also includes template uploads, setup checks and earlier rehearsals. Use the linked records rather than combining events from different sessions.

Open the [native evaluation comparisons](evaluations.md#open-the-recorded-comparisons) when comparing individual cases. These named workspaces select the relevant versions and leave the project default unchanged.

Participants copy a template into their own project, check access, and work through its steps. They use their own Forge authentication, inference access and notebook compute. There is no shared gateway or facilitator token. The [setup instructions](setup.md) cover hosted and laptop use.

## Show one ARIA citation check

Use this in place of the final discussion in a short demo. Open the [Pending conclusion activity](https://ash0ts.github.io/forge-workshop-kit/pending/aria-conclusion/). Do not introduce another experiment.

1. **Select the result and ask for an interpretation.** In Pending, show the three frozen harnesses: each passed four fresh tickets. Ask whether a different tool sequence establishes better account correctness.
2. **Ask ARIA or open the recording.** Use the notebook’s **Check our conclusion** card. Choose **Copy investigation prompt**, open the selected Forge record, and check ARIA’s project before sending. If live access is unavailable, choose **Use the recorded investigation**. The [actual instructor response](https://forge.coreweave.com/aria/threads/01a1e061-ff2e-7471-a695-0877d87d71aa) says the result does not show higher correctness for any harness. Its [bundled transcript and captures](../src/forge_workshop_kit/assets/aria/pending_inc/conclusion.json) remain accessible without that chat’s permissions.
3. **Check what ARIA actually established.** Open the [selected final-comparison run](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/fdcf3eb3fbcae1cf6b7b765e7654c36b) and its saved comparison. Match the four account checks per version. ARIA retrieved run summaries but used supplied execution excerpts for those counts; do not describe its answer as independent trace verification.
4. **Save the conclusion in your own words.** Use **Save citation check** to mark the claim supported, disputed, or unresolved. A supported tie still leaves a useful next question: which additional ticket could expose the value of the added checking?

The [activity guide](aria-investigations.md#use-the-investigation-card) gives the exact controls, evidence boundaries, and access fallback for all twelve stops. A pasted URL does not prove ARIA read a record. ARIA usage follows the organization’s settings and is outside the notebook’s inference allowance.

## Pending, Inc. in eight minutes

The agent handles a duplicate charge and an account-access request for a fictional company. Participants write its tools and the code that passes tool results back to the model. They then test changes to its instructions and procedures. The customer accounts are fictional; the saved model requests, tool calls and evaluations came from actual executions of that simulator.

1. **Show the task and the code.** In the notebook, open **Build an invoice tool** and show `my_invoice_tool`. Then open **Pass observations to the agent** and point to `my_dispatch` and `my_observation`. Explain that a returned tool result must enter the next model request for the employee to use it.
2. **Follow one actual ticket.** Open the [candidate that requires a check before completion](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46). Find the rejected `finish`, the `check_work` call, and the accepted completion afterward. Ask: “What did the added rule make the employee do?”
3. **Inspect a recovery.** Open the [original onboarding conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/319b6f367f8f69026d7e37aff42e3bc7). Find `provision_member` and the `onboarding_status` read afterward. The write had already committed before its response timed out. The status read established what happened before the employee decided how to continue.
4. **Show the editor's decision.** In **Improve twice**, open the actual diff. The first candidate set `verify_before_finish` to true. The editor's [round-one composition decision](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c04f575608c6f43d99e1b7b428a23791) kept the previous harness because the extra check added work without improving the candidate tests. Its [round-two decision](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a39aede201a0fe7320092976c0501e42) revised the verification skill. Follow that file change into the [execution that used it](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/d641da20ff5e553866a93a3c12bee913).
5. **Compare the fresh tickets.** Open the [November 13 Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==). All 12 state checks and explanation judgments pass. The changed skill did not improve these already-passing final scores. Retaining a version and testing a changed version are both visible in the branch history.
6. **Discuss what changed.** Ask: “Which edit changed the tool sequence? Did that change improve either score?” The added checks changed behavior without raising the final scores. Ask participants to suggest a billing or access case that would test whether those checks are useful.

For the full session, use the notebook's eight steps and the [current control reference](deck-guide.md#current-pending-exercise-references). Keep the account state and explanation judgment separate when discussing results.

## Solar forecasting in ten minutes

Participants predict future solar measurements and images, then ask an agent to modify the image model's training code. They compare every change using the same data partitions and scoring rule. The lab setting is fictional. The GOES-15 measurements and AIA 171 Å images are real observations from February 2014; the [data and evidence review](solar-evidence.md) explains their acquisition, processing and results.

1. **Start with a forecast people can read.** Open the image result in the notebook: previous image, current image, predicted future, observed future and error. Point to the timestamp shared by the versions. Explain that persistence copies the current observation into the future.
2. **Show how the experiment is recorded.** Open the [measurement Sweep](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pzigourv). Compare two configurations and their learning curves. This search changes settings within existing implementations; it does not write a new model.
3. **Show what the research agent receives.** Open the [first proposal conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7). Inspect `read_validation_evidence` and the model request. The agent sees training and validation evidence, not reserved-date results. This request also shows an output-limit interruption and the recorded retry.
4. **Follow one code change into training.** Round one changes the training loss to absolute error within the solar-disk mask. In [round two](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f67b35115662dea4c433dcd112ad6d68), the agent initializes the residual model's output layer to zero. The model initially predicts no change from the current image, then training learns a correction. Open the [selected version's training call](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289) and [its saved files](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0). Find those two edits in the source and the weights produced by that run.
5. **Compare the reserved dates.** In the [November 13 Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==), show image error separately from GOES error. Image error falls from 0.122442 for the manual model to 0.110011 for the agent-selected model, a 10.15% relative reduction. These are 199 overlapping windows from two days and one seed. The GOES model loses to persistence: 2.468975 versus 0.192706 log-flux MAE.
6. **Ask for the next experiment.** “Would this edit still help with another seed and another date range?” The observed image improvement is a reason to test that question. The GOES failure needs its own investigation; averaging the two tasks together would hide it.

Explain which model is changing. We use the same language model for the research agent throughout the workshop. It edits Python code; running that code trains the small forecasting model's weights. Follow the [six-hour runbook](facilitator.md) for the hands-on session.

## Show the qualified repairs

In Pending's **Pass observations to the agent** step, edit `recover_access` and click **Compare the two retry procedures**. A new operation ID adds Alex twice; reusing the original ID and reading the account leaves one membership. This is a code repair against actual simulator state. It does not turn the separate 4/4 harness tie into a gain. [Saved repair and native trace links](../evidence/v050-publication-check.json).

For Solar, open the [three-seed qualification](solar-qualification.md). The repaired GOES model has 15.15% lower mean error than persistence and improves all three seeds. The image edit improves two seeds and slightly regresses on the third. Explain why the average image gain does not meet the stricter all-seed teaching gate. These use previously inspected dates and are teaching retests.

## Request routing in six minutes

1. Open the [routing deck](https://ash0ts.github.io/forge-workshop-kit/routing/) and compare a missing card with a card that does not work. Ask which support workflow each needs.
2. Show the TF–IDF and frozen-embedding classifiers. The recorded official-test macro-F1 rises from 0.879385 to 0.920229. Explain that the encoder stays fixed while the classifier is fitted.
3. Open the [recorded judge disagreement](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01). The request says “Can I activate a card in the app?” The judge accepts `activate_my_card`; the dataset says `card_linking`. Ask what else a reviewer would need before accepting a label.
4. In the notebook, save a review, show its dataset version, and follow it into retraining. The participant's later improvement is measured separately from the qualified classifier comparison. [Five-and-a-half-hour instructions](routing-workshop.md).

## Circuit-board inspection in six minutes

1. Open the [inspection deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) and show one actual board before revealing its mask.
2. Compare a whole-image feature vector with the patch-distance grid. The latter can expose small local differences; it is not a defect-segmentation model.
3. Show `pcb1-anomaly-048`, where the patch version catches a defect the whole-image model misses, then `pcb1-anomaly-015`, where the result reverses. Keep the counterexample visible.
4. Open the [recorded Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-defective-parts-before-they-ship:-5ec44d92--VmlldzoxODMwNzU3Nw==). Compare AP, misses, false alarms and review volume. Both active and random selection receive 24 additional labels.
5. Reload a frozen classifier file and reproduce its prediction. The first patch recipe failed; the revised 1.284-point AP gain is a teaching retest. [Protocol and all outcomes](inspection-workshop.md).

## Transit software factory in eight minutes

Use the [transit deck](https://ash0ts.github.io/forge-workshop-kit/transit/) and [R5 results](transit-workshop.md#what-the-final-engineering-rehearsal-showed). The app reads a frozen historical MBTA schedule, not current arrival predictions.

1. **Read a departure.** Show `24:08:00` on service date November 28. It means November 29 at 00:08 in the feed’s timezone. Follow the record into the displayed departure.
2. **Follow a worker’s patch.** Inspect the assigned file, proposed edit, component test, and integration check. Two completed worker tasks do not establish that the combined app works.
3. **Show the coordination repair.** Use the free task-claim check to demonstrate why two workers must not claim the same task. Keep task ownership, project contracts, and accepted lessons distinct.
4. **Compare the delivered builds.** The [first-release table](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=dg2ogm6wp3z) shows 10/10 checks for the solo build and 8/10 for the team. Inspect the matching UTC-input rows: two failed checks expose the same wrong-train selection.
5. **Check what memory changed.** In the [follow-up comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=f9jpm0yjsxy), both builds pass 12/18 checks and their query workers stop at request limits. Find the accepted lesson and the request that received it. Retrieval alone does not establish that it improved the product.
6. **Discuss the release.** Ask which version can be reproduced and which failed checks prevent shipping the follow-up. Elapsed builder time excludes human review and integration. Use the [runbook](transit-facilitator.md) for the full session.

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

- **The hosted notebook preview is blank:** try **Copy to project** and open the editable copy. If it cannot start, use [laptop setup](setup.md#work-locally). A downloadable HTML preview is not a running notebook. The v0.10.0 maintainer check loaded all six previews and their copy controls; external-account execution remains a separate outstanding check. See [release checks](release-checks.md).
- **Agent Lens asks for sign-in:** use the saved notebook view or clearly labeled capture while the participant signs in. A Report link does not grant access to someone else's project.
- **A comparison is unavailable:** use the saved notebook result and choose **Retry publication**. Native EvalTables uses the Weave backend; the CES service remains unavailable. Publication retries do not repeat training or model calls. See [evaluation setup](evaluations.md).
- **A judgment is missing:** show the execution and the failure separately. A missing explanation judgment is not an incorrect account state and is not a zero score.
- **A participant is still running:** demonstrate the recorded result, then return to their own project. Their unexecuted edits did not produce the rehearsal's outcome.

The saved rehearsal records are [Pending](../evidence/v030-pending-rehearsal.json) and [Solar](../evidence/solar-rehearsal-v030-audit.json). These results are teaching rehearsals, not a repeated benchmark.
