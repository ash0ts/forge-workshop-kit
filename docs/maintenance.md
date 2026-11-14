# Build and publish the workshop

`pyproject.toml` owns the package version. `src/forge_workshop_kit/workshops.json` owns template names, exercise labels, dependency extras and workflow compatibility. Leave the workflow version unchanged for copy or packaging changes so saved experiments remain usable.

## Build locally

```sh
uv sync --frozen --all-extras
uv run --all-extras python scripts/build_release.py
```

This generates the notebooks, checks them, exports previews without participant credentials, and packages the wheel and source archive in `dist/v<VERSION>/`. It also records file hashes in `release-manifest.json`. Nothing is published and no exercise runs. Use `--only starter` or another manifest slug when building one template.

The notebook generator exports dependency pins from `uv.lock`. Do not hand-edit generated notebook headers. Acquisition tools use the separate `data-prep` group; participants receive prepared datasets.

Notebook generation also checks the uv version in `tool.workshop-build.uv-version` in `pyproject.toml`; CI reads that same value. Different uv releases can format equivalent dependency markers differently. Install the declared build version before generating notebooks. When upgrading it, regenerate the headers in the same change. Participants can use other uv versions to run the notebooks.

## Publish explicitly

First upload the matching wheel to the repository's versioned GitHub release. Then run:

```sh
uv run --all-extras python scripts/publish_templates.py \
  --project YOUR_ENTITY/YOUR_PROJECT \
  --build dist/v0.6.0
```

The publisher checks the public wheel and every selected source/preview hash before uploading. It keeps destination-specific receipts under `.workshop-deployments/`, verifies each notebook's destination project before updating it, and reads back the uploaded files. `--only` selects a template. Repeating the command resumes incomplete publication and skips matching uploads.

If notebook creation was interrupted before its ID was saved, the publisher stops rather than creating another copy. Find the notebook in the destination project and pass `--notebook-id SLUG=ID`. Use `--adopt-ids` to import the old unscoped receipt only after every listed destination has been verified.

Existing attendee copies are separate notebooks. Updating the templates does not replace them. Keep previous release assets and the recorded teaching evidence; do not rewrite Git history or delete participant state.

## Build the companion decks

The current decks live in `decks/pending`, `decks/solar`, `decks/routing`, `decks/inspection`, and `decks/transit`. Their storyboards generate the slides and presenter notes. Shared branch colors, labels and recorded-example identities live in `src/forge_workshop_kit/assets/visuals.json`. The official Slidev skill is pinned under `.agents/skills/slidev`, with its upstream revision in `UPSTREAM.md`. From the repository root, run:

```sh
python3 scripts/build_decks.py --install --pdf --validate
```

Use Node.js 22.23.2 or later and `uv`. PDF export needs Chrome; set `CHROME_PATH` to your installed browser executable, or install the deck's Playwright Chromium with `npx playwright install chromium` from `decks/solar`. The PDF checker installs its own pinned maintenance dependencies through `uv`; it does not add them to participants' notebooks.

The build writes browser decks to `dist/decks/site/` and PDFs, offline browser bundles, and editable source archives to `dist/decks/downloads/`. It checks each slide and reveal, exercises Back, renders every PDF page, checks image loading, and follows worked-answer links back to their exercises. PDF links use slide identities rather than physical page numbers, because a reveal adds a page. Use `--only transit` or another workshop name while editing one deck. Without `--pdf` and `--validate`, the command only builds browser copies and source archives.

Opening or building a deck sends no training or inference requests. The command does not publish. The `Workshop decks` GitHub Actions workflow publishes the validated site when a deck change reaches `main`, preserving each workshop’s address. Previous GitHub release attachments remain unchanged.

## Saved work

The shared library has no runtime dependency on `common_tools`, an operator checkout or any gateway. Authentication comes from the participant's Forge runtime or local W&B login. `.workshop/` contains their drafts and execution receipts. Do not treat it as disposable build output.

In the old operator repository, `dist/participant` is an independent Git checkout. Both builders that wrote into it are now retired. Its history was bundled before changing current setup links. It remains in place with the self-service release intact.

Use the [release checks](release-checks.md) to distinguish code/browser validation from external-account access and human rehearsal.
