# Airline monitoring

A six-hour workshop following a passenger request through an airline agent, human review, a monitoring rule, a regression case, and a tested repair. The bookings are simulated records adapted from a pinned public benchmark. A successful booking API call can still produce the wrong itinerary.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) · [Facilitator runbook](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/airline_monitoring-runbook.md) · [Presenter notes](notes/presenter.md)

## Edit and check

Edit `scripts/build-storyboard.py`; it generates the slides, presenter notes, and slide map. `AirlineMechanism.vue` contains the itinerary replacement, tracing, monitoring denominators, regression reconstruction, and matched-comparison diagrams. The same objects remain visible across reveals, with text descriptions and intermediate PDF states. Follow the [shared deck instructions](../README.md) to preview, build, and validate.

`data/native-captures.json` identifies each native image, source URL, and annotation. Keep the originals unchanged. The [visual map](notes/visual-coverage.json) connects diagrams to the operation they explain. Simplified itinerary labels and arithmetic examples are illustrations, not recorded agent outcomes.

## Recordings and qualification

The [captioned guide](public/walkthrough/index.html) uses saved v0.8.0 rehearsal screens. Its video, keyboard chapter navigation, and transcript preview the workshop; they do not show live clicks or every later revision. The ARIA investigations have their own actual responses and checked sources.

After browser validation, regenerate that guide from the repository root with:

```sh
python3 decks/airline_monitoring/scripts/build-walkthrough.py
```

Video rendering needs Pillow, ffmpeg, and a local font supplied through `--font`; the default is macOS Arial Unicode. `--skip-video` regenerates only HTML, transcript, and source manifest. The input captures must exist in the deck's `.screenshots` directory.

This remains a technical preview. All forty recorded agent conversations passed booking checks, so the live comparison shows a tie. Native AI Alignment requests returned HTTP 500, and the session had no completed Insights cluster. [Qualification](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/airline-monitoring-qualification.md) keeps those missing monitoring results separate from booking correctness. Do not turn an illustration into a claim that the native exercise passed.
