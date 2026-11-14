# Solar deck visual upgrade

The deck keeps the current controls, settings, and recorded v0.3.0 experiment. The fictional lab now prepares for a weekly forecast review: identify the code behind a score, compare forecasts, and test an AI research assistant’s proposed edits. This is a presentation change, not another experiment.

| Concept | Slides | Editable source / evidence | Meaning and text alternative |
| --- | --- | --- | --- |
| Forecast window and target | 13, 14 | ForecastWindow.vue; v031-goes-window.png; solar.py:load_goes | Sixty observed samples per channel at t−59…t become an input; XRS-B at t+30 is a separate target. The plotted lines and target are actual first accepted training observations. |
| Splits, missing observations, normalization | 15, 16, 17 | SolarComputation.vue:normalization; SolarDataRules.vue:gaps; solar.py:load_goes/partition | Fit a mean and standard deviation per input channel using training data. Reuse them for all splits. Targets and persistence stay in log-flux units. Gaps anywhere through the target or a crossed date split reject a window. |
| Persistence and its error | 20, 21 | SolarComputation.vue:error; solar.py:errors; solar_teaching.py:PERSISTENCE_SOLUTION | The latest log-flux observation becomes the prediction. A clearly labeled arithmetic example takes absolute per-case differences before averaging; these numbers are not rehearsal results. |
| MLP and temporal CNN computation | 35, 36 | SolarComputation.vue:mlp/cnn; examples/solar/candidate.py:build_model | MLP flattens 2×60 into 120 features. CNN uses 5-sample filters with padding 2, then averages its 60 positions. Both return one scalar. Channel/time shapes, not neuron counts drawn, are exact. |
| Training, configuration, and saved results | 26, 27, 28, 29, 30, 31, 32 | ResearchMap.vue; SolarComputation.vue:records/training/checkpoint; scripts/solar_cells.py:run_training; session.py | Training targets enter the loss and Adam updates forecast weights. Future targets enter the fixed scorer separately from model inputs. One saved execution links source/config/data, learned weights, outputs, metrics, and its trace. Checkpoint restore reuses verified completed work. |
| Search versus new implementations | 34, 37, 38, 39 | SolarMechanism.vue:search; examples/solar/candidate.py; scripts/solar_cells.py:Sweep | Changing a learning rate changes configuration; choosing MLP/CNN selects implemented code; a proposed loss edit changes source. The native Sweep is actual recorded evidence. |
| Image tensors and residual prediction | 45, 46, 47, 48, 49 | SolarMechanism.vue:residual; v031-residual-correction.png; examples/solar/candidate.py:forward | Two image channels become one forecast. The residual model adds current image to its correction. A saved validation prediction minus its current input supplies the actual correction figure; the correction is not observed solar change. |
| Disk error and training loss | 50, 51, 52 | SolarMechanism.vue:mask; SolarComputation.vue:loss; solar.py:errors | Mask=1 selects disk pixels. Absolute errors are averaged per image and then across images. The labeled one-pixel arithmetic example separates squared training loss from fixed absolute evaluation error. |
| Research model versus trained forecast weights | 56, 96 | SolarMechanism.vue:weights; SolarDataRules.vue:zero-head; saved round-two source | The fixed language model writes Python. The small forecasting model trains weights. The recorded zero-init edit applies only to the final Conv2d weights and bias; it initially produces zero correction, not an all-zero CNN. |
| Agent evidence, reviewed proposals, and adoption | 55, 58, 62, 64, 65, 66, 67, 69 | SolarComputation.vue:evidence; ResearchBranches.vue; SolarDataRules.vue:adoption; scripts/solar_cells.py:choose_adoption | Current source/settings/validation results enter the proposal; final-test records do not. Review gates precede candidate training. Composition reviews results but is separately tested. Strictly lower validation error adopts its code/weights; equal, worse, failed or missing results retain the parent. The lesson and retained code enter round two. |
| Frozen evaluation | 73, 74, 75 | SolarComputation.vue:inference; training.py; worker.py | Source+configuration construct a model and saved weights load into it as separate inputs. Reserved inputs produce predictions under eval/no_grad. Only the scorer receives reserved targets; no fit or optimizer step occurs. |

## Visual conventions

Teal marks the current computation, warm yellow marks a target or explicit decision, and blue/orange distinguish candidates. Colors do not indicate quality. Solid branch connections carry code; dashed connections carry reviewed results. Review is a gate before execution; a decision to retain is distinct from training that version.

SVG components have text alternatives, explicit shapes, and scoped arrow-marker IDs. Schematic examples are labeled. Scientific figures use saved arrays and maintain common scales when comparing forecasts. The new residual correction figure uses a separate signed scale, labeled beside its colorbar. It does not turn the network correction into a measurement of physical change.

The new figures use the same immutable solar-v1 data and rehearsal workspace as the existing figures. `scripts/build-evidence-figures.py` generated them without fitting or inference. `notes/visual-v030-figures.json` records source stage IDs and checksums. Presentation filenames beginning `v031` identify these explanatory figures, not a new research run.

## Inspection and checks

Ten representative diagram/figure frames were rendered in headless Chrome against the local Slidev preview, with no page errors. Full-size review caught and corrected a temporal-filter arrow crossing tensor labels, a misplaced operator in the residual figure, and a GOES annotation touching the axis. Model source and saved weights now enter inference separately. The early training frame uses ordinary squared error; its notes explain that the shared GOES loss mask contains only ones.

Exercise names, controls, source-to-probe matches, retained versions, and numerical results passed the exercise-contract, answer-code, and recorded-evidence checks. All 101 browser slides and PDF pages rendered successfully. Browser checks found no missing images, clipped SVG labels, page errors, or failed asset requests; all eight worked-answer keyboard return paths passed. The PDF contact sheets and representative full-size diagrams were visually reviewed. See `delivery-checks.json` and `pdf-checks.json` for the source hashes and validation records.

The November 14 text review inspected every PDF page through nine contact sheets, then enlarged the revised opening, research-assistant diagram, source capture, and worked answers. It corrected the MLP header touching “Flatten,” candidate headings extending beyond their document boxes, and a worked-answer title that described only the absolute metric while also showing squared training loss. The loss/metric distinction is now printed below the code. The revised scene stays separate from the real observations and recorded results; the final review includes both lower image error and the GOES model’s failure to beat persistence.

## Coordinated notebook inspection

The current notebook adds read-only views backed by its loaded arrays and saved execution files:

- The GOES window viewer shows both input channels and the separate future target. Toggling input normalization preserves target and persistence units.
- An explicit forward-pass check uses the participant’s `build_model` implementation and reports intermediate shapes. It does not call `fit`, create an optimizer, or alter the random state used by later training.
- Public scorer fixtures expose signed errors, included pixels, and per-image averaging. These arithmetic examples are labeled and do not replace solar observations.
- One timestamp aligns persistence, manual, and agent forecasts, with common intensity and error scales. Missing saved predictions remain unavailable. Per-case scores and full-split means appear separately.
- The GOES investigation pairs saved loss history, settings, prediction, and persistence. Final predictions appear only after the frozen evaluation is complete.

`solar_views.py` handles these views; the authored cells keep controls and learner code visible. Existing training outputs and experimental stage identities are unchanged. The recorded notebook callout now links the same v0.3.0 workspace as this deck.

Four code excerpts use native Slidev line highlights. Four actual Forge captures reveal numbered regions for arguments, returned values, validation evidence, and the pixel-wise score. Full-resolution captures remain linked. The interactive branch diagram uses the shared `visuals.json` grammar and actual round-one proposal, probe, composition, and selection records. Its detail panel includes the one-line loss diff and native evidence links; selection remains separate from execution.

Targeted browser inspection covered the code highlights, all annotated captures, and recorded branch selections without page errors. It caught and corrected a score annotation pointing to the adjacent evidence row. Notebook browser review found a reactive feedback loop; the writer now has its own cell and uses functional state updates, with a dependency regression check. Full-deck/PDF validation is performed by the coordinated build.
