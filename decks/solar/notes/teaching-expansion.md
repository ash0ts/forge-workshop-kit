# Six-hour Solar teaching sequence

The authored sequence is `scripts/build-storyboard.py` plus `scripts/teaching_sequence.py`. Both write the generated slides, presenter notes, and slide map. The slide map records each concept, notebook exercise, source, evidence type, reveal count, and timing block. Worked-answer links resolve from stable slide keys after insertion.

The main sequence has 107 slides; 16 reference and answer slides remain outside it. The session has 305 minutes of work and 55 minutes of breaks. The added time explains basic ML operations beside the real implementation, without adding training configurations, research rounds, or paid requests.

## Concrete objects retained across explanations

| Sequence | Object retained | New operation |
| --- | --- | --- |
| GOES window | February 1, 2014 at 01:00 UTC | History, target, normalization, persistence, error |
| Forecasting batch | Two channels and sixty samples per window | Index, flatten or convolve, predict one value |
| Training step | One set of current weights | Predict, calculate loss, differentiate, update |
| Image forecast | Earlier/current observations and the same future target | Normalize, predict correction, add, mask, score |
| Research change | Actual candidate source and its parent | Review, train, compose, test, adopt or retain |
| Final comparison | Saved source, weights and matched timestamps | Predict reserved inputs and report the fixed score |

The worked weighted sum and gradient are labeled arithmetic examples. The two-image score fixture is public checker data. Neither is presented as an observed solar execution. `data/teaching-window.json` is extracted from the pinned dataset; `scripts/prepare-teaching-window.py` reproduces it without training or network access.

`SolarComputation` now uses its reveal prop for normalization, MLP, CNN, training, loss and inference. `SolarMechanism` reveals masking operations. `SolarConcept` supplies window eligibility, tensor indexing context, the affine-unit calculation, filter sharing, gradient arithmetic, image axes, equal-image averaging, context boundaries, and tested adoption. Arrow meaning and scientific units remain explicit.

Four repeated storage-overview slides and the generic gaps statement were replaced with the worked explanations. The actual recorded GOES failure, known-date repair retest, image seed regression, and native comparison remain unchanged. The output-layer initialization explanation is now in the main sequence, with a separate account of how gradients reach the initially zero output layer.

The research-agent explanation follows the actual controller: Python reads the selected validation record, then builds a proposal request with source and allowed evidence. The model does not select that read operation. Forecast images remain available to participants; the proposal request sends metrics and loss history rather than image or prediction arrays.

Browser checks must cover every reveal, text line, SVG label, and worked-answer return. Inspect the actual screenshots at presentation size and half size, then render every PDF page. Passing DOM bounds alone does not establish that participants will understand an exercise; attendee and facilitator rehearsal remain separate checks.
