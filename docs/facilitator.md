# Solar Forecasting Lab facilitator guide

The research lab is fictional; the satellite observations are real. Start with the team’s four notebooks named `final` and a score nobody can reproduce. Then open the GOES measurements and AIA images. The workshop’s first job is to make a forecast whose code and data another person can find.

Before class, open the templates from an attendee account, check compute and inference access, and download the teaching data. Add participant project links to the progress monitor. Keep the [recorded deck](https://ash0ts.github.io/forge-workshop-kit/solar/) available if someone cannot run a step.

Use the [visual sequence guide](visual-sequence.md) beside this schedule. For each selector, ask participants to identify what changed and what stayed fixed. A different timestamp changes the case; toggling normalization changes the displayed input units; selecting a branch changes the record being inspected. None of these actions starts training.

## Four-hour schedule

Leave each exercise slide on screen while participants work. Give them time to try the code before opening a hint or worked answer.

| Minutes | Introduce the task | Ask participants to show you |
| --- | --- | --- |
| 0–15 | “Copy the notebook into your project. We’ll send a small trace first, so you can check where your work will appear.” | Their own conversation in Agent Lens and the arguments of its tool call. |
| 15–40 | “Predict the measurement 30 minutes from now by copying the latest reading. Before running it, check which timestamps become inputs.” | A forecast beside the observed value. Use the date diagram to explain why a window crossing a data gap or split boundary must be excluded. |
| 40–65 | “Now save enough information for a teammate to run this again.” Explain that a W&B Artifact stores a versioned collection of files. | The run’s code, settings, data version, and predictions. |
| 65–90 | “We’ll try six configurations using the models already written. Compare validation error before choosing one.” | Two runs in the Sweep, the setting that differs, and their learning curves. Keep test dates closed. |
| 90–100 | Take a ten-minute break after checking that the checkpoint uploaded. | Saved drafts and completed work. |
| 100–135 | “Now predict a future image. One model predicts the whole image; the other predicts a correction to the current image.” | The input, prediction, observed future, and error image for the same timestamp. |
| 135–160 | “So far, we’ve chosen the models and settings. Give the agent the code and validation results and ask it for two changes.” | Each proposed diff and an explanation of the behavior it should change. Open the agent’s evidence-read call in Agent Lens. |
| 160–195 | “Train both versions with the same settings. Compare their errors, ask the agent which changes to keep, and test that choice. Repeat once.” | Which code ran, its validation result, and the reason for choosing or rejecting it. |
| 195–225 | “We’ve finished choosing versions. Freeze them and evaluate on the reserved dates.” | Matching forecasts from each version, including a case where the average score hides a visible error. |
| 225–240 | “Write what changed and whether it helped. Then reopen one result using its saved files.” | A conclusion linked to the code, predictions, and metric that support it. |

At transitions, ask participants to explain one result to a neighbor. Use help requests to find people who are blocked. The monitor cannot tell whether someone is thinking, editing, or disconnected just because they haven’t published an update.

## Discuss the recorded result

Follow the residual-head initialization and training-loss changes into their validation runs, then open the final image predictions. Error fell from 0.122442 to 0.110011, a 10.2% reduction from the manual model. Ask which parts of an image improved and which still look wrong.

Keep the scope beside that number: one rehearsal, one seed, and overlapping windows from two reserved days. We haven’t established that the same edits will help other dates or training runs. The GOES model did worse than persistence; use its learning curve and predictions to discuss why a completed training run can still produce a poor forecast. The [evidence review](solar-evidence.md) contains the calculations.

## If someone gets stuck

- **Code check fails:** ask them to read the expected and returned values. Offer the first hint before the solution.
- **Access check fails:** distinguish project permissions, inference access, and notebook compute. Continue with local code checks or labeled recorded results while access is resolved.
- **Training or inference fails:** open the error. Do not switch models or claim the recorded result came from their code.
- **Publication fails:** use the saved notebook comparison. Retry uploading the result without rerunning the experiment. Native EvalTables uses the Weave backend. If publication fails, keep working from saved results and retry publication separately.
- **Time runs short:** stop starting new runs and walk through the saved example. Ask participants to explain the proposed change and how they would test it.

Close by asking each participant for one next experiment and the result that would convince them to keep the change.
