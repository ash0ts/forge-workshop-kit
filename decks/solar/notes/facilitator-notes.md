# Solar Autoresearch presenter notes

## 1. Build a research loop.<br>Then give it an agent.

0:00

We’ll build two small forecasts from real solar observations. First we’ll write and track the experiments ourselves. Then we’ll let a research agent propose changes to the image model’s code. The pixel lab is an illustration; the observations and recorded results come from the workshop dataset.

## 2. Your team has a promising result.

0:01

Imagine a teammate says the new model is better, but can only find a screenshot and several notebooks called final. That’s our fictional opening. Ask the room what they would need before trusting or repeating the comparison.

## 3. Two forecasts from real solar observations

0:02

Read the instruments before discussing models. The left plot measures solar X-ray flux; the right image records extreme-ultraviolet light at 171 Å. These are real February 2014 observations, prepared at a small scale for CPU teaching. The image uses false color. We are testing forecasts, not predicting a reliable flare warning.

## 4. First reproduce a result. Then try to improve it.

0:03

The reason for building the experiment stack comes first: we need to know whether a change helped and be able to repeat it. Once that works, the same loop can test code proposed by an agent. The language model stays fixed. The small forecasting model trains normally.

## 5. Build a forecast, then test changes to its code

0:04

Follow this sequence in the notebook. You’ll change Python, run a check, execute the experiment, and open the resulting evidence in Forge. A change that fails to improve the forecast is still something we can investigate.

## 6. Copy the notebook into your Forge project

0:05

Allow participants to get their own copy open before continuing. Run all stale cells creates the controls; it does not press the exercise run buttons. Hosted Forge supplies authentication, but attendees still need their own project and account access. Use fictional or public teaching data in a public project.

## 7. Copy the notebook into the project you will use

0:05

Show the native copy dialog. The copied notebook uses its destination project. A laptop uses manual entry. Confirm the project before executing. The browser preview limitation remains separate from notebook execution.

## 8. Run the same notebook on your laptop

0:06

Hosted participants can skip this slide. On a laptop, install Git and uv, clone the repository, and run these commands. Authenticate in the terminal and keep that terminal open while marimo runs. There is no extra workshop service to start.

## 9. Check the compute and inference settings

0:06

Check these settings before running anything. The eight-dollar allowance applies to inference, while hosted notebook compute is separate. The research agent uses GLM-5.3-Flash with temperature 0.2, JSON output, and up to 16,384 output tokens. If that model is unavailable, stop and inspect the error rather than changing models mid-comparison.

## 10. Wrap one operation, then inspect what you recorded

0:07

Conversation identifies the execution. Turn holds the mission. Tool records one operation. The attribute line is the learner edit, not a second call. Actual instrumentation also supplies start and end timestamps and records exceptions. Run the free check, send the setup trace, then find the same field in Agent Lens.

## 11. Connect and inspect your first tool call

0:08–0:15

Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding.

## 12. Find the field your code added to the span

0:15

The exercise is complete when the participant can find their own attribute in their own tool span. Here is the recorded reference. The tool arguments, result, and duration describe one actual operation. The same instrumentation function records later training calls.

## 13. Predict X-ray flux 30 minutes ahead

0:15

Read the timeline from left to right. The model gets sixty minutes of observed flux, then predicts the reading thirty minutes after now. We work in log10 flux, so the error is in transformed units rather than raw watts per square metre.

## 14. Use earlier dates to train, later dates to test

0:17

Train on February 1–10, choose models using February 11–12, and leave February 13–14 for the final comparison. Every input and the target of a window must belong to one partition. Fit normalization using training data only.

## 15. Leave out windows with missing observations

0:19

February 8 is absent from the prepared GOES source archive. A window that needs those readings cannot be used. Filling the absence with zero would tell the model that the instrument measured zero flux, which it did not.

## 16. Inspect a solar observation with SunPy

0:20

Open the representative FITS file and inspect its date, wavelength, and unit. Training uses prepared arrays so the class does not wait for archive downloads. The dataset includes the acquisition and preprocessing records, so we can trace those arrays back to the public observations.

## 17. Inspect the observations before training

0:21–0:27

Give participants six minutes. Have them explain one forecast window to a neighbor: which observations go in, which observation is the target, and which dates it belongs to. No training is needed yet.

## 18. Start by copying the latest reading

0:27

Persistence means predicting that the latest value will stay the same. Solar observations are correlated over time, so this simple baseline can be hard to beat. It gives us a comparison before we spend time training a network.

## 19. Measure how far the prediction missed

0:29

For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score.

## 20. Write and test persistence

0:30–0:40

Allow ten minutes. Let participants attempt the function before opening the answer. Ask them to find an interval where the real flux changed while persistence kept the previous value. That is a concrete error another model could try to reduce.

## 21. Save what changed between runs

0:40

Use these as possible explanations for a changed score, not claims about this rehearsal. If code, data, or training time differs, we need to know that before deciding why the score moved.

## 22. Which setting changed between these runs?

0:41

These are two recorded GOES runs. Before revealing the settings, ask what the scores let us conclude. Then click Show active settings. Both runs used the same source and budget, but their learning rates differed.

## 23. These runs used different learning rates

0:42

The learning rate changed from .001 to .003. Data, source, seed, steps, and batch size stayed the same. Both errors were worse than persistence, so choosing the smaller of these two errors still leaves a poor forecast.

## 24. Turn observations into a forecast

0:42

Start with the forecast itself: observations enter the model and it produces a number or an image. We’ll add the records around this process one piece at a time.

## 25. Save the model and training code with the run

0:43

The model and training functions are code we can change. Save the particular source used by this run, because the notebook may be edited again tomorrow.

## 26. Use the same scoring rule for every model

0:44

Keep the target, dates, and primary metric unchanged while comparing models. Otherwise a lower score might come from an easier test rather than a better forecast.

## 27. Save the files needed to repeat the run

0:45

A W&B run stores settings and metric history. A W&B Artifact stores a versioned bundle of files. Here that means the data, source, weights, and predictions needed to repeat or inspect a result.

## 28. Save code and outputs with each training run

0:47

This shortened example shows where saving sits around training. The notebook’s run_training function runs your source, then saves the result. If that same stage has already completed, the saved result can be restored instead of training again.

## 29. Restore a completed run after a restart

0:49

The local completion record tells the notebook which work finished. The checkpoint Artifact stores a copy in your project. If the runtime is replaced, restore the checkpoint before continuing. An upload failure can be retried using the local files.

## 30. Write the loss and metric

0:50–1:05

Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example.

## 31. Three ways to change an experiment

1:05

Point to the exact change in each row. A Sweep changes values within the current program. Comparing an MLP with a CNN selects an implementation we wrote. The research agent will edit the program itself. Every version still needs the same data partitions and score.

## 32. Compare six model configurations

1:07

These six configurations are the workshop defaults: two model families, three settings per family, seed 17, batch size 32, and sixty training steps. It’s a short CPU exercise, so inspect whether the models have trained enough before drawing an architecture conclusion.

## 33. Run the configurations through W&B Sweeps

1:09

W&B Sweeps assigns each configuration to a run. Our training function does the fitting and saves its outputs. This is a shortened excerpt; the notebook contains the entity, project, and complete configuration setup.

## 34. Compare the six configurations in Forge

1:10

Use the latest rehearsal Sweep pzigourv. Start with two width-16 MLP runs, then compare their learning rates, error, and runtime. All six models lost to persistence. Do not infer an architecture conclusion from this short training exercise.

## 35. Read the loss curve before choosing another model

1:11

This is the actual selected GOES run, not an invented trend. Its loss is still falling at sixty steps. Inspect its predictions and fixed validation metric too. A falling training loss alone does not tell us the future forecast is good. Longer training is a concrete follow-up, but this workshop did not run it.

## 36. Run six configurations and inspect one forecast

1:15–1:30

Allow fifteen minutes. Ask participants to predict which configuration will win before running the search. After it finishes, have them explain one result from the loss curve and forecast. Keep failed runs visible so the comparison accounts for what happened.

## 37. The experiments can wait ten minutes.

1:30–1:40

Take ten minutes. Confirm saved work is visible before leaving. No background experiment is required during the break.

## 38. Predict the solar image one hour ahead

1:40

Now we give the model images from sixty minutes ago and now, and ask for the image sixty minutes ahead. The AIA 171 Å arrays are 64 by 64 pixels so the exercise can run on CPU.

## 39. Save image experiments the same way

1:42

The inputs are now images, but we still save the same kinds of records: data, code, settings, weights, and predictions. Image values use normalized log1p intensity, so their errors have a different scale from the GOES errors.

## 40. See exactly which images become input and target

1:44

Read the observation times. Channel zero is the earlier image; channel one is the current image. The third image is the future target. These are three real observations from a training window, not three outputs of an AI image generator.

## 41. Two image channels enter. One forecast comes out.

1:46

Here the network predicts the entire future image. A batch has two input channels, each 64 by 64. The output has one channel. The forward function returns self.net(x). Keep this geometry in view for the residual reveal.

## 42. Let the current image carry what has not changed

1:48

The network now predicts a correction. The arrow around the network copies the current input image and adds the correction to it. In x[:, 1:2], the slice keeps the channel dimension, giving batch by one by 64 by 64. Zero correction returns persistence exactly. That is the behavior participants add to forward.

## 43. Write the addition you just traced

1:49

The diagram and code describe the same addition. Ask participants why x[:, 1] would remove a dimension and why x[:, 1:2] preserves it. The notebook implementation also branches on architecture so the convolutional comparison still returns only the network output.

## 44. Count errors on the solar disk

1:50

This is a diagram of the scoring calculation, not a forecast. The fixed mask assigns one to disk pixels and zero outside. Multiply absolute errors by the mask, average over the selected pixels per image, then average images. A changed off-disk pixel must not affect the score.

## 45. Write the scorer, then test a deliberate miss

1:51

Run the three local examples before training. They explain what the scorer measures. The participant writes this development scorer, and the protected primary scorer checks the comparison with the same published rule. Missing or invalid predictions are not zero error.

## 46. Train with one loss; compare with a fixed metric

1:52

The training loss supplies gradients that update weights. The evaluation metric tells us how the forecast compares with another model. We can try a different training loss while keeping the scoring rule fixed. That will be one of the agent’s recorded proposals.

## 47. Compare forecasts for the same validation case

1:54

The same current image and observed future appear in both rows. The convolutional forecast is above, residual below. The figure uses the first accepted case, not a selected success. Colors use the same scale across both rows. A single image is an example; the validation score includes all 142 windows.

## 48. Implement and compare the image predictors

1:55–2:15

Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed.

## 49. Give the research agent your code and results

2:15

Read this transition as one explanation. Until now, we wrote the models and chose the settings ourselves. We’ll now ask an agent for two code changes, inspect them, and use the experiment we built to test them. The selected code becomes the next round’s starting point.

## 50. The agent edits code. The forecast model learns weights.

2:17

There are two models with different jobs. The language model writes Python and keeps the same weights. The small forecasting network trains weights using that Python and the earlier solar observations. Validation evidence returns to the research agent for another proposed edit. This is code-directed research, not post-training the language model.

## 51. Decide which files the agent may change

2:19

The agent can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox.

## 52. Send the code, settings, and validation results

2:21

Send the files and settings that produced the current result, plus its validation outputs. A default learning rate in source may differ from the value used in the run. The agent needs the active values to propose a relevant change.

## 53. Follow the agent’s work in Agent Lens

2:23

Open the research conversation in Agent Lens. Start with the mission, then find the evidence-reading tool and the returned code. Follow a training call to its result or error. Compare that sequence with the agent’s explanation of its change.

## 54. Read the evidence that went into the proposal

2:24

Open read_validation_evidence. Find the residual architecture, forty training steps, seed seventeen, and parent validation error. Then inspect the returned proposal. This request initially exhausted its output budget and used a saved retry; that is an execution event, not a change in forecasting quality.

## 55. Choose the evidence for the research agent

2:25–2:40

Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request.

## 56. Ask for two changes to the same starting code

2:40

Both candidates start from the same code and settings. This borrows Propose–Probe–Compose from Harness². Here the probes train forecasting models and give validation scores to the editor, so it is a teaching adaptation rather than the paper’s exact task protocol.

## 57. The first proposal changes one loss operation

2:41

This is the actual first-round Candidate A edit in v0.3.0. It changes the training objective, while the evaluation scorer remains fixed. The alternative candidate retains the original squared loss. The diff establishes the proposed change; it does not establish an improvement until both run.

## 58. Train and score each candidate

2:42

Train each candidate on the same training dates and compare its validation error. If one fails before producing a forecast, inspect the error and leave its score missing.

## 59. Ask the agent which changes to keep

2:44

The agent reads both test results and can keep one candidate, combine changes, or retain the starting code. The dashed lines mean that it reviewed the results. They do not mean both sets of changes were merged.

## 60. Test the version the agent chose

2:46

Run the chosen code before accepting it. Combining two changes can behave differently from either one alone. If the unchanged version is retained, testing it creates another execution of the same code.

## 61. Open the training call behind the chosen version

2:47

The operation trained and validated the selected source. Find the returned score and compare the run to the saved source artifact. An error metric of 0.110916 is the forecasting metric, not a tool failure. If a span actually failed, inspect its exception separately.

## 62. Start round two from the selected version

2:48

The selected code and a short lesson enter round two. The agent now proposes changes on top of that version. We are still forecasting the same image task and selecting with the same validation metric.

## 63. Propose and test two changes

2:50–3:00

Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice.

## 64. Test the selected code, then begin round two

3:00–3:15

Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work.

## 65. Follow one proposal through the branch diagram

3:15

Click a candidate, its test, and the selection step. Ask someone to explain what happened along that path. This diagram explains the process; the notebook’s branch view opens their actual files and results.

## 66. Freeze both the code and the trained weights

3:17

Select using validation, then freeze the code and its trained weights together. The final step loads those weights and predicts later dates; it does not keep fitting or ask the agent which final score it likes. Once you inspect final results, further editing needs a new reserved test for a new comparison.

## 67. Load the saved weights to make final predictions

3:19

Load the saved weights, switch to evaluation mode, and predict without an optimizer step. Final evaluation measures the selected trained model; it does not train another one.

## 68. Compare predictions for the same times

3:21

Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Native EvalTables was unavailable during the rehearsal, so the notebook and Weave comparison remain available; publication can be retried separately.

## 69. Test the selected models on reserved dates

3:25–3:45

Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies.

## 70. In this rehearsal, image error fell 10.15%

3:45 · RECORDED REHEARSAL

The selected agent code combined the absolute training loss from round one with a zero-initialized residual head from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods.

## 71. Compare one saved forecast at the same time

3:46 · RECORDED REHEARSAL

This figure is regenerated from the fresh v0.3.0 saved predictions. Compare manual and agent-selected forecasts on exactly the same case. The fixed error scale helps show differences without changing the colors between rows. The aggregate score includes all 199 accepted final windows.

## 72. The selected GOES forecast lost to persistence

3:47 · RECORDED REHEARSAL

These are the fresh saved final GOES predictions. The selected sixty-step neural model misses badly, while persistence follows the observed flux much more closely. The training curve suggests a longer equal budget as a follow-up. That follow-up has not been run, and the failure does not establish that neural forecasting cannot work.

## 73. Read the saved score for one image in Weave

3:48

This expanded native Weave row is the first final agent-selected image, file_index zero. Prediction mean is −1.760701 and target mean is −1.759181, but masked MAE is 0.109328. Differences between bright and dark pixels can cancel in a mean. The scorer instead takes each pixel’s absolute error before averaging. Open the saved array to see the forecast. The notebook supplies the aligned comparison; this is not native EvalTables.

## 74. Check that the saved source contains both selected edits

3:49

This is execution-f7550caa1639e8366efbf9d84a782289, the exact selected round-two composition. Open the source and weights together. The final evaluation loaded these weights. A different source file with the same model label would not reproduce this experiment.

## 75. Write down what changed and whether it helped

3:50–3:58

Allow eight minutes. Ask participants to name a change, report what happened, and include a remaining miss. A negative result is fine. If publication fails, save the conclusion and retry the upload without rerunning the experiment.

## 76. Write what changed, what helped, and what still missed

3:58–4:00

Close with the measured result and a concrete next test, such as a longer equal GOES training budget or new reserved dates for the image change. The recorded result is one seed across two reserved days. Participants should explain their own result, including failures and remaining misses.

## 77. Reference and worked answers

REFERENCE

These pages are optional answers and recorded examples. Open an answer after participants have tried the exercise. Use the return link to get back to the teaching sequence.

## 78. Put the attribute inside the tool scope

WORKED ANSWER

The attribute is attached inside the Tool scope. The complete notebook function also supplies its call identity and outer conversation. Use the operation’s timestamps so Agent Lens shows when the work happened, not when it was uploaded.

## 79. Return a copy of the latest observation

WORKED ANSWER

The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.

## 80. Take the mean of the absolute errors

WORKED ANSWER

Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.

## 81. Compare the settings and loss curves

WORKED ANSWER

Open the configuration and curve for two runs. Find the settings they share and the value that differs. If training failed, inspect the error rather than assigning a score to a forecast that does not exist.

## 82. Average the error inside the disk mask

WORKED ANSWER

The mask selects the solar disk. Compute the sum and count per image, then average across images. Check identical arrays, a constant one-unit difference, and a difference only outside the mask.

## 83. Add the correction to input channel 1

WORKED ANSWER

Channel zero is the earlier image and channel one is the current image. Add the correction to channel one. With a zero correction, this function returns the current image exactly.

## 84. Return validation evidence only

WORKED ANSWER

First check that the record belongs to validation. Then return only the listed evidence fields. The current source is supplied separately. The final-test example should raise an error before the agent sees it.

## 85. Pass the candidate’s code to training

WORKED ANSWER

Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.

## 86. Use the saved model without training it again

WORKED ANSWER

The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.

## 87. Round 1: absolute loss versus the unchanged model

RECORDED REHEARSAL

The alternative is a real KEEP decision and it is still tested. Candidate A changes only the loss and lowers validation error in this run. The composition keeps A. This is one seed, not evidence of a repeatable effect.

## 88. Round 2: start the correction at zero

RECORDED REHEARSAL

This is the second-round selected edit in v0.3.0. The last convolution starts at zero; before training, the residual correction is zero. The model begins at persistence and learns a correction. Its probe and separate composition test produce the measured validation score.

## 89. Round 2: a plausible sampling change did not help

RECORDED REHEARSAL

Candidate B changes the batch sampling to seeded permutations. Its validation error is essentially the same as the parent and slightly higher. The composition keeps zero initialization and rejects the sampling change. Do not attribute a benefit to an untested combination.

## 90. Open the recorded research conversation

RECORDED REHEARSAL

Open the proposal conversation and follow the evidence-reading tool to the candidate source. The downloadable records contain the same decisions and scores if the native view requires sign-in.

## 91. When a service is unavailable

REFERENCE

Start with the failed operation. An authentication problem needs corrected access. A failed training run needs its saved error inspected. An upload failure needs a publication retry. Native EvalTables returned HTTP 500 during this rehearsal; the notebook and Weave comparisons are still available.

## 92. Four-hour session

REFERENCE

Use these times to pace the room. They include coding and discussion, not just execution. If a section takes longer, use its recorded example for discussion rather than claiming a learner’s unexecuted code produced that result.

## 93. Keep working in your own project

REFERENCE

Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.