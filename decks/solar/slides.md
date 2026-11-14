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

<div class="kicker">0:00–0:25</div>

# Solar forecasting<br>with agent-assisted<br>experiments

<div class="sub">Use satellite observations to compare forecasting models and test agent-written code changes.</div><LabScene /><div class="bottom-note">A six-hour Python workshop using real archived observations.</div>


<!--
You are joining a fictional research lab preparing for its weekly forecast review. We will use real February 2014 satellite observations to predict X-ray flux thirty minutes ahead and solar images one hour ahead. First we will compare small trained models with copying the latest observation. Then we will ask an agent to edit the image experiment’s code and test those changes with the same comparison. This is a CPU teaching experiment, not an operational solar forecast. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: arrival
---

<div class="kicker">0:00–0:25</div>

# The lab needs a forecast for its weekly review

<div class="lab-assignment"><div class="lab-dialogue"><div class="scene-label">Fictional lab · the principal investigator</div><p>“Does the model predict anything better than assuming the Sun stays as it is?”</p></div><div class="lab-task"><h2>Your assignment</h2><p>Use observations from February 1–14, 2014 to test that question. Bring a forecast, its errors, and the code a colleague needs to repeat it.</p><p class="aside">The lab is fictional. The satellite observations are real.</p></div></div>


<!--
The principal investigator, or PI, runs the weekly research meeting. You are the researcher preparing a comparison for that meeting. The question is deliberately concrete: does a trained model predict the next observation better than simply copying the current one? We have two weeks of archived data, so we can hide later observations, make predictions, and then compare them with what was actually recorded. We are practicing an experiment design; these short runs cannot establish reliable solar forecasting. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: assignment
---

<div class="kicker">0:00–0:25</div>

# What the satellites recorded

<div class="opening-observations"><div class="scientific-figure"><img class="solar-photo" src="/images/v030-observations.png" alt="A GOES-15 XRS-B time series and an AIA 171 Å solar image from February 1, 2014"><div class="image-caption">Actual archive observations. NOAA GOES-15 and NASA/SDO AIA; false-color image.</div></div><div class="observation-tasks"><p><strong>GOES-15:</strong> two whole-Sun X-ray readings each minute, measured in watts per square metre.</p><p><strong>AIA 171 Å:</strong> an extreme-ultraviolet view of the Sun’s outer atmosphere, reduced to 64 × 64 pixels.</p></div></div>


<!--
GOES gives us two numerical measurements each minute: XRS-A and XRS-B measure X-ray power per square metre in different wavelength bands. The plot shows XRS-B, transformed with log10 because its values span a wide range. AIA is a different instrument on NASA’s Solar Dynamics Observatory. Its 171-angstrom images show extreme-ultraviolet emission from the Sun’s outer atmosphere. The colors represent intensity, not visible light or a direct temperature measurement. Our teaching arrays reduce the images to sixty-four by sixty-four pixels. SunPy retrieves and reads the observations and metadata; our preprocessing code builds the training arrays. These are separate forecasting tasks, not two inputs to one model. Sources: https://www.spaceweather.gov/products/goes-x-ray-flux and https://sdo.gsfc.nasa.gov/data/channels.php. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: path
---

<div class="kicker">0:00–0:25</div>

# What one forecast example contains

<ForecastExample /><div class="bottom-note">Persistence predicts no change. A trained model must beat it on the same future observations.</div>


<!--
Both examples shown here exist in the prepared training data. Set the clock to 01:00 UTC on February 1. For GOES, the model can read sixty one-minute samples in each channel, from 00:01 through 01:00, and must predict XRS-B at 01:30. Persistence uses only the current XRS-B reading as that forecast. For AIA, the model sees images from 00:00 and 01:00 and predicts the image at 02:00; persistence copies the 01:00 image. The future observations are targets for scoring, never inputs to the prediction. We compare absolute error in log-flux units for GOES and mean absolute error in normalized image intensity inside the solar disk for AIA. The scores stay separate. If little changes over the horizon, copying the latest observation can be hard to beat. We will measure that rather than assume the trained model wins. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: research-question
---

<div class="kicker">0:00–0:25</div>

# Bring a comparison your colleagues can repeat

<div class="lab-files"><div class="lab-folder"><div class="scene-label">Fictional lab shared folder</div><code>forecast_final.py</code><code>forecast_final_v2.py</code><code>forecast_final_final.py</code><code>forecast_final_USE_THIS.py</code><p>Last week’s score came from one of these.</p></div><div><h2>Show the comparison.</h2><p>Predictions and errors on the same dates, including persistence and the cases the model got wrong.</p><h2>Save what produced it.</h2><p>Data version, source, settings, trained weights, and outputs, together in one run.</p></div></div><div class="bottom-note">Later, an agent will edit the image-model code. We’ll test its changes using this same comparison.</div>


<!--
At the review, a lower error is useful only if we know what produced it and what it was compared with. The four final files are our fictional lab’s previous filing system. We will use Forge and W&B to connect the code, configuration, data, weights, and predictions to each run. The measurement task teaches that stack with a scalar output; the image task reuses it for predictions we can inspect pixel by pixel. Only then do we add an AI research assistant. It will read the image code and validation results and propose edits to the model or training procedure. It will not alter the data, target, or final scoring rules. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: copy
---

<div class="kicker">0:00–0:25</div>

# Copy the notebook into your Forge project

<div class="copy-layout"><div class="template-qr"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view"><img src="/images/solar-template-qr.svg" alt="QR code opening the Solar workshop template"></a><p><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Open the Solar template ↗</a></p></div><ol><li>Open the template.</li><li>Choose <strong>Copy to project</strong> and select your writable project.</li><li>Open the copy in <strong>Edit</strong>. Choose <strong>Run all stale cells</strong> once.</li><li>In <strong>Connect</strong>, check your project. Exercise run buttons stay unpressed.</li></ol></div><div class="bottom-note">Hosted Forge supplies authentication. Your account supplies notebook compute and inference access.</div>


<!--
Allow participants to get their own copy open before continuing. Run all stale cells creates the controls; it does not press the exercise run buttons. Hosted Forge supplies authentication, but attendees still need their own project and account access. Use fictional or public teaching data in a public project. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: setup-screen
---

<div class="kicker">0:00–0:25</div>

# Copy the notebook into the project you will use

<div class="copy-native"><a class="copy-dialog" href="/images/visual-v030-solar-setup.png" target="_blank"><img src="/images/visual-v030-solar-setup.png" alt="Native Forge Copy to project dialog"></a><div><h2>Choose your destination.</h2><p>Select a project you can write to. Open the copy in Edit.</p><h2>Check it in the notebook.</h2><p>Hosted Forge detects the copied notebook’s project. Laptop users enter it in Connect.</p><p class="aside">After copying, check the project name in Connect. Your runs and traces should land there.</p></div></div>


<!--
Show the native copy dialog. The copied notebook uses its destination project. A laptop uses manual entry. Confirm the project before executing. The browser preview limitation remains separate from notebook execution. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: local
---

<div class="kicker">0:00–0:25</div>

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
Hosted participants can skip this slide. On a laptop, install Git and uv, clone the repository, and run these commands. Authenticate in the terminal and keep that terminal open while marimo runs. There is no extra workshop service to start. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: settings
---

<div class="kicker">0:00–0:25</div>

# Check the compute and inference settings

<table class="clean-table"><tbody><tr><th>Setting</th><th>This workshop</th></tr><tr><td>Project and credentials</td><td>Your own Forge project and account</td></tr><tr><td>Training compute</td><td>Notebook CPU; billed separately if hosted</td></tr><tr><td>Research agent</td><td><code>zai-org/GLM-5.3-Flash</code>, fixed</td></tr><tr><td>Inference allowance</td><td>$8 by default; adjustable in Connect</td></tr><tr><td>Execution</td><td>Explicit run buttons; saved work restores</td></tr></tbody></table><div class="bottom-note">A higher allowance permits more calls. It does not grant account access or include compute.</div>


<!--
Check these settings before running anything. The eight-dollar allowance applies to inference, while hosted notebook compute is separate. The research agent uses GLM-5.3-Flash with temperature 0.2, JSON output, and up to 16,384 output tokens. If that model is unavailable, stop and inspect the error rather than changing models mid-comparison. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: trace-scopes
---

<div class="kicker">0:00–0:25</div>

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
Conversation identifies the execution. Turn holds the mission. Tool records one operation. The attribute line is the learner edit, not a second call. Actual instrumentation also supplies start and end timestamps and records exceptions. Run the free check, send the setup trace, then find the same field in Agent Lens. Advance the code highlights one step at a time; use Back to revisit the previous statement. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: setup-turn
---

<div class="kicker">0:00–0:25 · YOUR TURN</div>

<a class="answer-link" href="/109">Worked answer → 109</a>

# Connect and inspect your first tool call

<div class="task">Open <strong>1 · Connect</strong>.</div><ol class="exercise-controls"><li>Click <strong>Connect and restore my work</strong>. Check that the project is yours.</li><li>In <code>instrument_tool</code>, add the <code>workshop.exercise</code> attribute with value <code>solar-research</code>. Click <strong>Check my tracing code</strong>.</li><li>Click <strong>Send my first Agent Lens trace</strong>. Open the tool call in Agent Lens and find the attribute you added.</li></ol><div class="done">Check your work: Find your attribute beside the tool’s arguments and result.</div>


<!--
Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: instrumentation-screen
---

<div class="kicker">0:00–0:25</div>

# Find the field your code added to the span

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-trace" href="/images/visual-v030-solar-trace.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-trace.png" alt="Native Agent Lens setup tool span from the current Solar rehearsal"><span v-click="1" class="capture-mark" style="left:430px;top:195px;width:676px;height:74px" aria-label="Annotation 1: Tool arguments"><b>1</b></span><span v-click="2" class="capture-mark" style="left:430px;top:278px;width:676px;height:115px" aria-label="Annotation 2: Returned observation"><b>2</b></span></a><div class="product-caption"><span>Read the returned NumPy version. Open Raw to find workshop.exercise.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/4ca0a7e5c9d1fe30d24079ea5b98b750">Open the setup trace ↗</a></div><div class="image-caption">Recorded v0.3.0 environment check. No language-model call was needed.</div></div>


<!--
The exercise is complete when the participant can find their own attribute in their own tool span. Here is the recorded reference. The tool arguments, result, and duration describe one actual operation. The same instrumentation function records later training calls. Session block: Connect and trace an operation (minutes 0–25).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: goes-window
---

<div class="kicker">0:25–1:05</div>

# Predict X-ray flux 30 minutes ahead

<SolarConcept mode="window" :reveal="Math.min($clicks + 1, 3)" />


<!--
Set the clock to 01:00 UTC on February 1. Reveal the 01:30 target, then persistence. All numerical values are from the immutable teaching dataset, extracted without training. Ask which number a forecasting program is allowed to use at 01:00. The answer is the observation, not the later target. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: goes-actual-window
---

<div class="kicker">0:25–1:05</div>

# Read the arrays for that same forecast

```python {1-2|3|4-5|all}
example = splits["train"]
i = 1  # Forecast origin: 2014-02-01T01:00 UTC
x = example["x"][i]          # shape (2, 60)
y = example["y"][i]          # shape (1,)
latest = example["persistence"][i]  # shape (1,)
```

<div class="bottom-note">The dictionary keeps the inputs, target, timestamp and persistence forecast aligned.</div>


<!--
A NumPy array stores numbers with named positions, not timestamp metadata in every entry. The shared index identifies the same forecast across x, y, ids and persistence. Channel zero is XRSA; channel one is XRSB. The final axis runs from the oldest to the latest minute. The persistence array preserves log-flux units before input standardization. This is a read-only excerpt; use the notebook window selector to inspect it. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: chronology
---

<div class="kicker">0:25–1:05</div>

# Use different dates to fit, choose, and evaluate

<ForecastWindow :split="true" /><div class="bottom-note">February 2014, UTC. Each example’s inputs and target stay inside one date partition.</div>


<!--
These dates serve three different research decisions. February 1–10 trains the model weights and supplies the normalization statistics. February 11–12 lets us compare architectures, settings, and later the agent’s code changes. We will look at those validation errors repeatedly, so they cannot also be our final test. February 13–14 stays reserved until we freeze the selected code and weights. Then we evaluate without training again. A window whose history or target crosses a boundary is excluded. The reserved dates give us an honest comparison for this short period, not evidence of reliable forecasting in other months. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: window-validity
---

<div class="kicker">0:25–1:05</div>

# Keep the whole example inside one date split

<SolarConcept mode="validity" :reveal="Math.min($clicks + 1, 3)" />


<!--
Reveal one invalid cross-boundary window and then one gap. load_goes checks every one-minute interval from the first history sample through the target, including the forecast horizon. It rejects windows crossing a date partition. Randomly shuffling overlapping windows across train and test would let nearly identical histories occur on both sides. The workshop uses chronological partitions, but adjacent accepted windows still overlap within a partition. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: goes-normalization
---

<div class="kicker">0:25–1:05</div>

# Normalize the inputs without changing the target units

<SolarComputation mode="normalization" :reveal="Math.min($clicks + 1, 4)" /><div class="bottom-note">Notebook: choose a window, then toggle standardized inputs. The target does not change.</div>


<!--
load_goes first takes log10 of both flux channels. It fits one mean and standard deviation per channel using training inputs only, then reuses those values for validation and final inputs. The target remains unstandardized log10 XRS-B. That is why persistence returns split["persistence"] rather than copying a standardized tensor entry. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: normalization-values
---

<div class="kicker">0:25–1:05</div>

# Calculate the value the model receives

```python {1|2|3|all}
log_flux = np.log10(raw_flux)
model_input = (log_flux - training_mean) / training_std
# Target and persistence remain in log10 XRS-B units.
```

<table class="clean-table teaching-values"><tbody><tr><th>01:00 XRS-B observation</th><th>Value</th></tr><tr><td>Raw flux</td><td>2.92329e-06 W/m²</td></tr><tr><td>log10 flux</td><td>-5.534128</td></tr><tr><td>Training mean / standard deviation</td><td>-5.469873 / 0.275522</td></tr><tr><td>Standardized input</td><td>-0.233211</td></tr></tbody></table>


<!--
These numbers come from the same 01:00 window. Subtract the XRS-B training mean and divide by the training standard deviation to obtain minus 0.233211. The different number is a change of units, not a different observation. Both channels get their own training-derived statistics. Learners should reproduce the value using the notebook table and its normalization checkbox. The baseline must return minus 5.534128, not minus 0.233211. Rounded displayed values may differ in their last digit from full-precision calculations. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: sunpy
---

<div class="kicker">0:25–1:05</div>

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
Open the representative FITS file and inspect its date, wavelength, and unit. Training uses prepared arrays so the class does not wait for archive downloads. The dataset includes the acquisition and preprocessing records, so we can trace those arrays back to the public observations. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: data-turn
---

<div class="kicker">0:25–1:05 · YOUR TURN</div>

# Inspect the observations before training

<div class="task">Open <strong>2 · Solar data</strong>.</div><ol class="exercise-controls"><li>Click <strong>Load the solar dataset</strong>.</li><li>In the data preview, find an observation time, the image wavelength, and the train/validation/test dates.</li><li>Use the date diagram to explain why a window with inputs on February 10 and a target on February 11 would be excluded.</li></ol><div class="done">Check your work: You can say what the model receives and which future observation it must predict.</div>


<!--
Give participants six minutes. Have them explain one forecast window to a neighbor: which observations go in, which observation is the target, and which dates it belongs to. No training is needed yet. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: persistence
---

<div class="kicker">0:25–1:05</div>

# Start by copying the latest reading

```python
def persistence_forecast(split):
    # Latest observed value becomes the future prediction.
    ...
```

<p class="big">Predict flux 30 minutes ahead by copying the latest reading.</p><div class="bottom-note">This uses only a reading we already have. It does not look at the future target.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> The latest observed reading in each window</span><span><strong>Output:</strong> One 30-minute-ahead prediction per window</span></div>


<!--
Persistence means predicting that the latest value will stay the same. Solar observations are correlated over time, so this simple baseline can be hard to beat. At the lab review, someone will ask why we needed a neural network if copying the last reading worked. We should run that comparison before they ask. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: metric
---

<div class="kicker">0:25–1:05</div>

# Measure how far the prediction missed

<SolarComputation mode="error" />


<!--
For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: actual-baseline-error
---

<div class="kicker">0:25–1:05</div>

# Score the forecast we just made

<div class="teaching-equation"><p>At 01:00, predict <strong>-5.534128</strong>.</p><p>At 01:30, the observed target is <strong>-4.940862</strong>.</p><p class="mono">|prediction − target| = 0.593266</p></div><div class="bottom-note">One window’s absolute error, in log10 flux units. The reported MAE averages all accepted windows.</div>


<!--
This particular forecast misses a rise in flux. Persistence can work well on slowly changing periods and miss rapid changes. Do not infer the mean from this one example. The existing arithmetic slide shows how individual errors are averaged. A log10 error of about 0.59 corresponds to a ratio near four, not a 59 percent error. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: persistence-turn
---

<div class="kicker">0:25–1:05 · YOUR TURN</div>

<a class="answer-link" href="/110">Worked answer → 110</a>

# Write and test persistence

<div class="task">Open <strong>3 · Persistence</strong>.</div><ol class="exercise-controls"><li>Implement <code>persistence_forecast(split)</code>.</li><li>Click <strong>Check my persistence function</strong>, then <strong>Run my persistence baseline</strong>.</li><li>Inspect the observed and predicted curves. Identify one interval where copying the present misses the future.</li></ol><div class="done">Check your work: The plot shows your persistence forecast beside the observed flux. Point to one miss.</div>


<!--
Allow ten minutes. Let participants attempt the function before opening the answer. Ask them to find an interval where the real flux changed while persistence kept the previous value. That is a concrete error another model could try to reduce. Session block: Read observations and implement persistence (minutes 25–65).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: number
---

<div class="kicker">1:05–1:35</div>

# Save what changed between runs

<p class="big">Suppose a second run has a lower validation error. What changed?</p><div class="step-path"><div><h2>Code</h2><p>You changed the loss function.</p></div><div><h2>Data</h2><p>You excluded an incomplete window.</p></div><div><h2>Settings</h2><p>You trained for more steps.</p></div></div><div class="bottom-note">Save these differences so someone else can repeat the comparison.</div>


<!--
A colleague at the review asks which setting changed. These are possible explanations, not claims about this rehearsal. If code, data, or training time differs, we need to know that before deciding why the score moved. Saving the active values answers the question without searching all four final notebooks. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: run-inspector
---

<div class="kicker">1:05–1:35</div>

# Which setting changed between these runs?

<RunInspector />


<!--
These are two recorded GOES runs. Before revealing the settings, ask what the scores let us conclude. Then click Show active settings. Both runs used the same source and training budget; their learning rates differed. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: run-inspector-reveal
---

<div class="kicker">1:05–1:35</div>

# These runs used different learning rates

<RunInspector :revealed="true" />


<!--
The learning rate changed from .001 to .003. Data, source, seed, steps, and batch size stayed the same. Both errors were worse than persistence. We can explain the setting change at the review, but we still cannot claim to have beaten the baseline. Check the predictions before deciding what to try next. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: independent
---

<div class="kicker">1:05–1:35</div>

# Use the same scoring rule for every model

<ResearchMap :level="2" /><div class="bottom-note">The model can change. The target, partition, and primary scoring rule stay fixed.</div>


<!--
Keep the target, dates, and primary metric unchanged while comparing models. If we changed the metric after seeing a result, the lower number could describe a different task. Our candidate code can change the predictor and training procedure while this comparison rule stays fixed. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: stage
---

<div class="kicker">1:05–1:35</div>

# Save code and outputs with each training run

```python {1-3|4-5|6|all}
with session.stage(name, config=config,
    sources={"candidate.py": source},
    inputs={"dataset": dataset_version}) as stage:
    if stage.needs_run:
        result, predictions = training.train(...)
        stage.record(result, files=output_files)
```

<div class="bottom-note">Shortened from run_training. The saved files include source, weights, predictions and losses.</div>


<!--
Find the full editable run_training function in the notebook. The stage identifies a request to train specific source with specific settings and data. Its completed result is reused only for that matching request. training.train runs the program and returns predictions. stage.record stores its result and output files. Publication follows execution; an upload failure does not erase training or require training again. The ellipsis abbreviates arguments in this teaching excerpt; it is not a paste-ready function. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: training-step
---

<div class="kicker">1:05–1:35</div>

# What changes during one training step

<SolarComputation mode="training" :reveal="Math.min($clicks + 1, 4)" />


<!--
In fit, the GOES model predicts a batch and computes squared error against training targets. The shared loss function has an all-ones mask for GOES; the image exercise later uses the mask to select disk pixels. loss.backward computes gradients. Adam updates the forecasting model weights. The training targets participate in these updates. Validation inputs are predicted without gradients, and validation targets are scored by the parent process outside candidate code. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: gradient-arithmetic
---

<div class="kicker">1:05–1:35</div>

# Use the error to decide which way a weight should move

<SolarConcept mode="gradient" :reveal="Math.min($clicks + 1, 3)" />


<!--
Use a one-weight model to explain the derivative before showing PyTorch. With x equal two and target three, loss is (2w minus three) squared. At w equal one, its derivative is minus four. A simple gradient-descent step subtracts learning rate times gradient. The displayed update uses 0.1 and gives w equal 1.4. This is arithmetic, not a logged workshop result. Our real model uses Adam, which also maintains estimates of gradient moments. Do not describe this example as an exact Adam update. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: optimizer-code
---

<div class="kicker">1:05–1:35</div>

# Separate prediction, gradients and the optimizer step

```python {1-2|3|4|5|all}
prediction = model(batch_x)
loss = training_loss(prediction, batch_y, mask)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

<div class="bottom-note">A forward pass returns predictions. Only the optimizer step changes model parameters.</div>


<!--
zero_grad clears accumulated gradients; PyTorch adds new gradients unless we clear them. The forward pass creates predictions and records the operations needed for differentiation. backward computes derivatives of the loss with respect to trainable parameters. step applies the optimizer update. The workshop loops over a fixed number of optimizer steps, not a promised number of full dataset epochs. Training sample order and initialization depend on the seed. Learners edit training_loss; they can inspect the surrounding fit function. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: validation-code
---

<div class="kicker">1:05–1:35</div>

# Validation measures the current weights without fitting them

```python {1|2-3|4|all}
model.eval()
with torch.no_grad():
    prediction = model(validation_x)
error = fixed_score(prediction, validation_y)
```

<div class="bottom-note">eval() changes layer behavior; no_grad() stops gradient recording. Neither call selects a model.</div>


<!--
eval disables training-specific behavior such as dropout if a candidate uses it. no_grad prevents autograd from retaining a differentiation graph. Our current small models do not need dropout to illustrate the distinction. The fixed parent scorer compares predictions to validation targets. Participants choose a configuration using validation; the optimizer itself never updates from these validation targets in this workshop. This is an explanatory excerpt of the scoring boundary, not the exact function signature. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: artifacts
---

<div class="kicker">1:05–1:35</div>

# Restore a completed run after a restart

<SolarComputation mode="checkpoint" />


<!--
The local completion record tells the notebook which work finished. The checkpoint Artifact stores a copy in your project. If the runtime is replaced, restore the checkpoint before continuing. An upload failure can be retried using the local files. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: tracking-turn
---

<div class="kicker">1:05–1:35 · YOUR TURN</div>

<a class="answer-link" href="/111">Worked answer → 111</a>

# Write the loss and metric

<div class="task">Open <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Implement <code>training_loss</code> and <code>my_flux_mae</code>.</li><li>Click <strong>Check my measurement code</strong>. Test identical arrays and a constant one-unit error.</li><li>In <code>run_training</code>, find where it saves source, settings, weights, and predictions. The next exercise will produce those files.</li></ol><div class="done">Check your work: Your checks pass, and you can point to where run_training saves its files.</div>


<!--
Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example. Session block: Explain loss and save a training run (minutes 65–95).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: break-one
---

<div class="kicker">1:35–1:50</div>

# Take a fifteen-minute break

<p>Your draft loss and metric should be saved. Check that completed results remain visible after navigating away and back.</p><p>After the break, we’ll follow a batch through the two forecasting models.</p>


<!--
Use minutes 95 through 110. Do not start a new training run during the break. A pending publication can be retried from saved results later. Session block: Break (minutes 95–110).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: search-levels
---

<div class="kicker">1:50–2:35</div>

# Changing settings, choosing models, and editing code

<SolarMechanism mode="search" />


<!--
There are three different operations here. Hyperparameter search supplies different values to the same implementation, such as learning rate or width. Architecture comparison chooses between implementations we already wrote, such as an MLP and a temporal CNN. Later, the research agent will write a code change that our current configuration options cannot express, such as replacing squared training loss with absolute loss. We’ll test that changed program with the same dates and scoring rule. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: batch-shapes
---

<div class="kicker">1:50–2:35</div>

# Read the batch, channel and time axes

<SolarConcept mode="batch" :reveal="Math.min($clicks + 1, 3)" />


<!--
B counts windows processed together. Each window has two instrument channels and sixty time positions. The target has one value per window. The training configuration uses batch size thirty-two. The notebook free shape demonstration uses batch size two and width four so learners can inspect a small forward pass; it does not train and does not change later random state. Ask learners to explain x[0,1,-1] before revealing the output shape. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: batch-indexing
---

<div class="kicker">1:50–2:35</div>

# Index one value, then keep the batch shape

```python {1|2|3|4|all}
x.shape             # (B, 2, 60)
x[0, 1, -1]         # latest XRS-B input in window 0
x[:, 1, -1:]        # latest XRS-B input, shape (B, 1)
model(x).shape      # (B, 1)
```

<div class="bottom-note">The values in x are standardized. This indexing exercise does not define a persistence forecast.</div>


<!--
Explain colon as selecting every item and negative one as the final position. Using -1 removes the last axis; -1: preserves it as length one. Shape-compatible subtraction matters: (B,1) minus (B,) can broadcast to a B by B matrix and silently score the wrong pairs. Both predictions and targets should remain B by one. Ask experienced participants to demonstrate that broadcasting issue with a small local NumPy array; no training is needed. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: goes-mlp
---

<div class="kicker">1:50–2:35</div>

# How the MLP uses an hour of measurements

<SolarComputation mode="mlp" :reveal="Math.min($clicks + 1, 4)" /><div class="bottom-note">Notebook: Run one forward pass and show tensor shapes. This does not train weights.</div>


<!--
The actual candidate code flattens a two-by-sixty input into one hundred twenty values. A linear layer learns weights for every input position, followed by ReLU and a linear scalar output. Width is sixteen or thirty-two in the search. The diagram omits the batch dimension and draws a few hidden units to represent the layer. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: one-neuron
---

<div class="kicker">1:50–2:35</div>

# Calculate one hidden unit before adding the whole layer

<SolarConcept mode="neuron" :reveal="Math.min($clicks + 1, 3)" />


<!--
The arithmetic uses three values for legibility. The real MLP flattens 120 values. A Linear layer gives every hidden unit one learned weight per input plus a bias. ReLU retains positive values and sets negative values to zero. A second Linear layer combines hidden outputs into one forecast. With no nonlinear activation between linear layers, their composition would still be one affine transformation. The example illustrates the operation; it is not a neuron from a trained checkpoint. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: goes-cnn
---

<div class="kicker">1:50–2:35</div>

# How the temporal CNN uses the same measurements

<SolarComputation mode="cnn" :reveal="Math.min($clicks + 1, 4)" /><div class="bottom-note">Choose Temporal CNN in the same check. Compare its output shapes with the MLP.</div>


<!--
The same two-by-sixty input now passes through a five-sample convolution with padding two. Filter weights are reused along time. The output has width channels and sixty positions; AdaptiveAvgPool1d(1) averages over time, then the linear layer predicts one value. This compares two implemented computations, not just two model names. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: convolution-weights
---

<div class="kicker">1:50–2:35</div>

# Reuse one filter at each time position

<SolarConcept mode="filter" :reveal="Math.min($clicks + 1, 3)" />


<!--
One Conv1d output channel uses a five-position filter for each of the two input channels, sums ten products and adds its bias. Slide the highlighted window once while retaining the same weights. Multiple output channels learn different filters. Padding two preserves the time dimension at sixty. Average pooling then discards the time-position axis. That is a modeling assumption, not merely a shape trick: the network summarizes local features across the hour. The MLP gives distinct weights to each time position. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: parameter-code
---

<div class="kicker">1:50–2:35</div>

# Choose settings separately from the weights being learned

```python {1-2|3|4-5|all}
config = {"architecture": "cnn", "width": 16,
          "learning_rate": 0.001, "steps": 60, "seed": 17}
model = build_model((2, 60), config)
optimizer = torch.optim.Adam(model.parameters(),
                             lr=config["learning_rate"])
```

<div class="bottom-note">Width and learning rate are settings. The weights and biases inside model.parameters() are trained.</div>


<!--
The six Sweep configurations are predefined; the required exercise is a bounded comparison, not an adaptive search algorithm. Architecture chooses an existing implementation. Width changes its number of hidden features. Learning rate scales updates. Steps fixes the update budget. Seed controls initialization and sampling. None of these is itself a learned model weight. All comparisons must record the settings because a favorable score does not tell us which choices produced it. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: configs
---

<div class="kicker">1:50–2:35</div>

# Compare six model configurations

<table class="clean-table"><tbody><tr><th>Architecture</th><th>Widths</th><th>Learning rates</th><th>Training budget</th></tr><tr><td>Small MLP</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr><tr><td>Temporal CNN</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr></tbody></table><div class="bottom-note">Seed 17. Batch size 32. The notebook records the active values.</div>


<!--
The MLP reads the history as a fixed set of inputs. The temporal CNN applies shared filters along time. We’ll try three settings for each: widths sixteen and thirty-two, and learning rates .001 and .003. Every run gets seed seventeen, batch size thirty-two, and sixty training steps. That small budget keeps the exercise short; it does not establish which architecture would win after longer training. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: sweep
---

<div class="kicker">1:50–2:35</div>

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
The Sweep assigns a trial configuration, and wandb.init creates its tracked run. run_training fits the model, saves its files, and returns metrics; run.log adds those metrics to the run. wandb.agent repeats this for the six configurations. The notebook includes the full entity, project, and configuration setup shown in this shortened excerpt. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: native-sweep
---

<div class="kicker">1:50–2:35</div>

# Compare the six configurations in Forge

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-sweep" href="/images/visual-v030-solar-sweep.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-sweep.png" alt="Native six-run W&amp;B Sweep from the v0.3.0 Solar rehearsal"></a><div class="product-caption"><span>Find two MLP runs with the same width and different learning rates.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pzigourv">Open the Sweep ↗</a></div><div class="image-caption">All six validation forecasts were worse than persistence. A smaller error among them is still a failed baseline comparison.</div></div>


<!--
Use the latest rehearsal Sweep pzigourv. Start with two width-16 MLP runs, then compare their learning rates, error, and runtime. All six models lost to persistence. Do not infer an architecture conclusion from this short training exercise. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: learning-curve
---

<div class="kicker">1:50–2:35</div>

# Check whether the model has finished learning

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-loss.png" alt="Saved GOES model loss curve over 60 training steps"><div class="image-caption">Selected MLP: width 16, learning rate .003, seed 17. Saved v0.3.0 training losses.</div></div><div class="bottom-note">Historical 60-step run. A later worked repair tests scaling, residual prediction, and a longer budget together.</div>


<!--
The selected GOES model’s loss was still falling after sixty steps. That suggests testing a longer training budget, but it does not tell us that more steps would beat persistence. Look at the predictions and validation score alongside the curve. The later qualification tested a complete repaired recipe. It does not isolate the effect of additional training alone. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: search-turn
---

<div class="kicker">1:50–2:35 · YOUR TURN</div>

<a class="answer-link" href="/112">Worked answer → 112</a>

# Run six configurations and inspect one forecast

<div class="task">Stay in <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Click <strong>Run six tracked configurations</strong>.</li><li>Open the Sweep. Compare validation error and training time for two configurations.</li><li>In the notebook, choose <strong>Inspect a saved measurement run</strong>. Compare its loss, forecast, and persistence. Follow its Forge links to the saved source.</li></ol><div class="done">Check your work: Explain one comparison using the settings, curve, and forecast.</div>


<!--
Allow fifteen minutes. Ask participants to predict which configuration will win before running the search. After it finishes, have them explain one result from the loss curve and forecast. Keep failed runs visible so the comparison accounts for what happened. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: goes-repair-code
---

<div class="kicker">1:50–2:35</div>

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
The latest XRS-B input is standardized. Add a learned correction, then convert it back with the same training-fitted center and scale. A zero-initialized final layer begins exactly at persistence. The fit function divides the prediction and target error by the same scale. We changed several parts of the recipe together, so the measured result cannot tell us which individual change caused the gain. Ask participants to point to the addition and unit conversion in their editable code. Advance the code highlights one step at a time; use Back to revisit the previous statement. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: goes-repair-turn
---

<div class="kicker">1:50–2:35 · YOUR TURN</div>

# Test the worked measurement repair

<div class="task">Stay in <strong>4 · Track and search</strong>, below the saved forecasts.</div><ol class="exercise-controls"><li>Read <code>forward</code> and <code>fit</code> in <strong>Worked GOES repair: inspect or edit the forecasting code</strong>.</li><li>Click <strong>Check the GOES repair code</strong>, then <strong>Train the worked GOES repair</strong>.</li><li>Compare validation error with persistence and your search. Open its training call and weights Artifact.</li></ol><div class="done">Check your work: Explain the initial forecast, the output units, and whether your validation error fell.</div>


<!--
Use the last five minutes of the measurement exercise. This is one CPU run, not another paid agent request. Its exact source, configuration, and weights are saved separately. The recipe beat persistence on three predeclared seeds in qualification, but a learner edit is a new experiment. Final selection considers its validation score; do not choose using final dates. Session block: Inspect model shapes and compare configurations (minutes 110–155).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: images-window
---

<div class="kicker">2:35–3:20</div>

# Predict the solar image one hour ahead

<ForecastWindow mode="images" /><div class="bottom-note">AIA 171 Å. Prepared 64 × 64 arrays. One-hour forecasting.</div>


<!--
Now we give the model images from sixty minutes ago and now, and ask for the image sixty minutes ahead. The AIA 171 Å arrays are 64 by 64 pixels so the exercise can run on CPU. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: persistence-image
---

<div class="kicker">2:35–3:20</div>

# See exactly which images become input and target

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-image-window.png" alt="Earlier and current AIA observations beside the future target"><div class="image-caption">First accepted training window. All three images share the same intensity scale.</div></div><div class="bottom-note">The target is hidden from the model during prediction. It is used afterward to measure the miss.</div>


<!--
Read the observation times. Channel zero is the earlier image; channel one is the current image. The third image is the future target. These are three real observations from a training window, not three outputs of an AI image generator. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: image-units
---

<div class="kicker">2:35–3:20</div>

# Put image inputs and targets in the same units

```python {1|2|3|all}
logged = np.log1p(pixel_rate)
normalized = (logged - training_center) / training_scale
# Apply the same transform to inputs and future targets.
```

<p>AIA arrays use exposure-normalized intensity. The loader fits its center and scale using training pixels inside the disk.</p><div class="bottom-note">GOES targets stayed in log-flux units. Image targets are standardized along with image inputs.</div>


<!--
This difference deserves explicit attention. The prepared AIA images are exposure-normalized rates. log1p reduces the dynamic range while accepting zero. The loader computes center and scale over on-disk training pixels, then uses the same transform for all frames and targets. Negative normalized values are possible; they do not mean negative observed light. Display colors encode intensity and are not the three input channels of an RGB model. The model receives two grayscale frames as channels. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: image-batch
---

<div class="kicker">2:35–3:20</div>

# Keep the two image times in separate channels

<SolarConcept mode="image" :reveal="Math.min($clicks + 1, 3)" />


<!--
Use the same earlier and current observations already displayed. The input is B by two by sixty-four by sixty-four. The output is B by one by sixty-four by sixty-four. x[:,1:2] selects the current image while retaining the channel dimension. x[:,1] would drop it and can broadcast incorrectly. The image diagram is a shape illustration; the preceding slide supplies actual solar observations. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: conv
---

<div class="kicker">2:35–3:20</div>

# Predicting the future image with a small CNN

<SolarMechanism mode="residual" :reveal="1" />


<!--
The two observations become two input channels. The CNN returns one channel containing its predicted future image. The batch dimension stays the same: input shape is batch by two by sixty-four by sixty-four, and output shape is batch by one by sixty-four by sixty-four. This direct predictor has to produce the whole image from its learned weights. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: residual
---

<div class="kicker">2:35–3:20</div>

# Predict a correction to the current image

<SolarMechanism mode="residual" :reveal="2" />


<!--
Much of the current image may remain similar one hour later. We can copy that image and ask the network to predict the correction. Add the network output to x[:, 1:2], the current-image channel. The slice preserves the channel dimension. If the correction is zero, the model returns persistence exactly. The local check will test that behavior. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: residual-code
---

<div class="kicker">2:35–3:20</div>

# Implement the residual predictor’s forward pass

```python {2|3|4|all}
def forward(self, x):
    correction = self.net(x)       # [batch, 1, 64, 64]
    current_image = x[:, 1:2]      # keep the channel axis
    return current_image + correction
```

<div class="code-contract"><span><strong>Input:</strong> earlier image + current image</span><span><strong>Output:</strong> one future image per example</span></div><p class="aside">Check: if <code>correction</code> is zero, the forecast equals the current image.</p>


<!--
The diagram and code describe the same addition. Ask participants why x[:, 1] would remove a dimension and why x[:, 1:2] preserves it. The notebook implementation also branches on architecture so the convolutional comparison still returns only the network output. Advance the code highlights one step at a time; use Back to revisit the previous statement. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: residual-observed
---

<div class="kicker">2:35–3:20</div>

# Inspect the correction produced by the saved model

<div class="scientific-figure"><img class="solar-photo" src="/images/v031-residual-correction.png" alt="Current AIA image plus the saved residual model correction equals its forecast"><div class="image-caption">First validation case. Current image and forecast use the same intensity scale; the middle panel shows a signed correction.</div></div>


<!--
The center image is calculated from the saved manual residual forecast minus the current input. It shows what this trained network added. It is not the physical change observed on the Sun. Zero is white in the correction view, with negative and positive values on opposite sides of the colorbar. The panels show the equation implemented by forward. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: image-score
---

<div class="kicker">2:35–3:20</div>

# Measure prediction error inside the solar disk

<SolarMechanism mode="mask" :reveal="Math.min($clicks + 1, 4)" />


<!--
This is a diagram of the scoring calculation, not a forecast. The fixed mask assigns one to disk pixels and zero outside. Multiply absolute errors by the mask, average over the selected pixels per image, then average images. A changed off-disk pixel must not affect the score. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: image-score-code
---

<div class="kicker">2:35–3:20</div>

# Check the image scorer on three known errors

```python {1|2-3|4|all}
absolute_error = np.abs(prediction - target)
per_image = (absolute_error * disk_mask).sum(axis=(1, 2, 3))
per_image /= disk_mask.sum(axis=(1, 2, 3))
return float(per_image.mean())
```

<div class="code-contract"><span><strong>Identical arrays:</strong> score 0</span><span><strong>Every disk pixel +1:</strong> score 1</span><span><strong>Only off-disk pixels +1:</strong> score 0</span></div>


<!--
Run the three local examples before training. They explain what the scorer measures. The participant writes this development scorer, and the protected primary scorer checks the comparison with the same published rule. Missing or invalid predictions are not zero error. Advance the code highlights one step at a time; use Back to revisit the previous statement. In the notebook, move the error outside the scoring mask, then click Try my image scorer on these pixels. The two public grids have different mask sizes; images still receive equal weight. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: equal-image-average
---

<div class="kicker">2:35–3:20</div>

# Give each forecast image one score

<SolarConcept mode="averaging" :reveal="Math.min($clicks + 1, 3)" />


<!--
This is the exact arithmetic of the public scorer fixture with error set to one and inside selected. The first image includes one pixel with error one. The second includes four pixels with error two, so its sum is eight but its per-image MAE is two. Average one and two to obtain 1.5. Pooling all pixels gives 1.8 and changes the weighting. In the notebook, move the error outside the mask and run Try my image scorer on these pixels; the score becomes zero. Missing predictions do not become a zero score. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: loss
---

<div class="kicker">2:35–3:20</div>

# Training loss and evaluation error have different jobs

<SolarComputation mode="loss" :reveal="Math.min($clicks + 1, 3)" />


<!--
The training loss supplies gradients for the optimizer. The evaluation metric scores the finished predictions. Our starting loss uses squared error, while the comparison uses absolute error inside the disk. A candidate can change the loss to alter how weights are learned. We keep the evaluation metric fixed so we can compare the resulting forecasts. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: image-code-screen
---

<div class="kicker">2:35–3:20</div>

# Compare forecasts for the same validation case

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-validation-predictions.png" alt="Matched convolutional and residual predictions beside the same observed future"><div class="image-caption">Recorded v0.3.0 forecasts. First accepted validation case; common intensity and error scales.</div></div><div class="bottom-note">Notebook: select one forecast timestamp. Compare persistence and both models on common scales.</div>


<!--
The same current image and observed future appear in both rows. The convolutional forecast is above, residual below. The figure uses the first accepted case, not a selected success. Colors use the same scale across both rows. A single image is an example; the validation score includes all 142 windows. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: image-turn
---

<div class="kicker">2:35–3:20 · YOUR TURN</div>

<a class="answer-link" href="/113">Worked answer → 113</a>

# Implement and compare the image predictors

<div class="task">Open <strong>5 · Solar images</strong>.</div><ol class="exercise-controls"><li>Edit <code>ImagePredictor.forward</code>, <code>training_loss</code>, and <code>my_image_mae</code>.</li><li>Click <strong>Check my image code</strong>. A +1 error should score 1; an off-disk change should score 0.</li><li>Click <strong>Compare convolutional and residual predictors</strong>. Inspect both forecasts.</li></ol><div class="done">Check your work: Show which model validation selected, then point to a region where its forecast missed.</div>


<!--
Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed. Session block: Implement image prediction and scoring (minutes 155–200).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: meal-break
---

<div class="kicker">3:20–3:50</div>

# Pause for thirty minutes before the research-agent exercise

<p>Keep the image comparison open at one timestamp. Save the draft you trained and the observation you want the agent to investigate.</p><p>After the break, we’ll give the agent the code and validation evidence behind that result.</p>


<!--
Use minutes 200 through 230 for the meal break. Completed work should already be saved. Do not ask people to leave an unreviewed paid action running during the break. Session block: Meal break (minutes 200–230).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: agent-need
---

<div class="kicker">3:50–4:20</div>

# Use the experiment to test agent-written changes

<SolarComputation mode="evidence" /><div class="bottom-note">The lab has recruited an AI research assistant. We still review and test its work.</div>


<!--
The lab now has code, saved experiments, and a comparison we can inspect. The PI suggests bringing in an AI research assistant to propose the next changes. It reads the current source, active settings, validation errors, and any failures. We still review its diffs and run them through the training and scoring functions we built. The new colleague gets no exemption from testing. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: weights
---

<div class="kicker">3:50–4:20</div>

# Which model is being trained?

<SolarMechanism mode="weights" />


<!--
The language model and the forecasting network have different roles. GLM writes Python using its fixed pretrained weights; we are not fine-tuning it. The small forecasting network trains new weights each time we test candidate Python. We send its validation results back to the language model when requesting the next edit. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: boundaries
---

<div class="kicker">3:50–4:20</div>

# Limit edits to the model and training code

<div class="two-col"><div><h2>The assistant may edit</h2><p>Model layers<br>Feature computation<br>Training loss<br>Training procedure</p></div><div><h2>The experiment keeps fixed</h2><p>Training and validation dates<br>What we predict<br>How we score predictions<br>The reserved final-test dates</p></div></div><div class="bottom-note">Candidate Python runs in this notebook’s environment after your review.</div>


<!--
The research assistant can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution, just as you would for a colleague. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: agent-context
---

<div class="kicker">3:50–4:20</div>

# Give each program only the data it needs

<SolarConcept mode="context" :reveal="Math.min($clicks + 1, 3)" />


<!--
Separate three programs. The language model receives selected source and validation evidence and proposes code. Reviewed training code receives training arrays and fits the forecasting network. The parent scorer receives validation predictions and targets. The research agent can inspect validation evidence, but final-test scores and dates stay outside its improvement request. File access is scoped by the workshop; reviewed subprocess execution is not a security sandbox. These arrows describe data flow, not a guarantee that an arbitrary untrusted program is safe. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: research-tool-result
---

<div class="kicker">3:50–4:20</div>

# Gather validation evidence before requesting a proposal

```python {1-3|4-5|6|all}
_, observed = event("read_validation_evidence",
                    {"execution": evidence["stage_id"]},
                    read_validation)
prompt = {"mission": "Propose two competing code changes...",
          "source": source, "evidence": allowed}
# validated_json sends this prompt in the model request.
```

<div class="bottom-note">Shortened from research.propose(). The notebook chooses and runs the evidence-read operation.</div>


<!--
The notebook reads the selected validation execution before asking the model for proposals. read_validation returns the saved configuration, metrics and source fingerprint; event records that operation for Agent Lens. The request is built separately from the current source and the allowed evidence dictionary. It does not send prediction arrays or images, and the model does not choose this evidence-read call. Open the recorded operation to find its config and metrics, then open the model request to inspect source and evidence. A separate reviewed training action tests each proposed program. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: evidence
---

<div class="kicker">3:50–4:20</div>

# Give the agent the inputs needed to explain a run

<div class="step-path"><div><h2>Exact source</h2><p>The files that produced the parent result.</p></div><div><h2>Active settings</h2><p>Architecture, steps, width, optimizer values.</p></div><div><h2>Validation evidence</h2><p>Loss history, validation metrics, and recorded errors.</p></div></div><div class="bottom-note">A default in source may not be the value the run used.</div>


<!--
The request contains the exact source that produced the current result, the settings used in that run, and selected validation metrics and loss history. Errors, trace links and lessons are included when the selected record contains them. Participants can inspect forecast images in the notebook; the proposal request does not send those images or prediction arrays. For example, a default learning rate in candidate.py may be overridden by the active configuration. If we sent only the default, the agent could propose a change based on a setting we never used. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: agent-span
---

<div class="kicker">3:50–4:20</div>

# Follow the agent’s work in Agent Lens

<div class="step-path"><div><h2>Open the request</h2><p>Read what we asked the agent to change.</p></div><div><h2>Inspect notebook operations</h2><p>Find the saved evidence read before the request.</p></div><div><h2>Follow the test</h2><p>Open the training call and look at its result or error.</p></div></div><div class="bottom-note">Compare the agent’s stated reason with what happened when its code ran.</div>


<!--
Open the research conversation in Agent Lens. The notebook records its evidence read, sends the proposal request, and saves the returned code. These operation spans show the notebook controller’s work; they are not tool choices made by the model. Follow the separately requested training call to its result or error. Compare that sequence with the agent’s explanation of its change. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: native-lens
---

<div class="kicker">3:50–4:20</div>

# Read the evidence that went into the proposal

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-evidence" href="/images/visual-v030-solar-evidence.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-evidence.png" alt="Native read_validation_evidence span from the current Solar proposal"><span v-click="1" class="capture-mark" style="left:70px;top:3px;width:800px;height:190px" aria-label="Annotation 1: Parent settings"><b>1</b></span><span v-click="2" class="capture-mark" style="left:70px;top:210px;width:800px;height:184px" aria-label="Annotation 2: Validation evidence"><b>2</b></span></a><div class="product-caption"><span>Find the parent configuration and validation error before reading its proposal.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7/spans">Open the proposal ↗</a></div><div class="image-caption">Recorded v0.3.0 round 1. The agent receives validation evidence, never the reserved-date score.</div></div>


<!--
Open read_validation_evidence. Find the residual architecture, forty training steps, seed seventeen, and parent validation error. Then inspect the returned proposal. This request initially exhausted its output budget and used a saved retry; that is an execution event, not a change in forecasting quality. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: evidence-turn
---

<div class="kicker">3:50–4:20 · YOUR TURN</div>

<a class="answer-link" href="/115">Worked answer → 115</a>

# Choose the evidence for the research agent

<div class="task">Open <strong>6. Test agent-written changes to the image model</strong>.</div><ol class="exercise-controls"><li>In <code>select_validation_evidence(record)</code>, keep the active settings and validation results. Click <strong>Check my evidence selection</strong>.</li><li>Read the check result. Confirm that the final-test example is rejected.</li><li>Name the validation fields your function will send to the agent. What can it learn from them?</li></ol><div class="done">Check your work: You can name the code and validation results the agent will receive.</div>


<!--
Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request. Session block: Build the research-agent request (minutes 230–260).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: propose
---

<div class="kicker">4:20–5:10</div>

# Ask for two changes to the same starting code

<ResearchBranches :level="1" /><div class="bottom-note"><a href="https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335">Harness²-inspired</a>: our probes train forecasting weights and include validation scores.</div>


<!--
Both candidates start from the same source and training configuration. We ask the agent to explain each proposed change, then review its diff. This uses the Propose–Probe–Compose structure from Harness². In our teaching adaptation, a probe trains forecasting weights and gives validation results to the editor. It differs from the paper’s task protocol. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: native-diff
---

<div class="kicker">4:20–5:10</div>

# The first proposal changes one loss operation

```python
def training_loss(prediction, target, mask):
    # Before: square each miss.
    # After: take its absolute size.
    return ((prediction - target).abs() * mask).sum() / mask.sum()
```

<div class="diff"><div class="del">− (prediction - target).square()</div><div class="add">+ (prediction - target).abs()</div></div><p class="aside">Agent’s hypothesis: training on absolute error may help the fixed absolute-error score. The probe tests that claim.</p>


<!--
This is the actual first-round Candidate A edit in v0.3.0. It changes the training objective, while the evaluation scorer remains fixed. The alternative candidate retains the original squared loss. The diff establishes the proposed change; it does not establish an improvement until both run. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: loss-change-effect
---

<div class="kicker">4:20–5:10</div>

# The loss edit changes which errors receive larger gradients

<table class="clean-table"><tbody><tr><th>Illustrative absolute error</th><th>Squared loss</th><th>Absolute loss</th></tr><tr><td>0.1</td><td>0.01</td><td>0.1</td></tr><tr><td>1.0</td><td>1.0</td><td>1.0</td></tr><tr><td>3.0</td><td>9.0</td><td>3.0</td></tr></tbody></table><div class="bottom-note">The evaluation metric stays masked absolute error. Only the training objective changes.</div>


<!--
Squared error grows quadratically, and its gradient magnitude grows with the error. Absolute error grows linearly and has constant magnitude away from zero. Matching the objective to the final metric is a plausible hypothesis, not a guarantee of better generalization. The model may trade large localized errors against smaller widespread errors. Inspect the actual validation forecasts after testing. These three arithmetic values are illustrations, not measured solar residuals. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: probe
---

<div class="kicker">4:20–5:10</div>

# Train and score each candidate

<ResearchBranches :level="2" /><div class="bottom-note">Use the same training and validation data. Keep failed runs visible.</div>


<!--
Train each candidate on the same training dates and compare its validation error. If one fails before producing a forecast, inspect the error and leave its score missing. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: compose
---

<div class="kicker">4:20–5:10</div>

# Choose or combine changes using the probe results

<ResearchBranches :level="3" /><div class="bottom-note">The agent can keep A, keep B, combine changes, or retain the starting code.</div>


<!--
After both probes, the agent receives their code and validation results. It can keep one candidate, combine changes, or retain the starting source. Two suggestions do not obligate the lab to accept two changes. Read its rationale beside the scores. The dashed lines show which results it reviewed; they do not mean both candidates were merged into the selected code. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: test-composed
---

<div class="kicker">4:20–5:10</div>

# Train the composed version before adopting it

<ResearchBranches :level="4" /><div class="bottom-note">Run the selected code on the same training and validation dates.</div>


<!--
A combined edit has not yet been measured, so it needs its own training run. Even if the agent retains an existing version, the controller tests the chosen source and records the result. This separates the decision about what to keep from the execution that confirms what ran. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 2
name: composition-versus-adoption
---

<div class="kicker">4:20–5:10</div>

# Test the recommendation before carrying it forward

<SolarConcept mode="selection" :reveal="Math.min($clicks + 1, 3)" />


<!--
The agent chooses or combines source changes after reviewing probes. That is one decision. The notebook trains that proposed source and applies the strict validation-error rule. That is another decision. Equal, worse or failed results keep the earlier version. A KEEP composition may train unchanged source again; it is an additional execution without an invented code change. The branch panel should expose the actual source and execution attached to each node. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: adoption-rule
---

<div class="kicker">4:20–5:10</div>

# Adopt the tested code only if validation error is lower

<SolarDataRules mode="adoption" />


<!--
The composition is a proposed source version. After it trains, choose_adoption compares its fixed validation_error with the parent. A strictly lower score adopts the tested version. Equal error, a higher error, or failed execution retains the parent. The decision and the execution are separate records. This rule uses no final-test score. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: native-training
---

<div class="kicker">4:20–5:10</div>

# Open the training call behind the chosen version

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-training" href="/images/visual-v030-solar-training.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-training.png" alt="Native train_and_validate tool span with actual source settings and returned metrics"><span v-click="1" class="capture-mark" style="left:14px;top:45px;width:880px;height:160px" aria-label="Annotation 1: Training settings"><b>1</b></span><span v-click="2" class="capture-mark" style="left:14px;top:245px;width:880px;height:145px" aria-label="Annotation 2: Measured output"><b>2</b></span></a><div class="product-caption"><span>Check the configuration, then find validation_error in the returned result.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289">Open the selected training call ↗</a></div><div class="image-caption">Recorded v0.3.0 round 2 composition test. “error” is forecast error here, not an exception.</div></div>


<!--
The operation trained and validated the selected source. Find the returned score and compare the run to the saved source artifact. An error metric of 0.110916 is the forecasting metric, not a tool failure. If a span actually failed, inspect its exception separately. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
name: recorded-code
---

<div class="kicker">4:20–5:10</div>

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
This is the second-round selected edit in v0.3.0. The last convolution starts at zero; before training, the residual correction is zero. The model begins at persistence and learns a correction. Its probe and separate composition test produce the measured validation score. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: zero-head
---

<div class="kicker">4:20–5:10</div>

# Zero initialization applies only to the output layer

<SolarDataRules mode="zero-head" />


<!--
The recorded second-round edit zeros the weights and bias of self.net[-1], the last Conv2d. Earlier convolution layers retain their normal initialization. The last layer initially returns zero, so adding its output to the current image reproduces persistence before training. Adam can then learn a correction. This explains the edit; its measured effect is still limited to the recorded comparison. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: zero-head-gradients
---

<div class="kicker">4:20–5:10</div>

# Zeroing the last layer still allows learning

```python {1-3|4|5|all}
features = earlier_layers(x)
correction = output_layer(features)  # starts at zero
forecast = current_image + correction
# First update: output-layer weights can change.
# Later updates: gradients also reach earlier layers.
```

<div class="bottom-note">Earlier layers retain their normal initialization. The recorded edit does not zero every parameter.</div>


<!--
At initialization the final layer weights are zero, so its output correction is zero. The output weights still receive gradients because their derivative depends on the preceding features. For the first backward pass the zero output weights block gradients to preceding layers; after the output weights move, gradients can flow farther back. This explains why a zero residual head is compatible with learning. Do not teach zero initialization of every hidden layer as an equivalent change. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: repeat
---

<div class="kicker">4:20–5:10</div>

# Use the selected code and results in round two

<ResearchBranches :level="5" /><div class="bottom-note">Use the selected code and what the first tests showed to plan the next changes.</div>


<!--
Round two begins with the code selected in round one and a saved lesson explaining what the probes showed. The agent reads both before proposing its next edits. It may now change code introduced by its previous proposal. That repeated use of the earlier result is the recursive part of this research procedure. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: round1-turn
---

<div class="kicker">4:20–5:10 · YOUR TURN</div>

# Propose and test two changes

<div class="task">Inspect <code>next_research_action</code> in <strong>6. Test agent-written changes to the image model</strong>.</div><ol class="exercise-controls"><li><strong>Propose two code changes</strong>. Read both diffs.</li><li>Confirm review of Candidate A → <strong>Test Candidate A</strong>. Confirm review of Candidate B → <strong>Test Candidate B</strong>.</li><li><strong>Record my comparison</strong>, then <strong>Request a composition</strong>.</li></ol><div class="done">Check your work: Each candidate’s proposal diff and training result are linked in Agent Lens.</div>


<!--
Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: round2-turn
---

<div class="kicker">4:20–5:10 · YOUR TURN</div>

<a class="answer-link" href="/116">Worked answer → 116</a>

# Test the selected code, then begin round two

<div class="task">Continue the same workbench.</div><ol class="exercise-controls"><li>Confirm review of composition, then <strong>Test the composition</strong>.</li><li>Click <strong>Save the adopted version and lesson</strong>. Check whether the parent was retained.</li><li>Repeat the process in round two using the previous outcome.</li></ol><div class="done">Check your work: Open the selected version from each round and explain why it was kept.</div>


<!--
Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: branch-inspect
---

<div class="kicker">4:20–5:10</div>

# Follow one proposal through the branch diagram

<ResearchBranches :level="5" :interactive="true" :recorded="true" />


<!--
Click a candidate, its test, and the selection step. Follow the source change to its validation result and explain why the agent retained or rejected it. This deck diagram explains the process. The notebook’s branch view links the participant’s own files, decisions, traces, and results. Session block: Review and test two rounds of changes (minutes 260–310).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: break-two
---

<div class="kicker">5:10–5:20</div>

# Take ten minutes before opening the final dates

<p>Finish the current action and save the selected version. Do not make another code choice from the final comparison.</p><p>We’ll load the saved weights when we return.</p>


<!--
Use minutes 310 through 320. If a run is still incomplete, keep its status visible. Use the labeled recorded case for discussion rather than assigning its outcome to the learner edit. Session block: Break (minutes 310–320).
Source notes and recorded evidence: notes/sources.md.
-->

---
clicks: 3
name: freeze
---

<div class="kicker">5:20–5:45</div>

# Keep the selected code and weights fixed for final evaluation

<SolarComputation mode="inference" :reveal="Math.min($clicks + 1, 4)" />


<!--
We have used validation dates to choose the version we will bring to the review. Save that source and its trained weights together before looking at February thirteenth and fourteenth. Final evaluation loads those weights and predicts the reserved inputs without training or selecting again. If we edit after inspecting these results, we need new reserved dates to test the next claim. Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: frozen-code
---

<div class="kicker">5:20–5:45</div>

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
Load the saved weights, switch to evaluation mode, and predict without an optimizer step. Final evaluation measures the selected trained model; it does not train another one. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: aligned
---

<div class="kicker">5:20–5:45</div>

# Match each prediction to the same observation times

<table class="clean-table"><tbody><tr><th>Case identity</th><th>Persistence</th><th>Manual</th><th>Agent-selected</th></tr><tr><td>Same input timestamps</td><td>Prediction + error</td><td>Prediction + error</td><td>Prediction + error</td></tr><tr><td>Same target timestamp</td><td>Saved output</td><td>Executed source</td><td>Executed source</td></tr></tbody></table><div class="bottom-note">Use each case ID to find the same input and target times in Weave or EvalTables.</div>


<!--
Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Click Compare in EvalTables to open the native Weave-backed Evaluation Tables Preview. Open Solar images and GOES measurements separately: their errors have different meanings. Upload retries reuse the saved arrays. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: final-turn
---

<div class="kicker">5:20–5:45 · YOUR TURN</div>

<a class="answer-link" href="/117">Worked answer → 117</a>

# Test the selected models on reserved dates

<div class="task">Open <strong>7. Evaluate the selected models on reserved dates</strong>.</div><ol class="exercise-controls"><li>Click <strong>Freeze versions and evaluate reserved dates</strong>.</li><li>Choose one timestamp. Compare each image forecast with the same observed future.</li><li>Open one result’s training record and Agent Lens call. Compare the image scores separately from the GOES scores.</li></ol><div class="done">Check your work: Explain a difference between two forecasts using their images and scores.</div>


<!--
Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-final
---

<div class="kicker">5:20–5:45</div>

# In this rehearsal, image error fell 10.15%

<div class="measured-grid"><div><div class="measured-gain">10.15%</div><p>less error than the manually selected model</p><p class="aside">Agent edits: use absolute training loss, then zero-initialize the residual head.</p></div><table class="clean-table"><tbody><tr><th>Frozen version</th><th>Masked MAE ↓</th></tr><tr><td>Persistence</td><td>0.125762</td></tr><tr><td>Manual residual model</td><td>0.122442</td></tr><tr><td>Agent-selected code</td><td>0.110011</td></tr></tbody></table></div><p class="aside">Actual AIA 171 Å observations. 199 overlapping windows; February 13–14, 2014; one seed. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the recorded comparison ↗</a></p><div class="bottom-note">A measured result from this rehearsal, not a promised outcome for your edits.</div>


<!--
The selected agent code combined the absolute training loss from round one with a zero-initialized residual head from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-image
---

<div class="kicker">5:20–5:45</div>

# Compare the two models on one reserved-date image

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-final-predictions.png" alt="Manual and agent-selected forecasts for the same first accepted final case"><div class="image-caption">Forecast origin 2014-02-13T02:48 UTC. Same inputs, target, intensity scale, and error scale.</div></div><div class="bottom-note">The first accepted case is shown, not the case with the largest improvement.</div>


<!--
This figure is regenerated from the fresh v0.3.0 saved predictions. Compare manual and agent-selected forecasts on exactly the same case. The fixed error scale helps show differences without changing the colors between rows. The aggregate score includes all 199 accepted final windows. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: qualified-images
---

<div class="kicker">5:20–5:45</div>

# The image edits helped two seeds and slightly hurt one

<div class="scientific-figure"><img class="solar-photo" src="/images/images-seeds-deck.png" alt="Combined image edits lower error for seed 17 from 0.122442 to 0.110011 and seed 29 from 0.117650 to 0.109566, but raise seed 43 from 0.110168 to 0.110397"><div class="image-caption">Same saved sources, 40 updates per run, three predeclared training seeds. Final dates were already known.</div></div><div class="bottom-note">Mean error falls 5.79%. The predeclared requirement to improve every seed fails.</div>


<!--
The earlier ten point one five percent result remains correct for seed seventeen. It is not a result to promise for every run. Seed forty-three already has a strong manual model, and the combined edits are slightly worse. Its loss-only edit does better than both, which is retained in the full table. Initialization and sampled batches both change with the seed, so we do not know which caused this difference. This is fixed-code repetition, not three independent agent discoveries. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: repeatability
---

<div class="kicker">5:20–5:45</div>

# Separate repeated forecasts from repeated experiments

<div class="teaching-equation"><p><strong>199 windows</strong> reuse observations across two dates.</p><p><strong>Three seeds</strong> repeat fixed training recipes with different initialization and sampling.</p><p><strong>One agent discovery</strong> produced the edits we repeated.</p></div><div class="bottom-note">Neither count establishes performance across different solar periods or independent research-agent searches.</div>


<!--
Overlapping windows are not independent solar events. The three-seed qualification tests fixed source, not three agents independently discovering the same edit. Seed seventeen and twenty-nine improve, while seed forty-three slightly regresses. The mean improvement and that regression both belong in the conclusion. A next study could predeclare different dates, more training seeds and independent agent adaptations, but this workshop does not run that study. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-goes
---

<div class="kicker">5:20–5:45</div>

# The GOES model performed worse than persistence

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-final.png" alt="Observed GOES flux, persistence forecast, and selected model prediction on reserved dates"><div class="image-caption">Final log-flux MAE: selected model 2.469; persistence 0.193. 2,694 accepted windows.</div></div><div class="bottom-note">Compare the forecast with its loss curve. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=dtm5k18fpo4">Compare these forecasts in EvalTables ↗</a></div>


<!--
These are the fresh saved final GOES predictions. The selected sixty-step neural model misses badly, while persistence follows the observed flux much more closely. The later repaired recipe changes scaling, residual initialization, loss, and training budget together. Its separately recorded three-seed test follows; this historical failure remains unchanged. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: qualified-goes
---

<div class="kicker">5:20–5:45</div>

# The measurement repair passed its three-seed check

<div class="scientific-figure"><img class="solar-photo" src="/images/goes-seeds-deck.png" alt="GOES persistence MAE is 0.192706; the repaired recipe scores 0.162878, 0.163880 and 0.163760 for seeds 17, 29 and 43"><div class="image-caption">Recorded qualification: selected on validation dates, then evaluated with frozen weights on known final dates.</div></div><div class="bottom-note"><a href="https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md">All configurations, seeds, sources, and reproduction instructions ↗</a></div>


<!--
The residual MLP at twelve hundred updates was selected using the mean validation score across seeds seventeen, twenty-nine, and forty-three. Its final mean error is 0.163506, fifteen point one five percent below persistence. All three repetitions improve. These are the same known final dates and overlapping windows; this is a teaching retest, not another independent solar benchmark. There were no new agent calls. The notebook runs this recipe only when the learner clicks Train the worked GOES repair. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: result-meaning
---

<div class="kicker">5:20–5:45</div>

# Compare forecasts for the same timestamp

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=91ypk2or045"><img src="/images/evaltables-native.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:6%;top:39%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:6%;top:77%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:6%;top:53%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Choose image versions</b><br>Persistence, manual, and agent-selected use the same cases.</p><p><b>2 · Match forecast times</b><br>Input and target times must match across versions.</p><p><b>3 · Read masked error</b><br>Lower is better for this image task.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=91ypk2or045">Open this comparison ↗</a></p>


<!--
Open Compare in EvalTables in the final notebook step. The native Weave-backed Evaluation Tables Preview compares saved predictions. Keep GOES measurement results in their separate comparison. This screenshot comes from saved rehearsal data; publishing it does not retrain the models. Match this case_id and file_index to the notebook timestamp selector. The per-image score and full-split mean are shown separately. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: native-forecast
---

<div class="kicker">5:20–5:45</div>

# Compare errors for one observed future image

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=91ypk2or045"><img src="/images/evaltables-native-detail.png" alt="Native Forge Evaluation Tables Preview showing saved workshop results"></a><span class="eval-native-pin" style="left:11%;top:80%" aria-hidden="true">1</span><span class="eval-native-pin" style="left:28.3%;top:45%" aria-hidden="true">2</span><span class="eval-native-pin" style="left:28.3%;top:97%" aria-hidden="true">3</span></div><div class="eval-native-notes"><p><b>1 · Match the case</b><br>Use the same case ID in all three columns.</p><p><b>2 · Read the target</b><br>Every forecast is checked against this observed image.</p><p><b>3 · Compare the errors</b><br>The agent-selected version has lower masked error on this case.</p></div></div><p class="eval-native-caption">Recorded results in Forge · Evaluation Tables (Preview) · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=91ypk2or045">Open this comparison ↗</a></p>


<!--
The per-case image error averages absolute pixel differences inside the fixed solar-disk mask. Summary means cannot replace that score. Use the notebook image selector or saved prediction artifact to inspect the full arrays. Do not imply that the CES v2 backend succeeded; this is the working native Weave-backed Preview. Session block: Freeze and compare on reserved dates (minutes 320–345).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: reproduce
---

<div class="kicker">5:45–6:00</div>

# Check that the saved source contains both selected edits

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-artifact" href="/images/visual-v030-solar-artifact.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-artifact.png" alt="Native W&amp;B Artifact code view showing the selected candidate.py"></a><div class="product-caption"><span>Find the zero-initialized output layer and the absolute training loss.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0">Open the Artifact ↗</a></div><div class="image-caption">The same Artifact also holds <code>losses.json</code>, <code>weights.pt</code>, and <code>predictions.npy</code> from this training run.</div></div>


<!--
This is execution-f7550caa1639e8366efbf9d84a782289, the exact selected round-two composition. Open the source and weights together. The final evaluation loaded these weights. A different source file with the same model label would not reproduce this experiment. Session block: Reproduce and explain the result (minutes 345–360).
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
name: conclusion-turn
---

<div class="kicker">5:45–6:00 · YOUR TURN</div>

# Write down what changed and whether it helped

<div class="task">Use your own comparison.</div><ol class="exercise-controls"><li>Name one code change and report its error on the reserved dates.</li><li>Include a forecast that still missed. Say what you would try next.</li><li>Click <strong>Publish my conclusion</strong>. Follow a link in your Report back to the saved code or prediction.</li></ol><div class="done">Check your work: Your conclusion names the change, the measured result, and a remaining problem.</div>


<!--
Allow eight minutes. Ask participants to name a change, report what happened, and include a remaining miss. A negative result is fine. If publication fails, save the conclusion and retry the upload without rerunning the experiment. Session block: Reproduce and explain the result (minutes 345–360).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: close
---

<div class="kicker">5:45–6:00</div>

# Bring the results to the lab review

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-report" href="/images/visual-v030-solar-report.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-report.png" alt="Native Report excerpt summarizing the latest Solar technical rehearsal"></a><div class="product-caption"><span>Bring one result, its saved source, and the next experiment you would try.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the Report ↗</a></div><div class="image-caption">Recorded technical rehearsal. Use your own completed runs when writing your Report.</div></div>


<!--
Return to the weekly lab review. Ask participants to open their Report and follow one result to its source and saved prediction. In the recorded rehearsal, the selected image model reduced error, while the GOES model still lost to persistence. Both belong in the review. The image result uses one seed and two test days; it needs testing on other dates. The later qualification found that a repaired GOES recipe beat persistence on all three seeds. The saved image edits helped two seeds and slightly hurt one. Bring both facts to the review; neither replaces the original evidence. Ask each participant to propose a next test grounded in their own forecast. Session block: Reproduce and explain the result (minutes 345–360).
Source notes and recorded evidence: notes/sources.md.
-->

---
name: reference
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
name: answer-trace
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
name: answer-persistence
---

<div class="kicker">WORKED ANSWER</div>

# Return a copy of the latest observation

```python
def persistence_forecast(split):
    return split["persistence"].copy()
```

<p>The copy lets you work with the predictions without changing the dataset.</p>
<div class="source-link"><a href="/24">Return to Write and test persistence →</a></div>

<!--
The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
name: answer-flux
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
<div class="source-link"><a href="/35">Return to Write the loss and metric →</a></div>

<!--
Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: answer-search
---

<div class="kicker">WORKED ANSWER</div>

# Compare the settings and loss curves

<p class="big">Open two runs from the Sweep. Compare their model, width, learning rate, and training steps.</p><p>Then open the loss curves. A lower validation error is easier to interpret when you can see how each model trained.</p><div class="bottom-note">If a run failed, inspect its error. A missing score cannot rank that model.</div>
<div class="source-link"><a href="/49">Return to Run six configurations and inspect one forecast →</a></div>

<!--
Open the configuration and curve for two runs. Find the settings they share and the value that differs. If training failed, inspect the error rather than assigning a score to a forecast that does not exist.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
name: answer-images
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
<div class="source-link"><a href="/65">Return to Implement and compare the image predictors →</a></div>

<!--
The mask selects the solar disk. Compute the sum and count per image, then average across images. Check identical arrays, a constant one-unit difference, and a difference only outside the mask.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
name: answer-residual
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
name: answer-evidence
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
<div class="source-link"><a href="/75">Return to Choose the evidence for the research agent →</a></div>

<!--
First check that the record belongs to validation. Then return only the listed evidence fields. The current source is supplied separately. The final-test example should raise an error before the agent sees it.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
name: answer-controller
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
<div class="source-link"><a href="/90">Return to Test the selected code, then begin round two →</a></div>

<!--
Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: answer-final
---

<div class="kicker">WORKED ANSWER</div>

# Use the saved model without training it again

<p class="big">Load each selected model’s saved weights and predict the reserved dates.</p><p>Compare the three image forecasts at one timestamp. The input images and observed future should match across all three rows.</p><div class="bottom-note">Persistence copies the current image and needs no trained weights.</div>
<div class="source-link"><a href="/96">Return to Test the selected models on reserved dates →</a></div>

<!--
The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-edit
---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 1: absolute loss versus the unchanged model

<table class="clean-table"><tbody><tr><th>Tested source</th><th>Validation error ↓</th></tr><tr><td>Starting residual model</td><td>0.122116</td></tr><tr><td>A · use absolute training loss</td><td>0.120553</td></tr><tr><td>B · retain squared training loss</td><td>0.122116</td></tr></tbody></table><p>The composition selected A. Its separate test reproduced 0.120553.</p><div class="bottom-note">Recorded v0.3.0: one seed, 142 validation windows, the same forty-step budget.</div>


<!--
The alternative is a real KEEP decision and it is still tested. Candidate A changes only the loss and lowers validation error in this run. The composition keeps A. This is one seed, not evidence of a repeatable effect.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-keep
---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 2: sampling without replacement did not reduce error

<table class="clean-table"><tbody><tr><th>Tested source</th><th>Validation error ↓</th></tr><tr><td>Starting absolute-loss model</td><td>0.120553</td></tr><tr><td>A · zero-initialize the residual head</td><td>0.110916</td></tr><tr><td>B · sample without replacement</td><td>0.120557</td></tr></tbody></table><p>The composition selected A. It did not combine the unhelpful sampling change.</p><div class="bottom-note">Keep the tested sampling result alongside the selected version for comparison.</div>


<!--
Candidate B changes the batch sampling to seeded permutations. Its validation error is essentially the same as the parent and slightly higher. The composition keeps zero initialization and rejects the sampling change. Do not attribute a benefit to an untested combination.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recorded-lens
---

<div class="kicker">RECORDED REHEARSAL</div>

# Open the recorded research conversation

<p class="big"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7">Open the proposal and recorded notebook operations ↗</a></p><p>Find the active configuration, the requested edit, and the returned candidate code. Compare the proposal with the tested source.</p><p class="aside"><a href="https://ash0ts.github.io/forge-workshop-kit/solar/recorded-study.json">Download the recorded source, decisions, scores, and evidence links ↗</a></p><div class="bottom-note">Agent Lens may require sign-in. The source and saved decisions are also in the downloadable evidence.</div>


<!--
Open the proposal conversation. The notebook’s evidence-read span identifies the saved parent execution. The model request contains source and allowed evidence; its response contains the proposed candidates. Compare those separate records before following a training call. The downloadable records contain the same decisions and scores if the native view requires sign-in.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: recovery
---

<div class="kicker">REFERENCE</div>

# When a service is unavailable

<table class="clean-table"><tbody><tr><th>Failure</th><th>Next action</th></tr><tr><td>Project authentication or permission</td><td>Fix access, then retry the check</td></tr><tr><td>Training or inference failed</td><td>Inspect the saved error before retrying work</td></tr><tr><td>Trace or artifact upload failed</td><td>Retry export of the saved execution</td></tr><tr><td>Evaluation comparison upload failed</td><td>Use saved notebook results and retry publication</td></tr></tbody></table>


<!--
Start with the failed operation. An authentication problem needs corrected access. A failed training run needs its saved error inspected. An upload failure needs a publication retry. The separate CES v2 API remains unavailable. Native Evaluation Tables Preview uses verified Weave evaluation calls and is the workshop comparison path. If any upload fails, retain the notebook results and retry publication only.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: schedule-reference
name: schedule
---

<div class="kicker">REFERENCE</div>

# Six-hour session with three breaks

<table class="clean-table schedule"><tbody><tr><th>Minutes</th><th>Work</th></tr><tr><td>0–25</td><td>Connect and trace an operation</td></tr><tr><td>25–65</td><td>Read observations and implement persistence</td></tr><tr><td>65–95</td><td>Explain loss and save a training run</td></tr><tr><td>95–110</td><td>Break</td></tr><tr><td>110–155</td><td>Inspect model shapes and compare configurations</td></tr><tr><td>155–200</td><td>Implement image prediction and scoring</td></tr><tr><td>200–230</td><td>Meal break</td></tr><tr><td>230–260</td><td>Build the research-agent request</td></tr><tr><td>260–310</td><td>Review and test two rounds of changes</td></tr><tr><td>310–320</td><td>Break</td></tr><tr><td>320–345</td><td>Freeze and compare on reserved dates</td></tr><tr><td>345–360</td><td>Reproduce and explain the result</td></tr></tbody></table>


<!--
One six-hour session for a mixed room. The schedule includes fifty-five minutes of breaks. Keep introductory arithmetic beside implementation; experienced participants use the shape, broadcasting and metric checks to inspect assumptions. No extra training or paid research round has been added.
Source notes and recorded evidence: notes/sources.md.
-->

---
name: links
---

<div class="kicker">REFERENCE</div>

# Keep working in your own project

<p class="big"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Copy the Solar notebook ↗</a></p><p><a href="https://github.com/ash0ts/forge-workshop-kit">Source, setup, dataset, and facilitator guide ↗</a></p><p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Recorded rehearsal Report ↗</a></p><p class="aside"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view">For an office-agent example, open Pending, Inc. ↗</a></p><div class="bottom-note">Keep your notebook, code edits, and checkpoints. The facilitator needs no control over your runtime.</div>


<!--
Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.
Source notes and recorded evidence: notes/sources.md.
-->
