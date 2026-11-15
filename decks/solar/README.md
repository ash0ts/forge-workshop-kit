# Solar forecasting with agent-assisted experiments

This six-hour workshop follows a research lab preparing its weekly forecast review. Participants use real GOES measurements to forecast X-ray flux thirty minutes ahead, then AIA images to predict an image one hour ahead. They implement persistence, train small models, and save enough code, settings, and outputs to reproduce the comparison. A research agent then proposes changes to the image model's training code.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/solar/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) · [Facilitator runbook](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/facilitator.md) · [Presenter notes](notes/facilitator-notes.md)

## Edit and check

Edit `scripts/build-storyboard.py` and `scripts/teaching_sequence.py`, then regenerate the slides, slide map, and presenter notes. Diagram components live in `components/`; typography and spacing live in `style.css`. Follow the [shared deck instructions](../README.md) to preview, build, and validate.

The browser includes selectors for saved branches and configurations. The PDF preserves the explanatory reveal states and worked answers. Keep an exercise slide visible while participants code; its functions and buttons correspond to the authored notebook cells.

## Recorded examples

The lab and its four notebooks named `final` are fictional. The observations, forecasts, source changes, and Forge records are real. `public/recorded-study.json` contains the original November 13 rehearsal: image error fell from 0.122442 to 0.110011 compared with the manual model, while the GOES model lost to persistence. The image result covers 199 overlapping windows on two days with one seed.

The later [three-seed qualification](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md) preserves a mixed image result and a successful combined GOES repair. Those are teaching retests on previously inspected dates. Keep them separate from the original rehearsal and from a learner's live results. The [evidence review](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-evidence.md) explains the source data and limits.

The forecasting models train their weights; the research agent stays fixed while proposing Python changes. Development investigations use validation records. Frozen measurement and image comparisons remain separate because their metrics measure different tasks.

[Source notes](notes/sources.md) identify captures and figures. [Earlier design notes](../README.md#earlier-design-notes) preserve prior visual mappings and validation history. Current slide identities and exercise references live in `notes/slide-map.json`.
