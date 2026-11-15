# Recorded workshop results

These are instructor executions, not results produced by a participant’s edits. Use the linked protocol and execution records when presenting a comparison.

The November 14 qualification adds these worked examples. Scores are not interchangeable across tasks.

| Exercise | Measured outcome | What it establishes |
| --- | --- | --- |
| Pending retry repair | Two memberships with a new operation ID; one with the original ID and an account check | A deterministic implementation repair in the fictional simulator. The later harness comparison remains a 4/4 tie. |
| Banking77 | Macro-F1 **0.879385 → 0.920229** on 3,080 official test requests | Frozen sentence features beat TF–IDF in this fixed classifier comparison. Three deterministic seeds reproduced the same result; they are not three independent experiments. |
| VisA PCB1 | Average precision **0.872900 → 0.885742**; misses **4 → 3**, false alarms **23 → 18** on 442 test boards | The bounded follow-up improved on already-inspected test images. This is a teaching retest; the failed first recipe remains published. |
| GOES | Persistence MAE **0.192706**; residual MLP **0.162878, 0.163880, 0.163760** across seeds 17, 29, 43 | The validation-selected recipe beat persistence in all three teaching retests. Previously inspected final dates are not newly unseen data. |
| AIA images | Changes of **+10.15%, +6.87%, −0.21%** against the manual model across the same seeds | Two improvements and one small regression. The fixed recipe did not pass the all-seed reliability gate. |
| Transit app | One worker **10/10**; two workers **8/10**. Both follow-ups **12/18** | The faster team selected the wrong train for a UTC input. Follow-up query workers stopped at input/output limits; this does not establish a memory benefit or loss. |
| Airline bookings | All **40/40** live conversations pass independent booking checks. Starting and repaired agents each pass **6/6** reserved and **4/4** subsequent requests. | No live quality gain was observed. A separately labeled local adapter drill demonstrates the itinerary repair; its controlled failures are not counted as live agent mistakes. |

See [transit results and the captioned walkthrough](transit-workshop.md), [routing evidence](routing-workshop.md), [inspection evidence](inspection-workshop.md), and [Solar qualification](solar-qualification.md) for frozen protocols, all outcomes, sources, and limitations. Dataset labels supplied by the authors, participant reviews, and model suggestions remain distinct.

The [airline qualification](airline-monitoring-qualification.md) and [machine-readable results](../examples/airline-monitoring/qualification.json) record all 40 conversations. They cost **$0.02330616**; one explanation-judge call brought direct inference to **$0.02401506**, with no unknown usage. Native tag judging and notebook compute are separate. Native tag configuration and manual labels were accessible, but six Alignment test requests returned HTTP 500, and Insights had no completed cluster for the new session. The workshop therefore does not claim demonstrated automatic monitoring accuracy or a ready-to-run classroom experience. External-account and human rehearsals remain outstanding.

For the earlier November 13 results, Reports and dashboards, see the [rehearsal archive](archive.md#november-13-rehearsals). The [demo guide](current-demo-guide.md) identifies which saved run to open for each exercise.
