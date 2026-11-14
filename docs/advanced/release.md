# Release, reproduce and roll back

Use a saved routing model or PCB detector. A release decision connects its exact artifact version to the evaluation that justified using it. Registry organizes that selection; it does not run the classifier for you.

```python
from forge_workshop_kit.releases import record_release, reproduce, link_registry

release = record_release(
    session,
    artifact=selected_artifact,       # entity/project/model:v3, never :latest
    evaluation=evaluation_url,
    decision="release",
    metrics=measured_metrics,
    checks=release_checks,            # participant-authored checks over real results
    previous=previous_artifact,
    reason="Explain the measured tradeoff and the unresolved failures.",
)
files = reproduce(release["artifact"], root="reproduced-model")
# Load the saved preprocessing and classifier from these files.
# Recompute one saved prediction and assert that it matches the published row.
```

Before executing this cell, write your checks using the validation decisions you froze. For inspection, include both misses and false alarms; do not approve a detector solely because it sends more boards to human review. For routing, include coverage as well as accuracy.

To exercise a failed release, submit a candidate whose actual result fails one check. `record_release` must reject a `release` decision. Record it with `decision="reject"` and its real check values. Do not change a score to make this demonstration work.

With Registry permission, call `link_registry(session, release["id"], "wandb-registry-Models/routing")`. Open the collection and follow the link to the evaluated version. Without Registry access, the pinned Artifact and reproduction exercise remain available.

To roll back, create a new decision with the previous artifact as `artifact`, the currently selected one as `previous`, and `decision="rollback"`. Check that the old version still meets the release requirements. Load that exact version in the batch predictor and reproduce its earlier output. This is a new selection, not deletion of the unsuccessful model or its evaluation.

[Registry documentation](https://docs.coreweave.com/products/registry)
