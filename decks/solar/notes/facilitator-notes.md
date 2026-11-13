# Solar Autoresearch presenter notes

## 1. Build a research loop.<br>Then give it an agent.

0:00

We’ll build two small forecasts from real solar observations. First we’ll write and track the experiments ourselves. Then we’ll let a research agent propose changes to the image model’s code. The pixel lab is an illustration; the observations and recorded results come from the workshop dataset.

## 2. Your team has a promising result.

0:01

Imagine a teammate says the new model is better, but can only find a screenshot and several notebooks called final. That’s our fictional opening. Ask the room what they would need before trusting or repeating the comparison.

## 3. Forecast the next solar observation

0:02

Our first task uses the last hour of GOES X-ray measurements to predict flux thirty minutes later. The second uses two AIA images to predict another image one hour ahead. SunPy helps us inspect the observation times, wavelength, and units.

## 4. Can an agent improve the research code?

0:03

Once we can run and compare an experiment, we can give an agent the code and ask it to propose a change. We’ll train the small forecasting models as usual. The language model writing those proposals stays fixed.

## 5. Build a forecast, then test changes to its code

0:04

Follow this sequence in the notebook. You’ll change Python, run a check, execute the experiment, and open the resulting evidence in Forge. A change that fails to improve the forecast is still something we can investigate.

## 6. Copy the notebook into your Forge project

0:05

Allow participants to get their own copy open before continuing. Run all stale cells creates the controls; it does not press the exercise run buttons. Hosted Forge supplies authentication, but attendees still need their own project and account access. Use fictional or public teaching data in a public project.

## 7. Run the same notebook on your laptop

0:06

Hosted participants can skip this slide. On a laptop, install Git and uv, clone the repository, and run these commands. Authenticate in the terminal and keep that terminal open while marimo runs. There is no extra workshop service to start.

## 8. Check the compute and inference settings

0:06

Check these settings before running anything. The eight-dollar allowance applies to inference, while hosted notebook compute is separate. The research agent uses GLM-5.3-Flash with temperature 0.2, JSON output, and up to 16,384 output tokens. If that model is unavailable, stop and inspect the error rather than changing models mid-comparison.

## 9. Record a tool call in Agent Lens

0:07

A conversation groups the work. A turn records a request, and a tool span records one operation and its result. The notebook supplies the outer scopes. You’ll edit the tool scope and add an attribute you can then find in Agent Lens.

## 10. Connect and inspect your first tool call

0:08–0:15

Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding.

## 11. Check the project before you run an exercise

0:15

This screenshot shows the Connect step before access is checked. Enter your own project, choose an inference allowance, then click Connect and restore my work. This image does not show a completed connection.

## 12. Add an attribute to the tool span

0:15

Point to the attribute inside the tool scope. The free code check tests the function locally. The separate trace button publishes the environment check. This same function will record later training calls.

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

## 31. Choose settings, choose a model, or write new code

1:05

Changing learning rate is a hyperparameter search. Choosing MLP or CNN compares existing architectures. Later, the research agent will write different model or training code. These are different kinds of changes, and we’ll record which one we made.

## 32. Compare six model configurations

1:07

These six configurations are the workshop defaults: two model families, three settings per family, seed 17, batch size 32, and sixty training steps. It’s a short CPU exercise, so inspect whether the models have trained enough before drawing an architecture conclusion.

## 33. Run the configurations through W&B Sweeps

1:09

W&B Sweeps assigns each configuration to a run. Our training function does the fitting and saves its outputs. This is a shortened excerpt; the notebook contains the entity, project, and complete configuration setup.

## 34. Compare forecast error and training time

1:10

This is the recorded six-run Sweep. Find validation error, performance relative to persistence, and training time. All six models performed worse than persistence here. The lowest error among them does not make it a successful forecast.

## 35. Check whether the models learned enough

1:11

In the recorded runs, the loss curves and forecasts showed the models were still undertrained after sixty steps. Compare that with the forecasts you just produced. A longer, equal training budget for all models would be a separate experiment.

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

## 40. Look at the forecast beside the observed future

1:44

Read this recorded example from input to prediction, observed future, and error map. Ask someone to point to a region that changed. After training, the notebook will show the same view for their own result.

## 41. Have the network predict the whole image

1:46

The first model takes two image channels and predicts a whole future image. Its output has one channel. We keep the network small enough to compare on CPU during the workshop.

## 42. Add a learned correction to the current image

1:48

The residual model adds its learned correction to the current image. If the correction is zero, its forecast is exactly persistence. Participants implement this branch in the same forward method.

## 43. Measure error inside the solar disk

1:50

Compute absolute error only inside the fixed solar-disk mask. Sum and divide within each image, then average the image errors. An edit outside the mask should not change this score.

## 44. Train with one loss; compare with a fixed metric

1:52

The training loss supplies gradients that update weights. The evaluation metric tells us how the forecast compares with another model. We can try a different training loss while keeping the scoring rule fixed. That will be one of the agent’s recorded proposals.

## 45. Compare the two forecasts on the same case

1:54

These two recorded rows use the same input and target times. The convolutional forecast is above; the residual forecast is below. Compare the images and error maps, then look at the validation scores. The final dates have not been used to select either model.

## 46. Implement and compare the image predictors

1:55–2:15

Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed.

## 47. Give the research agent your code and results

2:15

Read this transition as one explanation. Until now, we wrote the models and chose the settings ourselves. We’ll now ask an agent for two code changes, inspect them, and use the experiment we built to test them. The selected code becomes the next round’s starting point.

## 48. The research agent writes code; the forecast model trains

2:17

There are two different models here. GLM writes research proposals and its weights stay fixed. The small forecasting networks train their weights for each candidate. The research agent changes the program that performs that training.

## 49. Decide which files the agent may change

2:19

The agent can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox.

## 50. Send the code, settings, and validation results

2:21

Send the files and settings that produced the current result, plus its validation outputs. A default learning rate in source may differ from the value used in the run. The agent needs the active values to propose a relevant change.

## 51. Follow the agent’s work in Agent Lens

2:23

Open the research conversation in Agent Lens. Start with the mission, then find the evidence-reading tool and the returned code. Follow a training call to its result or error. Compare that sequence with the agent’s explanation of its change.

## 52. Find the validation evidence the agent read

2:24

Open the evidence-reading tool and find the current source settings and validation result. Then inspect the returned proposal and follow its training result. This capture comes from the recorded rehearsal, not a new request. The full-size image remains available when sign-in is required.

## 53. Choose the evidence for the research agent

2:25–2:40

Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request.

## 54. Ask for two changes to the same starting code

2:40

Both candidates start from the same code and settings. This borrows Propose–Probe–Compose from Harness². Here the probes train forecasting models and give validation scores to the editor, so it is a teaching adaptation rather than the paper’s exact task protocol.

## 55. Read the proposed change before running it

2:41

This recorded candidate changes squared training loss to absolute loss. Ask what that might change during training, then inspect the test result. Reading the diff tells us what was proposed; it does not tell us whether the forecast improved.

## 56. Train and score each candidate

2:42

Train each candidate on the same training dates and compare its validation error. If one fails before producing a forecast, inspect the error and leave its score missing.

## 57. Ask the agent which changes to keep

2:44

The agent reads both test results and can keep one candidate, combine changes, or retain the starting code. The dashed lines mean that it reviewed the results. They do not mean both sets of changes were merged.

## 58. Test the version the agent chose

2:46

Run the chosen code before accepting it. Combining two changes can behave differently from either one alone. If the unchanged version is retained, testing it creates another execution of the same code.

## 59. Start round two from the selected version

2:48

The selected code and a short lesson enter round two. The agent now proposes changes on top of that version. We are still forecasting the same image task and selecting with the same validation metric.

## 60. Propose and test two changes

2:50–3:00

Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice.

## 61. Test the selected code, then begin round two

3:00–3:15

Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work.

## 62. Follow one proposal through the branch diagram

3:15

Click a candidate, its test, and the selection step. Ask someone to explain what happened along that path. This diagram explains the process; the notebook’s branch view opens their actual files and results.

## 63. Stop editing before the final comparison

3:17

Select the versions before looking at the final dates. The image comparison includes persistence, the manually selected model, and the agent-selected model. Keep the saved code and weights fixed while evaluating them.

## 64. Load the saved weights to make final predictions

3:19

Load the saved weights, switch to evaluation mode, and predict without an optimizer step. Final evaluation measures the selected trained model; it does not train another one.

## 65. Compare predictions for the same times

3:21

Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Native EvalTables was unavailable during the rehearsal, so the notebook and Weave comparison remain available; publication can be retried separately.

## 66. Test the selected models on reserved dates

3:25–3:45

Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies.

## 67. In this rehearsal, image error fell 10.15%

3:45 · RECORDED REHEARSAL

The selected agent code combined the zero-initialized residual head from round one with absolute training loss from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods.

## 68. Compare the saved forecasts at the same time

3:46 · RECORDED REHEARSAL

These are saved forecasts for the same final timestamp. Compare the manual row with the agent-selected row, including the error images. The full screenshot also contains the score tables. It is the notebook comparison from the rehearsal.

## 69. The recorded GOES model lost to persistence

3:47 · RECORDED REHEARSAL

The GOES model’s final log-flux MAE was 2.469; persistence scored 0.193. Its learning curve showed it was still undertrained after sixty steps. Keep this failure beside the image result. It does not establish that MLPs or CNNs cannot forecast solar measurements.

## 70. Open the comparison in your project

3:48

This saved workspace contains only the runs from one rehearsal. Compare final image scores, then inspect GOES separately. Open a run to see its settings, runtime, and evidence. Do not combine these two tasks into one average. The selected runs and source metrics are unchanged.

## 71. Open the files behind one result

3:49

Open the Artifact file list for round two’s tested composition. candidate.py is the executed code, losses.json records training, weights.pt holds trained parameters, and predictions.npy and predictions.png contain the output. execution.json links the settings and result. This is the saved training run whose weights were subsequently frozen, not a new execution.

## 72. Write down what changed and whether it helped

3:50–3:58

Allow eight minutes. Ask participants to name a change, report what happened, and include a remaining miss. A negative result is fine. If publication fails, save the conclusion and retry the upload without rerunning the experiment.

## 73. Explain the result, then choose the next experiment

3:58–4:00

A teammate should be able to follow this explanation back to the run, source, and prediction. Ask for one next experiment based on an error someone inspected: what would change, what would stay fixed, and what would make them keep the previous version? This Report describes the recorded rehearsal; participants publish their own conclusions.

## 74. Reference and worked answers

REFERENCE

These pages are optional answers and recorded examples. Open an answer after participants have tried the exercise. Use the return link to get back to the teaching sequence.

## 75. Put the attribute inside the tool scope

WORKED ANSWER

The attribute is attached inside the Tool scope. The complete notebook function also supplies its call identity and outer conversation. Use the operation’s timestamps so Agent Lens shows when the work happened, not when it was uploaded.

## 76. Return a copy of the latest observation

WORKED ANSWER

The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.

## 77. Take the mean of the absolute errors

WORKED ANSWER

Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.

## 78. Compare the settings and loss curves

WORKED ANSWER

Open the configuration and curve for two runs. Find the settings they share and the value that differs. If training failed, inspect the error rather than assigning a score to a forecast that does not exist.

## 79. Average the error inside the disk mask

WORKED ANSWER

The mask selects the solar disk. Compute the sum and count per image, then average across images. Check identical arrays, a constant one-unit difference, and a difference only outside the mask.

## 80. Add the correction to input channel 1

WORKED ANSWER

Channel zero is the earlier image and channel one is the current image. Add the correction to channel one. With a zero correction, this function returns the current image exactly.

## 81. Return validation evidence only

WORKED ANSWER

First check that the record belongs to validation. Then return only the listed evidence fields. The current source is supplied separately. The final-test example should raise an error before the agent sees it.

## 82. Pass the candidate’s code to training

WORKED ANSWER

Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.

## 83. Use the saved model without training it again

WORKED ANSWER

The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.

## 84. Round 1: two changes, two measured outcomes

RECORDED REHEARSAL

In our November 13 rehearsal, Candidate A changed the loss to absolute error. Candidate B initialized the residual head at zero and had lower validation error. The composition kept B and its separate test reproduced the same score. These models shared the image data, seed, and forty-step training configuration.

## 85. Initialize the correction at zero

RECORDED REHEARSAL

Zero weights and bias in the last convolution make the initial correction zero. The residual model therefore starts by copying the present image, then learns a correction during training. This is the actual first-round edit that was selected in the recorded run.

## 86. Round 2 also tested the unchanged version

RECORDED REHEARSAL

Round two started from the zero-initialized model. Candidate A added absolute training loss. Candidate B kept the source unchanged and reproduced its error. The tested composition selected A. This small validation difference comes from one seed, so it does not establish repeatability.

## 87. Open the recorded research conversation

RECORDED REHEARSAL

Open the proposal conversation and follow the evidence-reading tool to the candidate source. The downloadable records contain the same decisions and scores if the native view requires sign-in.

## 88. When a service is unavailable

REFERENCE

Start with the failed operation. An authentication problem needs corrected access. A failed training run needs its saved error inspected. An upload failure needs a publication retry. Native EvalTables returned HTTP 500 during this rehearsal; the notebook and Weave comparisons are still available.

## 89. Four-hour session

REFERENCE

Use these times to pace the room. They include coding and discussion, not just execution. If a section takes longer, use its recorded example for discussion rather than claiming a learner’s unexecuted code produced that result.

## 90. Keep working in your own project

REFERENCE

Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.

## 91. The same kit also runs an office-agent workshop

OPTIONAL · PENDING, INC.

This optional sequence shows the current Pending workshop, not the older gateway-based release. Copy it into your own project. The notebook screenshot shows the current setup controls; it does not prove hosted access or completed training.

## 92. Check what the invoice tool returned

OPTIONAL · PENDING, INC.

Follow the lookup arguments and returned observation. This is the function the participant wrote, used by the real agent loop. Find where the next action used its result. It is a separate office rehearsal, not evidence from the solar experiment.

## 93. Compare the office state and explanation separately

OPTIONAL · PENDING, INC.

There was no observed task-quality gain on these four tickets: all twelve state checks passed. Eleven explanation judgments were available; the missing one is not a failed state check. Manual and agent-selected harnesses were the same executable version. Use the saved case table to inspect a recovery.

## 94. Write what the office comparison showed

OPTIONAL · PENDING, INC.

Open the Report for the separate office workshop. Follow a ticket to its checked state and trace, and explain why the selected instructions were retained. Use the return link to resume the Solar setup sequence.