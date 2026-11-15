# Find defective parts before they ship

This four-hour workshop puts participants on a fictional circuit-board inspection team. The photos are real VisA PCB1 observations. Participants write feature assembly, threshold selection and review-selection code, then compare the same boards across the resulting classifiers.

Copy the Visual Inspection notebook into a writable Forge project. The core path runs on notebook CPU and makes no inference API calls. Locally, install the `inspection` extra and open `notebooks/visual_inspection.py` with marimo. The project login is yours; no gateway or facilitator credential is involved.

## Data and prediction task

The [VisA authors](https://github.com/amazon-science/spot-diff/tree/2a692ab575001cbde74d402d897a7286086c6199) released 1,104 PCB1 photos: 1,004 normal and 100 anomalous boards. We preserve their `2cls_highshot.csv` supervised test set: 402 normal and 40 anomalous images. Seed 2718 partitions only the official training set into 397 fit, 133 review and 132 validation boards. Validation contains 12 defects. The small number matters when interpreting a threshold chosen to catch 90% of validation defects.

The task is binary defect detection. The supplied masks help participants inspect the mistakes. They never enter feature extraction or fitting. These images cover one board family; this workshop does not qualify an industrial quality-control system.

The downloadable cache contains display photos, masks, whole-image and patch features, four lossless encoder inputs for a recomputation exercise, per-file checksums and the CC BY 4.0 license. It uses fixed ImageNet ResNet-18 weights with SHA256 `f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec`. Images resize to 224 × 224 using PIL bilinear interpolation and ImageNet channel normalization. Layer 2 and 3 features produce a 14 × 14 patch grid, projected to 64 channels with seed 20261114; layer 4 supplies 512 whole-image features. The exact encoder is `inspection_encoder.py`. Recomputing the retained four inputs checks the cache without downloading the entire raw dataset again.

Participants fit a class-balanced logistic classifier. The worked follow-up fixes C=0.03, selected using validation from the predeclared grid {0.03, 0.3, 3}. The patch model appends distance to the closest normal training patch at the same spatial position. A normal training image cannot match itself. The reference bank, standardization, classifier coefficients and operating threshold are saved together.

## Timed facilitation

The deck follows a real board through its feature arrays, a classifier score, an operating decision, and a saved detector. Participants see the array shape and relevant code before each exercise. The longer session adds explanation and practice, with the same dataset and training runs.

| Time | Participants change or investigate | Check before moving on |
|---|---|---|
| 0–27 | Inspect the bundled fitting-board photo before connecting, then add a Forge Tool attribute | Give a pass/review reason, reveal the annotation, and find the actual operation in Agent Lens |
| 27–53 | Inspect training boards, follow the frozen encoder and fit, then explore the threshold fixture | Distinguish a photograph, feature vector, classifier score, and decision |
| 53–72 | Complete `choose_threshold`, train the whole-image baseline, and inspect a validation error | Save a hypothesis before introducing patch features |
| 72–104 | Calculate one actual patch distance and implement `build_features`; optionally verify four cached rows | Explain 512 whole-image values plus 196 patch distances, preserving board order |
| 104–130 | Train the patch alternative with the same settings, then inspect ranking and operating errors | Compare saved models and explain AP, missed defects, and false alarms |
| 130–140 | Break | Both trained versions are saved |
| 140–173 | Implement `choose_review`, compare active and random selections, save an assessment | Both branches select 24 boards before opening labels |
| 173–200 | Train both reviewed classifiers, select a version and freeze the comparison | Keep feature changes, extra labels and review policy distinct |
| 200–210 | Break | Selected source, models and thresholds are saved |
| 210–234 | Evaluate the same 442 boards and inspect improvements and regressions | Read scores against each model’s threshold; use AP for the complete ranking |
| 234–240 | Reload a classifier and publish the conclusion | Reproduce one saved score and name the next validation question |

The interactive threshold and AP illustrations use the notebook’s existing public five-board fixture. They are labeled as practice values, not PCB1 results. The actual recorded comparison and native captures remain separate. No extra training or inference is needed to use the deck controls.

The whole-image baseline works with the starter feature function; its patch branch is intentionally unfinished. Saving that first result completes the baseline step. The comparison checkpoint requires both representations. A learner can add patch behavior without changing the saved baseline’s whole-image inputs or threshold rule. Existing completed runs remain reusable.

The review batch uses the dataset's supplied labels to simulate acquiring annotations. Participants' individual assessments are saved separately. We do not label the whole batch human-reviewed or claim active selection wins because it obtained additional labels. Both selection methods receive exactly 24 labels.

## Recorded qualification

The first recipe failed its primary improvement gate. Whole-image average precision was **0.861762** and the positional-mean patch recipe scored **0.855382**. Its reduced operating errors did not turn that AP loss into a passing result. [Every first-recipe outcome](../evidence/inspection-qualification-v1/results.json), including three fixed active/random review seeds, remains published.

One follow-up replaced distance to an average normal patch with distance to an actual nearest normal training patch. Both representations received the same predeclared regularization grid, selected only by validation AP. They chose C=0.03. The follow-up was frozen before its final comparison and used already-inspected official test images. It is a **teaching retest**, not new held-out research evidence.

| Frozen method | Average precision | Missed defects / 40 | False alarms / 402 |
|---|---:|---:|---:|
| Whole-image | 0.872900 | 4 | 23 |
| Nearest-patch plus whole-image | 0.885742 | 3 | 18 |

The AP gain is **1.284 percentage points** on this test partition. The fixed recipe passed the teaching-retest gate; it does not establish repeatability across new datasets or board families. [All validation settings, both final outcomes and predictions](../evidence/inspection-teaching-retest-v2/results.json) are retained. No further test-driven tuning was performed.

Actual image inspection provides a useful contrast. In `pcb1-anomaly-048`, the mask marks the right-hand header-pin area; the whole-image version missed the case and the patch version flagged it at their respective frozen thresholds. In `pcb1-anomaly-015`, a small solder/header-area annotation was flagged by the whole-image classifier but missed by the patch classifier. The distance maps also respond to background variation. They are not defect segmentation and do not prove why a classifier changed its decision.

Feature extraction took **39.25 seconds** on the preparation Mac using two Torch CPU threads. The bounded follow-up fit/evaluation script took **0.195 seconds** with the cache already loaded and BLAS limited to two threads; file preparation and publication are outside that timer. These are preparation measurements, not promises for every attendee laptop.

## Reproduction and boundaries

```sh
uv run --extra inspection python scripts/prepare_inspection.py
uv run --extra inspection python scripts/qualify_inspection_followup.py
```

The first-recipe source is preserved in its evidence bundle. Its source hash intentionally differs from the current module, which adds the follow-up method. Published data include test images for independent reproduction; notebook controls keep them out of fitting and selection, but a learner can inspect their local files.

Opening a notebook does not train, download weights or publish. An explicit button runs each operation. Saved models contain no Python pickle. Final comparisons reload the frozen model file and feature function. An export retry reuses the saved evaluations. If native EvalTables is unavailable, the notebook and saved Weave comparison remain the result; the publication status must remain visible.

Fresh external-account copying, browser completion and human rehearsal are release acceptance checks. Local numerical qualification does not substitute for them.


The [live publication check](../evidence/inspection-live-v050.json) used the saved worked-answer executions, with no additional inference or classifier fitting. All four W&B image tables and all four Weave evaluation calls were published and read back. The CES EvalTables attempt returned HTTP 500 in that check. The current release publishes these saved results through the native Weave-backed Evaluation Tables Preview instead; see [publication checks](evaluations.md). The [rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-defective-parts-before-they-ship:-5ec44d92--VmlldzoxODMwNzU3Nw==) compares all four frozen versions. Its selected version follows validation, so it need not have the best final-test result.
