# Workshop decks

The six decks share one pinned Slidev installation. Each workshop keeps its own storyboard, diagrams, photographs, product captures, and presenter notes.

A single-deck source download contains only its selected workshop. Use that directory name in the example commands below; the other workshop links open their repository guides.

| Deck directory | Workshop | Author and presenter guide |
|---|---|---|
| `pending` | Pending, Inc. | [Office workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/pending/README.md) |
| `solar` | Solar forecasting | [Research workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/solar/README.md) |
| `routing` | Request routing | [Routing workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/routing/README.md) |
| `inspection` | Visual inspection | [Inspection workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/inspection/README.md) |
| `transit` | Transit software factory | [Transit workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/transit/README.md) |
| `airline_monitoring` | Airline monitoring | [Airline workshop](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/airline_monitoring/README.md) |

## Preview a deck

Use Node.js **22.23.2 or later**. From the repository root:

```sh
cd decks
npm ci
npm run dev -- routing
```

Replace `routing` with a directory name from the table. Open the address printed in the terminal; `/presenter/1` opens the speaker notes. The wrapper runs the existing generated slides. It does not regenerate their storyboard. Install dependencies here, not inside each workshop directory.

## Edit the source

Edit the workshop's `scripts/build-storyboard.py` and any helper named in its README. Regenerate from the repository root, for example:

```sh
python3 decks/routing/scripts/build-storyboard.py
```

`slides.md`, presenter notes, and `notes/slide-map.json` are generated. Put prose changes in the storyboard, diagrams in the Vue/SVG components, and source attribution beside the captures or data. Use the slide map's stable identities for exercise and worked-answer links.

## Build and validate

The shared build creates the browser deck, PDF, offline browser bundle, and editable source package:

```sh
python3 scripts/build_decks.py --only routing --install --pdf --validate
```

Run this command from the repository root. It needs Python, uv, and Chrome for PDF export. See [maintenance](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/maintenance.md#build-the-decks) for browser setup, output paths, validation, and publication. Downloaded source bundles also have a root README with commands for their included files.

Opening or building a deck runs no workshop exercises or model requests. Product links still use the viewer's own Forge access. Keep recorded examples distinct from a participant's results, and check [release qualification](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/release-checks.md) before describing a workshop as ready for attendees.

## Earlier design notes

These November 14, 2026 notes preserve design decisions, visual provenance, and the checks performed for earlier revisions. Their slide numbers and validation counts are historical; current mappings come from each generated slide map.

- [Pending visual design](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/pending/notes/visual-upgrade.md)
- [Solar visual design](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/solar/notes/visual-upgrade.md)
- [Solar teaching expansion](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/solar/notes/teaching-expansion.md)
- [Solar worked diagrams](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/solar/notes/visual-coverage.md)
