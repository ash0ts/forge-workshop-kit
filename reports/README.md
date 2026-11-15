# Learning Reports

Read a worked example, then copy its notebook into your own Forge project. These Reports teach the problem, the code, and the recorded outcome. They preserve ties, failures, and missing judgments. The materials remain technical previews; reading a public Report does not establish that every service is enabled for your account.

| Workshop | Learning Report | Run it |
| --- | --- | --- |
| Pending, Inc. | [Build an agent you can inspect, then test changes to its harness](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-an-agent-you-can-inspect%2C-then-test-changes-to-its-harness--VmlldzoxODMxMzUzMQ==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) |
| Solar Autoresearch | [Test research-agent changes against real solar observations](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Test-research-agent-changes-against-real-solar-observations--VmlldzoxODMxMzUzMg==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) |
| Customer request routing | [Train a support router, then check what you released](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Train-a-support-router%2C-then-check-what-you-released--VmlldzoxODMxMzUzNw==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) |
| Circuit-board inspection | [Find a missed defect, then test the change](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-a-missed-defect%2C-then-test-the-change--VmlldzoxODMxMzUzOA==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) |
| Transit software factory | [Coordinate coding agents, then test the app they built](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Coordinate-coding-agents%2C-then-test-the-app-they-built--VmlldzoxODMxMzUzOQ==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) |
| Airline monitoring | [Turn an airline agent's behavior into monitoring rules and regression tests](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Turn-an-airline-agent%27s-behavior-into-monitoring-rules-and-regression-tests--VmlldzoxODMxMzU0MA==) | [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) |

Use the [setup guide](../docs/setup.md) for account requirements, local installation, and recovery. The [deck library](https://ash0ts.github.io/forge-workshop-kit/) pairs each Report with its slides.

## Maintain these Reports

Edit the six Markdown sources here. The `sources-*.json` ledgers link claims and visuals to existing public evidence; they are contributor records, not Report body content. Update the ledger when changing a claim. `published.json` records the stable public destinations and exact source hashes.

Figures follow one example through its inputs, code, and result. `figures-*.json` records their source data, interpretation, and limits. Generated PNGs and editable SVGs live in `assets/`; native Forge screenshots keep their original pixels and a link to the captured record. Use the caption to tell readers which field to inspect.

Regenerate the explanatory figures with the matching script:

```sh
uv run --extra routing python scripts/build_report_pending_solar_visuals.py
uv run --extra routing python scripts/build_report_routing_inspection_visuals.py
uv run --extra routing python scripts/build_report_transit_airline_visuals.py
```

These commands read saved evidence and render figures; they do not train models or call services. Publish new image files to the public repository before updating a Report that references them. Inspect the rendered figures and native Report page, including full-size image links and the notebook invitation.

[Build and publication instructions](../docs/maintenance.md#publish-learning-reports) explain the preview, destination checks, anonymous readback, and recovery after an interrupted save. Publication creates no experiment runs. Existing rehearsal Reports and participant conclusions remain separate.
