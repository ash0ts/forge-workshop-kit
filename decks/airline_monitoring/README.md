# Airline monitoring deck

The authored source is `scripts/build-storyboard.py`. It generates `slides.md`, presenter notes, and the slide map used by browser/PDF validation. The session follows one itinerary through observation, native tag review, regression-case curation, a code repair, matched evaluation, and subsequent monitoring.

The deck uses the Workshop Kit's shared pinned Slidev toolchain. From the repository root:

```sh
python scripts/build_decks.py --only airline_monitoring --pdf --validate
```

No workshop execution, training, inference, or publication occurs during this build. Use Node.js 22.23.2 or later and the existing locked dependencies in `decks/`.

The simplified itinerary labels and arithmetic examples are explicitly identified as illustrations. Native captures are included only when `data/native-captures.json` identifies an existing image, source URL, and annotations. The original images remain unchanged. Missing native verification does not become a successful exercise through a diagram.

See the [facilitator runbook](../../docs/airline_monitoring-runbook.md) for the six-hour schedule and recovery instructions. The notebook's manifest and authored cells own exact learner function and control names.

The [recorded guide](public/walkthrough/index.html) follows 13 saved screens in 3 minutes 42 seconds. It includes a captioned MP4, keyboard chapter navigation, and a transcript. It is assembled from the verified deck and native rehearsal captures; it does not depict live clicks. The video preserves the captured screen and places captions below it.

After validating the deck, regenerate the guide with `python decks/airline_monitoring/scripts/build-walkthrough.py` from the repository root. Video rendering needs Pillow, ffmpeg, and a local font supplied through `--font` (the default is macOS Arial Unicode). `--skip-video` regenerates only the HTML, transcript, and source manifest. The source captures must be present in the deck's `.screenshots` directory from browser validation.
