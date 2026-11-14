# Visual inspection presenter notes

## 1. Find defective parts<br>before they ship

0:00

The inspection team is fictional. The VisA PCB1 images, masks and recorded comparisons are real. Do not promise that every participant run improves.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 2. The factory has two ways to waste a good morning

0:02

Ask participants which cost matters in their own work. We will count both errors. The joke does not define the release threshold.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 3. Start with the boards, not the score

0:04

Ask learners to identify a region they would inspect. Do not infer a defect type without checking the supplied mask. They will reveal masks in the notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 4. What is in the teaching set?

0:08

Explain the distinction between detecting a defective board and locating its defect. This classifier does the former. A patch-distance heatmap is not a segmentation model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 5. Separate the data before choosing a model

0:11

The 132 validation boards contain 12 defects. A threshold targeting 90 percent recall must catch at least 11. Test data is public for reproduction, so this is a teaching boundary rather than a security barrier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 6. Connect to your own experiment

0:16

Hosted authentication comes from the copied notebook. A laptop uses uv run wandb login. The core path has no inference calls; notebook compute remains separately billed.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 7. The trace describes a call that actually ran

0:23

The training receipt is recorded before export. A publication failure does not mean the classifier failed. Retrying publication must not train it again.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 8. Inspect one board before revealing its label

0:27

This is a participant decision, not a model evaluation. Give people a minute to make their own assessment before discussion.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 9. Predict a label for the whole board

0:32

After participants inspect a training photo, identify the input photograph and the binary target separately. A detector flags a board. The supplied mask marks pixels, but this model does not learn pixel labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 10. Use the mask to investigate the decision

0:34

Ask which input would leak the answer if passed to the classifier. The mask is reference evidence for human inspection; neither masks nor test labels enter feature assembly.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 11. Reuse a fixed image encoder

0:37

The ImageNet encoder is fixed. Fitting our logistic classifier changes its weights but not ResNet-18. The small cache can be reused in a CPU notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 12. Keep local information as well as the whole image

0:41

Read the shapes out loud: N boards, 14 rows, 14 columns, 64 feature channels. The overlay shows feature positions schematically, not exact independent image crops. The whole-image representation has 512 values; the grid retains spatial differences.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 13. Compare local features at the same board position

0:47

Use only normal fitting boards as the reference bank. At each spatial position, find the closest actual reference vector after scaling. A normal fitting board cannot match itself. The older mean-patch result is preserved beside the later recorded comparison.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 14. Append 196 distances to the 512 whole-image values

0:53

Walk the same board through errors, log1p, reshape and concatenate. The output has 708 columns. axis=0 would add observations rather than features and fail the shape/order fixture. log1p compresses large distances; it does not turn them into probabilities.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 15. Add local information to the classifier

0:59

The learner function is passed into fitting and saved with the freeze. Final evaluation reloads that saved source, not the current draft.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 16. Check the feature cache without rebuilding everything

1:14

The retained lossless inputs allow exact feature comparison. The prepared full cache took 39.25 seconds on the preparation Mac using two Torch CPU threads. This is not an attendee timing guarantee.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 17. Train the same classifier on each representation

1:19

Do not describe this as training a vision foundation model. We fit a logistic classifier over fixed encoder outputs. Patch distances add features but do not use pixel masks.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 18. Fit on training boards; measure on validation boards

1:22

Point to the learner build_features argument. The same function must be supplied to fit and score. We fit a small class-balanced logistic classifier, not the ResNet encoder. Saving a completed fit and exporting its trace happen afterward.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 19. A detector score still needs an operating rule

1:26

Scores are decision values, not calibrated defect probabilities. The optional review margin is in score units. A valid threshold function does not make the policy safe.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 20. Require 11 of the 12 validation defects to be caught

1:32

The slider uses the exact existing free fixture. With three fixture defects and recall 2/3 the cutoff is 0.7. For the real validation set, ceil(.9*12)=11. Explain that the chosen cutoff constrains this validation set only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 21. Implement the validation threshold

1:38

Allow participants to finish the local check before training. The 90 percent requirement constrains recall on validation only, not a guarantee for the final set.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 22. Keep ranking quality and operating errors separate

1:52

AP summarizes precision over recall levels. Do not compare it to accuracy or confuse a change in review volume with better detection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 23. Calculate ranking quality before choosing one cutoff

1:54

Use the five public fixture scores. Defects occur at ranks 2,3,4; precision is 1/2,2/3,3/4 at those recalls. Average precision is their mean, 0.638889. This is an illustrative calculation, not a PCB1 result.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 24. Count operating errors at the chosen cutoff

1:57

At cutoff 0.7, the fixture has one missed defect and one false alarm. Moving the cutoff leaves the score ordering and AP unchanged. A review band sends additional cases to people and should be reported as workload, not detection improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 25. Follow one trained classifier through Forge

1:59

These are actual inspection tasks rather than a generic dashboard tour. If export is unavailable, state that the execution is saved and show the publication retry.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 26. Read the recorded training call

2:02

Show the exact method, training count and C arguments. Then match the returned classifier path, saved file hash and validation metrics. The next execution uses the saved model. Native capture uses the rehearsal project; participants open their own links. This is tool-only tracing: there was no model-provider call.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 27. Match the tool call to the saved validation result

2:06

Return to the code and identify the training arguments corresponding to the capture. The trace is a CPU tool operation, with no LLM provider call. A failed trace upload must not cause another fit. Find C, method, training count and validation counts in your own run.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 28. Take ten minutes. Return at 2:20.

2:10

Break from elapsed 2:10 to 2:20. Confirm both models are saved. After the break we choose where to spend 24 additional labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 29. Choose uncertain boards before opening their labels

2:20

Predict which scores the selector will choose. The public fixture uses row IDs 10,20,30,40 with scores .8,-.1,.01,-.9. At threshold 0, the two closest rows are 20 and 30. The function receives no labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 30. Give random selection the same labeling budget

2:26

Both branches start from the same nearest-patch parent and review pool. Each gets 24 labels; overlapping selections are allowed across methods. Random selection controls for simply receiving more data. Do not promise that uncertainty sampling wins.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 31. Choose where the review time goes

2:31

The random condition matters because any additional labeled data might help. We cannot credit the selection strategy for the entire gain.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 32. Save what the reviewer actually decided

2:42

Do not call all 24 labels human-verified because a participant pressed one button. Individual saved assessments and the supplied dataset labels are separate records.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 33. Train with the additional labels

2:53

A tie or loss is still a usable experiment. Never select the final threshold from the official test labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 34. Choose before opening the final results

3:08

Retaining the starting representation is valid. The final comparison includes all four versions regardless of selection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 35. Freeze the preprocessing and reference bank too

3:14

Name the pieces needed to reproduce a score: reference bank, scaling, participant feature code, coefficients and threshold. Selecting the version uses validation. The final comparison still includes all four frozen versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 36. Take ten minutes. Return at 3:30.

3:20

Break from elapsed 3:20 to 3:30. No training runs during the break. On return, evaluate the saved versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.

## 37. Evaluate the same 442 boards

3:30

This is untouched for an attendee following the path. The recorded follow-up used a previously inspected test set, so its claim is narrower. Use Compare in EvalTables after publication. The native Weave-backed Preview and the separate CES v2 service have independent publication statuses.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 38. Compare four detectors on the same boards

3:39

Click Publish saved comparisons to Forge, then Compare in EvalTables. The native Weave-backed Evaluation Tables Preview sits in the W&B workspace. These panels show per-case correctness and error, not average precision. The notebook computes average precision from the complete ranking. Scores and typed images come from the saved final evaluation; this action does not fit another classifier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 39. Inspect the board behind a prediction

3:42

Click once to reveal the reference defect mask for the same board. White pixels are supplied annotations, not model localization. Do not claim a patch heatmap is a causal explanation or segmentation model. Masks are used for inspection, not classifier inputs. Average precision ranks all boards; one row explains a particular operating decision. The separate CES v2 API remains unavailable; this is the working native Preview.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 40. The first worked recipe did not pass its gate

3:45

Preserve the failed result and all active/random review outcomes. This is why we choose the criterion before seeing results.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 41. The bounded follow-up improved this teaching retest

3:47

Both methods selected C=.03 from the same grid. No further tuning followed the retest. This result does not establish repeatability on a new product.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 42. Inspect a corrected miss

3:49

Point to the missing or damaged header-pin area marked by the dataset. The heatmap also responds to background; do not claim it identifies the causal feature or performs accurate segmentation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 43. Inspect a new miss too

3:51

Show the contrast without hiding the final summary. This is a narrower, more honest explanation than saying patch features found all small defects.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 44. Reload the version you chose

3:54

Saved artifacts are useful because another person can repeat the prediction without guessing which notebook cell you last ran.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 45. Reproduce one score from the saved detector

3:56

The reload operation uses the frozen feature source rather than the current editor draft. Compare its output with the previously saved score for the same case. An artifact makes that complete version addressable; Registry is an optional release extension.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 46. A tested artifact can become the next release

3:57

This extension needs Registry permissions. The Artifact-based reproduction path remains available without them.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 47. Write down the decision you would make

3:59

Have participants explain the result to someone else before publishing. A reasonable decision can be to retain the previous detector.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 48. Worked answer: assemble the local features

Optional answer

The complete function signature is in the notebook. This body includes the historical mean-patch branch required by the free fixture. Each row remains one board; concatenation extends its feature columns.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 49. Worked answer: meet the validation recall target

Optional answer

The retained cutoff depends on validation examples. It does not guarantee the same recall on final boards.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 50. Worked answer: choose uncertain cases

Optional answer

Active selection here is uncertainty sampling. It is one policy to test, not a proven universal choice.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.