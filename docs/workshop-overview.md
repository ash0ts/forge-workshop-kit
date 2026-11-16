# Learn to investigate and improve an AI system

An agent can return a convincing answer after changing the wrong booking. A classifier can score well and still route requests incorrectly after release. Two coding agents can finish their assignments while the combined application fails its checks.

In these six Python workshops, you inspect a result like this and work through the code responsible for it. Then you make a small change and test what happens. Each workshop includes a worked example, editable notebook, illustrated deck, saved results, and a facilitator guide.

Watch the [ten-minute captioned tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) to see the exercises and their saved Forge records before choosing one.

## Choose a problem

| Workshop | What you build and examine | Duration |
| --- | --- | --- |
| Pending, Inc. | Give an office agent invoice and account tools. Inspect its actions, repair an ambiguous retry, and compare changes to its harness. | 4 hours |
| Solar Autoresearch | Train forecasts on real satellite observations. Compare models, then review and test a research agent's code changes. | 6 hours |
| Customer request routing | Train a banking-request classifier, review errors, and reproduce, repair, and roll back the selected batch predictor. | 5½ hours |
| Circuit-board inspection | Compare whole-image and patch features on real photographs. Inspect missed defects and test equal-budget labeling policies. | 4 hours |
| Transit software factory | Coordinate coding agents building a departure board. Integrate their patches and test whether a verified lesson helps the next build. | 6 hours |
| Airline monitoring | Inspect simulated booking changes, review a monitoring rule, reconstruct regression cases, and test a repair. | 6 hours |

The durations include hands-on exercises and breaks. All workshops assume basic Python. The supplied data is public or fictional; use it when working in a public project.

## Follow the work through Forge

The exercises give you a reason to use each screen. When an airline tool call succeeds, open **Agent Lens** and check whether the returned booking still contains the passenger's return flight. When a forecast is poor, open its **training run** to inspect the settings and loss history. When you change a circuit-board detector, use **EvalTables** to compare the same photographs across versions, including the new mistakes. Recover the selected model and preprocessing from **Artifacts** and reproduce its predictions in your notebook.

Twice during each workshop, ask **ARIA** to check your explanation of a saved result. Read one of its cited records before deciding what you agree with and what you would test next. The final **Report** records your conclusion and links the results that support it.

## Start with the example

Choose a workshop in the [public library](https://ash0ts.github.io/forge-workshop-kit/). Read its example or deck without an account. To try the code, download the current notebook and follow its start page's login and launch commands. It runs locally and saves results to your own Forge project.

Current website notebooks include the revised explanations and use the v0.12.0 runtime. Optional hosted templates remain on v0.11.1 while notebook-management access blocks their update; use the website download for the current exercises and direct ARIA controls.

The default notebook inference allowance is $8 and can be adjusted. Compute, ARIA, and native tag judging are billed separately. Opening a notebook does not begin training or send a model request. [Setup and recovery](setup.md) explains access checks and saved progress.

## What the recorded runs showed

The recorded classifier comparisons improved, Pending's final harnesses tied, and Transit’s two-agent build failed checks that the solo build passed. The workshops use those outcomes to work out what to inspect or test next. See the [recorded results](recorded-results.md) for the measurements and source records.

These are technical previews. External-account checks and participant rehearsals are still outstanding, and Airline's native monitoring activities have additional access limitations. Check [current status](../next-up.md) before scheduling a full class.

To lead a session, use the [facilitator start guide](facilitator-start.md) and its workshop-specific run guide. To adapt the materials, start with the [contributor guide](../CONTRIBUTING.md).
