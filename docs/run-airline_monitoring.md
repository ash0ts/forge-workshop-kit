# Run Airline Monitoring

**Six hours · basic Python · Agent Lens investigation, monitoring rules, and regression tests**

A passenger wants to change one part of a trip. The booking API replaces the entire itinerary, so a successful call can still remove an untouched connection or return flight. Participants inspect the booking, review a monitoring rule, reconstruct regression cases, and test a repair. The bookings are simulated data adapted from the public τ-bench airline environment.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) · [Copy notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) · [Full runbook](airline_monitoring-runbook.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Use the recorded walkthrough for a meeting. Native tag configuration and manual labels were verified, but the last AI Alignment tests returned HTTP 500 and prepared Insights has no completed clustering run. Those activities remain unqualified. Rehearse the intended native access and participant path before scheduling the full class.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–1:05 | Inspect the requested change, try the local booking drill, connect and instrument, then run one discovery request before the remaining seven. |
| 1:05–1:40 | Follow conversations and booking outcomes; save a human review before drafting tag criteria. |
| 1:40–1:50 | Break. |
| 1:50–3:10 | Challenge the review with ARIA, examine Alignment counterexamples, save criteria, then calculate agreement and processing coverage on new requests. |
| 3:10–3:50 | Reconstruct a reviewed incident and an unflagged control as regression cases. |
| 3:50–4:00 | Break. |
| 4:00–4:45 | Repair the itinerary builder and compare matched development requests. |
| 4:45–5:45 | Freeze versions, compare reserved requests, then inspect subsequent traffic under the same monitoring rule. |
| 5:45–6:00 | Check the conclusion, reproduce a case, publish it, and verify automatic tagging is off. |

The notebook opens with Sofia's connection change; the deck's early API diagram also uses a separate round-trip example. Name that switch. “Fewer flights” alone does not establish an unrequested change, and an absent tag does not establish a negative judgment.

## Give a ten-minute demo

Follow the [recorded walkthrough](current-demo-guide.md#airline-monitoring-in-ten-minutes): request, original booking, actual tool result, human review, and reconstructed test. Label the controlled omitted-return example explicitly. Both live agent versions passed their reserved and subsequent requests; that comparison tied.

## If native monitoring is unavailable

Continue with source-linked turns, local review arithmetic, and the labeled calibration example. Keep monitor precision and recall unavailable. Do not substitute a notebook grouping for native Insights. Tag judging has separate billing; finish by disabling **Apply with AI** and using **Verify automatic tagging is off**. Closing the notebook does not disable it.
