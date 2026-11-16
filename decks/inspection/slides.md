---
theme: default
title: Find defective parts before they ship
author: Anish Shah
class: cover workshop-setting-slide
clicks: 1
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

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="inspection/start"><img :src="&quot;/scenes/inspection/start.svg&quot;" alt="Circuit-board inspection: Follow one board from the bench into inspection. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="sub">Find the board a detector missed.<br>Test different features and check the false alarms they create.</div><div class="bottom-note">Four hours · CPU classifiers · your own Forge project</div></div>


<!--
The team needs to catch defective boards without asking a person to inspect every good one. Start by looking at a real VisA PCB1 photograph before revealing its annotation. After training the baseline, follow a missed board through its features, score, and cutoff. Use EvalTables to compare that same board across versions, then inspect the other misses and false alarms before choosing a detector.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
Source: notes/sources.md.
-->

---
class: technical-manual
clicks: 4
---

<div class="kicker">0:02</div>

# What you will build and inspect

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;board&quot;, &quot;label&quot;: &quot;Board&quot;, &quot;svg&quot;: &quot;01-board.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/inspection/overview/slide/01-board.svg&quot;}, {&quot;id&quot;: &quot;features&quot;, &quot;label&quot;: &quot;Features&quot;, &quot;svg&quot;: &quot;02-features.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/inspection/overview/slide/02-features.svg&quot;}, {&quot;id&quot;: &quot;decision&quot;, &quot;label&quot;: &quot;Decision&quot;, &quot;svg&quot;: &quot;03-decision.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/inspection/overview/slide/03-decision.svg&quot;}, {&quot;id&quot;: &quot;recover&quot;, &quot;label&quot;: &quot;Recover&quot;, &quot;svg&quot;: &quot;04-recover.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/inspection/overview/slide/04-recover.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/inspection/overview/slide/05-complete.svg&quot;}]" :step="$clicks" />


<!--
Introduce the real task, the data available, and the outcome participants will check. Point to each Forge product at the operation it helps investigate.
Visual guide: inspection/overview. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">0:02</div>

# The factory has two ways to waste a good morning

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="inspection/inspect"><img :src="&quot;/scenes/inspection/inspect.svg&quot;" alt="Circuit-board inspection: Catch defects without sending every normal board for review. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="two-col"><div class="box"><h2>A defect gets through</h2><p>A board with a missing or damaged component passes inspection.</p></div><div class="box"><h2>A good board gets held</h2><p>An inspector spends time checking a normal board that the detector rejected.</p></div></div><div class="bottom-note">Management has requested fewer of both. It has not supplied a third category called “probably fine.”</div></div>


<!--
Ask participants which cost matters in their own work. We will count both errors. The joke does not define the release threshold.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:04</div>

# Start with the boards, not the score

<div class="photo-pair"><div><img src="/images/fit-normal.jpg" alt="VisA PCB1 fitting photograph A, viewed from above"><p>Training example A</p></div><div><img src="/images/fit-defect.jpg" alt="VisA PCB1 fitting photograph B, viewed from above"><p>Training example B</p></div></div><div class="bottom-note">VisA PCB1 · real photographs · labels hidden for this first inspection</div>


<!--
Ask learners to identify a region they would inspect. Do not infer a defect type without checking the supplied mask. They will reveal masks in the notebook. The same fitting example is bundled in the notebook setup. Ask for a pass/review choice before revealing its annotation; no authentication or download is needed.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:06</div>

# Predict a label for the whole board

<InspectionMechanism kind="data" :step="1" />


<!--
Ask participants to choose pass or inspection before advancing. The first figure hides its source label and mask. Identify the photograph as the input and the binary label as the target. A detector flags a board; it does not learn pixel labels here.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:08</div>

# Use the mask to investigate the decision

<InspectionMechanism kind="data" :step="2" />


<!--
Now reveal pcb1-anomaly-005 from the fitting partition: source image pcb1/Data/Images/Anomaly/005.JPG, SHA-256 ec34541be729af29a287bde12d4e3955cf3f83c734baea8a9505a7b801ce54e2, VisA CC BY 4.0. Source metadata and bundled image/mask checksums are in decks/inspection/data/feature-example.json. Ask which input would leak the answer if passed to the classifier. The mask is reference evidence for human inspection; neither masks nor test labels enter feature assembly.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:10</div>

# What is in the teaching set?

<div class="cards"><div class="card"><strong>1,104 photographs</strong><p>One PCB family. 1,004 normal boards and 100 defective boards.</p></div><div class="card"><strong>Image labels</strong><p>A board-level normal or defective label is the classifier target.</p></div><div class="card"><strong>Defect masks</strong><p>Annotations let us inspect mistakes. They never enter the classifier.</p></div></div><div class="bottom-note">VisA, Zou et al. · CC BY 4.0 · the provided supervised split is preserved</div>


<!--
Explain the distinction between detecting a defective board and locating its defect. This classifier does the former. A patch-distance heatmap is not a segmentation model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:13</div>

# Separate the data before choosing a model

<div class="flow"><div class="box">397<br><small>fit models</small></div><span>+</span><div class="box">133<br><small>review pool</small></div><span>+</span><div class="box">132<br><small>validation</small></div><span>│</span><div class="box">442<br><small>final test</small></div></div><div class="bottom-note">Only the authors’ training partition is subdivided. The official test partition stays unchanged.</div>


<!--
The 132 validation boards contain 12 defects. A threshold targeting 90 percent recall must catch at least 11. Test data is public for reproduction, so this is a teaching boundary rather than a security barrier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: workshop-sharing
---

<div class="kicker">0:17</div>

# Open the materials and download the notebook

<div class="workshop-share-layout"><div class="workshop-share-instructions"><ol><li><strong>Open this workshop’s page.</strong> Scan the code or type the short link.</li><li><strong>Download the current notebook.</strong> Save the Python file in a folder you will keep.</li><li><strong>Follow the two commands.</strong> Sign in, then open the saved file in marimo.</li><li><strong>Check the destination.</strong> Use your own writable project and account.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuH99" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuH99">utm.io/uuH99</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The first exercise follows. Opening the file does not start training or inference.</p>


<!--
Leave this QR code visible while participants open the workshop page. It links the current notebook, Report, deck, and run guide. Download the v0.12.0 Python file to a persistent folder. The page provides the pinned W&B sign-in and marimo launch commands. Enter a writable Forge project in notebook setup. The older hosted template is an optional path, not the current download. Continue to the existing setup exercise. The short link is managed in docs/share-links.json; do not reuse a historical event QR.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:17</div>

# Connect to your own experiment

<div class="task">Save the current Inspection notebook and follow its start page’s login and launch commands.</div><ol class="exercise-controls"><li>Confirm <strong>Your Forge entity/project</strong>.</li><li>Click <strong>Connect and restore my inspection work</strong>.</li><li>Edit the attribute in <code>instrument_inspection_tool</code>, then click <strong>Send my first inspection trace</strong>.</li></ol><div class="done">Check: Find your attribute and the returned NumPy version in Agent Lens.</div>


<!--
Use the pinned login command on the start page, initialize the controls once, and enter a writable Forge project. The core path uses the laptop CPU and makes no inference calls. Hosted compute, if used, has separate charges.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
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
---

<div class="kicker">0:32</div>

# Reuse a fixed image encoder

<InspectionMechanism kind="encoder" :step="1" />


<!--
The ImageNet encoder is fixed. Fitting our logistic classifier changes its weights but not ResNet-18. The small cache can be reused in a CPU notebook.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:37</div>

# Fit a first detector on whole-image features

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
---

<div class="kicker">0:40</div>

# Fit on training boards; measure on validation boards

<InspectionMechanism kind="train" :step="1" />


<!--
Point to the learner build_features argument. The same function must be supplied to fit and score. We fit a small class-balanced logistic classifier, not the ResNet encoder. Saving a completed fit and exporting its trace happen afterward.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: technical-manual
clicks: 3
---

<div class="kicker">0:44</div>

# Choose a threshold from validation data

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;score&quot;, &quot;label&quot;: &quot;Score&quot;, &quot;svg&quot;: &quot;01-score.svg&quot;, &quot;caption&quot;: &quot;Which tradeoff changes when the cutoff moves?&quot;, &quot;src&quot;: &quot;/guides/inspection/threshold/slide/01-score.svg&quot;}, {&quot;id&quot;: &quot;choose&quot;, &quot;label&quot;: &quot;Choose&quot;, &quot;svg&quot;: &quot;02-choose.svg&quot;, &quot;caption&quot;: &quot;Which tradeoff changes when the cutoff moves?&quot;, &quot;src&quot;: &quot;/guides/inspection/threshold/slide/02-choose.svg&quot;}, {&quot;id&quot;: &quot;count&quot;, &quot;label&quot;: &quot;Count&quot;, &quot;svg&quot;: &quot;03-count.svg&quot;, &quot;caption&quot;: &quot;Which tradeoff changes when the cutoff moves?&quot;, &quot;src&quot;: &quot;/guides/inspection/threshold/slide/03-count.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Which tradeoff changes when the cutoff moves?&quot;, &quot;src&quot;: &quot;/guides/inspection/threshold/slide/04-complete.svg&quot;}]" :step="$clicks" />


<!--
Scores are decision values, not calibrated defect probabilities. The optional review margin is in score units. A valid threshold function does not make the policy safe.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Visual guide: inspection/threshold. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
---

<div class="kicker">0:48</div>

# Require 11 of the 12 validation defects to be caught

<InspectionMechanism kind="threshold" :step="2" />


<!--
The slider uses the exact existing free fixture. With three fixture defects and recall 2/3 the cutoff is 0.7. For the real validation set, ceil(.9*12)=11. Explain that the chosen cutoff constrains this validation set only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:53</div>

<a class="answer-link" href="/61">Worked answer →</a>

# Implement the validation threshold

<div class="task">Notebook step: Train the whole-image baseline.</div><ol class="exercise-controls"><li>In <code>choose_threshold</code>, sort the scores of known validation defects.</li><li>Choose the largest cutoff that still catches at least 90% of them.</li><li>Click <strong>Check my threshold function</strong>, then <strong>Train the whole-image baseline</strong>.</li></ol><div class="done">Check: Open one validation miss or false alarm before adding patch features.</div>


<!--
Allow participants to finish the local check before training. The 90 percent requirement constrains recall on validation only, not a guarantee for the final set.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:05</div>

# Inspect a baseline miss or false alarm

<div class="task">Notebook: Train the whole-image baseline</div><ol class="exercise-controls"><li>Select a validation board. Compare the photograph, annotation, score, and cutoff.</li><li>Explain what the whole-image detector missed or flagged. What local detail might help?</li><li>Optionally click <strong>Save my baseline observation</strong>.</li></ol><p class="done"><b>Check:</b> A saved baseline decision supports your hypothesis. No patch model has run yet.</p>


<!--
Choose a saved validation error if available; do not force a failure. If the baseline gets the selected board right, describe what evidence would distinguish the next representation. The displayed score comes from the saved weights and feature source.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">1:04 · 8 minutes across these three frames</div>

# Investigate this result

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">Is this validation error about features, the threshold, or missing evidence?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f18536533b586759997a5dc392e6d94d" target="_blank" rel="noopener">compare/whole ↗</a></li></ul></div></div><p class="aria-foot">Use only the selected development or validation records. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>


<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">1:04 · 8 minutes across these three frames</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-response.png" target="_blank"><img src="/aria/investigate/investigate-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>91.7% defect recall and 8.3% false-alarm rate</blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/investigate/investigate-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e06c-ffe3-7542-863d-c0ade9bf44ee" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>


<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">1:04 · 8 minutes across these three frames</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-verification.png" target="_blank"><img src="/aria/investigate/investigate-verification.png" alt="Whole-image validation: one missed defect and ten false alarms among 132 boards."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="650.0" y="425.0" width="575.0" height="105.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="636.0" cy="438.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="636.0" y="442.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="650.0" y="575.0" width="575.0" height="51.99999999999999" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="636.0" cy="588.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="636.0" y="592.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> Errors at the frozen threshold</span><span><b>2</b> Validation denominator</span></figcaption></figure><div><b>Citation check: supported</b><p>Saved compare/whole metrics contain misses=1, defective=12, false_alarms=10, and normal=120. This gives defect recall 11/12 and false-alarm rate 10/120, matching the native run and training-call values quoted by ARIA. The attached board and supplied score do not establish that representation caused the miss; ARIA correctly left the cause unresolved.</p><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f18536533b586759997a5dc392e6d94d" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/investigate/investigate-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>


<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: technical-manual
clicks: 4
---

<div class="kicker">1:12</div>

# Compare whole-image and patch features

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;photo&quot;, &quot;label&quot;: &quot;Photo&quot;, &quot;svg&quot;: &quot;01-photo.svg&quot;, &quot;caption&quot;: &quot;Shared image and aligned board rows; whole and patch arrays are separate encoder outputs.&quot;, &quot;src&quot;: &quot;/guides/inspection/representations/slide/01-photo.svg&quot;}, {&quot;id&quot;: &quot;whole&quot;, &quot;label&quot;: &quot;Whole&quot;, &quot;svg&quot;: &quot;02-whole.svg&quot;, &quot;caption&quot;: &quot;Shared image and aligned board rows; whole and patch arrays are separate encoder outputs.&quot;, &quot;src&quot;: &quot;/guides/inspection/representations/slide/02-whole.svg&quot;}, {&quot;id&quot;: &quot;local&quot;, &quot;label&quot;: &quot;Local&quot;, &quot;svg&quot;: &quot;03-local.svg&quot;, &quot;caption&quot;: &quot;Shared image and aligned board rows; whole and patch arrays are separate encoder outputs.&quot;, &quot;src&quot;: &quot;/guides/inspection/representations/slide/03-local.svg&quot;}, {&quot;id&quot;: &quot;join&quot;, &quot;label&quot;: &quot;Join&quot;, &quot;svg&quot;: &quot;04-join.svg&quot;, &quot;caption&quot;: &quot;Shared image and aligned board rows; whole and patch arrays are separate encoder outputs.&quot;, &quot;src&quot;: &quot;/guides/inspection/representations/slide/04-join.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;Shared image and aligned board rows; whole and patch arrays are separate encoder outputs.&quot;, &quot;src&quot;: &quot;/guides/inspection/representations/slide/05-complete.svg&quot;}]" :step="$clicks" />


<!--
Read the shapes out loud: N boards, 14 rows, 14 columns, 64 feature channels. The overlay shows feature positions schematically, not exact independent image crops. The whole-image representation has 512 values; the grid retains spatial differences.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Visual guide: inspection/representations. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
---

<div class="kicker">1:16</div>

# Compare local features at the same board position

<InspectionMechanism kind="patch" :step="1" />


<!--
Use only normal fitting boards as the reference bank. At each spatial position, find the closest actual reference vector after scaling. A normal fitting board cannot match itself. The older mean-patch result is preserved beside the later recorded comparison.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: technical-manual
clicks: 4
---

<div class="kicker">1:22</div>

# Calculate one location’s distance

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;query&quot;, &quot;label&quot;: &quot;Query&quot;, &quot;svg&quot;: &quot;01-query.svg&quot;, &quot;caption&quot;: &quot;Which normal patch is the closest reference for this location?&quot;, &quot;src&quot;: &quot;/guides/inspection/patch-distance/slide/01-query.svg&quot;}, {&quot;id&quot;: &quot;scale&quot;, &quot;label&quot;: &quot;Scale&quot;, &quot;svg&quot;: &quot;02-scale.svg&quot;, &quot;caption&quot;: &quot;Which normal patch is the closest reference for this location?&quot;, &quot;src&quot;: &quot;/guides/inspection/patch-distance/slide/02-scale.svg&quot;}, {&quot;id&quot;: &quot;distance&quot;, &quot;label&quot;: &quot;Distance&quot;, &quot;svg&quot;: &quot;03-distance.svg&quot;, &quot;caption&quot;: &quot;Which normal patch is the closest reference for this location?&quot;, &quot;src&quot;: &quot;/guides/inspection/patch-distance/slide/03-distance.svg&quot;}, {&quot;id&quot;: &quot;map&quot;, &quot;label&quot;: &quot;Map&quot;, &quot;svg&quot;: &quot;04-map.svg&quot;, &quot;caption&quot;: &quot;Which normal patch is the closest reference for this location?&quot;, &quot;src&quot;: &quot;/guides/inspection/patch-distance/slide/04-map.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;Which normal patch is the closest reference for this location?&quot;, &quot;src&quot;: &quot;/guides/inspection/patch-distance/slide/05-complete.svg&quot;}]" :step="$clicks" />


<!--
These values come from the real prepared feature cache, not the five-board threshold fixture. Only fitting boards form the reference bank. The free calculation does not fit a classifier.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.
Visual guide: inspection/patch-distance. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
---

<div class="kicker">1:27</div>

# Append 196 distances to the 512 whole-image values

<InspectionMechanism kind="features" :step="2" />


<!--
Walk the same board through errors, log1p, reshape and concatenate. The output has 708 columns. axis=0 would add observations rather than features and fail the shape/order fixture. log1p compresses large distances; it does not turn them into probabilities.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:32</div>

<a class="answer-link" href="/60">Worked answer →</a>

# Add local information to the classifier

<div class="task">Notebook step: Compute image features.</div><ol class="exercise-controls"><li>Complete <code>build_features</code>: calculate patch errors, apply <code>np.log1p</code>, and flatten one row per board.</li><li>Append the patch values to the whole-image vector along axis 1.</li><li>Click <strong>Check my patch-feature function</strong>.</li></ol><div class="done">Check: The check preserves board order and verifies both whole-image and nearest-patch behavior.</div>


<!--
The learner function is passed into fitting and saved with the freeze. Final evaluation reloads that saved source, not the current draft.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">1:41</div>

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
class: exercise
---

<div class="kicker">1:44</div>

# Test patches against the saved baseline

<div class="task">Notebook: Compare global and patch features</div><ol class="exercise-controls"><li>Keep the whole-image branch, C=0.03, and threshold rule unchanged.</li><li>Click <strong>Train the patch-feature alternative</strong>.</li><li>Compare its validation mistakes with the saved whole-image result.</li></ol><p class="done"><b>Check:</b> Both representations are saved before continuing to review selection.</p>


<!--
The first fit remains valid while learners implement the patch branch. A changed threshold rule or changed whole-image inputs would confound this comparison and is rejected. Previously saved matching runs are reused.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py.
Source: notes/sources.md.
-->

---
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
---

<div class="kicker">1:54</div>

# Calculate ranking quality before choosing one cutoff

<InspectionMechanism kind="ranking" :step="1" />


<!--
Use the five public fixture scores. Defects occur at ranks 2,3,4; precision is 1/2,2/3,3/4 at those recalls. Average precision is their mean, 0.638889. This is an illustrative calculation, not a PCB1 result.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">1:57</div>

# Count operating errors at the chosen cutoff

<InspectionMechanism kind="ranking" :step="2" />


<!--
At cutoff 0.7, the fixture has one missed defect and one false alarm. Moving the cutoff leaves the score ordering and AP unchanged. A review band sends additional cases to people and should be reported as workload, not detection improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
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
---

<div class="kicker">2:06</div>

# Match the tool call to the saved validation result

<InspectionMechanism kind="train" :step="2" />


<!--
Return to the code and identify the training arguments corresponding to the capture. The trace is a CPU tool operation, with no LLM provider call. A failed trace upload must not cause another fit. Find C, method, training count and validation counts in your own run.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
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
class: technical-manual
clicks: 3
---

<div class="kicker">2:20</div>

# Compare equal labeling budgets

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;active&quot;, &quot;label&quot;: &quot;Active&quot;, &quot;svg&quot;: &quot;01-active.svg&quot;, &quot;caption&quot;: &quot;Did the selection policy help, or did more labeled data help?&quot;, &quot;src&quot;: &quot;/guides/inspection/review/slide/01-active.svg&quot;}, {&quot;id&quot;: &quot;random&quot;, &quot;label&quot;: &quot;Random&quot;, &quot;svg&quot;: &quot;02-random.svg&quot;, &quot;caption&quot;: &quot;Did the selection policy help, or did more labeled data help?&quot;, &quot;src&quot;: &quot;/guides/inspection/review/slide/02-random.svg&quot;}, {&quot;id&quot;: &quot;compare&quot;, &quot;label&quot;: &quot;Compare&quot;, &quot;svg&quot;: &quot;03-compare.svg&quot;, &quot;caption&quot;: &quot;Did the selection policy help, or did more labeled data help?&quot;, &quot;src&quot;: &quot;/guides/inspection/review/slide/03-compare.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Did the selection policy help, or did more labeled data help?&quot;, &quot;src&quot;: &quot;/guides/inspection/review/slide/04-complete.svg&quot;}]" :step="$clicks" />


<!--
Predict which scores the selector will choose. The public fixture uses row IDs 10,20,30,40 with scores .8,-.1,.01,-.9. At threshold 0, the two closest rows are 20 and 30. The function receives no labels.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Visual guide: inspection/review. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
---

<div class="kicker">2:26</div>

# Give random selection the same labeling budget

<InspectionMechanism kind="review" :step="2" />


<!--
Both branches start from the same nearest-patch parent and review pool. Each gets 24 labels; overlapping selections are allowed across methods. Random selection controls for simply receiving more data. Do not promise that uncertainty sampling wins.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:31</div>

<a class="answer-link" href="/62">Worked answer →</a>

# Choose where the review time goes

<div class="task">Notebook step: Choose examples to review.</div><ol class="exercise-controls"><li>Complete <code>choose_review</code> using distance from the current threshold. Do not read labels.</li><li>Click <strong>Check my review selector</strong>.</li><li>Click <strong>Select 24 boards for each review method</strong>.</li></ol><div class="done">Check: The active and random methods select 24 cases each from the same pool.</div>


<!--
The random condition matters because any additional labeled data might help. We cannot credit the selection strategy for the entire gain.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">2:42</div>

# Save what the reviewer actually decided

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="inspection/build"><img :src="&quot;/scenes/inspection/build.svg&quot;" alt="Circuit-board inspection: Save the reviewer’s decision before revealing the supplied label. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="two-col"><div class="box"><h2>Your assessment</h2><p>Choose normal, defective, or needs another reviewer before revealing the annotation.</p><p>Save your assessment and whether the annotation was visible.</p></div><div class="box"><h2>Batch acquisition</h2><p>Reveal the authors’ supplied labels for the selected 24 boards.</p><p>Label this a simulation of acquiring annotations.</p></div></div></div>


<!--
Do not call all 24 labels human-verified because a participant pressed one button. Individual saved assessments and the supplied dataset labels are separate records.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
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
---

<div class="kicker">3:14</div>

# Freeze the preprocessing and reference bank too

<InspectionMechanism kind="freeze" :step="1" />


<!--
Name the pieces needed to reproduce a score: reference bank, scaling, participant feature code, coefficients and threshold. Selecting the version uses validation. The final comparison still includes all four frozen versions.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
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
class: technical-manual
clicks: 3
---

<div class="kicker">3:49</div>

# Inspect a recovered defect and a new miss

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;miss&quot;, &quot;label&quot;: &quot;Miss&quot;, &quot;svg&quot;: &quot;01-miss.svg&quot;, &quot;caption&quot;: &quot;Did the change help this board, and what happened elsewhere?&quot;, &quot;src&quot;: &quot;/guides/inspection/case-changes/slide/01-miss.svg&quot;}, {&quot;id&quot;: &quot;recover&quot;, &quot;label&quot;: &quot;Recover&quot;, &quot;svg&quot;: &quot;02-recover.svg&quot;, &quot;caption&quot;: &quot;Did the change help this board, and what happened elsewhere?&quot;, &quot;src&quot;: &quot;/guides/inspection/case-changes/slide/02-recover.svg&quot;}, {&quot;id&quot;: &quot;regression&quot;, &quot;label&quot;: &quot;Regression&quot;, &quot;svg&quot;: &quot;03-regression.svg&quot;, &quot;caption&quot;: &quot;Did the change help this board, and what happened elsewhere?&quot;, &quot;src&quot;: &quot;/guides/inspection/case-changes/slide/03-regression.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Did the change help this board, and what happened elsewhere?&quot;, &quot;src&quot;: &quot;/guides/inspection/case-changes/slide/04-complete.svg&quot;}]" :step="$clicks" />


<!--
Point to the missing or damaged header-pin area marked by the dataset. The heatmap also responds to background; do not claim it identifies the causal feature or performs accurate segmentation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Visual guide: inspection/case-changes. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">3:49</div>

# Inspect a new miss too

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="inspection/compare"><img :src="&quot;/scenes/inspection/compare.svg&quot;" alt="Circuit-board inspection: Recorded retest: 048 is recovered; 015 becomes a new miss. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><InspectionMechanism kind="outcomes" case-id="pcb1-anomaly-015" /></div>


<!--
Show the contrast without hiding the final summary. This is a narrower, more honest explanation than saying patch features found all small defects.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">3:50 · 7 minutes across these three frames</div>

# Check our conclusion

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">Which defects were recovered, and which mistakes remain?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/08c45f8ed417d216d026cf1abdc280b2" target="_blank" rel="noopener">evaluate ↗</a></li></ul></div></div><p class="aria-foot">Keep the compared versions frozen. Suggest a future experiment without running it. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>


<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">3:50 · 7 minutes across these three frames</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-response.png" target="_blank"><img src="/aria/conclusion/conclusion-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>16 false alarms versus 12</blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/conclusion/conclusion-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e06d-f15f-75e0-b27a-43e3063e6110" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>


<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: aria-investigation
---

<div class="kicker">3:50 · 7 minutes across these three frames</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-verification.png" target="_blank"><img src="/aria/conclusion/conclusion-verification.png" alt="Native final comparison aligns 442 boards across whole-image, patch, active-review, and random-review versions."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="97.0" y="398.0" width="275.0" height="137.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="83.0" cy="411.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="83.0" y="415.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="1090.0" y="672.0" width="160.0" height="30.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="1076.0" cy="685.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="1076.0" y="689.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> Correctness, not miss count</span><span><b>2</b> 442 aligned cases</span></figcaption></figure><div><b>Citation check: supported</b><p>The saved evaluate result has selected=review/random. Among the same 442 boards, review/active has misses=1 and false_alarms=16, while review/random has misses=5 and false_alarms=12. These match the artifact values ARIA reports reading. The native screenshot shows rounded correctness, not those separate counts. This check does not independently establish the time of selection or a causal advantage of active sampling.</p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/08c45f8ed417d216d026cf1abdc280b2" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/conclusion/conclusion-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>


<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/visual_inspection/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
Source: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:57</div>

# Reload the version you chose

<div class="task">Notebook step: Reproduce the selected version.</div><ol class="exercise-controls"><li>Click <strong>Reload the selected classifier and reproduce one prediction</strong>.</li><li>Compare the reloaded score with the saved value.</li><li>Explain what improved, what did not, and what data you would collect next.</li></ol><div class="done">Check: The exact file and source reproduce the saved result; your conclusion links to its evidence.</div>


<!--
Saved artifacts are useful because another person can repeat the prediction without guessing which notebook cell you last ran.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: technical-manual
clicks: 4
---

<div class="kicker">3:58</div>

# Recover every component of the detector

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;encoder&quot;, &quot;label&quot;: &quot;Encoder&quot;, &quot;svg&quot;: &quot;01-encoder.svg&quot;, &quot;caption&quot;: &quot;What must be loaded to reproduce a board’s decision?&quot;, &quot;src&quot;: &quot;/guides/inspection/reproduce/slide/01-encoder.svg&quot;}, {&quot;id&quot;: &quot;bank&quot;, &quot;label&quot;: &quot;Bank&quot;, &quot;svg&quot;: &quot;02-bank.svg&quot;, &quot;caption&quot;: &quot;What must be loaded to reproduce a board’s decision?&quot;, &quot;src&quot;: &quot;/guides/inspection/reproduce/slide/02-bank.svg&quot;}, {&quot;id&quot;: &quot;classifier&quot;, &quot;label&quot;: &quot;Classifier&quot;, &quot;svg&quot;: &quot;03-classifier.svg&quot;, &quot;caption&quot;: &quot;What must be loaded to reproduce a board’s decision?&quot;, &quot;src&quot;: &quot;/guides/inspection/reproduce/slide/03-classifier.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;What must be loaded to reproduce a board’s decision?&quot;, &quot;src&quot;: &quot;/guides/inspection/reproduce/slide/04-complete.svg&quot;}, {&quot;id&quot;: &quot;native-capture&quot;, &quot;label&quot;: &quot;The training call and returned classifier&quot;, &quot;svg&quot;: &quot;05-native-capture.svg&quot;, &quot;caption&quot;: &quot;Match nearest-patch, fitting count, and C to this returned classifier. These metrics use validation boards.&quot;, &quot;src&quot;: &quot;/guides/inspection/reproduce/slide/05-native-capture.svg&quot;}]" :step="$clicks" />


<!--
The reload operation uses the frozen feature source rather than the current editor draft. Compare its output with the previously saved score for the same case. An artifact makes that complete version addressable; Registry is an optional release extension.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Visual guide: inspection/reproduce. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
Source: notes/sources.md.
-->

---
---

<div class="kicker">3:58</div>

# A tested artifact can become the next release

<div class="flow"><div class="box">Evaluation<br><small>result + decision</small></div><span>→</span><div class="box">Registry<br><small>exact artifact</small></div><span>→</span><div class="box">Batch predictor<br><small>load that version</small></div></div><div class="bottom-note">Optional: fail a release check, then restore the previous artifact. Registry does not deploy an arbitrary Python classifier.</div>


<!--
This extension needs Registry permissions. The Artifact-based reproduction path remains available without them.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">3:59</div>

# Write down the decision you would make

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="inspection/release"><img :src="&quot;/scenes/inspection/release.svg&quot;" alt="Circuit-board inspection: Preserve the encoder, normal bank, and classifier. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="box"><p>“We changed ____. On the same boards, ____ improved and ____ got worse. We selected ____ because ____. Before releasing it, we would test ____.”</p></div><div class="bottom-note">Publish my inspection Report · include actual comparisons, saved artifacts, and the next question.</div></div>


<!--
Have participants explain the result to someone else before publishing. A reasonable decision can be to retain the previous detector.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
Source: notes/sources.md.
-->

---
class: workshop-sharing
---

<div class="kicker">3:59</div>

# Keep the notebook and workshop materials

<div class="workshop-share-layout"><div class="workshop-share-instructions"><p>Reopen your saved notebook file to continue your work.</p><ol><li><strong>Revisit the example.</strong> The Report links its claims to recorded results.</li><li><strong>Keep the materials.</strong> Open the deck, download the PDF, or get the source.</li><li><strong>Run a session.</strong> Use the short run guide and facilitator notes.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuH99" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuH99">utm.io/uuH99</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The shared page has the current download and references. Your Forge records remain in your own project.</p>


<!--
Keep this slide up during questions. Participants resume their saved notebook file. The QR page provides the current notebook, Report, downloads, and short facilitator run guide. Use recorded examples for a demo; check the current readiness notes before scheduling live delivery.
Source: notes/sources.md.
-->

---
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
# Compress distances, then preserve one row per board.
local = np.log1p(errors).reshape(len(rows), -1)
# Feature axis: 512 whole-image values + 196 patch values.
return np.concatenate([whole, local], axis=1)
```
<div class="bottom-note">Both branches are exercised by the free check. The live comparison uses nearest-patch.</div>
<div class="source-link"><a href="/27">Return to Add local information to the classifier</a></div>

<!--
The complete function signature is in the notebook. This body includes the historical mean-patch branch required by the free fixture. Each row remains one board; concatenation extends its feature columns.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
---

<div class="kicker">Optional answer</div>

# Worked answer: meet the validation recall target

```python
# Rank validation defects from highest score to lowest.
positives = np.sort(scores[target == 1])[::-1]
# ceil(.90 * 12) = 11; subtract 1 to address the eleventh array entry.
position = int(np.ceil(recall * len(positives))) - 1
return float(positives[position])  # Highest cutoff that still catches 11.
```
<div class="bottom-note">At 12 validation defects and recall .90, keep the top 11 above the threshold.</div>
<div class="source-link"><a href="/18">Return to Implement the validation threshold</a></div>

<!--
The retained cutoff depends on validation examples. It does not guarantee the same recall on final boards.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->

---
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
<div class="source-link"><a href="/39">Return to Choose where the review time goes</a></div>

<!--
Active selection here is uncertainty sampling. It is one policy to test, not a proven universal choice.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/inspection.py.
Source: notes/sources.md.
-->
