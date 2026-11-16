# Run Solar Autoresearch

**Six hours · basic Python · forecasting, experiment tracking, and agent-written research code**

A research lab needs a forecast someone else can reproduce before its weekly review. Participants start with persistence, train small models, then test an agent's proposed code changes. GOES-15 measurements and AIA 171 Å images are real satellite observations from February 2014; the lab is fictional.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/solar/) · [Start notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/solar.html) · [Full runbook](facilitator.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Load the teaching data through its explicit control and open one saved forecast with its source, weights, and predictions. The required training runs on CPU. Rehearse the intended attendee account and runtime before a class; the full workshop remains a technical preview.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–1:35 | Inspect the forecast window, connect and trace, implement persistence and scoring, then explain training and saved files. |
| 1:35–1:50 | Break. |
| 1:50–2:35 | Run one Sweep trial, inspect its curve and forecast, then complete the other five. Write a diagnosis before the first ARIA investigation or worked repair. |
| 2:35–3:20 | Implement image prediction and masked error; compare predictions at the same timestamp. |
| 3:20–3:50 | Meal break. |
| 3:50–5:10 | Select validation evidence and complete two rounds of proposal, diff review, training, and selection. |
| 5:10–5:20 | Break. |
| 5:20–6:00 | Freeze source and weights, evaluate reserved dates, reproduce a result, check the conclusion, and publish it. |

Keep the agent's fixed language model separate from the forecasting models whose weights train. Ask participants to locate the source line responsible for one tensor shape or error value before opening the corresponding run in Forge.

## Give a ten-minute demo

Follow the [recorded walkthrough](current-demo-guide.md#solar-forecasting-in-ten-minutes): aligned forecast panels, a Sweep, an actual agent diff, its training call, and the saved weights. End by separating the measurement and image outcomes.

## If live work stops

Use saved curves, diffs, and predictions. Do not rerun training to repair an upload. Preserve the failed original GOES recipe and label its later repair a teaching retest. The fixed image edit improved two qualification seeds and regressed on the third; the mean gain does not establish that it always helps.
