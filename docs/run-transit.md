# Run the Transit Software Factory

**Six hours · basic Python · coding workers, coordination, integration, and shared lessons**

A software team is building a departure board for people leaving an evening event. Participants implement the Python that assigns work to coding agents, reviews their patches, and checks the combined app. The frozen MBTA schedule is historical, not a source of live arrivals.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/transit/) · [Start notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/transit.html) · [Full runbook](transit-facilitator.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Open the saved timetable and the recorded app. Find the `24:08:00` departure and explain both its service date and following civil date. Rehearse the free worker, dependency, and claim checks before any live builder. External-account and human rehearsals remain required for the full class.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–0:50 | Inspect a real departure, write a scenario, connect, and send a trace. |
| 0:50–1:35 | Complete one worker's read/edit/test loop, run it, review its patch, and preview the tested app. |
| 1:35–1:45 | Break. |
| 1:45–3:00 | Implement dependencies and atomic claims, run two workers, review ownership and patches, then test integration. |
| 3:00–3:20 | Break. |
| 3:20–4:45 | Investigate the development builds with ARIA, save a supported lesson, and compare fresh teams with and without that lesson. |
| 4:45–4:55 | Break. |
| 4:55–6:00 | Freeze and evaluate the builds, decide what can be released, check the conclusion, and reproduce the app. |

Use **Review and test the one-builder app**, then **Preview this saved app**, before introducing coordination. Keep “submitted,” “tested,” and “integrated” distinct. Seeing a solo preview does not choose the starting source for the later memory comparison.

## Give an eight-minute demo

Use the [recorded walkthrough](current-demo-guide.md#transit-software-factory-in-eight-minutes). Follow one service-time conversion, worker patch, and integration check. Show the free claim-race repair, then inspect the actual solo/team and memory comparisons.

## If live work stops

Preserve the stopped worker and its cost. Use the labeled reference app if both integrations fail. In R5, the solo build passed 10/10 checks, the team passed 8/10, and both follow-ups passed 12/18. The recording establishes neither a team advantage nor a memory benefit. Retry uploads from saved work rather than launching another builder.
