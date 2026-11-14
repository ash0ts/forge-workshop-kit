---
theme: default
title: Find defective parts before they ship
author: Anish Shah
class: cover
layout: default
aspectRatio: 16/9
canvasWidth: 1280
colorSchema: light
transition: fade
wakeLock: false
fonts:
  sans: IBM Plex Sans
  mono: IBM Plex Mono
  provider: none
mdc: true
highlighter: shiki
drawings:
  enabled: false
download: false
exportFilename: visual-inspection
---

<div class="kicker">0:00</div>

# Find defective parts<br>before they ship

<div class="sub">Use real circuit-board photos to compare detectors, review their mistakes, and save a version another engineer can reproduce.</div><div class="bottom-note">Four hours · CPU classifiers · your own Forge project</div>


<!--
The inspection team is fictional. The VisA PCB1 images, masks and recorded comparisons are real. Do not promise that every participant run improves.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:02</div>

# The factory has two ways to waste a good morning

<div class="two-col"><div class="box"><h2>A defect gets through</h2><p>A board with a missing or damaged component passes inspection.</p></div><div class="box"><h2>A good board gets held</h2><p>An inspector spends time checking a normal board that the detector rejected.</p></div></div><div class="bottom-note">Management has requested fewer of both. It has not supplied a third category called “probably fine.”</div>


<!--
Ask participants which cost matters in their own work. We will count both errors. The joke does not define the release threshold.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:04</div>

# Start with the boards, not the score

<div class="photo-pair"><div><img src="/images/fit-normal.jpg" alt="Actual normal PCB1 training photograph"><p>Training example A</p></div><div><img src="/images/fit-defect.jpg" alt="Actual anomalous PCB1 training photograph"><p>Training example B</p></div></div><div class="bottom-note">VisA PCB1 · real photographs · labels hidden for this first inspection</div>


<!--
Ask learners to identify a region they would inspect. Do not infer a defect type without checking the supplied mask. They will reveal masks in the notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:08</div>

# What is in the teaching set?

<div class="cards"><div class="card"><strong>1,104 photographs</strong><p>One PCB family. 1,004 normal boards and 100 defective boards.</p></div><div class="card"><strong>Image labels</strong><p>A board-level normal or defective label is the classifier target.</p></div><div class="card"><strong>Defect masks</strong><p>Annotations let us inspect mistakes. They never enter the classifier.</p></div></div><div class="bottom-note">VisA, Zou et al. · CC BY 4.0 · the provided supervised split is preserved</div>


<!--
Explain the distinction between detecting a defective board and locating its defect. This classifier does the former. A patch-distance heatmap is not a segmentation model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:11</div>

# Separate the data before choosing a model

<div class="flow"><div class="box">397<br><small>fit models</small></div><span>+</span><div class="box">133<br><small>review pool</small></div><span>+</span><div class="box">132<br><small>validation</small></div><span>│</span><div class="box">442<br><small>final test</small></div></div><div class="bottom-note">Only the authors’ training partition is subdivided. The official test partition stays unchanged.</div>


<!--
The 132 validation boards contain 12 defects. A threshold targeting 90 percent recall must catch at least 11. Test data is public for reproduction, so this is a teaching boundary rather than a security barrier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:16</div>

# Connect to your own experiment

<div class="task">Open the Visual Inspection notebook and copy it into your Forge project.</div><ol class="exercise-controls"><li>Confirm <strong>Your Forge entity/project</strong>.</li><li>Click <strong>Connect and restore my inspection work</strong>.</li><li>Edit the attribute in <code>instrument_inspection_tool</code>, then click <strong>Send my first inspection trace</strong>.</li></ol><div class="done">Check: Find your attribute and the returned NumPy version in Agent Lens.</div>


<!--
Hosted authentication comes from the copied notebook. A laptop uses uv run wandb login. The core path has no inference calls; notebook compute remains separately billed.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:23</div>

# The trace describes a call that actually ran

```python {1-4|5-6|7-8|all}
with tracing.Tool(
    name=observation["name"],
    arguments=observation["arguments"],
    result=observation["result"],
    started_at=stamp(observation["started_at"]),
    ended_at=stamp(observation["ended_at"]),
) as tool:
    tool.set_attributes({"workshop.exercise": "pcb-inspection"})
```
<div class="bottom-note">Open the same call in Agent Lens. Match its arguments, result and timing to these fields.</div>


<!--
The training receipt is recorded before export. A publication failure does not mean the classifier failed. Retrying publication must not train it again.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:27</div>

# Inspect one board before revealing its label

<div class="task">Notebook step: Inspect the boards.</div><ol class="exercise-controls"><li>Click <strong>Download and verify the PCB1 teaching data</strong>.</li><li>Choose a training board. Explain what would make you inspect it.</li><li>Turn on <strong>Reveal the published defect label and mask</strong>.</li></ol><div class="done">Check: Describe the annotated region without treating the mask as an input to your detector.</div>


<!--
This is a participant decision, not a model evaluation. Give people a minute to make their own assessment before discussion.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:32</div>

# Predict a label for the whole board

<InspectionWalk kind="data" :step="1" />


<!--
After participants inspect a training photo, identify the input photograph and the binary target separately. A detector flags a board. The supplied mask marks pixels, but this model does not learn pixel labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:34</div>

# Use the mask to investigate the decision

<InspectionWalk kind="data" :step="2" />


<!--
Ask which input would leak the answer if passed to the classifier. The mask is reference evidence for human inspection; neither masks nor test labels enter feature assembly.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:37</div>

# Reuse a fixed image encoder

<InspectionWalk kind="encoder" :step="1" />


<!--
The ImageNet encoder is fixed. Fitting our logistic classifier changes its weights but not ResNet-18. The small cache can be reused in a CPU notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:41</div>

# Keep local information as well as the whole image

<InspectionWalk kind="encoder" :step="2" />


<!--
Read the shapes out loud: N boards, 14 rows, 14 columns, 64 feature channels. The overlay shows feature positions schematically, not exact independent image crops. The whole-image representation has 512 values; the grid retains spatial differences.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:47</div>

# Compare local features at the same board position

<InspectionWalk kind="patch" :step="1" />


<!--
Use only normal fitting boards as the reference bank. At each spatial position, find the closest actual reference vector after scaling. A normal fitting board cannot match itself. The older mean-patch result is preserved beside the later recorded comparison.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">0:53</div>

# Append 196 distances to the 512 whole-image values

<InspectionWalk kind="patch" :step="2" />


<!--
Walk the same board through errors, log1p, reshape and concatenate. The output has 708 columns. axis=0 would add observations rather than features and fail the shape/order fixture. log1p compresses large distances; it does not turn them into probabilities.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:59</div>

<a class="answer-link" href="/48">Worked answer →</a>

# Add local information to the classifier

<div class="task">Notebook step: Compute image features.</div><ol class="exercise-controls"><li>Complete <code>build_features</code>: calculate patch errors, apply <code>np.log1p</code>, and flatten one row per board.</li><li>Append the patch values to the whole-image vector along axis 1.</li><li>Click <strong>Check my patch-feature function</strong>.</li></ol><div class="done">Check: The check preserves board order and verifies both whole-image and nearest-patch behavior.</div>


<!--
The learner function is passed into fitting and saved with the freeze. Final evaluation reloads that saved source, not the current draft.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:14</div>

# Check the feature cache without rebuilding everything

```python
weights = teaching.fetch_weights(weights_path)
result = teaching.recompute_batch(data_root, weights)
assert result["matching_cached_features"]
```
<div class="bottom-note">Optional button: Recompute four cached board features. Downloads pinned weights; no model-provider call.</div>


<!--
The retained lossless inputs allow exact feature comparison. The prepared full cache took 39.25 seconds on the preparation Mac using two Torch CPU threads. This is not an attendee timing guarantee.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:19</div>

# Train the same classifier on each representation

```python {1-4|6|all}
model = inspection.fit_classifier(
    data, fit_rows, method,
    build_features=build_features,
    C=0.03,
)
validation_scores = inspection.score(
    data, validation_rows, model,
    build_features=build_features,
)
```
<div class="bottom-note">C controls regularization. This worked recipe fixes C before your run; labels and training cases are the same.</div>


<!--
Do not describe this as training a vision foundation model. We fit a logistic classifier over fixed encoder outputs. Patch distances add features but do not use pixel masks.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:22</div>

# Fit on training boards; measure on validation boards

<InspectionWalk kind="train" :step="1" />


<!--
Point to the learner build_features argument. The same function must be supplied to fit and score. We fit a small class-balanced logistic classifier, not the ResNet encoder. Saving a completed fit and exporting its trace happen afterward.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:26</div>

# A detector score still needs an operating rule

<InspectionWalk kind="threshold" :step="1" />


<!--
Scores are decision values, not calibrated defect probabilities. The optional review margin is in score units. A valid threshold function does not make the policy safe.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:32</div>

# Require 11 of the 12 validation defects to be caught

<InspectionWalk kind="threshold" :step="2" />


<!--
The slider uses the exact existing free fixture. With three fixture defects and recall 2/3 the cutoff is 0.7. For the real validation set, ceil(.9*12)=11. Explain that the chosen cutoff constrains this validation set only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:38</div>

<a class="answer-link" href="/49">Worked answer →</a>

# Implement the validation threshold

<div class="task">Notebook step: Compare global and patch features.</div><ol class="exercise-controls"><li>In <code>choose_threshold</code>, sort the scores of known validation defects.</li><li>Choose the largest cutoff that still catches at least 90% of them.</li><li>Click <strong>Check my threshold function</strong>, then <strong>Train both feature representations</strong>.</li></ol><div class="done">Check: Compare misses and false alarms alongside average precision.</div>


<!--
Allow participants to finish the local check before training. The 90 percent requirement constrains recall on validation only, not a guarantee for the final set.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:52</div>

# Keep ranking quality and operating errors separate

<table class="clean-table"><tbody><tr><th>Measure</th><th>Question it answers</th></tr><tr><td>Average precision</td><td>Are defective boards ranked ahead of normal boards?</td></tr><tr><td>Misses and false alarms</td><td>What happens at the frozen threshold?</td></tr><tr><td>Review volume</td><td>How many decisions are handed to a person?</td></tr></tbody></table>


<!--
AP summarizes precision over recall levels. Do not compare it to accuracy or confuse a change in review volume with better detection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:54</div>

# Calculate ranking quality before choosing one cutoff

<InspectionWalk kind="ranking" :step="1" />


<!--
Use the five public fixture scores. Defects occur at ranks 2,3,4; precision is 1/2,2/3,3/4 at those recalls. Average precision is their mean, 0.638889. This is an illustrative calculation, not a PCB1 result.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:57</div>

# Count operating errors at the chosen cutoff

<InspectionWalk kind="ranking" :step="2" />


<!--
At cutoff 0.7, the fixture has one missed defect and one false alarm. Moving the cutoff leaves the score ordering and AP unchanged. A review band sends additional cases to people and should be reported as workload, not detection improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">1:59</div>

# Follow one trained classifier through Forge

<div class="flow"><div class="box">Agent Lens<br><small>training operation</small></div><span>→</span><div class="box">W&B run<br><small>settings + metrics</small></div><span>→</span><div class="box">Artifact<br><small>classifier + source</small></div></div><div class="bottom-note">Open your own links. Find C, the representation, the validation errors, and the saved classifier file.</div>


<!--
These are actual inspection tasks rather than a generic dashboard tour. If export is unavailable, state that the execution is saved and show the publication retry.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:02</div>

# Read the recorded training call

<div class="native-pair"><div class="native-crop"><img src="/images/agent-lens-training-original.png" alt="Native Agent Lens tool input and validation output for the nearest-patch classifier"><span class="pin one">1</span><span class="pin two">2</span></div><div class="native-notes"><h2>1 · What ran</h2><p>397 fitting boards.<br>Nearest-patch features.<br>C = 0.03.</p><h2>2 · What it returned</h2><p>On <strong>132 validation boards</strong>: AP 0.883923, one missed defect, four false alarms.</p><p class="small">These are validation results. Final-test AP is reported later.</p></div></div><div class="bottom-note"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ff65c2eaa1cc5c5cf8adb6cb706f5f52">Open this recorded call in Agent Lens ↗</a> · Cropped for legibility; the source capture is included.</div>


<!--
Show the exact method, training count and C arguments. Then match the returned classifier path, saved file hash and validation metrics. The next execution uses the saved model. Native capture uses the rehearsal project; participants open their own links. This is tool-only tracing: there was no model-provider call.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:06</div>

# Match the tool call to the saved validation result

<InspectionWalk kind="train" :step="2" />


<!--
Return to the code and identify the training arguments corresponding to the capture. The trace is a CPU tool operation, with no LLM provider call. A failed trace upload must not cause another fit. Find C, method, training count and validation counts in your own run.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:10</div>

# Take ten minutes. Return at 2:20.

<div class="sub">Before you leave, check that both trained versions are saved. The notebook will wait; it has not developed an independent work ethic.</div>


<!--
Break from elapsed 2:10 to 2:20. Confirm both models are saved. After the break we choose where to spend 24 additional labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:20</div>

# Choose uncertain boards before opening their labels

<InspectionWalk kind="review" :step="1" />


<!--
Predict which scores the selector will choose. The public fixture uses row IDs 10,20,30,40 with scores .8,-.1,.01,-.9. At threshold 0, the two closest rows are 20 and 30. The function receives no labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:26</div>

# Give random selection the same labeling budget

<InspectionWalk kind="review" :step="2" />


<!--
Both branches start from the same nearest-patch parent and review pool. Each gets 24 labels; overlapping selections are allowed across methods. Random selection controls for simply receiving more data. Do not promise that uncertainty sampling wins.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:31</div>

<a class="answer-link" href="/50">Worked answer →</a>

# Choose where the review time goes

<div class="task">Notebook step: Choose examples to review.</div><ol class="exercise-controls"><li>Complete <code>choose_review</code> using distance from the current threshold. Do not read labels.</li><li>Click <strong>Check my review selector</strong>.</li><li>Click <strong>Select 24 boards for each review method</strong>.</li></ol><div class="done">Check: The active and random methods select 24 cases each from the same pool.</div>


<!--
The random condition matters because any additional labeled data might help. We cannot credit the selection strategy for the entire gain.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">2:42</div>

# Save what the reviewer actually decided

<div class="two-col"><div class="box"><h2>Your assessment</h2><p>Choose normal, defective, or needs another reviewer before revealing the annotation.</p><p>Save your assessment and whether the annotation was visible.</p></div><div class="box"><h2>Batch acquisition</h2><p>Reveal the authors’ supplied labels for the selected 24 boards.</p><p>Label this a simulation of acquiring annotations.</p></div></div>


<!--
Do not call all 24 labels human-verified because a participant pressed one button. Individual saved assessments and the supplied dataset labels are separate records.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:53</div>

# Train with the additional labels

<div class="task">Use both review selections, not just the one you prefer.</div><ol class="exercise-controls"><li>Inspect selected board photos and masks. Save at least one assessment.</li><li>Click <strong>Reveal batch labels and train the two reviewed classifiers</strong>.</li><li>Compare validation AP, misses and false alarms with the initial detector.</li></ol><div class="done">Check: Both new models use 397 initial boards plus 24 revealed cases.</div>


<!--
A tie or loss is still a usable experiment. Never select the final threshold from the official test labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:08</div>

# Choose before opening the final results

<div class="task">Notebook step: Freeze the detector.</div><ol class="exercise-controls"><li>Compare the four validation rows.</li><li>Choose a version and explain the tradeoff you accept.</li><li>Click <strong>Freeze models and thresholds before testing</strong>.</li></ol><div class="done">Check: The freeze contains the classifier, exact feature source, threshold and selection reason.</div>


<!--
Retaining the starting representation is valid. The final comparison includes all four versions regardless of selection.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:14</div>

# Freeze the preprocessing and reference bank too

<InspectionWalk kind="freeze" :step="1" />


<!--
Name the pieces needed to reproduce a score: reference bank, scaling, participant feature code, coefficients and threshold. Selecting the version uses validation. The final comparison still includes all four frozen versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:20</div>

# Take ten minutes. Return at 3:30.

<p class="sub">Your detector and threshold are frozen. Leave the final comparison for when everyone is back.</p>


<!--
Break from elapsed 3:20 to 3:30. No training runs during the break. On return, evaluate the saved versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:30</div>

# Evaluate the same 442 boards

<div class="task">Notebook step: Inspect untouched boards.</div><ol class="exercise-controls"><li>Click <strong>Evaluate all four frozen detectors on 442 test boards</strong>.</li><li>Choose a test board and compare predictions against its photo and mask.</li><li>Click <strong>Publish saved comparisons to Forge</strong>.</li></ol><div class="done">Check: Every version has a row for the same board; unavailable publication is shown separately.</div>


<!--
This is untouched for an attendee following the path. The recorded follow-up used a previously inspected test set, so its claim is narrower. Use Compare in EvalTables after publication. The native Weave-backed Preview and the separate CES v2 service have independent publication statuses.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:39</div>

# Compare four detectors on the same boards

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu"><img src="/images/evaltables-native.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:6%;top:39%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:6%;top:79%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:6%;top:60%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Set the reference</b><br>Use the whole-image detector first.</p><p><b>2 · Align the board</b><br>Open one case to compare the same photograph.</p><p><b>3 · Read checked outcomes</b><br>Correct and error score the frozen decisions. Review policy is separate.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu">Open this comparison ↗</a></p>


<!--
Click Publish saved comparisons to Forge, then Compare in EvalTables. The native Weave-backed Evaluation Tables Preview sits in the W&B workspace. These panels show per-case correctness and error, not average precision. The notebook computes average precision from the complete ranking. Scores and typed images come from the saved final evaluation; this action does not fit another classifier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:42</div>

# Inspect the board behind a prediction

<div class="eval-native-states"><div><div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu"><img src="/images/evaltables-native-detail.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:28.3%;top:25%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:28.3%;top:85.5%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:28.3%;top:95%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Look at the board</b><br>This is the actual PCB1 test photograph.</p><p><b>2 · Compare predictions</b><br>All four flag this board as defective.</p><p><b>3 · Check the threshold</b><br>Read each score against that detector’s frozen cutoff.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu">Open this comparison ↗</a></p></div><div v-click="1" class="eval-native-overlay"><div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu"><img src="/images/evaltables-native-mask.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:28.3%;top:40%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:28.3%;top:22%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:28.3%;top:88%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Read the annotation</b><br>White pixels mark the dataset’s reference defects.</p><p><b>2 · Compare decisions</b><br>All four detectors flag this same board.</p><p><b>3 · Check the result</b><br>Every prediction matches the defective label on this case.</p></div></div><p class="eval-native-caption">Reference defect mask: white marks annotated defects, not model localization. · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu">Open this comparison ↗</a></p></div></div>


<!--
Click once to reveal the reference defect mask for the same board. White pixels are supplied annotations, not model localization. Do not claim a patch heatmap is a causal explanation or segmentation model. Masks are used for inspection, not classifier inputs. Average precision ranks all boards; one row explains a particular operating decision. The separate CES v2 API remains unavailable; this is the working native Preview.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:45</div>

# The first worked recipe did not pass its gate

<table class="clean-table"><tbody><tr><th>First frozen recipe</th><th>Average precision</th><th>Misses</th><th>False alarms</th></tr><tr><td>Whole image</td><td>0.861762</td><td>4</td><td>36</td></tr><tr><td>Mean-patch + whole image</td><td>0.855382</td><td>2</td><td>33</td></tr></tbody></table><div class="bottom-note">Its declared primary measure was average precision. Fewer operating errors did not turn the AP loss into a pass.</div>


<!--
Preserve the failed result and all active/random review outcomes. This is why we choose the criterion before seeing results.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:47</div>

# The bounded follow-up improved this teaching retest

<table class="clean-table"><tbody><tr><th>Frozen follow-up</th><th>Average precision</th><th>Misses / 40</th><th>False alarms / 402</th></tr><tr><td>Whole image</td><td>0.872900</td><td>4</td><td>23</td></tr><tr><td>Nearest-patch + whole image</td><td>0.885742</td><td>3</td><td>18</td></tr></tbody></table><div class="bottom-note">One predeclared validation grid; already-inspected final images. AP gain: 1.284 points. This is a teaching retest, not fresh benchmark evidence.</div>


<!--
Both methods selected C=.03 from the same grid. No further tuning followed the retest. This result does not establish repeatability on a new product.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:49</div>

# Inspect a corrected miss

<div class="figure"><img src="/images/pcb1-anomaly-048.png" alt="Actual PCB1 anomaly-048. The supplied mask marks the right-hand header-pin area."><div class="caption">Actual PCB1 anomaly-048. The supplied mask marks the right-hand header-pin area.</div></div><div class="bottom-note">Whole image missed this board; nearest-patch flagged it at its own frozen threshold.</div>


<!--
Point to the missing or damaged header-pin area marked by the dataset. The heatmap also responds to background; do not claim it identifies the causal feature or performs accurate segmentation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:51</div>

# Inspect a new miss too

<div class="figure"><img src="/images/pcb1-anomaly-015.png" alt="Actual PCB1 anomaly-015. The small annotated region is near the solder/header area."><div class="caption">Actual PCB1 anomaly-015. The small annotated region is near the solder/header area.</div></div><div class="bottom-note">Whole image flagged this board; nearest-patch missed it. The average gain does not remove individual regressions.</div>


<!--
Show the contrast without hiding the final summary. This is a narrower, more honest explanation than saying patch features found all small defects.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:54</div>

# Reload the version you chose

<div class="task">Notebook step: Reproduce the selected version.</div><ol class="exercise-controls"><li>Click <strong>Reload the selected classifier and reproduce one prediction</strong>.</li><li>Compare the reloaded score with the saved value.</li><li>Explain what improved, what did not, and what data you would collect next.</li></ol><div class="done">Check: The exact file and source reproduce the saved result; your conclusion links to its evidence.</div>


<!--
Saved artifacts are useful because another person can repeat the prediction without guessing which notebook cell you last ran.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:56</div>

# Reproduce one score from the saved detector

<InspectionWalk kind="freeze" :step="2" />


<!--
The reload operation uses the frozen feature source rather than the current editor draft. Compare its output with the previously saved score for the same case. An artifact makes that complete version addressable; Registry is an optional release extension.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:57</div>

# A tested artifact can become the next release

<div class="flow"><div class="box">Evaluation<br><small>result + decision</small></div><span>→</span><div class="box">Registry<br><small>exact artifact</small></div><span>→</span><div class="box">Batch predictor<br><small>load that version</small></div></div><div class="bottom-note">Optional: fail a release check, then restore the previous artifact. Registry does not deploy an arbitrary Python classifier.</div>


<!--
This extension needs Registry permissions. The Artifact-based reproduction path remains available without them.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">3:59</div>

# Write down the decision you would make

<div class="box"><p>“We changed ____. On the same boards, ____ improved and ____ got worse. We selected ____ because ____. Before releasing it, we would test ____.”</p></div><div class="bottom-note">Publish my inspection Report · include actual comparisons, saved artifacts, and the next question.</div>


<!--
Have participants explain the result to someone else before publishing. A reasonable decision can be to retain the previous detector.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">Optional answer</div>

# Worked answer: assemble the local features

```python
whole = data["whole"][rows]
if method == "whole":
    return whole
if method == "nearest-patch":
    errors = inspection.nearest_patch_errors(data, rows, reference)
else:
    errors = inspection.patch_errors(data["patches"][rows], reference)
local = np.log1p(errors).reshape(len(rows), -1)
return np.concatenate([whole, local], axis=1)
```
<div class="bottom-note">Both branches are exercised by the free check. The live comparison uses nearest-patch.</div>
<div class="source-link"><a href="/15">Return to Add local information to the classifier</a></div>

<!--
The complete function signature is in the notebook. This body includes the historical mean-patch branch required by the free fixture. Each row remains one board; concatenation extends its feature columns.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">Optional answer</div>

# Worked answer: meet the validation recall target

```python
positives = np.sort(scores[target == 1])[::-1]
position = int(np.ceil(recall * len(positives))) - 1
return float(positives[position])
```
<div class="bottom-note">At 12 validation defects and recall .90, keep the top 11 above the threshold.</div>
<div class="source-link"><a href="/21">Return to Implement the validation threshold</a></div>

<!--
The retained cutoff depends on validation examples. It does not guarantee the same recall on final boards.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---

<div class="kicker">Optional answer</div>

# Worked answer: choose uncertain cases

```python
rng = np.random.default_rng(seed)
order = rng.permutation(len(rows))
order = order[np.argsort(
    np.abs(scores[order] - threshold), kind="stable"
)]
return np.asarray(rows)[order[:budget]]
```
<div class="bottom-note">The permutation only breaks equal-distance ties. Do not pass labels to this function.</div>
<div class="source-link"><a href="/31">Return to Choose where the review time goes</a></div>

<!--
Active selection here is uncertainty sampling. It is one policy to test, not a proven universal choice.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->
