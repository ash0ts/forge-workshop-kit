# Learning Reports

These six articles follow a practical problem through the code, a recorded execution, and the decision that followed. You can inspect a refund, forecast, routing mistake, defective board, departure query, or changed booking before opening a notebook. Each article explains which Forge record supports its conclusion and links to the editable exercise.

Start with a Report for the technical explanation. Its packet contains the deck, visual guides, copyable notebook, and instructions for a short demonstration or a facilitated session. To try the code, open the workshop start page and choose the Forge copy, import, or laptop path. In Forge, choose **Copy to project**. Your copy uses your credentials and saves work in your project; the facilitator only reads published progress.

| Workshop | Learning Report | Materials and running instructions |
| --- | --- | --- |
| Pending, Inc. | [Build an agent you can inspect, then test changes to its harness](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-an-agent-you-can-inspect%2C-then-test-changes-to-its-harness--VmlldzoxODMxMzUzMQ==) | [Pending packet](https://utm.io/uuH96) |
| Solar Autoresearch | [Test research-agent changes against real solar observations](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Test-research-agent-changes-against-real-solar-observations--VmlldzoxODMxMzUzMg==) | [Solar packet](https://utm.io/uuH97) |
| Customer request routing | [Train a support router, then check what you released](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Train-a-support-router%2C-then-check-what-you-released--VmlldzoxODMxMzUzNw==) | [Routing packet](https://utm.io/uuH98) |
| Circuit-board inspection | [Find a missed defect, then test the change](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-a-missed-defect%2C-then-test-the-change--VmlldzoxODMxMzUzOA==) | [Inspection packet](https://utm.io/uuH99) |
| Transit software factory | [Coordinate coding agents, then test the app they built](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Coordinate-coding-agents%2C-then-test-the-app-they-built--VmlldzoxODMxMzUzOQ==) | [Transit packet](https://utm.io/uuIaa) |
| Airline monitoring | [Turn an airline agent's behavior into monitoring rules and regression tests](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Turn-an-airline-agent%27s-behavior-into-monitoring-rules-and-regression-tests--VmlldzoxODMxMzU0MA==) | [Airline packet](https://utm.io/uuIab) |

The direct ARIA controls are in the [v0.12.0 downloads](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.12.0). Hosted templates remain on v0.11.1 while Forge notebook-management access blocks their update. Each Report links the current notebook download and its import or laptop instructions.

Use the [setup guide](../docs/setup.md) for account requirements, local installation, and recovery. The [recorded-results guide](../docs/recorded-results.md) explains the measured gains, ties, regressions, and teaching retests. These remain technical previews: native access and participant rehearsals must be checked for the intended class. See [current status](../next-up.md) before describing a complete live workshop as ready.

The packet links are managed in [the sharing-link registry](../docs/share-links.json). They identify the workshop; they do not identify an attendee or prove notebook completion. Follow [the tracking guide](../docs/share-links.md) when creating a separate link for a channel or event.

## Maintain these Reports

Edit the six Markdown sources here. The `sources-*.json` ledgers link claims and visuals to existing public evidence; they are contributor records, not Report body content. Update the ledger when changing a claim. `published.json` records the stable public destinations and exact source hashes.

Figures follow one example through its inputs, code, and result. `figures-*.json` records their source data, interpretation, and limits. Generated PNGs and editable SVGs live in `assets/`; native Forge screenshots keep their original pixels and a link to the captured record. Use the caption to tell readers which field to inspect.

The mechanism drawings use the same 1200 × 675 artwork as the notebook and deck. Their labels, example values, and geometry stay aligned across those surfaces; `figures-guide-layout.json` identifies the exact guide state. Keep scientific plots and native captures at their original aspect ratio. Never stretch a screenshot to match a diagram. The publisher places figures in the Report text column and adds a full-size link to each caption so a reader can inspect small native fields.

Regenerate the explanatory figures with the matching script:

```sh
uv run --extra routing python scripts/build_report_pending_solar_visuals.py
uv run --extra routing python scripts/build_report_routing_inspection_visuals.py
uv run --extra routing python scripts/build_report_transit_airline_visuals.py
uv run python scripts/build_report_guide_figures.py
```

These commands read saved evidence and render figures; they do not train models or call services. Publish new image files to the public repository before updating a Report that references them. Inspect the rendered figures and native Report page, including full-size image links and the notebook invitation.

When revising code excerpts, explain the operation at the line where it happens: which axis is averaged, which records remain in the denominator, or which label belongs to a probability column. A teaching excerpt may omit setup, but must say so. Keep measured source files and participant drafts unchanged when only the explanation changes.

[Build and publication instructions](../docs/maintenance.md#publish-learning-reports) explain the preview, destination checks, anonymous readback, and recovery after an interrupted save. Publication creates no experiment runs. Existing rehearsal Reports and participant conclusions remain separate.
