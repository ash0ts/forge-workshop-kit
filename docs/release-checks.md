# Release checks · 0.7.0 technical preview

This release adds workshop authoring commands, a repository-local skill, stable exercise references, and a Routing release-and-recovery capstone. Routing is allocated five and a half hours. The other four workshop schedules and their experiments remain unchanged.

## What the release drill measures

The capstone uses the participant's selected Banking77 classifier without training it again. One review-pool request per intent forms a frozen regression batch. A deliberately faulty loader changes the mapping between probability columns and intent names. Participants reproduce that fault, fix the mapping, compare the same requests, and verify a rollback.

This is a labeled release drill. Its corrected outputs demonstrate a loader repair, not an improved classifier or a new independent test result. The official-test comparison remains separate. Registry and ARIA are optional and do not gate the exercise.

## Coverage

| Check | Result |
|---|---|
| Free checks and domain tests | 330 tests passed locally. The release workflow also passed on macOS, Windows, and Linux. |
| Authored notebook references | All 44 exercise references match their current functions and controls. All seven notebooks pass marimo checks and regenerate identically. |
| Rehearsal adapters | Passive loading of all five workshops starts no execution. Replay preserved the saved workspace byte-for-byte. Live mode runs selected current action cells and retains review gates; it does not substitute historical runners. |
| Routing browser path | Current editors and controls exercised setup, two classifier fits, one review and judge, freezing, the official-test comparisons, the complete release capstone, and the Report. The eight prompted routes and reviewed-label retraining were omitted from this capstone rehearsal. |
| Release recovery | Exact artifact reload, controlled defect, learner-written check and repair, release decision, and verified rollback completed. A publication-only retry preserved all 19 execution results, the earlier model response, and native evaluation identities. |
| Native publication | All 3,080 rows in each of three official-test comparisons and all 77 rows in each of four release variants passed native readback. Agent Lens spans were read back for all four release executions. |
| Decks and packages | Five browser decks, PDFs, and source archives verified. Routing has 70 slides and 73 reveal/PDF states; all 18 new capstone frames were visually reviewed. A source archive built from a fresh temporary directory. |
| External account and human rehearsal | Still required. Neither is implied by maintainer checks. |

The [live capstone receipt](../evidence/v070-routing-live.json) records executed versions, scores, traces, artifacts, costs, and coverage. The [code audit](../evidence/v070-capstone-audit.json) and [deck checks](../decks/routing/notes/release-capstone-checks.json) cover their separate checks. Maintainer-supplied worked answers were used in the browser rehearsal; it is not a learner usability test.

Opening, navigating, restoring, and replaying saved work must not train or call a model. Publication retries reuse saved results. Rehearsals preserve review gates and identify any worked answers supplied by the maintainer.

## Observed release drill

The healthy release routed 71 of the 77 regression requests correctly. Rotating the labels reduced that to zero without changing confidence or review coverage. The repaired loader and the downloaded prior artifact both reproduced every healthy prediction, including the six remaining classifier errors. The capstone made no model calls and trained no model. The earlier single-judge setup check cost $0.00017744 in inference; notebook compute is separate.

Open the [native comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=37umm80le0d) or [rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Route-customer-requests-and-learn-from-mistakes:-c9407529--VmlldzoxODMwODkyNA==). The [capture](../evidence/captures/v070/routing-release-evaltables.png) shows the healthy, faulty, repaired, and rolled-back versions, in that order. The release defect was intentionally introduced; these results do not show improved model generalization.

## Prior experiments and releases

The [0.6.2 checks](archive/release-checks-v062.md) preserve earlier package, browser, publication, and cross-platform receipts. The [recorded outcomes](../README.md#what-happened-in-the-recorded-rehearsal) remain the source for the existing experiments. The release drill is additive and does not replace a tie, regression, or missing judgment with a more favorable result.

## Remaining readiness gates

Fresh external-account copying and human usability rehearsals remain outstanding. Maintainer publication and scripted browser checks do not establish that new participants can complete the workshop unaided. These remain technical-preview materials until those checks are completed.

Native comparisons use the Weave-backed Evaluation Tables Preview path. Report the capstone's actual publication status; the earlier separate CES HTTP 500 does not establish a failure or success in this path. See [evaluation setup](evaluations.md).

The participant-adjustable inference allowance remains $8. Notebook compute is separate. The release capstone requires no model API calls.
