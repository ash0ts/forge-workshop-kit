---
theme: default
title: Build a research loop, then give it an agent
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

# Build a research loop.<br>Then give it an agent.

<div class="sub">A four-hour experiment in the Solar Forecasting Lab.</div><LabScene /><div class="bottom-note">Solar forecasting, experiment tracking, and agents that edit research code.</div>


<!--
We’ll build two small forecasts from real solar observations. First we’ll write and track the experiments ourselves. Then we’ll let a research agent propose changes to the image model’s code. The pixel lab is an illustration; the observations and recorded results come from the workshop dataset.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:01</div>

# Your team has a promising result.

<div class="quote">“The new model looks better.”<small>THE RESEARCH UPDATE · FICTIONAL SCENE</small></div><div class="two-col" style="margin-top:40px"><div><h2>You ask which run.</h2><p>Someone shares a screenshot.</p></div><div><h2>You ask which code.</h2><p>Someone shares a notebook called final.</p></div></div><div class="bottom-note">There are four notebooks called final.</div>


<!--
Imagine a teammate says the new model is better, but can only find a screenshot and several notebooks called final. That’s our fictional opening. Ask the room what they would need before trusting or repeating the comparison.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:02</div>

# Two forecasts from real solar observations

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-observations.png" alt="GOES X-ray readings and an AIA solar image from February 1, 2014"><div class="image-caption">Real training observations. NOAA GOES-15 and NASA/SDO AIA 171 Å; prepared with SunPy.</div></div><div class="observation-tasks"><p><strong>Measurements:</strong> use the previous hour to predict flux 30 minutes ahead.</p><p><strong>Images:</strong> use two observations to predict an image one hour ahead.</p></div>


<!--
Read the instruments before discussing models. The left plot measures solar X-ray flux; the right image records extreme-ultraviolet light at 171 Å. These are real February 2014 observations, prepared at a small scale for CPU teaching. The image uses false color. We are testing forecasts, not predicting a reliable flare warning.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:03</div>

# First reproduce a result. Then try to improve it.

<div class="quote">“Could an agent try the next experiment?”<small>THE LAB’S NEXT REQUEST</small></div><div class="step-path"><div><h2>First, you build the experiment.</h2><p>Define the target, train a model, and save what ran.</p></div><div><h2>Then the agent changes its code.</h2><p>Review the change, run it, and compare the prediction.</p></div></div>


<!--
The reason for building the experiment stack comes first: we need to know whether a change helped and be able to repeat it. Once that works, the same loop can test code proposed by an agent. The language model stays fixed. The small forecasting model trains normally.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:04</div>

# Build a forecast, then test changes to its code

<div class="step-path"><div><h2>Forecast</h2><p>Load observations and write a baseline.</p></div><div><h2>Track</h2><p>Save code, settings, weights, and predictions.</p></div><div><h2>Improve</h2><p>Review and test the agent’s code changes.</p></div><div><h2>Evaluate</h2><p>Compare the selected models on later dates.</p></div></div><div class="bottom-note">You’ll edit Python in your own notebook and publish the results to your project.</div>


<!--
Follow this sequence in the notebook. You’ll change Python, run a check, execute the experiment, and open the resulting evidence in Forge. A change that fails to improve the forecast is still something we can investigate.
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

```python
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
Conversation identifies the execution. Turn holds the mission. Tool records one operation. The attribute line is the learner edit, not a second call. Actual instrumentation also supplies start and end timestamps and records exceptions. Run the free check, send the setup trace, then find the same field in Agent Lens.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:08–0:15 · YOUR TURN</div>

<a class="answer-link" href="/78">Worked answer → 78</a>

# Connect and inspect your first tool call

<div class="task">Open <strong>1 · Connect</strong>.</div><ol class="exercise-controls"><li>Click <strong>Connect and restore my work</strong>. Check that the project is yours.</li><li>In <code>instrument_tool</code>, add the <code>workshop.exercise</code> attribute with value <code>solar-research</code>. Click <strong>Check my tracing code</strong>.</li><li>Click <strong>Send my first Agent Lens trace</strong>. Open the tool call in Agent Lens and find the attribute you added.</li></ol><div class="done">Check your work: Find your attribute beside the tool’s arguments and result.</div>


<!--
Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Find the field your code added to the span

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-trace" href="/images/visual-v030-solar-trace.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-trace.png" alt="Native Agent Lens setup tool span from the current Solar rehearsal"></a><div class="product-caption"><span>Read the returned NumPy version. Open Raw to find workshop.exercise.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/4ca0a7e5c9d1fe30d24079ea5b98b750">Open the setup trace ↗</a></div><div class="image-caption">Recorded v0.3.0 environment check. No language-model call was needed.</div></div>


<!--
The exercise is complete when the participant can find their own attribute in their own tool span. Here is the recorded reference. The tool arguments, result, and duration describe one actual operation. The same instrumentation function records later training calls.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Predict X-ray flux 30 minutes ahead

<ForecastWindow mode="goes" /><div class="bottom-note">Predict log10 XRS-B flux. A forecast window includes observations, timestamps, and a future target.</div>


<!--
Read the timeline from left to right. The model gets sixty minutes of observed flux, then predicts the reading thirty minutes after now. We work in log10 flux, so the error is in transformed units rather than raw watts per square metre.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:17</div>

# Use earlier dates to train, later dates to test

<ForecastWindow :split="true" /><div class="bottom-note">February 2014, UTC. Fit normalization on training data only.</div>


<!--
Train on February 1–10, choose models using February 11–12, and leave February 13–14 for the final comparison. Every input and the target of a window must belong to one partition. Fit normalization using training data only.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:19</div>

# Leave out windows with missing observations

<div class="two-col"><div><h2>Check the timestamps</h2><p>The prepared GOES archive has no data for February 8.</p><p>A window needs its full input history and its future target.</p></div><div><h2>Skip an incomplete window</h2><p>Keep the missing date in the coverage record.</p><p>A zero would invent a measurement that the instrument never supplied.</p></div></div><div class="bottom-note">Use the same accepted windows for every model in the comparison.</div>


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
Persistence means predicting that the latest value will stay the same. Solar observations are correlated over time, so this simple baseline can be hard to beat. It gives us a comparison before we spend time training a network.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:29</div>

# Measure how far the prediction missed

```python
error = mean(abs(predicted_log_flux - observed_log_flux))
```

<div class="two-col" style="margin-top:35px"><div><h2>Lower is better</h2><p>The same target, transform, and units apply to every run.</p></div><div><h2>Look at individual misses</h2><p>Inspect the times where the forecast misses.</p></div></div><div class="bottom-note">Compare each prediction with the observed future, then average the errors.</div><div class="code-contract compact-contract"><span><strong>Input:</strong> Predictions and matching future observations</span><span><strong>Output:</strong> One mean absolute error in log-flux units</span></div>


<!--
For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:30–0:40 · YOUR TURN</div>

<a class="answer-link" href="/79">Worked answer → 79</a>

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
Use these as possible explanations for a changed score, not claims about this rehearsal. If code, data, or training time differs, we need to know that before deciding why the score moved.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:41</div>

# Which setting changed between these runs?

<RunInspector />


<!--
These are two recorded GOES runs. Before revealing the settings, ask what the scores let us conclude. Then click Show active settings. Both runs used the same source and budget, but their learning rates differed.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:42</div>

# These runs used different learning rates

<RunInspector :revealed="true" />


<!--
The learning rate changed from .001 to .003. Data, source, seed, steps, and batch size stayed the same. Both errors were worse than persistence, so choosing the smaller of these two errors still leaves a poor forecast.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:42</div>

# Turn observations into a forecast

<ResearchMap :level="0" />


<!--
Start with the forecast itself: observations enter the model and it produces a number or an image. We’ll add the records around this process one piece at a time.
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
Keep the target, dates, and primary metric unchanged while comparing models. Otherwise a lower score might come from an easier test rather than a better forecast.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:45</div>

# Save the files needed to repeat the run

<ResearchMap :level="3" /><div class="bottom-note">A W&B Artifact is a versioned bundle of files: here, data, code, trained weights, and predictions.</div>


<!--
A W&B run stores settings and metric history. A W&B Artifact stores a versioned bundle of files. Here that means the data, source, weights, and predictions needed to repeat or inspect a result.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:47</div>

# Save code and outputs with each training run

```python
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
This shortened example shows where saving sits around training. The notebook’s run_training function runs your source, then saves the result. If that same stage has already completed, the saved result can be restored instead of training again.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:49</div>

# Restore a completed run after a restart

<div class="step-path"><div><h2>Finish a run</h2><p>Save its code, outputs, and completion record locally.</p></div><div><h2>Upload a checkpoint</h2><p>Store a versioned copy as a W&B Artifact in your project.</p></div><div><h2>Reopen the notebook</h2><p>Restore that checkpoint and inspect the completed results.</p></div></div><div class="bottom-note">You can continue from the saved run without training the model again.</div>


<!--
The local completion record tells the notebook which work finished. The checkpoint Artifact stores a copy in your project. If the runtime is replaced, restore the checkpoint before continuing. An upload failure can be retried using the local files.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:50–1:05 · YOUR TURN</div>

<a class="answer-link" href="/80">Worked answer → 80</a>

# Write the loss and metric

<div class="task">Open <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Implement <code>training_loss</code> and <code>my_flux_mae</code>.</li><li>Click <strong>Check my measurement code</strong>. Test identical arrays and a constant one-unit error.</li><li>In <code>run_training</code>, find where it saves source, settings, weights, and predictions. The next exercise will produce those files.</li></ol><div class="done">Check your work: Your checks pass, and you can point to where run_training saves its files.</div>


<!--
Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:05</div>

# Three ways to change an experiment

<SolarMechanism mode="search" />


<!--
Point to the exact change in each row. A Sweep changes values within the current program. Comparing an MLP with a CNN selects an implementation we wrote. The research agent will edit the program itself. Every version still needs the same data partitions and score.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:07</div>

# Compare six model configurations

<table class="clean-table"><tbody><tr><th>Architecture</th><th>Widths</th><th>Learning rates</th><th>Training budget</th></tr><tr><td>Small MLP</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr><tr><td>Temporal CNN</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr></tbody></table><div class="bottom-note">Seed 17. Batch size 32. The notebook records the active values.</div>


<!--
These six configurations are the workshop defaults: two model families, three settings per family, seed 17, batch size 32, and sixty training steps. It’s a short CPU exercise, so inspect whether the models have trained enough before drawing an architecture conclusion.
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
W&B Sweeps assigns each configuration to a run. Our training function does the fitting and saves its outputs. This is a shortened excerpt; the notebook contains the entity, project, and complete configuration setup.
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

# Read the loss curve before choosing another model

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-loss.png" alt="Saved GOES model loss curve over 60 training steps"><div class="image-caption">Selected MLP: width 16, learning rate .003, seed 17. Saved v0.3.0 training losses.</div></div><div class="bottom-note">The loss was still falling at the limit. Longer training is a next experiment, not a measured result here.</div>


<!--
This is the actual selected GOES run, not an invented trend. Its loss is still falling at sixty steps. Inspect its predictions and fixed validation metric too. A falling training loss alone does not tell us the future forecast is good. Longer training is a concrete follow-up, but this workshop did not run it.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:15–1:30 · YOUR TURN</div>

<a class="answer-link" href="/81">Worked answer → 81</a>

# Run six configurations and inspect one forecast

<div class="task">Stay in <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Click <strong>Run six tracked configurations</strong>.</li><li>Open the Sweep. Compare validation error and training time for two configurations.</li><li>Open one run’s Artifact. Find its source and predictions, then compare the forecast with its loss curve and score.</li></ol><div class="done">Check your work: Explain one comparison using the settings, curve, and forecast.</div>


<!--
Allow fifteen minutes. Ask participants to predict which configuration will win before running the search. After it finishes, have them explain one result from the loss curve and forecast. Keep failed runs visible so the comparison accounts for what happened.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:30–1:40</div>

# The experiments can wait ten minutes.

<p class="big">Save your work and take ten minutes.<br>We’ll start the image experiment when we return.</p><div class="bottom-note">The notebook can stay open. There’s no exercise to run during the break.</div>


<!--
Take ten minutes. Confirm saved work is visible before leaving. No background experiment is required during the break.
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

# Save image experiments the same way

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

# Two image channels enter. One forecast comes out.

<SolarMechanism mode="residual" :reveal="1" />


<!--
Here the network predicts the entire future image. A batch has two input channels, each 64 by 64. The output has one channel. The forward function returns self.net(x). Keep this geometry in view for the residual reveal.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:48</div>

# Let the current image carry what has not changed

<SolarMechanism mode="residual" :reveal="2" />


<!--
The network now predicts a correction. The arrow around the network copies the current input image and adds the correction to it. In x[:, 1:2], the slice keeps the channel dimension, giving batch by one by 64 by 64. Zero correction returns persistence exactly. That is the behavior participants add to forward.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:49</div>

# Write the addition you just traced

```python
def forward(self, x):
    correction = self.net(x)       # [batch, 1, 64, 64]
    current_image = x[:, 1:2]      # keep the channel axis
    return current_image + correction
```

<div class="code-contract"><span><strong>Input:</strong> earlier image + current image</span><span><strong>Output:</strong> one future image per example</span></div><p class="aside">Check: if <code>correction</code> is zero, the forecast equals the current image.</p>


<!--
The diagram and code describe the same addition. Ask participants why x[:, 1] would remove a dimension and why x[:, 1:2] preserves it. The notebook implementation also branches on architecture so the convolutional comparison still returns only the network output.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:50</div>

# Count errors on the solar disk

<SolarMechanism mode="mask" />


<!--
This is a diagram of the scoring calculation, not a forecast. The fixed mask assigns one to disk pixels and zero outside. Multiply absolute errors by the mask, average over the selected pixels per image, then average images. A changed off-disk pixel must not affect the score.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:51</div>

# Write the scorer, then test a deliberate miss

```python
absolute_error = np.abs(prediction - target)
per_image = (absolute_error * disk_mask).sum(axis=(1, 2, 3))
per_image /= disk_mask.sum(axis=(1, 2, 3))
return float(per_image.mean())
```

<div class="code-contract"><span><strong>Identical arrays:</strong> score 0</span><span><strong>Every disk pixel +1:</strong> score 1</span><span><strong>Only off-disk pixels +1:</strong> score 0</span></div>


<!--
Run the three local examples before training. They explain what the scorer measures. The participant writes this development scorer, and the protected primary scorer checks the comparison with the same published rule. Missing or invalid predictions are not zero error.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:52</div>

# Train with one loss; compare with a fixed metric

<table class="clean-table"><tbody><tr><th>Training loss</th><th>Primary evaluation metric</th></tr><tr><td>Supplies gradients while fitting weights</td><td>Measures predictions for comparison</td></tr><tr><td>Candidate code can change it</td><td>Fixed outside candidate code</td></tr><tr><td>The starting implementation uses squared error</td><td>The image comparison uses masked absolute error</td></tr></tbody></table>


<!--
The training loss supplies gradients that update weights. The evaluation metric tells us how the forecast compares with another model. We can try a different training loss while keeping the scoring rule fixed. That will be one of the agent’s recorded proposals.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:54</div>

# Compare forecasts for the same validation case

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-validation-predictions.png" alt="Matched convolutional and residual predictions beside the same observed future"><div class="image-caption">Recorded v0.3.0 forecasts. First accepted validation case; common intensity and error scales.</div></div><div class="bottom-note">Compare the error maps, then check the score across all 142 validation windows.</div>


<!--
The same current image and observed future appear in both rows. The convolutional forecast is above, residual below. The figure uses the first accepted case, not a selected success. Colors use the same scale across both rows. A single image is an example; the validation score includes all 142 windows.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:55–2:15 · YOUR TURN</div>

<a class="answer-link" href="/82">Worked answer → 82</a>

# Implement and compare the image predictors

<div class="task">Open <strong>5 · Solar images</strong>.</div><ol class="exercise-controls"><li>Edit <code>ImagePredictor.forward</code>, <code>training_loss</code>, and <code>my_image_mae</code>.</li><li>Click <strong>Check my image code</strong>. A +1 error should score 1; an off-disk change should score 0.</li><li>Click <strong>Compare convolutional and residual predictors</strong>. Inspect both forecasts.</li></ol><div class="done">Check your work: Show which model validation selected, then point to a region where its forecast missed.</div>


<!--
Give participants twenty minutes. Start with the local scorer examples, then train both model versions. Ask each participant to explain why validation selected one and show a region it still missed.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:15</div>

# Give the research agent your code and results

<p class="agent-explanation">So far, you’ve written the models and chosen their settings. Now give a research agent that code and its validation results, and ask for two changes. Read the diffs, train both candidates, and compare their errors. The version selected by validation error becomes the starting point for the next round.</p><div class="bottom-note">The agent writes proposals. You review the code before the notebook runs it.</div>


<!--
Read this transition as one explanation. Until now, we wrote the models and chose the settings ourselves. We’ll now ask an agent for two code changes, inspect them, and use the experiment we built to test them. The selected code becomes the next round’s starting point.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:17</div>

# The agent edits code. The forecast model learns weights.

<SolarMechanism mode="weights" />


<!--
There are two models with different jobs. The language model writes Python and keeps the same weights. The small forecasting network trains weights using that Python and the earlier solar observations. Validation evidence returns to the research agent for another proposed edit. This is code-directed research, not post-training the language model.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:19</div>

# Decide which files the agent may change

<div class="two-col"><div><h2>The agent may edit</h2><p>Model layers<br>Feature computation<br>Training loss<br>Training procedure</p></div><div><h2>The experiment keeps fixed</h2><p>Training and validation dates<br>What we predict<br>How we score predictions<br>The reserved final-test dates</p></div></div><div class="bottom-note">Candidate Python runs in this notebook’s environment after your review.</div>


<!--
The agent can edit feature, model, loss, and training code. It cannot change the date partitions, forecast target, or comparison metric. Review every proposed diff before execution. These training subprocesses are time-limited and do not inherit Forge credentials, but they are not a security sandbox.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:21</div>

# Send the code, settings, and validation results

<div class="step-path"><div><h2>Exact source</h2><p>The files that produced the parent result.</p></div><div><h2>Active settings</h2><p>Architecture, steps, width, optimizer values.</p></div><div><h2>Validation evidence</h2><p>Curves, errors, predictions, and failed attempts.</p></div></div><div class="bottom-note">A default in source may not be the value the run used.</div>


<!--
Send the files and settings that produced the current result, plus its validation outputs. A default learning rate in source may differ from the value used in the run. The agent needs the active values to propose a relevant change.
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

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-evidence" href="/images/visual-v030-solar-evidence.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-evidence.png" alt="Native read_validation_evidence span from the current Solar proposal"></a><div class="product-caption"><span>Find the parent configuration and validation error before reading its proposal.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/23f4a8510534f241b9c6ccacb0ef3cb7/spans">Open the proposal ↗</a></div><div class="image-caption">Recorded v0.3.0 round 1. The agent receives validation evidence, never the reserved-date score.</div></div>


<!--
Open read_validation_evidence. Find the residual architecture, forty training steps, seed seventeen, and parent validation error. Then inspect the returned proposal. This request initially exhausted its output budget and used a saved retry; that is an execution event, not a change in forecasting quality.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:25–2:40 · YOUR TURN</div>

<a class="answer-link" href="/84">Worked answer → 84</a>

# Choose the evidence for the research agent

<div class="task">Open <strong>6 · Research agent</strong>.</div><ol class="exercise-controls"><li>In <code>select_validation_evidence(record)</code>, keep the active settings and validation results. Click <strong>Check my evidence selection</strong>.</li><li>Read the check result. Confirm that the final-test example is rejected.</li><li>Name the validation fields your function will send to the agent. What can it learn from them?</li></ol><div class="done">Check your work: You can name the code and validation results the agent will receive.</div>


<!--
Allow twelve minutes. Participants should edit the evidence selector, then run the check that accepts validation evidence and rejects the final-test example. Ask them to name what the agent will receive before sending a request.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:40</div>

# Ask for two changes to the same starting code

<ResearchBranches :level="1" /><div class="bottom-note"><a href="https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335">Harness²-inspired</a>: our probes train forecasting weights and include validation scores.</div>


<!--
Both candidates start from the same code and settings. This borrows Propose–Probe–Compose from Harness². Here the probes train forecasting models and give validation scores to the editor, so it is a teaching adaptation rather than the paper’s exact task protocol.
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

# Ask the agent which changes to keep

<ResearchBranches :level="3" /><div class="bottom-note">The agent can keep A, keep B, combine changes, or retain the starting code.</div>


<!--
The agent reads both test results and can keep one candidate, combine changes, or retain the starting code. The dashed lines mean that it reviewed the results. They do not mean both sets of changes were merged.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:46</div>

# Test the version the agent chose

<ResearchBranches :level="4" /><div class="bottom-note">Run the selected code on the same training and validation dates.</div>


<!--
Run the chosen code before accepting it. Combining two changes can behave differently from either one alone. If the unchanged version is retained, testing it creates another execution of the same code.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:47</div>

# Open the training call behind the chosen version

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-training" href="/images/visual-v030-solar-training.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-training.png" alt="Native train_and_validate tool span with actual source settings and returned metrics"></a><div class="product-caption"><span>Check the configuration, then find validation_error in the returned result.</span><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/f7550caa1639e8366efbf9d84a782289">Open the selected training call ↗</a></div><div class="image-caption">Recorded v0.3.0 round 2 composition test. “error” is forecast error here, not an exception.</div></div>


<!--
The operation trained and validated the selected source. Find the returned score and compare the run to the saved source artifact. An error metric of 0.110916 is the forecasting metric, not a tool failure. If a span actually failed, inspect its exception separately.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">2:48</div>

# Start round two from the selected version

<ResearchBranches :level="5" /><div class="bottom-note">Use the selected code and what the first tests showed to plan the next changes.</div>


<!--
The selected code and a short lesson enter round two. The agent now proposes changes on top of that version. We are still forecasting the same image task and selecting with the same validation metric.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:50–3:00 · YOUR TURN</div>

# Propose and test two changes

<div class="task">Inspect <code>next_research_action</code> in <strong>6 · Research agent</strong>.</div><ol class="exercise-controls"><li><strong>Propose two code changes</strong>. Read both diffs.</li><li>Confirm review of Candidate A → <strong>Test Candidate A</strong>. Confirm review of Candidate B → <strong>Test Candidate B</strong>.</li><li><strong>Record my comparison</strong>, then <strong>Request a composition</strong>.</li></ol><div class="done">Check your work: Each candidate’s proposal diff and training result are linked in Agent Lens.</div>


<!--
Keep this slide visible while participants propose and test the first two candidates. Ask them to explain each diff before confirming review. After both tests, record a comparison and request the agent’s choice.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:00–3:15 · YOUR TURN</div>

<a class="answer-link" href="/85">Worked answer → 85</a>

# Test the selected code, then begin round two

<div class="task">Continue the same workbench.</div><ol class="exercise-controls"><li>Confirm review of composition, then <strong>Test the composition</strong>.</li><li>Click <strong>Save the adopted version and lesson</strong>. Check whether the parent was retained.</li><li>Repeat the process in round two using the previous outcome.</li></ol><div class="done">Check your work: Open the selected version from each round and explain why it was kept.</div>


<!--
Give participants fifteen minutes for the tested selection and the second round. Retaining the previous code is a valid outcome. Ask why it was retained, then show its saved execution rather than treating KEEP as skipped work.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:15</div>

# Follow one proposal through the branch diagram

<ResearchBranches :level="5" :interactive="true" />


<!--
Click a candidate, its test, and the selection step. Ask someone to explain what happened along that path. This diagram explains the process; the notebook’s branch view opens their actual files and results.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:17</div>

# Freeze both the code and the trained weights

<SolarMechanism mode="freeze" />


<!--
Select using validation, then freeze the code and its trained weights together. The final step loads those weights and predicts later dates; it does not keep fitting or ask the agent which final score it likes. Once you inspect final results, further editing needs a new reserved test for a new comparison.
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

# Compare predictions for the same times

<table class="clean-table"><tbody><tr><th>Case identity</th><th>Persistence</th><th>Manual</th><th>Agent-selected</th></tr><tr><td>Same input timestamps</td><td>Prediction + error</td><td>Prediction + error</td><td>Prediction + error</td></tr><tr><td>Same target timestamp</td><td>Saved output</td><td>Executed source</td><td>Executed source</td></tr></tbody></table><div class="bottom-note">Use each case ID to find the same input and target times in Weave or EvalTables.</div>


<!--
Choose one case identity and compare the predictions for its shared input and target times. Weave stores these evaluation records. Native EvalTables was unavailable during the rehearsal, so the notebook and Weave comparison remain available; publication can be retried separately.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">3:25–3:45 · YOUR TURN</div>

<a class="answer-link" href="/86">Worked answer → 86</a>

# Test the selected models on reserved dates

<div class="task">Open <strong>7 · Final evaluation</strong>.</div><ol class="exercise-controls"><li>Click <strong>Freeze versions and evaluate reserved dates</strong>.</li><li>Choose one timestamp. Compare each image forecast with the same observed future.</li><li>Open one result’s training record and Agent Lens call. Compare the image scores separately from the GOES scores.</li></ol><div class="done">Check your work: Explain a difference between two forecasts using their images and scores.</div>


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

# Compare one saved forecast at the same time

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-final-predictions.png" alt="Manual and agent-selected forecasts for the same first accepted final case"><div class="image-caption">Forecast origin 2014-02-13T02:48 UTC. Same inputs, target, intensity scale, and error scale.</div></div><div class="bottom-note">The first accepted case is shown, not the case with the largest improvement.</div>


<!--
This figure is regenerated from the fresh v0.3.0 saved predictions. Compare manual and agent-selected forecasts on exactly the same case. The fixed error scale helps show differences without changing the colors between rows. The aggregate score includes all 199 accepted final windows.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:47 · RECORDED REHEARSAL</div>

# The selected GOES forecast lost to persistence

<div class="scientific-figure"><img class="solar-photo" src="/images/v030-goes-final.png" alt="Observed GOES flux, persistence forecast, and selected model prediction on reserved dates"><div class="image-caption">Final log-flux MAE: selected model 2.469; persistence 0.193. 2,694 accepted windows.</div></div><div class="bottom-note">Keep this failure in the comparison. The image result does not erase it.</div>


<!--
These are the fresh saved final GOES predictions. The selected sixty-step neural model misses badly, while persistence follows the observed flux much more closely. The training curve suggests a longer equal budget as a follow-up. That follow-up has not been run, and the failure does not establish that neural forecasting cannot work.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:48</div>

# Read the saved score for one image in Weave

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-comparison" href="/images/visual-v030-solar-comparison.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-comparison.png" alt="Native Weave expanded row showing prediction mean, target mean, file index, and error"></a><div class="product-caption"><span>Find file_index 0 and its error. Why is the score not the difference between the two means?</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the linked results ↗</a></div><div class="image-caption">One saved agent-selected case. Image means summarize the arrays; the score averages pixel errors inside the disk mask.</div></div>


<!--
This expanded native Weave row is the first final agent-selected image, file_index zero. Prediction mean is −1.760701 and target mean is −1.759181, but masked MAE is 0.109328. Differences between bright and dark pixels can cancel in a mean. The scorer instead takes each pixel’s absolute error before averaging. Open the saved array to see the forecast. The notebook supplies the aligned comparison; this is not native EvalTables.
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

# Write what changed, what helped, and what still missed

<div class="native-product-evidence"><a class="product-screen visual-v030-solar-report" href="/images/visual-v030-solar-report.png" target="_blank" aria-label="Open full-size capture"><img src="/images/visual-v030-solar-report.png" alt="Native Report excerpt summarizing the latest Solar technical rehearsal"></a><div class="product-caption"><span>Follow one result to its source and forecast, then propose the next test.</span><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==">Open the Report ↗</a></div><div class="image-caption">A recorded technical rehearsal. Your Report should describe your own completed experiments.</div></div>


<!--
Close with the measured result and a concrete next test, such as a longer equal GOES training budget or new reserved dates for the image change. The recorded result is one seed across two reserved days. Participants should explain their own result, including failures and remaining misses.
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
<div class="source-link"><a href="/20">Return to Write and test persistence →</a></div>

<!--
The prepared split includes the last observed reading for each forecast window. Return a copy so later changes to the prediction array cannot alter the dataset.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Take the mean of the absolute errors

```python
def training_loss(prediction, target, mask):
    return ((prediction - target).square() * mask).sum() / mask.sum()

def my_flux_mae(prediction, target):
    return float(np.abs(prediction - target).mean())

assert my_flux_mae(np.ones(3), np.zeros(3)) == 1.0
assert my_flux_mae(np.zeros(3), np.zeros(3)) == 0.0
```


<div class="source-link"><a href="/30">Return to Write the loss and metric →</a></div>

<!--
Subtract prediction and target, take absolute values, and average. A prediction of one against a target of zero gives one. These are log10 flux units. The training loss above it is separate and uses squared error.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Compare the settings and loss curves

<p class="big">Open two runs from the Sweep. Compare their model, width, learning rate, and training steps.</p><p>Then open the loss curves. A lower validation error is easier to interpret when you can see how each model trained.</p><div class="bottom-note">If a run failed, inspect its error. A missing score cannot rank that model.</div>
<div class="source-link"><a href="/36">Return to Run six configurations and inspect one forecast →</a></div>

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
<div class="source-link"><a href="/48">Return to Implement and compare the image predictors →</a></div>

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
<div class="source-link"><a href="/55">Return to Choose the evidence for the research agent →</a></div>

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
<div class="source-link"><a href="/64">Return to Test the selected code, then begin round two →</a></div>

<!--
Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Use the saved model without training it again

<p class="big">Load each selected model’s saved weights and predict the reserved dates.</p><p>Compare the three image forecasts at one timestamp. The input images and observed future should match across all three rows.</p><div class="bottom-note">Persistence copies the current image and needs no trained weights.</div>
<div class="source-link"><a href="/69">Return to Test the selected models on reserved dates →</a></div>

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

# Round 2: a plausible sampling change did not help

<table class="clean-table"><tbody><tr><th>Tested source</th><th>Validation error ↓</th></tr><tr><td>Starting absolute-loss model</td><td>0.120553</td></tr><tr><td>A · zero-initialize the residual head</td><td>0.110916</td></tr><tr><td>B · sample without replacement</td><td>0.120557</td></tr></tbody></table><p>The composition selected A. It did not combine the unhelpful sampling change.</p><div class="bottom-note">The sampling idea was plausible. Its measured result supplied the reason to leave it out.</div>


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
