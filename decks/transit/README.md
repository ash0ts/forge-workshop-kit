# Transit software-factory workshop deck

**Technical preview.** The deck builds and its interactions have been checked. Live worker execution and native Forge readback are recorded; workshop readiness still requires an external-account check and a human rehearsal.

A six-hour companion to the current Transit notebook. Participants build a historical MBTA departures board, write a small task coordinator, run two coding workers, review and integrate their changes, and test whether checked project lessons help a later feature.

Edit `scripts/build-storyboard.py` and its `scripts/depth-sequences.py` extension, then regenerate `slides.md`. The six-hour schedule includes breaks at 1:35–1:45, 3:00–3:20 and 4:45–4:55. The editable Vue/SVG diagrams keep task, worker, integration and memory positions stable across reveals. Presenter notes and worked-answer links are generated from the same storyboard. Native product screenshots are added only after the corresponding transit publication has been read back; the reference-app screenshot is labeled separately from agent results. Source hashes and its unedited original are retained.

```sh
npm ci --prefix ..
python3 scripts/build-storyboard.py
npm run dev
npm run build
npm run export
```

The repository build command will generate browser and source bundles, a PDF containing the meaningful reveals, and delivery checks. Building or opening the deck makes no model requests. The data receipt in the notebook identifies the public archive, retained rows and source checksum.

See the [workshop guide](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/transit-workshop.md) for setup and technical boundaries and the [facilitator script](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/transit-facilitator.md) for the schedule. The working lesson requires an actual attendee access check and a human rehearsal before it is described as ready for a live class.

The captioned browser recording is `public/walkthrough/worked-example.mp4`. Its adjacent `index.html` provides chapter navigation and a transcript. It shows worked code edits, free local checks and the reference application, with no model calls. The native R3 Agent Lens capture is separate and explicitly labeled. Capture and recording receipts preserve the distinction between reference output, recorded worker behavior and integrated product results.

The player links a separate `transit-reference-app.zip`. This is the instructor-authored application shown in the recording, with its 18 passing reference checks. It includes historical MBTA data and runs locally with `uv run --with marimo marimo edit app.py`; it makes no model calls.

A second recording, `public/walkthrough/recorded-result.mp4`, follows actual saved R4 executions through the task board, query patch, matching Agent Lens test span, native aligned evaluation and exported team app. It records navigation of existing results, not new inference. The player states the first-release passes and the failed follow-ups separately.
