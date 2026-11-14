# Worked Solar diagrams

This pass replaces eight existing explanations without extending the 123-slide session. The editable diagrams live in `components/SolarWorked.vue`; `scripts/teaching_sequence.py` places them beside the relevant code. Each has three states and a text description.

| Slide identity | What the figure makes visible | Source or boundary |
| --- | --- | --- |
| `normalization-values` | One observation on log-flux and standardized axes, aligned around the training mean | `data/teaching-window.json`; target units do not change |
| `actual-baseline-error` | The distance between persistence and the observed +30-minute target | Same real February 1 window; one error is not the mean |
| `batch-indexing` | Paired errors versus an accidentally broadcast matrix | Labeled two-case arithmetic; not satellite measurements |
| `validation-code` | A training update followed by validation with unchanged weights | Training and scoring behavior in the existing runtime |
| `configs` | The six tested settings as a two-architecture, three-setting grid | Existing width, learning rate, batch, seed and update settings |
| `loss-change-effect` | Squared and absolute loss curves with their gradients at the same error | Labeled arithmetic; the reported metric remains fixed |
| `zero-head-gradients` | Why the output layer can learn while its initial weights block earlier gradients | One-feature derivation of the recorded residual-head edit |
| `repeatability` | Paired manual and agent-recipe errors for each of three seeds | `data/qualification-summary.json`, copied from the public evidence summary; seed 43 regresses slightly |

Existing images, forecasts, masks, loss histories, branches and native Forge captures remain in the deck. The new diagrams do not execute experiments. The three-seed chart repeats fixed code on the same dates, not three independent agent searches or unseen-date benchmarks.

Build and validate through `scripts/build_decks.py --only solar --pdf --validate`. The renderer checks every reveal, text bounds, answer links and PDF page. Screenshots and delivery receipts belong to that build, not to a new experiment.

## Delivery validation

The final build renders all 123 slides and 216 reveal states, including 216 PDF pages. `visual-validation.json` records source hashes, checks, and the preview provenance. `public/graphics-preview.png` is the final reveal of slide 78, captured from this build; it illustrates the loss calculation rather than a new experiment.
