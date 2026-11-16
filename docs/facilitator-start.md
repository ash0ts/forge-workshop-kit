# Run a Forge workshop

Pick one workshop for the audience, then choose a recorded demonstration or a hands-on pilot. You do not need to teach all six. A demonstration follows saved code and results; a pilot asks each participant to copy the notebook and run an exercise in their own project.

**The full workshops are technical previews.** Complete the external-account and participant checks in [current status](../next-up.md) before scheduling a class. The published decks and recorded examples can be used for meetings now.

## Choose a session

| Workshop | Teach this decision | Full session | Quick running guide |
| --- | --- | --- | --- |
| Pending | Did a harness edit change the agent's behavior or improve the account outcome? | 4 hours | [Run Pending](run-pending.md) |
| Solar | Does a research-code change beat the existing forecast on the same observations? | 6 hours | [Run Solar](run-solar.md) |
| Routing | Which requests should we route, and does the released classifier reproduce its predictions? | 5½ hours | [Run Routing](run-routing.md) |
| Inspection | Do local image features or additional labels reduce defects we miss? | 4 hours | [Run Inspection](run-inspection.md) |
| Transit | Do separately built components work together, and did a saved lesson help? | 6 hours | [Run Transit](run-transit.md) |
| Airline | Does the monitoring rule catch the booking mistakes we care about? | 6 hours | [Run Airline](run-airline_monitoring.md) |

All assume basic Python. The durations include explanations, coding, and breaks. For a short meeting, choose the guide’s recorded demo. The [workshop overview](workshop-overview.md) introduces the collection and its product connections.

## Prepare the room

1. Open the chosen guide, browser deck, PDF, and notebook start page. Keep the PDF and the recorded example available if a service is slow. For offline interaction, extract the browser ZIP and run `python3 serve.py --open` (Windows: `py serve.py --open`). The PDF opens directly. The [deck guide](deck-guide.md) explains presentation controls and worked answers.
2. For a hands-on session, rehearse an attendee-style copy using the intended account type. Check notebook compute, project writes, tracing, inference, and evaluation publication separately. Use the [participant setup guide](setup.md); laptop instructions are included.
3. Send the workshop’s [registered sharing link or QR](share-links.md), setup guide, and duration before the session. Its public packet card includes the notebook link. Participants use their own project and credentials. Ask for their project link only if they want you to read progress. Public teaching projects must contain only the supplied public or fictional data.
4. Copy the [facilitator monitor](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view) into your project. Add the project roster, select the workshop, then use **Save roster and filters** and **Refresh progress**. [Monitor setup](setup.md#read-participant-progress) covers filtering and saved rosters.
5. Confirm the spending explanation: the default $8 notebook inference allowance is adjustable. Notebook compute, ARIA, and native tag judging are separate. A recorded demonstration requires none of those live calls.

## Lead each exercise

Start with the bundled example before authentication. Ask what should change, then follow the same input through the code and its result. Leave the exercise slide visible while people edit. Name the notebook step, free check, and explicit Run control; do not ask everyone to rerun a whole notebook to recover one failed action.

After execution, ask someone to explain one intermediate value and open the Forge record that supports it. The two scheduled ARIA stops check interpretations of saved work. Use their recorded investigations when live access is unavailable; ARIA is not required to continue coding.

The monitor is read-only. Missing progress means unknown, so ask what the participant sees before diagnosing a failure. It reads progress from the participant projects in your roster. Sharing-link visits are a separate measure and do not establish that someone copied or completed a notebook.

## Recover and finish

- If execution completed but an upload failed, use publication-only retry. Do not rerun a model or training job to obtain a dashboard.
- If execution stopped, follow [saved-work recovery](setup.md#resume-or-recover). A request with an uncertain outcome needs inspection before another attempt.
- If time or access prevents completion, switch to the labeled recorded example and preserve the participant's unfinished draft. Recorded results do not describe their edit.
- Before ending, ask participants to open one saved result, identify the version that produced it, and state what they would test next. Confirm checkpoint uploads before replacing a runtime. In Airline, verify automatic tagging is off.

Keep the [recorded improvements, ties, and failures](recorded-results.md) intact. The detailed runbooks linked from each quick guide own the full schedule, exact controls, and teaching notes.
