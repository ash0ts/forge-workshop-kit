# Real observations, measured improvement

Solar Autoresearch uses satellite observations and a small CPU experiment. The lab, researchers and dialogue are fictional. The measurements, images, saved predictions and reported scores are real.

The recorded rehearsal gives us a concrete result to teach: two reviewed code changes reduced final image-forecast error by **10.15% against the manually built model** and **12.52% against copying the latest image**. The gain comes from one run on two reserved dates. Participants reproduce the method and measure their own outcome; their edits do not inherit the recorded result.

## Where the data came from

The dates were fixed before training: February 1–10, 2014 for training, February 11–12 for validation, and February 13–14 for final evaluation.

| Exercise | Observations | Prediction | Prepared windows: train / validation / final |
|---|---|---|---|
| Measurements | NOAA GOES-15 XRS, one-minute averages | Use 60 minutes of history to predict XRS-B flux 30 minutes ahead | 11,122 / 2,779 / 2,694 |
| Images | NASA/SDO AIA 171 Å images from JSOC | Use images from an hour ago and now to predict one hour ahead | 1,036 / 142 / 199 |

GOES retrieval uses SunPy's Fido interface and retains positive measurements with zero quality flags. The download inventory contains 13 daily files; February 8 is absent. Of 18,720 downloaded rows, 18,499 survive filtering. Windows cannot cross a gap or partition boundary. [NOAA archive](https://www.ncei.noaa.gov/products/goes-1-15/space-weather-instruments), [SunPy retrieval and quality filtering](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html).

The AIA archive contains observations processed to level 1.5 and reduced to 1024 × 1024 pixels. We request a frame every 12 minutes, divide pixel values by exposure once, average to 64 × 64, then apply log1p scaling fitted on training images. This leaves 1,627 of 1,680 requested frames: 44 fail the quality rule and nine are absent. Actual observation times, exposure, wavelength, source URL and exclusion reason remain in the manifest. [JSOC archive description and units](https://jsoc1.stanford.edu/data/aia/synoptic/README.html), [SunPy AIA client](https://docs.sunpy.org/en/stable/generated/api/sunpy.net.dataretriever.AIASynopsisClient.html).

The prepared download is 26,136,236 bytes. The audit verified its published checksum, every prepared-file checksum, all 13 raw GOES checksums and all 1,671 available AIA FITS checksums. Reprocessing the first, middle and last retained FITS files exactly reproduced their prepared image arrays. Acquisition code also matches the manifest's saved hash. See [machine-readable review](../evidence/solar-realism-review.json), [data contract](solar-contract.md) and [acquisition code](../scripts/prepare_solar.py).

## What the agent changed

The manual image model predicts a correction to the latest image. Its final layer initially contains random weights. The fixed research agent proposed and tested these changes:

1. **Start from a known forecast.** Zero-initialize the residual head, so the untrained model's correction is zero and its initial output equals the latest image. Training then learns a correction from that starting point.
2. **Train against the error we report.** Replace masked squared error with masked absolute error. Keep the data, forecast horizon and independent final scorer fixed.

The agent explored another first-round candidate that changed only the loss. Its validation error was 0.120553, compared with 0.111434 for the zero-initialized head. The first composition selected the tested head change. The next round tested the loss change on top of that version, then adopted the combination. An unchanged candidate remained visible in the branch history.

| Tested version | Validation image error |
|---|---:|
| Copy the latest image | 0.126451 |
| Manual residual model | 0.122116 |
| Round 1: zero-initialized residual head | 0.111434 |
| Round 2: zero-initialized head + absolute-error loss | 0.110916 |

Each image training run used width 8, learning rate 0.001, batch size 8, 40 update steps and seed 17. Candidate training started from scratch. Final evaluation loaded the selected weights without further training. Saved sources and model parameters match their adopted training versions; the final subprocess inputs contain prediction inputs only. [Decisions, diffs, run links and traces](../evidence/ux-v020-solar.json).

## What improved on the reserved dates

The fixed metric averages absolute error inside the target solar-disk mask, then averages windows equally. Values are in train-standardized log1p image units. Lower is better.

| Frozen version | Final image error | Change against copying the latest image |
|---|---:|---:|
| Copy the latest image | 0.125762 | Reference |
| Manual residual model | 0.122442 | 2.64% lower |
| Agent-selected model | 0.110011 | 12.52% lower |

The agent-selected model reduces the manual model's mean error by 0.012431, or **10.15%**. It has lower mean image error on all 199 matching windows, with gains on both final dates. These are overlapping windows from two days, not 199 independent trials. Individual pixels can still get worse, and whole-disk error does not establish better prediction of a small flare or other localized event.

The audit recomputed these means from the saved prediction arrays and independent scorer. It also inspected the prediction and error images. The benefit belongs to the adopted combination under this short training budget. We have not run held-out ablations, multiple seeds, a matched expert search, or an Agent Lens versus no-Agent-Lens control. Those would answer different questions.

## Keep the unsuccessful forecast visible

The GOES neural model's final log-flux MAE is **2.468975**, while persistence achieves **0.192706**. The six-configuration search used a short 60-step budget. Winning that search did not make the selected neural model useful. Its training curve, source and poor predictions are part of the lesson: compare against a simple baseline before celebrating the best run in a dashboard.

The measured image gain is the positive example. The measurement failure teaches why this research loop needs baselines, held-out evaluation and inspectable evidence. Neither result should be replaced with a promised outcome for live participants.

## How the office workshop differs

Pending, Inc. stays an office simulation. Its account, invoice, refund and membership records are explicitly fictional. Its situations model real integration problems: a timeout after a write has committed, a reused operation ID, two different invoices mistaken for a duplicate charge, and missing information that requires clarification. Real APIs also use stable idempotency keys to avoid repeated mutations, and a network timeout can leave a write's outcome uncertain. [Stripe idempotency](https://docs.stripe.com/api/idempotent_requests), [network-error guidance](https://docs.stripe.com/error-low-level#network-errors).

The simulator simplifies those systems and deliberately permits some bad actions so independent checks can catch them. It is not a Stripe replica or real customer data. In the recorded office rehearsal all 12 final executions pass the state checks; one explanation judgment remains unavailable. The agent retains the manually revised harness. This demonstrates a working improvement loop and a valid decision to retain a version, with **no observed task-quality gain**. [Pending rehearsal evidence](../evidence/ux-v020-pending.json).
