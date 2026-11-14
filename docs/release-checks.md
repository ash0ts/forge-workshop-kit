# Release checks · 0.8.0 technical preview

This release adds the six-hour airline monitoring workshop. It follows an agent's booking operations into Agent Lens, reviewed tags, offline regression cases, a code repair, and subsequent traffic. Existing workshops, recorded outcomes, and attendee copies remain unchanged.

The [airline qualification record](airline-monitoring-qualification.md) and [machine-readable results](../examples/airline-monitoring/qualification.json) own the live execution and publication details. This page separates that evidence from the checks still required before classroom use.

## Observed results

All 40 live conversations passed the independent booking checks: eight discovery, four monitoring, eight paired development, twelve reserved, and eight subsequent executions. Starting and repaired versions each passed 6/6 reserved requests and 4/4 subsequent requests. No live quality gain was observed. These are simulated airline operations, not production conversations or an official tau-bench result.

The separate local adapter exercise intentionally returns only the replacement flights. Its reviewed incident and controls show whether the learner's repair preserves the rest of the booking. The replay consumes the saved reviewed cases, checks their original state and source identities, and makes no model calls. Controlled failures are labeled and excluded from live agent scores.

The 40 conversations cost **$0.02330616** in direct inference; one separate explanation-judge call brought the total to **$0.02401506**, with **zero bounded unknown usage**. Native tag judging and notebook compute are separate. The participant's default inference allowance remains $8.

## Native monitoring status

| Capability | Qualification result |
| --- | --- |
| Conversation and tool/model trace export | Live executions were exported and checked against saved operation receipts; see the qualification record for identities. |
| Native tag configuration and scope | Saved configuration was read back. |
| Native Alignment manual labels | Accessible and saved. |
| Native Alignment AI tests | Six requests returned HTTP 500. Their predictions remain unavailable. |
| Insights | No clusters were available for this new session. No local grouping is presented as native Insights. |
| Agent quality | All 40 live executions passed; the repair comparison tied. |

A missing live assignment is not an explicit negative judgment. The workshop calculates precision and recall only from completed predictions paired with human reviews of the same turn. It reports processing as unknown when the service provides assignments without a completion denominator.

## Validation boundaries

Domain tests cover source checksums, family-separated partitions, full-itinerary replacement, confirmation, recovered reads, participant hooks, attempt limits, protected evaluation inputs, saved-result reuse, and the reviewed-case regression replay. Current notebook checks cover free exercises, navigation without paid work, restoration, and publication-only recovery. The final suite passed 369 tests. Consult the qualification record for the test coverage and actual browser coverage; a direct runtime rehearsal does not establish complete notebook interaction coverage.

Opening, editing, restoring, and inspecting results must not send model requests. Explicit execution controls spend the participant's own inference allowance. Native tag judging has separate billing, and participants must turn off **Apply with AI** when they finish.

Fresh external-account copying, native monitoring service recovery, and a human usability rehearsal remain outstanding. Maintainer execution and automated checks do not establish that participants can finish unaided. Keep this workshop labeled **technical preview** until those checks pass.

## Prior releases

The [0.7.0 release checks](archive/release-checks-v070.md) preserve the Routing capstone's browser, artifact, rollback, and native evaluation evidence. Earlier qualifications remain in the [archive](archive.md). Native EvalTables publication uses the Weave-backed Preview path; its status is independent of the Agent Lens Alignment HTTP 500 described above. See [evaluation setup and recovery](evaluations.md).
