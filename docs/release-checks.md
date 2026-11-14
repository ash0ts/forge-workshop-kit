# Release checks · 0.7.0 technical preview

This release adds workshop authoring commands, a repository-local skill, stable exercise references, and a Routing release-and-recovery capstone. Routing is allocated five and a half hours. The other four workshop schedules and their experiments remain unchanged.

## What the release drill measures

The capstone uses the participant's selected Banking77 classifier without training it again. One review-pool request per intent forms a frozen regression batch. A deliberately faulty loader changes the mapping between probability columns and intent names. Participants reproduce that fault, fix the mapping, compare the same requests, and verify a rollback.

This is a labeled release drill. Its corrected outputs demonstrate a loader repair, not an improved classifier or a new independent test result. The official-test comparison remains separate. Registry and ARIA are optional and do not gate the exercise.

## Coverage

The current implementation is being validated. Publication and coverage receipts will be added here after their checks finish. Historical runtime scripts do not count as current notebook rehearsal. The shared runner distinguishes free checks, domain execution, authored-cell execution, browser interaction, external-account access, and human rehearsal.

Opening, navigating, restoring, and replaying saved work must not train or call a model. Publication retries reuse saved results. Rehearsals preserve review gates and identify any worked answers supplied by the maintainer.

## Prior experiments and releases

The [0.6.2 checks](archive/release-checks-v062.md) preserve earlier package, browser, publication, and cross-platform receipts. The [recorded outcomes](../README.md#what-happened-in-the-recorded-rehearsal) remain the source for the existing experiments. The release drill is additive and does not replace a tie, regression, or missing judgment with a more favorable result.

## Remaining readiness gates

Fresh external-account copying and human usability rehearsals remain outstanding. Maintainer publication and scripted browser checks do not establish that new participants can complete the workshop unaided. These remain technical-preview materials until those checks are completed.

Native comparisons use the Weave-backed Evaluation Tables Preview path. Report the capstone's actual publication status; the earlier separate CES HTTP 500 does not establish a failure or success in this path. See [evaluation setup](evaluations.md).

The participant-adjustable inference allowance remains $8. Notebook compute is separate. The release capstone requires no model API calls.
