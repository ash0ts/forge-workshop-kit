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
Opening, 30 seconds. This is a computational research lab studying solar observations. The pixel room is an illustration, not a live instrument feed. The notebook contains real public solar observations and actual training code. We will first build the experiment, then give a fixed-model agent a limited role in changing it.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:01</div>

# Your team has a promising result.

<div class="quote">“The new model looks better.”<small>THE RESEARCH UPDATE · FICTIONAL SCENE</small></div><div class="two-col" style="margin-top:40px"><div><h2>You ask which run.</h2><p>Someone shares a screenshot.</p></div><div><h2>You ask which code.</h2><p>Someone shares a notebook called final.</p></div></div><div class="bottom-note">There are four notebooks called final.</div>


<!--
Tell the fictional scene briefly. It establishes the familiar problem of a score without the program, data, and settings that produced it. Do not imply this anecdote happened in the rehearsal.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:02</div>

# The Sun has supplied the data.

<p class="big">Predict what we will observe next from what we have observed so far.</p><div class="step-path"><div><h2>First: measurements</h2><p>Predict X-ray flux 30 minutes ahead.</p></div><div><h2>Then: images</h2><p>Predict a solar image one hour ahead.</p></div></div><div class="bottom-note">A small teaching experiment. No operational space-weather claims.</div>


<!--
Define forecasting before introducing the agent. SunPy gives astronomy-aware tools for acquiring and inspecting observations. This is not flare classification or a reproduction of a foundation-model benchmark.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:03</div>

# Can an agent improve the research code?

<div class="quote">“Once the experiment works, could an agent improve it?”<small>THE NEXT LAB QUESTION</small></div><ResearchMap :level="4" />


<!--
Move from running a fixed experiment to testing an agent-written change. The answer is a tested workflow, not a promise of better performance. Research-agent weights stay fixed; the small forecasting models are trained.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:04</div>

# What you will build

<div class="step-path"><div><h2>Forecast</h2><p>Data, persistence, metrics.</p></div><div><h2>Track</h2><p>Code, settings, trained weights.</p></div><div><h2>Improve</h2><p>Review and test agent-written edits.</p></div><div><h2>Evaluate</h2><p>Freeze, compare, reproduce.</p></div></div><div class="bottom-note">Your own notebook and project. The facilitator can read the progress you publish.</div>


<!--
Show the work in order. Participants edit visible Python. Every execution is explicit. A higher score is optional; an explainable experiment is the goal.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:05</div>

# Your notebook, in your project

<div class="copy-layout"><div class="template-qr"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view"><img src="/images/solar-template-qr.svg" alt="QR code opening the Solar workshop template"></a><p><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Open the Solar template ↗</a></p></div><ol><li>Open the template.</li><li>Choose <strong>Copy to project</strong> and select your writable project.</li><li>Open the copy in <strong>Edit</strong>. Choose <strong>Run all stale cells</strong> once.</li><li>In <strong>Connect</strong>, check your project. Exercise run buttons stay unpressed.</li></ol></div><div class="bottom-note">Hosted Forge supplies authentication. Your account supplies notebook compute and inference access.</div>


<!--
Use the template, not a facilitator rehearsal notebook. A public project is a teaching default, not an entitlement grant. Do not put private data in it. No host-issued token or gateway URL is required. Run all stale cells initializes the controls. It does not press exercise buttons or start training or paid inference. The first access check is also free.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:06</div>

# The same notebook on your laptop

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen
uv run wandb login --verify
uv run marimo edit notebooks/solar_autoresearch.py
```

<p class="aside">In Connect, enter <code>your-entity/your-project</code>. Keep the terminal open.</p><div class="bottom-note">Install Git and uv first. Hosted participants skip these commands.</div>


<!--
Local alternative. Dependencies are locked. Authenticate at the terminal, never in a shared code cell. There is no local workshop service to launch. Notebook CPU compute and direct provider billing belong to the participant. The configured inference allowance defaults to $8 and is adjustable.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:06</div>

# Know what this notebook will run

<table class="clean-table"><tbody><tr><th>Setting</th><th>This workshop</th></tr><tr><td>Project and credentials</td><td>Your own Forge project and account</td></tr><tr><td>Training compute</td><td>Notebook CPU; billed separately if hosted</td></tr><tr><td>Research agent</td><td><code>zai-org/GLM-5.3-Flash</code>, fixed</td></tr><tr><td>Inference allowance</td><td>$8 by default; adjustable in Connect</td></tr><tr><td>Execution</td><td>Explicit run buttons; saved work restores</td></tr></tbody></table><div class="bottom-note">A higher allowance permits more calls. It does not grant account access or include compute.</div>


<!--
The provider records requested and returned model IDs. Research calls use temperature 0.2, JSON output, and a maximum 16,384 output tokens. The model does not silently change when unavailable. Opening, restoring, or editing does not run training or inference.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:07</div>

# The first thing you publish is a trace

```python
with tracing.Conversation(conversation_id=execution_id):
    with tracing.Turn(agent_name="researcher", messages=mission):
        with tracing.Tool(
            name="inspect_training_environment",
            arguments={}, result=observed_environment,
        ):
            ...
```

<div class="bottom-note">The actual tool result, timestamps, and error belong in the span.</div>


<!--
Illustrative excerpt of the pinned Forge SDK scope hierarchy; exact instrument_tool code is in the notebook. Parent conversation and turn scopes are supplied by export_trace, while learners write the tool scope. A successful export call is not the same as verified stored-span readback.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">0:08–0:15 · YOUR TURN</div>

<a class="answer-link" href="/75">Worked answer → 75</a>

# Connect and find your first span

<div class="task">Open <strong>1 · Connect</strong>.</div><ol class="exercise-controls"><li>Click <strong>Connect and restore my work</strong>. Check the project and inference allowance.</li><li>In the visible <code>instrument_tool</code> editor, add <code>workshop.exercise</code>. Click <strong>Check my tracing code</strong>.</li><li>Click <strong>Send my first Agent Lens trace</strong>. Open the conversation and find your attribute, arguments, and result.</li></ol><div class="done">Done when: you can point to your own stored tool span in Agent Lens.</div>


<!--
Allow 7 minutes. Help users distinguish project permission errors from inference access. The setup trace is tool-only and makes no provider call.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:15</div>

# Your work stays in your project

<div class="native-columns"><a href="/images/ux-v021-solar-setup.png" target="_blank"><img src="/images/ux-v021-solar-setup.png" alt="Revised notebook showing the participant project, allowance and guided exercise navigation"></a><div><h2>Check your project.</h2><p>The example uses the rehearsal project. Your copy must name your own.</p><h2>Check your allowance.</h2><p>Inference and notebook compute are separate.</p><p class="aside"><a href="/images/ux-v021-solar-setup.png" target="_blank">Open full capture ↗</a></p></div></div><div class="bottom-note">Actual revised notebook after restoring saved work.</div>


<!--
Captured from the revised notebook. Project, tool location, allowance and current progress stay together. The screenshot is a restored rehearsal, not an empty new workspace. Do not ask attendees to enter the facilitator project shown here.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:15</div>

# The trace comes from the code you write

<a class="instrumentation-crop" href="/images/ux-v020-solar-instrumentation.png" target="_blank" aria-label="Open the full tracing exercise"><img src="/images/ux-v020-solar-instrumentation.png" alt="Actual editable instrument_tool function with the attribute exercise and free tracing check"></a><p class="aside">Add the attribute inside the tool scope. This writer also instruments your later training calls.</p><div class="image-caption">Recorded rehearsal: the attribute is added and the local check passes. <a href="/images/ux-v020-solar-instrumentation.png" target="_blank">Open full capture ↗</a></div>


<!--
Actual completed setup editor from the revised-notebook rehearsal. The local check is free and exports nothing. The separate trace button exports an actual operation; stored span 3836f2a676d91bdf contains the attribute. Later training uses the same writer.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:15</div>

# The measurement forecast

<ForecastWindow mode="goes" /><div class="bottom-note">Predict log10 XRS-B flux. A forecast window includes observations, timestamps, and a future target.</div>


<!--
GOES-15 one-minute X-ray measurements. The task is a 60-minute history predicting flux 30 minutes ahead. Explain log scaling without suggesting these models are calibrated operational forecasts.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:17</div>

# Dates are part of the experiment

<ForecastWindow :split="true" /><div class="bottom-note">February 2014, UTC. Fit normalization on training data only.</div>


<!--
The splits are dates, not random neighboring rows. All source observations and the target must fit inside one partition. Otherwise near-duplicate solar states can leak from training into evaluation.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:19</div>

# A missing observation is a gap

<div class="two-col"><div><h2>What the archive returned</h2><p>GOES February 8 is absent.</p><p>Incomplete forecast windows are excluded.</p></div><div><h2>What the loader must preserve</h2><p>Observation time and quality flags.</p><p>The split and the reason for each exclusion.</p></div></div><div class="bottom-note">Do not replace an absent flux measurement with zero.</div>


<!--
Actual source coverage from dataset manifest. The image archive and GOES have different exclusions. Do not treat a missing measurement as evidence that solar flux reached zero.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:20</div>

# SunPy gives the observations context

```python
from sunpy.map import Map

observation = Map(dataset_path / "sample-aia.fits")
print(observation.date)
print(observation.wavelength)
print(observation.unit)
```

<div class="bottom-note">Inspect a real FITS file. Train from the prepared, checksum-verified arrays.</div>


<!--
The package is approximately 26.1 MB. Prepared arrays keep downloads small; a representative FITS file retains astronomy metadata. Acquisition code and manifest preserve source URLs, checksums, preprocessing, and exclusions. Credit NOAA, NASA/SDO, AIA, JSOC, and SunPy.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">0:21–0:27 · YOUR TURN</div>

# Inspect the observations before training

<div class="task">Open <strong>2 · Solar data</strong>.</div><ol class="exercise-controls"><li>Click <strong>Load the solar dataset</strong>.</li><li>Find an observation time, the image wavelength, and the dataset version.</li><li>Explain why a forecast window that crosses February 10–11 must be excluded.</li></ol><div class="done">Done when: you can identify the inputs, target, units, and partition of a forecast.</div>


<!--
Use 6 minutes. No model fit belongs in this exercise. The archive was prepared before class, so students inspect versioned data rather than waiting for thousands of downloads.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:27</div>

# The first model predicts no change

```python
def persistence_forecast(split):
    # Latest observed value becomes the future prediction.
    ...
```

<p class="big">A difficult baseline to beat can still be a one-line function.</p><div class="bottom-note">The baseline uses the current observation, never the future target.</div>


<!--
Persistence is meaningful for correlated solar observations. A model must beat this simple prediction before complexity has demonstrated value. Do not claim persistence will win every task.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:29</div>

# A forecast needs a defined error

```python
error = mean(abs(predicted_log_flux - observed_log_flux))
```

<div class="two-col" style="margin-top:35px"><div><h2>Lower is better</h2><p>The same target, transform, and units apply to every run.</p></div><div><h2>The average is not the plot</h2><p>Inspect the times where the forecast misses.</p></div></div><div class="bottom-note">The observed future supplies the target. Numeric forecast quality uses a fixed metric, not an LLM judge.</div>


<!--
Primary measurement metric is log-flux MAE in log10 W/m² units. Don’t average this number with image error. A trend chart and individual errors provide information the mean omits.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">0:30–0:40 · YOUR TURN</div>

<a class="answer-link" href="/76">Worked answer → 76</a>

# Write and test persistence

<div class="task">Open <strong>3 · Persistence</strong>.</div><ol class="exercise-controls"><li>Implement <code>persistence_forecast(split)</code>.</li><li>Click <strong>Check my persistence function</strong>, then <strong>Run my persistence baseline</strong>.</li><li>Inspect the observed and predicted curves. Identify one interval where copying the present misses the future.</li></ol><div class="done">Done when: your function returns the current observation and your saved baseline has a metric and a plot.</div>


<!--
Allow 10 minutes. Local checks are free. Do not reveal the answer until students have attempted it.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:40</div>

# A score alone cannot reproduce a run

<p class="big">The validation error is lower.</p><div class="step-path"><div><h2>Which source?</h2><p>A loss changed yesterday.</p></div><div><h2>Which data?</h2><p>A gap changed the windows.</p></div><div><h2>Which settings?</h2><p>One run trained longer.</p></div></div><div class="bottom-note">Each is a different experiment, even when the notebook has the same filename.</div>


<!--
These are possible causes, not claims about a hidden failure in the rehearsal. Ask what information a teammate needs to rerun a result.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:41</div>

# These scores need their configurations

<RunInspector />


<!--
Interactive illustration using two actual recorded rehearsal rows. Ask what changed before revealing the active configuration. Both runs use the same source and training budget; learning rate differs. Reproduction also requires data and executed source. No training or inference occurs in this widget.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:42</div>

# The learning rate changed. The budget did not.

<RunInspector :revealed="true" />


<!--
Static reveal for the PDF and the live teaching sequence. The two actual runs share data, source, seed, steps and batch size. At this short budget, the lower error alone does not establish a better converged architecture.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:42</div>

# The program produces the forecast

<ResearchMap :level="0" />


<!--
First build of the shared research diagram. Forecast model, observation and prediction stay in place throughout the progression.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:43</div>

# The executed code belongs to the record

<ResearchMap :level="1" /><div class="bottom-note">Saving a notebook and saving the code that executed are different operations.</div>


<!--
Attach exact source. The model and training functions are editable. The stage receipt fingerprints source and settings.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:44</div>

# Keep the measurement fixed

<ResearchMap :level="2" /><div class="bottom-note">The model can change. The target, partition, and primary scoring rule stay fixed.</div>


<!--
The primary scorer is supplied by the experiment. Learner metrics are checked against it. A revised metric creates a different question and must not retroactively improve old scores.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:45</div>

# Save the work needed to explain the score

<ResearchMap :level="3" /><div class="bottom-note">W&B runs show metrics. Artifacts preserve data, source, weights, and predictions.</div>


<!--
No generic product pitch. Runs make settings and loss history comparable; artifacts preserve files for restoration and reproduction.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:47</div>

# Visible training, durable saving

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

<div class="bottom-note">The notebook owns the training code. The session saves completed work.</div>


<!--
Conceptual public API example. In the actual notebook run_training invokes training.train and saves weights/predictions. A completed receipt must be restored rather than repeating work on refresh.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">0:49</div>

# A restart should restore, not rerun

<div class="step-path"><div><h2>Local receipt</h2><p>Which stage finished and which files it produced.</p></div><div><h2>Checkpoint artifact</h2><p>A versioned copy in the participant’s project.</p></div><div><h2>New runtime</h2><p>Restore saved results before offering the next action.</p></div></div><div class="bottom-note">Publication retry uploads saved work. It does not launch training again.</div>


<!--
Use the actual restoration behavior. An upload failure should preserve local results and clearly identify what is unpublished. Monitoring is read-only and cannot gate participant progress.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">0:50–1:05 · YOUR TURN</div>

<a class="answer-link" href="/77">Worked answer → 77</a>

# Make the result reproducible

<div class="task">Open <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Implement <code>training_loss</code> and <code>my_flux_mae</code>, then run <strong>Check my measurement code</strong>.</li><li>Inspect <code>run_training</code>. Find where it records source, data, settings, and outputs.</li><li>Open a saved run and its artifact. Identify the fields you would need after deleting the runtime.</li></ol><div class="done">Done when: you can match a metric to its source fingerprint and dataset version.</div>


<!--
15 minutes. Students should change the metric, then see a local wrong-value check fail and fix it. Do not make this a form-only reflection.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:05</div>

# Settings, architectures, and new code

<table class="clean-table"><tbody><tr><th>Operation</th><th>What changes</th></tr><tr><td>Hyperparameter search</td><td>Values used by an existing program</td></tr><tr><td>Architecture comparison</td><td>Which implemented model runs</td></tr><tr><td>Agent-directed research</td><td>The model, loss, or training program itself</td></tr></tbody></table><div class="bottom-note">We will do all three. The first two do not require a research agent.</div>


<!--
This distinction is the spine of the workshop. Searching learning rates is useful, but it is not an agent inventing new code.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:07</div>

# Six controlled starting configurations

<table class="clean-table"><tbody><tr><th>Architecture</th><th>Widths</th><th>Learning rates</th><th>Training budget</th></tr><tr><td>Small MLP</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr><tr><td>Temporal CNN</td><td>16, 32, 16</td><td>.001, .001, .003</td><td>60 steps each</td></tr></tbody></table><div class="bottom-note">Seed 17. Batch size 32. The notebook records the active values.</div>


<!--
These are the fixed rehearsal settings from the notebook. Short budget is deliberate for class, not a claim of tuning quality. Settings remain editable and must be recorded if changed.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:09</div>

# W&B Sweeps supplies the configurations

```python
sweep_id = wandb.sweep(sweep_config, entity=entity, project=project)

def trial():
    with wandb.init() as run:
        result = run_training(config_for(run.config.trial))
        run.log(result["metrics"])

wandb.agent(sweep_id, function=trial, count=6)
```

<div class="bottom-note">The notebook shows the full implementation. Completed stage receipts prevent duplicate training.</div>


<!--
Teaching excerpt, not a standalone complete cell. The actual notebook specifies entity and project on both calls. The sweep and stage journal have different jobs: assignment versus durable execution reuse.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:10</div>

# Compare error, baseline skill, and runtime

<a class="sweep-crop" href="/images/ux-v020-solar-sweep.png" target="_blank" aria-label="Open the full native W&B Sweep capture"><img src="/images/ux-v020-solar-sweep.png" alt="Actual W&B Sweep charts showing six validation errors, negative skill relative to persistence, and runtime"></a><p class="aside">All six recorded forecasts are worse than persistence. A lower error among them does not change that.</p><div class="image-caption"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pr1xsoaw">Open the actual Sweep ↗</a> · <a href="/images/ux-v020-solar-sweep.png" target="_blank">Full capture ↗</a></div>


<!--
Fresh revised-notebook rehearsal: native Sweep pr1xsoaw. This is a crop of the actual first chart row; the full image preserves the Forge workspace context and ingestion-delay notice. The short training budget produced negative skill versus persistence. The charts retain all six runs; they do not demonstrate an architecture winner.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:11</div>

# A smaller error can still be a poor forecast

<p class="big">Before ranking architectures, inspect whether training had time to learn the target scale.</p><div class="warning">In the recorded rehearsal, the short GOES models remained undertrained. Persistence won.</div><div class="bottom-note">Keep the failed comparison. A longer uniform training budget is a new experiment.</div>


<!--
Do not preannounce learners’ results. This is a recorded example and remains labeled. The six short rehearsal models did not justify an architecture claim.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">1:15–1:30 · YOUR TURN</div>

<a class="answer-link" href="/78">Worked answer → 78</a>

# Run the same search and inspect a loss curve

<div class="task">Stay in <strong>4 · Track and search</strong>.</div><ol class="exercise-controls"><li>Click <strong>Run six tracked configurations</strong>.</li><li>Open the Sweep and compare validation error with runtime.</li><li>Open one poor result. Inspect its training curve and prediction rather than deleting it.</li></ol><div class="done">Done when: all six attempts are accounted for and you can explain one comparison.</div>


<!--
15 minutes. Request a prediction before students click. If provider or publication is unavailable, training can still have saved local results. Do not rerun inference to repair a link.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:30–1:40</div>

# The experiments can wait ten minutes.

<p class="big">Save the checkpoint.<br>Leave the notebook open.<br>Give your own optimizer a break.</p><div class="bottom-note">We resume at 1:40 with image predictions.</div>


<!--
Ten-minute break. No new background experiments are required. Confirm checkpoint status before leaving.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:40</div>

# The target is now a future image

<ForecastWindow mode="images" /><div class="bottom-note">AIA 171 Å. Prepared 64 × 64 arrays. One-hour forecasting.</div>


<!--
The image task receives frames at t−60 and t and predicts t+60. The same chronological split rules apply. Larger images are an optional separate compute experiment.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:42</div>

# Reuse the experiment record

<ResearchMap :level="3" /><div class="bottom-note">The input and prediction changed shape. Source, settings, weights, and evidence still belong together. The image score uses normalized log1p intensity.</div>


<!--
Do not reintroduce every product. Reuse the same record structure to make the new task less cognitively expensive.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:44</div>

# A forecast produces an image you can inspect

<img class="solar-photo" src="/images/solar-validation.png" alt="Recorded image input, prediction, future observation, and error"><div class="image-caption">Recorded rehearsal image forecast. The notebook shows your own prediction after training.</div>


<!--
Source evidence/solar-validation.png. Use it to identify which panel is input, prediction, target, error. It is not the participant’s current result.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:46</div>

# Predict the full future image

```python
class ImagePredictor(nn.Module):
    def forward(self, x):
        return self.net(x)
```

<p class="big">The convolutional model must produce the whole image.</p><div class="bottom-note">Two input channels: the earlier and current images. One output channel: the forecast.</div>


<!--
Keep technical detail concrete. This is a tiny model for CPU class time, not a solar foundation model.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:48</div>

# Or predict a correction to the present

```python
class ImagePredictor(nn.Module):
    def forward(self, x):
        correction = self.net(x)
        return x[:, 1:2] + correction
```

<p class="big">The current image supplies a starting point. The network learns the change.</p>


<!--
The residual path makes persistence accessible when correction is zero. It does not guarantee better forecasting. Participants implement the branch in the actual code editor.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:50</div>

# Score the solar disk

```python
error = abs(prediction - target)
masked_error = error * disk_mask
score = mean(masked_error.sum_per_image() / disk_mask.sum_per_image())
```

<div class="bottom-note">A change outside the mask must not affect the score. Test that explicitly.</div>


<!--
Pseudocode for disk-masked MAE. The real answer sums axes 1,2,3 per example before averaging. A whole-image average can hide a scientifically important small region.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:52</div>

# Training loss and final metric have different jobs

<table class="clean-table"><tbody><tr><th>Training loss</th><th>Primary evaluation metric</th></tr><tr><td>Supplies gradients while fitting weights</td><td>Measures predictions for comparison</td></tr><tr><td>Candidate code can change it</td><td>Fixed outside candidate code</td></tr><tr><td>The starting implementation uses squared error</td><td>The image comparison uses masked absolute error</td></tr></tbody></table>


<!--
Explain why an agent might test L1 without moving the goalposts. Changing training loss is an allowed edit; changing the independent scoring metric is not.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">1:54</div>

# Compare what each model actually predicts

<a class="model-crop" href="/images/ux-v020-solar-models.png" target="_blank" aria-label="Open the complete validation model comparison"><img src="/images/ux-v020-solar-models.png" alt="Actual convolutional and residual forecasts on the same validation case, with observed future and error images"></a><div class="image-caption">Recorded validation case: convolution above, residual below. <a href="/images/ux-v020-solar-models.png" target="_blank">Open full comparison and evidence links ↗</a></div>


<!--
Fresh revised-notebook rehearsal. Both rows share the same input and target timestamps. The full capture contains the native notebook score table, saved model predictions, and direct Agent Lens, run and artifact links. This is a validation example; final dates are still reserved.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">1:55–2:15 · YOUR TURN</div>

<a class="answer-link" href="/79">Worked answer → 79</a>

# Implement and compare the image predictors

<div class="task">Open <strong>5 · Solar images</strong>.</div><ol class="exercise-controls"><li>Edit <code>ImagePredictor.forward</code>, <code>training_loss</code>, and <code>my_image_mae</code>.</li><li>Click <strong>Check my image code</strong>. A +1 error should score 1; an off-disk change should score 0.</li><li>Click <strong>Compare convolutional and residual predictors</strong>. Inspect both forecasts.</li></ol><div class="done">Done when: you can identify the selected manual model and show a case where its forecast is wrong.</div>


<!--
20 minutes. Learners need an attempt before worked answers. Same data and training budgets apply to both models. Results are selected using validation only.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:15</div>

# Now the agent can edit the program

<ResearchMap :level="4" /><div class="bottom-note">The agent can draft the hypothesis and code. You still review the diff.</div>


<!--
Introduce the meta layer only after students have built a working experiment. The agent gets evidence and a constrained edit request. It can be mistaken.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:17</div>

# Two kinds of model, two kinds of change

<table class="clean-table"><tbody><tr><th></th><th>Research agent</th><th>Forecasting model</th></tr><tr><td>Job</td><td>Propose code edits</td><td>Predict solar observations</td></tr><tr><td>Weights</td><td>Fixed throughout</td><td>Trained on training dates</td></tr><tr><td>Changed by this loop</td><td>Its evidence and task context</td><td>Source, loss, training code, trained weights</td></tr></tbody></table><div class="bottom-note">No post-training of the research agent occurs in this workshop.</div>


<!--
Explicitly correct possible carryover from the Harness² agent workshop. There all runtime model weights stayed fixed. Here small forecasting models train normally.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:19</div>

# What the editor can change

<div class="two-col"><div><h2>Editable</h2><p>Model layers<br>Feature computation<br>Training loss<br>Training procedure</p></div><div><h2>Held fixed</h2><p>Data partitions<br>Target definition<br>Independent metric<br>Final-test access</p></div></div><div class="bottom-note">Reviewed subprocess execution is not a security sandbox. Training workers receive no Forge credentials.</div>


<!--
Use accurate isolation language. This workshop runs reviewed Python in a bounded subprocess, not remote Sandbox entitlement. Time limits and no inherited secrets reduce risk but do not turn arbitrary code into secure execution.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:21</div>

# Give the agent the active experiment

<div class="step-path"><div><h2>Exact source</h2><p>The files that produced the parent result.</p></div><div><h2>Active settings</h2><p>Architecture, steps, width, optimizer values.</p></div><div><h2>Validation evidence</h2><p>Curves, errors, predictions, and failed attempts.</p></div></div><div class="bottom-note">A default in source may not be the value the run used.</div>


<!--
The rehearsal retained an ineffective default-value edit when active configuration was missing. Teach the general mechanism without hiding the qualification history. No final-test scores enter this context.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:23</div>

# Agent Lens records how the edit happened

<div class="step-path"><div><h2>Request</h2><p>Mission, evidence, model settings.</p></div><div><h2>Tools</h2><p>Read evidence, produce code, run a test.</p></div><div><h2>Decision</h2><p>Proposed files, rationale, retained lesson.</p></div></div><div class="bottom-note">A persuasive rationale is a hypothesis. The probe determines what the code did.</div>


<!--
Model/tool spans, timestamps, arguments, results and errors must correspond to actual events. Automatic Insights clustering is not required for this small workshop. Deterministic records are not renamed Insights.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:24</div>

# Inspect the evidence the researcher read

<div class="native-columns"><a href="/images/ux-v020-solar-lens-current.png" target="_blank" aria-label="Open full-size Agent Lens capture"><img src="/images/ux-v020-solar-lens-current.png" alt="Recorded Agent Lens read_validation_evidence span with inputs and outputs"></a><div><h2>Find <code>read_validation_evidence</code>.</h2><p>The span preserves the active configuration and validation evidence.</p><h2>Then inspect the proposal.</h2><p>Compare its returned source with the program that the probe ran.</p><p class="aside"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4/spans">Open the recorded conversation ↗</a><br><a href="/images/ux-v020-solar-lens-current.png" target="_blank">Open full-size capture ↗</a></p></div></div><div class="bottom-note">Actual revised-notebook rehearsal, November 13. Your conversation contains your own execution.</div>


<!--
Native Agent Lens capture of the selected read_validation_evidence span 37fa531bfbbebdfb in the revised-notebook rehearsal. Authentication may be required for the conversation link.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">2:25–2:40 · YOUR TURN</div>

<a class="answer-link" href="/81">Worked answer → 81</a>

# Choose what the research agent may inspect

<div class="task">Open <strong>6 · Research agent</strong>.</div><ol class="exercise-controls"><li>Inspect <code>select_validation_evidence(record)</code>. Keep active settings and validation results, then click <strong>Check my evidence selection</strong>.</li><li>Check that reserved-date predictions and scores are excluded.</li><li>Read the mission. Name one proposed test that could show an edit did not help.</li></ol><div class="done">Done when: you can explain what the agent sees and what remains withheld.</div>


<!--
12 minutes. Code selection is the lesson, not copying an event identifier by hand. Use small visible checks for allowed split and supported source.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:40</div>

# Two candidates start from the same parent

<ResearchBranches :level="1" /><div class="bottom-note"><a href="https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335">Harness²-inspired</a>: our probes train forecasting weights and include validation scores.</div>


<!--
Introduce competing hypotheses. This is a teaching adaptation of Harness² Propose–Probe–Compose (https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335). Upstream task refinement uses execution evidence without ground-truth feedback. Here the agent explicitly receives validation metrics and edits an ML training program. A larger network is not automatically better.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:41</div>

# Review the actual change, then test it

<a class="diff-crop" href="/images/ux-v020-solar-diff.png" target="_blank" aria-label="Open the full proposed-change capture"><img src="/images/ux-v020-solar-diff.png" alt="Actual candidate diff changes squared training error to absolute error and requires review before the probe"></a><div class="image-caption">Fresh rehearsal proposal: <code>.square()</code> became <code>.abs()</code>. Review is not evidence of a gain. <a href="/images/ux-v020-solar-diff.png" target="_blank">Full capture ↗</a></div>


<!--
Actual round-one proposal in the revised browser rehearsal. This frame is cropped to the source diff and explicit review control. The full capture includes the agent-attributed rationale. We have not inferred a performance benefit from that rationale. Only the subsequent probe can measure it.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:42</div>

# Each proposed program must run

<ResearchBranches :level="2" /><div class="bottom-note">Use the same training and validation data. Keep failed runs visible.</div>


<!--
Show exact source fingerprints and receipts. If an attempt fails to train, preserve its failure; don’t coerce a missing score to zero.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:44</div>

# Composition reviews the probes

<ResearchBranches :level="3" /><div class="bottom-note">KEEP retains the source. Its next probe is a new execution, not a new executable version.</div>


<!--
Dashed lines mean reviewed evidence. They do not mean both candidates were adopted. This was a major ambiguity in older branch drawings.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:46</div>

# A composition is another proposal until tested

<ResearchBranches :level="4" /><div class="bottom-note">The proposed file must match the source the probe executes.</div>


<!--
A combined version can introduce new behavior. Even if both component candidates passed, the composition needs an execution. Retaining the parent preserves the source fingerprint.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">2:48</div>

# The next round uses the previous result

<ResearchBranches :level="5" /><div class="bottom-note">Carry the adopted source and an evidence-backed lesson into round two.</div>


<!--
Both rounds remain on the solar image task. The selection policy uses validation error. Repeated editing is not proof of recursive performance gains.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">2:50–3:00 · YOUR TURN</div>

# Run round one, one decision at a time

<div class="task">Inspect <code>next_research_action</code> in <strong>6 · Research agent</strong>.</div><ol class="exercise-controls"><li><strong>Propose two code changes</strong>. Read both diffs.</li><li>Confirm review of Candidate A → <strong>Test Candidate A</strong>. Confirm review of Candidate B → <strong>Test Candidate B</strong>.</li><li><strong>Record my comparison</strong>, then <strong>Request a composition</strong>.</li></ol><div class="done">Done when: you can point to each candidate’s files, training result, and Agent Lens conversation.</div>


<!--
Work alongside learners. Review actions are free; testing is explicit. Keep this slide visible during the first half of round one.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">3:00–3:15 · YOUR TURN</div>

<a class="answer-link" href="/82">Worked answer → 82</a>

# Test the composition, then repeat

<div class="task">Continue the same workbench.</div><ol class="exercise-controls"><li>Confirm review of composition, then <strong>Test the composition</strong>.</li><li>Click <strong>Save the adopted version and lesson</strong>. Check whether the parent was retained.</li><li>Repeat the process in round two using the previous outcome.</li></ol><div class="done">Done when: both rounds have a tested selection and rejected alternatives remain inspectable.</div>


<!--
15 minutes. A valid KEEP outcome completes the exercise. If calls are slow, inspect saved evidence and label replay rather than pretending an edit ran.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:15</div>

# Every branch should explain a decision

<ResearchBranches :level="5" :interactive="true" />


<!--
Optional two-minute interactive recap. Keyboard-accessible nodes explain the process. This diagram is an illustration; the notebook branch view opens actual records.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:17</div>

# The search ends before final evaluation

<div class="step-path"><div><h2>Persistence</h2><p>Copy the latest observed image.</p></div><div><h2>Manual selection</h2><p>Best implemented model on validation.</p></div><div><h2>Agent selection</h2><p>The last valid adopted code and weights.</p></div></div><div class="bottom-note">Freeze source and weights. No more selection using the reserved dates.</div>


<!--
The final image comparison has three versions on the same later windows. The measurement comparison is separate. The final stage loads weights rather than fitting again.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:19</div>

# Final inference loads the saved weights

```python
model = build_model(input_shape, frozen_config)
model.load_state_dict(saved_weights)
model.eval()
with torch.no_grad():
    prediction = model(final_inputs)
```

<div class="bottom-note">There is no optimizer step in this stage.</div>


<!--
Illustrative inference excerpt. Validate the actual execution uses the frozen model rather than silently retraining. The fixed scorer sees future targets; the candidate program does not during improvement.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:21</div>

# Compare the same forecast windows

<table class="clean-table"><tbody><tr><th>Case identity</th><th>Persistence</th><th>Manual</th><th>Agent-selected</th></tr><tr><td>Same input timestamps</td><td>Prediction + error</td><td>Prediction + error</td><td>Prediction + error</td></tr><tr><td>Same target timestamp</td><td>Trace or receipt</td><td>Executed source</td><td>Executed source</td></tr></tbody></table><div class="bottom-note">Weave and EvalTables use stable case IDs to align predictions across versions.</div>


<!--
Native EvalTables has returned HTTP500 in the recorded rehearsal. Show the notebook and Weave comparison when unavailable. Never label a fallback W&B Table as native EvalTables.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">3:25–3:45 · YOUR TURN</div>

<a class="answer-link" href="/83">Worked answer → 83</a>

# Evaluate the frozen versions

<div class="task">Open <strong>7 · Final evaluation</strong>.</div><ol class="exercise-controls"><li>Click <strong>Freeze versions and evaluate reserved dates</strong>.</li><li>Select one shared case. Inspect its prediction, observed future, and error for every version.</li><li>Open its training record, source, and Agent Lens evidence. Keep image and measurement scores separate.</li></ol><div class="done">Done when: all versions are represented, including missing results and failed publication.</div>


<!--
20 minutes. Score differences are evidence from these dates and this run. Do not count pixels or neighboring timestamps as independent studies.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:45 · RECORDED REHEARSAL</div>

# In this rehearsal, image error fell 10.15%

<div class="measured-grid"><div><div class="measured-gain">10.15%</div><p>less error than the manually selected model</p><p class="aside">Agent edits: zero-initialize the residual head, then use absolute training loss.</p></div><table class="clean-table"><tbody><tr><th>Frozen version</th><th>Masked MAE ↓</th></tr><tr><td>Persistence</td><td>0.125762</td></tr><tr><td>Manual residual model</td><td>0.122442</td></tr><tr><td>Agent-selected code</td><td>0.110011</td></tr></tbody></table></div><p class="aside">Actual AIA 171 Å observations. 199 overlapping windows; February 13–14, 2014; one seed. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==">Open the recorded comparison ↗</a></p><div class="bottom-note">A measured result from this rehearsal, not a promised outcome for your edits.</div>


<!--
Recorded November 13 rehearsal: public/recorded-study.json, images/final-comparison. Manual masked MAE 0.1224417336622075; agent 0.11001095193834161; persistence 0.12576198700564592. The 10.15% is relative error reduction versus manual, not percentage points of accuracy. Agent source contains the zero-init head from round one and absolute loss from round two. One seed, overlapping windows and two reserved dates sharply limit generalization.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:46 · RECORDED REHEARSAL</div>

# Recorded: inspect the matching forecasts

<a class="final-crop" href="/images/ux-v020-solar-final.png" target="_blank" aria-label="Open the complete final notebook comparison"><img src="/images/ux-v020-solar-final.png" alt="Actual notebook comparing manual and agent forecasts at the same reserved timestamp, with observed future and error images"></a><div class="image-caption">Same input and future timestamp. Manual above, agent-selected below. <a href="/images/ux-v020-solar-final.png" target="_blank">Full notebook comparison ↗</a></div>


<!--
Actual revised-notebook final comparison. The crop shows matching manual and agent forecast rows. The linked full screen includes the image score table and the separate GOES failure table. This is the notebook comparison, not native EvalTables. Source: evidence/ux-v020-solar-final.png; the underlying saved agent plot is public/images/solar-final.png.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:47 · RECORDED REHEARSAL</div>

# Recorded: the short measurement models lost

<img class="solar-photo" src="/images/goes-final.png" alt="Recorded observed flux and undertrained forecast"><div class="image-caption">Final log-flux MAE: selected model 2.469; persistence 0.193. The training budget was 60 steps.</div>


<!--
Fresh revised-notebook rehearsal: public/recorded-study.json, goes/final-comparison and saved predictions. Undertraining is supported by the saved learning curves; do not turn this into a claim that MLP or CNN cannot forecast these observations.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:48</div>

# Quality, effort, and execution are separate

<table class="clean-table"><tbody><tr><th>Question</th><th>Evidence</th></tr><tr><td>Did forecasts improve?</td><td>Matched final predictions and fixed metrics</td></tr><tr><td>What did improvement cost?</td><td>All proposals, probes, retries, and compute</td></tr><tr><td>Did execution get more reliable?</td><td>Errors, missing outputs, and recovery traces</td></tr></tbody></table>


<!--
A smoother execution may not produce a better forecast. A tiny score change may not justify a large search. Inference and notebook compute billing are separate.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:49</div>

# Your teammate should be able to reopen the result

<div class="step-path"><div><h2>Run</h2><p>Settings, metric, loss history.</p></div><div><h2>Artifact</h2><p>Source, data, weights, predictions.</p></div><div><h2>Trace</h2><p>Agent requests, edits, tests, decisions.</p></div></div><div class="bottom-note">The Report explains what changed and links to those records.</div>


<!--
Explain the evidence chain in ordinary language. Do not make facilitator monitoring a substitute for storing scientific outputs.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: exercise
---

<div class="kicker">3:50–3:58 · YOUR TURN</div>

# Publish the result you can defend

<div class="task">Use your own comparison.</div><ol class="exercise-controls"><li>State one code change and the result it produced on reserved dates.</li><li>Include an example where the forecast failed or changed little.</li><li>Click <strong>Publish my conclusion</strong>. Reopen one result from its saved artifact.</li></ol><div class="done">Done when: another person can trace your claim to its code, run, prediction, and score.</div>


<!--
Eight minutes. Permit a negative finding. If publication fails, save the conclusion and use publication-only retry.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">3:58–4:00</div>

# The agent can propose the next experiment.

<p class="big">You now have the part that makes the proposal testable.</p><p>Keep the data version. Save the executed source. Inspect the prediction. Measure on dates the search did not use.</p><div class="bottom-note">The next result still needs a source file, a dataset version, and a test.</div>


<!--
End on an actionable distinction. The research agent increases how many hypotheses can be proposed. The measurement stack determines whether we learn from them. Don’t promise unlimited autonomous research.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">REFERENCE</div>

# Reference and worked answers

<p class="big">Use these after an attempt, or when live access is unavailable.</p><p>Recorded examples belong to the November 13 technical rehearsal. They are not results from your unexecuted changes.</p><div class="bottom-note">Use the return links to continue the workshop.</div>


<!--
All following pages are optional and add no lecture time.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# A tool span records the actual operation

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


<div class="source-link"><a href="/10">Return to Connect and find your first span →</a></div>

<!--
Excerpt of the actual instrument_tool function. Parent scopes and tool_call_id are shown in the notebook. Compare stored spans with independent events; timestamps must describe the event, not a later export.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# Persistence returns the latest observation

```python
def persistence_forecast(split):
    return split["persistence"].copy()
```

<p>Changing the returned array must not mutate the original data.</p>
<div class="source-link"><a href="/20">Return to Write and test persistence →</a></div>

<!--
Worked answer uses public split persistence field. Tests must also reject using the target and preserve input data.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# A constant one-unit error scores one

```python
def training_loss(prediction, target, mask):
    return ((prediction - target).square() * mask).sum() / mask.sum()

def my_flux_mae(prediction, target):
    return float(np.abs(prediction - target).mean())

assert my_flux_mae(np.ones(3), np.zeros(3)) == 1.0
assert my_flux_mae(np.zeros(3), np.zeros(3)) == 0.0
```


<div class="source-link"><a href="/30">Return to Make the result reproducible →</a></div>

<!--
Code validated by scripts/check-answers.py. Units are the transformed flux units, not raw W/m².
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">WORKED ANSWER</div>

# A completed search keeps every attempt

<p class="big">Six configurations share data, source, split, seed, and a training budget.</p><p>Compare the actual configuration fields in the Sweep. A failed execution stays in the table with its error; an unavailable metric stays missing.</p><div class="bottom-note">Changing source creates a different set of stage identities.</div>
<div class="source-link"><a href="/36">Return to Run the same search and inspect a loss curve →</a></div>

<!--
This is an inspection answer, not a promised outcome. W&B sweep assignment and journal execution reuse are separate responsibilities.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# The image scorer ignores off-disk pixels

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
Code validated against small deterministic fixtures. Production scorer remains independent.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# A zero correction reproduces persistence

```python
def forward(self, x):
    correction = self.net(x)
    if architecture == "residual":
        return x[:, 1:2] + correction
    return correction
```

<div class="bottom-note">The current image is input channel 1. The return has one channel.</div>


<!--
Excerpt of ImagePredictor in candidate.py. A constant zero correction produces the current image exactly. This tests wiring, not learned forecasting quality.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">WORKED ANSWER</div>

# Evidence selection excludes final results

```python
def select_validation_evidence(record):
    if record.get("split") != "validation":
        raise ValueError("Only validation evidence is allowed.")
    fields = ("split", "config", "metrics", "losses",
              "errors", "trace", "stage_id", "lessons")
    return {name: record[name] for name in fields if name in record}
```

<div class="bottom-note">The parent source is supplied separately. Final predictions and scores are excluded.</div>
<div class="source-link"><a href="/53">Return to Choose what the research agent may inspect →</a></div>

<!--
The notebook provides the exact schema and checked implementation. The exercise should show a validation fixture accepted and a test fixture rejected.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">WORKED ANSWER</div>

# The probe must run the proposed source

```python
candidate = proposal["candidates"][candidate_index]
probe = run_training(
    session, stage_name, candidate["source"],
    image_splits, parent["config"], dataset_version, metric_source,
)
```

<div class="bottom-note">Passing the parent source here would test the wrong program while producing a plausible result.</div>
<div class="source-link"><a href="/61">Return to Test the composition, then repeat →</a></div>

<!--
Code excerpt mirrors the visible controller. Compare candidate.py in the saved proposal with candidate.py in the execution receipt. A complete source-bundle fingerprint also includes the metric file. The caller provides validation evidence, not final results.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">WORKED ANSWER</div>

# The final comparison does not refit

<p class="big">Each selected version uses its saved weights.</p><p>Check the freeze receipt, source fingerprint, weight artifact, target timestamps, and all three prediction rows.</p><div class="bottom-note">Persistence needs no training weights. Missing outputs remain visible.</div>
<div class="source-link"><a href="/66">Return to Evaluate the frozen versions →</a></div>

<!--
The frozen inference path calls training.train with supplied weights and no training split. Tests verify the fit function is not invoked.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 1: two changes, two measured outcomes

<table class="clean-table"><tbody><tr><th>Source</th><th>Validation error ↓</th></tr><tr><td>Manual residual model</td><td>0.122116</td></tr><tr><td>A · replace squared loss with absolute loss</td><td>0.120553</td></tr><tr><td>B · initialize the residual head at zero</td><td>0.111434</td></tr></tbody></table><p>The composition selected B. Its separate test reproduced 0.111434.</p><p class="aside"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4">Open the actual proposals and evidence ↗</a></p>


<!--
Fresh revised-notebook rehearsal. Same date partitions, independent metric, seed and 40-step image training configuration. The composition selected the tested zero-init source without adding an untested loss change. This is one validation experiment, not a treatment estimate. Source: public/recorded-study.json.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---
class: answer-code
---

<div class="kicker">RECORDED REHEARSAL</div>

# The selected edit starts at persistence

```python
if architecture == 'residual':
    nn.init.zeros_(self.net[4].weight)
    nn.init.zeros_(self.net[4].bias)

# The residual forward pass remains:
return prediction + x[:, 1:2]
```

<div class="bottom-note">Zero initial correction → the initial forecast is the current image.</div>


<!--
This is the actual first-round Candidate B edit. The final convolution is zero-initialized only for the residual architecture. Training can then learn a correction. The existing residual forward pass is unchanged. Its observed validation error belongs on the preceding slide; the code alone does not establish a general gain.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Round 2: KEEP was a real comparison

<table class="clean-table"><tbody><tr><th>Source</th><th>Validation error ↓</th></tr><tr><td>Adopted zero-init model</td><td>0.111434</td></tr><tr><td>A · add absolute loss to that source</td><td>0.110916</td></tr><tr><td>B · KEEP the zero-init source unchanged</td><td>0.111434</td></tr></tbody></table><p>KEEP reproduced the parent. The tested composition selected A.</p><div class="bottom-note">An unchanged source can have a new execution. It does not become a new executable version.</div>


<!--
Fresh revised-notebook rehearsal. Candidate B explicitly returned KEEP and its source fingerprint matched the parent. Candidate A proposed the loss change on the previously adopted source. The final composition test returned 0.11091556898305115. This small single-seed validation change should not be presented as repeatable evidence.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">RECORDED REHEARSAL</div>

# Open the recorded research conversation

<p class="big"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4">Open the proposal and its recorded tool activity ↗</a></p><p>Find the active configuration, the requested edit, and the returned candidate code. Compare the proposal with the tested source.</p><p class="aside"><a href="https://ash0ts.github.io/forge-workshop-kit/solar/recorded-study.json">Download the recorded source, decisions, scores, and evidence links ↗</a></p><div class="bottom-note">Agent Lens may require sign-in. The source and saved decisions are also in the downloadable evidence.</div>


<!--
The direct native conversation is linked from the recorded walkthrough and executed evidence. This slide does not use a loading-placeholder screenshot as proof of a completed trace.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">REFERENCE</div>

# When a service is unavailable

<table class="clean-table"><tbody><tr><th>Failure</th><th>Next action</th></tr><tr><td>Project authentication or permission</td><td>Fix access, then retry the check</td></tr><tr><td>Training or inference failed</td><td>Inspect the saved error before retrying work</td></tr><tr><td>Trace or artifact upload failed</td><td>Retry export of the saved execution</td></tr><tr><td>Native EvalTables HTTP 500</td><td>Use notebook and Weave comparisons; retry publication</td></tr></tbody></table>


<!--
The current technical preview has verified W&B and Weave publication but native EvalTables returned HTTP500. Do not imply a retry always succeeds. Never substitute provider models silently.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">REFERENCE</div>

# Four-hour session

<table class="clean-table schedule"><tbody><tr><th>Minutes</th><th>Work</th></tr><tr><td>0–15</td><td>Copy, connect, instrument</td></tr><tr><td>15–40</td><td>Data and persistence</td></tr><tr><td>40–90</td><td>Tracking and six configurations</td></tr><tr><td>90–100</td><td>Break</td></tr><tr><td>100–135</td><td>Image predictors</td></tr><tr><td>135–195</td><td>Evidence and two research rounds</td></tr><tr><td>195–240</td><td>Freeze, compare, reproduce, explain</td></tr></tbody></table>


<!--
Facilitator pacing target, not a measured participant completion time. Technical rehearsal training and provider time are separate from human learning and review.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->

---

<div class="kicker">REFERENCE</div>

# The workshop lives in your project

<p class="big"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view">Copy the Solar notebook ↗</a></p><p><a href="https://github.com/ash0ts/forge-workshop-kit">Source, setup, dataset, and facilitator guide ↗</a></p><p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==">Recorded rehearsal Report ↗</a></p><div class="bottom-note">Keep your notebook, code edits, and checkpoints. The facilitator needs no control over your runtime.</div>


<!--
Primary public links. Older Pending releases remain historical; this deck teaches the direct participant-owned Workshop Kit runtime.
Source: forge-workshop-kit notebook and recorded evidence; template copy/auth details must be checked before class.
-->
