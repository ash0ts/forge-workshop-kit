# Forge Workshop Kit 0.7.0

Routing now continues beyond selecting a classifier. Participants reproduce its exact artifact, investigate a deliberately faulty label mapping, add a regression check, repair the loader, and verify rollback. The additional 90 minutes include a break. The existing test-set comparison stays separate from this development regression drill.

Maintainers have a repository-local workshop skill and shared commands for authoring, checking, rehearsing, building, and publishing. Exercise references connect current action cells to their controls and deck instructions. Rehearsals report their actual coverage; old qualification scripts are not counted as current notebook runs. The decks share one dependency toolchain.

Previous releases and attendee copies remain intact. The default inference allowance stays at $8; the release drill needs no model calls. See [release checks](release-checks.md) for validation and remaining external-account and human-rehearsal requirements.

## 0.5.1

The four workshops now publish native **Evaluation Tables (Preview)** through the pinned W&B SDK’s Weave backend. Each comparison opens in a named Forge workspace with its reference version, matching cases and individual scores. Agent Lens links remain attached to the executions; the evaluation table compares their outputs.

Pending publishes the retry repair and harness comparisons. Routing makes judge alignment and final classifier results available before the concluding Report. Solar publishes actual forecast, target and error images, with measurement forecasts in a separate comparison. Inspection publishes board photographs and defect masks as media cells.

Publication is resumable from saved rows and SDK receipts. A failed upload does not repeat training, inference or judging. Missing judgments remain missing. Current decks include native captures and instructions for reading the reference, inputs, outputs and scores.

This revision reuses saved experiments. Scores, datasets, model settings and participant allowances are unchanged. The separate CES backend still returned HTTP 500 on November 14; the native Weave-backed path is verified. External-account and human usability rehearsals remain separate release requirements. See [evaluation setup](evaluations.md) and [release checks](release-checks.md).

## 0.4.0 technical preview

Pending and Solar now follow the same objects through the code, notebook views, and slides. In Pending, participants inspect a tool call and the account state it changed. In Solar, they select a forecast timestamp and compare the models against the same observation. Next and Back reveal the operation being explained without starting another execution.

The branch views use gray for the parent, blue for Candidate A, and orange for Candidate B. Solid connections show code or execution flow; dashed connections show reviewed evidence. Selection and status are written explicitly. A retained version shows the unchanged code and its reason. Saved decisions, diffs, results, and Forge links appear beside the selected branch.

The office exercise explains when a skill was actually read, gives participants a resettable timeout example, and separates the agent's check from the development scorer, final grader, and explanation judge. The lab exercise adds forecast-window inspection, free model-shape checks, scorer arithmetic, matched image predictions, and a closer look at the unsuccessful GOES run.

Slides reveal code and annotations in steps; the downloadable PDFs retain those steps. Both workshops use the existing November 13 rehearsal. No training, paid inference, model settings, data, or scores changed. Native EvalTables availability and the external-attendee rehearsal remain explicit limits. See [release checks](release-checks.md).

## 0.3.1

The decks now explain the forecasting and account-support tasks before introducing the experiment machinery. Solar opens with the observations, forecast horizons, and baseline comparison. Pending opens with a duplicate charge and a request that succeeds before returning a timeout. Code walkthroughs describe the inputs, changed behavior, and outputs participants should check.

The Solar workshop is titled **Solar forecasting with agent-assisted experiments**. Both notebook introductions, the exercise explanations, and presenter notes use the same framing. This is a copy revision: workflow identities, model settings, data, saved results, and existing attendee copies are unchanged. No training or inference was run.

The decks use the recorded November 13 rehearsals. Native EvalTables availability and external-attendee rehearsal requirements remain as described in the [release checks](release-checks.md).

## 0.2.3

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
