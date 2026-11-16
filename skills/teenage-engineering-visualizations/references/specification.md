# Figure specification and exports

Author one UTF-8 JSON file per explanation. Start from a file in `templates/` and inspect the corresponding example in `examples/`. The renderer is intentionally small: it lays out these six compositions, rather than positioning arbitrary user-supplied HTML.

## Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | `1` |
| `id` | Stable figure identity, using letters, digits, hyphens, or underscores |
| `kind` | `overview`, `sequence`, `transformation`, `comparison`, `branches`, or `poster` |
| `title`, `eyebrow`, `question`, `summary` | Heading, section label, reader's question, and accessible explanation |
| `provenance` | `actual`, `recorded`, `illustrative`, `planned`, or `unavailable` |
| `steps` | Components in their displayed order. Each has an `id`, `title`, and `body`; optional `input`, `code`, `output`, `status`, `symbol`, and local `media` explain the transformation. |
| `states` | Ordered views with `id`, `label`, `visible` component IDs, `focus` component IDs, and a `caption` |
| `annotations` | Numbered explanations targeting a component ID: `{ "number": 1, "label": "Inspect this result", "target": "observation" }` |
| `source_links` | `{ "label": "Source record", "url": "https://…" }` entries. Identify which source supports the explanation. |
| `hero` | Optional local SVG or image for an `overview`. The assembled system remains visible on the left; the selected component's explanation appears on the right. Resolve the path relative to the specification. |

Use a short code excerpt. Keep the complete implementation in its own source file and link to it. State whether arithmetic is illustrative. A proposed operation has no invented duration, output, or trace.

Every `transformation` step requires a nonempty `input` and `output`. Its output must feed the next step. Use `comparison` or `branches` for alternative methods, and `sequence` for a teaching procedure whose operations do not form one data pipeline.

`media` paths resolve relative to the specification. The renderer embeds local media; it does not fetch remote images. Preserve original captures and their attribution. The built-in symbols are `file`, `record`, `component`, `input`, `output`, `observation`, and `state`.

An overview `hero` is separate from `poster.hero`, which supplies the poster's dominant drawing. Include an accessible title and description in each SVG. Keep its labels readable at the size allocated by the surrounding layout. The browser validator measures outer SVG text; an embedded SVG is an image to that validator. Open the hero SVG itself to check its inner text bounds, then inspect the assembled export for scaled-down labels, clipping, and overlaps. Preserve the editable hero alongside the figure specification.

For a poster, add a `poster` object containing `situation`, exactly three `outcomes`, `duration`, `prerequisites`, `dataset`, up to three concise `roles` entries (`name` and `action`), and a `cta` (`label` and `url`). Set `roles_title` to describe those responsibilities. `forge` remains a supported alias for the initial workshop application. An optional local `hero` SVG supplies the main drawing. Do not require Forge in a standalone example.

A `native_capture` adds a separate evidence view with `media`, `title`, `source_url`, and `investigation`. Optional fields preserve `original`, `capture_date`, and annotation records. Its `provenance` defaults to `recorded`, independently of the conceptual diagram's provenance. Keep the screenshot's values unobscured and distinguish capture time from the date you reviewed it. Inspect embedded capture labels directly as well as the surrounding figure.

## Run the renderer

Python 3.11 or later renders SVG and standalone HTML. PNG, PDF, and poster QR codes use the pinned Node.js dependencies. Install them in the skill directory:

```sh
npm ci
npx playwright install chromium
```

The lockfile pins Playwright and QR generation. Installing export dependencies can use the network. Rendering only reads local files and blocks browser network requests.

```sh
python scripts/render.py examples/transformation.json --output /tmp/transformation --layout slide --formats svg,html,png,pdf
python scripts/validate.py /tmp/transformation --browser
```

| Layout | Size |
| --- | --- |
| `slide` | 1200 × 675 |
| `notebook` | 960 × 780 |
| `digital` | 1200 × 1500 poster |
| `print` | A2 portrait, 420 × 594 mm PDF |

The output directory contains `index.html`, `index.json`, one numbered SVG per meaningful state, a `final.svg` alias, and text-bound records. Requested PNGs correspond to those states. `print.pdf` contains the meaningful states, with a single A2 page for a poster. Keep the source JSON and its local media beside the exported delivery package.

`validate.py --browser` checks actual rendered glyph bounds. It does not prove that labels are useful, an arrow describes the correct dependency, or a QR destination is public. Inspect those separately. A narrow HTML viewport retains the complete drawing and provides a text explanation and native keyboard controls.

## Compatibility

The token file defines shared colors, font families, baseline strokes, and output dimensions. The renderer defines the geometry, spacing, and type sizes for each composition. The standalone HTML stylesheet uses CSS variables generated from the same color tokens. Change these sources intentionally, then rebuild the example gallery and check every export. Keep existing component and state identities when revising an explanation so links and reveal selections remain meaningful. Never put project credentials, experiment execution, or publication logic into display controls.
