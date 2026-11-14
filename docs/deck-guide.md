# Workshop decks

Use each deck to explain the next code change, then leave the exercise instructions on screen while participants work in the notebook. The Solar workshop covers forecasting experiments in a research lab. Pending, Inc. covers an office agent handling billing and account access.

The expanded decks teach the foundations and the implementation in one session. Pending and Inspection take four hours; Routing takes five and a half; Solar and Transit take six. These allocations include exercises and breaks. Participants need basic Python, but do not need to arrive knowing the metrics, tensor shapes or coordination mechanisms.

Follow the same request, observation or proposed edit through its intermediate values before moving to a product screen. Then ask participants to explain one value and find the code that produced it. The diagrams retain their positions as each operation appears. The PDF includes those states so it can be read without the presenter.

Each exercise links to a worked answer after the main deck. Give participants time to try before opening it, then use the return link to resume. When showing a rehearsal capture, say that it is a recorded result.

The [visual sequence guide](visual-sequence.md) explains the new selectors, code highlights, branch connections, and questions to ask at each view. Advance one operation at a time, then ask someone to point to the value that changed. These inspection controls read saved records; execution still requires a separate run button.

## Solar forecasting with agent-assisted experiments

Follow the [six-hour runbook](facilitator.md) and [slide-by-slide presenter notes](../decks/solar/notes/facilitator-notes.md). The diagrams add one part at a time in both the browser deck and PDF.

Start by showing the observations and the forecast each exercise asks participants to make. Use GOES measurements to predict X-ray flux 30 minutes ahead, then AIA observations to predict a solar image one hour ahead. A forecast that copies the latest observation provides the first comparison. The fictional lab introduction explains why a score is difficult to interpret when its code and settings are missing.

Participants first implement and record their own models. They compare six configurations, inspect the learning curves, and repeat the experiment structure for images. Explain the difference between changing a learning rate, selecting an implemented architecture, and asking an agent to write new training code.

For the agent exercise, read both proposed diffs before training them. Compare their validation errors, ask the agent which changes to keep, and test the chosen code. The next round uses that code and a saved explanation of what happened. The language model remains fixed throughout; each training run fits the forecasting model's weights.

Choose the final source and trained weights before evaluating the reserved dates. Discuss the measurement and image results separately because their targets and error metrics differ.

Use the [README setup instructions](../README.md#start-in-forge) to copy the notebook into each participant’s project. They use their own Forge account. Explain the inference allowance during setup and note that notebook compute is billed separately.

## Pending, Inc.

Use the [current Pending browser deck](https://ash0ts.github.io/forge-workshop-kit/pending/) with the [current notebook template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view). The deck follows the same eight steps and uses the participant’s own project. Its tools run in local Python; onboarding calls a local MCP server. Follow the [presenter notes](../decks/pending/notes/facilitator-notes.md) for the four-hour session. The [Pending runbook](pending-facilitator.md) includes exercise time and both breaks.

The opening office scene is fictional. Recorded product screens come from the v0.3.0 rehearsal. The editor kept the previous instructions after round one, then changed the verification skill in round two. All three versions passed all four final cases. Show the changed file and the execution that loaded it, then explain that the final scores did not improve.

The [November 12 deck](https://github.com/ash0ts/pending-inc-workshop/releases/tag/workshop-2026-11-12) is preserved as a historical release. Its gateway setup and remote Sandbox registration do not apply to this notebook.

### Current Pending exercise references

The current deck explains each change with a concrete input and output before the exercise. Leave the exercise slide visible while participants write their code. Use these current controls:

| Topic | Current notebook step and editable code | Current action |
| --- | --- | --- |
| Trace a tool operation | **1 · Connect and trace**; `my_tool_span`, `my_model_span` | **Check my project and restore saved work**, then **Run this check and verify my Agent Lens trace** |
| Implement invoice lookup | **2 · Build an invoice tool**; `my_invoice_tool` | **Test my invoice lookup** |
| Pass tool results to the model | **3 · Pass observations to the agent**; `my_dispatch`, `my_observation` | **Test my tool-to-model handoff**, then **Freeze this executor and run the two starting tickets** |
| Check account state and the agent's explanation | **4 · Check the work**; `my_state_check`, `my_judge_validation`, judge rubric | **Test my scorer against four known examples**, then **Judge and publish the starting development comparison** |
| Edit the verification procedure | **5 · Edit one procedure**; selected evidence and verification skill | **Save this procedure and rerun both development tickets** |
| Propose and test procedure changes | **6 · Improve twice**; visible proposal, probe, composition and adoption code | Use the one current **Round N · …** control. Review the displayed diff before testing; the notebook advances from saved records. |
| Compare three versions on fresh cases | **7 · Compare fresh tickets**; frozen versions and independent scoring | **Freeze versions and run 12 evaluations** |
| Explain the result | **8 · Explain the result**; conclusion and evidence links | **Publish my conclusion with the comparison and evidence**. The optional ARIA prompt asks for analysis, not new executions. |

The invoice tool runs in local Python and onboarding uses actual local MCP. The participant's credentials publish directly to their project. Do not use the historical deck's remote Sandbox registration, gateway URL, host tokens, or renewal instructions. The editor changes the harness after the participant's executor is frozen; it cannot replace the tool loop or trusted final scorer.

The current authored cells live in `scripts/pending_cells.py`; the generated attendee notebook is `notebooks/pending_inc.py`. Those files are the source of truth for button labels and prerequisites.

## Product screens

Ask participants to open their own runs when possible. In Agent Lens, choose a particular model request or tool call and inspect its arguments and result. In W&B, find the settings and files used for a training run. In Weave or EvalTables, compare predictions for the same input rather than starting with the averages.

Use **Compare in EvalTables** to open the native Evaluation Tables Preview in the Forge W&B workspace. Select a row to compare its outputs and scores, then follow its Agent Lens link. This uses the SDK’s Weave backend. The CES backend remains unavailable; see [evaluation setup](evaluations.md).

## Routing, inspection and transit

For [Routing](routing-workshop.md), follow one customer message through features, fitting, prediction and review. Compute a per-intent F1 before averaging across the 77 intents. Separate confidence-based routing from margin-based review selection, and keep the prompted routing sample separate from the classifier evaluation. The release capstone then reproduces the selected model, introduces a labeled loader defect, repairs its intent mapping, and verifies rollback. Its regression batch comes from the development review pool; it is not another test benchmark.

For [Inspection](inspection-workshop.md), keep the same board visible while explaining its whole-image and patch features. Show how the normal reference bank produces distances, how the classifier produces a score, and how a frozen threshold produces a decision. Masks help inspect defects; they are not training inputs. Active and random selection receive equal review budgets.

For [Transit](transit-facilitator.md), follow an after-midnight GTFS departure from its service date to the displayed civil time. Then follow a worker's file edit, test and integration. Explain task ownership through the free two-worker race. Trace one accepted lesson through retrieval into the next worker request before discussing whether it helped.

The authored storyboards own the deck text. Their slide maps link concepts, code references, exercises, evidence and time allocations. Worked answers use stable identities so inserting an explanation does not send a learner back to the wrong exercise. Existing participant code and saved execution identities remain unchanged.
