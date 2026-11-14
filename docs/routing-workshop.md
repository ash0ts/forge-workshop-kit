# Route customer requests and learn from mistakes

A fictional banking support team needs to send each request to the right workflow. A card that has not arrived needs a different response from a card that does not work. Participants build the router, investigate its mistakes, label a few examples, and decide which requests should go to a person.

The data are real public support queries from [Banking77](https://github.com/PolyAI-LDN/task-specific-datasets), published by Casanueva and colleagues under CC-BY-4.0. This is an intent-routing exercise, not financial advice, fraud detection, or a system for taking action on accounts.

## Three-hour session

| Time | Participants change | Check before moving on |
|---|---|---|
| 0–15 | Copy the notebook into their project, add a tracing attribute, send a setup trace | Find the attribute in their own Agent Lens tool span |
| 15–30 | Inspect requests and predict labels before revealing them | Explain why card arrival and card not working need different workflows |
| 30–55 | Implement the linear classifier factory and train TF–IDF and frozen-embedding versions | Compare validation macro-F1, saved source, and runtime |
| 55–80 | Implement the review threshold, inspect uncertain requests, save at least four human labels | Identify a correct route and a mistake; separate coverage from accuracy |
| 80–90 | Break | Checkpoint is saved |
| 90–115 | Run eight typed model routes; write a judge validator and examine its rubric | Read an actual model request and compare judge decisions with personal reviews |
| 115–140 | Add reviewed examples to training and retrain | Compare validation results; improvement is not assumed |
| 140–160 | Freeze a classifier and threshold, evaluate the official test set | Compare all 3,080 matching requests and inspect per-intent mistakes |
| 160–180 | Publish the selected model, review dataset, comparison, and Report | Explain one result and reproduce it from saved artifacts |

Run labels and code checks are literal. The notebook's occasional support-desk humor does not replace an instruction or a failure message.

## Dataset and fixed worked example

The prepared download contains the authors' original CSV files, their license, assigned splits, cached embeddings, and checksums. Its source revision is `57ec275d8078af65b7731c2a98be812d844a6d6b`.

The official 10,003 training messages are partitioned by a fixed hash order within intent using seed 20261114. Ten examples per intent form validation and ten form a review pool. The remaining 8,463 examples train the classifiers. The original 3,080-example official test set is unchanged. Twenty validation and review examples per intent were considered before training, but the smallest class had only 35 training examples; the published ten-and-ten split preserves examples for every class.

Both classifiers use logistic regression with C=10 and at most 1,000 iterations. TF–IDF uses word unigrams and bigrams with sublinear term frequency. The second classifier uses attention-masked mean pooling and L2-normalized vectors from the frozen [all-MiniLM-L6-v2 encoder](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), pinned to `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. The encoder's weights do not change. Preparation code is in `scripts/prepare_routing.py`; the exact recipe was frozen in `examples/routing/qualification.json` before final evaluation.

## What qualification showed

| Version | Final macro-F1 | Accuracy | Automatically routed at 0.5 | Accuracy among routed requests |
|---|---:|---:|---:|---:|
| Word TF–IDF classifier | 0.879385 | 0.879545 | 75.84% | 96.06% |
| Frozen sentence embeddings + classifier | 0.920229 | 0.920779 | 91.10% | 96.15% |

The embedding classifier improved macro-F1 by **4.0844 percentage points** on these 3,080 requests. Predetermined seeds 17, 29, and 43 produced identical predictions because this fitting procedure is deterministic. They check reproducibility; they are not three independent datasets or an uncertainty interval. All six outcomes and per-case predictions are retained in `evidence/routing-qualification-20261114`.

Local CPU encoding took 23.16 seconds. Each classifier fit took approximately 0.3 seconds with cached embeddings and 3.3–3.7 seconds with TF–IDF on the preparation machine, using two numerical-library threads. Cache lookup latency omits the encoder forward pass; do not present the cached classifier timing as end-to-end production latency. Preparation used no paid inference. Participant notebook compute and the explicitly launched routing and judge calls are separate costs.

The confidence value is a classifier probability, not a calibrated promise of correctness. The threshold exercise reports both how many requests are routed and how often those routed requests are right. Deferring a request does not make the classifier's underlying prediction correct.

## Reviewed data and judge calibration

The review pool belongs to the original training partition. The notebook selects up to 50 small-margin predictions, then asks the participant to accept a label explicitly. Each review retains the case, suggested label, accepted label, reviewer, dataset version, and supporting evidence. Only verified human review records can extend the training data. A model-proposed or unverified label cannot silently become accepted training data.

`examples/routing/recorded-review.json` contains two recorded disagreements and two agreements with the dataset annotation from that pool. Their reference labels come from the published dataset. They are a teaching fallback, not attendee reviews and not a claim that human review has occurred.

The automated judge receives the request, proposed intent, and rubric. It does not receive the participant's accepted label or final-test examples. We compare its failure decision with the participant's decision separately. A malformed or unavailable judgment remains unavailable. Before freezing the classifier, participants must run this comparison on their saved reviews. The notebook saves the attempt even if the provider is unavailable, so missing judgments do not prevent completing the workshop. Routing eight requests alone does not complete the judge exercise. Native Agent Lens tag alignment and automatic Insights need a separate successful account/access rehearsal; this notebook's model-based judge comparison does not pretend to create native tags or clusters.

## Saving and recovery

Training and model calls require explicit buttons. Completed stage results, model files, checksums, human reviews, and provider receipts are saved locally and in checkpoint artifacts. Resume never trains again merely because a notebook opened. Trace or evaluation publication can be retried from saved outputs. A stopped execution needs an explicit retry decision; ambiguous provider calls retain their reservation.

The comparison publishes structured intent, confidence, and review fields to W&B, Weave, and native EvalTables. If native publication is unavailable, the notebook comparison and saved Weave records remain usable. Treat native availability as unverified until a successful live readback.

A fresh external-account run and a participant usability rehearsal remain release checks. CPU qualification establishes the worked classifier difference; it does not establish those product-access checks.

## Live routing and judge rehearsal

Twelve development-only model requests completed in the maintainer account: eight routing calls and four judgments. Every exported conversation passed stored-span readback. Observed inference cost was **$0.00113494**, with no bounded unknown cost or in-flight reservation remaining. The eight routing requests were chosen by fixed case ordering for an instrumentation check; they all concern card arrival and are not a quality benchmark.

Three of the four judge decisions matched the published dataset reference. This is not human calibration. For “Can I activate a card in the app?”, the classifier proposed `activate_my_card` and the judge agreed; the dataset label is `card_linking`. The text is ambiguous enough to warrant inspection instead of treating the reference label as infallible. [Open the recorded conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01).

The complete requests, costs, and verified trace identities are in `evidence/routing-live-v050.json`. The native capture in the deck preserves the actual question and judgment; its adjacent caption quotes the saved reason where the product's JSON pane clips the line.

The isolated browser check exercised the actual classifier editor, two CPU fits, a clearly labeled test-only review, retraining, freezing, all three 3,080-row final comparisons, and the publication controls. Provider and publication calls were disabled in that UI test. No browser errors or model calls occurred. This checks the interface separately from the live request/trace rehearsal; it is not an external attendee or human usability result.

A separate browser check verified the final prerequisite: freezing is disabled before a judge-comparison attempt and enabled after an attempted comparison with an explicitly unavailable judgment. That test disabled inference and publication; it verified the recovery path, not judge quality. Its record is `evidence/routing-judge-prerequisite-v050.json`.
