# Solar Forecasting Lab facilitator guide

The lab is fictional; its solar observations are real. Open with the research team trying to reproduce a promising score from a notebook called `final`. Then show the GOES measurements and AIA images the participants will forecast. The office setting belongs to the separate Pending workshop.

Before class: verify public templates, run the access check from an attendee account, download the data once, and open the monitor with participant project links. Ask everyone to check their own notebook compute and inference access. Keep the recorded fallback available.

| Minutes | Say and do | Check before moving on |
| --- | --- | --- |
| 0–15 | “This is your project. I can see progress you publish; I cannot operate your notebook.” Copy, connect, instrument a small operation. | Everyone can open their own Agent Lens conversation. |
| 15–40 | “Before predicting the future, check the timestamps.” Build persistence and inspect gaps. | Learner explains why a window crossing a gap is excluded. |
| 40–65 | “Which code and data produced that number?” Inspect source, scaling, split and run metadata. | A partner can locate the exact source and data version. |
| 65–90 | “These are different settings, not an agent inventing a new model.” Run six bounded configurations. | Compare validation quality and cost without opening test results. |
| 90–100 | Break. | Checkpoint has uploaded. |
| 100–135 | “The records stay the same shape; the prediction becomes an image.” Edit and compare the two models. | Open input, prediction, observed future and error. |
| 135–160 | “Now the agent can change the program.” Inspect its prompt, tools and two proposed diffs. | Each participant can explain a proposed behavioral change. |
| 160–195 | Probe, compose, test, retain a lesson, then repeat. | Adopted source matches an actual execution; rejected versions remain visible. |
| 195–225 | “Stop choosing. Freeze the versions and open the reserved dates.” | Compare all final versions on matching cases. |
| 225–240 | Write the conclusion and reproduce one result from its artifacts. | One claim, a code change, an execution, and a score are linked. |

At each transition, ask participants to explain one result to a neighbor. Use help requests to find blocked participants, not model scores to rank them. Missing progress is unknown; ask before assuming someone is stuck.

If time runs short, stop launching additional experiments and inspect saved evidence. Label a recorded walkthrough as recorded. Do not suggest a learner's unexecuted code produced those results.

For the recorded improvement example, follow the residual-head initialization and loss edits into their validation runs, then open the frozen image predictions. Final error fell from 0.122442 to 0.110011, a 10.2% relative reduction from the manual model. Compare the largest and smallest changes on matching forecasts, then inspect where pixel errors remain. These are correlated windows from two reserved days, not independent research trials. Keep the unsuccessful GOES result in the comparison. The [evidence review](solar-evidence.md) records the source and calculation.

If publication fails, continue with the local comparison. Retry saved publication later. If inference fails, show the real error and use recorded evidence; do not change models silently. If a model regresses, inspect the prediction and keep the regression in the comparison.
