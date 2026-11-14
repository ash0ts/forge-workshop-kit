# Continue from a tested model

These optional modules begin with a completed core workshop. They do not change its results or require a facilitator's account. Keep the selected dataset, evaluation split, and scoring code fixed while testing the new intervention.

| Module | What changes | What you need |
|---|---|---|
| [Train a routing specialist](sft.md) | Model weights | Training entitlement, supported base model, current cost forecast |
| [Release and reproduce](release.md) | The artifact selected for use | Artifact access; Registry permission for the Registry exercise |
| [Run code outside the notebook](remote.md) | Execution location | Enabled Sandboxes; a prepared Launch worker for ARIA experiments |

Core inference allowances do not cover these services. Forecast billed training, inference, storage and remote compute separately. The scripts require an explicit launch and cost approval. Merely importing them makes no service call.

These modules have contract tests and current API checks. They are not qualified live training lessons until their access, timing, cost and end-to-end reproduction have been rehearsed. Model Distillation is a separate private-preview product; generating teacher labels in the routing exercise does not use that product. RL is deferred until the dataset, evaluator and SFT comparison work.
