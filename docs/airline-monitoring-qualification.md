# Airline monitoring qualification

The airline workshop remains a **technical preview**. The live booking runs, native traces, and evaluation comparisons completed. Native AI Alignment testing did not: all six test requests returned HTTP 500. This prevents a demonstrated automatic-monitor accuracy result. External-account access and a human rehearsal are also outstanding.

The [qualification JSON](../examples/airline-monitoring/qualification.json) records native identities and publication receipts. [Execution records](../examples/airline-monitoring/executions.json) preserve the requests, operations, starting and resulting bookings, checks, and costs. The [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Monitor-an-airline-service-agent:-recorded-qualification--VmlldzoxODMwOTE2MQ==) links the comparison to its evidence.

## Data and task

Passengers ask for a flight change, an itinerary read, or a change that the policy prohibits. The full-itinerary update tool replaces the booking's complete flight list. The agent must preserve flights the passenger did not ask to change, quote the price, obtain confirmation, and check what was saved.

These are fictional records adapted from Sierra's MIT-licensed [tau2-bench v2.0.0 snapshot](https://github.com/sierra-research/tau2-bench/tree/989d3285ae669e49503324bdb9981bf14fccedeb/data/tau2/domains/airline). We reuse source customers, reservations, flights, and the API's replacement semantics, then construct narrower requests and scripted passenger confirmations. This is neither an official benchmark run nor production airline data. There is no passenger-simulator LLM.

The bundled fixture has 26 requests. Its discovery, monitor-check, development, reserved, and subsequent partitions contain 8, 4, 4, 6, and 4 cases. Related source customer families stay within a partition; source train families overlapping the source test families were excluded. The [provenance file](../src/forge_workshop_kit/assets/airline/provenance.json) records the exact task IDs, selection rules, exclusions, source checksums, and adaptations. Reserved cases never enter repair inputs or development judging. Public local files remain inspectable; this is a teaching separation rather than a secret benchmark.

## What the live runs showed

| Phase | Starting agent | Repaired agent |
| --- | --- | --- |
| Discovery | 8/8 | Not run |
| Monitor check | 4/4 | Not run |
| Matched development | 4/4 | 4/4 |
| Reserved evaluation | 6/6 | 6/6 |
| Subsequent traffic | 4/4 | 4/4 |

All **40/40** conversations passed the independent booking checks. Ten tool errors occurred within those executions, but the final bookings passed; an error count alone would misclassify successful recovery. The repaired agent invoked the learner's itinerary-planning helper nine times. Installing that helper does not imply it was used in every request, and the observed tie does not establish a quality improvement.

The 40 conversations used 193 model attempts and cost **$0.02330616**. One separate explanation-judge call brought recorded direct inference to **$0.02401506**, with zero bounded unknown usage and no outstanding reservation. That judge accepted the saved explanation and cited actual events; one valid response is not evidence that a judge agrees reliably with people. Native tag judging and notebook compute have separate billing and are excluded from these figures.

The provider limits each conversation to ten actual model attempts, counting transport retries. The $8 default workspace allowance remains adjustable. Reopening or retrying publication does not repeat the 40 executions.

## Native product checks

All 40 live conversation traces passed stored-span checks against their independent operation receipts. For a concrete example, open the [recovered-read conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae): the first reservation read times out, the retry succeeds, and the confirmed update retains the return flight.

The [saved starting-agent view](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/views/01a1dc0a-3ea9-73bd-b0b8-bd7ecd7d9951) was checked in the native UI. It filters the exact workshop agent and the custom `airline.version=baseline` attribute. The native Agent Version dropdown had no options in this session; the working view uses the recorded custom attribute instead.

The native Weave-backed EvalTables path published and read back all six version tables: two development versions with four rows each, two reserved versions with six rows each, and two subsequent versions with four rows each. These are 28 versioned prediction rows, not 28 independent requests. Open [development](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1), [reserved](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=m6e4y19blu9), or [subsequent](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=8woi2lgyt5c) comparisons.

The native tag's criteria, exact agent scope, and manual Alignment labels were saved and read back. Six explicit AI Alignment test requests returned HTTP 500. Their predictions and costs remain unavailable; they are not negative predictions or failed bookings. Live assignment readback likewise did not establish completed negatives or processing coverage. Precision and recall must therefore remain unavailable for this qualification.

Insights returned project-level clustering metadata, but no completed cluster covering this workshop session was available to investigate. The workshop does not substitute local grouping and call it Insights. A prepared cluster demonstration still needs relevant native evidence and an access check.

Automatic tagging was **disabled and verified by native readback** at the end. Closing a notebook alone does not turn it off. Native judging is billed outside the notebook's inference allowance.

## The worked repair

Six labeled, tool-only calibration examples provide an omitted-return incident and controls: one-way travel, a valid connection-to-nonstop change, a requested full replacement, successful recovery, and pending confirmation. They execute actual simulator tools but contain no model calls. They are excluded from the 40 live quality results.

The [curated regression proof](../examples/airline-monitoring/regression-proof.md) takes the saved omitted-return incident and one-way control through the canonical learner functions. The omission adapter fails the requested-change check; the repaired builder passes. Both versions preserve the read-only control. The proof also verifies that a second invocation reuses its saved result and leaves the request ledger unchanged. Its worked reviews were supplied for technical verification, not by workshop attendees.

## What has and has not been rehearsed

| Coverage | Evidence and limit |
| --- | --- |
| Domain execution | All 40 required live conversations completed and were scored. This is a direct runtime qualification, not a full notebook interaction rehearsal. |
| Free domain checks | Source/partition validation, full-itinerary semantics, confirmation, recovery, learner hooks, attempt limits, reserved-input exclusion, and regression replay are covered by domain tests. |
| Authored notebook cells | Thirteen authored-cell tests cover free checks, learner hooks, restoration, publication-only retries, actual curated-regression execution, navigation callbacks, and display refresh dependencies. The authoring check resolved 72 cells, 35 actions, and 20 exercise references. Worked answers were supplied. |
| Browser interactions | Native pages and notebook screens have maintainer checks, but a complete current end-to-end browser execution of every participant action is not established by the runtime results above. |
| Native services | Traces and all six EvalTables verified; tag configuration/manual labels verified; AI Alignment tests unavailable; no relevant completed Insights cluster. |
| External account | Not verified. A maintainer's successful publication does not prove a fresh attendee can copy and use every required feature. |
| Human usability | Not completed. The proposed six-hour schedule has not been validated with participants. |

The recorded package test run passed **369 tests**, with seven dependency deprecation warnings, in 57.73 seconds. Tests are distinct from live native access and human usability. After the 40-conversation qualification, the runtime gained saved `trace_context` metadata for publication retries and broader tool-error recording for exceptions from learner functions. A mocked-provider check verifies that a learner's `RuntimeError` is saved with arguments and timestamps, returned to the next model step, and counted as an execution error. The exact earlier source remains with the live execution artifacts; the latest runtime is not byte-identical to that source. No booking run was repeated or reattributed to the later code.

Before advertising the workshop as ready, resolve or explicitly redesign around the native Alignment failure, verify a relevant Insights example, finish the full browser path, test a fresh participant account, and rehearse with people who did not write the notebook. Keep the live tie and missing monitoring results visible throughout those checks.
