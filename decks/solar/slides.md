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

# Forecast the next solar observation

<p class="big">Use the observations we have now to predict what the instruments will measure later.</p><div class="step-path"><div><h2>Measurements</h2><p>Use one hour of X-ray readings to predict flux 30 minutes ahead.</p></div><div><h2>Images</h2><p>Use two solar images to predict the image one hour ahead.</p></div></div><div class="bottom-note">These small experiments use real observations. They are not operational forecasts.</div>


<!--
Our first task uses the last hour of GOES X-ray measurements to predict flux thirty minutes later. The second uses two AIA images to predict another image one hour ahead. SunPy helps us inspect the observation times, wavelength, and units.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:03</div>

# Can an agent improve the research code?

<div class="quote">“Once the experiment works, could an agent improve it?”<small>THE NEXT LAB QUESTION</small></div><ResearchMap :level="4" />


<!--
Once we can run and compare an experiment, we can give an agent the code and ask it to propose a change. We’ll train the small forecasting models as usual. The language model writing those proposals stays fixed.
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

<div class="kicker">0:06</div>

# Run the same notebook on your laptop

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen
uv run wandb login --verify
uv run marimo edit notebooks/solar_autoresearch.py
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

# Record a tool call in Agent Lens

```python
with tracing.Conversation(conversation_id=execution_id):
    with tracing.Turn(agent_name="researcher", messages=mission):
        with tracing.Tool(
            name="inspect_training_environment",
            arguments={}, result=observed_environment,
        ):
            ...
```

<div class="bottom-note">Record the tool’s inputs, result, timing, and any error.</div>


<!--
A conversation groups the work. A turn records a request, and a tool span records one operation and its result. The notebook supplies the outer scopes. You’ll edit the tool scope and add an attribute you can then find in Agent Lens.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:08–0:15 · YOUR TURN</div>

<a class="answer-link" href="/75">Worked answer → 75</a>

# Connect and inspect your first tool call

<div class="task">Open <strong>1 · Connect</strong>.</div><ol class="exercise-controls"><li>Click <strong>Connect and restore my work</strong>. Check that the project is yours.</li><li>In <code>instrument_tool</code>, add the <code>workshop.exercise</code> attribute with value <code>solar-research</code>. Click <strong>Check my tracing code</strong>.</li><li>Click <strong>Send my first Agent Lens trace</strong>. Open the tool call in Agent Lens and find the attribute you added.</li></ol><div class="done">Check your work: Find your attribute beside the tool’s arguments and result.</div>


<!--
Allow 7 minutes. Ask participants to show the attribute they added in their own Agent Lens tool call. The setup operation inspects the notebook environment and makes no language-model request. If someone cannot publish it, check project access before proceeding.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Check the project before you run an exercise

<div class="native-columns"><a href="/images/ux-v022-solar-setup.png" target="_blank"><img src="/images/ux-v022-solar-setup.png" alt="Revised notebook showing the participant project, allowance and guided exercise navigation"></a><div><h2>Check your project.</h2><p>Enter the Forge project where you want to save this workshop.</p><h2>Check your allowance.</h2><p>Inference and notebook compute are separate.</p><p class="aside"><a href="/images/ux-v022-solar-setup.png" target="_blank">Open full capture ↗</a></p></div></div><div class="bottom-note">The setup screen before connecting to a project.</div>


<!--
This screenshot shows the Connect step before access is checked. Enter your own project, choose an inference allowance, then click Connect and restore my work. This image does not show a completed connection.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">0:15</div>

# Add an attribute to the tool span

<div><a class="instrumentation-crop" href="/images/ux-v020-solar-instrumentation.png" target="_blank" aria-label="Open the full tracing exercise"><img src="/images/ux-v020-solar-instrumentation.png" alt="Actual editable instrument_tool function with the attribute exercise and free tracing check"></a><p class="aside">Add the attribute inside the tool scope. This writer also instruments your later training calls.</p><div class="image-caption">Recorded rehearsal: the attribute is added and the local check passes. <a href="/images/ux-v020-solar-instrumentation.png" target="_blank">Open full capture ↗</a></div></div>


<!--
Point to the attribute inside the tool scope. The free code check tests the function locally. The separate trace button publishes the environment check. This same function will record later training calls.
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

<div class="bottom-note">Inspect the FITS metadata here; use the prepared arrays for training.</div>


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

<p class="big">Predict flux 30 minutes ahead by copying the latest reading.</p><div class="bottom-note">This uses only a reading we already have. It does not look at the future target.</div>


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

<div class="two-col" style="margin-top:35px"><div><h2>Lower is better</h2><p>The same target, transform, and units apply to every run.</p></div><div><h2>Look at individual misses</h2><p>Inspect the times where the forecast misses.</p></div></div><div class="bottom-note">Compare each prediction with the observed future, then average the errors.</div>


<!--
For each forecast, subtract the observed log-flux target, take the absolute error, then average across windows. Lower is better. The average can hide a bad interval, so we also inspect the curves. Keep flux error separate from the later image score.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">0:30–0:40 · YOUR TURN</div>

<a class="answer-link" href="/76">Worked answer → 76</a>

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

<div class="bottom-note">You write the training function. The session records its code and outputs.</div>


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

<a class="answer-link" href="/77">Worked answer → 77</a>

# Write the loss and metric

<div class="task">Open <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Implement <code>training_loss</code> and <code>my_flux_mae</code>.</li><li>Click <strong>Check my measurement code</strong>. Test identical arrays and a constant one-unit error.</li><li>In <code>run_training</code>, find where it saves source, settings, weights, and predictions. The next exercise will produce those files.</li></ol><div class="done">Check your work: Your checks pass, and you can point to where run_training saves its files.</div>


<!--
Allow fifteen minutes. Have participants implement the loss and metric, run the small checks, then find the file-saving calls in run_training. The next exercise produces those files. If they struggle with the metric, use a prediction of one against a target of zero as the first example.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:05</div>

# Choose settings, choose a model, or write new code

<table class="clean-table"><tbody><tr><th>Operation</th><th>What changes</th></tr><tr><td>Hyperparameter search</td><td>Values used by an existing program</td></tr><tr><td>Architecture comparison</td><td>Which implemented model runs</td></tr><tr><td>Agent-directed research</td><td>The model, loss, or training program itself</td></tr></tbody></table><div class="bottom-note">We will do all three. The first two do not require a research agent.</div>


<!--
Changing learning rate is a hyperparameter search. Choosing MLP or CNN compares existing architectures. Later, the research agent will write different model or training code. These are different kinds of changes, and we’ll record which one we made.
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

<div class="bottom-note">The notebook contains the full implementation and reuses already-completed runs.</div>


<!--
W&B Sweeps assigns each configuration to a run. Our training function does the fitting and saves its outputs. This is a shortened excerpt; the notebook contains the entity, project, and complete configuration setup.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:10</div>

# Compare forecast error and training time

<a class="sweep-crop" href="/images/ux-v020-solar-sweep.png" target="_blank" aria-label="Open the full native W&B Sweep capture"><img src="/images/ux-v020-solar-sweep.png" alt="Actual W&B Sweep charts showing six validation errors, negative skill relative to persistence, and runtime"></a><p class="aside">All six recorded forecasts are worse than persistence. A lower error among them does not change that.</p><div class="image-caption"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pr1xsoaw">Open the actual Sweep ↗</a> · <a href="/images/ux-v020-solar-sweep.png" target="_blank">Full capture ↗</a></div>


<!--
This is the recorded six-run Sweep. Find validation error, performance relative to persistence, and training time. All six models performed worse than persistence here. The lowest error among them does not make it a successful forecast.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:11</div>

# Check whether the models learned enough

<p class="big">Open the loss curve and prediction plot before choosing a model.</p><div class="warning">In our recorded GOES runs, 60 training steps left the models undertrained. Copying the latest reading gave lower error.</div><div class="bottom-note">Testing a longer training budget would be a separate comparison.</div>


<!--
In the recorded runs, the loss curves and forecasts showed the models were still undertrained after sixty steps. Compare that with the forecasts you just produced. A longer, equal training budget for all models would be a separate experiment.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:15–1:30 · YOUR TURN</div>

<a class="answer-link" href="/78">Worked answer → 78</a>

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

# Look at the forecast beside the observed future

<img class="solar-photo" src="/images/solar-validation.png" alt="Recorded image input, prediction, future observation, and error"><div class="image-caption">Recorded rehearsal image forecast. The notebook shows your own prediction after training.</div>


<!--
Read this recorded example from input to prediction, observed future, and error map. Ask someone to point to a region that changed. After training, the notebook will show the same view for their own result.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:46</div>

# Have the network predict the whole image

```python
class ImagePredictor(nn.Module):
    def forward(self, x):
        return self.net(x)
```

<p class="big">The convolutional model must produce the whole image.</p><div class="bottom-note">Two input channels: the earlier and current images. One output channel: the forecast.</div>


<!--
The first model takes two image channels and predicts a whole future image. Its output has one channel. We keep the network small enough to compare on CPU during the workshop.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:48</div>

# Add a learned correction to the current image

```python
class ImagePredictor(nn.Module):
    def forward(self, x):
        correction = self.net(x)
        return x[:, 1:2] + correction
```

<p class="big">The current image supplies a starting point. The network learns the change.</p>


<!--
The residual model adds its learned correction to the current image. If the correction is zero, its forecast is exactly persistence. Participants implement this branch in the same forward method.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">1:50</div>

# Measure error inside the solar disk

```python
error = abs(prediction - target)
masked_error = error * disk_mask
score = mean(masked_error.sum_per_image() / disk_mask.sum_per_image())
```

<div class="bottom-note">A change outside the mask must not affect the score. Test that explicitly.</div>


<!--
Compute absolute error only inside the fixed solar-disk mask. Sum and divide within each image, then average the image errors. An edit outside the mask should not change this score.
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

# Compare the two forecasts on the same case

<a class="model-crop" href="/images/ux-v020-solar-models.png" target="_blank" aria-label="Open the complete validation model comparison"><img src="/images/ux-v020-solar-models.png" alt="Actual convolutional and residual forecasts on the same validation case, with observed future and error images"></a><div class="image-caption">Recorded validation case: convolution above, residual below. <a href="/images/ux-v020-solar-models.png" target="_blank">Open full comparison and evidence links ↗</a></div>


<!--
These two recorded rows use the same input and target times. The convolutional forecast is above; the residual forecast is below. Compare the images and error maps, then look at the validation scores. The final dates have not been used to select either model.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">1:55–2:15 · YOUR TURN</div>

<a class="answer-link" href="/79">Worked answer → 79</a>

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

# The research agent writes code; the forecast model trains

<table class="clean-table"><tbody><tr><th></th><th>Research agent</th><th>Forecasting model</th></tr><tr><td>Job</td><td>Propose code edits</td><td>Predict solar observations</td></tr><tr><td>Weights</td><td>Fixed throughout</td><td>Trained on training dates</td></tr><tr><td>Changed by this loop</td><td>Its evidence and task context</td><td>Source, loss, training code, trained weights</td></tr></tbody></table><div class="bottom-note">No post-training of the research agent occurs in this workshop.</div>


<!--
There are two different models here. GLM writes research proposals and its weights stay fixed. The small forecasting networks train their weights for each candidate. The research agent changes the program that performs that training.
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

# Find the validation evidence the agent read

<div class="native-columns"><a href="/images/ux-v020-solar-lens-current.png" target="_blank" aria-label="Open full-size Agent Lens capture"><img src="/images/ux-v020-solar-lens-current.png" alt="Recorded Agent Lens read_validation_evidence span with inputs and outputs"></a><div><h2>Find <code>read_validation_evidence</code>.</h2><p>Open the tool output and find the settings and validation results.</p><h2>Then inspect the proposal.</h2><p>Read the returned code, then open the training result for that candidate.</p><p class="aside"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4/spans">Open the recorded conversation ↗</a><br><a href="/images/ux-v020-solar-lens-current.png" target="_blank">Open full-size capture ↗</a></p></div></div><div class="bottom-note">Recorded on November 13. Open your own conversation after sending the request.</div>


<!--
In this recorded conversation, select read_validation_evidence. Its output includes the active configuration and validation evidence. Then inspect the proposed code and follow its training result. The full-size capture link helps when the native view requires sign-in.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: exercise
---

<div class="kicker">2:25–2:40 · YOUR TURN</div>

<a class="answer-link" href="/81">Worked answer → 81</a>

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

# Read the proposed change before running it

<a class="diff-crop" href="/images/ux-v020-solar-diff.png" target="_blank" aria-label="Open the full proposed-change capture"><img src="/images/ux-v020-solar-diff.png" alt="Actual candidate diff changes squared training error to absolute error and requires review before the probe"></a><div class="image-caption">Recorded proposal: <code>.square()</code> became <code>.abs()</code>. The training result will show whether it helped. <a href="/images/ux-v020-solar-diff.png" target="_blank">Full capture ↗</a></div>


<!--
This recorded candidate changes squared training loss to absolute loss. Ask what that might change during training, then inspect the test result. Reading the diff tells us what was proposed; it does not tell us whether the forecast improved.
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

<a class="answer-link" href="/82">Worked answer → 82</a>

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

# Stop editing before the final comparison

<div class="step-path"><div><h2>Persistence</h2><p>Copy the latest observed image.</p></div><div><h2>Manual selection</h2><p>The model selected using validation error.</p></div><div><h2>Agent selection</h2><p>The code and weights selected after round two.</p></div></div><div class="bottom-note">Keep these versions fixed while testing the reserved dates.</div>


<!--
Select the versions before looking at the final dates. The image comparison includes persistence, the manually selected model, and the agent-selected model. Keep the saved code and weights fixed while evaluating them.
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

<a class="answer-link" href="/83">Worked answer → 83</a>

# Test the selected models on reserved dates

<div class="task">Open <strong>7 · Final evaluation</strong>.</div><ol class="exercise-controls"><li>Click <strong>Freeze versions and evaluate reserved dates</strong>.</li><li>Choose one timestamp. Compare each image forecast with the same observed future.</li><li>Open one result’s training record and Agent Lens call. Compare the image scores separately from the GOES scores.</li></ol><div class="done">Check your work: Explain a difference between two forecasts using their images and scores.</div>


<!--
Allow twenty minutes. Have participants choose one timestamp and explain a difference in the forecasts using the error images. Keep the GOES and image tables separate. Nearby windows overlap, so they are not independent studies.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:45 · RECORDED REHEARSAL</div>

# In this rehearsal, image error fell 10.15%

<div class="measured-grid"><div><div class="measured-gain">10.15%</div><p>less error than the manually selected model</p><p class="aside">Agent edits: zero-initialize the residual head, then use absolute training loss.</p></div><table class="clean-table"><tbody><tr><th>Frozen version</th><th>Masked MAE ↓</th></tr><tr><td>Persistence</td><td>0.125762</td></tr><tr><td>Manual residual model</td><td>0.122442</td></tr><tr><td>Agent-selected code</td><td>0.110011</td></tr></tbody></table></div><p class="aside">Actual AIA 171 Å observations. 199 overlapping windows; February 13–14, 2014; one seed. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==">Open the recorded comparison ↗</a></p><div class="bottom-note">A measured result from this rehearsal, not a promised outcome for your edits.</div>


<!--
The selected agent code combined the zero-initialized residual head from round one with absolute training loss from round two. Its final masked MAE was 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The 10.15% is a relative reduction in error versus manual. This is one seed and 199 overlapping windows across two reserved days, not evidence of reliable solar forecasting across other periods.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:46 · RECORDED REHEARSAL</div>

# Compare the saved forecasts at the same time

<a class="final-crop" href="/images/ux-v020-solar-final.png" target="_blank" aria-label="Open the complete final notebook comparison"><img src="/images/ux-v020-solar-final.png" alt="Actual notebook comparing manual and agent forecasts at the same reserved timestamp, with observed future and error images"></a><div class="image-caption">Same input and future timestamp. Manual above, agent-selected below. <a href="/images/ux-v020-solar-final.png" target="_blank">Full notebook comparison ↗</a></div>


<!--
These are saved forecasts for the same final timestamp. Compare the manual row with the agent-selected row, including the error images. The full screenshot also contains the score tables. It is the notebook comparison from the rehearsal.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:47 · RECORDED REHEARSAL</div>

# The recorded GOES model lost to persistence

<img class="solar-photo" src="/images/goes-final.png" alt="Recorded observed flux and undertrained forecast"><div class="image-caption">Final log-flux MAE: selected model 2.469; persistence 0.193. The training budget was 60 steps.</div>


<!--
The GOES model’s final log-flux MAE was 2.469; persistence scored 0.193. Its learning curve showed it was still undertrained after sixty steps. Keep this failure beside the image result. It does not establish that MLPs or CNNs cannot forecast solar measurements.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:48</div>

# Compare forecast quality, time, and cost

<table class="clean-table"><tbody><tr><th>What to ask</th><th>What to inspect</th></tr><tr><td>Did the forecast error fall?</td><td>The same final dates and scoring rule for every model</td></tr><tr><td>How much work did that take?</td><td>Training time and inference cost, including failed attempts</td></tr><tr><td>Did a run fail before producing a forecast?</td><td>The error in its training call or agent trace</td></tr></tbody></table>


<!--
Ask whether forecast error fell, how much training and inference it took, and whether any executions failed. These answer different questions. A run can finish cleanly and still make poor predictions.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">3:49</div>

# Open the files behind one result

<div class="step-path"><div><h2>Run</h2><p>Settings, metric, loss history.</p></div><div><h2>Artifact</h2><p>Source, data, weights, predictions.</p></div><div><h2>Trace</h2><p>Agent requests, edits, tests, decisions.</p></div></div><div class="bottom-note">The Report explains what changed and links to those records.</div>


<!--
Open a result’s run for settings and loss history, its Artifact for files, and its Agent Lens conversation for the agent’s actions. These links let a teammate inspect the result instead of relying on our summary.
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

# Choose the next experiment from what you observed

<p class="big">Pick one error you saw and propose a change that might reduce it.</p><p>Say which code you’d change, which comparison you’d run, and what result would make you keep the previous version.</p><div class="bottom-note">For the next study, choose new final-test dates before making more changes.</div>


<!--
Ask for one next experiment based on an error someone inspected. What code would change, what would stay fixed, and what would make them keep the old version? Use new final-test dates for another round of model development.
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


<div class="source-link"><a href="/10">Return to Connect and inspect your first tool call →</a></div>

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
<div class="source-link"><a href="/46">Return to Implement and compare the image predictors →</a></div>

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
<div class="source-link"><a href="/53">Return to Choose the evidence for the research agent →</a></div>

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
<div class="source-link"><a href="/61">Return to Test the selected code, then begin round two →</a></div>

<!--
Pass candidate['source'] to training, along with the shared configuration. Passing the parent source here would train the old program while the interface appeared to test a new proposal. Open the saved candidate.py if the result looks suspicious.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Use the saved model without training it again

<p class="big">Load each selected model’s saved weights and predict the reserved dates.</p><p>Compare the three image forecasts at one timestamp. The input images and observed future should match across all three rows.</p><div class="bottom-note">Persistence copies the current image and needs no trained weights.</div>
<div class="source-link"><a href="/66">Return to Test the selected models on reserved dates →</a></div>

<!--
The selected weights are already trained. Load them and predict the final inputs. Compare the same target timestamps across all versions; persistence uses the current image directly.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 1: two changes, two measured outcomes

<table class="clean-table"><tbody><tr><th>Source</th><th>Validation error ↓</th></tr><tr><td>Manual residual model</td><td>0.122116</td></tr><tr><td>A · replace squared loss with absolute loss</td><td>0.120553</td></tr><tr><td>B · initialize the residual head at zero</td><td>0.111434</td></tr></tbody></table><p>The composition selected B. Its separate test reproduced 0.111434.</p><p class="aside"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4">Open the actual proposals and evidence ↗</a></p>


<!--
In our November 13 rehearsal, Candidate A changed the loss to absolute error. Candidate B initialized the residual head at zero and had lower validation error. The composition kept B and its separate test reproduced the same score. These models shared the image data, seed, and forty-step training configuration.
Source notes and recorded evidence: notes/sources.md.
-->

---
class: answer-code
---

<div class="kicker">RECORDED REHEARSAL</div>

# Initialize the correction at zero

```python
if architecture == 'residual':
    nn.init.zeros_(self.net[4].weight)
    nn.init.zeros_(self.net[4].bias)

# The residual forward pass remains:
return prediction + x[:, 1:2]
```

<div class="bottom-note">Zero initial correction → the initial forecast is the current image.</div>


<!--
Zero weights and bias in the last convolution make the initial correction zero. The residual model therefore starts by copying the present image, then learns a correction during training. This is the actual first-round edit that was selected in the recorded run.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 2 also tested the unchanged version

<table class="clean-table"><tbody><tr><th>Source</th><th>Validation error ↓</th></tr><tr><td>Adopted zero-init model</td><td>0.111434</td></tr><tr><td>A · add absolute loss to that source</td><td>0.110916</td></tr><tr><td>B · KEEP the zero-init source unchanged</td><td>0.111434</td></tr></tbody></table><p>The unchanged version reproduced its earlier error. The tested composition selected A.</p><div class="bottom-note">KEEP ran the same code again so we could compare it with Candidate A.</div>


<!--
Round two started from the zero-initialized model. Candidate A added absolute training loss. Candidate B kept the source unchanged and reproduced its error. The tested composition selected A. This small validation difference comes from one seed, so it does not establish repeatability.
Source notes and recorded evidence: notes/sources.md.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Open the recorded research conversation

<p class="big"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4">Open the proposal and its recorded tool activity ↗</a></p><p>Find the active configuration, the requested edit, and the returned candidate code. Compare the proposal with the tested source.</p><p class="aside"><a href="https://ash0ts.github.io/forge-workshop-kit/solar/recorded-study.json">Download the recorded source, decisions, scores, and evidence links ↗</a></p><div class="bottom-note">Agent Lens may require sign-in. The source and saved decisions are also in the downloadable evidence.</div>


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

<p class="big"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Copy the Solar notebook ↗</a></p><p><a href="https://github.com/ash0ts/forge-workshop-kit">Source, setup, dataset, and facilitator guide ↗</a></p><p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==">Recorded rehearsal Report ↗</a></p><div class="bottom-note">Keep your notebook, code edits, and checkpoints. The facilitator needs no control over your runtime.</div>


<!--
Participants keep their notebook and project. Use these links to continue the exercises, inspect the source, or revisit the recorded example. There is no facilitator gateway to renew.
Source notes and recorded evidence: notes/sources.md.
-->
