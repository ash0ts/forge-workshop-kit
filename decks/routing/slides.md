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

<div class="sub">Train a support router, review its errors, and test a revised version, then release and recover it using public banking requests.</div><div class="bottom-note">5½ hours · CPU classifiers · Agent Lens · W&B · Weave and EvalTables</div>

<!--
The support team is fictional. The messages are public Banking77 data. We will make a genuine measured classifier comparison, then let participants run an open-ended data review experiment. Do not promise that every personal review will improve the score.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: queue
---

<div class="kicker">0:02</div>

# The support queue needs a destination

<div class="two-col"><div class="ticket"><small>Request A</small>“Is there a way to know when my card will arrive?”</div><div class="ticket"><small>Request B</small>“I think my card is broken”</div></div><div v-click class="two-col"><div>Card delivery</div><div>Card troubleshooting</div></div><p class="caption">Actual examples in the dataset authors’ README. A fluent response does not tell us that the request reached the right workflow.</p>

<!--
Ask people what team should handle each request. These short examples explain the target before the model appears. We classify intent; we are not resolving accounts or giving financial advice. Source: PolyAI-LDN/task-specific-datasets.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: manager
---

<div class="kicker">0:04</div>

# A manager has offered to automate forwarding

<div class="quote">“If the system can write the whole email, surely it can pick a queue.”</div><div class="flow"><div>Message<small>What the customer wrote</small></div><b class="arrow">→</b><div>Routing decision<small>One intent, or human review</small></div><b class="arrow">→</b><div>Support workflow<small>Delivery, troubleshooting, disputed payment…</small></div></div>

<!--
This is fictional dialogue. The engineering problem is a constrained label choice. A wrong label wastes time even if the message is polite and the JSON validates. Keep the humor in the manager line, and the task literal.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: dataset
---

<div class="kicker">0:07</div>

# The dataset contains 77 banking intents

<div class="two-col"><div class="metric">10,003<small>Original training messages</small></div><div class="metric">3,080<small>Original test messages</small></div></div><p>Banking77 was published by PolyAI researchers with intent annotations. We preserve the official test split.</p><p class="caption">CC-BY-4.0 · Casanueva et al., 2020 · Dataset source and checksums travel with the workshop download.</p>

<!--
The data are public queries, not attendee customer records. There are 77 classes. The official test set contains 40 examples per class. One low-resource training class has only 35 examples, which is why we reserve ten validation and ten review cases per class rather than twenty each.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: partitions
---

<div class="kicker">0:10</div>

# Give each partition one job

<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="8463 train messages fit models,770 validation choose changes,770 review accept labels,3080 official test evaluate frozen versions"><rect x="0" y="30" width="330" height="135" fill="#d5e5d8"/><rect x="350" y="30" width="230" height="135" fill="#e6e5ce"/><rect x="600" y="30" width="230" height="135" fill="#e6e5ce"/><rect x="850" y="30" width="260" height="135" fill="#dfe3e0"/><text x="24" y="70" style="font-size:29px">8,463 train</text><text x="24" y="115" style="font-size:22px">Fit classifier weights</text><text x="372" y="70" style="font-size:29px">770 validation</text><text x="372" y="115" style="font-size:22px">Choose settings</text><text x="622" y="70" style="font-size:29px">770 review</text><text x="622" y="115" style="font-size:22px">Accept labels</text><text x="872" y="70" style="font-size:29px">3,080 test</text><text x="872" y="115" style="font-size:22px">Score frozen choices</text><path d="M20 190H820" stroke="#587a69" stroke-width="2"/><text x="225" y="230" style="font-size:23px">Derived from the authors’ training split</text><text x="872" y="230" style="font-size:23px">Official test split</text></svg>

<!--
The split order was fixed before any model score. Ten examples of every intent go to validation and ten to the review pool. The test partition is only opened after selection freezes. Files are public for teaching; the code keeps final cases out of model-editing and labeling prompts.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: connect
---

<div class="kicker">0:15</div>

# Open your copy and add your first trace



<p class="where">Notebook → Connect</p><ol><li>Copy the template into a writable project and open Edit.</li><li>Run stale cells to create the controls; exercise buttons stay unpressed.</li><li>In <code>instrument_tool</code>, add a descriptive span attribute.</li></ol><div class="done"><strong>Run:</strong> Connect and restore my work → Send my first Agent Lens trace<br><strong>Check:</strong> Find your attribute in the tool span.</div>

<!--
Let everyone open their own project. Hosted authentication is inherited; there is no shared gateway or host token. The $8 adjustable allowance covers fixed-model inference; CPU notebook charges are separate.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: trace
---

<div class="kicker">0:22</div>

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
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: read-request
---

<div class="kicker">0:26</div>

# Read a request before revealing its label



<p class="where">Notebook → Inspect requests</p><ol><li>Click Download and check Banking77.</li><li>Choose a request and explain the support workflow it needs.</li><li>Reveal the published label. Keep any disagreement as a question to inspect.</li></ol><div class="done"><strong>Run:</strong> Download and check Banking77<br><strong>Check:</strong> Identify a request where similar wording could lead to a different intent.</div>

<!--
Allow five minutes for individual predictions and partner discussion. The download includes 20 MB of cached features, original CSVs, license, and checksum manifest. Data loading sends no model call.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: words
---

<div class="kicker">0:36</div>

# Start with a word-based classifier

<div class="flow"><div>Request<small>“Where is my card?”</small></div><b class="arrow">→</b><div>TF–IDF<small>Word unigrams and bigrams</small></div><b class="arrow">→</b><div>Linear classifier<small>77 intent probabilities</small></div></div><p>TF–IDF gives distinctive words and phrases more weight. The classifier learns which combinations indicate each intent.</p><p class="caption">The text example illustrates the representation. The measured comparison uses the complete fixed partitions.</p>

<!--
Explain unigrams and bigrams with card and my card. Fit the vectorizer only on training messages so validation vocabulary does not alter the feature space. This is a standard, inexpensive baseline, not a deliberately broken model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: word-vector
---

<div class="kicker">0:39</div>

# Turn one request into words and adjacent pairs

<RoutingWalk kind="representation" :step="1" />

<!--
Read the real review-pool message aloud. The default tokenizer produces my, card, isn, here, yet; single-letter t is omitted. The diagram shows vocabulary positions, not invented TF–IDF weights. IDF and the vocabulary are fit on training text only.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: embeddings
---

<div class="kicker">0:46</div>

# Then change the representation

<div class="flow"><div>Request<small>Same messages and splits</small></div><b class="arrow">→</b><div>Frozen MiniLM<small>384 numbers per message</small></div><b class="arrow">→</b><div>Linear classifier<small>Same training recipe</small></div></div><p>The pretrained encoder gives semantically similar sentences nearby representations. Only the classifier’s weights train here.</p><p class="caption">all-MiniLM-L6-v2 · pinned revision · attention-masked mean pooling · L2 normalization</p>

<!--
Contrast sentence representation with lexical overlap. The cached encoder features are versioned and can be regenerated by the supplied preparation code. Cache lookup timing is not end-to-end encoder latency. The comparison changes representation, not data quantity or test cases.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: sentence-vector
---

<div class="kicker">0:49</div>

# Keep one vector for each request

<RoutingWalk kind="representation" :step="2" />

<!--
Compare the unchanged message with the different representation. Explain 384 as the encoder output size, not a count of hand-chosen keywords. The graphic is a schematic vector. Encoder weights stay frozen; no embedding geometry or semantic distances are fabricated.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: construct-head
---

<div class="kicker">0:52</div>

# Construct the estimator before fitting it

<RoutingWalk kind="fit" :step="1" />

<!--
Point to make_classifier: it returns an unfitted estimator. C is inverse regularization strength; changing it changes the training objective, not the number of output intents. max_iter limits optimization. Use the fixed recipe in the required path.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: fit-head
---

<div class="kicker">0:54</div>

# Fit the head on the labeled training rows

<RoutingWalk kind="fit" :step="2" />

<!--
The learner factory supplies the estimator in both branches. TF–IDF fits a vectorizer and head; the embedding branch fits the head on cached features. Both see the same 8,463 labels. The sparse vocabulary width and 384 embedding values are different input spaces.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: classifier-exercise
---

<div class="kicker">0:57</div>

# Implement the classifier head

<a class="answer-link" href="/66">Worked answer ↗</a>

<p class="where">Notebook → Train classifiers</p><ol><li>Complete <code>make_classifier</code> with <code>LogisticRegression(C=10, max_iter=1000, random_state=17)</code>.</li><li>Run the free practice check.</li><li>Train both representations using that same function.</li></ol><div class="done"><strong>Run:</strong> Train both classifiers on the same messages<br><strong>Check:</strong> Compare validation macro-F1 and open the saved source in Forge.</div>

<!--
The participant function is used in both actual fits. CPU training is bounded by iterations and two numerical-library threads. In preparation each fit took under four seconds with cached features; participant machines and hosting differ.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: predict-probabilities
---

<div class="kicker">1:08</div>

# A fitted classifier returns 77 probabilities

<RoutingWalk kind="fit" :step="3" />

<!--
After the exercise, locate predict_proba and classes_. Array position alone is not an intent label; the class order maps columns to names. Ask which files would be needed to predict after restarting.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: macro-f1
---

<div class="kicker">1:12</div>

# Macro-F1 gives each intent equal weight

<div class="two-col"><div><h2>Precision</h2><p>Of the requests sent to an intent, how many belonged there?</p><h2>Recall</h2><p>Of the requests that belonged there, how many did we find?</p></div><div><h2>F1 per intent</h2><p>The harmonic mean of that intent’s precision and recall.</p><h2>Macro-F1</h2><p>Average the 77 intent scores. Keep per-intent mistakes alongside it.</p></div></div>

<!--
Do not average row-wise F1 values. Macro-F1 is computed from the whole matched prediction set. Accuracy is also reported. Neither metric tells the whole operational story because review can defer some cases.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: intent-counts
---

<div class="kicker">1:15</div>

# Count the errors for one intent

<RoutingWalk kind="metrics" :step="1" />

<!--
These are the recorded embedding model’s official-test card_arrival predictions: 34 true positives, 3 false positives, 6 false negatives. Trace a misroute to the appropriate count. This example explains the metric; do not select a new model using these final examples.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: intent-average
---

<div class="kicker">1:18</div>

# Calculate F1, then average across intents

<RoutingWalk kind="metrics" :step="2" />

<!--
Compute precision 34/37 and recall 34/40. F1 is 68/77=0.883117 for this intent. The bars show all 77 saved intent F1s; their mean is the existing 0.920229 result. A per-case correct flag is a different measurement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: recorded-gain
---

<div class="kicker">1:22</div>

# The worked comparison reduced routing mistakes

<table class="clean-table"><tbody><tr><th>Fixed recipe</th><th>Test macro-F1</th><th>Accuracy</th></tr><tr><td>Word TF–IDF + classifier</td><td>0.879385</td><td>0.879545</td></tr><tr><td>Frozen MiniLM + classifier</td><td>0.920229</td><td>0.920779</td></tr></tbody></table><p>Embedding features improved macro-F1 by <strong>4.0844 percentage points</strong> on the same 3,080 test messages.</p><p class="caption">Recorded qualification, not your live result. Seeds 17, 29, 43 produced identical fits; this is one dataset split, not three independent studies.</p>

<!--
The fixed contract preceded final evaluation. Publish all six outcomes. Participants will inspect their own validation results first; the recorded result is a worked comparison and cannot be attributed to unexecuted learner edits. The deterministic seed repetitions check reproduction rather than uncertainty.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: deferral
---

<div class="kicker">1:35</div>

# A router can also ask a person

<div class="two-col"><div class="metric">Coverage<small>Fraction routed automatically</small></div><div class="metric">Selective accuracy<small>Accuracy among those routed requests</small></div></div><p>Raising the review threshold can improve selective accuracy while sending more work to people. That is a policy tradeoff, not a new classifier.</p><p class="caption">At threshold 0.5 in the recorded test: TF–IDF routes 75.84%; embeddings route 91.10%. Both are about 96% accurate among routed requests.</p>

<!--
Ask what happens if every request is deferred. Coverage becomes zero, selective accuracy is unavailable, and full classifier quality remains unchanged. The model probabilities are not calibrated guarantees.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: threshold-policy
---

<div class="kicker">1:38</div>

# Move the threshold without retraining

<RoutingWalk kind="policy" :step="1" />

<!--
Use the keyboard on the slider. The request and classifier probabilities stay unchanged. Coverage and selective accuracy recompute from the 770 saved validation predictions. At zero accepted cases, show unavailable rather than claiming perfect accuracy.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: review-margin
---

<div class="kicker">1:42</div>

# Choose labeling candidates by their top-two margin

<RoutingWalk kind="policy" :step="2" />

<!--
The displayed review-pool request has confidence 0.508052 and margin 0.180419. Confidence controls automatic deferral; margin ranks which examples to ask someone to label. These are distinct rules in predict and select_review.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: policy-exercise
---

<div class="kicker">1:45</div>

# Write the rule that sends a request to review

<a class="answer-link" href="/67">Worked answer ↗</a>

<p class="where">Notebook → Review requests</p><ol><li>Complete <code>needs_review(confidence, threshold)</code>.</li><li>Move the threshold and compare coverage with selective accuracy.</li><li>Pick a small-margin request and read both proposed intents.</li></ol><div class="done"><strong>Run:</strong> Check my review rule<br><strong>Check:</strong> Explain why a confidence of 0.2 at threshold 0.5 should go to a person.</div>

<!--
The function changes the displayed policy and the policy frozen for final evaluation. Its local check is free. Let people observe the coverage tradeoff rather than supply a preferred threshold.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: review-case
---

<div class="kicker">1:52</div>

# Read the disagreement before declaring failure

<RoutingCase />

<!--
These four examples are actual outputs from the training-derived review pool. The published annotation is a reference, not proof that every message is unambiguous. The first two were selected as disagreements with the dataset annotation; the last two agree with it. They are not human review records. Let learners explain disagreement in their own words.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: review-exercise
---

<div class="kicker">2:00</div>

# Save labels someone can trace back to a decision



<p class="where">Notebook → Review requests</p><ol><li>Review at least four requests, including a correct route and a mistake.</li><li>Select the accepted intent yourself and enter a reviewer name or alias.</li><li>Save each label; do not copy the model suggestion just because it is available.</li></ol><div class="done"><strong>Run:</strong> Save my reviewed label<br><strong>Check:</strong> The saved record contains case, proposal, accepted label, reviewer, and dataset version.</div>

<!--
Show the provenance fields in the dataset artifact. Accepted human labels alone can extend training. Teacher suggestions and published-reference replay remain distinct. Encourage a discussion when participants disagree with the benchmark annotation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: review-provenance
---

<div class="kicker">2:06</div>

# Keep the proposal and accepted label separate

<RoutingWalk kind="review" :step="1" />

<!--
Ask the participant to find all three labels for a case: model proposal, dataset reference, personal accepted label. Do not overwrite the proposal when accepting a correction. The record must preserve who made the decision and which data it belongs to.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: break-one
---

<div class="kicker">2:10</div>

# Take ten minutes. Return at 2:20.

<p class="sub">Save the checkpoint. Your reviews and completed training stay with this notebook copy.</p><p class="aside">The support queue can survive ten minutes without being automatically forwarded.</p>

<!--
Break from elapsed 2:10 to 2:20. Confirm the reviews and trained versions are saved. Reopening does not train or call a model.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: typed-route
---

<div class="kicker">2:20</div>

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
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: two-model-tasks
---

<div class="kicker">2:25</div>

# There are two different model exercises

<RoutingWalk kind="judge" :step="1" />

<!--
The first lane routes eight fixed validation requests. The second judges classifier proposals attached to human reviews. The judge does not consume the eight prompted routes. Both use actual provider calls and native spans; neither sample ranks models on the complete final dataset.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: prompted-exercise
---

<div class="kicker">2:31</div>

# Inspect eight actual model routes



<p class="where">Notebook → Check the judge</p><ol><li>Click the routing button once.</li><li>Open a model span in Agent Lens and find the customer request and returned intent.</li><li>Compare one answer with the corresponding classifier output.</li></ol><div class="done"><strong>Run:</strong> Route eight development requests with the fixed model<br><strong>Check:</strong> Match the case ID and response to the saved provider receipt.</div>

<!--
Every request is durable and bounded. Each case gets a separate stage, so completed siblings can be reused after a failure. No test examples or accepted review labels enter the routing prompt.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: judge-purpose
---

<div class="kicker">2:40</div>

# Check the model-based judge against your reviews

<div class="flow"><div>Request + route<small>What happened</small></div><b class="arrow">→</b><div>Judge rubric<small>Was this the wrong workflow?</small></div><b class="arrow">→</b><div>Compare with a person<small>False alarms and missed failures</small></div></div><p>A successful API call can return the wrong intent. A valid judgment can also disagree with your review.</p>

<!--
The notebook uses a model-based judge exercise. It is not silently creating native Agent Lens tags or pretending to generate Insights. Native tag alignment is an optional access-qualified extension. Prepared Insights require an independently verified cohort, not waiting live for new clusters.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: judge-evidence
---

<div class="kicker">2:44</div>

# Keep the accepted label out of the judge prompt

<RoutingWalk kind="judge" :step="2" />

<!--
Show the user message fields in the actual notebook. The accepted label is used afterward to calculate human failure labels, not supplied to the judge. Contrast a malformed response, a valid disagreement and an unavailable request. This exercise is not an automatic native Insights cluster or tag.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: validator-exercise
---

<div class="kicker">2:50</div>

# Implement the judge response check

<a class="answer-link" href="/68">Worked answer ↗</a>

<p class="where">Notebook → Check the judge</p><ol><li>Complete <code>validate_judge</code>. Reject a string such as <code>"false"</code>.</li><li>Read the failure-tag instructions. Define what counts as unresolved rather than wrong.</li><li>Run the judge on up to eight reviewed cases.</li></ol><div class="done"><strong>Run:</strong> Check my judge validator → Compare the judge with up to eight of my reviews<br><strong>Check:</strong> Click Compare in EvalTables beside the judge result. Read the judge reason and your accepted review together; unavailable judgments stay blank.</div>

<!--
The human accepted intent stays out of the judge prompt. The judge receives the request and proposed route. Check one reason, even if the JSON passes. Missing judgments stay missing; do not score them as correct or incorrect.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: recorded-judge
---

<div class="kicker">3:03</div>

# The judge disagreed with the dataset label

<div class="capture-layout"><div class="capture"><img src="/images/agent-lens-judge-detail.png" alt="Actual Agent Lens conversation: Can I activate a card in the app? Proposed intent activate_my_card; judge returned failed false."/><span class="capture-pin pin-request">1</span><span class="capture-pin pin-decision">2</span></div><div class="capture-notes"><p><b>1 · Request</b><br>“Can I activate a card in the app?”</p><p><b>2 · Judge</b><br><code>failed: false</code><br>“Request asks about activating a card, which matches the activate_my_card intent.”</p><p>The dataset says <code>card_linking</code>. Inspect the ambiguity before calling either side wrong.</p></div></div><p class="caption"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01">Open the actual conversation ↗</a> · Recorded development rehearsal. Three of four judge decisions matched the dataset reference; no human calibration is claimed.</p>

<!--
The screenshot is an authenticated native capture. Its JSON pane clips the end of the reason; the caption quotes the full saved response. Both the request and failed:false are visible. Twelve development-only requests completed, their stored spans were verified, and observed inference cost was $0.00113494. Eight routing requests were an instrumentation sample, not a quality benchmark. Human review is still necessary.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: review-dataset
---

<div class="kicker">3:10</div>

# Use reviewed data to run a new experiment

<div class="flow"><div>Accepted review<small>Human label and provenance</small></div><b class="arrow">→</b><div>Training dataset version<small>Original training + reviewed cases</small></div><b class="arrow">→</b><div>Revised classifier<small>Same frozen encoder</small></div></div><p>The test set does not enter this path. Use validation to decide whether to keep the revised model.</p>

<!--
The request review changes training data. It does not alter the encoder or hide difficult test examples. A review can be wrong, redundant, or too small to matter. Live improvement is measured, not scripted.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: accepted-training
---

<div class="kicker">3:14</div>

# Refit the head with your accepted labels

<RoutingWalk kind="review" :step="2" />

<!--
Only unique review-pool cases with label_source=human_review and verified=true may extend training. The fixed encoder and original training rows stay. Extra labels can be useful, redundant or wrong; compare validation before selecting a version.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: retrain-exercise
---

<div class="kicker">3:18</div>

# Train with your accepted labels



<p class="where">Notebook → Improve the router</p><ol><li>Inspect the saved review dataset.</li><li>Train the classifier using those labels.</li><li>Compare validation errors with the earlier embedding classifier. Keep the earlier version if the revision does not help.</li></ol><div class="done"><strong>Run:</strong> Train a classifier with my reviewed examples<br><strong>Check:</strong> Explain one changed prediction and decide whether it supports your selection.</div>

<!--
This is the honest live experiment after the qualified representation improvement. Do not replace its result with the recorded gain. If labels disagree with the published annotation, inspect the text and the choice before attributing a score change to better data.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: break-two
---

<div class="kicker">3:30</div>

# Take ten minutes. Return at 3:40.

<p class="sub">Save the revised classifier and your validation-based choice.</p><p class="aside">No tickets will be forwarded while you are away.</p>

<!--
Break from elapsed 3:30 to 3:40. Keep the final test closed. On return, freeze the version and policy you chose from validation.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/routing_cells.py.
-->

---
name: freeze
---

<div class="kicker">3:40</div>

# Freeze what the final comparison will use

<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="Classifier weights, preprocessing, review threshold and source are frozen before final evaluation"><g fill="#e4e9dc" stroke="#96ad9e"><rect x="10" y="45" width="250" height="120"/><rect x="290" y="45" width="250" height="120"/><rect x="570" y="45" width="250" height="120"/><rect x="850" y="45" width="250" height="120"/></g><g style="font-size:26px"><text x="32" y="90">Classifier weights</text><text x="313" y="90">Preprocessing</text><text x="593" y="90">Review threshold</text><text x="873" y="90">Source + datasets</text></g><g style="font-size:19px"><text x="32" y="130">Exact saved file</text><text x="313" y="130">Vectorizer or encoder</text><text x="593" y="130">Your tested policy</text><text x="873" y="130">What produced them</text></g><path d="M10 205H1100" stroke="#237a6c" stroke-width="4"/><text x="360" y="250" style="font-size:26px">Then open the official test partition</text></svg>

<!--
The notebook records the selected training stage and model checksum. A policy is part of the release decision and must be fixed before seeing the final requests. After final evaluation, another choice is a separately labeled teaching retest.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: freeze-files
---

<div class="kicker">3:42</div>

# Save the transformations with the weights

<RoutingWalk kind="freeze" :step="1" />

<!--
Have someone name the missing component if only coefficients are saved. TF–IDF needs its fitted vectorizer; the embedding model needs the encoder identity and preprocessing. The review policy also changes what users see.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: exercise
name: final-exercise
---

<div class="kicker">3:45</div>

# Evaluate all matching test requests



<p class="where">Notebook → Final comparison</p><ol><li>Choose the selected classifier and give a validation-based reason.</li><li>Freeze the classifier and review threshold.</li><li>Evaluate TF–IDF, embeddings, and your selected version on the same 3,080 messages.</li></ol><div class="done"><strong>Run:</strong> Freeze the classifier and review threshold → Evaluate the frozen versions on all 3,080 test requests<br><strong>Check:</strong> Compare macro-F1, per-intent errors, coverage, and latency separately.</div>

<!--
All final predictions are retained. The selected model may equal the existing embedding model; that is a valid keep decision, not an invented third improvement. Keep classifier quality separate from deferral policy.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: aligned-requests
---

<div class="kicker">3:48</div>

# Compare matching requests, then the operating policy

<RoutingWalk kind="freeze" :step="2" />

<!--
First compare intent predictions across versions on all 3,080 requests. Then compare how many were automatically routed under the chosen policy. A selected version may be the same saved embedding model. Reusing it is a keep decision, not another improvement.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: native-comparison
---

<div class="kicker">3:50</div>

# Compare the same requests in Forge

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo"><img src="/images/evaltables-native.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:6%;top:39%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:6%;top:70%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:6%;top:53%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Set the reference</b><br>Start with the word-based classifier.</p><p><b>2 · Read aligned outputs</b><br>Each version must show the same request.</p><p><b>3 · Separate review from quality</b><br>Deferring a request is a policy choice, not a corrected intent.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo">Open this comparison ↗</a></p>

<!--
Final evaluation publishes saved classifier predictions before the Report chapter. Click Compare in EvalTables. This is the native Weave-backed Evaluation Tables Preview in the W&B workspace. Aggregate macro-F1 remains computed from the whole prediction set; it is not the mean of row F1 scores.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: native-row
---

<div class="kicker">3:52</div>

# Read one routing decision

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo"><img src="/images/evaltables-native-detail.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:28.3%;top:25%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:28.3%;top:44%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:28.3%;top:40%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Read the request</b><br>The customer does not recognize an ATM withdrawal.</p><p><b>2 · Compare intents</b><br>Both classifiers choose the published intent on this case.</p><p><b>3 · Check confidence</b><br>The scores differ, but neither model sends this case for review.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=fthby6owcpo">Open this comparison ↗</a></p>

<!--
Use the saved case ID to match outputs. The automated judge comparison is separate and uses participant-reviewed development cases. Its target is agreement with those reviews, not classification accuracy on the official test set. The separate CES v2 service can remain unavailable while this Preview works.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
name: release-break
---

<div class="kicker">3:55</div>

# Take ten minutes. Return at 4:05.

<p class="sub">Your classifier is selected. After the break, we will load its saved files and check that it still routes requests the same way.</p><p class="aside">The support team has asked whether “saved somewhere” counts as released.</p>

<!--
Break from 3:55 to 4:05. Existing official-test results are complete; do not tune against them during the release lab.
-->

---
name: release-request
---

<div class="kicker">4:05</div>

# The classifier works. Can another process use it?

<div class="quote">“Please put the chosen version into the batch router. The queues are already there.”</div><div class="flow"><div>Selected experiment<small>Known predictions</small></div><b class="arrow">→</b><div>Saved release<small>Exact files and metadata</small></div><b class="arrow">→</b><div>Reloaded predictor<small>Do the destinations still match?</small></div></div><p class="caption">We will introduce a loader defect deliberately. This is a release drill, not a newly discovered model failure.</p>

<!--
The scenario changes from model selection to delivery. The model weights stay fixed. Participants will see how an integration defect can invalidate an otherwise useful model. Explain the fault in advance; do not stage it as an organic discovery.
-->

---
name: release-bundle
---

<div class="kicker">4:08</div>

# Save what the predictor needs, then reload it

<ReleaseWalk kind="bundle" />

<!--
The artifact contains classifier, feature representation identity, intent order, review policy, source, checks, and fixed case IDs. The source sequence is abbreviated. An exact artifact version permits reproduction; a mutable latest alias does not identify what ran. Never unpickle arbitrary downloaded models; use the artifact just created in the participant project.
-->

---
class: exercise
name: release-prepare-exercise
---

<div class="kicker">4:11</div>

# Load your selected version from its artifact



<p class="where">Notebook → Release and recover</p><ol><li>Click <b>Prepare the selected router for release</b>. Inspect the files it saves.</li><li>Click <b>Publish and reload the exact release artifact</b>. Copy its exact version into your notes.</li><li>Compare the reloaded predictions with the intact saved release.</li></ol><div class="done"><strong>Run:</strong> Prepare the selected router for release → Publish and reload the exact release artifact<br><strong>Check:</strong> Prediction parity passes without fitting another classifier.</div>

<!--
Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.
-->

---
name: release-cohort
---

<div class="kicker">4:17</div>

# Choose the regression cases before predicting

<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="The existing 770-example review pool supplies one case per intent. Lexically first case IDs define 77 fixed regression cases. The official test set is unchanged."><rect x="0" y="45" width="300" height="115" fill="#e5e9dc"/><text x="22" y="86" style="font-size:28px">770 review requests</text><text x="22" y="128" style="font-size:21px">Training-derived pool</text><path d="M315 105H390" stroke="#718a7c" stroke-width="3"/><rect x="405" y="45" width="300" height="115" fill="#d3e6dc"/><text x="427" y="86" style="font-size:28px">One per intent</text><text x="427" y="128" style="font-size:21px">First case ID, sorted</text><path d="M720 105H795" stroke="#718a7c" stroke-width="3"/><rect x="810" y="45" width="300" height="115" fill="#d3e6dc"/><text x="832" y="86" style="font-size:28px">77 fixed cases</text><text x="832" y="128" style="font-size:21px">Same batch, each release</text><text x="0" y="230" style="font-size:24px">Regression and reproduction check: not a new independent test set.</text></svg>

<!--
The cohort is selected and saved before predictions, using the lexical first review-pool case per intent. Some reviewed cases may have been accepted into training. This batch tests release behavior, not generalization. The original 3,080 official test predictions remain unchanged.
-->

---
name: release-columns
---

<div class="kicker">4:20</div>

# A probability belongs to a specific intent

<ReleaseWalk kind="mapping" :step="1" />

<!--
Illustrative three-column values; the real model has 77 intent columns. Trace column 1 from 0.84 to card_not_working using model.classes_. The message and probabilities are explanatory, not a recorded participant output.
-->

---
name: release-fault
---

<div class="kicker">4:22</div>

# Rotated labels send column 1 to another queue

<ReleaseWalk kind="mapping" :step="2" />

<!--
The deliberately faulty loader rotates the names by one position. Column1 still contains 0.84 but now names cash_withdrawal_not_recognised. Valid output and high confidence do not establish a correct destination. Participants inspect actual 77-class predictions in the next exercise.
-->

---
class: exercise
name: release-incident-exercise
---

<div class="kicker">4:26</div>

# Find one request sent to the wrong queue



<p class="where">Notebook → Release and recover</p><ol><li>Run the faulty loader on the fixed batch.</li><li>Open its Agent Lens operation and compare the loaded label order with the saved model classes.</li><li>Choose a changed route. Record its case, proposed intent, accepted label, and your reason.</li></ol><div class="done"><strong>Run:</strong> Run the deliberately faulty release<br><strong>Check:</strong> The weights and confidence are unchanged; the returned intent moves.</div>

<!--
Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.
-->

---
name: release-set-check
---

<div class="kicker">4:33</div>

# Checking the label set misses this defect

<ReleaseWalk kind="checks" :step="1" />

<!--
All expected names are still present. A set comparison discards order, precisely the part that links probability columns to intents. Ask learners which extra check would detect the fault.
-->

---
name: release-order-check
---

<div class="kicker">4:35</div>

# Check order before accepting the loaded model

<ReleaseWalk kind="checks" :step="2" />

<!--
Implement both exact order and set checks. Do not sort labels as the repair: a classifier may use another class order. The free fixture intentionally uses a nonalphabetical order.
-->

---
class: exercise
name: release-repair-exercise
---

<div class="kicker">4:40</div>

# Repair the loader and write its regression check

<a class="answer-link" href="/69">Worked answer ↗</a>

<p class="where">Notebook → Release and recover</p><ol><li>Complete <code>label_names(model_classes)</code> by preserving the supplied order.</li><li>Complete <code>check_release(model_classes, loaded_labels)</code>. Check the label set and exact order.</li><li>Run the free check, then execute your repaired loader on the same 77 requests.</li></ol><div class="done"><strong>Run:</strong> Check my release and repair code → Run my repaired loader on the same requests<br><strong>Check:</strong> Order and prediction parity pass. Existing classifier mistakes may remain.</div>

<!--
Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.
-->

---
name: release-parity
---

<div class="kicker">4:50</div>

# A repaired loader should reproduce the intact release

<ReleaseWalk kind="checks" :step="3" />

<!--
Compare the healthy, faulty and repaired outputs by case ID. Parity with the intact release establishes recovery from this drill. Macro-F1 still measures agreement with labels. A model can reproduce its own mistakes perfectly. Keep those two claims separate.
-->

---
name: release-investigate
---

<div class="kicker">4:56</div>

# Compare three versions of the same request

<table class="clean-table small-table"><thead><tr><th>Version</th><th>What to inspect</th><th>Question</th></tr></thead><tbody><tr><td>Intact release</td><td>Saved intent + confidence</td><td>What did the selected version return?</td></tr><tr><td>Faulty loader</td><td>Same probabilities, rotated names</td><td>Which destination changed?</td></tr><tr><td>Your repair</td><td>Restored mapping + regression check</td><td>Did the prediction return to its original value?</td></tr></tbody></table><p class="release-evidence">Open the notebook’s saved comparison in EvalTables. Then follow one changed case to its batch trace and exact artifact.</p><p class="caption">No fabricated result is shown here. Use your actual saved rows; publication status is separate from execution.</p>

<!--
This is an investigation guide rather than a product screenshot. Use native links from the release result. If publication is unavailable, inspect the notebook comparison and retry publication only. Do not rerun the batch to fix an export error.
-->

---
class: exercise
name: release-decision-exercise
---

<div class="kicker">5:00</div>

# Decide whether this release passes its checks



<p class="where">Notebook → Release and recover</p><ol><li>Review label order, set membership, and prediction parity.</li><li>Select release or reject and explain the choice. A failed check cannot be approved as a passing release.</li><li>Save the exact artifact and comparison alongside your decision.</li></ol><div class="done"><strong>Run:</strong> Save my release decision<br><strong>Check:</strong> The decision names the tested artifact and its checks.</div>

<!--
Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.
-->

---
name: release-rollback
---

<div class="kicker">5:08</div>

# Rollback reloads a version; it does not undo training

<div class="flow"><div>Previous intact artifact<small>Exact version remains available</small></div><b class="arrow">→</b><div>Fresh restore folder<small>Load saved model and metadata</small></div><b class="arrow">→</b><div>Same request batch<small>Verify the original predictions</small></div></div><p>You are switching the batch predictor’s selected files. No new fit and no model-weight reversal are needed.</p><p class="caption">Registry can organize approved versions. It does not deploy this Python predictor automatically.</p>

<!--
Require an explicit rollback action. Preserve the faulty release and its evidence for diagnosis rather than deleting it. The required path uses Artifacts in the participant project; Registry permissions are optional.
-->

---
class: exercise
name: release-rollback-exercise
---

<div class="kicker">5:12</div>

# Restore the previous version and verify it



<p class="where">Notebook → Release and recover</p><ol><li>Click the restore control. Confirm it loads the previously recorded exact artifact.</li><li>Run its fixed batch and check parity with the intact release.</li><li>Explain which defect the rollback removed and which classifier errors it cannot fix.</li></ol><div class="done"><strong>Run:</strong> Restore the previous release and verify its predictions<br><strong>Check:</strong> Restored predictions match the saved intact version.</div>

<!--
Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.
-->

---
name: release-conclusion
---

<div class="kicker">5:20</div>

# Separate the model gain from the release repair

<div class="two-col"><div><h2>Model comparison</h2><p>Did a different representation or accepted training data improve routing on the official test set?</p></div><div><h2>Release drill</h2><p>Did the repaired loader reproduce the selected model’s destinations on the fixed regression batch?</p></div></div><p class="caption">The first measures a classifier change. The second verifies recovery from a known implementation defect.</p>

<!--
Have participants explain both results without merging denominators or calling the drill a new benchmark. Preserve original 3,080-test predictions; the 77-case capstone cohort is reused and may overlap reviewed training additions. Keep remaining genuine classifier errors in the conclusion.
-->

---
class: exercise
name: report-exercise
---

<div class="kicker">5:25</div>

# Write the decision you would make



<p class="where">Notebook → Explain the result</p><ol><li>Separate the official-test classifier result from the controlled release repair.</li><li>Describe a remaining routing mistake and the regression check you added.</li><li>Publish the saved comparison and your explanation.</li></ol><div class="done"><strong>Run:</strong> Publish my conclusion with the saved comparisons<br><strong>Check:</strong> A colleague can follow the reported score to the predictions, selected model, and reviewed data.</div>

<!--
Final five minutes: explain the classifier comparison and the release drill separately. Include the tested artifact, decision, rollback evidence, and remaining errors. Publication reuses saved work.
-->

---
name: release
---

<div class="kicker">5:28</div>

# Optional: organize approved versions in Registry

<p>Link the exact evaluated artifact to Registry if your project has permission. Keep the checks, previous version, and release decision alongside it.</p><p>ARIA can investigate the saved incident where access permits. Verify its cited event before accepting a proposed next test.</p><p class="caption">These are optional. Your batch predictor and Artifact-based rollback already work without Registry or ARIA.</p>

<!--
Registry manages versions, not automatic deployment. ARIA access and usage are separate; it cannot approve a repair automatically. The core capstone contains no new inference calls or training. Specialist fine-tuning remains a separately qualified future lesson.
-->

---
name: close
---

<div class="kicker">5:29</div>

# What to take back to your team

<p>Pick a real routing decision with a small, clear label set. Save the requests you reviewed, explain what a wrong route means, and compare the next version on cases you did not edit against.</p><p>Keep the human review cost visible. Sending every difficult case to a person can improve the reported selective accuracy while leaving the support team with more work.</p><p class="caption">Optional ARIA investigation: ask it to inspect one published disagreement and propose a regression case. Check the cited event before accepting its proposal.</p>

<!--
Close with a concrete transfer task. Ask each participant to name one queue, one failure, one measurable outcome, and one person who can review labels in their own workflow. No claims beyond the recorded Banking77 experiment.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
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

<p>This function constructs the head. The later fit call trains it for both feature representations. It does not load or fine-tune the sentence encoder.</p><p class="answer-nav source-link"><a href="/15">Return to the classifier exercise ↩</a></p>

<!--
Offer the answer only after an attempt or a hint request. Learners must still run the free check and both actual training calls.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
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

<p>At 0.5, a 0.2 prediction is deferred. A 0.9 prediction is routed. Choosing a threshold remains a policy decision that should be checked on validation cases.</p><p class="answer-nav source-link"><a href="/24">Return to the review exercise ↩</a></p>

<!--
The function should return a boolean. Exactly the threshold is routed in this specified policy. It is not a proof that the predicted probability is calibrated.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: answer
name: validator-answer
---

<div class="kicker">Reference</div>

# Worked answer: judge validator

```python
def validate_judge(value):
    if not isinstance(value, dict) or set(value) != {"failed", "reason"}:
        raise ValueError("Return failed and reason.")
    if type(value["failed"]) is not bool:
        raise ValueError("Use a boolean.")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("Give a reason.")
    return value
```

<p class="answer-nav source-link"><a href="/34">Return to the judge exercise ↩</a></p>

<!--
This uses the same type guard as the notebook. Valid JSON is only a response contract; it does not establish agreement with a reviewer.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->

---
class: answer
name: release-repair-answer
---

<div class="kicker">Reference</div>

# Worked answer: preserve the probability-column order

```python
def label_names(model_classes):
    return list(model_classes)

def check_release(model_classes, loaded_labels):
    expected = list(model_classes)
    loaded = list(loaded_labels)
    return {
        "label_set": set(loaded) == set(expected),
        "label_order": loaded == expected,
    }
```

<p class="answer-nav source-link"><a href="/56">Return to the release repair exercise ↩</a></p>

<!--
This checks the metadata contract; the subsequent saved batch checks prediction parity independently. Passing both checks does not prove every route is correct. Give the worked answer after an attempt or explicit request.
-->

---
name: sources
---

<div class="kicker">Reference</div>

# Sources and recorded evidence

<ul><li><a href="https://github.com/PolyAI-LDN/task-specific-datasets">Banking77 data, splits, license, and citation</a></li><li><a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2">Frozen MiniLM encoder model card</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/examples/routing/qualification.json">Frozen qualification recipe</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/routing-workshop.md">Facilitator timing, results, and limitations</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_routing.py">Acquisition and feature preparation</a></li></ul>

<!--
All measured claims come from the saved qualification. The native comparison captures show the verified routing publication and link to that saved record. Until external-account and human rehearsals pass, label this a technical preview.
Teaching source: https://github.com/ash0ts/forge-workshop-kit/blob/main/src/forge_workshop_kit/routing.py.
-->
