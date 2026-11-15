## 1. Route customer requests and learn from mistakes

0:00

The support team is fictional. The messages are public Banking77 data. We will make a genuine measured classifier comparison, then let participants run an open-ended data review experiment. Do not promise that every personal review will improve the score.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 2. The support queue needs a destination

0:02

Ask people what team should handle each request. These short examples explain the target before the model appears. We classify intent; we are not resolving accounts or giving financial advice. Source: PolyAI-LDN/task-specific-datasets.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 3. A manager has offered to automate forwarding

0:04

This is fictional dialogue. The engineering problem is a constrained label choice. A wrong label wastes time even if the message is polite and the JSON validates. Keep the humor in the manager line, and the task literal.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 4. Read a request before revealing its label

0:06

Allow five minutes for individual predictions and partner discussion. The download includes 20 MB of cached features, original CSVs, license, and checksum manifest. Data loading sends no model call. Inspect the bundled development request in setup before authenticating. Guess its intent, then reveal the published annotation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 5. The dataset contains 77 banking intents

0:09

The data are public queries, not attendee customer records. There are 77 classes. The official test set contains 40 examples per class. One low-resource training class has only 35 examples, which is why we reserve ten validation and ten review cases per class rather than twenty each.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 6. Give each partition one job

0:12

The split order was fixed before any model score. Ten examples of every intent go to validation and ten to the review pool. The test partition is only opened after selection freezes. Files are public for teaching; the code keeps final cases out of model-editing and labeling prompts.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 7. Open your copy and add your first trace

0:16

Let everyone open their own project. Hosted authentication is inherited; there is no shared gateway or host token. The $8 adjustable allowance covers fixed-model inference; CPU notebook charges are separate.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 8. The span should explain the operation

0:23

The notebook captures an independent event receipt and uses this participant-written function to export it. We compare stored spans with the receipt. A publication failure does not mean the operation failed or should be repeated.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 9. Start with a word-based classifier

0:30

Explain unigrams and bigrams with card and my card. Fit the vectorizer only on training messages so validation vocabulary does not alter the feature space. This is a standard, inexpensive baseline, not a deliberately broken model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 10. Measure the words and phrases in one request

0:35

Read the real review-pool message aloud. The default tokenizer produces my, card, isn, here, yet; single-letter t is omitted. The nine nonzero TF–IDF weights are recalculated from the frozen 8,463 training messages and shown against the actual 21,527-column vocabulary. IDF and the vocabulary use training text only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 11. Implement the classifier head

0:40

The participant function is used in both actual fits. CPU training is bounded by iterations and two numerical-library threads. In preparation each fit took under four seconds with cached features; participant machines and hosting differ. Use the four-point practice fit to distinguish creating an estimator from fitting it. Practice points are illustrative and are not Banking77 embeddings.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 12. Read one prediction before comparing models

0:51

Keep the baseline result on screen before discussing embeddings or aggregate gains. Opening another case only reads saved predictions. Ask participants for a testable representation hypothesis, not a claim that every mistake will disappear.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/routing_cells.py.

## 13. Then change the representation

0:56

Contrast sentence representation with lexical overlap. The cached encoder features are versioned and can be regenerated by the supplied preparation code. Cache lookup timing is not end-to-end encoder latency. The comparison changes representation, not data quantity or test cases.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 14. Keep one vector for each request

0:59

Compare the unchanged message with the different representation. Explain 384 as the encoder output size, not a count of hand-chosen keywords. The heatmap shows all 384 actual cached coordinates in index order. Color is signed magnitude, not semantic location. Encoder weights stay frozen.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 15. Construct the estimator before fitting it

1:02

Point to make_classifier: it returns an unfitted estimator. C is inverse regularization strength; changing it changes the training objective, not the number of output intents. max_iter limits optimization. Use the fixed recipe in the required path.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 16. Fit the head on the labeled training rows

1:04

The learner factory supplies the estimator in both branches. TF–IDF fits a vectorizer and head; the embedding branch fits the head on cached features. Both see the same 8,463 labels. The sparse vocabulary width and 384 embedding values are different input spaces.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 17. A fitted classifier returns 77 probabilities

1:07

After the exercise, locate predict_proba and classes_. Array position alone is not an intent label; the class order maps columns to names. Ask which files would be needed to predict after restarting.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 18. Test the sentence-feature alternative

1:10

The encoder is frozen and its cached vectors are versioned. This button completes the existing two-run comparison; it adds no third fit. Previously completed workspaces reuse their saved runs.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/routing_cells.py.

## 19. Macro-F1 gives each intent equal weight

1:16

Do not average row-wise F1 values. Macro-F1 is computed from the whole matched prediction set. Accuracy is also reported. Neither metric tells the whole operational story because review can defer some cases.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 20. Count the errors for one intent

1:18

These are the recorded embedding model’s official-test card_arrival predictions: 34 true positives, 3 false positives, 6 false negatives. Trace a misroute to the appropriate count. This example explains the metric; do not select a new model using these final examples.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 21. Calculate F1, then average across intents

1:21

Compute precision 34/37 and recall 34/40. F1 is 68/77=0.883117 for this intent. The bars show all 77 saved intent F1s; their mean is the existing 0.920229 result. A per-case correct flag is a different measurement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 22. The worked comparison reduced routing mistakes

1:26

The fixed contract preceded final evaluation. Publish all six outcomes. Participants will inspect their own validation results first; the recorded result is a worked comparison and cannot be attributed to unexecuted learner edits. The deterministic seed repetitions check reproduction rather than uncertainty.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 23. A router can also ask a person

1:35

Ask what happens if every request is deferred. Coverage becomes zero, selective accuracy is unavailable, and full classifier quality remains unchanged. The model probabilities are not calibrated guarantees.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 24. Move the threshold without retraining

1:38

Use the keyboard on the slider. The request and classifier probabilities stay unchanged. Coverage and selective accuracy recompute from the 770 saved validation predictions. At zero accepted cases, show unavailable rather than claiming perfect accuracy.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 25. Choose labeling candidates by their top-two margin

1:42

The displayed review-pool request has confidence 0.508052 and margin 0.180419. Confidence controls automatic deferral; margin ranks which examples to ask someone to label. These are distinct rules in predict and select_review.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 26. Write the rule that sends a request to review

1:45

The function changes the displayed policy and the policy frozen for final evaluation. Its local check is free. Let people observe the coverage tradeoff rather than supply a preferred threshold.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 27. Read the disagreement before declaring failure

1:52

These four examples are actual outputs from the training-derived review pool. The published annotation is a reference, not proof that every message is unambiguous. The first two were selected as disagreements with the dataset annotation; the last two agree with it. They are not human review records. Let learners explain disagreement in their own words.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 28. Save labels someone can trace back to a decision

2:00

Show the provenance fields in the dataset artifact. Accepted human labels alone can extend training. Teacher suggestions and published-reference replay remain distinct. Encourage a discussion when participants disagree with the benchmark annotation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 29. Keep the proposal and accepted label separate

2:06

Ask the participant to find all three labels for a case: model proposal, dataset reference, personal accepted label. Do not overwrite the proposal when accepting a correction. The record must preserve who made the decision and which data it belongs to.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 30. Take ten minutes. Return at 2:20.

2:10

Break from elapsed 2:10 to 2:20. Confirm the reviews and trained versions are saved. Reopening does not train or call a model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 31. A prompted model returns a typed decision

2:20

Run only eight preselected development requests. This sample teaches model behavior and trace inspection; it is too small to rank against classifiers evaluated on 3,080 final cases. The provider is fixed and charged to the participant allowance.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 32. The judge reviews a route in a separate call

2:25

The first lane routes eight fixed validation requests. The second judges classifier proposals attached to human reviews. The judge does not consume the eight prompted routes. Both use actual provider calls and native spans; neither sample ranks models on the complete final dataset.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 33. Inspect eight actual model routes

2:31

Every request is durable and bounded. Each case gets a separate stage, so completed siblings can be reused after a failure. No test examples or accepted review labels enter the routing prompt.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 34. Check the model-based judge against your reviews

2:40

The notebook uses a model-based judge exercise. It is not silently creating native Agent Lens tags or pretending to generate Insights. Native tag alignment is an optional access-qualified extension. Prepared Insights require an independently verified cohort, not waiting live for new clusters.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 35. Keep the accepted label out of the judge prompt

2:44

Show the user message fields in the actual notebook. The accepted label is used afterward to calculate human failure labels, not supplied to the judge. Contrast a malformed response, a valid disagreement and an unavailable request. This exercise is not an automatic native Insights cluster or tag.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 36. Implement the judge response check

2:50

The human accepted intent stays out of the judge prompt. The judge receives the request and proposed route. Check one reason, even if the JSON passes. Missing judgments stay missing; do not score them as correct or incorrect.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 37. The judge disagreed with the dataset label

3:03

The screenshot is an authenticated native capture. Its JSON pane clips the end of the reason; the caption quotes the full saved response. Both the request and failed:false are visible. Twelve development-only requests completed, their stored spans were verified, and observed inference cost was $0.00113494. Eight routing requests were an instrumentation sample, not a quality benchmark. Human review is still necessary.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 38. Use reviewed data to run a new experiment

3:10

The request review changes training data. It does not alter the encoder or hide difficult test examples. A review can be wrong, redundant, or too small to matter. Live improvement is measured, not scripted.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 39. Refit the head with your accepted labels

3:14

Only unique review-pool cases with label_source=human_review and verified=true may extend training. The fixed encoder and original training rows stay. Extra labels can be useful, redundant or wrong; compare validation before selecting a version.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 40. Train with your accepted labels

3:18

This is the honest live experiment after the qualified representation improvement. Do not replace its result with the recorded gain. If labels disagree with the published annotation, inspect the text and the choice before attributing a score change to better data.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 41. Take ten minutes. Return at 3:40.

3:30

Break from elapsed 3:30 to 3:40. Keep the final test closed. On return, freeze the version and policy you chose from validation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/routing_cells.py.

## 42. Freeze what the final comparison will use

3:40

The notebook records the selected training stage and model checksum. A policy is part of the release decision and must be fixed before seeing the final requests. After final evaluation, another choice is a separately labeled teaching retest.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 43. Save the transformations with the weights

3:42

Have someone name the missing component if only coefficients are saved. TF–IDF needs its fitted vectorizer; the embedding model needs the encoder identity and preprocessing. The review policy also changes what users see.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 44. Evaluate all matching test requests

3:45

All final predictions are retained. The selected model may equal the existing embedding model; that is a valid keep decision, not an invented third improvement. Keep classifier quality separate from deferral policy.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 45. Compare matching requests, then the operating policy

3:48

First compare intent predictions across versions on all 3,080 requests. Then compare how many were automatically routed under the chosen policy. A selected version may be the same saved embedding model. Reusing it is a keep decision, not another improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 46. Compare the same requests in Forge

3:50

Final evaluation publishes saved classifier predictions before the Report chapter. Click Compare in EvalTables. This is the native Weave-backed Evaluation Tables Preview in the W&B workspace. Aggregate macro-F1 remains computed from the whole prediction set; it is not the mean of row F1 scores.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 47. Read one routing decision

3:52

Use the saved case ID to match outputs. The automated judge comparison is separate and uses participant-reviewed development cases. Its target is agreement with those reviews, not classification accuracy on the official test set. The separate CES v2 service can remain unavailable while this Preview works.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 48. Take ten minutes. Return at 4:05.

3:55

Break from 3:55 to 4:05. Existing official-test results are complete; do not tune against them during the release lab.

## 49. The classifier works. Can another process use it?

4:05

The scenario changes from model selection to delivery. The model weights stay fixed. Participants will see how an integration defect can invalidate an otherwise useful model. Explain the fault in advance; do not stage it as an organic discovery.

## 50. Save what the predictor needs, then reload it

4:08

The artifact contains classifier, feature representation identity, intent order, review policy, source, checks, and fixed case IDs. The source sequence is abbreviated. An exact artifact version permits reproduction; a mutable latest alias does not identify what ran. Never unpickle arbitrary downloaded models; use the artifact just created in the participant project.

## 51. Load your selected version from its artifact

4:11

Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.

## 52. Choose the regression cases before predicting

4:17

The cohort is selected and saved before predictions, using the lexical first review-pool case per intent. Some reviewed cases may have been accepted into training. This batch tests release behavior, not generalization. The original 3,080 official test predictions remain unchanged.

## 53. A probability belongs to a specific intent

4:20

Illustrative three-column values; the real model has 77 intent columns. Trace column 1 from 0.84 to card_not_working using model.classes_. The message and probabilities are explanatory, not a recorded participant output.

## 54. Rotated labels send column 1 to another queue

4:22

The deliberately faulty loader rotates the names by one position. Column1 still contains 0.84 but now names cash_withdrawal_not_recognised. Valid output and high confidence do not establish a correct destination. Participants inspect actual 77-class predictions in the next exercise.

## 55. Find one request sent to the wrong queue

4:26

Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.

## 56. Checking the label set misses this defect

4:33

All expected names are still present. A set comparison discards order, precisely the part that links probability columns to intents. Ask learners which extra check would detect the fault.

## 57. Check order before accepting the loaded model

4:35

Implement both exact order and set checks. Do not sort labels as the repair: a classifier may use another class order. The free fixture intentionally uses a nonalphabetical order.

## 58. Repair the loader and write its regression check

4:40

Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.

## 59. A repaired loader should reproduce the intact release

4:50

Compare the healthy, faulty and repaired outputs by case ID. Parity with the intact release establishes recovery from this drill. Macro-F1 still measures agreement with labels. A model can reproduce its own mistakes perfectly. Keep those two claims separate.

## 60. Compare three versions of the same request

4:56

This is an investigation guide rather than a product screenshot. Use native links from the release result. If publication is unavailable, inspect the notebook comparison and retry publication only. Do not rerun the batch to fix an export error.

## 61. Decide whether this release passes its checks

5:00

Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.

## 62. Rollback reloads a version; it does not undo training

5:08

Reload the exact previous artifact, then check the same fixed case IDs. No fit or model request is required. Keep the faulty version for diagnosis. Registry can organize selected artifacts but does not deploy this Python predictor.

## 63. Restore the previous version and verify it

5:12

Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.

## 64. Separate the model gain from the release repair

5:20

Have participants explain both results without merging denominators or calling the drill a new benchmark. Preserve original 3,080-test predictions; the 77-case capstone cohort is reused and may overlap reviewed training additions. Keep remaining genuine classifier errors in the conclusion.

## 65. Write the decision you would make

5:25

Final five minutes: explain the classifier comparison and the release drill separately. Include the tested artifact, decision, rollback evidence, and remaining errors. Publication reuses saved work.

## 66. Optional: organize approved versions in Registry

5:28

Registry manages versions, not automatic deployment. ARIA access and usage are separate; it cannot approve a repair automatically. The core capstone contains no new inference calls or training. Specialist fine-tuning remains a separately qualified future lesson.

## 67. What to take back to your team

5:29

Close with a concrete transfer task. Ask each participant to name one queue, one failure, one measurable outcome, and one person who can review labels in their own workflow. No claims beyond the recorded Banking77 experiment.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 68. Worked answer: classifier head



Offer the answer only after an attempt or a hint request. Learners must still run the free check and both actual training calls.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 69. Worked answer: review policy



The function should return a boolean. Exactly the threshold is routed in this specified policy. It is not a proof that the predicted probability is calibrated.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 70. Worked answer: judge validator



This uses the same type guard as the notebook. Valid JSON is only a response contract; it does not establish agreement with a reviewer.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.

## 71. Worked answer: preserve the probability-column order



This checks the metadata contract; the subsequent saved batch checks prediction parity independently. Passing both checks does not prove every route is correct. Give the worked answer after an attempt or explicit request.

## 72. Sources and recorded evidence



All measured claims come from the saved qualification. The native comparison captures show the verified routing publication and link to that saved record. Until external-account and human rehearsals pass, label this a technical preview.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.