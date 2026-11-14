---
theme: default
title: Solar forecasting with agent-assisted experiments
author: Anish Shah
info: Solar Forecasting Lab
class: cover
layout: default
aspectRatio: 16/9
canvasWidth: 1280
colorSchema: light
transition: fade
wakeLock: false
fonts:
  sans: IBM Plex Sans
  mono: IBM Plex Mono
  provider: none
mdc: true
highlighter: shiki
drawings:
  enabled: false
download: false
exportFilename: solar-autoresearch
---

<div class="kicker">0:00</div>

# Solar forecasting<br>with agent-assisted<br>experiments

<div class="sub">Use satellite observations to compare forecasting models and test agent-written code changes.</div><LabScene /><div class="bottom-note">A four-hour Python workshop using real archived observations.</div>


<!--
You are joining a fictional research lab preparing for its weekly forecast review. We will use real February 2014 satellite observations to predict X-ray flux thirty minutes ahead and solar images one hour ahead. First we will compare small trained models with copying the latest observation. Then we will ask an agent to edit the image experiment’s code and test those changes with the same comparison. This is a CPU teaching experiment, not an operational solar forecast.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:01</div>

# The lab needs a forecast for its weekly review

<div class="lab-assignment"><div class="lab-dialogue"><div class="scene-label">Fictional lab · the principal investigator</div><p>“Does the model predict anything better than assuming the Sun stays as it is?”</p></div><div class="lab-task"><h2>Your assignment</h2><p>Use observations from February 1–14, 2014 to test that question. Bring a forecast, its errors, and the code a colleague needs to repeat it.</p><p class="aside">The lab is fictional. The satellite observations are real.</p></div></div>


<!--
The principal investigator, or PI, runs the weekly research meeting. You are the researcher preparing a comparison for that meeting. The question is deliberately concrete: does a trained model predict the next observation better than simply copying the current one? We have two weeks of archived data, so we can hide later observations, make predictions, and then compare them with what was actually recorded. We are practicing an experiment design; these short runs cannot establish reliable solar forecasting.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:02</div>

# What the satellites recorded

<div class="opening-observations"><div class="scientific-figure"><img class="solar-photo" src="/images/v030-observations.png" alt="A GOES-15 XRS-B time series and an AIA 171 Å solar image from February 1, 2014"><div class="image-caption">Actual archive observations. NOAA GOES-15 and NASA/SDO AIA; false-color image.</div></div><div class="observation-tasks"><p><strong>GOES-15:</strong> two whole-Sun X-ray readings each minute, measured in watts per square metre.</p><p><strong>AIA 171 Å:</strong> an extreme-ultraviolet view of the Sun’s outer atmosphere, reduced to 64 × 64 pixels.</p></div></div>


<!--
GOES gives us two numerical measurements each minute: XRS-A and XRS-B measure X-ray power per square metre in different wavelength bands. The plot shows XRS-B, transformed with log10 because its values span a wide range. AIA is a different instrument on NASA’s Solar Dynamics Observatory. Its 171-angstrom images show extreme-ultraviolet emission from the Sun’s outer atmosphere. The colors represent intensity, not visible light or a direct temperature measurement. Our teaching arrays reduce the images to sixty-four by sixty-four pixels. SunPy retrieves and reads the observations and metadata; our preprocessing code builds the training arrays. These are separate forecasting tasks, not two inputs to one model. Sources: https://www.spaceweather.gov/products/goes-x-ray-flux and https://sdo.gsfc.nasa.gov/data/channels.php.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:03</div>

# What one forecast example contains

<ForecastExample /><div class="bottom-note">Persistence predicts no change. A trained model must beat it on the same future observations.</div>


<!--
Both examples shown here exist in the prepared training data. Set the clock to 01:00 UTC on February 1. For GOES, the model can read sixty one-minute samples in each channel, from 00:01 through 01:00, and must predict XRS-B at 01:30. Persistence uses only the current XRS-B reading as that forecast. For AIA, the model sees images from 00:00 and 01:00 and predicts the image at 02:00; persistence copies the 01:00 image. The future observations are targets for scoring, never inputs to the prediction. We compare absolute error in log-flux units for GOES and mean absolute error in normalized image intensity inside the solar disk for AIA. The scores stay separate. If little changes over the horizon, copying the latest observation can be hard to beat. We will measure that rather than assume the trained model wins.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:04</div>

# Bring a comparison your colleagues can repeat

<div class="lab-files"><div class="lab-folder"><div class="scene-label">Fictional lab shared folder</div><code>forecast_final.py</code><code>forecast_final_v2.py</code><code>forecast_final_final.py</code><code>forecast_final_USE_THIS.py</code><p>Last week’s score came from one of these.</p></div><div><h2>Show the comparison.</h2><p>Predictions and errors on the same dates, including persistence and the cases the model got wrong.</p><h2>Save what produced it.</h2><p>Data version, source, settings, trained weights, and outputs, together in one run.</p></div></div><div class="bottom-note">Later, an agent will edit the image-model code. We’ll test its changes using this same comparison.</div>


<!--
At the review, a lower error is useful only if we know what produced it and what it was compared with. The four final files are our fictional lab’s previous filing system. We will use Forge and W&B to connect the code, configuration, data, weights, and predictions to each run. The measurement task teaches that stack with a scalar output; the image task reuses it for predictions we can inspect pixel by pixel. Only then do we add an AI research assistant. It will read the image code and validation results and propose edits to the model or training procedure. It will not alter the data, target, or final scoring rules.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:05</div>

# Copy the notebook into your Forge project

<div class="copy-layout"><div class="template-qr"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view"><img src="/images/solar-template-qr.svg" alt="QR code opening the Solar workshop template"></a><p><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Open the Solar template ↗</a></p></div><ol><li>Open the template.</li><li>Choose <strong>Copy to project</strong> and select your writable project.</li><li>Open the copy in <strong>Edit</strong>. Choose <strong>Run all stale cells</strong> once.</li><li>In <strong>Connect</strong>, check your project. Exercise run buttons stay unpressed.</li></ol></div><div class="bottom-note">Hosted Forge supplies authentication. Your account supplies notebook compute and inference access.</div>


<!--
Allow participants to get their own copy open before continuing. Run all stale cells creates the controls; it does not press the exercise run buttons. Hosted Forge supplies authentication, but attendees still need their own project and account access. Use fictional or public teaching data in a public project.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:05</div>

# Copy the notebook into the project you will use

<div class="copy-native"><a class="copy-dialog" href="/images/visual-v030-solar-setup.png" target="_blank"><img src="/images/visual-v030-solar-setup.png" alt="Native Forge Copy to project dialog"></a><div><h2>Choose your destination.</h2><p>Select a project you can write to. Open the copy in Edit.</p><h2>Check it in the notebook.</h2><p>Hosted Forge detects the copied notebook’s project. Laptop users enter it in Connect.</p><p class="aside">After copying, check the project name in Connect. Your runs and traces should land there.</p></div></div>


<!--
Show the native copy dialog. The copied notebook uses its destination project. A laptop uses manual entry. Confirm the project before executing. The browser preview limitation remains separate from notebook execution.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:06</div>

# Run the same notebook on your laptop

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra solar
uv run --extra solar wandb login --verify
uv run --extra solar marimo edit notebooks/solar_autoresearch.py
```

<p class="aside">In Connect, enter <code>your-entity/your-project</code>. Keep the terminal open.</p><div class="bottom-note">Install Git and uv first. Hosted participants skip these commands.</div>


<!--
Hosted participants can skip this slide. On a laptop, install Git and uv, clone the repository, and run these commands. Authenticate in the terminal and keep that terminal open while marimo runs. There is no extra workshop service to start.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:06</div>

# Check the compute and inference settings

<table class="clean-table"><tbody><tr><th>Setting</th><th>This workshop</th></tr><tr><td>Project and credentials</td><td>Your own Forge project and account</td></tr><tr><td>Training compute</td><td>Notebook CPU; billed separately if hosted</td></tr><tr><td>Research agent</td><td><code>zai-org/GLM-5.3-Flash</code>, fixed</td></tr><tr><td>Inference allowance</td><td>$8 by default; adjustable in Connect</td></tr><tr><td>Execution</td><td>Explicit run buttons; saved work restores</td></tr></tbody></table><div class="bottom-note">A higher allowance permits more calls. It does not grant account access or include compute.</div>


<!--
Check these settings before running anything. The eight-dollar allowance applies to inference, while hosted notebook compute is separate. The research agent uses GLM-5.3-Flash with temperature 0.2, JSON output, and up to 16,384 output tokens. If that model is unavailable, stop and inspect the error rather than changing models mid-comparison.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:07</div>

# Wrap one operation, then inspect what you recorded

```python {1-2|3-6|7|all}
with tracing.Conversation(conversation_id=execution_id):
    with tracing.Turn(agent_name="researcher", messages=mission):
        with tracing.Tool(
            name="inspect_training_environment",
            arguments={}, result={"numpy": np.__version__},
        ) as tool:
            tool.set_attributes({"workshop.exercise": "solar-research"})
```

<div class="code-contract"><span><strong>Input:</strong> one operation and its observed result</span><span><strong>Output:</strong> a tool span inside a conversation</span></div>


<!--
Conversation identifies the execution. Turn holds the mission. Tool records one operation. The attribute line is the learner edit, not a second call. Actual instrumentation also supplies start and end timestamps and records exceptions. Run the free check, send the setup trace, then find the same field in Agent Lens. Advance the code highlights one step at a time; use Back to revisit the previous statement.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:08–0:15 · YOUR TURN</div>

<a class="answer-link" href="/89">Worked answer → 89</a>

# Connect and inspect your first tool call

<div class="task">Open <strong>1 · Connect</strong>.</div><ol class="exercise-controls"><li>Click <strong>Connect and restore my work</strong>. Check that the project is yours.</li><li>In <code>instrument_tool</code>, add the <code>workshop.exercise</code> attribute with value <code>solar-research</code>. Click <strong>Check my tracing code</strong>.</li><li>Click <strong>Send my first Agent Lens trace</strong>. Open the tool call in Agent Lens and find the attribute you added.</li></ol><div class="done">Check your work: Find your attribute beside the tool’s arguments and result.</div>


<!--
Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Find the field your code added to the span

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-trace" href="/images/visual-v030-solar-trace.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-trace.png" alt="Native Agent Lens setup tool span from the current Solar rehearsal"><span v-click="1" class="capture-mark" style="left:430px;top:195px;width:676px;height:74px" aria-label="Annotation 1: Tool arguments"><b>1</b></span><span v-click="2" class="capture-mark" style="left:430px;top:278px;width:676px;height:115px" aria-label="Annotation 2: Returned observation"><b>2</b></span></a><div class="product-caption"><span>Read the returned NumPy version. Open Raw to find workshop.exercise.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/4ca0a7e5c9d1fe30d24079ea5b98b750">Open the setup trace ↗</a></div><div class="image-caption">Recorded v0.3.0 environment check. No language-model call was needed.</div></div>


<!--
The exercise is complete when the participant can find their own attribute in their own tool span. Here is the recorded reference. The tool arguments, result, and duration describe one actual operation. The same instrumentation function records later training calls.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Predict X-ray flux 30 minutes ahead

<ForecastWindow mode="goes" /><div class="bottom-note">Predict log10 XRS-B flux. A forecast window includes observations, timestamps, and a future target.</div>


<!--
Read the timeline from left to right. The model receives sixty minutes of X-ray flux measurements and predicts XRS-B thirty minutes after the last input. Flux is measured in watts per square metre. We take log10 because values span a wide range; the forecast error is therefore in log-flux units. The model never receives the future target as an input.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:16</div>

# Locate the observed history and future target

<div class="scientific-figure"><img class="solar-photo" src="/images/v031-goes-window.png" alt="Actual first GOES training window with sixty samples of XRSA and XRSB, followed by the XRSB target thirty minutes later"><div class="image-caption">The two lines are observations. The orange point is the future target; no model forecast is plotted.</div></div>


<!--
Each input contains two channels and sixty one-minute samples, from minute minus fifty-nine through zero. Only XRS-B is predicted thirty minutes later. This plot reverses input standardization to show both channels in log-flux units. The target point is kept out of the input tensor.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:17</div>

# Use different dates to fit, choose, and evaluate

<ForecastWindow :split="true" /><div class="bottom-note">February 2014, UTC. Each example’s inputs and target stay inside one date partition.</div>


<!--
These dates serve three different research decisions. February 1–10 trains the model weights and supplies the normalization statistics. February 11–12 lets us compare architectures, settings, and later the agent’s code changes. We will look at those validation errors repeatedly, so they cannot also be our final test. February 13–14 stays reserved until we freeze the selected code and weights. Then we evaluate without training again. A window whose history or target crosses a boundary is excluded. The reserved dates give us an honest comparison for this short period, not evidence of reliable forecasting in other months.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:18</div>

# Normalize the inputs without changing the target units

<SolarComputation mode="normalization" /><div class="bottom-note">Notebook: choose a window, then toggle standardized inputs. The target does not change.</div>


<!--
load_goes first takes log10 of both flux channels. It fits one mean and standard deviation per channel using training inputs only, then reuses those values for validation and final inputs. The target remains unstandardized log10 XRS-B. That is why persistence returns split["persistence"] rather than copying a standardized tensor entry.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:19</div>

# Leave out windows with missing observations

<SolarDataRules mode="gaps" />


<!--
February 8 is absent from the prepared GOES source archive. A window that needs those readings cannot be used. Filling the absence with zero would tell the model that the instrument measured zero flux, which it did not.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:20</div>

# Inspect a solar observation with SunPy

```python
from sunpy.map import Map

observation = Map(dataset_path / "sample-aia.fits")
print(observation.date)
print(observation.wavelength)
print(observation.unit)
```

<div class="bottom-note">Inspect the FITS metadata here; use the prepared arrays for training.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> A representative FITS file</span><span><strong>Output:</strong> Observation time, wavelength, and units</span></div>


<!--
Open the representative FITS file and inspect its date, wavelength, and unit. Training uses prepared arrays so the class does not wait for archive downloads. The dataset includes the acquisition and preprocessing records, so we can trace those arrays back to the public observations.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:21–0:27 · YOUR TURN</div>

# Inspect the observations before training

<div class="task">Open <strong>2 · Solar data</strong>.</div><ol class="exercise-controls"><li>Click <strong>Load the solar dataset</strong>.</li><li>In the data preview, find an observation time, the image wavelength, and the train/validation/test dates.</li><li>Use the date diagram to explain why a window with inputs on February 10 and a target on February 11 would be excluded.</li></ol><div class="done">Check your work: You can say what the model receives and which future observation it must predict.</div>


<!--
Give participants six minutes. Have them explain one forecast window to a neighbor: which observations go in, which observation is the target, and which dates it belongs to. No training is needed yet.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:27</div>

# Start by copying the latest reading

```python
def persistence_forecast(split):
    # Latest observed value becomes the future prediction.
    ...
```

<p class="big">Predict flux 30 minutes ahead by copying the latest reading.</p><div class="bottom-note">This uses only a reading we already have. It does not look at the future target.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> The latest observed reading in each window</span><span><strong>Output:</strong> One 30-minute-ahead prediction per window</span></div>


<!--
Persistence means predicting that the latest value will stay the same. Solar observations are correlated over time, so this simple baseline can be hard to beat. At the lab review, someone will ask why we needed a neural network if copying the last reading worked. We should run that comparison before they ask.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:29</div>

# Measure how far the prediction missed

<SolarComputation mode="error" />


<!--
For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:30–0:40 · YOUR TURN</div>

<a class="answer-link" href="/90">Worked answer → 90</a>

# Write and test persistence

<div class="task">Open <strong>3 · Persistence</strong>.</div><ol class="exercise-controls"><li>Implement <code>persistence_forecast(split)</code>.</li><li>Click <strong>Check my persistence function</strong>, then <strong>Run my persistence baseline</strong>.</li><li>Inspect the observed and predicted curves. Identify one interval where copying the present misses the future.</li></ol><div class="done">Check your work: The plot shows your persistence forecast beside the observed flux. Point to one miss.</div>


<!--
Allow ten minutes. Let participants attempt the function before opening the answer. Ask them to find an interval where the real flux changed while persistence kept the previous value. That is a concrete error another model could try to reduce.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:40</div>

# Save what changed between runs

<p class="big">Suppose a second run has a lower validation error. What changed?</p><div class="step-path"><div><h2>Code</h2><p>You changed the loss function.</p></div><div><h2>Data</h2><p>You excluded an incomplete window.</p></div><div><h2>Settings</h2><p>You trained for more steps.</p></div></div><div class="bottom-note">Save these differences so someone else can repeat the comparison.</div>


<!--
A colleague at the review asks which setting changed. These are possible explanations, not claims about this rehearsal. If code, data, or training time differs, we need to know that before deciding why the score moved. Saving the active values answers the question without searching all four final notebooks.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:41</div>

# Which setting changed between these runs?

<RunInspector />


<!--
These are two recorded GOES runs. Before revealing the settings, ask what the scores let us conclude. Then click Show active settings. Both runs used the same source and training budget; their learning rates differed.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:42</div>

# These runs used different learning rates

<RunInspector :revealed="true" />


<!--
The learning rate changed from .001 to .003. Data, source, seed, steps, and batch size stayed the same. Both errors were worse than persistence. We can explain the setting change at the review, but we still cannot claim to have beaten the baseline. Check the predictions before deciding what to try next.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:42</div>

# How an observation becomes a prediction

<ResearchMap :level="0" />


<!--
The forecast model receives an input window and returns a number or image. The diagram starts with this calculation. We’ll add the model source, scoring rule, and saved outputs so another run can be compared with it.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:43</div>

# Save the model and training code with the run

<ResearchMap :level="1" /><div class="bottom-note">Save the source used for this run before editing it for the next experiment.</div>


<!--
The model and training functions are code we can change. Save the particular source used by this run, because the notebook may be edited again tomorrow.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:44</div>

# Use the same scoring rule for every model

<ResearchMap :level="2" /><div class="bottom-note">The model can change. The target, partition, and primary scoring rule stay fixed.</div>


<!--
Keep the target, dates, and primary metric unchanged while comparing models. If we changed the metric after seeing a result, the lower number could describe a different task. Our candidate code can change the predictor and training procedure while this comparison rule stays fixed.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:45</div>

# Save the files needed to repeat the run

<SolarComputation mode="records" />


<!--
A W&B run stores settings and metric history. A W&B Artifact stores a versioned bundle of files. Here that means the data, source, weights, and predictions needed to repeat or inspect a result.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:47</div>

# Save code and outputs with each training run

```python {1-5|6-7|8|all}
with session.stage(
    "measurement/run", config=config,
    sources={"candidate.py": source},
    inputs={"dataset": dataset_version, "split": "validation"},
) as stage:
    if stage.needs_run:
        result = train_model(data, config)
        stage.record(result)
```

<div class="bottom-note">You write the training function. The session records its code and outputs.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> Your source, configuration, and dataset version</span><span><strong>Output:</strong> A saved result that can be restored after restart</span></div>


<!--
This shortened example shows where saving sits around training. The notebook’s run_training function runs your source, then saves the result. If that same stage has already completed, the saved result can be restored instead of training again. Advance the code highlights one step at a time; use Back to revisit the previous statement.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:48</div>

# What changes during one training step

<SolarComputation mode="training" />


<!--
In fit, the GOES model predicts a batch and computes squared error against training targets. The shared loss function has an all-ones mask for GOES; the image exercise later uses the mask to select disk pixels. loss.backward computes gradients. Adam updates the forecasting model weights. The training targets participate in these updates. Validation inputs are predicted without gradients, and validation targets are scored by the parent process outside candidate code.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:49</div>

# Restore a completed run after a restart

<SolarComputation mode="checkpoint" />


<!--
The local completion record tells the notebook which work finished. The checkpoint Artifact stores a copy in your project. If the runtime is replaced, restore the checkpoint before continuing. An upload failure can be retried using the local files.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:50–1:05 · YOUR TURN</div>

<a class="answer-link" href="/91">Worked answer → 91</a>

# Write the loss and metric

<div class="task">Open <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Implement <code>training_loss</code> and <code>my_flux_mae</code>.</li><li>Click <strong>Check my measurement code</strong>. Test identical arrays and a constant one-unit error.</li><li>In <code>run_training</code>, find where it saves source, settings, weights, and predictions. The next exercise will produce those files.</li></ol><div class="done">Check your work: Your checks pass, and you can point to where run_training saves its files.</div>


<!--
Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:05</div>

# Changing settings, choosing models, and editing code

<SolarMechanism mode="search" />


<!--
There are three different operations here. Hyperparameter search supplies different values to the same implementation, such as learning rate or width. Architecture comparison chooses between implementations we already wrote, such as an MLP and a temporal CNN. Later, the research agent will write a code change that our current configuration options cannot express, such as replacing squared training loss with absolute loss. We’ll test that changed program with the same dates and scoring rule.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:06</div>

# How the MLP uses an hour of measurements

<SolarComputation mode="mlp" /><div class="bottom-note">Notebook: Run one forward pass and show tensor shapes. This does not train weights.</div>


<!--
The actual candidate code flattens a two-by-sixty input into one hundred twenty values. A linear layer learns weights for every input position, followed by ReLU and a linear scalar output. Width is sixteen or thirty-two in the search. The diagram omits the batch dimension and draws a few hidden units to represent the layer.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:06</div>

# How the temporal CNN uses the same measurements

<SolarComputation mode="cnn" /><div class="bottom-note">Choose Temporal CNN in the same check. Compare its output shapes with the MLP.</div>


<!--
The same two-by-sixty input now passes through a five-sample convolution with padding two. Filter weights are reused along time. The output has width channels and sixty positions; AdaptiveAvgPool1d(1) averages over time, then the linear layer predicts one value. This compares two implemented computations, not just two model names.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:07</div>

# Compare six model configurations

<table class="clean-table"><tbody><tr><th>Architecture</th><th>Widths</th><th>Learning rates</th><th>Training budget</th></tr><tr><td>Small MLP</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr><tr><td>Temporal CNN</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr></tbody></table><div class="bottom-note">Seed 17. Batch size 32. The notebook records the active values.</div>


<!--
The MLP reads the history as a fixed set of inputs. The temporal CNN applies shared filters along time. We’ll try three settings for each: widths sixteen and thirty-two, and learning rates .001 and .003. Every run gets seed seventeen, batch size thirty-two, and sixty training steps. That small budget keeps the exercise short; it does not establish which architecture would win after longer training.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:09</div>

# Run the configurations through W&B Sweeps

```python
sweep_id = wandb.sweep(sweep_config, entity=entity, project=project)

def trial():
    with wandb.init() as run:
        result = run_training(config_for(run.config.trial))
        run.log(result["metrics"])

wandb.agent(sweep_id, function=trial, count=6)
```

<div class="bottom-note">The notebook contains the full implementation and reuses already-completed runs.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> Six predefined configurations</span><span><strong>Output:</strong> Six tracked training runs with matching metrics</span></div>


<!--
The Sweep assigns a trial configuration, and wandb.init creates its tracked run. run_training fits the model, saves its files, and returns metrics; run.log adds those metrics to the run. wandb.agent repeats this for the six configurations. The notebook includes the full entity, project, and configuration setup shown in this shortened excerpt.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:10</div>

# Compare the six configurations in Forge

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-sweep" href="/images/visual-v030-solar-sweep.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-sweep.png" alt="Native six-run W&amp;B Sweep from the v0.3.0 Solar rehearsal"></a><div class="product-caption"><span>Find two MLP runs with the same width and different learning rates.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pzigourv">Open the Sweep ↗</a></div><div class="image-caption">All six validation forecasts were worse than persistence. A smaller error among them is still a failed baseline comparison.</div></div>


<!--
Use the latest rehearsal Sweep pzigourv. Start with two width-16 MLP runs, then compare their learning rates, error, and runtime. All six models lost to persistence. Do not infer an architecture conclusion from this short training exercise.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:11</div>

# Check whether the model has finished learning

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-loss.png" alt="Saved GOES model loss curve over 60 training steps"><div class="image-caption">Selected MLP: width 16, learning rate .003, seed 17. Saved v0.3.0 training losses.</div></div><div class="bottom-note">Historical 60-step run. A later worked repair tests scaling, residual prediction, and a longer budget together.</div>


<!--
The selected GOES model’s loss was still falling after sixty steps. That suggests testing a longer training budget, but it does not tell us that more steps would beat persistence. Look at the predictions and validation score alongside the curve. The later qualification tested a complete repaired recipe. It does not isolate the effect of additional training alone.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:15–1:30 · YOUR TURN</div>

<a class="answer-link" href="/92">Worked answer → 92</a>

# Run six configurations and inspect one forecast

<div class="task">Stay in <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Click <strong>Run six tracked configurations</strong>.</li><li>Open the Sweep. Compare validation error and training time for two configurations.</li><li>In the notebook, choose <strong>Inspect a saved measurement run</strong>. Compare its loss, forecast, and persistence. Follow its Forge links to the saved source.</li></ol><div class="done">Check your work: Explain one comparison using the settings, curve, and forecast.</div>


<!--
Allow fifteen minutes. Ask participants to predict which configuration will win before running the search. After it finishes, have them explain one result from the loss curve and forecast. Keep failed runs visible so the comparison accounts for what happened.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:24</div>

# Let the model learn a correction to persistence

```python {2|3|4|all}
def forward(self, x):
    correction = self.net(x)
    standardized = x[:, 1, -1:] + correction
    return standardized * self.scale + self.center

# Zero-initialize the correction head before training.
# Fit scaling on training dates; score in log-flux units.
```

<div class="bottom-note">The repair also uses absolute loss and 1,200 updates. These choices are tested together.</div>


<!--
The latest XRS-B input is standardized. Add a learned correction, then convert it back with the same training-fitted center and scale. A zero-initialized final layer begins exactly at persistence. The fit function divides the prediction and target error by the same scale. We changed several parts of the recipe together, so the measured result cannot tell us which individual change caused the gain. Ask participants to point to the addition and unit conversion in their editable code. Advance the code highlights one step at a time; use Back to revisit the previous statement.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:25–1:30 · YOUR TURN</div>

# Test the worked measurement repair

<div class="task">Stay in <strong>4 · Track and search</strong>, below the saved forecasts.</div><ol class="exercise-controls"><li>Read <code>forward</code> and <code>fit</code> in <strong>Worked GOES repair: inspect or edit the forecasting code</strong>.</li><li>Click <strong>Check the GOES repair code</strong>, then <strong>Train the worked GOES repair</strong>.</li><li>Compare validation error with persistence and your search. Open its training call and weights Artifact.</li></ol><div class="done">Check your work: Explain the initial forecast, the output units, and whether your validation error fell.</div>


<!--
Use the last five minutes of the measurement exercise. This is one CPU run, not another paid agent request. Its exact source, configuration, and weights are saved separately. The recipe beat persistence on three predeclared seeds in qualification, but a learner edit is a new experiment. Final selection considers its validation score; do not choose using final dates.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:30–1:40</div>

# Ten-minute break

<p class="big">Save your work and take ten minutes.<br>We’ll start the image experiment when we return.</p><p>The lab coffee has no validation score. Use your judgment.</p><div class="bottom-note">The notebook can stay open. There’s no exercise to run during the break.</div>


<!--
Take ten minutes. Confirm saved work is visible before leaving. The lab coffee is optional; saving the experiment is worth doing first. No background experiment is required during the break.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:40</div>

# Predict the solar image one hour ahead

<ForecastWindow mode="images" /><div class="bottom-note">AIA 171 Å. Prepared 64 × 64 arrays. One-hour forecasting.</div>


<!--
Now we give the model images from sixty minutes ago and now, and ask for the image sixty minutes ahead. The AIA 171 Å arrays are 64 by 64 pixels so the exercise can run on CPU.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:42</div>

# Track the image model with the same experiment records

<ResearchMap :level="3" /><div class="bottom-note">The input and prediction changed shape. Source, settings, weights, and evidence still belong together. The image score uses normalized log1p intensity.</div>


<!--
The inputs are now images, but we still save the same kinds of records: data, code, settings, weights, and predictions. Image values use normalized log1p intensity, so their errors have a different scale from the GOES errors.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:44</div>

# See exactly which images become input and target

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-image-window.png" alt="Earlier and current AIA observations beside the future target"><div class="image-caption">First accepted training window. All three images share the same intensity scale.</div></div><div class="bottom-note">The target is hidden from the model during prediction. It is used afterward to measure the miss.</div>


<!--
Read the observation times. Channel zero is the earlier image; channel one is the current image. The third image is the future target. These are three real observations from a training window, not three outputs of an AI image generator.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:46</div>

# Predicting the future image with a small CNN

<SolarMechanism mode="residual" :reveal="1" />


<!--
The two observations become two input channels. The CNN returns one channel containing its predicted future image. The batch dimension stays the same: input shape is batch by two by sixty-four by sixty-four, and output shape is batch by one by sixty-four by sixty-four. This direct predictor has to produce the whole image from its learned weights.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:48</div>

# Predict a correction to the current image

<SolarMechanism mode="residual" :reveal="2" />


<!--
Much of the current image may remain similar one hour later. We can copy that image and ask the network to predict the correction. Add the network output to x[:, 1:2], the current-image channel. The slice preserves the channel dimension. If the correction is zero, the model returns persistence exactly. The local check will test that behavior.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:49</div>

# Implement the residual predictor’s forward pass

```python {2|3|4|all}
def forward(self, x):
    correction = self.net(x)       # [batch, 1, 64, 64]
    current_image = x[:, 1:2]      # keep the channel axis
    return current_image + correction
```

<div class="code-contract"><span><strong>Input:</strong> earlier image + current image</span><span><strong>Output:</strong> one future image per example</span></div><p class="aside">Check: if <code>correction</code> is zero, the forecast equals the current image.</p>


<!--
The diagram and code describe the same addition. Ask participants why x[:, 1] would remove a dimension and why x[:, 1:2] preserves it. The notebook implementation also branches on architecture so the convolutional comparison still returns only the network output. Advance the code highlights one step at a time; use Back to revisit the previous statement.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:49</div>

# Inspect the correction produced by the saved model

<div class="scientific-figure"><img class="solar-photo" src="/images/v031-residual-correction.png" alt="Current AIA image plus the saved residual model correction equals its forecast"><div class="image-caption">First validation case. Current image and forecast use the same intensity scale; the middle panel shows a signed correction.</div></div>


<!--
The center image is calculated from the saved manual residual forecast minus the current input. It shows what this trained network added. It is not the physical change observed on the Sun. Zero is white in the correction view, with negative and positive values on opposite sides of the colorbar. The panels show the equation implemented by forward.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:50</div>

# Measure prediction error inside the solar disk

<SolarMechanism mode="mask" />


<!--
This is a diagram of the scoring calculation, not a forecast. The fixed mask assigns one to disk pixels and zero outside. Multiply absolute errors by the mask, average over the selected pixels per image, then average images. A changed off-disk pixel must not affect the score.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:51</div>

# Check the image scorer on three known errors

```python {1|2-3|4|all}
absolute_error = np.abs(prediction - target)
per_image = (absolute_error * disk_mask).sum(axis=(1, 2, 3))
per_image /= disk_mask.sum(axis=(1, 2, 3))
return float(per_image.mean())
```

<div class="code-contract"><span><strong>Identical arrays:</strong> score 0</span><span><strong>Every disk pixel +1:</strong> score 1</span><span><strong>Only off-disk pixels +1:</strong> score 0</span></div>


<!--
Run the three local examples before training. They explain what the scorer measures. The participant writes this development scorer, and the protected primary scorer checks the comparison with the same published rule. Missing or invalid predictions are not zero error. Advance the code highlights one step at a time; use Back to revisit the previous statement. In the notebook, move the error outside the scoring mask, then click Try my image scorer on these pixels. The two public grids have different mask sizes; images still receive equal weight.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:52</div>

# Training loss and evaluation error have different jobs

<SolarComputation mode="loss" />


<!--
The training loss supplies gradients for the optimizer. The evaluation metric scores the finished predictions. Our starting loss uses squared error, while the comparison uses absolute error inside the disk. A candidate can change the loss to alter how weights are learned. We keep the evaluation metric fixed so we can compare the resulting forecasts.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:54</div>

# Compare forecasts for the same validation case

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-validation-predictions.png" alt="Matched convolutional and residual predictions beside the same observed future"><div class="image-caption">Recorded v0.3.0 forecasts. First accepted validation case; common intensity and error scales.</div></div><div class="bottom-note">Notebook: select one forecast timestamp. Compare persistence and both models on common scales.</div>


<!--
The same current image and observed future appear in both rows. The convolutional forecast is above, residual below. The figure uses the first accepted case, not a selected success. Colors use the same scale across both rows. A single image is an example; the validation score includes all 142 windows.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:55–2:15 · YOUR TURN</div>

<a class="answer-link" href="/93">Worked answer → 93</a>

# Implement and compare the image predictors

<div class="task">Open <strong>5 · Solar images</strong>.</div><ol class="exercise-controls"><li>Edit <code>ImagePredictor.forward</code>, <code>training_loss</code>, and <code>my_image_mae</code>.</li><li>Click <strong>Check my image code</strong>. A +1 error should score 1; an off-disk change should score 0.</li><li>Click <strong>Compare convolutional and residual predictors</strong>. Inspect both forecasts.</li></ol><div class="done">Check your work: Show which model validation selected, then point to a region where its forecast missed.</div>


<!--
Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:15</div>

# Use the experiment to test agent-written changes

<SolarComputation mode="evidence" /><div class="bottom-note">The lab has recruited an AI research assistant. We still review and test its work.</div>


<!--
The lab now has code, saved experiments, and a comparison we can inspect. The PI suggests bringing in an AI research assistant to propose the next changes. It reads the current source, active settings, validation errors, and any failures. We still review its diffs and run them through the training and scoring functions we built. The new colleague gets no exemption from testing.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:17</div>

# Which model is being trained?

<SolarMechanism mode="weights" />


<!--
The language model and the forecasting network have different roles. GLM writes Python using its fixed pretrained weights; we are not fine-tuning it. The small forecasting network trains new weights each time we test candidate Python. We send its validation results back to the language model when requesting the next edit.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:19</div>

# Limit edits to the model and training code

<div class="two-col"><div><h2>The assistant may edit</h2><p>Model layers<br>Feature computation<br>Training loss<br>Training procedure</p></div><div><h2>The experiment keeps fixed</h2><p>Training and validation dates<br>What we predict<br>How we score predictions<br>The reserved final-test dates</p></div></div><div class="bottom-note">Candidate Python runs in this notebook’s environment after your review.</div>


<!--
The research assistant can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution, just as you would for a colleague. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:21</div>

# Give the agent the inputs needed to explain a run

<div class="step-path"><div><h2>Exact source</h2><p>The files that produced the parent result.</p></div><div><h2>Active settings</h2><p>Architecture, steps, width, optimizer values.</p></div><div><h2>Validation evidence</h2><p>Curves, errors, predictions, and failed attempts.</p></div></div><div class="bottom-note">A default in source may not be the value the run used.</div>


<!--
The agent needs the exact source that produced the current result, the settings used in that run, and its validation outputs. For example, a default learning rate in candidate.py may be overridden by the active configuration. If we sent only the default, the agent could propose a change based on a setting we never used.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:23</div>

# Follow the agent’s work in Agent Lens

<div class="step-path"><div><h2>Open the request</h2><p>Read what we asked the agent to change.</p></div><div><h2>Inspect the tool calls</h2><p>Find the evidence it read and the code it returned.</p></div><div><h2>Follow the test</h2><p>Open the training call and look at its result or error.</p></div></div><div class="bottom-note">Compare the agent’s stated reason with what happened when its code ran.</div>


<!--
Open the research conversation in Agent Lens. Start with the mission, then find the evidence-reading tool and the returned code. Follow a training call to its result or error. Compare that sequence with the agent’s explanation of its change.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:24</div>

# Read the evidence that went into the proposal

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-evidence" href="/images/visual-v030-solar-evidence.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-evidence.png" alt="Native read_validation_evidence span from the current Solar proposal"><span v-click="1" class="capture-mark" style="left:70px;top:3px;width:800px;height:190px" aria-label="Annotation 1: Parent settings"><b>1</b></span><span v-click="2" class="capture-mark" style="left:70px;top:210px;width:800px;height:184px" aria-label="Annotation 2: Validation evidence"><b>2</b></span></a><div class="product-caption"><span>Find the parent configuration and validation error before reading its proposal.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7/spans">Open the proposal ↗</a></div><div class="image-caption">Recorded v0.3.0 round 1. The agent receives validation evidence, never the reserved-date score.</div></div>


<!--
Open read_validation_evidence. Find the residual architecture, forty training steps, seed seventeen, and parent validation error. Then inspect the returned proposal. This request initially exhausted its output budget and used a saved retry; that is an execution event, not a change in forecasting quality.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:25–2:40 · YOUR TURN</div>

<a class="answer-link" href="/95">Worked answer → 95</a>

# Choose the evidence for the research agent

<div class="task">Open <strong>6. Test agent-written changes to the image model</strong>.</div><ol class="exercise-controls"><li>In <code>select_validation_evidence(record)</code>, keep the active settings and validation results. Click <strong>Check my evidence selection</strong>.</li><li>Read the check result. Confirm that the final-test example is rejected.</li><li>Name the validation fields your function will send to the agent. What can it learn from them?</li></ol><div class="done">Check your work: You can name the code and validation results the agent will receive.</div>


<!--
Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:40</div>

# Ask for two changes to the same starting code

<ResearchBranches :level="1" /><div class="bottom-note"><a href="https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335">Harness²-inspired</a>: our probes train forecasting weights and include validation scores.</div>


<!--
Both candidates start from the same source and training configuration. We ask the agent to explain each proposed change, then review its diff. This uses the Propose–Probe–Compose structure from Harness². In our teaching adaptation, a probe trains forecasting weights and gives validation results to the editor. It differs from the paper’s task protocol.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:41</div>

# The first proposal changes one loss operation

```python
def training_loss(prediction, target, mask):
    # Before: square each miss.
    # After: take its absolute size.
    return ((prediction - target).abs() * mask).sum() / mask.sum()
```

<div class="diff"><div class="del">− (prediction - target).square()</div><div class="add">+ (prediction - target).abs()</div></div><p class="aside">Agent’s hypothesis: training on absolute error may help the fixed absolute-error score. The probe tests that claim.</p>


<!--
This is the actual first-round Candidate A edit in v0.3.0. It changes the training objective, while the evaluation scorer remains fixed. The alternative candidate retains the original squared loss. The diff establishes the proposed change; it does not establish an improvement until both run.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:42</div>

# Train and score each candidate

<ResearchBranches :level="2" /><div class="bottom-note">Use the same training and validation data. Keep failed runs visible.</div>


<!--
Train each candidate on the same training dates and compare its validation error. If one fails before producing a forecast, inspect the error and leave its score missing.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:44</div>

# Choose or combine changes using the probe results

<ResearchBranches :level="3" /><div class="bottom-note">The agent can keep A, keep B, combine changes, or retain the starting code.</div>


<!--
After both probes, the agent receives their code and validation results. It can keep one candidate, combine changes, or retain the starting source. Two suggestions do not obligate the lab to accept two changes. Read its rationale beside the scores. The dashed lines show which results it reviewed; they do not mean both candidates were merged into the selected code.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:46</div>

# Train the composed version before adopting it

<ResearchBranches :level="4" /><div class="bottom-note">Run the selected code on the same training and validation dates.</div>


<!--
A combined edit has not yet been measured, so it needs its own training run. Even if the agent retains an existing version, the controller tests the chosen source and records the result. This separates the decision about what to keep from the execution that confirms what ran.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:48</div>

# Adopt the tested code only if validation error is lower

<SolarDataRules mode="adoption" />


<!--
The composition is a proposed source version. After it trains, choose_adoption compares its fixed validation_error with the parent. A strictly lower score adopts the tested version. Equal error, a higher error, or failed execution retains the parent. The decision and the execution are separate records. This rule uses no final-test score.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:47</div>

# Open the training call behind the chosen version

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-training" href="/images/visual-v030-solar-training.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-training.png" alt="Native train_and_validate tool span with actual source settings and returned metrics"><span v-click="1" class="capture-mark" style="left:14px;top:45px;width:880px;height:160px" aria-label="Annotation 1: Training settings"><b>1</b></span><span v-click="2" class="capture-mark" style="left:14px;top:245px;width:880px;height:145px" aria-label="Annotation 2: Measured output"><b>2</b></span></a><div class="product-caption"><span>Check the configuration, then find validation_error in the returned result.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289">Open the selected training call ↗</a></div><div class="image-caption">Recorded v0.3.0 round 2 composition test. “error” is forecast error here, not an exception.</div></div>


<!--
The operation trained and validated the selected source. Find the returned score and compare the run to the saved source artifact. An error metric of 0.110916 is the forecasting metric, not a tool failure. If a span actually failed, inspect its exception separately.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:48</div>

# Use the selected code and results in round two

<ResearchBranches :level="5" /><div class="bottom-note">Use the selected code and what the first tests showed to plan the next changes.</div>


<!--
Round two begins with the code selected in round one and a saved lesson explaining what the probes showed. The agent reads both before proposing its next edits. It may now change code introduced by its previous proposal. That repeated use of the earlier result is the recursive part of this research procedure.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:50–3:00 · YOUR TURN</div>

# Propose and test two changes

<div class="task">Inspect <code>next_research_action</code> in <strong>6. Test agent-written changes to the image model</strong>.</div><ol class="exercise-controls"><li><strong>Propose two code changes</strong>. Read both diffs.</li><li>Confirm review of Candidate A → <strong>Test Candidate A</strong>. Confirm review of Candidate B → <strong>Test Candidate B</strong>.</li><li><strong>Record my comparison</strong>, then <strong>Request a composition</strong>.</li></ol><div class="done">Check your work: Each candidate’s proposal diff and training result are linked in Agent Lens.</div>


<!--
Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:00–3:15 · YOUR TURN</div>

<a class="answer-link" href="/96">Worked answer → 96</a>

# Test the selected code, then begin round two

<div class="task">Continue the same workbench.</div><ol class="exercise-controls"><li>Confirm review of composition, then <strong>Test the composition</strong>.</li><li>Click <strong>Save the adopted version and lesson</strong>. Check whether the parent was retained.</li><li>Repeat the process in round two using the previous outcome.</li></ol><div class="done">Check your work: Open the selected version from each round and explain why it was kept.</div>


<!--
Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:15</div>

# Follow one proposal through the branch diagram

<ResearchBranches :level="5" :interactive="true" :recorded="true" />


<!--
Click a candidate, its test, and the selection step. Follow the source change to its validation result and explain why the agent retained or rejected it. This deck diagram explains the process. The notebook’s branch view links the participant’s own files, decisions, traces, and results.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:17</div>

# Keep the selected code and weights fixed for final evaluation

<SolarComputation mode="inference" />


<!--
We have used validation dates to choose the version we will bring to the review. Save that source and its trained weights together before looking at February thirteenth and fourteenth. Final evaluation loads those weights and predicts the reserved inputs without training or selecting again. If we edit after inspecting these results, we need new reserved dates to test the next claim.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:19</div>

# Load the saved weights to make final predictions

```python
model = build_model(input_shape, frozen_config)
model.load_state_dict(saved_weights)
model.eval()
with torch.no_grad():
    prediction = model(final_inputs)
```

<div class="bottom-note">There is no optimizer step in this stage.</div>


<!--
Load the saved weights, switch to evaluation mode, and predict without an optimizer step. Final evaluation measures the selected trained model; it does not train another one.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:21</div>

# Match each prediction to the same observation times

<table class="clean-table"><tbody><tr><th>Case identity</th><th>Persistence</th><th>Manual</th><th>Agent-selected</th></tr><tr><td>Same input timestamps</td><td>Prediction + error</td><td>Prediction + error</td><td>Prediction + error</td></tr><tr><td>Same target timestamp</td><td>Saved output</td><td>Executed source</td><td>Executed source</td></tr></tbody></table><div class="bottom-note">Use each case ID to find the same input and target times in Weave or EvalTables.</div>


<!--
Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Native EvalTables was unavailable during the rehearsal, so the notebook and Weave comparison remain available; publication can be retried separately.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:25–3:45 · YOUR TURN</div>

<a class="answer-link" href="/97">Worked answer → 97</a>

# Test the selected models on reserved dates

<div class="task">Open <strong>7. Evaluate the selected models on reserved dates</strong>.</div><ol class="exercise-controls"><li>Click <strong>Freeze versions and evaluate reserved dates</strong>.</li><li>Choose one timestamp. Compare each image forecast with the same observed future.</li><li>Open one result’s training record and Agent Lens call. Compare the image scores separately from the GOES scores.</li></ol><div class="done">Check your work: Explain a difference between two forecasts using their images and scores.</div>


<!--
Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:45 · RECORDED REHEARSAL</div>

# In this rehearsal, image error fell 10.15%

<div class="measured-grid"><div><div class="measured-gain">10.15%</div><p>less error than the manually selected model</p><p class="aside">Agent edits: use absolute training loss, then zero-initialize the residual head.</p></div><table class="clean-table"><tbody><tr><th>Frozen version</th><th>Masked MAE ↓</th></tr><tr><td>Persistence</td><td>0.125762</td></tr><tr><td>Manual residual model</td><td>0.122442</td></tr><tr><td>Agent-selected code</td><td>0.110011</td></tr></tbody></table></div><p class="aside">Actual AIA 171 Å observations. 199 overlapping windows; February 13–14, 2014; one seed. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the recorded comparison ↗</a></p><div class="bottom-note">A measured result from this rehearsal, not a promised outcome for your edits.</div>


<!--
The selected agent code combined the absolute training loss from round one with a zero-initialized residual head from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:46 · RECORDED REHEARSAL</div>

# Compare the two models on one reserved-date image

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-final-predictions.png" alt="Manual and agent-selected forecasts for the same first accepted final case"><div class="image-caption">Forecast origin 2014-02-13T02:48 UTC. Same inputs, target, intensity scale, and error scale.</div></div><div class="bottom-note">The first accepted case is shown, not the case with the largest improvement.</div>


<!--
This figure is regenerated from the fresh v0.3.0 saved predictions. Compare manual and agent-selected forecasts on exactly the same case. The fixed error scale helps show differences without changing the colors between rows. The aggregate score includes all 199 accepted final windows.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:46 · THREE-SEED CHECK</div>

# The image edits helped two seeds and slightly hurt one

<div class="scientific-figure"><img class="solar-photo" src="/images/images-seeds-deck.png" alt="Combined image edits lower error for seed 17 from 0.122442 to 0.110011 and seed 29 from 0.117650 to 0.109566, but raise seed 43 from 0.110168 to 0.110397"><div class="image-caption">Same saved sources, 40 updates per run, three predeclared training seeds. Final dates were already known.</div></div><div class="bottom-note">Mean error falls 5.79%. The predeclared requirement to improve every seed fails.</div>


<!--
The earlier ten point one five percent result remains correct for seed seventeen. It is not a result to promise for every run. Seed forty-three already has a strong manual model, and the combined edits are slightly worse. Its loss-only edit does better than both, which is retained in the full table. Initialization and sampled batches both change with the seed, so we do not know which caused this difference. This is fixed-code repetition, not three independent agent discoveries.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:47 · RECORDED REHEARSAL</div>

# The GOES model performed worse than persistence

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-final.png" alt="Observed GOES flux, persistence forecast, and selected model prediction on reserved dates"><div class="image-caption">Final log-flux MAE: selected model 2.469; persistence 0.193. 2,694 accepted windows.</div></div><div class="bottom-note">Compare this forecast with its loss curve before deciding what to change next.</div>


<!--
These are the fresh saved final GOES predictions. The selected sixty-step neural model misses badly, while persistence follows the observed flux much more closely. The later repaired recipe changes scaling, residual initialization, loss, and training budget together. Its separately recorded three-seed test follows; this historical failure remains unchanged.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:47 · THREE-SEED CHECK</div>

# The measurement repair passed its three-seed check

<div class="scientific-figure"><img class="solar-photo" src="/images/goes-seeds-deck.png" alt="GOES persistence MAE is 0.192706; the repaired recipe scores 0.162878, 0.163880 and 0.163760 for seeds 17, 29 and 43"><div class="image-caption">Recorded qualification: selected on validation dates, then evaluated with frozen weights on known final dates.</div></div><div class="bottom-note"><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md">All configurations, seeds, sources, and reproduction instructions ↗</a></div>


<!--
The residual MLP at twelve hundred updates was selected using the mean validation score across seeds seventeen, twenty-nine, and forty-three. Its final mean error is 0.163506, fifteen point one five percent below persistence. All three repetitions improve. These are the same known final dates and overlapping windows; this is a teaching retest, not another independent solar benchmark. There were no new agent calls. The notebook runs this recipe only when the learner clicks Train the worked GOES repair.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:48</div>

# Read the saved score for one image in Weave

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-comparison" href="/images/visual-v030-solar-comparison.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-comparison.png" alt="Native Weave expanded row showing prediction mean, target mean, file index, and error"><span v-click="1" class="capture-mark" style="left:23px;top:56px;width:1000px;height:253px" aria-label="Annotation 1: Array summaries"><b>1</b></span><span v-click="2" class="capture-mark" style="left:23px;top:310px;width:1000px;height:36px" aria-label="Annotation 2: Pixel-wise score"><b>2</b></span></a><div class="product-caption"><span>Find file_index 0 and its error. Why is the score not the difference between the two means?</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the linked results ↗</a></div><div class="image-caption">One saved agent-selected case. Image means summarize the arrays; the score averages pixel errors inside the disk mask.</div></div>


<!--
This expanded native Weave row is the first final agent-selected image, file_index zero. Prediction mean is −1.760701 and target mean is −1.759181, but masked MAE is 0.109328. Differences between bright and dark pixels can cancel in a mean. The scorer instead takes each pixel’s absolute error before averaging. Open the saved array to see the forecast. The notebook supplies the aligned comparison; this is not native EvalTables. Match this case_id and file_index to the notebook timestamp selector. The per-image score and full-split mean are shown separately.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:49</div>

# Check that the saved source contains both selected edits

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-artifact" href="/images/visual-v030-solar-artifact.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-artifact.png" alt="Native W&amp;B Artifact code view showing the selected candidate.py"></a><div class="product-caption"><span>Find the zero-initialized output layer and the absolute training loss.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0">Open the Artifact ↗</a></div><div class="image-caption">The same Artifact also holds <code>losses.json</code>, <code>weights.pt</code>, and <code>predictions.npy</code> from this training run.</div></div>


<!--
This is execution-f7550caa1639e8366efbf9d84a782289, the exact selected round-two composition. Open the source and weights together. The final evaluation loaded these weights. A different source file with the same model label would not reproduce this experiment.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:50–3:58 · YOUR TURN</div>

# Write down what changed and whether it helped

<div class="task">Use your own comparison.</div><ol class="exercise-controls"><li>Name one code change and report its error on the reserved dates.</li><li>Include a forecast that still missed. Say what you would try next.</li><li>Click <strong>Publish my conclusion</strong>. Follow a link in your Report back to the saved code or prediction.</li></ol><div class="done">Check your work: Your conclusion names the change, the measured result, and a remaining problem.</div>


<!--
Allow eight minutes. Ask participants to name a change, report what happened, and include a remaining miss. A negative result is fine. If publication fails, save the conclusion and retry the upload without rerunning the experiment.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:58–4:00</div>

# Bring the results to the lab review

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-report" href="/images/visual-v030-solar-report.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-report.png" alt="Native Report excerpt summarizing the latest Solar technical rehearsal"></a><div class="product-caption"><span>Bring one result, its saved source, and the next experiment you would try.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the Report ↗</a></div><div class="image-caption">Recorded technical rehearsal. Use your own completed runs when writing your Report.</div></div>


<!--
Return to the weekly lab review. Ask participants to open their Report and follow one result to its source and saved prediction. In the recorded rehearsal, the selected image model reduced error, while the GOES model still lost to persistence. Both belong in the review. The image result uses one seed and two test days; it needs testing on other dates. The later qualification found that a repaired GOES recipe beat persistence on all three seeds. The saved image edits helped two seeds and slightly hurt one. Bring both facts to the review; neither replaces the original evidence. Ask each participant to propose a next test grounded in their own forecast.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">REFERENCE</div>

# Reference and worked answers

<p class="big">Use these after an attempt, or when live access is unavailable.</p><p>Recorded examples belong to the November 13 technical rehearsal. They are not results from your unexecuted changes.</p><div class="bottom-note">Use the return links to continue the workshop.</div>


<!--
These pages are optional answers and recorded examples. Open an answer after participants have tried the exercise. Use the return link to get back to the teaching sequence.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Put the attribute inside the tool scope

```python
def instrument_tool(observation):
    with tracing.Tool(
        name=observation["name"],
        arguments=observation["arguments"],
        result=observation["result"],
        started_at=stamp(observation["started_at"]),
        ended_at=stamp(observation["ended_at"]),
    ) as tool:
        tool.set_attributes({"workshop.exercise": "solar-research"})
        if observation.get("error"):
            tool.record_error(RuntimeError(observation["error"]))
```


<div class="source-link"><a href="/11">Return to Connect and inspect your first tool call →</a></div>

<!--
The attribute is attached inside the Tool scope. The complete notebook function also supplies its call identity and outer conversation. Use the operation’s timestamps so Agent Lens shows when the work happened, not when it was uploaded.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Return a copy of the latest observation

```python
def persistence_forecast(split):
    return split["persistence"].copy()
```

<p>The copy lets you work with the predictions without changing the dataset.</p>
<div class="source-link"><a href="/22">Return to Write and test persistence →</a></div>

<!--
The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Implement the training loss and forecast metric

```python
def training_loss(prediction, target, mask):
    return ((prediction - target).square() * mask).sum() / mask.sum()

def my_flux_mae(prediction, target):
    return float(np.abs(prediction - target).mean())

assert my_flux_mae(np.ones(3), np.zeros(3)) == 1.0
assert my_flux_mae(np.zeros(3), np.zeros(3)) == 0.0
```

<p class="aside">Training uses squared error. Evaluation reports mean absolute error.</p>
<div class="source-link"><a href="/33">Return to Write the loss and metric →</a></div>

<!--
Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Compare the settings and loss curves

<p class="big">Open two runs from the Sweep. Compare their model, width, learning rate, and training steps.</p><p>Then open the loss curves. A lower validation error is easier to interpret when you can see how each model trained.</p><div class="bottom-note">If a run failed, inspect its error. A missing score cannot rank that model.</div>
<div class="source-link"><a href="/41">Return to Run six configurations and inspect one forecast →</a></div>

<!--
Open the configuration and curve for two runs. Find the settings they share and the value that differs. If training failed, inspect the error rather than assigning a score to a forecast that does not exist.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Average the error inside the disk mask

```python
def my_image_mae(prediction, target, disk_mask):
    errors = np.abs(prediction - target) * disk_mask
    per_image = errors.sum(axis=(1, 2, 3))
    per_image /= disk_mask.sum(axis=(1, 2, 3))
    return float(per_image.mean())
```

<p>Test zero error, constant +1 error, and an error only outside the mask.</p>
<div class="source-link"><a href="/56">Return to Implement and compare the image predictors →</a></div>

<!--
The mask selects the solar disk. Compute the sum and count per image, then average across images. Check identical arrays, a constant one-unit difference, and a difference only outside the mask.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Add the correction to input channel 1

```python
def forward(self, x):
    correction = self.net(x)
    if architecture == "residual":
        return x[:, 1:2] + correction
    return correction
```

<div class="bottom-note">The current image is input channel 1. The return has one channel.</div>


<!--
Channel zero is the earlier image and channel one is the current image. Add the correction to channel one. With a zero correction, this function returns the current image exactly.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Return validation evidence only

```python
def select_validation_evidence(record):
    if record.get("split") != "validation":
        raise ValueError("Only validation evidence is allowed.")
    fields = ("split", "config", "metrics", "losses",
              "errors", "trace", "stage_id", "lessons")
    return {name: record[name] for name in fields if name in record}
```

<div class="bottom-note">The agent also receives the current source. Keep final predictions and scores out of this request.</div>
<div class="source-link"><a href="/63">Return to Choose the evidence for the research agent →</a></div>

<!--
First check that the record belongs to validation. Then return only the listed evidence fields. The current source is supplied separately. The final-test example should raise an error before the agent sees it.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Pass the candidate’s code to training

```python
candidate = proposal["candidates"][candidate_index]
probe = run_training(
    session, stage_name, candidate["source"],
    image_splits, parent["config"], dataset_version, metric_source,
)
```

<div class="bottom-note">Use the candidate’s source here. Passing the parent would train the old program again.</div>
<div class="source-link"><a href="/73">Return to Test the selected code, then begin round two →</a></div>

<!--
Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Use the saved model without training it again

<p class="big">Load each selected model’s saved weights and predict the reserved dates.</p><p>Compare the three image forecasts at one timestamp. The input images and observed future should match across all three rows.</p><div class="bottom-note">Persistence copies the current image and needs no trained weights.</div>
<div class="source-link"><a href="/78">Return to Test the selected models on reserved dates →</a></div>

<!--
The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 1: absolute loss versus the unchanged model

<table class="clean-table"><tbody><tr><th>Tested source</th><th>Validation error ↓</th></tr><tr><td>Starting residual model</td><td>0.122116</td></tr><tr><td>A · use absolute training loss</td><td>0.120553</td></tr><tr><td>B · retain squared training loss</td><td>0.122116</td></tr></tbody></table><p>The composition selected A. Its separate test reproduced 0.120553.</p><div class="bottom-note">Recorded v0.3.0: one seed, 142 validation windows, the same forty-step budget.</div>


<!--
The alternative is a real KEEP decision and it is still tested. Candidate A changes only the loss and lowers validation error in this run. The composition keeps A. This is one seed, not evidence of a repeatable effect.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 2: start the correction at zero

```python
if architecture == 'residual':
    nn.init.zeros_(self.net[-1].weight)
    nn.init.zeros_(self.net[-1].bias)

# The residual forward pass remains:
return prediction + x[:, 1:2]
```

<div class="bottom-note">The round-one absolute loss stays. Zero initial correction makes the initial forecast persistence.</div>


<!--
This is the second-round selected edit in v0.3.0. The last convolution starts at zero; before training, the residual correction is zero. The model begins at persistence and learns a correction. Its probe and separate composition test produce the measured validation score.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Zero initialization applies only to the output layer

<SolarDataRules mode="zero-head" />


<!--
The recorded second-round edit zeros the weights and bias of self.net[-1], the last Conv2d. Earlier convolution layers retain their normal initialization. The last layer initially returns zero, so adding its output to the current image reproduces persistence before training. Adam can then learn a correction. This explains the edit; its measured effect is still limited to the recorded comparison.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 2: sampling without replacement did not reduce error

<table class="clean-table"><tbody><tr><th>Tested source</th><th>Validation error ↓</th></tr><tr><td>Starting absolute-loss model</td><td>0.120553</td></tr><tr><td>A · zero-initialize the residual head</td><td>0.110916</td></tr><tr><td>B · sample without replacement</td><td>0.120557</td></tr></tbody></table><p>The composition selected A. It did not combine the unhelpful sampling change.</p><div class="bottom-note">Keep the tested sampling result alongside the selected version for comparison.</div>


<!--
Candidate B changes the batch sampling to seeded permutations. Its validation error is essentially the same as the parent and slightly higher. The composition keeps zero initialization and rejects the sampling change. Do not attribute a benefit to an untested combination.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Open the recorded research conversation

<p class="big"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7">Open the proposal and its recorded tool activity ↗</a></p><p>Find the active configuration, the requested edit, and the returned candidate code. Compare the proposal with the tested source.</p><p class="aside"><a href="https://ash0ts.github.io/forge-workshop-kit/solar/recorded-study.json">Download the recorded source, decisions, scores, and evidence links ↗</a></p><div class="bottom-note">Agent Lens may require sign-in. The source and saved decisions are also in the downloadable evidence.</div>


<!--
Open the proposal conversation and follow the evidence-reading tool to the candidate source. The downloadable records contain the same decisions and scores if the native view requires sign-in.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">REFERENCE</div>

# When a service is unavailable

<table class="clean-table"><tbody><tr><th>Failure</th><th>Next action</th></tr><tr><td>Project authentication or permission</td><td>Fix access, then retry the check</td></tr><tr><td>Training or inference failed</td><td>Inspect the saved error before retrying work</td></tr><tr><td>Trace or artifact upload failed</td><td>Retry export of the saved execution</td></tr><tr><td>Native EvalTables HTTP 500</td><td>Use notebook and Weave comparisons; retry publication</td></tr></tbody></table>


<!--
Start with the failed operation. An authentication problem needs corrected access. A failed training run needs its saved error inspected. An upload failure needs a publication retry. Native EvalTables returned HTTP 500 during this rehearsal; the notebook and Weave comparisons are still available.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">REFERENCE</div>

# Four-hour session

<table class="clean-table schedule"><tbody><tr><th>Minutes</th><th>Work</th></tr><tr><td>0–15</td><td>Copy, connect, instrument</td></tr><tr><td>15–40</td><td>Data and persistence</td></tr><tr><td>40–90</td><td>Tracking and six configurations</td></tr><tr><td>90–100</td><td>Break</td></tr><tr><td>100–135</td><td>Image predictors</td></tr><tr><td>135–195</td><td>Evidence and two research rounds</td></tr><tr><td>195–240</td><td>Freeze, compare, reproduce, explain</td></tr></tbody></table>


<!--
Use these times to pace the room. They include coding and discussion, not just execution. If a section takes longer, use its recorded example for discussion rather than claiming a learner’s unexecuted code produced that result.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">REFERENCE</div>

# Keep working in your own project

<p class="big"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Copy the Solar notebook ↗</a></p><p><a href="https://github.com/ash0ts/forge-workshop-kit">Source, setup, dataset, and facilitator guide ↗</a></p><p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Recorded rehearsal Report ↗</a></p><p class="aside"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view">For an office-agent example, open Pending, Inc. ↗</a></p><div class="bottom-note">Keep your notebook, code edits, and checkpoints. The facilitator needs no control over your runtime.</div>


<!--
Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.
Source notes and recorded evidence: notes/sources.md.
-->
