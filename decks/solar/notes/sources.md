# Sources and visual contract

## Current walkthrough

The deck uses the November 13, 2026 v0.3.0 Solar technical rehearsal in project `wandb/forge-workshop-kit`, workspace `6e768bbe071648e094cb296a0a57c21e`. The rehearsal ran authored notebook cells. It is not a human usability test.

The same workspace supplies proposals, executed source, validation scores, final predictions, artifacts, and product links. Older rehearsal captures remain available in prior releases; the current slides do not mix their branch order into this result.

- `public/recorded-study.json`: selected saved stages, source, decisions, scores, and verified trace identities.
- `data/recorded-runs.json` and `public/recorded-runs.json`: the same two GOES records used by the interactive configuration inspector.
- `scripts/snapshot-rehearsal.py`: reads a completed journal to produce the public snapshot. It makes no requests and repeats no execution.
- `notes/recorded-evidence-checks.json`: source-to-probe and composition-to-execution checks, including the valid unchanged candidate.

The first round selected absolute training loss over the unchanged squared-loss version. The second selected a zero-initialized residual head and rejected permutation batching. The final source includes the two selected changes in that order.

## Teaching sources

The editable source and exercise controls come from `scripts/solar_cells.py` and `src/forge_workshop_kit/solar_teaching.py`. `notes/exercise-contract-checks.json` reconciles the deck's named functions and buttons against those files. Both paths are relative to the repository root.

- [SunPy time-series tutorial](https://docs.sunpy.org/en/stable/tutorial/timeseries.html): inspect actual observations and units before modeling them.
- [SunPy map tutorial](https://docs.sunpy.org/en/stable/tutorial/maps.html): inspect dates, wavelength, and FITS metadata.
- [SunPy AIA synopsis client](https://docs.sunpy.org/en/stable/generated/api/sunpy.net.dataretriever.AIASynopsisClient.html) and [JSOC calibrated archive](https://jsoc1.stanford.edu/data/aia/synoptic/README.html): AIA acquisition and provenance.
- [PyTorch Quickstart](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html): explain a concept beside a short code example and its output. Our wording, diagrams, and exercises are original.
- [Pinned Harness² workflow](https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335): Propose–Probe–Compose. This workshop adapts that structure to ML code edits with validation scores; it does not reproduce the paper's task protocol.
- [Agent Lens](https://docs.coreweave.com/products/agent-lens): native request and tool inspection.
- [EvalTables comparisons](https://docs.coreweave.com/products/wandb/evaltables/compare-runs): the intended aligned comparison surface. Publication remained unavailable in this rehearsal.

## Scientific figures

Data is NOAA GOES-15 and NASA/SDO AIA 171 Å observations from February 1–14, 2014, prepared with SunPy. Credit NOAA, the AIA science team, JSOC, and SunPy. The immutable dataset manifest preserves acquisition URLs, checksums, quality exclusions, and preprocessing. The prepared image arrays are 64 × 64.

`scripts/build-evidence-figures.py` plots actual observations and saved predictions without training or inference. `notes/visual-v030-figures.json` records each output, stage identity, and checksum.

| Figure | Selection and meaning |
| --- | --- |
| `v030-observations.png` | First accepted training measurements and first accepted current AIA image. Establishes the two real instruments and targets. |
| `v030-image-window.png` | First accepted training window: earlier image, current image, future target. Common intensity scale. |
| `v030-goes-loss.png` | Saved losses for the selected width-16 MLP, learning rate .003, 60 steps. No extended training was run. |
| `v030-validation-predictions.png` | Convolutional and residual predictions for the first accepted validation case. Same image and error scales. |
| `v030-final-predictions.png` | Manual and agent-selected predictions for the first accepted final case, origin 2014-02-13T02:48 UTC. This is not the largest-improvement example. |
| `v030-goes-final.png` | All 2,694 accepted final GOES windows and saved selected-model predictions. |

Image intensity is training-normalized log1p AIA rate. Matched figures use intensity limits −2 to 3 and error limits 0 to 1 in both rows. The fixed disk mask defines which pixels contribute to error. GOES targets retain log10 XRS-B flux units; its score is never averaged with the image score.

The final image score is 0.11001095193834161, versus 0.1224417336622075 for the manual model and 0.12576198700564592 for persistence. The relative reduction against manual is 10.15%. These are 199 overlapping windows across two reserved days, one seed. The selected GOES model scored 2.468974582071028 versus persistence 0.19270602844340234. Its failure stays in the main sequence.

## Native product captures

Every `visual-v030-solar-*.png` is an actual product capture. Cropping enlarges the relevant screen region; full captures are linked from slides. A product screen is never generated artwork.

| Capture | Recorded identity and inspection task |
| --- | --- |
| `setup` | Native Copy to project dialog for Solar template `Tm90ZWJvb2s6MTU3NzU=`. The preview was unavailable in this browser. This is a dialog capture, not proof of a successful external copy. |
| `trace` | Setup conversation `4ca0a7e5c9d1fe30d24079ea5b98b750`; find the learner's attribute and returned environment. |
| `sweep` | Sweep `pzigourv`; inspect the six configurations, metrics, and runtime. |
| `evidence` | Round-one proposal conversation `23f4a8510534f241b9c6ccacb0ef3cb7`; inspect the validation evidence supplied to the agent. |
| `training` | Selected round-two training conversation `f7550caa1639e8366efbf9d84a782289`; inspect the actual configuration and result. |
| `artifact` | `execution-f7550caa1639e8366efbf9d84a782289:v0`, native `candidate.py` view; locate absolute loss and zero initialization. |
| `comparison` | Native Weave expanded first final agent-selected case: prediction mean −1.760701, target mean −1.759181, file_index 0, and masked error 0.109328. This is not a multi-version comparison or native EvalTables. |
| `report` | The current rehearsal Report, ID `VmlldzoxODMwMzU3Nw==`. |

Native EvalTables returned HTTP 500. The notebook comparison, Weave rows, and W&B Report remain available and retain their actual product names. Publication retries must reuse saved executions.

## Diagrams and setting

The original research-lab illustration supplies atmosphere. Its monitor and props are illustrative, and the opening dialogue is explicitly fictional. No generated scientific result is used.

`SolarMechanism.vue`, `ForecastWindow.vue`, `ResearchMap.vue`, and `ResearchBranches.vue` are editable SVG diagrams. They explain input shapes, residual addition, masked error, fixed versus trained weights, experiment records, and branching decisions. They do not claim a proposed edit improves quality. The mask picture is labeled an illustration of the calculation.

Solid branch lines carry code forward; dashed lines carry reviewed results. Selecting or retaining a version is a decision. Training it is an execution. Candidate colors identify alternatives and do not represent quality.

The participant uses their own project, credentials, and adjustable inference allowance. Training runs reviewed Python in the notebook environment. It does not require a remote Sandbox entitlement and is not a security sandbox. The research agent's model weights stay fixed while forecasting weights train normally.
