# Train a routing specialist

The routing workshop changes features and training labels. This extension changes an LLM's weights using the labels you accepted. Keep the routing prompt, output schema, cases and evaluator unchanged when comparing its base model with its trained checkpoint.

1. Finish the human-review step. Export the **review** records and case text from your own notebook. Teacher predictions alone are not accepted labels. `sft_examples` rejects final-test cases and unverified labels.
2. Read the current [Serverless SFT documentation](https://docs.wandb.ai/serverless-training/sft/). Confirm supported models and billing for your account. Its preview terms can change; the workshop does not assume training is free.
3. From your checkout, run `uv run python examples/advanced/sft.py check --project ENTITY/PROJECT --state YOUR_WORKSPACE`. This checks entitlement without training. Your workspace directory is shown in the notebook's recovery details.
4. Run the script's `prepare` action with `--dataset-version` and `--cases`. It saves `train.jsonl` as a versioned training-data Artifact. Inspect three accepted examples before continuing.
5. Create a forecast JSON containing `maximum_usd`, `checked_at` and `basis`. The basis should list the current training, inference and storage rates, maximum training steps, evaluation calls and expected duration. Choose a model only after checking its availability. The core workshop's GLM model is unchanged.
6. Use the `launch` action with `--base-model`, `--forecast` and `--approve-usd`. The script saves the request before submission and the returned job ID afterward. Use `status --job-key ...` to monitor the same job after a restart. A timeout with no returned ID requires provider-side investigation; it is not automatically resubmitted.
7. Use `checkpoints --model-id ...` after completion. It lists the newest 100 checkpoints first; check `has_more` if you need an older version. Select an exact checkpoint, then use the comparison script below. It keeps the same prompt and typed response schema for both models.
8. Publish macro-F1, abstention coverage, latency and actual cost together. A more fluent explanation does not count as a correct route. Preserve the unchanged base model as a comparison.

The raw API uses a learning-rate schedule, not an `epochs` field. `sft_request` explicitly converts the requested epochs and batch size into that schedule. The current public API schema is checked during release; the account and launch still need live qualification.

A successful trained checkpoint can be called through Serverless Inference. Linking an artifact to Registry alone does not provide that serving endpoint.

## Compare the base model with its checkpoint

This optional extension has offline contract tests. It has **not** completed a live training-and-comparison rehearsal. Check the account's model support and prices before launching it. A returned model ID that differs from the requested ID stops the comparison; the script never substitutes the workshop's core model.

Export the public routing records from the notebook's data directory. `sft.py prepare` expects a mapping from case ID to record. The original `cases.json` contains a list, so convert it first:

```python
from pathlib import Path
import json

rows = json.loads(Path("YOUR_WORKSPACE/datasets/banking77-v1/cases.json").read_text())
training_cases = {row["id"]: row for row in rows if row["split"] in {"train", "review"}}
Path("routing-training-cases.json").write_text(json.dumps(training_cases, indent=2))
```

The training output contains `intent`, `needs_review` and `reason`, matching `routing.validate_route`. Accepted labels set `needs_review` to false. If the review has no written reason, its target says only which queue to use. That format fallback is not a human explanation of why the request belongs there.

Before inference, choose the evaluation cases once. For a bounded teaching comparison, select the first official-test case ID in each intent, sorted lexically. This gives 77 matched requests per model without selecting by score. It does not replace evaluation on the full Banking77 test set.

Write `sft-comparison-spec.json` with:

- `cases`: records containing `case_id`, `text`, `target` and `split: "test"`.
- `intents`: all 77 allowed labels.
- `models.base` and `models.checkpoint`: each contains `model`, `input_usd_per_million` and `output_usd_per_million` using current verified prices. The checkpoint must use its exact `wandb-artifact:///ENTITY/PROJECT/MODEL:stepN` or `:vN` identity. Do not use `latest`.
- `max_tokens`: 512 for this comparison.

```sh
uv run python examples/advanced/compare_sft.py plan \
  --project ENTITY/PROJECT --state YOUR_WORKSPACE --spec sft-comparison-spec.json
```

Planning writes `sft-comparison-plan.json` and prints the maximum inference charge under the recorded rates. It sends no requests. Record that total, the checked date, and the pricing basis in a separate forecast JSON; then explicitly approve the amount:

```sh
uv run python examples/advanced/compare_sft.py run \
  --project ENTITY/PROJECT --state YOUR_WORKSPACE \
  --forecast comparison-forecast.json --approve-usd YOUR_APPROVED_AMOUNT
```

Restarting this command reuses saved responses. Missing usage counts at its full reserved maximum. A lost response or unexpected model stops further work and requires investigation; it is never silently retried. This advanced comparison has its own explicit approval, separate from the core workshop allowance. Printed costs are estimates from reported usage at the frozen rates; they do not assume cache discounts.

Use the returned `advanced-sft/...` identity to publish the saved rows and Agent Lens trace:

```sh
uv run python examples/advanced/compare_sft.py publish \
  --project ENTITY/PROJECT --state YOUR_WORKSPACE --identity SAVED_COMPARISON_ID
```

Publication can be retried without inference. An invalid or missing response remains an unavailable row. If any rows are unavailable, the full-comparison F1 and accuracy stay missing; available-response summaries are labeled separately. Native EvalTables availability must be checked on the participant account; local results remain in the workspace if publication fails.

The API contract follows the [current public training schema](https://api.training.wandb.ai/openapi.json) and the [ART serverless implementation](https://github.com/OpenPipe/ART/blob/main/src/art/serverless/backend.py), checked November 14, 2026. API compatibility is narrower than a successful live rehearsal.
