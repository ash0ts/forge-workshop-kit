---
name: forge-workshops
description: Author, revise, rehearse, and publish Forge Workshop Kit notebooks and companion decks. Use when building a hands-on workshop or preparing its delivery.
---

# Forge workshops

Work in the standalone Workshop Kit checkout. The participant copies a notebook into their own project and uses their own credentials. Keep the editable lesson in the authored cells; the shared package owns saving, accounting, publication, and progress. Read the [source map](../../../docs/source-map.md) and [framework contract](../../../docs/framework.md) before changing those boundaries.

## Establish the lesson

Read the current notebook, storyboard, and runbook before proposing changes. Record the audience, duration, learning outcome, dataset and license, intervention, comparison, metric, and budget. Preserve decisions already supplied by the requester. Ask only for choices that affect the exercise and cannot be recovered from the existing material.

Follow one concrete example through intermediate values, the responsible code, its output, a participant exercise, and a specific investigation in Forge. Give learners a bounded code change, a free local check, an explicit execution control, and a result they can explain. A form or approval is not a replacement for implementing the concept.

For new workshops, use `forge-workshop new` from the [authoring guide](../../../docs/authoring.md). Complete the scaffold before publishing it. The manifest owns exercise references and entry points; authored cells and storyboards own explanations. Edit those sources and regenerate, rather than patching generated notebooks or slide Markdown.

## Preserve the experiment

Use the existing session, stage, provider, and publication contracts. A completed execution with a failed upload is still completed. A replay is saved evidence, never the outcome of a learner's unexecuted edit. Keep unknown usage reserved, unavailable judgments missing, and publication retries independent of model or training calls.

Keep the learner's project and the exact executed code attached to results. Opening, editing, navigating, restoring, or building a notebook must not execute an exercise. Review gates remain real in a rehearsal. Do not silently substitute models, change splits, or select examples by favorable scores.

Read [evaluation publication](../../../docs/evaluations.md) when changing comparisons. Consult the [official W&B skills](https://github.com/wandb/skills) for product-specific guidance, but check their dependency requirements against this kit before using their helpers. They are optional authoring aids, not participant dependencies.

## Rehearse what participants receive

Use the current authored action cells and stable exercise IDs. Historical qualification scripts can establish a recipe or domain behavior; they cannot establish that the current notebook works. Record free checks, domain execution, authored-cell execution, browser interaction, external-account access, and human rehearsal separately.

Inspect the actual notebook and rendered deck. Check code beside its effect, readable labels, meaningful reveal states, Back navigation, worked-answer returns, and exact function/button references. Preserve original product captures and their source links. Use diagrams for mechanisms and real captures for observed product behavior. Never invent traces, scores, screenshots, or successful publication.

## Build and publish

Use the commands and destination checks in [maintenance](../../../docs/maintenance.md). Building is local; publishing is a separate action to an explicit project. Existing task authorization applies. If publication was not requested, provide the validated build rather than uploading it. If authentication or a product feature is unavailable, preserve the build and report the affected check; do not introduce a gateway or facilitator credential workaround.

Keep previous releases and attendee copies intact. Package version and workflow compatibility are separate. Update [release checks](../../../docs/release-checks.md) with the coverage actually obtained, including any external-account or human checks still outstanding.

## Completion

- The participant-authored change affects the subsequent execution.
- Notebook, deck, runbook, and manifest identify the same exercise and control.
- Results open the matching code, data, trace, and comparison where available.
- Validation distinguishes observed behavior from untested access or usability.
- Requested deliverables are built and publication status is explicit.
