# Solar forecasting with agent-assisted experiments

This four-hour deck accompanies the Solar Autoresearch notebook. Participants use GOES X-ray measurements to forecast flux thirty minutes ahead, then use AIA images to predict an image one hour ahead. They implement persistence, train small models, and save the code, settings, and outputs needed to compare results. Once that comparison works, a research agent proposes changes to the image model’s training code. Participants review the diffs and test their effect on forecast error. The setting is a fictional lab’s weekly forecast review. Participants bring a result, its saved code, and a next experiment. Pending, Inc. remains the separate office workshop.

Start with the [Solar notebook template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view). Choose **Copy to project**, open your copy in **Edit**, and follow the **Connect** step. Each participant uses their own project and account. There is no workshop gateway or host token.

## Present the workshop

```sh
npm ci
npm run dev
```

Open the URL printed in the terminal. Use `/presenter/1` for the speaker notes. Node.js 22.22 or newer is required. Fonts and images are included, and opening the deck does not train models or send model requests.

The deck has 87 main frames and 18 optional worked-answer, recorded-evidence, and reference frames. The main sequence builds diagrams a step at a time, then pauses for participants to work in the notebook. Keep each exercise slide visible while they code. Its button names match the notebook, and its worked-answer link returns to the exercise.

The speaker notes explain what to demonstrate, where to pause, and what participants should inspect. Most of the four hours is for coding and discussion. The opening scene with four notebooks called final is fictional. Forecasting results come from the recorded rehearsal. Native Forge screens show those saved runs, Artifacts, traces, and Reports. Click any product capture to inspect it at full resolution.

## Build the browser copy and PDF

From the repository root, run the shared build command:

```sh
python3 scripts/build_decks.py --only solar --install --pdf --validate
```

This builds the browser deck, exports the PDF, and checks every slide and PDF page. It requires Chrome. The browser copy is written to `dist/decks/site/solar/`; the PDF, offline browser bundle, and editable source archive are in `dist/decks/downloads/`.

The PDF includes all incremental diagrams and worked-answer links. In the browser, participants can also select branches and reveal the settings behind two recorded runs. Separate static frames keep those explanations readable in the PDF.

## Edit the deck

Edit `scripts/build-storyboard.py`, then run:

```sh
python3 scripts/build-storyboard.py
```

This regenerates `slides.md`, the slide map, and presenter notes. Diagram components live in `components/`; colors, typography, and spacing live in `style.css`. The [visual guide](notes/visual-upgrade.md) maps each explanation to its code or saved data. The laboratory artwork is an illustration. Keep it distinct from the saved product captures and forecast images.

## Use the recorded example

One complete November 13 rehearsal supplies the recorded scores, forecasts, code changes, and Agent Lens links. The image model’s error fell 10.15% relative to the manually selected model on 199 overlapping windows across two reserved days, using one seed. The GOES model performed worse than persistence. Both results remain in the main teaching sequence.

`public/recorded-study.json` contains the saved source, settings, decisions, scores, and links behind those examples. Attendees’ edits need their own executions and results.

The small forecasting models train their weights. The research agent’s weights stay fixed while it proposes changes to model and training code. Both improvement rounds use validation results; the final comparison loads the selected weights and predicts the reserved dates.

Native EvalTables returned HTTP 500 during the rehearsal. Use the saved notebook and Weave comparisons if that view is unavailable. Retrying publication can use the completed results without rerunning training.

[Workshop source and setup](https://github.com/ash0ts/forge-workshop-kit) · [Source notes](notes/sources.md)

## Check and package changes

Use the shared build command above for the final browser, PDF, navigation, and image checks. The answer, exercise-contract, and recorded-evidence checks verify code examples, notebook controls, and the saved results without training or model calls.

See [deck build and publication instructions](../../docs/maintenance.md) for publishing the generated files. Publishing is a separate action from building.
