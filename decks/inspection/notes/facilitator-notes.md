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

Ask learners to identify a region they would inspect. Do not infer a defect type without checking the supplied mask. They will reveal masks in the notebook. The same fitting example is bundled in the notebook setup. Ask for a pass/review choice before revealing its annotation; no authentication or download is needed.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 4. Predict a label for the whole board

0:06

Ask participants to choose pass or inspection before advancing. The first figure hides its source label and mask. Identify the photograph as the input and the binary label as the target. A detector flags a board; it does not learn pixel labels here.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 5. Use the mask to investigate the decision

0:08

Now reveal pcb1-anomaly-005 from the fitting partition: source image pcb1/Data/Images/Anomaly/005.JPG, SHA-256 ec34541be729af29a287bde12d4e3955cf3f83c734baea8a9505a7b801ce54e2, VisA CC BY 4.0. Source metadata and bundled image/mask checksums are in decks/inspection/data/feature-example.json. Ask which input would leak the answer if passed to the classifier. The mask is reference evidence for human inspection; neither masks nor test labels enter feature assembly.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 6. What is in the teaching set?

0:10

Explain the distinction between detecting a defective board and locating its defect. This classifier does the former. A patch-distance heatmap is not a segmentation model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 7. Separate the data before choosing a model

0:13

The 132 validation boards contain 12 defects. A threshold targeting 90 percent recall must catch at least 11. Test data is public for reproduction, so this is a teaching boundary rather than a security barrier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 8. Connect to your own experiment

0:17

Hosted authentication comes from the copied notebook. A laptop uses uv run wandb login. The core path has no inference calls; notebook compute remains separately billed.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 9. The trace describes a call that actually ran

0:23

The training receipt is recorded before export. A publication failure does not mean the classifier failed. Retrying publication must not train it again.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 10. Inspect one board before revealing its label

0:27

This is a participant decision, not a model evaluation. Give people a minute to make their own assessment before discussion.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 11. Reuse a fixed image encoder

0:32

The ImageNet encoder is fixed. Fitting our logistic classifier changes its weights but not ResNet-18. The small cache can be reused in a CPU notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 12. Fit a first detector on whole-image features

0:37

Do not describe this as training a vision foundation model. We fit a logistic classifier over fixed encoder outputs. Patch distances add features but do not use pixel masks.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 13. Fit on training boards; measure on validation boards

0:40

Point to the learner build_features argument. The same function must be supplied to fit and score. We fit a small class-balanced logistic classifier, not the ResNet encoder. Saving a completed fit and exporting its trace happen afterward.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 14. A detector score still needs an operating rule

0:44

Scores are decision values, not calibrated defect probabilities. The optional review margin is in score units. A valid threshold function does not make the policy safe.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 15. Require 11 of the 12 validation defects to be caught

0:48

The slider uses the exact existing free fixture. With three fixture defects and recall 2/3 the cutoff is 0.7. For the real validation set, ceil(.9*12)=11. Explain that the chosen cutoff constrains this validation set only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 16. Implement the validation threshold

0:53

Allow participants to finish the local check before training. The 90 percent requirement constrains recall on validation only, not a guarantee for the final set.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 17. Inspect a baseline miss or false alarm

1:05

Choose a saved validation error if available; do not force a failure. If the baseline gets the selected board right, describe what evidence would distinguish the next representation. The displayed score comes from the saved weights and feature source.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.

## 18. Investigate this result

1:04 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 19. Read one claim in the recorded response

1:04 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 20. Open the source and check that claim

1:04 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 21. Keep local information as well as the whole image

1:12

Read the shapes out loud: N boards, 14 rows, 14 columns, 64 feature channels. The overlay shows feature positions schematically, not exact independent image crops. The whole-image representation has 512 values; the grid retains spatial differences.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 22. Compare local features at the same board position

1:16

Use only normal fitting boards as the reference bank. At each spatial position, find the closest actual reference vector after scaling. A normal fitting board cannot match itself. The older mean-patch result is preserved beside the later recorded comparison.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 23. Calculate the distance at one image position

1:22

These values come from the real prepared feature cache, not the five-board threshold fixture. Only fitting boards form the reference bank. The free calculation does not fit a classifier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.

## 24. Append 196 distances to the 512 whole-image values

1:27

Walk the same board through errors, log1p, reshape and concatenate. The output has 708 columns. axis=0 would add observations rather than features and fail the shape/order fixture. log1p compresses large distances; it does not turn them into probabilities.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 25. Add local information to the classifier

1:32

The learner function is passed into fitting and saved with the freeze. Final evaluation reloads that saved source, not the current draft.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 26. Check the feature cache without rebuilding everything

1:41

The retained lossless inputs allow exact feature comparison. The prepared full cache took 39.25 seconds on the preparation Mac using two Torch CPU threads. This is not an attendee timing guarantee.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 27. Test patches against the saved baseline

1:44

The first fit remains valid while learners implement the patch branch. A changed threshold rule or changed whole-image inputs would confound this comparison and is rejected. Previously saved matching runs are reused.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.

## 28. Keep ranking quality and operating errors separate

1:52

AP summarizes precision over recall levels. Do not compare it to accuracy or confuse a change in review volume with better detection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 29. Calculate ranking quality before choosing one cutoff

1:54

Use the five public fixture scores. Defects occur at ranks 2,3,4; precision is 1/2,2/3,3/4 at those recalls. Average precision is their mean, 0.638889. This is an illustrative calculation, not a PCB1 result.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 30. Count operating errors at the chosen cutoff

1:57

At cutoff 0.7, the fixture has one missed defect and one false alarm. Moving the cutoff leaves the score ordering and AP unchanged. A review band sends additional cases to people and should be reported as workload, not detection improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 31. Follow one trained classifier through Forge

1:59

These are actual inspection tasks rather than a generic dashboard tour. If export is unavailable, state that the execution is saved and show the publication retry.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 32. Read the recorded training call

2:02

Show the exact method, training count and C arguments. Then match the returned classifier path, saved file hash and validation metrics. The next execution uses the saved model. Native capture uses the rehearsal project; participants open their own links. This is tool-only tracing: there was no model-provider call.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 33. Match the tool call to the saved validation result

2:06

Return to the code and identify the training arguments corresponding to the capture. The trace is a CPU tool operation, with no LLM provider call. A failed trace upload must not cause another fit. Find C, method, training count and validation counts in your own run.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 34. Take ten minutes. Return at 2:20.

2:10

Break from elapsed 2:10 to 2:20. Confirm both models are saved. After the break we choose where to spend 24 additional labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 35. Choose uncertain boards before opening their labels

2:20

Predict which scores the selector will choose. The public fixture uses row IDs 10,20,30,40 with scores .8,-.1,.01,-.9. At threshold 0, the two closest rows are 20 and 30. The function receives no labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 36. Give random selection the same labeling budget

2:26

Both branches start from the same nearest-patch parent and review pool. Each gets 24 labels; overlapping selections are allowed across methods. Random selection controls for simply receiving more data. Do not promise that uncertainty sampling wins.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 37. Choose where the review time goes

2:31

The random condition matters because any additional labeled data might help. We cannot credit the selection strategy for the entire gain.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 38. Save what the reviewer actually decided

2:42

Do not call all 24 labels human-verified because a participant pressed one button. Individual saved assessments and the supplied dataset labels are separate records.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 39. Train with the additional labels

2:53

A tie or loss is still a usable experiment. Never select the final threshold from the official test labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 40. Choose before opening the final results

3:08

Retaining the starting representation is valid. The final comparison includes all four versions regardless of selection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 41. Freeze the preprocessing and reference bank too

3:14

Name the pieces needed to reproduce a score: reference bank, scaling, participant feature code, coefficients and threshold. Selecting the version uses validation. The final comparison still includes all four frozen versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 42. Take ten minutes. Return at 3:30.

3:20

Break from elapsed 3:20 to 3:30. No training runs during the break. On return, evaluate the saved versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.

## 43. Evaluate the same 442 boards

3:30

This is untouched for an attendee following the path. The recorded follow-up used a previously inspected test set, so its claim is narrower. Use Compare in EvalTables after publication. The native Weave-backed Preview and the separate CES v2 service have independent publication statuses.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 44. Compare four detectors on the same boards

3:39

Click Publish saved comparisons to Forge, then Compare in EvalTables. The native Weave-backed Evaluation Tables Preview sits in the W&B workspace. These panels show per-case correctness and error, not average precision. The notebook computes average precision from the complete ranking. Scores and typed images come from the saved final evaluation; this action does not fit another classifier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 45. Inspect the board behind a prediction

3:42

Click once to reveal the reference defect mask for the same board. White pixels are supplied annotations, not model localization. Do not claim a patch heatmap is a causal explanation or segmentation model. Masks are used for inspection, not classifier inputs. Average precision ranks all boards; one row explains a particular operating decision. The separate CES v2 API remains unavailable; this is the working native Preview.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 46. The first worked recipe did not pass its gate

3:45

Preserve the failed result and all active/random review outcomes. This is why we choose the criterion before seeing results.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 47. The bounded follow-up improved this teaching retest

3:47

Both methods selected C=.03 from the same grid. No further tuning followed the retest. This result does not establish repeatability on a new product.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 48. Inspect a corrected miss

3:49

Point to the missing or damaged header-pin area marked by the dataset. The heatmap also responds to background; do not claim it identifies the causal feature or performs accurate segmentation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 49. Inspect a new miss too

3:49

Show the contrast without hiding the final summary. This is a narrower, more honest explanation than saying patch features found all small defects.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 50. Check our conclusion

3:50 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 51. Read one claim in the recorded response

3:50 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 52. Open the source and check that claim

3:50 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 53. Reload the version you chose

3:57

Saved artifacts are useful because another person can repeat the prediction without guessing which notebook cell you last ran.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 54. Reproduce one score from the saved detector

3:58

The reload operation uses the frozen feature source rather than the current editor draft. Compare its output with the previously saved score for the same case. An artifact makes that complete version addressable; Registry is an optional release extension.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 55. A tested artifact can become the next release

3:58

This extension needs Registry permissions. The Artifact-based reproduction path remains available without them.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 56. Write down the decision you would make

3:59

Have participants explain the result to someone else before publishing. A reasonable decision can be to retain the previous detector.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 57. Worked answer: assemble the local features

Optional answer

The complete function signature is in the notebook. This body includes the historical mean-patch branch required by the free fixture. Each row remains one board; concatenation extends its feature columns.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 58. Worked answer: meet the validation recall target

Optional answer

The retained cutoff depends on validation examples. It does not guarantee the same recall on final boards.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.

## 59. Worked answer: choose uncertain cases

Optional answer

Active selection here is uncertainty sampling. It is one policy to test, not a proven universal choice.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.