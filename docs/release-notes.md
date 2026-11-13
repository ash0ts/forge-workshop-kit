# Forge Workshop Kit 0.2.3 technical preview

The recorded workshops now have focused Forge dashboards and shorter Reports. Each dashboard selects its own rehearsal runs, names the scores and units, and links the result to the trace and saved code. The [demo guide](current-demo-guide.md) gives an eight-minute office walkthrough and a ten-minute research walkthrough. New native product captures in the Solar deck show those same pages.

Solar’s final comparison now gives image and GOES persistence separate labels and links. Previously, one persistence link could replace the other in the notebook’s upload status. A regression check covers both saved comparisons and keeps unavailable uploads distinct.

No experiments were rerun. Data, scores, model settings, inference allowances, prior releases, and existing attendee copies are unchanged. Native EvalTables remains unavailable in the saved rehearsal; the notebook, Weave records, and ordinary W&B Tables provide the comparison. External-attendee and human usability rehearsals remain open requirements.

## 0.2.2

The Solar deck, both notebooks, setup instructions, and presenter notes now explain each exercise in the order you do it: change the code, run it, and examine the result. Instructions name the function and control to use. Forge callouts point to a particular request, prediction, or account change to investigate.

Pending keeps its office setting; Solar keeps its research lab. The recorded image improvement and unsuccessful GOES forecast remain visible, with their limits beside the results. Data, experiment settings, saved outcomes, and inference allowances are unchanged. This revision adds no training or model calls.

The release includes updated notebook templates, the Solar browser deck and PDF, editable source, and facilitator notes. Previous releases and existing attendee copies are preserved. See [release checks](release-checks.md) for publication checks and remaining rehearsal requirements.

## 0.2.1

Pending, Inc. remains an office workshop. Solar now takes place in a computational research lab, with a solar observing screen, experiment records and an agent proposing code changes. The deck and notebook use the same lab setting.

The image experiment demonstrates a recorded improvement on real AIA observations: the adopted model reduced final error from 0.122442 to 0.110011, a 10.2% relative reduction from the manual model. The lesson follows the code edits through validation, frozen weights and matched predictions. It labels these results as a single rehearsal and keeps the unsuccessful GOES comparison visible. Data, scores, model settings and experiment budgets are unchanged.

See the [data and evidence review](solar-evidence.md) for archive provenance and the scope of the measured result. The original office cases remain fictional simulations of billing and account-access work.

No training or inference was added for this presentation revision. The prior release and existing attendee copies remain available. Native EvalTables and attendee-rehearsal limits are recorded in [release checks](release-checks.md).

## 0.2.0

The Solar workshop now has a browser deck and PDF, with incremental diagrams, real experiment screens, exact exercise instructions and optional worked answers. Its visual language follows the Pending, Inc. workshop: cream, teal, IBM Plex and a research team whose paperwork has not kept up with its optimism.

Both notebooks now use the same sequence: write code, check it locally, run explicitly, inspect the result, and follow the evidence into Forge. A numbered navigator shows the current step. Prerequisites link back to the required exercise. Drafts, completed runs, selected versions and evidence links survive reopening.

Pending restores exercises for the invoice tool, tool dispatch, observation handoff, tracing, state scorer, explanation judge and improvement controller. Solar separates measurement and image code, adds bounded starter gaps and local checks, and guides each candidate through review, testing, composition and adoption. The branch view keeps rejected and unchanged versions visible.

Browser rehearsal found and repaired two integration problems that standalone scripts missed: local MCP and Weave evaluation needed an event-loop bridge inside marimo, and native Sweep runs needed separation from checkpoint publication. Saved work is reused after recovery. Export and publication retries do not repeat inference or training.

The notebooks use the participant's own project and account. There is no workshop gateway or host token. The $8 inference allowance remains adjustable, and notebook compute is billed separately. Prior releases and attendee copies are unchanged.

Native EvalTables still returns HTTP 500. Weave and notebook comparisons remain available, with the publication status shown explicitly. External-attendee verification and a human usability rehearsal remain before classroom-ready status. See [release checks](release-checks.md) for current evidence and limits.
