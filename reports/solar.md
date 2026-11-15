# Test research-agent changes against real solar observations

The lab has a weekly forecast review. Someone brings a lower error score, but the notebook called `final` isn't the one that produced it. We need the observations, preprocessing, source, settings, weights, and predictions before we can decide what to keep.

Solar Autoresearch turns that situation into a small research project you can run on CPU. You first build and track forecasts yourself. Then a fixed research agent reads your code and validation results, proposes edits, and receives the results of testing them. You review the code and decide what evidence supports using it.

The lab is fictional; the satellite observations are real. Recorded results include a failed neural forecast, its repair, and an image change that helped two seeds and hurt a third.

## Start with the observations and the question

The first task uses one-minute GOES-15 X-ray measurements. Given an hour of observations, predict XRS-B flux 30 minutes ahead. The second uses AIA 171 Å images of the Sun: given an image from an hour ago and one from now, predict the image one hour ahead.

The prepared dataset covers February 1–14, 2014. Training uses days 1–10, validation uses 11–12, and the original final evaluation uses 13–14. A forecast window cannot cross a date partition or a data gap. Normalization is fitted on training observations only. The missing February 8 GOES file remains missing; we don't fill it to make the training set look tidy.

SunPy supports acquisition and FITS inspection. Prepared arrays, checksums, quality exclusions, and a representative FITS file let you inspect provenance without downloading the entire archive. Credit belongs to NOAA, NASA/SDO, the AIA science team, JSOC, and SunPy. The [data contract](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-contract.md) specifies units and preprocessing.

![An actual GOES training window separates sixty observed samples from the future XRS-B target.](https://ash0ts.github.io/forge-workshop-kit/solar/images/v031-goes-window.png)

*The lines are observed input channels; the orange point is the separate future target. A prediction must use only the history to the left of the forecast origin. Flux is shown on a log10 scale.*

Before training a neural network, implement persistence: predict that the latest reading will remain unchanged. Its code is small because the dataset already saves the correctly scaled last observation for each window:

```python
def persistence_forecast(split):
    return split["persistence"].copy()

def my_flux_mae(prediction, target):
    return float(np.abs(prediction - target).mean())
```

The free checks verify that you didn't read the future target and that opposite-signed errors cannot cancel. We score measurement forecasts using mean absolute error in log10 XRS-B flux units. A trained model has to beat this simple forecast to justify its added work on the chosen measure.

## Find out what produced a training result

Compare a small multilayer perceptron, which flattens the history into features, with a temporal convolutional network, which applies learned filters across time. A free forward-pass check exposes their tensor shapes before training.

Training adjusts forecasting weights using a loss; validation evaluates them without updating them. Inspect one configuration's learning curve before completing the six-run W&B Sweep.

Save the source, configuration, data reference, loss history, weights, and predictions with the run. W&B Artifacts store versioned files: you can reopen the exact `candidate.py` and weights associated with a prediction instead of hoping the current editor still contains them. The run records settings and curves; Agent Lens records the research agent's requests and tool calls.

![An artifact file viewer shows the exact candidate source saved with the selected image training run.](https://ash0ts.github.io/forge-workshop-kit/solar/images/visual-v030-solar-artifact.png)

*In the [recorded source artifact](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0/files/files/0/candidate.py), find the zero-initialized output layer and absolute-error loss. Opening today's notebook code would not establish which source produced these weights.*

The original measurement search demonstrates why this record matters. Its selected neural model scored **2.468975**, while persistence scored **0.192706** on the original final dates. Lower is better. Each model had only 60 update steps; a decreasing training curve had not made the selected forecast competitive. Winning the Sweep meant winning among those configurations under that budget.

A follow-up tested a persistence-residual predictor with consistent prediction/target scaling, a zero-initialized output layer, absolute-error loss, and a longer bounded training budget. The recipe was selected using validation error across seeds 17, 29, and 43. Its final errors were **0.162878, 0.163880, and 0.163760**, each below persistence.

Those changes were tested together, so the experiment doesn't isolate one cause. The final dates had already been inspected. This is a [teaching retest](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md), not a fresh unseen benchmark. The failed original runs remain available.

## Move from a scalar forecast to an image

The image task uses prepared 64 × 64 arrays. Preprocessing divides pixel values by exposure, averages spatially, and applies training-fitted log1p scaling. The two input frames become channels of a convolutional predictor.

A direct predictor outputs the future image. A residual predictor outputs a correction to the current image:

```python
# Abbreviated model forward pass: x contains earlier and current frames.
correction = self.net(x)
prediction = x[:, 1:2] + correction
```

If the final correction layer starts at zero, this model initially produces persistence. Training learns changes from that starting point.

Implement the image metric by averaging absolute error over each target image's solar-disk mask, then averaging images equally. Off-disk pixels do not count. Inspect the prediction, target, and error images for localized errors hidden by the average. This score uses standardized log1p intensity units and must remain separate from GOES log-flux error.

![Matched manual and agent-selected image forecasts, targets, and errors from one recorded final timestamp.](https://ash0ts.github.io/forge-workshop-kit/solar/images/v030-final-predictions.png)

*Both rows use the same forecast origin and display scales. This is the first accepted final example in the recording, not the largest observed improvement. The error panel shows where each prediction differs from the observed future image.*

## Give the research agent a bounded job

There are three different interventions here. Hyperparameter search changes settings within existing code. Architecture comparison selects among implemented models. Agent-directed research writes new code, which must then be reviewed and tested.

For the required image exercise, the research agent receives the selected implementation and validation evidence. It proposes two candidates per round. You read each diff, train each candidate from scratch, compare validation results, and test any composition before adopting it. The chosen source and a lesson carry into another round. Retaining the current version is allowed.

The agent's model weights stay fixed. Forecasting weights train normally. Data partitions, prediction targets, and the independent scorer remain outside the agent's editable scope, and reserved results stay out of improvement prompts. Agent Lens lets you inspect which evidence the editor read and which changes it proposed. A plausible rationale is a hypothesis until the experiment tests it.

In the current recorded image run, the first round selected absolute-error loss. The second selected a zero-initialized residual output layer. With seed 17, final error fell from **0.122442** for the manual model to **0.110011** for the selected version, a **10.15% reduction**. Persistence scored **0.125762**.

We then reran those saved sources with three predetermined seeds, without asking the agent to discover new edits. Two seeds improved; one regressed slightly:

![The combined image edits improve seeds 17 and 29 and slightly worsen seed 43.](https://ash0ts.github.io/forge-workshop-kit/solar/images/images-seeds-deck.png)

*The error reductions versus the manual model were 10.15%, 6.87%, and −0.21%. The recipe failed the predeclared requirement to improve every seed. This checks the saved recipe's behavior, not the agent's ability to rediscover it.*

The image comparison contains 199 overlapping windows from two days. Three seeds do not turn those dates into three independent datasets. These experiments teach reproduction and comparison; they do not establish an operational solar forecast or a general advantage for agent-written research code.

## Inspect the comparison, then run your own

Freeze source and trained weights before final prediction. In native EvalTables, align the same timestamp across persistence, manual, and agent-selected forecasts, then follow the run and artifact links. If publication fails, the notebook retains completed results and offers an upload retry without another training run. The optional ARIA activities ask you to explain a result and verify one cited observation; ARIA's answer does not become a forecast score.

Open the [Solar Autoresearch notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view), choose **Copy to project**, and open the editable copy. Use **Run all stale cells** to create the controls, check your project, and start with the observation window and persistence function. Explicit exercise controls start training and inference.

The [six-hour deck](https://ash0ts.github.io/forge-workshop-kit/solar/) explains the calculations alongside the exercises. The [setup guide](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/setup.md) includes a laptop path using `uv sync --frozen --extra solar`. You use your own project, compute, and inference access; the adjustable $8 inference allowance excludes notebook compute and ARIA usage. Remote Sandboxes are not required.

The materials are technical previews; external-account and participant rehearsals remain outstanding. You can inspect the prepared observations and recorded outcomes before spending on inference, then use your own runs to decide which change to test next.
