# Solar Autoresearch presenter notes

## 1. Build a research loop.<br>Then give it an agent.

0:00

Opening, 30 seconds. This is the research team at the fictional Pending, Inc. The notebook contains real public solar observations and actual training code. We will first build the experiment, then give a fixed-model agent a limited role in changing it.

## 2. Your team has a promising result.

0:01

Tell the fictional scene briefly. It establishes the familiar problem of a score without the program, data, and settings that produced it. Do not imply this anecdote happened in the rehearsal.

## 3. The Sun has supplied the data.

0:02

Define forecasting before introducing the agent. SunPy gives astronomy-aware tools for acquiring and inspecting observations. This is not flare classification or a reproduction of a foundation-model benchmark.

## 4. Management has another request.

0:03

The joke is the escalation from doing research to automating pieces of research. The answer is a tested workflow, not a promise of better performance. Research-agent weights stay fixed; the small forecasting models are trained.

## 5. What you will build

0:04

Show the work in order. Participants edit visible Python. Every execution is explicit. A higher score is optional; an explainable experiment is the goal.

## 6. Your notebook, in your project

0:05

Use the template, not a facilitator rehearsal notebook. A public project is a teaching default, not an entitlement grant. Do not put private data in it. No host-issued token or gateway URL is required. Run all stale cells initializes the controls. It does not press exercise buttons or start training or paid inference. The first access check is also free.

## 7. The same notebook on your laptop

0:06

Local alternative. Dependencies are locked. Authenticate at the terminal, never in a shared code cell. There is no local workshop service to launch. Notebook CPU compute and direct provider billing belong to the participant. The configured inference allowance defaults to $8 and is adjustable.

## 8. Know what this notebook will run

0:06

The provider records requested and returned model IDs. Research calls use temperature 0.2, JSON output, and a maximum 16,384 output tokens. The model does not silently change when unavailable. Opening, restoring, or editing does not run training or inference.

## 9. The first thing you publish is a trace

0:07

Illustrative excerpt of the pinned Forge SDK scope hierarchy; exact instrument_tool code is in the notebook. Parent conversation and turn scopes are supplied by export_trace, while learners write the tool scope. A successful export call is not the same as verified stored-span readback.

## 10. Connect and find your first span

0:08–0:15

Allow 7 minutes. Help users distinguish project permission errors from inference access. The setup trace is tool-only and makes no provider call.

## 11. Your work stays in your project

0:15

Captured from the revised notebook. Project, tool location, allowance and current progress stay together. The screenshot is a restored rehearsal, not an empty new workspace. Do not ask attendees to enter the facilitator project shown here.

## 12. The trace comes from the code you write

0:15

Actual completed setup editor from the revised-notebook rehearsal. The local check is free and exports nothing. The separate trace button exports an actual operation; stored span 3836f2a676d91bdf contains the attribute. Later training uses the same writer.

## 13. The measurement forecast

0:15

GOES-15 one-minute X-ray measurements. The task is a 60-minute history predicting flux 30 minutes ahead. Explain log scaling without suggesting these models are calibrated operational forecasts.

## 14. Dates are part of the experiment

0:17

The splits are dates, not random neighboring rows. All source observations and the target must fit inside one partition. Otherwise near-duplicate solar states can leak from training into evaluation.

## 15. A missing observation is a gap

0:19

Actual source coverage from dataset manifest. The image archive and GOES have different exclusions. Do not treat a missing measurement as evidence that solar flux reached zero.

## 16. SunPy gives the observations context

0:20

The package is approximately 26.1 MB. Prepared arrays keep downloads small; a representative FITS file retains astronomy metadata. Acquisition code and manifest preserve source URLs, checksums, preprocessing, and exclusions. Credit NOAA, NASA/SDO, AIA, JSOC, and SunPy.

## 17. Inspect the observations before training

0:21–0:27

Use 6 minutes. No model fit belongs in this exercise. The archive was prepared before class, so students inspect versioned data rather than waiting for thousands of downloads.

## 18. The first model predicts no change

0:27

Persistence is meaningful for correlated solar observations. A model must beat this simple prediction before complexity has demonstrated value. Do not claim persistence will win every task.

## 19. A forecast needs a defined error

0:29

Primary measurement metric is log-flux MAE in log10 W/m² units. Don’t average this number with image error. A trend chart and individual errors provide information the mean omits.

## 20. Write and test persistence

0:30–0:40

Allow 10 minutes. Local checks are free. Do not reveal the answer until students have attempted it.

## 21. A score alone cannot reproduce a run

0:40

These are possible causes, not claims about a hidden failure in the rehearsal. Ask what information a teammate needs to rerun a result.

## 22. These scores need their configurations

0:41

Interactive illustration using two actual recorded rehearsal rows. Ask what changed before revealing the active configuration. Both runs use the same source and training budget; learning rate differs. Reproduction also requires data and executed source. No training or inference occurs in this widget.

## 23. The learning rate changed. The budget did not.

0:42

Static reveal for the PDF and the live teaching sequence. The two actual runs share data, source, seed, steps and batch size. At this short budget, the lower error alone does not establish a better converged architecture.

## 24. The program produces the forecast

0:42

First build of the shared research diagram. Forecast model, observation and prediction stay in place throughout the progression.

## 25. The executed code belongs to the record

0:43

Attach exact source. The model and training functions are editable. The stage receipt fingerprints source and settings.

## 26. Keep the measurement fixed

0:44

The primary scorer is supplied by the experiment. Learner metrics are checked against it. A revised metric creates a different question and must not retroactively improve old scores.

## 27. Save the work needed to explain the score

0:45

No generic product pitch. Runs make settings and loss history comparable; artifacts preserve files for restoration and reproduction.

## 28. Visible training, durable saving

0:47

Conceptual public API example. In the actual notebook run_training invokes training.train and saves weights/predictions. A completed receipt must be restored rather than repeating work on refresh.

## 29. A restart should restore, not rerun

0:49

Use the actual restoration behavior. An upload failure should preserve local results and clearly identify what is unpublished. Monitoring is read-only and cannot gate participant progress.

## 30. Make the result reproducible

0:50–1:05

15 minutes. Students should change the metric, then see a local wrong-value check fail and fix it. Do not make this a form-only reflection.

## 31. Settings, architectures, and new code

1:05

This distinction is the spine of the workshop. Searching learning rates is useful, but it is not an agent inventing new code.

## 32. Six controlled starting configurations

1:07

These are the fixed rehearsal settings from the notebook. Short budget is deliberate for class, not a claim of tuning quality. Settings remain editable and must be recorded if changed.

## 33. W&B Sweeps supplies the configurations

1:09

Teaching excerpt, not a standalone complete cell. The actual notebook specifies entity and project on both calls. The sweep and stage journal have different jobs: assignment versus durable execution reuse.

## 34. Compare error, baseline skill, and runtime

1:10

Fresh revised-notebook rehearsal: native Sweep pr1xsoaw. This is a crop of the actual first chart row; the full image preserves the Forge workspace context and ingestion-delay notice. The short training budget produced negative skill versus persistence. The charts retain all six runs; they do not demonstrate an architecture winner.

## 35. A smaller error can still be a poor forecast

1:11

Do not preannounce learners’ results. This is a recorded example and remains labeled. The six short rehearsal models did not justify an architecture claim.

## 36. Run the same search and inspect a loss curve

1:15–1:30

15 minutes. Request a prediction before students click. If provider or publication is unavailable, training can still have saved local results. Do not rerun inference to repair a link.

## 37. The experiments can wait ten minutes.

1:30–1:40

Ten-minute break. No new background experiments are required. Confirm checkpoint status before leaving.

## 38. The target is now a future image

1:40

The image task receives frames at t−60 and t and predicts t+60. The same chronological split rules apply. Larger images are an optional separate compute experiment.

## 39. Reuse the experiment record

1:42

Do not reintroduce every product. Reuse the same record structure to make the new task less cognitively expensive.

## 40. A forecast produces an image you can inspect

1:44

Source evidence/solar-validation.png. Use it to identify which panel is input, prediction, target, error. It is not the participant’s current result.

## 41. Predict the full future image

1:46

Keep technical detail concrete. This is a tiny model for CPU class time, not a solar foundation model.

## 42. Or predict a correction to the present

1:48

The residual path makes persistence accessible when correction is zero. It does not guarantee better forecasting. Participants implement the branch in the actual code editor.

## 43. Score the solar disk

1:50

Pseudocode for disk-masked MAE. The real answer sums axes 1,2,3 per example before averaging. A whole-image average can hide a scientifically important small region.

## 44. Training loss and final metric have different jobs

1:52

Explain why an agent might test L1 without moving the goalposts. Changing training loss is an allowed edit; changing the independent scoring metric is not.

## 45. Compare what each model actually predicts

1:54

Fresh revised-notebook rehearsal. Both rows share the same input and target timestamps. The full capture contains the native notebook score table, saved model predictions, and direct Agent Lens, run and artifact links. This is a validation example; final dates are still reserved.

## 46. Implement and compare the image predictors

1:55–2:15

20 minutes. Learners need an attempt before worked answers. Same data and training budgets apply to both models. Results are selected using validation only.

## 47. Now the agent can edit the program

2:15

Introduce the meta layer only after students have built a working experiment. The agent gets evidence and a constrained edit request. It can be mistaken.

## 48. Two kinds of model, two kinds of change

2:17

Explicitly correct possible carryover from the Harness² agent workshop. There all runtime model weights stayed fixed. Here small forecasting models train normally.

## 49. What the editor can change

2:19

Use accurate isolation language. This workshop runs reviewed Python in a bounded subprocess, not remote Sandbox entitlement. Time limits and no inherited secrets reduce risk but do not turn arbitrary code into secure execution.

## 50. Give the agent the active experiment

2:21

The rehearsal retained an ineffective default-value edit when active configuration was missing. Teach the general mechanism without hiding the qualification history. No final-test scores enter this context.

## 51. Agent Lens records how the edit happened

2:23

Model/tool spans, timestamps, arguments, results and errors must correspond to actual events. Automatic Insights clustering is not required for this small workshop. Deterministic records are not renamed Insights.

## 52. Inspect the evidence the researcher read

2:24

Native Agent Lens capture of the selected read_validation_evidence span 37fa531bfbbebdfb in the revised-notebook rehearsal. Authentication may be required for the conversation link.

## 53. Choose what the research agent may inspect

2:25–2:40

12 minutes. Code selection is the lesson, not copying an event identifier by hand. Use small visible checks for allowed split and supported source.

## 54. Two candidates start from the same parent

2:40

Introduce competing hypotheses. This is a teaching adaptation of Harness² Propose–Probe–Compose (https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335). Upstream task refinement uses execution evidence without ground-truth feedback. Here the agent explicitly receives validation metrics and edits an ML training program. A larger network is not automatically better.

## 55. Review the actual change, then test it

2:41

Actual round-one proposal in the revised browser rehearsal. This frame is cropped to the source diff and explicit review control. The full capture includes the agent-attributed rationale. We have not inferred a performance benefit from that rationale. Only the subsequent probe can measure it.

## 56. Each proposed program must run

2:42

Show exact source fingerprints and receipts. If an attempt fails to train, preserve its failure; don’t coerce a missing score to zero.

## 57. Composition reviews the probes

2:44

Dashed lines mean reviewed evidence. They do not mean both candidates were adopted. This was a major ambiguity in older branch drawings.

## 58. A composition is another proposal until tested

2:46

A combined version can introduce new behavior. Even if both component candidates passed, the composition needs an execution. Retaining the parent preserves the source fingerprint.

## 59. The next round uses the previous result

2:48

Both rounds remain on the solar image task. The selection policy uses validation error. Repeated editing is not proof of recursive performance gains.

## 60. Run round one, one decision at a time

2:50–3:00

Work alongside learners. Review actions are free; testing is explicit. Keep this slide visible during the first half of round one.

## 61. Test the composition, then repeat

3:00–3:15

15 minutes. A valid KEEP outcome completes the exercise. If calls are slow, inspect saved evidence and label replay rather than pretending an edit ran.

## 62. Every branch should explain a decision

3:15

Optional two-minute interactive recap. Keyboard-accessible nodes explain the process. This diagram is an illustration; the notebook branch view opens actual records.

## 63. The search ends before final evaluation

3:17

The final image comparison has three versions on the same later windows. The measurement comparison is separate. The final stage loads weights rather than fitting again.

## 64. Final inference loads the saved weights

3:19

Illustrative inference excerpt. Validate the actual execution uses the frozen model rather than silently retraining. The fixed scorer sees future targets; the candidate program does not during improvement.

## 65. Compare the same forecast windows

3:21

Native EvalTables has returned HTTP500 in the recorded rehearsal. Show the notebook and Weave comparison when unavailable. Never label a fallback W&B Table as native EvalTables.

## 66. Evaluate the frozen versions

3:25–3:45

20 minutes. Score differences are evidence from these dates and this run. Do not count pixels or neighboring timestamps as independent studies.

## 67. Quality, effort, and execution are separate

3:45

A smoother execution may not produce a better forecast. A tiny score change may not justify a large search. Inference and notebook compute billing are separate.

## 68. Your teammate should be able to reopen the result

3:47

Explain the evidence chain in ordinary language. Do not make facilitator monitoring a substitute for storing scientific outputs.

## 69. Publish the result you can defend

3:50–3:58

Eight minutes. Permit a negative finding. If publication fails, save the conclusion and use publication-only retry.

## 70. The agent can propose the next experiment.

3:58–4:00

End on an actionable distinction. The research agent increases how many hypotheses can be proposed. The measurement stack determines whether we learn from them. Don’t promise unlimited autonomous research.

## 71. Reference and worked answers

REFERENCE

All following pages are optional and add no lecture time.

## 72. A tool span records the actual operation

WORKED ANSWER

Excerpt of the actual instrument_tool function. Parent scopes and tool_call_id are shown in the notebook. Compare stored spans with independent events; timestamps must describe the event, not a later export.

## 73. Persistence returns the latest observation

WORKED ANSWER

Worked answer uses public split persistence field. Tests must also reject using the target and preserve input data.

## 74. A constant one-unit error scores one

WORKED ANSWER

Code validated by scripts/check-answers.py. Units are the transformed flux units, not raw W/m².

## 75. A completed search keeps every attempt

WORKED ANSWER

This is an inspection answer, not a promised outcome. W&B sweep assignment and journal execution reuse are separate responsibilities.

## 76. The image scorer ignores off-disk pixels

WORKED ANSWER

Code validated against small deterministic fixtures. Production scorer remains independent.

## 77. A zero correction reproduces persistence

WORKED ANSWER

Excerpt of ImagePredictor in candidate.py. A constant zero correction produces the current image exactly. This tests wiring, not learned forecasting quality.

## 78. Evidence selection excludes final results

WORKED ANSWER

The notebook provides the exact schema and checked implementation. The exercise should show a validation fixture accepted and a test fixture rejected.

## 79. The probe must run the proposed source

WORKED ANSWER

Code excerpt mirrors the visible controller. Compare candidate.py in the saved proposal with candidate.py in the execution receipt. A complete source-bundle fingerprint also includes the metric file. The caller provides validation evidence, not final results.

## 80. The final comparison does not refit

WORKED ANSWER

The frozen inference path calls training.train with supplied weights and no training split. Tests verify the fit function is not invoked.

## 81. Round 1: two changes, two measured outcomes

RECORDED REHEARSAL

Fresh revised-notebook rehearsal. Same date partitions, independent metric, seed and 40-step image training configuration. The composition selected the tested zero-init source without adding an untested loss change. This is one validation experiment, not a treatment estimate. Source: public/recorded-study.json.

## 82. The selected edit starts at persistence

RECORDED REHEARSAL

This is the actual first-round Candidate B edit. The final convolution is zero-initialized only for the residual architecture. Training can then learn a correction. The existing residual forward pass is unchanged. Its observed validation error belongs on the preceding slide; the code alone does not establish a general gain.

## 83. Round 2: KEEP was a real comparison

RECORDED REHEARSAL

Fresh revised-notebook rehearsal. Candidate B explicitly returned KEEP and its source fingerprint matched the parent. Candidate A proposed the loss change on the previously adopted source. The final composition test returned 0.11091556898305115. This small single-seed validation change should not be presented as repeatable evidence.

## 84. Recorded image comparison

RECORDED REHEARSAL

Fresh revised-notebook rehearsal: public/recorded-study.json, images/final-comparison. Agent versus manual is approximately 10.15% relative error reduction, not percentage points of accuracy. The final source contains the zero-init head from round one and absolute loss from round two. Temporal correlation and one seed sharply limit inference.

## 85. Recorded: inspect the matching forecasts

RECORDED REHEARSAL

Actual revised-notebook final comparison. The crop shows matching manual and agent forecast rows. The linked full screen includes the image score table and the separate GOES failure table. This is the notebook comparison, not native EvalTables. Source: evidence/ux-v020-solar-final.png; the underlying saved agent plot is public/images/solar-final.png.

## 86. Recorded: the short measurement models lost

RECORDED REHEARSAL

Fresh revised-notebook rehearsal: public/recorded-study.json, goes/final-comparison and saved predictions. Undertraining is supported by the saved learning curves; do not turn this into a claim that MLP or CNN cannot forecast these observations.

## 87. Open the recorded research conversation

RECORDED REHEARSAL

The direct native conversation is linked from the recorded walkthrough and executed evidence. This slide does not use a loading-placeholder screenshot as proof of a completed trace.

## 88. When a service is unavailable

REFERENCE

The current technical preview has verified W&B and Weave publication but native EvalTables returned HTTP500. Do not imply a retry always succeeds. Never substitute provider models silently.

## 89. Four-hour session

REFERENCE

Facilitator pacing target, not a measured participant completion time. Technical rehearsal training and provider time are separate from human learning and review.

## 90. The workshop lives in your project

REFERENCE

Primary public links. Older Pending releases remain historical; this deck teaches the direct participant-owned Workshop Kit runtime.