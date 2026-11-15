# Release checks · 0.4.1 technical preview

Version 0.4.1 expands the openings in both decks and notebooks. Pending explains the customer requests, starting account records, and required account changes. Solar introduces the lab's review assignment, instruments, forecast inputs and targets, and comparison against persistence before project setup. The exercises, datasets, settings, and saved results are unchanged. The Solar introduction now appears only on the setup step.

This revision changes the teaching views, deck reveals, and notebook explanations. The data, model settings, scores, three-hour Pending schedule, four-hour Solar schedule, and workflow compatibility version 1 are unchanged. It uses the November 13 rehearsals. No new training or inference was run.

## Notebook checks

The browser checks used isolated copies of saved rehearsal workspaces. Inference, training, trace export, and publication were disabled in those verification processes. The controls were tested against real saved outputs; project access was stubbed and is not an attendee-access check.

- Pending: action/arguments/result/message tabs; timeout, retry with the same operation ID, a new operation, and reset; actual skill-read status; branch selection; and aligned final-case selection. The saved request and execution records did not change.
- Solar: accepted-window selection and normalization; learner-authored MLP and CNN forward passes without training; scorer arithmetic inside and outside the disk mask; and aligned frozen predictions at the selected timestamp. Navigation remains responsive after the free code check. The saved request and execution records did not change.
- Shared branch views: desktop, narrow and dark presentation, keyboard selection, and the sequence Candidate A → Test A → Candidate B → Test B. The detail panel separates proposals, actual executions, decisions, missing results, and retained versions.
- Unit checks cover retained versions, rejected changes, missing traces, scorer errors, per-image averaging, shared image scales, selected execution identity, and the notebook's reactive dependencies. The existing recovery and accounting checks remain in the full suite.

See [browser and source checks](../../evidence/v040/validation.json). The [visual walkthrough](../teaching-sequence.md#use-consistent-visual-conventions) describes what to inspect at each step.

## Deck and package checks

Pending has 82 slides and 98 reveal states; Solar has 101 slides and 121 reveal states. Every state was rendered and checked for clipping, missing images, malformed text, diagram label collisions, keyboard advance and return. Every PDF page was rendered and visually reviewed. Worked-answer links return to the correct exercise even when reveals add PDF pages.

Numbered annotations use the original native Forge captures and preserve their source links. The decks label recorded results and show the actual W&B and Weave comparisons. They do not present an unavailable native EvalTables page as a successful publication.

The official Slidev skill is vendored from the reviewed revision listed in [UPSTREAM.md](../../.agents/skills/slidev/UPSTREAM.md). The package and notebook previews are built without participant credentials. Source bundles include the shared visual definitions. Notebook regeneration, marimo validation, distribution-content checks, and the full unit suite are part of the release build.

## What the recorded results establish

Pending's three versions each passed all four final cases. It demonstrates changed behavior and an inspectable improvement process, without a measured quality gain. Solar's selected image model improved on the manual model in the recorded rehearsal; its GOES neural model performed worse than persistence. Those are fixed-seed teaching examples, not independent statistical replications. The complete scores, costs and historical service checks remain in the [v0.3.0 evidence review](release-checks-v030.md).

## Remaining limits

Native EvalTables returned HTTP 500 in the last live service check. This presentation revision made no new service-test claim. W&B results, Weave evaluations and notebook comparisons remain available, and publication can be retried from saved records without another experiment.

Hosted template publication is verified by reading back the uploaded source and preview files. That does not establish that a fresh attendee can copy and run them. The external-account copy/restore check and human usability rehearsal remain outstanding. This release is a technical preview.
