# Solar Autoresearch experiment

The teaching question is whether a tested change to a small research program improves its forecasts on later observations. A successful workshop requires reproducible evidence, not a favorable result.

## Data

Use February 1–14, 2014 UTC. Train on February 1–10, validate on February 11–12, and evaluate frozen versions on February 13–14. All inputs and targets in a window must belong to its partition. Drop incomplete windows; do not interpolate across gaps. Fit scaling on training data only.

GOES-15 one-minute XRS measurements come from the NOAA science archive through [SunPy Fido](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html). Retain positive flux with zero quality flags. The archive query returned no February 8 file; the manifest and window counts preserve that absence. Predict log10 XRS-B flux 30 minutes after a 60-minute history. Report mean absolute error in log10 W/m² units.

AIA 171 Å observations come from the [calibrated synopsis archive](https://jsoc1.stanford.edu/data/aia/synoptic/README.html), accessed through the URL convention documented by [SunPy](https://docs.sunpy.org/en/stable/generated/api/sunpy.net.dataretriever.AIASynopsisClient.html). Select every 12-minute slot. Keep zero-quality-flag images with positive exposure and at least 99% finite pixels. Record actual observation timestamps and reject offsets beyond two minutes. Divide archive DN/pixel by exposure once, average to 64×64, then apply train-fitted log1p scaling. Preserve source URLs, checksums, units, FITS metadata and every exclusion.

Predict t+60 minutes from t−60 and t. Score absolute error on the target solar-disk mask; report skill relative to copying the latest image. Show prediction, target, and error images. A small region can matter scientifically while contributing little to the mean.

The release contains prepared arrays and a representative FITS file, not thousands of raw archive downloads. The acquisition script and manifest make preparation reproducible. Credit NOAA, NASA/SDO, the AIA science team, JSOC and SunPy.

## Search and agent edits

Configuration search compares six bounded runs: MLP and temporal CNN, each with three width/learning-rate configurations. Image experiments compare a convolutional model and a residual predictor. CPU settings and source are pinned in each run.

The research agent is `zai-org/GLM-5.3-Flash`, fixed throughout a workspace. It proposes two code candidates per round, receives validation evidence, and composes or retains a version. Every proposed source is reviewed; compositions are tested. There are two rounds. Data partitions, target definitions and the independent scorer remain fixed. No test scores enter the research prompt.

Final image comparison: persistence, best manual version by validation error, and the adopted agent version. Freeze executed source and model weights before final inference. Reuse that model, without fitting on final data. Keep errors, missing outputs and failed attempts distinct.

Each claim follows source → executed fingerprint → training receipt → validation decision → frozen predictions → independent score. The branch history retains rejected and unchanged versions. Model weights in the forecasting experiment are trained; the research agent's weights are fixed.

## Limits

This is a small teaching excerpt, not an operational flare forecast, a reproduction of Surya, or evidence of general recursive improvement. Adjacent frames are correlated. Report task means and examples; do not count pixels or neighboring timestamps as independent research trials. We use deterministic metrics rather than an LLM judge for numeric prediction quality.

The six initial measurement runs deliberately use a short, visible 60-step training budget. Inspect the training curve before interpreting an architecture comparison: a model still learning its output scale is undertrained. Participants can change that budget uniformly and record another search. This is not a claim that these settings tune either architecture well.

Optional GPU extension: start a separate workspace, change the worker device explicitly, and record device, precision, batch size, training budget and compute cost. Keep partitions and the independent scorer unchanged. Do not compare a longer GPU search with the CPU exercise as though only the architecture changed.
