# Solar forecasting workshop presenter notes

## 1. Solar forecasting<br>with agent-assisted<br>experiments

0:00–0:25

You are joining a fictional research lab preparing for its weekly forecast review. We will use real February 2014 satellite observations to predict X-ray flux thirty minutes ahead and solar images one hour ahead. First we will compare small trained models with copying the latest observation. Then we will ask an agent to edit the image experiment’s code and test those changes with the same comparison. This is a CPU teaching experiment, not an operational solar forecast. Session block: Connect and trace an operation (minutes 0–25).
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.

## 2. What you will build and inspect

0:00–0:25

Introduce the real task, the data available, and the outcome participants will check. Point to each Forge product at the operation it helps investigate.
Visual guide: solar/overview. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 3. The lab needs a forecast for its weekly review

0:00–0:25

The principal investigator, or PI, runs the weekly research meeting. You are the researcher preparing a comparison for that meeting. The question is deliberately concrete: does a trained model predict the next observation better than simply copying the current one? We have two weeks of archived data, so we can hide later observations, make predictions, and then compare them with what was actually recorded. We are practicing an experiment design; these short runs cannot establish reliable solar forecasting. Session block: Connect and trace an operation (minutes 0–25).

## 4. What the satellites recorded

0:00–0:25

GOES gives us two numerical measurements each minute: XRS-A and XRS-B measure X-ray power per square metre in different wavelength bands. The plot shows XRS-B, transformed with log10 because its values span a wide range. AIA is a different instrument on NASA’s Solar Dynamics Observatory. Its 171-angstrom images show extreme-ultraviolet emission from the Sun’s outer atmosphere. The colors represent intensity, not visible light or a direct temperature measurement. Our teaching arrays reduce the images to sixty-four by sixty-four pixels. SunPy retrieves and reads the observations and metadata; our preprocessing code builds the training arrays. These are separate forecasting tasks, not two inputs to one model. Sources: https://www.spaceweather.gov/products/goes-x-ray-flux and https://sdo.gsfc.nasa.gov/data/channels.php. Session block: Connect and trace an operation (minutes 0–25).

## 5. What one forecast example contains

0:00–0:25

Both examples shown here exist in the prepared training data. Set the clock to 01:00 UTC on February 1. For GOES, the model can read sixty one-minute samples in each channel, from 00:01 through 01:00, and must predict XRS-B at 01:30. Persistence uses only the current XRS-B reading as that forecast. For AIA, the model sees images from 00:00 and 01:00 and predicts the image at 02:00; persistence copies the 01:00 image. The future observations are targets for scoring, never inputs to the prediction. We compare absolute error in log-flux units for GOES and mean absolute error in normalized image intensity inside the solar disk for AIA. The scores stay separate. If little changes over the horizon, copying the latest observation can be hard to beat. We will measure that rather than assume the trained model wins. Session block: Connect and trace an operation (minutes 0–25).

## 6. Bring a comparison your colleagues can repeat

0:00–0:25

At the review, a lower error is useful only if we know what produced it and what it was compared with. The four final files are our fictional lab’s previous filing system. We will use Forge and W&B to connect the code, configuration, data, weights, and predictions to each run. The measurement task teaches that stack with a scalar output; the image task reuses it for predictions we can inspect pixel by pixel. Only then do we add an AI research assistant. It will read the image code and validation results and propose edits to the model or training procedure. It will not alter the data, target, or final scoring rules. Session block: Connect and trace an operation (minutes 0–25).
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.

## 7. Copy the notebook into your Forge project

0:00–0:25

Allow participants to get their own copy open before continuing. Run all stale cells creates the controls; it does not press the exercise run buttons. Hosted Forge supplies authentication, but attendees still need their own project and account access. Use fictional or public teaching data in a public project. Session block: Connect and trace an operation (minutes 0–25).

## 8. Copy the notebook into the project you will use

0:00–0:25

Show the native copy dialog. The copied notebook uses its destination project. A laptop uses manual entry. Confirm the project before executing. The browser preview limitation remains separate from notebook execution. Session block: Connect and trace an operation (minutes 0–25).

## 9. Run the same notebook on your laptop

0:00–0:25

Hosted participants can skip this slide. On a laptop, install Git and uv, clone the repository, and run these commands. Authenticate in the terminal and keep that terminal open while marimo runs. There is no extra workshop service to start. Session block: Connect and trace an operation (minutes 0–25).

## 10. Check the compute and inference settings

0:00–0:25

Check these settings before running anything. The eight-dollar allowance applies to inference, while hosted notebook compute is separate. The research agent uses GLM-5.3-Flash with temperature 0.2, JSON output, and up to 16,384 output tokens. If that model is unavailable, stop and inspect the error rather than changing models mid-comparison. Session block: Connect and trace an operation (minutes 0–25).

## 11. Wrap one operation, then inspect what you recorded

0:00–0:25

Conversation identifies the execution. Turn holds the mission. Tool records one operation. The attribute line is the learner edit, not a second call. Actual instrumentation also supplies start and end timestamps and records exceptions. Run the free check, send the setup trace, then find the same field in Agent Lens. Advance the code highlights one step at a time; use Back to revisit the previous statement. Session block: Connect and trace an operation (minutes 0–25).

## 12. Connect and inspect your first tool call

0:00–0:25

Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding. Session block: Connect and trace an operation (minutes 0–25).

## 13. Find the field your code added to the span

0:00–0:25

The exercise is complete when the participant can find their own attribute in their own tool span. Here is the recorded reference. The tool arguments, result, and duration describe one actual operation. The same instrumentation function records later training calls. Session block: Connect and trace an operation (minutes 0–25).

## 14. Construct one forecast window

0:25–1:05

Set the clock to 01:00 UTC on February 1. Reveal the 01:30 target, then persistence. All numerical values are from the immutable teaching dataset, extracted without training. Ask which number a forecasting program is allowed to use at 01:00. The answer is the observation, not the later target. Session block: Read observations and implement persistence (minutes 25–65).
Visual guide: solar/window. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 15. Read the arrays for that same forecast

0:25–1:05

A NumPy array stores numbers with named positions, not timestamp metadata in every entry. The shared index identifies the same forecast across x, y, ids and persistence. Channel zero is XRSA; channel one is XRSB. The final axis runs from the oldest to the latest minute. The persistence array preserves log-flux units before input standardization. This is a read-only excerpt; use the notebook window selector to inspect it. Session block: Read observations and implement persistence (minutes 25–65).

## 16. Use different dates to fit, choose, and evaluate

0:25–1:05

These dates serve three different research decisions. February 1–10 trains the model weights and supplies the normalization statistics. February 11–12 lets us compare architectures, settings, and later the agent’s code changes. We will look at those validation errors repeatedly, so they cannot also be our final test. February 13–14 stays reserved until we freeze the selected code and weights. Then we evaluate without training again. A window whose history or target crosses a boundary is excluded. The reserved dates give us an honest comparison for this short period, not evidence of reliable forecasting in other months. Session block: Read observations and implement persistence (minutes 25–65).

## 17. Keep the whole example inside one date split

0:25–1:05

Reveal one invalid cross-boundary window and then one gap. load_goes checks every one-minute interval from the first history sample through the target, including the forecast horizon. It rejects windows crossing a date partition. Randomly shuffling overlapping windows across train and test would let nearly identical histories occur on both sides. The workshop uses chronological partitions, but adjacent accepted windows still overlap within a partition. Session block: Read observations and implement persistence (minutes 25–65).

## 18. Normalize the inputs without changing the target units

0:25–1:05

load_goes first takes log10 of both flux channels. It fits one mean and standard deviation per channel using training inputs only, then reuses those values for validation and final inputs. The target remains unstandardized log10 XRS-B. That is why persistence returns split["persistence"] rather than copying a standardized tensor entry. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Read observations and implement persistence (minutes 25–65).

## 19. Calculate the value the model receives

0:25–1:05

These numbers come from the same 01:00 window. Subtract the XRS-B training mean and divide by the training standard deviation to obtain minus 0.233211. The different number is a change of units, not a different observation. Both channels get their own training-derived statistics. Learners should reproduce the value using the notebook table and its normalization checkbox. The baseline must return minus 5.534128, not minus 0.233211. Rounded displayed values may differ in their last digit from full-precision calculations. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Read observations and implement persistence (minutes 25–65).

## 20. Inspect a solar observation with SunPy

0:25–1:05

Open the representative FITS file and inspect its date, wavelength, and unit. Training uses prepared arrays so the class does not wait for archive downloads. The dataset includes the acquisition and preprocessing records, so we can trace those arrays back to the public observations. Session block: Read observations and implement persistence (minutes 25–65).

## 21. Inspect the observations before training

0:25–1:05

Give participants six minutes. Have them explain one forecast window to a neighbor: which observations go in, which observation is the target, and which dates it belongs to. No training is needed yet. Session block: Read observations and implement persistence (minutes 25–65).

## 22. Start by copying the latest reading

0:25–1:05

Persistence means predicting that the latest value will stay the same. Solar observations are correlated over time, so this simple baseline can be hard to beat. At the lab review, someone will ask why we needed a neural network if copying the last reading worked. We should run that comparison before they ask. Session block: Read observations and implement persistence (minutes 25–65).

## 23. Measure how far the prediction missed

0:25–1:05

For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score. Session block: Read observations and implement persistence (minutes 25–65).

## 24. Score the forecast we just made

0:25–1:05

This particular forecast misses a rise in flux. Persistence can work well on slowly changing periods and miss rapid changes. Do not infer the mean from this one example. The existing arithmetic slide shows how individual errors are averaged. A log10 error of about 0.59 corresponds to a ratio near four, not a 59 percent error. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Read observations and implement persistence (minutes 25–65).

## 25. Write and test persistence

0:25–1:05

Allow ten minutes. Let participants attempt the function before opening the answer. Ask them to find an interval where the real flux changed while persistence kept the previous value. That is a concrete error another model could try to reduce. Session block: Read observations and implement persistence (minutes 25–65).

## 26. Save what changed between runs

1:05–1:35

A colleague at the review asks which setting changed. These are possible explanations, not claims about this rehearsal. If code, data, or training time differs, we need to know that before deciding why the score moved. Saving the active values answers the question without searching all four final notebooks. Session block: Explain training and saved experiment files (minutes 65–95).

## 27. Which setting changed between these runs?

1:05–1:35

These are two recorded GOES runs. Before revealing the settings, ask what the scores let us conclude. Then click Show active settings. Both runs used the same source and training budget; their learning rates differed. Session block: Explain training and saved experiment files (minutes 65–95).

## 28. These runs used different learning rates

1:05–1:35

The learning rate changed from .001 to .003. Data, source, seed, steps, and batch size stayed the same. Both errors were worse than persistence. We can explain the setting change at the review, but we still cannot claim to have beaten the baseline. Check the predictions before deciding what to try next. Session block: Explain training and saved experiment files (minutes 65–95).

## 29. Use the same scoring rule for every model

1:05–1:35

Keep the target, dates, and primary metric unchanged while comparing models. If we changed the metric after seeing a result, the lower number could describe a different task. Our candidate code can change the predictor and training procedure while this comparison rule stays fixed. Session block: Explain training and saved experiment files (minutes 65–95).

## 30. Keep the experiment and its outputs together

1:05–1:35

Find the full editable run_training function in the notebook. The stage identifies a request to train specific source with specific settings and data. Its completed result is reused only for that matching request. training.train runs the program and returns predictions. stage.record stores its result and output files. Publication follows execution; an upload failure does not erase training or require training again. The ellipsis abbreviates arguments in this teaching excerpt; it is not a paste-ready function. Session block: Explain training and saved experiment files (minutes 65–95).
Visual guide: solar/run-record. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 31. Turn a prediction error into a weight update

1:05–1:35

In fit, the GOES model predicts a batch and computes squared error against training targets. The shared loss function has an all-ones mask for GOES; the image exercise later uses the mask to select disk pixels. loss.backward computes gradients. Adam updates the forecasting model weights. The training targets participate in these updates. Validation inputs are predicted without gradients, and validation targets are scored by the parent process outside candidate code. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Explain training and saved experiment files (minutes 65–95).
Visual guide: solar/learning. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 32. Use the error to decide which way a weight should move

1:05–1:35

Use a one-weight model to explain the derivative before showing PyTorch. With x equal two and target three, loss is (2w minus three) squared. At w equal one, its derivative is minus four. A simple gradient-descent step subtracts learning rate times gradient. The displayed update uses 0.1 and gives w equal 1.4. This is arithmetic, not a logged workshop result. Our real model uses Adam, which also maintains estimates of gradient moments. Do not describe this example as an exact Adam update. Session block: Explain training and saved experiment files (minutes 65–95).

## 33. Separate prediction, gradients and the optimizer step

1:05–1:35

zero_grad clears accumulated gradients; PyTorch adds new gradients unless we clear them. The forward pass creates predictions and records the operations needed for differentiation. backward computes derivatives of the loss with respect to trainable parameters. step applies the optimizer update. The workshop loops over a fixed number of optimizer steps, not a promised number of full dataset epochs. Training sample order and initialization depend on the seed. Learners edit training_loss; they can inspect the surrounding fit function. Session block: Explain training and saved experiment files (minutes 65–95).

## 34. Validation measures the current weights without fitting them

1:05–1:35

eval disables training-specific behavior such as dropout if a candidate uses it. no_grad prevents autograd from retaining a differentiation graph. Our current small models do not need dropout to illustrate the distinction. The fixed parent scorer compares predictions to validation targets. Participants choose a configuration using validation; the optimizer itself never updates from these validation targets in this workshop. This is an explanatory excerpt of the scoring boundary, not the exact function signature. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Explain training and saved experiment files (minutes 65–95).

## 35. Restore a completed run after a restart

1:05–1:35

The local completion record tells the notebook which work finished. The checkpoint Artifact stores a copy in your project. If the runtime is replaced, restore the checkpoint before continuing. An upload failure can be retried using the local files. Session block: Explain training and saved experiment files (minutes 65–95).

## 36. Take a fifteen-minute break

1:35–1:50

Use minutes 95 through 110. Do not start a new training run during the break. A pending publication can be retried from saved results later. Session block: Break (minutes 95–110).

## 37. Changing settings, choosing models, and editing code

1:50–2:35

There are three different operations here. Hyperparameter search supplies different values to the same implementation, such as learning rate or width. Architecture comparison chooses between implementations we already wrote, such as an MLP and a temporal CNN. Later, the research agent will write a code change that our current configuration options cannot express, such as replacing squared training loss with absolute loss. We’ll test that changed program with the same dates and scoring rule. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 38. Follow the tensor through the model

1:50–2:35

B counts windows processed together. Each window has two instrument channels and sixty time positions. The target has one value per window. The training configuration uses batch size thirty-two. The notebook free shape demonstration uses batch size two and width four so learners can inspect a small forward pass; it does not train and does not change later random state. Ask learners to explain x[0,1,-1] before revealing the output shape. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Visual guide: solar/model-shapes. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 39. Keep each prediction paired with its own target

1:50–2:35

Explain colon as selecting every item and negative one as the final position. Using -1 removes the last axis; -1: preserves it as length one. Shape-compatible subtraction matters: (B,1) minus (B,) can broadcast to a B by B matrix and silently score the wrong pairs. Both predictions and targets should remain B by one. Ask experienced participants to demonstrate that broadcasting issue with a small local NumPy array; no training is needed. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 40. How the MLP uses an hour of measurements

1:50–2:35

The actual candidate code flattens a two-by-sixty input into one hundred twenty values. A linear layer learns weights for every input position, followed by ReLU and a linear scalar output. Width is sixteen or thirty-two in the search. The diagram omits the batch dimension and draws a few hidden units to represent the layer. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 41. Calculate one hidden unit before adding the whole layer

1:50–2:35

The arithmetic uses three values for legibility. The real MLP flattens 120 values. A Linear layer gives every hidden unit one learned weight per input plus a bias. ReLU retains positive values and sets negative values to zero. A second Linear layer combines hidden outputs into one forecast. With no nonlinear activation between linear layers, their composition would still be one affine transformation. The example illustrates the operation; it is not a neuron from a trained checkpoint. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 42. How the temporal CNN uses the same measurements

1:50–2:35

The same two-by-sixty input now passes through a five-sample convolution with padding two. Filter weights are reused along time. The output has width channels and sixty positions; AdaptiveAvgPool1d(1) averages over time, then the linear layer predicts one value. This compares two implemented computations, not just two model names. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 43. Reuse one filter at each time position

1:50–2:35

One Conv1d output channel uses a five-position filter for each of the two input channels, sums ten products and adds its bias. Slide the highlighted window once while retaining the same weights. Multiple output channels learn different filters. Padding two preserves the time dimension at sixty. Average pooling then discards the time-position axis. That is a modeling assumption, not merely a shape trick: the network summarizes local features across the hour. The MLP gives distinct weights to each time position. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 44. Choose settings separately from the weights being learned

1:50–2:35

The six Sweep configurations are predefined; the required exercise is a bounded comparison, not an adaptive search algorithm. Architecture chooses an existing implementation. Width changes its number of hidden features. Learning rate scales updates. Steps fixes the update budget. Seed controls initialization and sampling. None of these is itself a learned model weight. All comparisons must record the settings because a favorable score does not tell us which choices produced it. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 45. Write the loss and metric

1:50–2:35

Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 46. Compare six model configurations

1:50–2:35

The MLP reads the history as a fixed set of inputs. The temporal CNN applies shared filters along time. We’ll try three settings for each: widths sixteen and thirty-two, and learning rates .001 and .003. Every run gets seed seventeen, batch size thirty-two, and sixty training steps. That small budget keeps the exercise short; it does not establish which architecture would win after longer training. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 47. Run the configurations through W&B Sweeps

1:50–2:35

The Sweep assigns a trial configuration, and wandb.init creates its tracked run. run_training fits the model, saves its files, and returns metrics; run.log adds those metrics to the run. The first wandb.agent call schedules one trial. Inspect its saved files and forecast, then the second call schedules the other five. Counts come from assigned Sweep jobs; a cached training result still needs its matching tracked job. The notebook includes the full entity, project, and configuration setup shown in this shortened excerpt. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 48. Compare the six configurations in Forge

1:50–2:35

Use the latest rehearsal Sweep pzigourv. Start with two width-16 MLP runs, then compare their learning rates, error, and runtime. All six models lost to persistence. Do not infer an architecture conclusion from this short training exercise. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 49. Check whether the model has finished learning

1:50–2:35

The selected GOES model’s loss was still falling after sixty steps. That suggests testing a longer training budget, but it does not tell us that more steps would beat persistence. Look at the predictions and validation score alongside the curve. Before opening the worked repair, propose a check of output units or training progress. The later qualification tested a complete repaired recipe. It does not isolate the effect of additional training alone. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 50. Inspect one trial before running the rest

1:50–2:35

Allow fifteen minutes. Pause after the first trial and ask participants to identify its configuration, data and code before scheduling the remaining five. After it finishes, have them explain one result from the loss curve and forecast. Keep failed runs visible so the comparison accounts for what happened. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 51. Diagnose the forecast before opening the repair

1:50–2:35

Discuss the diagnosis before revealing the recipe. The optional note is for the learner and never enters an agent prompt. Use the last five minutes of the measurement exercise. This is one CPU run, not another paid agent request. Its exact source, configuration, and weights are saved separately. The recipe beat persistence on three predeclared seeds in qualification, but a learner edit is a new experiment. Final selection considers its validation score; do not choose using final dates. Session block: Inspect model shapes and compare configurations (minutes 110–155).

## 52. Investigate this result

2:27 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 53. Read one claim in the recorded response

2:27 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 54. Open the source and check that claim

2:27 · 8 minutes across these three frames

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 55. Predict the solar image one hour ahead

2:35–3:20

Now we give the model images from sixty minutes ago and now, and ask for the image sixty minutes ahead. The AIA 171 Å arrays are 64 by 64 pixels so the exercise can run on CPU. Session block: Implement image prediction and scoring (minutes 155–200).

## 56. See exactly which images become input and target

2:35–3:20

Read the observation times. Channel zero is the earlier image; channel one is the current image. The third image is the future target. These are three real observations from a training window, not three outputs of an AI image generator. Session block: Implement image prediction and scoring (minutes 155–200).

## 57. Put image inputs and targets in the same units

2:35–3:20

This difference deserves explicit attention. The prepared AIA images are exposure-normalized rates. log1p reduces the dynamic range while accepting zero. The loader computes center and scale over on-disk training pixels, then uses the same transform for all frames and targets. Negative normalized values are possible; they do not mean negative observed light. Display colors encode intensity and are not the three input channels of an RGB model. The model receives two grayscale frames as channels. Session block: Implement image prediction and scoring (minutes 155–200).

## 58. Keep the two image times in separate channels

2:35–3:20

Use the same earlier and current observations already displayed. The input is B by two by sixty-four by sixty-four. The output is B by one by sixty-four by sixty-four. x[:,1:2] selects the current image while retaining the channel dimension. x[:,1] would drop it and can broadcast incorrectly. The image diagram is a shape illustration; the preceding slide supplies actual solar observations. Session block: Implement image prediction and scoring (minutes 155–200).

## 59. Predicting the future image with a small CNN

2:35–3:20

The two observations become two input channels. The CNN returns one channel containing its predicted future image. The batch dimension stays the same: input shape is batch by two by sixty-four by sixty-four, and output shape is batch by one by sixty-four by sixty-four. This direct predictor has to produce the whole image from its learned weights. Session block: Implement image prediction and scoring (minutes 155–200).

## 60. Predict a correction to the current image

2:35–3:20

Much of the current image may remain similar one hour later. We can copy that image and ask the network to predict the correction. Add the network output to x[:, 1:2], the current-image channel. The slice preserves the channel dimension. If the correction is zero, the model returns persistence exactly. The local check will test that behavior. Session block: Implement image prediction and scoring (minutes 155–200).
Visual guide: solar/images. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 61. Implement the residual predictor’s forward pass

2:35–3:20

The diagram and code describe the same addition. Ask participants why x[:, 1] would remove a dimension and why x[:, 1:2] preserves it. The notebook implementation also branches on architecture so the convolutional comparison still returns only the network output. Advance the code highlights one step at a time; use Back to revisit the previous statement. Session block: Implement image prediction and scoring (minutes 155–200).

## 62. Inspect the correction produced by the saved model

2:35–3:20

The center image is calculated from the saved manual residual forecast minus the current input. It shows what this trained network added. It is not the physical change observed on the Sun. Zero is white in the correction view, with negative and positive values on opposite sides of the colorbar. The panels show the equation implemented by forward. Session block: Implement image prediction and scoring (minutes 155–200).

## 63. Measure prediction error inside the solar disk

2:35–3:20

This is a diagram of the scoring calculation, not a forecast. The fixed mask assigns one to disk pixels and zero outside. Multiply absolute errors by the mask, average over the selected pixels per image, then average images. A changed off-disk pixel must not affect the score. Session block: Implement image prediction and scoring (minutes 155–200).

## 64. Check the image scorer on three known errors

2:35–3:20

Run the three local examples before training. They explain what the scorer measures. The participant writes this development scorer, and the protected primary scorer checks the comparison with the same published rule. Missing or invalid predictions are not zero error. Advance the code highlights one step at a time; use Back to revisit the previous statement. In the notebook, move the error outside the scoring mask, then click Try my image scorer on these pixels. The two public grids have different mask sizes; images still receive equal weight. Session block: Implement image prediction and scoring (minutes 155–200).

## 65. Give each forecast image one score

2:35–3:20

This is the exact arithmetic of the public scorer fixture with error set to one and inside selected. The first image includes one pixel with error one. The second includes four pixels with error two, so its sum is eight but its per-image MAE is two. Average one and two to obtain 1.5. Pooling all pixels gives 1.8 and changes the weighting. In the notebook, move the error outside the mask and run Try my image scorer on these pixels; the score becomes zero. Missing predictions do not become a zero score. Session block: Implement image prediction and scoring (minutes 155–200).

## 66. Training loss and evaluation error have different jobs

2:35–3:20

The training loss supplies gradients for the optimizer. The evaluation metric scores the finished predictions. Our starting loss uses squared error, while the comparison uses absolute error inside the disk. A candidate can change the loss to alter how weights are learned. We keep the evaluation metric fixed so we can compare the resulting forecasts. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Implement image prediction and scoring (minutes 155–200).

## 67. Compare forecasts for the same validation case

2:35–3:20

The same current image and observed future appear in both rows. The convolutional forecast is above, residual below. The figure uses the first accepted case, not a selected success. Colors use the same scale across both rows. A single image is an example; the validation score includes all 142 windows. Session block: Implement image prediction and scoring (minutes 155–200).

## 68. Implement and compare the image predictors

2:35–3:20

Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed. Session block: Implement image prediction and scoring (minutes 155–200).

## 69. Pause for thirty minutes before the research-agent exercise

3:20–3:50

Use minutes 200 through 230 for the meal break. Completed work should already be saved. Do not ask people to leave an unreviewed paid action running during the break. Session block: Meal break (minutes 200–230).

## 70. Use the experiment to test agent-written changes

3:50–4:20

The lab now has code, saved experiments, and a comparison we can inspect. The PI suggests bringing in an AI research assistant to propose the next changes. It reads the current source, active settings, validation errors, and any failures. We still review its diffs and run them through the training and scoring functions we built. The new colleague gets no exemption from testing. Session block: Build the research-agent request (minutes 230–260).
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.

## 71. Which model is being trained?

3:50–4:20

The language model and the forecasting network have different roles. GLM writes Python using its fixed pretrained weights; we are not fine-tuning it. The small forecasting network trains new weights each time we test candidate Python. We send its validation results back to the language model when requesting the next edit. Session block: Build the research-agent request (minutes 230–260).

## 72. Limit edits to the model and training code

3:50–4:20

The research assistant can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution, just as you would for a colleague. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox. Session block: Build the research-agent request (minutes 230–260).

## 73. Give each program only the data it needs

3:50–4:20

Separate three programs. The language model receives selected source and validation evidence and proposes code. Reviewed training code receives training arrays and fits the forecasting network. The parent scorer receives validation predictions and targets. The research agent can inspect validation evidence, but final-test scores and dates stay outside its improvement request. File access is scoped by the workshop; reviewed subprocess execution is not a security sandbox. These arrows describe data flow, not a guarantee that an arbitrary untrusted program is safe. Session block: Build the research-agent request (minutes 230–260).

## 74. Gather validation evidence before requesting a proposal

3:50–4:20

The notebook reads the selected validation execution before asking the model for proposals. read_validation returns the saved configuration, metrics and source fingerprint; event records that operation for Agent Lens. The request is built separately from the current source and the allowed evidence dictionary. It does not send prediction arrays or images, and the model does not choose this evidence-read call. Open the recorded operation to find its config and metrics, then open the model request to inspect source and evidence. A separate reviewed training action tests each proposed program. Session block: Build the research-agent request (minutes 230–260).

## 75. Give the agent the inputs needed to explain a run

3:50–4:20

The request contains the exact source that produced the current result, the settings used in that run, and selected validation metrics and loss history. Errors, trace links and lessons are included when the selected record contains them. Participants can inspect forecast images in the notebook; the proposal request does not send those images or prediction arrays. For example, a default learning rate in candidate.py may be overridden by the active configuration. If we sent only the default, the agent could propose a change based on a setting we never used. Session block: Build the research-agent request (minutes 230–260).

## 76. Follow the agent’s work in Agent Lens

3:50–4:20

Open the research conversation in Agent Lens. The notebook records its evidence read, sends the proposal request, and saves the returned code. These operation spans show the notebook controller’s work; they are not tool choices made by the model. Follow the separately requested training call to its result or error. Compare that sequence with the agent’s explanation of its change. Session block: Build the research-agent request (minutes 230–260).

## 77. Read the evidence that went into the proposal

3:50–4:20

Open read_validation_evidence. Find the residual architecture, forty training steps, seed seventeen, and parent validation error. Then inspect the returned proposal. This request initially exhausted its output budget and used a saved retry; that is an execution event, not a change in forecasting quality. Session block: Build the research-agent request (minutes 230–260).

## 78. Choose the evidence for the research agent

3:50–4:20

Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request. Session block: Build the research-agent request (minutes 230–260).

## 79. Ask for two changes to the same starting code

4:20–5:10

Both candidates start from the same source and training configuration. We ask the agent to explain each proposed change, then review its diff. This uses the Propose–Probe–Compose structure from Harness². In our teaching adaptation, a probe trains forecasting weights and gives validation results to the editor. It differs from the paper’s task protocol. Session block: Review and test two rounds of changes (minutes 260–310).

## 80. The first proposal changes one loss operation

4:20–5:10

This is the actual first-round Candidate A edit in v0.3.0. It changes the training objective, while the evaluation scorer remains fixed. The alternative candidate retains the original squared loss. The diff establishes the proposed change; it does not establish an improvement until both run. Session block: Review and test two rounds of changes (minutes 260–310).

## 81. The loss edit changes which errors receive larger gradients

4:20–5:10

Squared error grows quadratically, and its gradient magnitude grows with the error. Absolute error grows linearly and has constant magnitude away from zero. Matching the objective to the final metric is a plausible hypothesis, not a guarantee of better generalization. The model may trade large localized errors against smaller widespread errors. Inspect the actual validation forecasts after testing. These three arithmetic values are illustrations, not measured solar residuals. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Review and test two rounds of changes (minutes 260–310).

## 82. Train and score each candidate

4:20–5:10

Train each candidate on the same training dates and compare its validation error. If one fails before producing a forecast, inspect the error and leave its score missing. Session block: Review and test two rounds of changes (minutes 260–310).

## 83. Test the research agent’s code changes

4:20–5:10

After both probes, the agent receives their code and validation results. It can keep one candidate, combine changes, or retain the starting source. Two suggestions do not obligate the lab to accept two changes. Read its rationale beside the scores. The dashed lines show which results it reviewed; they do not mean both candidates were merged into the selected code. Session block: Review and test two rounds of changes (minutes 260–310).
Visual guide: solar/research. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.

## 84. Train the composed version before adopting it

4:20–5:10

A combined edit has not yet been measured, so it needs its own training run. Even if the agent retains an existing version, the controller tests the chosen source and records the result. This separates the decision about what to keep from the execution that confirms what ran. Session block: Review and test two rounds of changes (minutes 260–310).

## 85. Test the recommendation before carrying it forward

4:20–5:10

The agent chooses or combines source changes after reviewing probes. That is one decision. The notebook trains that proposed source and applies the strict validation-error rule. That is another decision. Equal, worse or failed results keep the earlier version. A KEEP composition may train unchanged source again; it is an additional execution without an invented code change. The branch panel should expose the actual source and execution attached to each node. Session block: Review and test two rounds of changes (minutes 260–310).

## 86. Adopt the tested code only if validation error is lower

4:20–5:10

The composition is a proposed source version. After it trains, choose_adoption compares its fixed validation_error with the parent. A strictly lower score adopts the tested version. Equal error, a higher error, or failed execution retains the parent. The decision and the execution are separate records. This rule uses no final-test score. Session block: Review and test two rounds of changes (minutes 260–310).

## 87. Open the training call behind the chosen version

4:20–5:10

The operation trained and validated the selected source. Find the returned score and compare the run to the saved source artifact. An error metric of 0.110916 is the forecasting metric, not a tool failure. If a span actually failed, inspect its exception separately. Session block: Review and test two rounds of changes (minutes 260–310).

## 88. Round 2: start the correction at zero

4:20–5:10

This is the second-round selected edit in v0.3.0. The last convolution starts at zero; before training, the residual correction is zero. The model begins at persistence and learns a correction. Its probe and separate composition test produce the measured validation score. Session block: Review and test two rounds of changes (minutes 260–310).

## 89. Zero initialization applies only to the output layer

4:20–5:10

The recorded second-round edit zeros the weights and bias of self.net[-1], the last Conv2d. Earlier convolution layers retain their normal initialization. The last layer initially returns zero, so adding its output to the current image reproduces persistence before training. Adam can then learn a correction. This explains the edit; its measured effect is still limited to the recorded comparison. Session block: Review and test two rounds of changes (minutes 260–310).

## 90. Zeroing the last layer still allows learning

4:20–5:10

At initialization the final layer weights are zero, so its output correction is zero. The output weights still receive gradients because their derivative depends on the preceding features. For the first backward pass the zero output weights block gradients to preceding layers; after the output weights move, gradients can flow farther back. This explains why a zero residual head is compatible with learning. Do not teach zero initialization of every hidden layer as an equivalent change. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Review and test two rounds of changes (minutes 260–310).

## 91. Use the selected code and results in round two

4:20–5:10

Round two begins with the code selected in round one and a saved lesson explaining what the probes showed. The agent reads both before proposing its next edits. It may now change code introduced by its previous proposal. That repeated use of the earlier result is the recursive part of this research procedure. Session block: Review and test two rounds of changes (minutes 260–310).

## 92. Propose and test two changes

4:20–5:10

Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice. Session block: Review and test two rounds of changes (minutes 260–310).

## 93. Test the selected code, then begin round two

4:20–5:10

Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work. Session block: Review and test two rounds of changes (minutes 260–310).

## 94. Follow one proposal through the branch diagram

4:20–5:10

Click a candidate, its test, and the selection step. Follow the source change to its validation result and explain why the agent retained or rejected it. This deck diagram explains the process. The notebook’s branch view links the participant’s own files, decisions, traces, and results. Session block: Review and test two rounds of changes (minutes 260–310).

## 95. Take ten minutes before opening the final dates

5:10–5:20

Use minutes 310 through 320. If a run is still incomplete, keep its status visible. Use the labeled recorded case for discussion rather than assigning its outcome to the learner edit. Session block: Break (minutes 310–320).

## 96. Keep the selected code and weights fixed for final evaluation

5:20–5:45

We have used validation dates to choose the version we will bring to the review. Save that source and its trained weights together before looking at February thirteenth and fourteenth. Final evaluation loads those weights and predicts the reserved inputs without training or selecting again. If we edit after inspecting these results, we need new reserved dates to test the next claim. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Freeze and compare on reserved dates (minutes 320–345).
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.

## 97. Load the saved weights to make final predictions

5:20–5:45

Load the saved weights, switch to evaluation mode, and predict without an optimizer step. Final evaluation measures the selected trained model; it does not train another one. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 98. Match each prediction to the same observation times

5:20–5:45

Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Click Compare in EvalTables to open the native Weave-backed Evaluation Tables Preview. Open Solar images and GOES measurements separately: their errors have different meanings. Upload retries reuse the saved arrays. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 99. Test the selected models on reserved dates

5:20–5:45

Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 100. In this rehearsal, image error fell 10.15%

5:20–5:45

The selected agent code combined the absolute training loss from round one with a zero-initialized residual head from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 101. Compare the two models on one reserved-date image

5:20–5:45

This figure is regenerated from the fresh v0.3.0 saved predictions. Compare manual and agent-selected forecasts on exactly the same case. The fixed error scale helps show differences without changing the colors between rows. The aggregate score includes all 199 accepted final windows. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 102. The image edits helped two seeds and slightly hurt one

5:20–5:45

The earlier ten point one five percent result remains correct for seed seventeen. It is not a result to promise for every run. Seed forty-three already has a strong manual model, and the combined edits are slightly worse. Its loss-only edit does better than both, which is retained in the full table. Initialization and sampled batches both change with the seed, so we do not know which caused this difference. This is fixed-code repetition, not three independent agent discoveries. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 103. The same image edit helped two seeds and hurt one

5:20–5:45

Overlapping windows are not independent solar events. The three-seed qualification tests fixed source, not three agents independently discovering the same edit. Seed seventeen and twenty-nine improve, while seed forty-three slightly regresses. The mean improvement and that regression both belong in the conclusion. A next study could predeclare different dates, more training seeds and independent agent adaptations, but this workshop does not run that study. Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 104. The GOES model performed worse than persistence

5:20–5:45

These are the fresh saved final GOES predictions. The selected sixty-step neural model misses badly, while persistence follows the observed flux much more closely. The later repaired recipe changes scaling, residual initialization, loss, and training budget together. Its separately recorded three-seed test follows; this historical failure remains unchanged. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 105. The measurement repair passed its three-seed check

5:20–5:45

The residual MLP at twelve hundred updates was selected using the mean validation score across seeds seventeen, twenty-nine, and forty-three. Its final mean error is 0.163506, fifteen point one five percent below persistence. All three repetitions improve. These are the same known final dates and overlapping windows; this is a teaching retest, not another independent solar benchmark. There were no new agent calls. The notebook runs this recipe only when the learner clicks Train the worked GOES repair. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 106. Compare forecasts for the same timestamp

5:20–5:45

Open Compare in EvalTables in the final notebook step. The native Weave-backed Evaluation Tables Preview compares saved predictions. Keep GOES measurement results in their separate comparison. This screenshot comes from saved rehearsal data; publishing it does not retrain the models. Match this case_id and file_index to the notebook timestamp selector. The per-image score and full-split mean are shown separately. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 107. Compare errors for one observed future image

5:20–5:45

The per-case image error averages absolute pixel differences inside the fixed solar-disk mask. Summary means cannot replace that score. Use the notebook image selector or saved prediction artifact to inspect the full arrays. Do not imply that the CES v2 backend succeeded; this is the working native Weave-backed Preview. Session block: Freeze and compare on reserved dates (minutes 320–345).

## 108. Check that the saved source contains both selected edits

5:45–6:00

This is execution-f7550caa1639e8366efbf9d84a782289, the exact selected round-two composition. Open the source and weights together. The final evaluation loaded these weights. A different source file with the same model label would not reproduce this experiment. Session block: Reproduce and explain the result (minutes 345–360).

## 109. Check our conclusion

5:48 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 110. Read one claim in the recorded response

5:48 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 111. Open the source and check that claim

5:48 · 7 minutes across these three frames

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/solar_autoresearch/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 112. Write down what changed and whether it helped

5:45–6:00

Allow eight minutes. Ask participants to name a change, report what happened, and include a remaining miss. A negative result is fine. If publication fails, save the conclusion and retry the upload without rerunning the experiment. Session block: Reproduce and explain the result (minutes 345–360).

## 113. Bring the results to the lab review

5:45–6:00

Return to the weekly lab review. Ask participants to open their Report and follow one result to its source and saved prediction. In the recorded rehearsal, the selected image model reduced error, while the GOES model still lost to persistence. Both belong in the review. The image result uses one seed and two test days; it needs testing on other dates. The later qualification found that a repaired GOES recipe beat persistence on all three seeds. The saved image edits helped two seeds and slightly hurt one. Bring both facts to the review; neither replaces the original evidence. Ask each participant to propose a next test grounded in their own forecast. Session block: Reproduce and explain the result (minutes 345–360).
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.

## 114. Reference and worked answers

REFERENCE

These pages are optional answers and recorded examples. Open an answer after participants have tried the exercise. Use the return link to get back to the teaching sequence.

## 115. Put the attribute inside the tool scope

WORKED ANSWER

The attribute is attached inside the Tool scope. The complete notebook function also supplies its call identity and outer conversation. Use the operation’s timestamps so Agent Lens shows when the work happened, not when it was uploaded.

## 116. Return a copy of the latest observation

WORKED ANSWER

The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.

## 117. Implement the training loss and forecast metric

WORKED ANSWER

Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.

## 118. Compare the settings and loss curves

WORKED ANSWER

Open the configuration and curve for two runs. Find the settings they share and the value that differs. If training failed, inspect the error rather than assigning a score to a forecast that does not exist.

## 119. Let the model learn a correction to persistence

WORKED ANSWER

The latest XRS-B input is standardized. Add a learned correction, then convert it back with the same training-fitted center and scale. A zero-initialized final layer begins exactly at persistence. The fit function divides the prediction and target error by the same scale. We changed several parts of the recipe together, so the measured result cannot tell us which individual change caused the gain. Ask participants to point to the addition and unit conversion in their editable code. Advance the code highlights one step at a time; use Back to revisit the previous statement.

## 120. Average the error inside the disk mask

WORKED ANSWER

The mask selects the solar disk. Compute the sum and count per image, then average across images. Check identical arrays, a constant one-unit difference, and a difference only outside the mask.

## 121. Add the correction to input channel 1

WORKED ANSWER

Channel zero is the earlier image and channel one is the current image. Add the correction to channel one. With a zero correction, this function returns the current image exactly.

## 122. Return validation evidence only

WORKED ANSWER

First check that the record belongs to validation. Then return only the listed evidence fields. The current source is supplied separately. The final-test example should raise an error before the agent sees it.

## 123. Pass the candidate’s code to training

WORKED ANSWER

Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.

## 124. Use the saved model without training it again

WORKED ANSWER

The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.

## 125. Round 1: absolute loss versus the unchanged model

RECORDED REHEARSAL

The alternative is a real KEEP decision and it is still tested. Candidate A changes only the loss and lowers validation error in this run. The composition keeps A. This is one seed, not evidence of a repeatable effect.

## 126. Round 2: sampling without replacement did not reduce error

RECORDED REHEARSAL

Candidate B changes the batch sampling to seeded permutations. Its validation error is essentially the same as the parent and slightly higher. The composition keeps zero initialization and rejects the sampling change. Do not attribute a benefit to an untested combination.

## 127. Open the recorded research conversation

RECORDED REHEARSAL

Open the proposal conversation. The notebook’s evidence-read span identifies the saved parent execution. The model request contains source and allowed evidence; its response contains the proposed candidates. Compare those separate records before following a training call. The downloadable records contain the same decisions and scores if the native view requires sign-in.

## 128. When a service is unavailable

REFERENCE

Start with the failed operation. An authentication problem needs corrected access. A failed training run needs its saved error inspected. An upload failure needs a publication retry. The separate CES v2 API remains unavailable. Native Evaluation Tables Preview uses verified Weave evaluation calls and is the workshop comparison path. If any upload fails, retain the notebook results and retry publication only.

## 129. Six-hour session with three breaks

REFERENCE

One six-hour session for a mixed room. The schedule includes fifty-five minutes of breaks. Keep introductory arithmetic beside implementation; experienced participants use the shape, broadcasting and metric checks to inspect assumptions. No extra training or paid research round has been added.

## 130. Keep working in your own project

REFERENCE

Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.