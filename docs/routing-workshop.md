# Route customer requests and learn from mistakes

A fictional banking support team needs to send each request to the right workflow. A card that has not arrived needs a different response from a card that does not work. Participants build the router, investigate its mistakes, label a few examples, and decide which requests should go to a person.

The data are real public support queries from [Banking77](https://github.com/PolyAI-LDN/task-specific-datasets), published by Casanueva and colleagues under CC-BY-4.0. This is an intent-routing exercise, not financial advice, fraud detection, or a system for taking action on accounts.

## Five-and-a-half-hour session

The deck pauses at each transformation before the participant writes or runs it. One request stays visible while it becomes features, probabilities, a review decision, and a saved training example. The extra time is for explanation and practice; the experiment still uses the same cases, models and inference allowance.

| Time | Participants change or investigate | Check before moving on |
|---|---|---|
| 0–30 | Guess the bundled development request’s intent before connecting; inspect partitions and send a setup trace | Explain the expected route, then find the tracing field in Agent Lens |
| 30–51 | Implement `make_classifier`, fit four practice points, then train the word-feature baseline | Inspect a validation request and save an observation before discussing alternatives |
| 51–59 | Ask ARIA to examine your interpretation of one TF–IDF validation request | Check a cited prediction or feature before discussing embeddings |
| 59–76 | Explain frozen sentence features and run the alternative with unchanged classifier code | Compare both predictions on the same request; both saved runs complete the comparison |
| 76–95 | Calculate one intent’s precision, recall and F1 from recorded predictions | Explain why macro-F1 requires the complete matched prediction set |
| 95–130 | Implement the review policy, inspect confidence and margin, save four labels | Separate automatic deferral from choosing labeling candidates |
| 130–140 | Break | Trained versions and reviews are saved |
| 140–190 | Run eight model routes, implement the judge validator, compare with personal reviews | Keep schema validity, judgment agreement and routing quality separate |
| 190–210 | Refit using accepted review labels and compare validation results | Explain the data change and decide whether to retain the earlier model |
| 210–220 | Break | Save the selected version and keep final-test results closed |
| 220–235 | Freeze the classifier and policy, evaluate all 3,080 official test requests | Inspect matching requests in EvalTables and separate quality from coverage |
| 235–240 | Draft the model-quality conclusion | Name one remaining mistake and preserve the official-test comparison |
| 240–250 | Break | The selected model and predictions are saved |
| 250–265 | Package and reload the selected router from its exact artifact version | Find the classifier, preprocessing identity, label order, policy, and code |
| 265–285 | Run the controlled label-order incident and follow one request | Explain why a confident probability can reach the wrong support queue |
| 285–305 | Save a reviewed regression case, write the release check, and repair the loader | Match probability columns to intent names; compare all fixed requests |
| 305–318 | Release or reject the repair, then practice rollback when released | Verify the previous artifact reproduces its saved predictions |
| 318–325 | Check the frozen model and release conclusions with ARIA or the recording | Separate the classifier gain from the loader repair; verify one citation |
| 325–330 | Publish the model and release conclusions together | Separate model quality, release correctness, and the remaining errors |

The deck’s threshold slider recomputes coverage from the saved 770 validation predictions. It makes no model call. The F1 walkthrough uses actual saved `card_arrival` predictions: 34 true positives, three false positives and six false negatives. The eight prompted routing calls and the judge exercise are separate paths: the judge reviews classifier proposals attached to participants’ accepted labels, not those eight prompted routes.

The first training button saves the TF–IDF model and enables validation-case inspection. The baseline comparison checkpoint remains incomplete until the sentence-feature run is also saved. Existing completed comparisons restore without additional fitting. If the classifier draft differs from the first run, restore that source before continuing; a different recipe belongs in another workspace.

The notebook separates **Route with the fixed model** from **Check the automated reviewer**. In the latter, ask participants to read their saved human reviews before editing the rubric.

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

The judge exercise publishes its saved decisions beside the participant’s accepted reviews. Final evaluation publishes the classifier comparison before the Report exercise. Click **Compare in EvalTables** at either step to open Evaluation Tables (Preview) in the Forge W&B workspace. The two comparisons answer different questions: judge agreement on reviewed development cases, and classifier quality on the official test set. Upload retries read saved outputs without running the judge or classifiers again. [Publication details and current checks](evaluations.md).

A fresh external-account run and a participant usability rehearsal remain release checks. CPU qualification establishes the worked classifier difference; it does not establish those product-access checks.

## Live routing and judge rehearsal

Twelve development-only model requests completed in the maintainer account: eight routing calls and four judgments. Every exported conversation passed stored-span readback. Observed inference cost was **$0.00113494**, with no bounded unknown cost or in-flight reservation remaining. The eight routing requests were chosen by fixed case ordering for an instrumentation check; they all concern card arrival and are not a quality benchmark.

Three of the four judge decisions matched the published dataset reference. This is not human calibration. For “Can I activate a card in the app?”, the classifier proposed `activate_my_card` and the judge agreed; the dataset label is `card_linking`. The text is ambiguous enough to warrant inspection instead of treating the reference label as infallible. [Open the recorded conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f5427dc7f06703d62c00561b6bd27a01).

The complete requests, costs, and verified trace identities are in `evidence/routing-live-v050.json`. The native capture in the deck preserves the actual question and judgment; its adjacent caption quotes the saved reason where the product's JSON pane clips the line.

The isolated browser check exercised the actual classifier editor, two CPU fits, a clearly labeled test-only review, retraining, freezing, all three 3,080-row final comparisons, and the publication controls. Provider and publication calls were disabled in that UI test. No browser errors or model calls occurred. This checks the interface separately from the live request/trace rehearsal; it is not an external attendee or human usability result.

A separate browser check verified the final prerequisite: freezing is disabled before a judge-comparison attempt and enabled after an attempted comparison with an explicitly unavailable judgment. That test disabled inference and publication; it verified the recovery path, not judge quality. Its record is `evidence/routing-judge-prerequisite-v050.json`.


## Release and recovery capstone

The capstone adds a controlled deployment problem after the classifier comparison. It runs a batch predictor in the notebook; it does not start a production service or train another model.

Click **Prepare the selected router for release**. The package contains the fitted classifier, its label-column order, the participant's review policy and classifier source, the dataset/encoder identity, and prediction-runtime source. The regression set is fixed by taking the lexically first review-pool case ID in each intent before any release prediction runs. These 77 requests may include reviewed training examples. They check reproduction, not independent generalization. The official test results stay unchanged.

Click **Publish and reload the exact release artifact** to download the saved `:vN` version and predict the fixed batch. The embedding version uses the existing pinned feature cache. Its latency does not include sentence encoding. Only load artifacts you created or trust: joblib files can execute Python when loaded.

The incident is deliberately introduced. The faulty loader rotates label names, so the same probability column points at another support workflow. Run it, open the corresponding Agent Lens operation, and follow one request through healthy and faulty outputs. Confidence and review coverage can stay unchanged even while routing quality falls.

Write `check_release(model_classes, loaded_labels)` to check both label membership and ordering. Write `label_names(model_classes)` to preserve the classifier's column order. The free check includes nonalphabetical labels so sorting is not mistaken for a valid repair. The same functions are saved with and used by the repaired release. Use **Save this reviewed regression case** to record your accepted intent and the incident that prompted it. This does not change the frozen classifier or repeat training.

The repair comparison reports accuracy, macro-F1, routing coverage, prediction latency, and exact prediction parity against the healthy release. Passing parity restores the old behavior, including any original classifier mistakes. Choose **Save my release decision** after explaining the checks. Rejection retains the previous version and completes the decision exercise. If you release the repair, **Restore the previous release and verify its predictions** downloads the prior artifact and checks its outputs before recording rollback.

Execution and publication are separate. **Retry release publication only** uploads saved packages, traces, and aligned comparisons. It does not rerun predictions. Completed batches and decisions survive restarts. The Report includes the incident results and release decision alongside the original model-quality conclusion.

Each comparison row keeps the evidence links available when it was first published. A later successful export adds its link to the notebook and Report without creating another evaluation of the same predictions. Unavailable links stay visibly absent from the original row.

Registry is an optional way to curate the exact artifact version, where permissions allow it. It does not deploy the classifier. The scheduled ARIA conclusion check uses live access or the recorded investigation; verify its cited case before accepting its explanation. The core capstone adds no model API calls and keeps the existing inference allowance.

### Recorded release drill

The November 14 maintainer browser rehearsal completed the capstone using the selected embedding classifier. The healthy release correctly routed 71/77 regression requests; the deliberately rotated label mapping routed 0/77 correctly. The learner-written loader repair restored all 77 original predictions. Downloading the previous exact artifact reproduced those same predictions during rollback. Six original classifier mistakes remained throughout healthy, repaired, and rolled-back versions.

All four variants published to [native EvalTables](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=37umm80le0d), with matching case IDs and scores checked by readback. Retrying publication reused the saved executions and evaluation IDs. No capstone training or model requests ran. The [receipt](../evidence/v070-routing-live.json) distinguishes this completed capstone from omitted core exercises and the still-required external-account and human rehearsals.

Use the [ARIA investigation guide](aria-investigations.md) for native context attachment, the recorded fallback, citation checks, access requirements, and separate ARIA usage. These stops replace discussion time and do not add execution gates.
