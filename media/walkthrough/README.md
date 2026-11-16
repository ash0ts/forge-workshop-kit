# Collection walkthrough

This is the source for a ten-minute, silent tour of the six workshops. It shows real browser interactions with teaching guides and saved Forge records. It does not claim to be a new live experiment or a full workshop rehearsal.

The recording covers the v0.12.0 source release. At capture time, existing hosted templates remained on the previous revision because Forge notebook-management access was blocked. The setup chapter says so; the start pages also provide import and laptop paths.

[edit.json](edit.json) owns chapter order, source captures, crops, labels, reading holds, and narration for each shot. Captions stay within the shot that shows their subject. [narration.md](narration.md) is generated from it and gives the script for a voice-over. The same words appear in the captions.

## Use the recording

Watch the [public walkthrough](https://ash0ts.github.io/forge-workshop-kit/walkthrough/), or download the [captioned MP4](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-captioned.mp4), [clean MP4 for dubbing](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-clean.mp4), or [editable video package](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-video-edit.zip).

The production build writes these files into `dist/walkthrough-production/`:

- `forge-workshops-captioned.mp4`: 1920 × 1080, captions below the screen, no audio. Attach this when a silent preview is useful.
- `forge-workshops-clean.mp4`: the same edit without burned-in captions. Record a voice-over using `narration.md` and import the SRT into your editor.
- `forge-workshops.srt` and `forge-workshops.vtt`: timed captions.
- `index.html`: local video player with captions below the product screen; serve the directory over localhost.
- `poster.png`, `contact-sheet.png`, and `stills/`: cover image and chapter review frames.
- `production-receipt.json`: sources, capture timing, crops, hashes, reading holds, and export checks.
- `forge-workshops-video-edit.zip`: both exports, subtitles, narration, cover, chapter stills, and the already-cropped clips. `edit-final-cut.json` places those clips on an editable timeline.

The MP4s contain no music, narration, or other audio. They can be used as a base for a human dub. Check subtitle timing after editing or changing the narration speed.

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
