---
theme: default
title: Route customer requests and learn from mistakes
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
---

<div class="kicker">0:00</div>

# Route customer requests<br>and learn from mistakes

<div class="sub">Train a support router, review its errors, and test a revised version using public banking requests.</div><div class="bottom-note">Three hours · CPU classifiers · Agent Lens · W&B · Weave and EvalTables</div>

<!--
The support team is fictional. The messages are public Banking77 data. We will make a genuine measured classifier comparison, then let participants run an open-ended data review experiment. Do not promise that every personal review will improve the score.
-->

---

<div class="kicker">0:02</div>

# The support queue needs a destination

<div class="two-col"><div class="ticket"><small>Request A</small>“Is there a way to know when my card will arrive?”</div><div class="ticket"><small>Request B</small>“I think my card is broken”</div></div><div v-click class="two-col"><div>Card delivery</div><div>Card troubleshooting</div></div><p class="caption">Actual examples in the dataset authors’ README. A fluent response does not tell us that the request reached the right workflow.</p>

<!--
Ask people what team should handle each request. These short examples explain the target before the model appears. We classify intent; we are not resolving accounts or giving financial advice. Source: PolyAI-LDN/task-specific-datasets.
-->

---

<div class="kicker">0:04</div>

# A manager has offered to automate forwarding

<div class="quote">“If the system can write the whole email, surely it can pick a queue.”</div><div class="flow"><div>Message<small>What the customer wrote</small></div><b class="arrow">→</b><div>Routing decision<small>One intent, or human review</small></div><b class="arrow">→</b><div>Support workflow<small>Delivery, troubleshooting, disputed payment…</small></div></div>

<!--
This is fictional dialogue. The engineering problem is a constrained label choice. A wrong label wastes time even if the message is polite and the JSON validates. Keep the humor in the manager line, and the task literal.
-->

---

<div class="kicker">0:06</div>

# The dataset contains 77 banking intents

<div class="two-col"><div class="metric">10,003<small>Original training messages</small></div><div class="metric">3,080<small>Original test messages</small></div></div><p>Banking77 was published by PolyAI researchers with intent annotations. We preserve the official test split.</p><p class="caption">CC-BY-4.0 · Casanueva et al., 2020 · Dataset source and checksums travel with the workshop download.</p>

<!--
The data are public queries, not attendee customer records. There are 77 classes. The official test set contains 40 examples per class. One low-resource training class has only 35 examples, which is why we reserve ten validation and ten review cases per class rather than twenty each.
-->

---

<div class="kicker">0:08</div>

# Give each partition one job

<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="8463 train messages fit models,770 validation choose changes,770 review accept labels,3080 official test evaluate frozen versions"><rect x="0" y="30" width="330" height="135" fill="#d5e5d8"/><rect x="350" y="30" width="230" height="135" fill="#e6e5ce"/><rect x="600" y="30" width="230" height="135" fill="#e6e5ce"/><rect x="850" y="30" width="260" height="135" fill="#dfe3e0"/><text x="24" y="70" style="font-size:29px">8,463 train</text><text x="24" y="115" style="font-size:22px">Fit classifier weights</text><text x="372" y="70" style="font-size:29px">770 validation</text><text x="372" y="115" style="font-size:22px">Choose settings</text><text x="622" y="70" style="font-size:29px">770 review</text><text x="622" y="115" style="font-size:22px">Accept labels</text><text x="872" y="70" style="font-size:29px">3,080 test</text><text x="872" y="115" style="font-size:22px">Score frozen choices</text><path d="M20 190H820" stroke="#587a69" stroke-width="2"/><text x="225" y="230" style="font-size:23px">Derived from the authors’ training split</text><text x="872" y="230" style="font-size:23px">Official test split</text></svg>

<!--
The split order was fixed before any model score. Ten examples of every intent go to validation and ten to the review pool. The test partition is only opened after selection freezes. Files are public for teaching; the code keeps final cases out of model-editing and labeling prompts.
-->

---
class: exercise
---

<div class="kicker">0:10</div>

# Open your copy and add your first trace



<p class="where">Notebook → Connect</p><ol><li>Copy the template into a writable project and open Edit.</li><li>Run stale cells to create the controls; exercise buttons stay unpressed.</li><li>In <code>instrument_tool</code>, add a descriptive span attribute.</li></ol><div class="done"><strong>Run:</strong> Connect and restore my work → Send my first Agent Lens trace<br><strong>Check:</strong> Find your attribute in the tool span.</div>

<!--
Let everyone open their own project. Hosted authentication is inherited; there is no shared gateway or host token. The $8 adjustable allowance covers fixed-model inference; CPU notebook charges are separate.
-->

---

<div class="kicker">0:15</div>

# The span should explain the operation

```python {1-4|5-8|all}
with tracing.Tool(
    name=observation["name"],
    arguments=observation["arguments"],
    result=observation["result"],
    started_at=stamp(observation["started_at"]),
    ended_at=stamp(observation["ended_at"]),
) as span:
    span.set_attributes({"workshop.exercise": "request-routing"})
```

<p class="caption">Open the returned Agent Lens link. Check the arguments, result, timestamp, and your attribute.</p>

<!--
The notebook captures an independent event receipt and uses this participant-written function to export it. We compare stored spans with the receipt. A publication failure does not mean the operation failed or should be repeated.
-->

---
class: exercise
---

<div class="kicker">0:20</div>

# Read a request before revealing its label



<p class="where">Notebook → Inspect requests</p><ol><li>Click Download and check Banking77.</li><li>Choose a request and explain the support workflow it needs.</li><li>Reveal the published label. Keep any disagreement as a question to inspect.</li></ol><div class="done"><strong>Run:</strong> Download and check Banking77<br><strong>Check:</strong> Identify a request where similar wording could lead to a different intent.</div>

<!--
Allow five minutes for individual predictions and partner discussion. The download includes 20 MB of cached features, original CSVs, license, and checksum manifest. Data loading sends no model call.
-->

---

<div class="kicker">0:30</div>

# Start with a word-based classifier

<div class="flow"><div>Request<small>“Where is my card?”</small></div><b class="arrow">→</b><div>TF–IDF<small>Word unigrams and bigrams</small></div><b class="arrow">→</b><div>Linear classifier<small>77 intent probabilities</small></div></div><p>TF–IDF gives distinctive words and phrases more weight. The classifier learns which combinations indicate each intent.</p><p class="caption">The text example illustrates the representation. The measured comparison uses the complete fixed partitions.</p>

<!--
Explain unigrams and bigrams with card and my card. Fit the vectorizer only on training messages so validation vocabulary does not alter the feature space. This is a standard, inexpensive baseline, not a deliberately broken model.
-->

---

<div class="kicker">0:34</div>

# Then change the representation

<div class="flow"><div>Request<small>Same messages and splits</small></div><b class="arrow">→</b><div>Frozen MiniLM<small>384 numbers per message</small></div><b class="arrow">→</b><div>Linear classifier<small>Same training recipe</small></div></div><p>The pretrained encoder gives semantically similar sentences nearby representations. Only the classifier’s weights train here.</p><p class="caption">all-MiniLM-L6-v2 · pinned revision · attention-masked mean pooling · L2 normalization</p>

<!--
Contrast sentence representation with lexical overlap. The cached encoder features are versioned and can be regenerated by the supplied preparation code. Cache lookup timing is not end-to-end encoder latency. The comparison changes representation, not data quantity or test cases.
-->

---
class: exercise
---

<div class="kicker">0:38</div>

# Implement the classifier head

<a class="answer-link" href="33">Worked answer ↗</a>

<p class="where">Notebook → Train classifiers</p><ol><li>Complete <code>make_classifier</code> with <code>LogisticRegression(C=10, max_iter=1000, random_state=17)</code>.</li><li>Run the free practice check.</li><li>Train both representations using that same function.</li></ol><div class="done"><strong>Run:</strong> Train both classifiers on the same messages<br><strong>Check:</strong> Compare validation macro-F1 and open the saved source in Forge.</div>

<!--
The participant function is used in both actual fits. CPU training is bounded by iterations and two numerical-library threads. In preparation each fit took under four seconds with cached features; participant machines and hosting differ.
-->

---

<div class="kicker">0:45</div>

# Macro-F1 gives each intent equal weight

<div class="two-col"><div><h2>Precision</h2><p>Of the requests sent to an intent, how many belonged there?</p><h2>Recall</h2><p>Of the requests that belonged there, how many did we find?</p></div><div><h2>F1 per intent</h2><p>The harmonic mean of that intent’s precision and recall.</p><h2>Macro-F1</h2><p>Average the 77 intent scores. Keep per-intent mistakes alongside it.</p></div></div>

<!--
Do not average row-wise F1 values. Macro-F1 is computed from the whole matched prediction set. Accuracy is also reported. Neither metric tells the whole operational story because review can defer some cases.
-->

---

<div class="kicker">0:50</div>

# The worked comparison reduced routing mistakes

<table class="clean-table"><tr><th>Fixed recipe</th><th>Test macro-F1</th><th>Accuracy</th></tr><tr><td>Word TF–IDF + classifier</td><td>0.879385</td><td>0.879545</td></tr><tr><td>Frozen MiniLM + classifier</td><td>0.920229</td><td>0.920779</td></tr></table><p>Embedding features improved macro-F1 by <strong>4.0844 percentage points</strong> on the same 3,080 test messages.</p><p class="caption">Recorded qualification, not your live result. Seeds 17, 29, 43 produced identical fits; this is one dataset split, not three independent studies.</p>

<!--
The fixed contract preceded final evaluation. Publish all six outcomes. Participants will inspect their own validation results first; the recorded result is a worked comparison and cannot be attributed to unexecuted learner edits. The deterministic seed repetitions check reproduction rather than uncertainty.
-->

---

<div class="kicker">0:55</div>

# A router can also ask a person

<div class="two-col"><div class="metric">Coverage<small>Fraction routed automatically</small></div><div class="metric">Selective accuracy<small>Accuracy among those routed requests</small></div></div><p>Raising the review threshold can improve selective accuracy while sending more work to people. That is a policy tradeoff, not a new classifier.</p><p class="caption">At threshold 0.5 in the recorded test: TF–IDF routes 75.84%; embeddings route 91.10%. Both are about 96% accurate among routed requests.</p>

<!--
Ask what happens if every request is deferred. Coverage becomes zero, selective accuracy is unavailable, and full classifier quality remains unchanged. The model probabilities are not calibrated guarantees.
-->

---
class: exercise
---

<div class="kicker">1:00</div>

# Write the rule that sends a request to review

<a class="answer-link" href="34">Worked answer ↗</a>

<p class="where">Notebook → Review requests</p><ol><li>Complete <code>needs_review(confidence, threshold)</code>.</li><li>Move the threshold and compare coverage with selective accuracy.</li><li>Pick a small-margin request and read both proposed intents.</li></ol><div class="done"><strong>Run:</strong> Check my review rule<br><strong>Check:</strong> Explain why a confidence of 0.2 at threshold 0.5 should go to a person.</div>

<!--
The function changes the displayed policy and the policy frozen for final evaluation. Its local check is free. Let people observe the coverage tradeoff rather than supply a preferred threshold.
-->

---

<div class="kicker">1:07</div>

# Read the disagreement before declaring failure

<RoutingCase />

<!--
These four examples are actual outputs from the training-derived review pool. The published annotation is a reference, not proof that every message is unambiguous. The first two were selected as disagreements with the dataset annotation; the last two agree with it. They are not human review records. Let learners explain disagreement in their own words.
-->

---
class: exercise
---

<div class="kicker">1:13</div>

# Save labels someone can trace back to a decision



<p class="where">Notebook → Review requests</p><ol><li>Review at least four requests, including a correct route and a mistake.</li><li>Select the accepted intent yourself and enter a reviewer name or alias.</li><li>Save each label; do not copy the model suggestion just because it is available.</li></ol><div class="done"><strong>Run:</strong> Save my reviewed label<br><strong>Check:</strong> The saved record contains case, proposal, accepted label, reviewer, and dataset version.</div>

<!--
Show the provenance fields in the dataset artifact. Accepted human labels alone can extend training. Teacher suggestions and published-reference replay remain distinct. Encourage a discussion when participants disagree with the benchmark annotation.
-->

---

<div class="kicker">1:20</div>

# Break until 1:30

<p class="sub">Save the checkpoint. Your reviews and completed training stay with this notebook copy.</p><p class="aside">The support queue can survive ten minutes without being automatically forwarded.</p>

<!--
The break is ten minutes from elapsed 1:20 to 1:30. Ask people to leave the current page open. Restoring a saved checkpoint does not train or send model requests.
-->

---

<div class="kicker">1:30</div>

# A prompted model returns a typed decision

```json
{
  "intent": "card_arrival",
  "needs_review": false,
  "reason": "The customer asks about delivery."
}
```

<p>The validator checks allowed intents and real booleans. It cannot tell whether the chosen workflow fits the message.</p><p class="caption">Illustrative response. The notebook saves actual requests, provider settings, usage, and responses.</p>

<!--
Run only eight preselected development requests. This sample teaches model behavior and trace inspection; it is too small to rank against classifiers evaluated on 3,080 final cases. The provider is fixed and charged to the participant allowance.
-->

---
class: exercise
---

<div class="kicker">1:35</div>

# Inspect eight actual model routes



<p class="where">Notebook → Check the judge</p><ol><li>Click the routing button once.</li><li>Open a model span in Agent Lens and find the customer request and returned intent.</li><li>Compare one answer with the corresponding classifier output.</li></ol><div class="done"><strong>Run:</strong> Route eight development requests with the fixed model<br><strong>Check:</strong> Match the case ID and response to the saved provider receipt.</div>

<!--
Every request is durable and bounded. Each case gets a separate stage, so completed siblings can be reused after a failure. No test examples or accepted review labels enter the routing prompt.
-->

---

<div class="kicker">1:39</div>

# An automated failure tag needs its own evaluation

<div class="flow"><div>Request + route<small>What happened</small></div><b class="arrow">→</b><div>Judge rubric<small>Was this the wrong workflow?</small></div><b class="arrow">→</b><div>Compare with a person<small>False alarms and missed failures</small></div></div><p>A successful API call can return the wrong intent. A valid judgment can also disagree with your review.</p>

<!--
The notebook uses a model-based judge exercise. It is not silently creating native Agent Lens tags or pretending to generate Insights. Native tag alignment is an optional access-qualified extension. Prepared Insights require an independently verified cohort, not waiting live for new clusters.
-->

---
class: exercise
---

<div class="kicker">1:44</div>

# Implement the judge response check

<a class="answer-link" href="35">Worked answer ↗</a>

<p class="where">Notebook → Check the judge</p><ol><li>Complete <code>validate_judge</code>. Reject a string such as <code>"false"</code>.</li><li>Read the failure-tag instructions. Define what counts as unresolved rather than wrong.</li><li>Run the judge on up to eight reviewed cases.</li></ol><div class="done"><strong>Run:</strong> Check my judge validator → Compare the judge with up to eight of my reviews<br><strong>Check:</strong> Click Compare in EvalTables beside the judge result. Read the judge reason and your accepted review together; unavailable judgments stay blank.</div>

<!--
The human accepted intent stays out of the judge prompt. The judge receives the request and proposed route. Check one reason, even if the JSON passes. Missing judgments stay missing; do not score them as correct or incorrect.
-->

---

<div class="kicker">1:53</div>

# The judge disagreed with the dataset label

<div class="capture-layout"><div class="capture"><img src="/images/agent-lens-judge-detail.png" alt="Actual Agent Lens conversation: Can I activate a card in the app? Proposed intent activate_my_card; judge returned failed false."/><span class="capture-pin pin-request">1</span><span class="capture-pin pin-decision">2</span></div><div class="capture-notes"><p><b>1 · Request</b><br>“Can I activate a card in the app?”</p><p><b>2 · Judge</b><br><code>failed: false</code><br>“Request asks about activating a card, which matches the activate_my_card intent.”</p><p>The dataset says <code>card_linking</code>. Inspect the ambiguity before calling either side wrong.</p></div></div><p class="caption"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01">Open the actual conversation ↗</a> · Recorded development rehearsal. Three of four judge decisions matched the dataset reference; no human calibration is claimed.</p>

<!--
The screenshot is an authenticated native capture. Its JSON pane clips the end of the reason; the caption quotes the full saved response. Both the request and failed:false are visible. Twelve development-only requests completed, their stored spans were verified, and observed inference cost was $0.00113494. Eight routing requests were an instrumentation sample, not a quality benchmark. Human review is still necessary.
-->

---

<div class="kicker">1:55</div>

# Use reviewed data to run a new experiment

<div class="flow"><div>Accepted review<small>Human label and provenance</small></div><b class="arrow">→</b><div>Training dataset version<small>Original training + reviewed cases</small></div><b class="arrow">→</b><div>Revised classifier<small>Same frozen encoder</small></div></div><p>The test set does not enter this path. Use validation to decide whether to keep the revised model.</p>

<!--
The request review changes training data. It does not alter the encoder or hide difficult test examples. A review can be wrong, redundant, or too small to matter. Live improvement is measured, not scripted.
-->

---
class: exercise
---

<div class="kicker">2:00</div>

# Train with your accepted labels



<p class="where">Notebook → Improve the router</p><ol><li>Inspect the saved review dataset.</li><li>Train the classifier using those labels.</li><li>Compare validation errors with the earlier embedding classifier. Keep the earlier version if the revision does not help.</li></ol><div class="done"><strong>Run:</strong> Train a classifier with my reviewed examples<br><strong>Check:</strong> Explain one changed prediction and decide whether it supports your selection.</div>

<!--
This is the honest live experiment after the qualified representation improvement. Do not replace its result with the recorded gain. If labels disagree with the published annotation, inspect the text and the choice before attributing a score change to better data.
-->

---

<div class="kicker">2:15</div>

# Freeze what the final comparison will use

<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="Classifier weights, preprocessing, review threshold and source are frozen before final evaluation"><g fill="#e4e9dc" stroke="#96ad9e"><rect x="10" y="45" width="250" height="120"/><rect x="290" y="45" width="250" height="120"/><rect x="570" y="45" width="250" height="120"/><rect x="850" y="45" width="250" height="120"/></g><g style="font-size:26px"><text x="32" y="90">Classifier weights</text><text x="313" y="90">Preprocessing</text><text x="593" y="90">Review threshold</text><text x="873" y="90">Source + datasets</text></g><g style="font-size:19px"><text x="32" y="130">Exact saved file</text><text x="313" y="130">Vectorizer or encoder</text><text x="593" y="130">Your tested policy</text><text x="873" y="130">What produced them</text></g><path d="M10 205H1100" stroke="#237a6c" stroke-width="4"/><text x="360" y="250" style="font-size:26px">Then open the official test partition</text></svg>

<!--
The notebook records the selected training stage and model checksum. A policy is part of the release decision and must be fixed before seeing the final requests. After final evaluation, another choice is a separately labeled teaching retest.
-->

---
class: exercise
---

<div class="kicker">2:20</div>

# Evaluate all matching test requests



<p class="where">Notebook → Final comparison</p><ol><li>Choose the selected classifier and give a validation-based reason.</li><li>Freeze the classifier and review threshold.</li><li>Evaluate TF–IDF, embeddings, and your selected version on the same 3,080 messages.</li></ol><div class="done"><strong>Run:</strong> Freeze the classifier and review threshold → Evaluate the frozen versions on all 3,080 test requests<br><strong>Check:</strong> Compare macro-F1, per-intent errors, coverage, and latency separately.</div>

<!--
All final predictions are retained. The selected model may equal the existing embedding model; that is a valid keep decision, not an invented third improvement. Keep classifier quality separate from deferral policy.
-->

---

<div class="kicker">2:30</div>

# Compare the same requests in Forge

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo"><img src="/images/evaltables-native.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:6%;top:39%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:6%;top:70%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:6%;top:53%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Set the reference</b><br>Start with the word-based classifier.</p><p><b>2 · Read aligned outputs</b><br>Each version must show the same request.</p><p><b>3 · Separate review from quality</b><br>Deferring a request is a policy choice, not a corrected intent.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo">Open this comparison ↗</a></p>

<!--
Final evaluation publishes saved classifier predictions before the Report chapter. Click Compare in EvalTables. This is the native Weave-backed Evaluation Tables Preview in the W&B workspace. Aggregate macro-F1 remains computed from the whole prediction set; it is not the mean of row F1 scores.
-->

---

<div class="kicker">2:34</div>

# Read one routing decision

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo"><img src="/images/evaltables-native-detail.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:28.3%;top:25%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:28.3%;top:44%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:28.3%;top:40%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Read the request</b><br>The customer does not recognize an ATM withdrawal.</p><p><b>2 · Compare intents</b><br>Both classifiers choose the published intent on this case.</p><p><b>3 · Check confidence</b><br>The scores differ, but neither model sends this case for review.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo">Open this comparison ↗</a></p>

<!--
Use the saved case ID to match outputs. The automated judge comparison is separate and uses participant-reviewed development cases. Its target is agreement with those reviews, not classification accuracy on the official test set. The separate CES v2 service can remain unavailable while this Preview works.
-->

---
class: exercise
---

<div class="kicker">2:40</div>

# Write the decision you would make



<p class="where">Notebook → Explain the result</p><ol><li>State whether the revised classifier helped on the declared measure.</li><li>Describe one request that still needs a person.</li><li>Publish the saved comparison and your explanation.</li></ol><div class="done"><strong>Run:</strong> Publish my conclusion with the saved comparisons<br><strong>Check:</strong> A colleague can follow the reported score to the predictions, selected model, and reviewed data.</div>

<!--
Allow final ten minutes for pairs to explain one result. Publishing retries reuse saved executions. The report conclusion should be participant-authored. An improvement is welcome, but understanding a tie or regression completes the learning outcome.
-->

---

<div class="kicker">2:50</div>

# Reproduce the selected version before releasing it

<div class="flow"><div>Evaluation + decision<small>Why this version was selected</small></div><b class="arrow">→</b><div>Exact artifact<small>Code, preprocessing, weights</small></div><b class="arrow">→</b><div>Batch prediction<small>Reproduce a saved case</small></div></div><p>Optional: link the evaluated artifact to Registry, run a release check, and restore the previous version after a failed check.</p><p class="caption">Registry stores selected artifact versions. It does not automatically deploy an arbitrary model.</p>

<!--
The core ends with saved reproducible files and evaluation. Registry release and rollback is an advanced module with its own permissions. Specialist SFT changes model weights and needs a separate forecast and explicit launch; it is not required for this workshop.
-->

---

<div class="kicker">2:57</div>

# What to take back to your team

<p>Pick a real routing decision with a small, clear label set. Save the requests you reviewed, explain what a wrong route means, and compare the next version on cases you did not edit against.</p><p>Keep the human review cost visible. Sending every difficult case to a person can improve the reported selective accuracy while leaving the support team with more work.</p><p class="caption">Optional ARIA investigation: ask it to inspect one published disagreement and propose a regression case. Check the cited event before accepting its proposal.</p>

<!--
Close with a concrete transfer task. Ask each participant to name one queue, one failure, one measurable outcome, and one person who can review labels in their own workflow. No claims beyond the recorded Banking77 experiment.
-->

---
class: answer
name: classifier-answer
---

<div class="kicker">Reference</div>

# Worked answer: classifier head

```python
def make_classifier():
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(
        C=10, max_iter=1000, random_state=17
    )
```

<p>This function trains the head for both feature representations. It does not load or fine-tune the sentence encoder.</p><p class="answer-nav source-link"><a href="11">Return to the classifier exercise ↩</a></p>

<!--
Offer the answer only after an attempt or a hint request. Learners must still run the free check and both actual training calls.
-->

---
class: answer
name: policy-answer
---

<div class="kicker">Reference</div>

# Worked answer: review policy

```python
def needs_review(confidence, threshold):
    return confidence < threshold
```

<p>At 0.5, a 0.2 prediction is deferred. A 0.9 prediction is routed. Choosing a threshold remains a policy decision that should be checked on validation cases.</p><p class="answer-nav source-link"><a href="15">Return to the review exercise ↩</a></p>

<!--
The function should return a boolean. Exactly the threshold is routed in this specified policy. It is not a proof that the predicted probability is calibrated.
-->

---
class: answer
name: validator-answer
---

<div class="kicker">Reference</div>

# Worked answer: judge validator

```python
def validate_judge(value):
    if set(value) != {"failed", "reason"}:
        raise ValueError("Return failed and reason.")
    if type(value["failed"]) is not bool:
        raise ValueError("Use a boolean.")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("Give a reason.")
    return value
```

<p class="answer-nav source-link"><a href="22">Return to the judge exercise ↩</a></p>

<!--
The notebook worked answer also checks that value is a dictionary before reading its keys. Do not mistake passing this schema check for agreement with a human.
-->

---

<div class="kicker">Reference</div>

# Sources and recorded evidence

<ul><li><a href="https://github.com/PolyAI-LDN/task-specific-datasets">Banking77 data, splits, license, and citation</a></li><li><a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2">Frozen MiniLM encoder model card</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/examples/routing/qualification.json">Frozen qualification recipe</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/routing-workshop.md">Facilitator timing, results, and limitations</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_routing.py">Acquisition and feature preparation</a></li></ul>

<!--
All measured claims come from the saved qualification. The native comparison captures show the verified routing publication and link to that saved record. Until external-account and human rehearsals pass, label this a technical preview.
-->
