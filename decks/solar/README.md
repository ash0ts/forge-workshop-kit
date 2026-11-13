# Build a research loop, then give it an agent

A four-hour Slidev companion to the Solar Autoresearch notebook, set in the Solar Forecasting Lab. The visual style and incremental teaching sequence follow the Pending, Inc. Harness² workshop. This deck teaches the participant-owned Forge Workshop Kit setup.

Open the [Solar notebook template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view), choose **Copy to project**, and work in your own project. No workshop gateway or host token is involved.

## Present

```sh
npm ci
npm run dev
```

Open the URL printed in the terminal. The presenter view is `/presenter/1`. Node.js 22.22 or newer is required. Fonts and images are bundled. Slides make no training or model requests.

The deck has 73 main frames and 17 optional worked-answer, recorded-evidence, and reference frames. Many main frames reveal one part of the same diagram. Exercises occupy most of the four-hour schedule.

## Portable deck and PDF

```sh
npm run build
npm run export -- --executable-path '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

The browser package is `dist/`. Run `python3 dist/serve.py` on macOS/Linux or `py dist/serve.py` on Windows, then open the printed local address. The PDF includes every incremental frame. The branch inspector is interactive in the browser and a labeled diagram in the PDF. The run-configuration inspector also has a separate static reveal frame, so the PDF preserves its explanation.

## Edit

The storyboard is `scripts/build-storyboard.py`. Run `python3 scripts/build-storyboard.py` to regenerate `slides.md`, the slide map, and presenter notes. Edit diagram components in `components/` and the shared visual rules in `style.css`.

Speaker notes distinguish actual observations, explanatory diagrams, and fictional dialogue. The opening is an original scene in a computational research lab. The pixel observatory artwork is illustrative; product screenshots and forecasts are recorded evidence. Recorded results come from one complete November 13 rehearsal of the revised notebook. Learner changes must produce their own results.

Pending, Inc. keeps its office setting. This deck uses the same visual and teaching conventions for a separate research-lab workshop.

## Evidence

The recorded forecast images and scores come from the saved browser rehearsal. `public/recorded-study.json` preserves the source, configurations, metrics, decisions, and verified trace links used by these examples. The recorded research-agent conversation is linked directly. Native EvalTables returned HTTP 500 in the rehearsal; the deck teaches the saved notebook and Weave comparisons and publication-only recovery. It does not relabel a W&B Table as native EvalTables.

The forecasting models train weights. The research agent’s weights remain fixed. Two rounds edit the image experiment, using validation evidence only. Final evaluation loads frozen weights on reserved dates.

Full source and setup: https://github.com/ash0ts/forge-workshop-kit

After PDF export, `uv run --no-project --with pymupdf python scripts/finalize-pdf.py` checks every page and converts worked-answer links into internal PDF destinations. `scripts/check-render.mjs` checks the browser deck, branch interaction, and answer navigation against its generated slide map. `scripts/check-answers.py` validates the code examples without training or provider calls. `scripts/check-exercise-contract.py` reconciles the slide instructions with the authored notebook controls and functions.

For GitHub Pages, run `npm run build:pages`. It builds `dist-pages/` with `/forge-workshop-kit/solar/` paths and restores the portable source afterward. Copy that folder into `solar/` under the Pages site. Use its `404.html` as the site root fallback so direct slide links reload.
