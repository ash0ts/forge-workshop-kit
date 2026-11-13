# Sources and visual contract

## Design reference

The November 12 Pending, Inc. Slidev deck supplies the visual direction and teaching pattern: cream and deep teal, IBM Plex Sans/Mono, progressive diagrams, direct exercise instructions, optional worked answers, and brief contextual narration. The historical deck and releases remain unchanged.

The opening is an original computational research-lab scene. The canonical pixel artwork is `src/forge_workshop_kit/assets/solar-lab.svg`; the deck bundles an identical copy. Its solar monitor, curves, notebook and compute rack are illustrations, not native product screens or measured results. Dialogue is not a model transcript or a reported incident. Research diagrams explain implemented operations; they do not claim every candidate improves quality.

## Technical sources

- `scripts/solar_cells.py` and `notebooks/solar_autoresearch.py`: exercise names, visible code, controls, execution and publication.
- `src/forge_workshop_kit/solar_teaching.py`: practice checks, worked answers, and guided research steps.
- `docs/solar-contract.md`: dates, targets, transformations, metrics, and editable boundaries.
- `evidence/hosted-templates.json`: published template identities.
- `decks/solar/public/recorded-study.json`: a narrow, public snapshot of the revised notebook's November 13 browser rehearsal. It preserves executed source, configuration, metrics, candidate decisions, artifact links, and verified trace identities. It excludes credentials, request-account records, local paths, and notebook drafts.
- `decks/solar/public/recorded-runs.json`: two GOES executions from that same rehearsal, used by the configuration inspector.

Paths above are relative to the repository root. `scripts/snapshot-rehearsal.py` reads the saved journal to create the public evidence snapshot. It does not repeat execution. Human pacing is not inferred from training or provider durations.

The [pinned Harness² README](https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335) describes grade-free task-level Propose–Probe–Compose and retained experience. This workshop adapts that structure to ML code edits with validation metrics. It does not reproduce the paper's evaluation protocol.

## Data and forecast images

The data comes from NOAA GOES-15 measurements and NASA/SDO AIA 171 Å observations. Credit the AIA science team, JSOC, and SunPy. The dataset manifest preserves acquisition URLs, FITS metadata, source checksums, quality exclusions, and preprocessing.

- [SunPy GOES workflow](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html)
- [SunPy AIA synopsis client](https://docs.sunpy.org/en/stable/generated/api/sunpy.net.dataretriever.AIASynopsisClient.html)
- [JSOC calibrated archive](https://jsoc1.stanford.edu/data/aia/synoptic/README.html)

`solar-validation.png`, `solar-final.png`, and `goes-final.png` come from saved model predictions in the revised-notebook rehearsal. The final image is the saved frozen-agent prediction; the GOES plot was rendered from the saved final predictions and immutable test split without retraining. They are actual plot exports, not generated examples. The older rehearsal evidence remains in the repository but is not pooled into these displayed results.

GOES error is MAE in log10 XRS-B W/m². Inputs are normalized; targets retain log-flux units. Image error uses the fixed disk mask on training-normalized log1p intensity. These scores answer different questions and are not averaged together.

The measured image improvement, matching forecasts and contrasting GOES failure appear in the main teaching sequence. The 10.15% decrease is calculated from the saved manual and agent masked errors, not a new model execution.

## Native and notebook captures

All product screens are real browser captures. Slide crops change presentation only; linked full-size captures retain their context.

- `ux-v021-solar-setup.png`: the current Solar Forecasting Lab notebook's Connect screen with the saved rehearsal workspace. The actual rehearsal project and allowance are visible; attendees use their own project. Other v020 screens below preserve the original measured execution evidence.
- `ux-v020-solar-instrumentation.png`: the edited `instrument_tool` function and passing free check. The check itself exports nothing. The subsequent trace has verified stored span `3836f2a676d91bdf` in conversation `19f7b8c14211a63aa6a7e22bd14375bf`.
- `ux-v020-solar-models.png`: the settled validation model comparison: matching convolutional and residual forecasts, metrics, and actual Agent Lens/run/artifact links.
- `ux-v020-solar-diff.png`: first-round Candidate A changes squared training error to absolute error. The actual diff and review control are visible. The rationale is attributed to the agent; the measured outcome comes from the later probe.
- `ux-v020-solar-lens-current.png`: native Agent Lens `read_validation_evidence` span `37fa531bfbbebdfb` in [conversation ef590522f1af377a0bc04bd63eea23e4](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ef590522f1af377a0bc04bd63eea23e4/spans).
- `ux-v020-solar-final.png`: the settled final notebook comparison: matched manual/agent forecasts, 199 image windows, and the separately scored GOES failure. This is not native EvalTables.
- `ux-v020-solar-sweep.png`: native [Sweep pr1xsoaw](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/sweeps/pr1xsoaw), showing all six configurations, validation error, negative persistence skill, and runtime. Display names identify actual architecture, width, and learning rate. The full capture retains the ingestion-delay notice.
- `solar-template-qr.svg`: the published template URL `https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view`, encoded locally with the installed `uqr` library.

## Product and claim boundaries

Forge hosts the participant's notebook and project. The notebook uses that participant's authentication and inference allowance directly. Training runs reviewed Python in a bounded local subprocess. This is not a security sandbox and does not require a separate remote Sandbox entitlement. Forecasting weights train normally; the research agent's weights stay fixed.

Agent Lens stores actual request and tool evidence. Weave and W&B publication are separate from native EvalTables. Native EvalTables returned HTTP 500 during rehearsal and remains explicitly unavailable unless a publication retry succeeds.

The recorded result belongs to one seed and two reserved dates. Adjacent forecast windows overlap. It is not evidence of general solar forecasting improvement, a Surya reproduction, or a controlled diagnostics-treatment effect. The two research rounds demonstrate a working code-editing loop; quality is measured separately.
