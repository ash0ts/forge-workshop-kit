# Contributing

Workshop Kit contains the teaching material and the Python package used by the notebooks. A contribution might improve an explanation, repair an exercise, add a visualization, or change how work is saved. Start with the current notebook and deck for the workshop you are changing.

For the current release, known limitations, and planned work, read [next-up.md](next-up.md). For the runtime and its data flow, read [techspec.md](techspec.md).

## Set up a checkout

Use a Git checkout for contributing; the Python source distribution does not include the deck toolchain. Use Python 3.11–3.13 and run commands from this repository's root. Notebook generation requires the uv version declared in `tool.workshop-build.uv-version` in [pyproject.toml](pyproject.toml). Read it with:

```sh
python scripts/release_support.py --uv-version
```

Install only the workshop extras you need. This example sets up Routing, including the default development tools:

```sh
uv sync --frozen --extra routing
uv run --extra routing forge-workshop doctor request_routing
uv run --extra routing forge-workshop open request_routing
```

Use `pending`, `solar`, or `inspection` for the other dependency extras. Transit and Airline use the base dependencies. `uv sync --frozen --all-extras` installs the full maintainer environment used by CI. Node and Chrome are needed only when building or validating decks; see [maintenance](docs/maintenance.md#build-the-decks).

The local doctor does not contact a provider. Credentials are needed for live product checks and publication, not for editing source or running the free checks. Participant setup lives in [docs/setup.md](docs/setup.md).

## Edit the source

| Change | Edit here | Generated output |
| --- | --- | --- |
| Workshop explanations, learner code, and controls | `scripts/pending_cells.py`, `solar_cells.py`, `routing_cells.py`, `inspection_cells.py`, `transit_cells.py`, or `airline_monitoring_cells.py` | `notebooks/*.py` |
| Starter and facilitator notebooks | [scripts/build_notebooks.py](scripts/build_notebooks.py) | `notebooks/starter.py`, `notebooks/facilitator.py` |
| Titles, exercise references, metrics, compatibility, and ARIA stop definitions | [workshops.json](src/forge_workshop_kit/workshops.json) | Navigation, reference tables, publication labels |
| Slide order, explanations, and presenter notes | Each deck's `scripts/build-storyboard.py` | `slides.md` and slide maps in the same deck |
| Public learning Reports | [reports/](reports/README.md) Markdown and source ledgers | Native Forge Reports; stable links in `reports/published.json` |
| Shared saving, accounting, tracing, publication, or presentation | [src/forge_workshop_kit](src/forge_workshop_kit) | Package and notebook behavior |
| Recorded ARIA investigations | [assets/aria](src/forge_workshop_kit/assets/aria) | Offline transcripts and shared deck frames |

Generated notebooks are editable by attendees. Repository changes belong in their authored cells so regeneration preserves them. The same applies to generated slide Markdown. The [authoring guide](docs/authoring.md) explains manifest references, new workshops, and rehearsal adapters.

## Check a change

For a Routing exercise change:

```sh
uv run --extra routing forge-workshop check request_routing
uv run --extra routing python scripts/build_notebooks.py --only request_routing
uv run --extra routing marimo check notebooks/request_routing.py
uv run --extra routing forge-workshop open request_routing
```

`check` validates the authored cells and manifest references and runs that workshop's registered free checks. It does not establish that the rendered interaction or a live Forge service works. Open the changed step, try its prerequisite and next action, and inspect the output at a narrow width as well as your normal layout.

For package changes, run the relevant tests under `tests/`. The full cross-platform suite and generation check are defined in [Workshop checks](.github/workflows/check.yml). If behavior changes, update its contract in the same change. When a notebook or deck is regenerated, inspect the diff for unrelated changes.

## Describe the contribution

Explain what a participant or maintainer can do differently, why the change is needed, and what you checked. Link relevant saved evidence or screenshots, and name any checks that remain untested. A local test pass does not establish external-account access or participant usability.

Keep recorded results tied to their source, including failures and ties. Do not publish credentials, local journals, operator state, or a participant's private work. `.workshop/` is saved work, not a disposable build directory.

Builds and publication are separate. See [maintenance](docs/maintenance.md) when preparing a release. Contributor changes do not require a new release or a live rehearsal unless they affect what those checks establish.
