# Visual inspection

A four-hour workshop for a team checking circuit boards. Participants inspect real VisA PCB1 photographs, compare whole-image and patch features, select a threshold, and compare equal-budget review policies. Supplied defect masks help inspect errors; they are not classifier inputs or proof of why a prediction changed.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) · [Workshop and schedule](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/inspection-workshop.md) · [Presenter notes](notes/facilitator-notes.md)

## Edit and check

Edit `scripts/build-storyboard.py` and `scripts/depth_storyboard.py`, then regenerate the slides, presenter notes, and slide map. `InspectionMechanism.vue` follows features, distances, scores, and decisions beside their code. The controls match the [authored notebook cells](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py). Follow the [shared deck instructions](../README.md) to preview, build, and validate.

`data/feature-example.json` retains values derived from frozen public files and their checksums. `scripts/derive-visual-evidence.py` reproduces them without classifier training or paid calls. Schematic arrays and scorer fixtures are labeled separately from saved board predictions.

## Recorded examples

The deck preserves the failed first recipe and the later, labeled teaching retest. Show both a recovered defect and a new miss when explaining the changed representation. On the comparison detail slide, the next click reveals the reference mask; white pixels identify the supplied annotation, not model localization.

Photographs and masks retain VisA attribution. Native Agent Lens and Evaluation Tables Preview captures come from saved executions. The [qualification record](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/inspection-workshop.md#recorded-qualification) and [source notes](notes/sources.md) explain their provenance and limits. Learner edits need their own executions.
