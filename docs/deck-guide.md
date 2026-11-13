# Workshop decks

Use each deck to explain the next code change, then leave the exercise instructions on screen while participants work in the notebook. The Solar workshop covers forecasting experiments in a research lab. Pending, Inc. covers an office agent handling billing and account access.

Each exercise links to a worked answer after the main deck. Give participants time to try before opening it, then use the return link to resume. When showing a rehearsal capture, say that it is a recorded result.

## Solar forecasting with agent-assisted experiments

Follow the [four-hour runbook](facilitator.md) and [slide-by-slide presenter notes](../decks/solar/notes/facilitator-notes.md). The diagrams add one part at a time in both the browser deck and PDF.

Start by showing the observations and the forecast each exercise asks participants to make. Use GOES measurements to predict X-ray flux 30 minutes ahead, then AIA observations to predict a solar image one hour ahead. A forecast that copies the latest observation provides the first comparison. The fictional lab introduction explains why a score is difficult to interpret when its code and settings are missing.

Participants first implement and record their own models. They compare six configurations, inspect the learning curves, and repeat the experiment structure for images. Explain the difference between changing a learning rate, selecting an implemented architecture, and asking an agent to write new training code.

For the agent exercise, read both proposed diffs before training them. Compare their validation errors, ask the agent which changes to keep, and test the chosen code. The next round uses that code and a saved explanation of what happened. The language model remains fixed throughout; each training run fits the forecasting model's weights.

Choose the final source and trained weights before evaluating the reserved dates. Discuss the measurement and image results separately because their targets and error metrics differ.

Use the [README setup instructions](../README.md#start-in-forge) to copy the notebook into each participant’s project. They use their own Forge account. Explain the inference allowance during setup and note that notebook compute is billed separately.

## Pending, Inc.

Use the [current Pending browser deck](https://ash0ts.github.io/forge-workshop-kit/pending/) with the [current notebook template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view). The deck follows the same eight steps and uses the participant’s own project. Its tools run in local Python; onboarding calls a local MCP server. Follow the [presenter notes](../decks/pending/notes/facilitator-notes.md) for the three-hour session.

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

Native EvalTables returned HTTP 500 in the technical rehearsal. Use the notebook and Weave comparisons when that status persists, then retry publication without repeating training or model calls.
