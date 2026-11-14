# Solar Forecasting Lab facilitator guide

This is one six-hour session for people who know basic Python and for developers who have already trained models. Teach the numerical example first, then inspect the implementation. Experienced participants should help explain the assumptions, rather than skip directly to a lower score.

The research lab is fictional; the observations are real. The lab has four notebooks named `final` and a score nobody can reproduce. Its assignment is to predict the next observation better than copying the current one, and save enough information for a colleague to repeat the comparison. GOES measurements teach the experiment stack. AIA images then give the research agent code to edit and forecasts people can inspect.

Before class, open the templates from an attendee account, verify compute and inference access, and download the teaching data. Add participant project links to the read-only progress monitor. Keep the [recorded deck](https://ash0ts.github.io/forge-workshop-kit/solar/) available for discussion if a live action fails. Attendees use their own project and credentials. No facilitator gateway is needed.

## Six-hour schedule

The schedule includes two short breaks and a thirty-minute meal break. Leave the exercise slide visible while participants code. Most diagrams reveal one operation per click; use Back when someone asks about an earlier value.

| Minutes | Lead the room through | Completion check |
| --- | --- | --- |
| 0–25 | Introduce the weekly forecast review, both satellite instruments, and the two prediction tasks. Copy the notebook, connect, edit `instrument_tool`, and send the first trace. | Each participant finds the field they added in their own Agent Lens span. |
| 25–65 | Follow the actual 01:00 UTC GOES window through its history, target, date split, input normalization, persistence forecast, and error. Implement `persistence_forecast`. | Explain why the standardized input is not the persistence prediction. Reject a window crossing a split or gap. |
| 65–95 | Explain a training loss, gradient, optimizer step, and separate validation score. Complete `training_loss` and `my_flux_mae`. Inspect `run_training` and how it saves source and outputs. | Show the difference between predicting, updating weights, and recording results. Find the source and prediction attached to one execution. |
| 95–110 | Fifteen-minute break. Save drafts and completed work. | Reopening a completed result does not train again. |
| 110–155 | Read batch axes and indexing. Calculate one linear unit, then follow the MLP and CNN shapes. Run six configurations. Inspect the historical GOES failure and the worked repair. | Compare the saved configuration, forecast, loss curve, and persistence. Explain which settings differ and which model weights were trained. |
| 155–200 | Introduce image units and tensor shapes. Implement residual prediction and masked MAE. Use the public pixel fixture, then train the convolutional and residual models. | Match input, prediction, target, and error at one timestamp. Explain the per-image reduction before averaging images. |
| 200–230 | Thirty-minute meal break. Keep the selected image comparison saved. | Participants return to their own unchanged draft and results. |
| 230–260 | Build the research-agent context. Explain which program receives training targets, validation evidence, and final-test records. Complete `select_validation_evidence`; inspect the actual evidence-read span. | A participant can identify the fields sent in the request and the notebook operation that read their saved provenance. |
| 260–310 | Review two proposals, test both, compare, request a composition, test it, and adopt or retain. Repeat once. Explain the recorded loss edit and zero-initialized residual head. | Show a diff, its actual training run, the validation result, and the reason the notebook kept or rejected that version. |
| 310–320 | Ten-minute break before final evaluation. Save the selected version. | No new code choice is made from final-test results. |
| 320–345 | Freeze source and weights; evaluate the reserved dates. Inspect aligned cases in the notebook and EvalTables. Compare the recorded seed outcomes and preserve the unsuccessful GOES run. | Distinguish one forecast from an aggregate, repeated seeds from independent agent discoveries, and measured error from publication status. |
| 345–360 | Reproduce one saved result and write the Report. Explain the outcome to another participant. | Open the source, weights, forecast, and metric supporting the conclusion, then propose one next experiment. |

For each exercise, give participants time to attempt the function before opening the hint. Ask them to explain one result to a neighbor at transitions. A missing progress update means unknown; the monitor cannot tell whether a participant is thinking, editing, or disconnected.

## Questions that reveal whether the explanation worked

Use these as discussion prompts, not additional paid exercises.

- **After loading:** “At 01:00, which numbers can the forecast use? Where is the 01:30 observation stored?” Ask experienced participants why overlapping windows make a random train/test split misleading.
- **After normalization:** “What changed when we standardized the input?” Have someone calculate the displayed XRS-B value from the saved training mean and standard deviation. The target remains in log-flux units.
- **After the shape check:** “What does `x[:, 1, -1:]` return?” For an implementation check, compare `(B, 1) - (B, 1)` with `(B, 1) - (B,)` in a small local array. Explain broadcasting before scoring the wrong pairs.
- **After the optimizer explanation:** “Which line changes the weights?” Advanced participants can explain gradient accumulation, why the step count is not an epoch count, and why `eval()` and `no_grad()` do different jobs.
- **After image scoring:** “Why does the two-image fixture score 1.5 rather than 1.8?” The answer is equal weight per image after each mask-normalized score, not pooling every included pixel.
- **After the loss edit:** “What hypothesis does changing squared error to absolute error test?” Matching a training objective to the evaluation metric does not guarantee a better forecast.
- **After zero initialization:** “If the correction starts at zero, how can it learn?” Only the final layer is zeroed. Its weights can receive gradients from the earlier features; gradients reach earlier layers after the output weights move.
- **Before requesting a proposal:** “Who chooses the evidence-read operation?” The notebook does. It gathers the selected validation record, then sends current source and allowed evidence in one proposal request. Forecast images remain available to participants; they are not sent to the research model.
- **After composition:** “Did the agent select code, or did we test and adopt it?” The proposed source must run before the notebook compares its validation error with the parent.
- **At the final comparison:** “How many independent discoveries did we repeat?” The recorded three-seed check repeats fixed code, not three independent agents searching for an edit.

Keep arithmetic examples visibly separate from actual observations. The small weighted sum and gradient update teach mechanics. They are not logged parameters or optimizer updates from the rehearsal.

## Explain the recorded outcomes

Follow the actual `.square()` to `.abs()` change and the output-layer initialization through their diffs, training runs, and predictions. In the original image rehearsal, masked MAE fell from **0.122442 to 0.110011**, a **10.15%** reduction versus the manual model. The score covers **199 overlapping windows from February 13–14 with one seed**.

The fixed-code repetition improved seeds 17 and 29 and slightly worsened seed 43. Its mean reduction was 5.79%, but the predeclared requirement that every seed improve failed. Show that regression beside the aggregate. These are repeated training recipes, not repeated agent discoveries or new solar periods.

The original GOES model scored **2.468975**, worse than persistence at **0.192706**. Keep that failed recipe visible. The later repair combines persistence residuals, consistent output scaling, absolute training loss, zero head initialization, and 1,200 updates. It passed its three-seed check, but those final dates had already been inspected. Describe it as a teaching retest. The comparison does not isolate which individual repair caused the gain.

Use the [qualification outcomes](solar-qualification.md) and [evidence review](solar-evidence.md) for exact runs and calculations. Learners' edits require their own executions; a recorded result is never the outcome of an unexecuted draft.

## If someone gets stuck

- **Code check fails:** read the expected and returned values together. Use a small array before adding the whole training run.
- **Project or inference access fails:** identify the failed service. Continue with free checks or clearly labeled recorded results while access is repaired.
- **Training or inference fails:** open the saved error. Keep the fixed model and settings visible; do not silently substitute a model mid-comparison.
- **Upload fails:** use the saved notebook result. Retry publication without training or requesting another proposal. Native EvalTables uses the Weave backend; a publication failure does not change the measured score.
- **Time runs short:** stop launching work. Walk through a recorded diff, execution, and comparison, then let participants explain how they would test their draft. Keep its unexecuted status explicit.

End with each participant's next experiment and the result that would make them keep the change.
