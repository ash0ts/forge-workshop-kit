# Build and publish

Building produces local files. Publishing updates a named Forge project or the public deck site. Keep those operations separate so a contributor can inspect a change before it becomes a participant template.

[pyproject.toml](../pyproject.toml) owns the package version. [workshops.json](../src/forge_workshop_kit/workshops.json) owns workflow compatibility and template metadata. A wording or packaging change does not require a new workflow identity. Current release status and outstanding checks live in [next-up.md](../next-up.md); detailed evidence belongs in [release checks](release-checks.md).

## Prepare the build

Run from the source checkout. Install the build uv version reported by `python scripts/release_support.py --uv-version`, then install the locked maintainer dependencies:

```sh
uv sync --frozen --all-extras
```

The generator derives hosted notebook dependencies from `uv.lock`. Do not edit generated headers. If the build uv version changes, regenerate and review the headers in the same change. Data acquisition uses the separate `data-prep` dependency group; ordinary builds use prepared data.

## Build notebooks and packages

Build all templates:

```sh
uv run --all-extras python scripts/build_release.py
```

The command generates and checks notebooks, exports previews with credentials removed, and writes the wheel, source archive, ARIA recording bundle, and `release-manifest.json` to `dist/v<VERSION>/`. It runs no workshop exercises and publishes nothing. The manifest records file hashes and workflow identities.

For one template, use `--only request_routing`. For a scratch build that should not replace your local release directory, use `--output PATH`. Inspect the package allowlist in `pyproject.toml` whenever adding files that source archives need. Keep local journals, credentials, deployment receipts, downloaded training outputs, and operator backups out of distribution files.

`forge-workshop build request_routing --install --pdf --validate` is the combined one-workshop command: it builds the template package and its mapped deck. Use the script commands when you need separate destinations or only one type of output.

## Build the decks

All decks share the locked toolchain in [decks/package.json](../decks/package.json) and its lockfile. Use Node.js 22.23.2 or later, uv, and Chrome for PDF export:

```sh
python scripts/build_decks.py --install --pdf --validate
```

Use `--only routing` while editing one deck. Set `CHROME_PATH` to an installed Chrome executable, or run `npx playwright install chromium` from `decks/`. The PDF checker installs its pinned maintenance dependencies through uv; those dependencies are not added to participant notebooks.

Output goes to `dist/decks/site/` for the hosted site and `dist/decks/downloads/` for PDFs, offline browser decks, and editable source archives. `--output PATH` selects another root. Without `--pdf --validate`, the command builds browser copies and source archives only.

Validation checks slide and reveal states, Back navigation, worked-answer return links, image loading, and rendered PDF pages. Inspect the changed screens yourself as well: container bounds alone do not establish readable text or useful annotations. The [deck guide](deck-guide.md) covers presentation and the [teaching sequence](teaching-sequence.md#use-consistent-visual-conventions) defines the shared diagram conventions.

The [Workshop decks workflow](../.github/workflows/deck.yml) publishes validated site output after matching changes reach `main`, or by explicit workflow dispatch. It does not upload assets to a GitHub release or publish Forge templates.

## Publish Forge templates

Upload the matching wheel to the versioned GitHub release first. The template publisher downloads that public wheel and verifies its hash against the build. Then publish to an explicit destination:

```sh
uv run --all-extras forge-workshop publish request_routing --project YOUR_ENTITY/YOUR_PROJECT
```

To publish all built templates:

```sh
uv run --all-extras python scripts/publish_templates.py --project YOUR_ENTITY/YOUR_PROJECT
```

The publisher selects `dist/v<VERSION>/` by default; `--build PATH` selects another build for the same package version. It checks source and preview hashes before uploading, verifies each existing notebook's project, and reads back the uploaded files. Receipts live under `.workshop-deployments/<entity>/<project>/`. Rerunning the same command resumes incomplete publication and skips matching uploads.

If creation was interrupted before the notebook ID was saved, the publisher stops. Locate the notebook in the destination project, then use the script's `--notebook-id SLUG=ID` option to resume. Do not delete the pending receipt to force another creation. The script also accepts `--adopt-ids PATH` for an older unscoped receipt and verifies every destination before importing IDs.

Updating a template leaves attendee copies unchanged. Do not replace prior release assets under the same filename, move a published tag, or delete saved participant state. Corrections to an existing release need a separately named artifact or a new version, with the difference described in its release notes. Historical gateway material belongs in the [archive](archive.md), not current setup instructions.

## Record what shipped

Keep the source commit, package hashes, template destination/readback receipt, deck validation, and unresolved access checks together for each release. Verify the public links after publication. Do not promote a workshop's readiness because its build succeeded: browser, external-account, native-feature, and human-rehearsal evidence remain separate.

For an interrupted upload, retry publication from the existing build and saved execution records. For an execution recovery, follow [setup and recovery](setup.md) and the [technical specification](../techspec.md). A successful execution with an unavailable export must not be rerun merely to obtain a screenshot or link.
