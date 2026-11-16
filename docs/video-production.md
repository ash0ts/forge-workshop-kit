# Make a narrated workshop video

Start with one customer problem and show the code, its output, and the Forge record that explains the result. Record those screens, then write narration that follows what the viewer can see. Use the [collection tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) as an example; its [source inventory](../media/walkthrough/README.md) identifies the captures and editable files.

This workflow produces a narrated MP4, a silent version for another presenter to dub, speech-aligned captions, a transcript, and a poster. It uses the existing Python environment, FFmpeg, and ElevenLabs. It does not run workshop experiments.

## Prepare the edit

Edit [edit.json](../media/walkthrough/edit.json) for chapter order, source captures, narration, crops, and reading holds. [audio.json](../media/walkthrough/audio.json) owns the voice, speech settings, and sound cues. For another workshop, copy those two manifests into its media directory and pass their paths with `--manifest` and `--config`.

Use actual browser captures for product interactions. Keep requests, values, source, and results readable. Crop signed-in account headers before distribution. Mark recorded executions and controlled examples as such. A guide animation must not imply that a model ran. Save a screenshot of the final public player and the product views used to verify it.

The current narrator is [Adam · Engineering Professor](https://elevenlabs.io/voices/QIhD5ivPGEoYZQDocuHI), voice ID `QIhD5ivPGEoYZQDocuHI`. Keep its ID in the audio configuration. Label the published video as using synthetic narration. The original silent edit remains available for a human voice-over.

## Plan and generate

Run commands from the repository root with uv and Python 3.11–3.13. The audio script declares its pinned Python dependencies; uv installs them on the first run. FFmpeg and FFprobe must be installed. [The capture guide](../media/walkthrough/README.md#rebuild-the-edit) gives the pinned rendering dependencies and command for rebuilding the silent edit.

```sh
# Offline: review timing windows, request count, and characters before spending credits.
uv run scripts/build_workshop_audio.py plan

# Generate one selected shot and listen to it first.
uv run scripts/build_workshop_audio.py generate --only introduction-00 \
  --env-file /absolute/path/to/models.env

# Generate the remaining selected requests, reusing the completed pilot.
uv run scripts/build_workshop_audio.py generate \
  --env-file /absolute/path/to/models.env
```

The env file may contain `ELEVENLABS_API_KEY` or `ELEVEN_LABS_API_KEY`. The reader extracts only those names without executing the file or expanding shell expressions. An already-set environment variable also works. Keep credentials out of source, command arguments, screenshots, and receipts. ElevenLabs credits are separate from each notebook's inference allowance.

Check pronunciation, pace, and delivery in the pilot. Shorten a sentence or extend its screen hold when it does not fit. Do not remove a qualification or change a measured result to improve the delivery. Brief sound cues can mark chapter changes; they must not imitate an error or success notification from the product.

## Align and mix

```sh
# Offline: require completed takes, matching hashes, and valid character timings.
uv run scripts/build_workshop_audio.py check

# Offline: produce narration and effects stems, the mix, MP4s, and captions.
uv run scripts/build_workshop_audio.py mix
```

The mixer also checks the silent video’s hash against its production receipt and verifies the recorded screens against the visual edit. Use `--video-receipt` and `--visual-manifest` only when selecting a different verified source edit. Narration wording may change; the screens and timing still need to match.

The captions use returned speech timestamps, adjusted by the saved shot start and any permitted tempo change. Do not reuse the silent edit's reading captions as speech timing. The current configuration leaves 0.65 seconds before speech and 0.30 seconds after it, permits at most 1.08× tempo, and targets −18 LUFS for narration and −32 LUFS for effects. These are the configured targets; listen to the result as well as checking the file.

Each completed take has a request hash, audio hash, voice and model IDs, alignment, and available provider history IDs. Repeating a completed request reuses its audio. If a request was interrupted after dispatch, its cost and outcome may be unknown. Check its receipt and provider history before retrying; the script stops instead of automatically generating another take. A rejected request can be retried explicitly with `--retry-rejected` after the cause is fixed.

Listen through the full mix while watching it. Check that each explanation lands on the right operation, that captions leave values visible, and that sound effects remain below speech. Inspect the beginning and end of every chapter. A duration check alone cannot establish that the narration teaches what is on screen.

## Keep the assets organized

Use a versioned collection name, such as `Forge Workshop Kit / Collection v0.12.0`. In the ElevenLabs Assets interface, group the approved files under `Narration`, `Sound effects`, and `Exports`. Use a workshop slug for a workshop-specific production. Upload only cropped public exports and the selected audio takes.

The organizer names media with its collection, take, and content hash. It can reuse finished uploads and reconcile an interrupted upload by exact name. A receipt lock rejects concurrent uploaders; after a killed process, check that process and the pending receipt before removing its lock. It does not generate audio, delete media, or change access.

```sh
# Offline plan for the selected, checked takes.
python scripts/organize_workshop_audio.py plan \
  --audio-index dist/walkthrough-production/audio/audio-index.json

# Read-only capability check, then explicit upload if Assets access is available.
python scripts/organize_workshop_audio.py check --env-file /absolute/path/to/models.env
python scripts/organize_workshop_audio.py upload \
  --audio-index dist/walkthrough-production/audio/audio-index.json \
  --env-file /absolute/path/to/models.env
```

To hand off the selected takes without calling ElevenLabs, build the local audio ZIP:

```sh
python scripts/organize_workshop_audio.py package \
  --audio-index dist/walkthrough-production/audio/audio-index.json
```

It includes named narration and effects files, character alignment, safe generation receipts, the selected index, and matching provider history references. It excludes raw responses, credentials, superseded takes, and the large mixed WAV stems. Repeating the same package produces the same bytes. Files are checked against their receipts before packaging.

For a finished mix, video, or poster, use `plan --file PATH` followed by `upload --file PATH`. Upload receipts preserve remote IDs locally and omit temporary signed download URLs. The [public Assets API](https://elevenlabs.io/docs/eleven-api/guides/how-to/image-and-video/references) supports upload and name search; folders are managed in the UI. Speech generation, Assets, and Studio have separate access requirements. If Assets access is unavailable, retain the local inventory and record that remote placement is unfinished. Do not describe generation history as an organized asset library.

## Publish and verify

[media/walkthrough/published.json](../media/walkthrough/published.json) identifies the selected media revision and file hashes. Each asset has a stable website `filename`; an optional `release_filename` names its dated GitHub release attachment. This allows new media on the existing release without overwriting its earlier assets. [scripts/stage_workshop_video.py](../scripts/stage_workshop_video.py) verifies that package and stages the video, captions, and poster under the website's own origin. Stage a verified local production with:

```sh
python scripts/stage_workshop_video.py \
  --manifest media/walkthrough/published.json \
  --source dist/walkthrough-production \
  --site dist/decks/site
```

For a build without local media, `--fetch` explicitly downloads only the manifest's named public Workshop Kit release assets. Every filename, byte count, and SHA-256 is checked before replacing the existing site's media. A mismatch stops staging and keeps the prior files. The deployment manifest is written last. This lets the public player use normal same-origin media requests instead of relying on a cross-origin release attachment.

Keep the original silent release unchanged. Publish a new media revision, then update the player, downloads, transcript, and synthetic-voice label together. Autoplay stays off. Check playback with sound, seeking, captions, and download links on the public desktop and narrow layouts. Save the browser check separately from local render checks; if public playback fails, leave that status explicit.

For external video viewers, use the registered video link in the [sharing guide](share-links.md). Coworker review uses the direct library URL. A video visit does not prove that someone copied a notebook or completed an exercise.
