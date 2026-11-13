# Build a research loop, then give it an agent

This four-hour deck accompanies the Solar Autoresearch notebook. Participants write a solar forecast, save and compare its experiments in Forge, then ask a research agent to propose changes to the code. The setting is the Solar Forecasting Lab; Pending, Inc. remains the separate office workshop.

Start with the [Solar notebook template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view). Choose **Copy to project**, open your copy in **Edit**, and follow the **Connect** step. Each participant uses their own project and account. There is no workshop gateway or host token.

## Present the workshop

```sh
npm ci
npm run dev
```

Open the URL printed in the terminal. Use `/presenter/1` for the speaker notes. Node.js 22.22 or newer is required. Fonts and images are included, and opening the deck does not train models or send model requests.

The deck has 73 main frames and 21 optional worked-answer, recorded-evidence, and reference frames. The main sequence builds diagrams a step at a time, then pauses for participants to work in the notebook. Keep each exercise slide visible while they code. Its button names match the notebook, and its worked-answer link returns to the exercise.

The speaker notes explain what to demonstrate, where to pause, and what participants should inspect. Most of the four hours is for coding and discussion. The opening scene with four notebooks called final is fictional. Forecasting results come from the recorded rehearsal. Native Forge screens show those saved runs, Artifacts, traces, and Reports. Four optional frames at the end walk through the separate current Pending workshop; they do not change the Solar exercise sequence. Click any product capture to inspect it at full resolution.

## Use the browser copy or PDF

```sh
npm run build
npm run export -- --executable-path '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

Use your installed Chrome path for the PDF export. The browser output is in `dist/`. Run `python3 dist/serve.py` on macOS/Linux or `py dist/serve.py` on Windows, then open the printed address.

The PDF includes all incremental frames and linked worked answers. In the browser, you can also select branches and reveal the settings behind two recorded runs. Separate static frames keep those explanations readable in the PDF.

## Edit the deck

Edit `scripts/build-storyboard.py`, then run:

```sh
python3 scripts/build-storyboard.py
```

This regenerates `slides.md`, the slide map, and presenter notes. Diagram components live in `components/`; colors, typography, and spacing live in `style.css`. The laboratory artwork is an illustration. Keep it distinct from the saved product captures and forecast images.

## Use the recorded example

One complete November 13 rehearsal supplies the recorded scores, forecasts, code changes, and Agent Lens links. The image model’s error fell 10.15% relative to the manually selected model on 199 overlapping windows across two reserved days, using one seed. The GOES model performed worse than persistence. Both results remain in the main teaching sequence.

`public/recorded-study.json` contains the saved source, settings, decisions, scores, and links behind those examples. Attendees’ edits need their own executions and results.

The small forecasting models train their weights. The research agent’s weights stay fixed while it proposes changes to model and training code. Both improvement rounds use validation results; the final comparison loads the selected weights and predicts the reserved dates.

Native EvalTables returned HTTP 500 during the rehearsal. Use the saved notebook and Weave comparisons if that view is unavailable. Retrying publication can use the completed results without rerunning training.

[Workshop source and setup](https://github.com/ash0ts/forge-workshop-kit) · [Source notes](notes/sources.md)

## Check and package changes

After PDF export, run `uv run --no-project --with pymupdf python scripts/finalize-pdf.py` to check every page and convert worked-answer links to internal PDF destinations. `scripts/check-render.mjs` checks the browser layouts and navigation. The answer, exercise-contract, and recorded-evidence checks cover code examples, notebook controls, and the saved results without training or model calls.

For GitHub Pages, run `npm run build:pages`. It writes `dist-pages/` with the `/forge-workshop-kit/solar/` prefix and a page for every slide route. Publish that directory at `solar/`. Run `node scripts/check-pages.mjs` to check direct links, worked answers, images, and presenter navigation.
