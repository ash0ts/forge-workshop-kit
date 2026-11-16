# Run Circuit-board Inspection

**Four hours · basic Python · image features, thresholds, and review budgets**

A manufacturing team needs to flag defective circuit boards without sending every board for review. Participants compare whole-image and patch features on real VisA PCB1 photographs, inspect missed defects, and reproduce a frozen detector. Supplied masks help examine defects; they are not classifier inputs.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) · [Start notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/inspection.html) · [Full runbook](inspection-workshop.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Load the checksum-verified image and feature bundle through the notebook. Open a board before revealing its mask. The required path runs on CPU with cached features and makes no model API calls. ARIA has a recorded alternative. External-account and participant rehearsals remain open.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–1:12 | Inspect a board, connect and trace, explain the encoder and threshold, train the whole-image baseline, then investigate a validation mistake with ARIA or its recording. |
| 1:12–2:10 | Calculate one patch distance, implement feature assembly, train the alternative, and compare ranking and operating errors. |
| 2:10–2:20 | Break. |
| 2:20–3:20 | Select equal active and random review budgets, train both reviewed classifiers, and freeze a version. |
| 3:20–3:30 | Break. |
| 3:30–4:00 | Compare all 442 test boards, reproduce a prediction, check the conclusion, and publish it. |

Ask participants to explain a score against its model's threshold before comparing averages. Both review methods receive 24 labels. Additional labeled data and the method for selecting that data are different interventions.

## Give a six-minute demo

Follow the [recorded walkthrough](current-demo-guide.md#circuit-board-inspection-in-six-minutes). Show `pcb1-anomaly-048`, which the patch version catches, and `pcb1-anomaly-015`, which it newly misses. Open the aligned images and scores in the saved comparison. Patch-distance images show differences from the reference bank, not a causal explanation of a prediction.

## If live work stops

Use the saved image comparison and retry publication without fitting again. Preserve the first recipe's failed improvement gate. The later gain uses previously inspected test images and is labeled a teaching retest; show its new miss alongside the recovered one.
