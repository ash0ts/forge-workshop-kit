# Visual inspection presenter notes

## 1. Find defective parts<br>before they ship

0:00

The inspection team is fictional. The VisA PCB1 images, masks and recorded comparisons are real. Do not promise that every participant run improves.

## 2. The factory has two ways to waste a good morning

0:02

Ask participants which cost matters in their own work. We will count both errors. The joke does not define the release threshold.

## 3. Start with the boards, not the score

0:04

Ask learners to identify a region they would inspect. Do not infer a defect type without checking the supplied mask. They will reveal masks in the notebook.

## 4. What is in the teaching set?

0:07

Explain the distinction between detecting a defective board and locating its defect. This classifier does the former. A patch-distance heatmap is not a segmentation model.

## 5. Separate the data before choosing a model

0:09

The 132 validation boards contain 12 defects. A threshold targeting 90 percent recall must catch at least 11. Test data is public for reproduction, so this is a teaching boundary rather than a security barrier.

## 6. Connect to your own experiment

0:10

Hosted authentication comes from the copied notebook. A laptop uses uv run wandb login. The core path has no inference calls; notebook compute remains separately billed.

## 7. The trace describes a call that actually ran

0:14

The training receipt is recorded before export. A publication failure does not mean the classifier failed. Retrying publication must not train it again.

## 8. Inspect one board before revealing its label

0:18

This is a participant decision, not a model evaluation. Give people a minute to make their own assessment before discussion.

## 9. Reuse a fixed image encoder

0:24

The ImageNet encoder is fixed. Fitting our logistic classifier changes its weights but not ResNet-18. The small cache can be reused in a CPU notebook.

## 10. Compare each patch with real normal examples

0:30

This is the concrete mechanism we changed after the first recipe failed its AP gate. It is not a universal claim about nearest neighbors.

## 11. Add local information to the classifier

0:35

The learner function is passed into fitting and saved with the freeze. Final evaluation reloads that saved source, not the current draft.

## 12. Check the feature cache without rebuilding everything

0:48

The retained lossless inputs allow exact feature comparison. The prepared full cache took 39.25 seconds on the preparation Mac using two Torch CPU threads. This is not an attendee timing guarantee.

## 13. Train the same classifier on each representation

0:55

Do not describe this as training a vision foundation model. We fit a logistic classifier over fixed encoder outputs. Patch distances add features but do not use pixel masks.

## 14. A detector score still needs an operating rule

1:00

Scores are decision values, not calibrated defect probabilities. The optional review margin is in score units. A valid threshold function does not make the policy safe.

## 15. Implement the validation threshold

1:05

Allow participants to finish the local check before training. The 90 percent requirement constrains recall on validation only, not a guarantee for the final set.

## 16. Keep ranking quality and operating errors separate

1:15

AP summarizes precision over recall levels. Do not compare it to accuracy or confuse a change in review volume with better detection.

## 17. Follow one trained classifier through Forge

1:22

These are actual inspection tasks rather than a generic dashboard tour. If export is unavailable, state that the execution is saved and show the publication retry.

## 18. Read the recorded training call

1:25 · RECORDED

Show the exact method, training count and C arguments. Then match the returned classifier path, saved file hash and validation metrics. The next execution uses the saved model. Native capture uses the rehearsal project; participants open their own links. This is tool-only tracing: there was no model-provider call.

## 19. Take ten minutes

1:30

Return at 1 hour 40. Browsing and reopening do not start training.

## 20. Choose where the review time goes

1:40

The random condition matters because any additional labeled data might help. We cannot credit the selection strategy for the entire gain.

## 21. Save what the reviewer actually decided

1:49

Do not call all 24 labels human-verified because a participant pressed one button. Individual saved assessments and the supplied dataset labels are separate records.

## 22. Train with the additional labels

1:58

A tie or loss is still a usable experiment. Never select the final threshold from the official test labels.

## 23. Choose before opening the final results

2:10

Retaining the starting representation is valid. The final comparison includes all four versions regardless of selection.

## 24. Evaluate the same 442 boards

2:25

This is untouched for an attendee following the path. The recorded follow-up used a previously inspected test set, so its claim is narrower. Native EvalTables availability is verified separately from code correctness.

## 25. The first worked recipe did not pass its gate

2:31 · RECORDED

Preserve the failed result and all active/random review outcomes. This is why we choose the criterion before seeing results.

## 26. The bounded follow-up improved this teaching retest

2:33 · RECORDED

Both methods selected C=.03 from the same grid. No further tuning followed the retest. This result does not establish repeatability on a new product.

## 27. Inspect a corrected miss

2:35 · RECORDED

Point to the missing or damaged header-pin area marked by the dataset. The heatmap also responds to background; do not claim it identifies the causal feature or performs accurate segmentation.

## 28. Inspect a new miss too

2:37 · RECORDED

Show the contrast without hiding the final summary. This is a narrower, more honest explanation than saying patch features found all small defects.

## 29. Reload the version you chose

2:40

Saved artifacts are useful because another person can repeat the prediction without guessing which notebook cell you last ran.

## 30. A tested artifact can become the next release

2:48

This extension needs Registry permissions. The Artifact-based reproduction path remains available without them.

## 31. Write down the decision you would make

2:55

Have participants explain the result to someone else before publishing. A reasonable decision can be to retain the previous detector.

## 32. Worked answer: assemble the local features

OPTIONAL ANSWER

Use the complete notebook answer for the local check. The input has one row per board; axis 1 appends features.

## 33. Worked answer: meet the validation recall target

OPTIONAL ANSWER

The retained cutoff depends on validation examples. It does not guarantee the same recall on final boards.

## 34. Worked answer: choose uncertain cases

OPTIONAL ANSWER

Active selection here is uncertainty sampling. It is one policy to test, not a proven universal choice.