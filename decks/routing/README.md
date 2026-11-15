# Request routing

A five-and-a-half-hour workshop for a banking support team deciding where requests belong. Participants use real Banking77 messages, compare TF–IDF with frozen sentence embeddings, inspect mistakes, review labels, and check an automated reviewer. The final capstone reproduces the selected classifier, repairs a deliberately faulty label mapping, and verifies rollback.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/routing/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) · [Workshop and schedule](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/routing-workshop.md) · [Presenter notes](notes/presenter.md)

## Edit and check

`scripts/build-storyboard.py` generates the slides, presenter notes, and slide map. Use `scripts/depth_storyboard.py` for the worked explanations and `scripts/release_storyboard.py` for the release capstone. Follow the [shared deck instructions](../README.md) to preview, build, and validate.

`RoutingMechanism.vue` explains the feature and decision calculations; `RoutingCase.vue` uses saved review-pool predictions. `ReleaseWalk.vue` shows probability columns and their label mapping. Illustrative probabilities are labeled separately from actual predictions.

`data/feature-example.json` contains values derived from frozen public files and their checksums. `scripts/derive-visual-evidence.py` reproduces these examples without classifier training or paid calls. The slide map connects concepts to notebook functions, controls, evidence, and timing.

## Recorded examples

The frozen-embedding classifier gains 4.0844 macro-F1 percentage points over TF–IDF on the official test set. Participant review and retraining is a separate experiment that can tie or regress. The eight prompted requests are also separate from the full classifier evaluation and judge calibration.

The release drill rotates labels without changing probability columns, then restores the original predictions. It uses development review cases and adds no training or model calls. It does not improve the underlying classifier. [Qualification and release evidence](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/routing-workshop.md) identify the runs and limits. Native captures preserve their source links; [evaluation publication](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/evaluations.md) describes the working comparison path.
