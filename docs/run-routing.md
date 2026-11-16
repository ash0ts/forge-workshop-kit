# Run Customer Request Routing

**Five and a half hours · basic Python · classification, review, release, and rollback**

A support team must distinguish a card that has not arrived from one that does not work. Participants train a router on public Banking77 requests, investigate its mistakes, then reproduce the selected model and repair a deliberately faulty release loader.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/routing/) · [Copy notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) · [Full runbook](routing-workshop.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Download the teaching bundle through the notebook and open one validation request. Keep its prediction and the label-order incident available for a recorded demo. Classifier training uses CPU and cached features. The full session remains a technical preview pending attendee access and usability checks.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–1:35 | Predict a request's route, connect and trace, fit TF–IDF, investigate a mistake, then compare frozen embeddings and calculate F1. The first ARIA stop precedes the alternative representation. |
| 1:35–2:10 | Implement the review policy and save four reviewed labels. |
| 2:10–2:20 | Break. |
| 2:20–3:30 | Separate eight prompted routes from judge calibration, then refit using accepted labels. |
| 3:30–3:40 | Break. |
| 3:40–4:00 | Freeze the classifier and review policy; compare the official test requests. |
| 4:00–4:10 | Break. |
| 4:10–5:30 | Reproduce the exact artifact, investigate the controlled label-order defect, repair and check it, release or reject, practice rollback, and publish the checked conclusion. |

Use **Prepare the selected router for release** only after the model comparison. The capstone runs a notebook batch predictor and adds no required model calls or training. Its regression set checks reproduction; it is not another independent test set.

## Give a six-minute demo

Use the [recorded routing walkthrough](current-demo-guide.md#request-routing-in-six-minutes). Follow a request through features, predicted intent, and a reviewed disagreement. For a release discussion, show the healthy, faulty, and repaired label mapping from the [recorded drill](routing-workshop.md#recorded-release-drill).

## If live work stops

Use saved predictions and retry publication separately. Keep unavailable judgments explicit. The repaired loader restores the healthy predictions, including the classifier's remaining mistakes; it does not improve the classifier itself.
