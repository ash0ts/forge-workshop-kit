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

The command generates the shared visual guides, checks notebooks, exports previews with credentials removed, and writes the wheel, source archive, ARIA recording bundle, visual source bundles, and `release-manifest.json` to `dist/v<VERSION>/`. It runs no workshop exercises and publishes nothing. The manifest records file hashes and workflow identities. The poster QR encoder uses the skill's pinned Node dependencies; install them with `npm ci --prefix skills/teenage-engineering-visualizations` before a full build.

For one template, use `--only request_routing`. For a scratch build that should not replace your local release directory, use `--output PATH`. Inspect the package allowlist in `pyproject.toml` whenever adding files that source archives need. Keep local journals, credentials, deployment receipts, downloaded training outputs, and operator backups out of distribution files.

`forge-workshop build request_routing --install --pdf --validate` is the combined one-workshop command: it builds the template package and its mapped deck. Use the script commands when you need separate destinations or only one type of output.

## Build the decks

All decks share the locked toolchain in [decks/package.json](../decks/package.json) and its lockfile. Use Node.js 22.23.2 or later, uv, and Chrome for PDF export:

```sh
python scripts/build_decks.py --install --pdf --validate
```

Use `--only routing` while editing one deck. Set `CHROME_PATH` to an installed Chrome executable, or run `npx playwright install chromium` from `decks/`. The PDF checker installs its pinned maintenance dependencies through uv; those dependencies are not added to participant notebooks.

Output goes to `dist/decks/site/` for the hosted site and `dist/decks/downloads/` for PDFs, offline browser decks, and editable source archives. The build regenerates the [managed sharing links and QR codes](share-links.md) before rendering decks and posters. It also adds the poster gallery, standalone skill download, and shared notebook/deck figures. `--output PATH` selects another root. Without `--pdf --validate`, the command builds browser copies and source archives only. [Technical visuals](technical-visuals.md) covers individual figure builds.

Validation checks slide and reveal states, Back navigation, worked-answer return links, image loading, and rendered PDF pages. Inspect the changed screens yourself as well: container bounds alone do not establish readable text or useful annotations. The [deck guide](deck-guide.md) covers presentation and the [teaching sequence](teaching-sequence.md#use-consistent-visual-conventions) defines the shared diagram conventions.

The [Workshop decks workflow](../.github/workflows/deck.yml) publishes validated site output after matching changes reach `main`, or by explicit workflow dispatch. It does not upload assets to a GitHub release or publish Forge templates.

### Retry a Pages deployment

If deck validation and artifact upload succeeded but Pages deployment failed, run [Republish validated workshop decks](../.github/workflows/republish-decks.yml) on `main`. Set `source_run_id` to the numeric ID from the original Actions run URL:

```sh
gh workflow run republish-decks.yml --ref main -f source_run_id=RUN_ID
```

The recovery workflow checks that the source is a completed `deck.yml` run on this repository's `main` branch, with successful validation and upload steps. It uses [download-artifact](https://github.com/actions/download-artifact) to recover the existing `artifact.tar`, uploads that archive unchanged, waits for its metadata to become visible, and calls [deploy-pages](https://github.com/actions/deploy-pages). It does not rebuild decks or execute workshop code. Both publication workflows share the same concurrency group, so wait for any active publication to finish before starting recovery.

Pages artifacts expire after one day. If the artifact is missing or expired, rerun the ordinary deck workflow. Check the deployed site and its downloads after either path succeeds.

### Build participant materials

The complete deck build also creates `dist/decks/site/packet/`: a workshop overview and PDF, six deck PDFs, six downloadable notebook files and start pages, setup instructions, a facilitator start guide, short running guides, and detailed facilitator notes. The participant archive is `workshop-materials.zip`; the older `workshop-meeting-packet.zip` URL remains an alias. Its authored overview is [workshop-overview.md](workshop-overview.md). Workshop links come from the existing manifest and Report catalog.

The [sharing draft](sharing.md) and [recording script](loom-walkthrough.md) remain contributor documents in Git. They are not part of the public site's navigation or participant archive. The builder removes their older generated HTML and Markdown copies from the site output. Do not add personal communication drafts to the attendee document allowlist.

To rebuild only this packet from previously built decks:

```sh
python scripts/build_share_packet.py --site dist/decks/site --pdf
```

This requires the shared deck toolchain and Chrome. It makes no workshop or provider calls. Check the guide's PDF pages, the HTML on a narrow screen, and the links before sharing. The package contains only its explicit source documents, notebook files, public illustrations, and built PDFs. It excludes participant journals and credentials. The manifest records hashes and whether its source checkout had uncommitted changes.

For a coordinated documentation update, revise the README, affected learning Reports, and packet instructions together. Publish the Reports and verify their readback before committing the updated catalog. Build the site from that commit, then check the public packet and managed redirects. Register a separate placement link when attribution needs to distinguish a video from Slack; see [sharing and tracking](share-links.md). Do not use link clicks as a count of workshop completions.

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

## Publish learning Reports

The six [learning Reports](../reports/README.md) explain a worked example and link to the corresponding self-service notebook. Their Markdown sources are independent of saved participant conclusions and historical rehearsal Reports. Edit the source and claim ledger together; no training or inference is needed.

Build native Report payloads locally:

```sh
uv run python scripts/publish_learning_reports.py --project wandb/forge-workshop-kit
```

Inspect the Markdown, images, and payloads in `dist/learning-reports/`. Publish to the existing public project and refresh the public link catalog:

```sh
uv run python scripts/publish_learning_reports.py --project wandb/forge-workshop-kit --apply --catalog reports/published.json
```

Use `--only pending` for one Report; other names are `solar`, `routing`, `inspection`, `transit`, and `airline`. The publisher checks the destination, reuses IDs from `.workshop-deployments/<entity>/<project>/learning-reports.json`, and verifies the complete content without authentication. It preserves a backup before updating a Report and stops if someone edited the published content independently. Reconcile that change with the Markdown first.

If creation is interrupted before the ID is saved, locate the Report in that project and resume with `--adopt SLUG=REPORT_ID`. Do not discard the pending receipt and create another copy. After publication, inspect the native page, images, tables, code, and notebook CTA in a browser. Anonymous API readback and browser rendering are separate checks. Notebook execution still requires the reader's account and access.

A fresh contributor checkout has the public catalog but no private publication receipts. The publisher stops instead of creating duplicate Reports. For an existing destination, verify the Report linked in `reports/published.json`, then adopt its ID (the part after `--` in its URL). Use `--only` to update one Report. Publishing to a different project creates separate Reports there.

Commit the sources and `reports/published.json` together. The deck-library build reads this catalog to link the Report, deck, and current notebook start page. The optional hosted template has a separate URL in the catalog. The build does not publish Reports or run workshop code. Keep destination receipts and revision backups out of Git.

## Record what shipped

Keep the source commit, package hashes, template destination/readback receipt, deck validation, and unresolved access checks together for each release. Verify the public links after publication. Do not promote a workshop's readiness because its build succeeded: browser, external-account, native-feature, and human-rehearsal evidence remain separate.

For an interrupted upload, retry publication from the existing build and saved execution records. For an execution recovery, follow [setup and recovery](setup.md) and the [technical specification](../techspec.md). A successful execution with an unavailable export must not be rerun merely to obtain a screenshot or link.
