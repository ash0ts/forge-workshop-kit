# Collection walkthrough

This is the source for a ten-minute tour of the six workshops. It shows browser interactions with teaching guides and saved Forge records. The November 16, 2026 revision adds ElevenLabs narration, captions timed to the generated speech, and short transition sounds. The original silent release remains available.

The recording covers the v0.12.0 source release. Product screens show the records available when captured; the workshop start pages provide the current template, copy instructions, and import and laptop alternatives.

[edit.json](edit.json) owns chapter order, source captures, crops, labels, reading holds, and narration for each shot. Captions stay within the shot that shows their subject. [narration.md](narration.md) is generated from it and gives the script for a voice-over. The same words appear in the captions. [audio.json](audio.json) selects the voice, generation settings, and sound cues. [Video production](../../docs/video-production.md) explains generation, alignment, mixing, asset organization, and public playback checks.

## Use the recording

Watch the [narrated walkthrough](https://ash0ts.github.io/forge-workshop-kit/walkthrough/). These stable website links follow the selected media revision:

- [Captioned MP4 with narration](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-narrated-captioned.mp4), ready to attach to a message.
- [Clean MP4 with narration](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-narrated-clean.mp4), without burned-in captions.
- [SRT](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-narrated.srt) and [VTT](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-narrated.vtt), derived from the speech timestamps.
- [Selected audio assets](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-audio-assets.zip), including the original takes, alignment, receipts, and provider history references.
- [Editable video package](https://ash0ts.github.io/forge-workshop-kit/walkthrough/media/forge-workshops-video-edit.zip), with the current cropped clips, timing, narration script, and silent exports for another voice-over.

The narrated revision is archived under dated filenames such as `forge-workshops-narrated-captioned-20261116.mp4`. Its editable video ZIP is `forge-workshops-video-edit-20261116.zip`. The original [silent captioned MP4](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-captioned.mp4), [silent clean MP4](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-clean.mp4), and [original edit package](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-video-edit.zip) retain their existing release URLs. Use the script and captions from the matching revision when dubbing.

The production build writes these files into `dist/walkthrough-production/`:

- `forge-workshops-captioned.mp4`: 1920 × 1080, captions below the screen, no audio. Attach this when a silent preview is useful.
- `forge-workshops-clean.mp4`: the same edit without burned-in captions. Record a voice-over using `narration.md` and import the SRT into your editor.
- `forge-workshops.srt` and `forge-workshops.vtt`: timed captions.
- `index.html`: local video player with captions below the product screen; serve the directory over localhost.
- `poster.png`, `contact-sheet.png`, and `stills/`: cover image and chapter review frames.
- `production-receipt.json`: sources, capture timing, crops, hashes, reading holds, and export checks.
- `forge-workshops-video-edit.zip`: both exports, subtitles, narration, cover, chapter stills, and the already-cropped clips. `edit-final-cut.json` places those clips on an editable timeline.

The local build's unprefixed MP4s contain no audio and use the current edit timings. They are inputs to the narration mix and can also be used for a human dub. They do not overwrite the original release files. Check subtitle timing after changing the script or speaking speed.

For an external video audience, accompany the recording with **https://utm.io/uuIan**. External community Slack uses **https://utm.io/uuIaS**. For colleague review, use the direct [library link](https://ash0ts.github.io/forge-workshop-kit/) rather than an acquisition link. [Tracking definitions](../../docs/share-links.md) explain what those visits do and do not measure.

## Rebuild the edit

The source captures live in `dist/walkthrough-production/raw/<capture-name>/`. Each directory contains PNG browser frames and `capture.json`, whose frame timestamps determine playback. Raw frames stay outside Git and the distribution ZIP because their uncropped headers can contain the signed-in account. The ZIP includes cropped clips suitable for editing; share raw captures only through an approved internal handoff.

Install FFmpeg from [its official download page](https://ffmpeg.org/download.html) or your platform's package manager. The production used FFmpeg 8.1.2. Rendering uses Pillow and bundled IBM Plex fonts; it does not depend on FFmpeg's optional libass subtitle renderer.

```sh
uv run --no-project \
  --with pillow==12.3.0 --with fonttools==4.68.0 --with brotli==1.2.0 \
  python scripts/build_collection_video.py
```

`--prepare-only` generates the narration and subtitle assets and reports missing captures. `--chapter pending` renders that chapter's shots for layout review. Missing sources stop the full render; the builder never fills a missing product screen with an invented one.

Native Forge captures omit the signed-in account header with an explicit crop. The product record stays visible. Full screens keep their aspect ratio and fit within the same viewing area. Captions occupy a separate strip, and labels distinguish controlled teaching examples from saved executions.

After rendering, inspect the contact sheet, each chapter, and the transitions. The builder checks duration, dimensions, subtitle bounds, and the absence of audio, but those checks cannot establish that the selected screens explain the narration.


## Audio and publication records

Follow [video production](../../docs/video-production.md) to generate and mix narration or prepare another workshop video. The current selected voice is `QIhD5ivPGEoYZQDocuHI`, saved in the account as `Workshop Kit · Adam — Engineering Professor`.

The audio build adds these files under `dist/walkthrough-production/`:

- `audio/`: per-take audio, request and hash receipts, alignment, selected `audio-index.json`, and provider history references.
- `narration.wav`, `sound-effects.wav`, and `mix.wav`: separate stems and the combined soundtrack.
- `forge-workshops-narrated-clean.mp4` and `forge-workshops-narrated-captioned.mp4`: the selected voice and effects over the same recorded screens.
- `forge-workshops-narrated.srt` and `.vtt`: captions derived from actual speech timestamps.
- `mix-receipt.json`: source hashes, selected takes, timing, and output hashes.
- `audio-validation.json`: measured stream durations, loudness, caption count, and sampled screen checks.
- `audio/asset-library-receipt.json`: ElevenLabs Assets identities after verified uploads; it contains no temporary signed download URLs.
- `forge-workshops-audio-assets.zip`: the selected original narration/effects, alignment, safe receipts, and provider history index. It excludes raw responses, superseded takes, and the large mixed WAV stems.

[published.json](published.json) selects the media revision staged onto the public website. It is separate from the notebook runtime version. The old silent files and immutable v0.12.0 release stay intact.

The November 16 mix contains 26 narration clips, two reusable transition sounds, and 142 caption cues. Both MP4s have exactly 600 seconds of audio and video; the three WAV stems each contain 28,800,000 samples at 48 kHz. Automated timing and sampled visual checks passed. A human listening review has not been completed.

Speech generation and its history references are saved. A native ElevenLabs Assets folder was created, but the upload opened a blank page and asset placement has not been verified. The Assets API returned `missing_permissions` for `image_video_generation`; Studio returned `invalid_subscription` because its API requires separate enablement. Use the local audio ZIP and index until the existing folder can be checked. Do not change credentials or broaden permissions merely to organize these files.
