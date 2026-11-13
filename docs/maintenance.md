# Build and publish the workshop

`pyproject.toml` owns the package version. `src/forge_workshop_kit/workshops.json` owns template names, exercise labels, dependency extras and workflow compatibility. Leave the workflow version unchanged for copy or packaging changes so saved experiments remain usable.

## Build locally

```sh
uv sync --frozen --all-extras
uv run --all-extras python scripts/build_release.py
```

This generates the notebooks, checks them, exports previews without participant credentials, and packages the wheel and source archive in `dist/v<VERSION>/`. It also records file hashes in `release-manifest.json`. Nothing is published and no exercise runs. Use `--only starter` or another manifest slug when building one template.

The notebook generator exports dependency pins from `uv.lock`. Do not hand-edit generated notebook headers. Acquisition tools use the separate `data-prep` group; participants receive prepared datasets.

## Publish explicitly

First upload the matching wheel to the repository's versioned GitHub release. Then run:

```sh
uv run --all-extras python scripts/publish_templates.py \
  --project YOUR_ENTITY/YOUR_PROJECT \
  --build dist/v0.3.0
```

The publisher checks the public wheel and every selected source/preview hash before uploading. It keeps destination-specific receipts under `.workshop-deployments/`, verifies each notebook's destination project before updating it, and reads back the uploaded files. `--only` selects a template. Repeating the command resumes incomplete publication and skips matching uploads.

If notebook creation was interrupted before its ID was saved, the publisher stops rather than creating another copy. Find the notebook in the destination project and pass `--notebook-id SLUG=ID`. Use `--adopt-ids` to import the old unscoped receipt only after every listed destination has been verified.

Existing attendee copies are separate notebooks. Updating the templates does not replace them. Keep previous release assets and the recorded teaching evidence; do not rewrite Git history or delete participant state.

## Saved work

The shared library has no runtime dependency on `common_tools`, an operator checkout or any gateway. Authentication comes from the participant's Forge runtime or local W&B login. `.workshop/` contains their drafts and execution receipts. Do not treat it as disposable build output.

In the old operator repository, `dist/participant` is an independent Git checkout. Both builders that wrote into it are now retired. Its history was bundled before changing current setup links. It remains in place with the self-service release intact.

Use the [release checks](release-checks.md) to distinguish code/browser validation from external-account access and human rehearsal.
