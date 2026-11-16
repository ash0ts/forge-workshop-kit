# Forge Workshop Kit

Six hands-on Python workshops that follow a customer or engineering problem through code, a result, and a tested change. Handle a refund, forecast solar observations, route a support request, inspect a circuit board, coordinate coding agents, or investigate a booking agent.

Getting a first output is the beginning of the exercise. Participants then inspect a mistake or unexpected result, change the relevant code, and test it on the same cases. Each workshop includes an illustrated Report, an editable notebook, a deck, free code checks, and recorded outcomes you can inspect before running anything.

Participants run an editable notebook and save results to their own Forge project. The facilitator can read published progress and help requests. There is no workshop gateway or shared account.

**These are technical previews.** The notebooks and decks are published, but external-account checks and participant rehearsals are still outstanding. See [current status and next steps](next-up.md) before scheduling a class.

The [ten-minute captioned tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) follows all six problems through their diagrams and saved Forge records. A [clean video, subtitles, and narration](media/walkthrough/README.md) are available for presenting or recording your own explanation.

Start with the [workshop overview](docs/workshop-overview.md), then choose a [package for reading, demonstrating, running, or adapting a workshop](docs/use-the-workshops.md). The [public library](https://ash0ts.github.io/forge-workshop-kit/) links each example, notebook start page, deck, and download.

Download the [QR codes and tracked sharing links](https://ash0ts.github.io/forge-workshop-kit/share/) for invitations, slides, and handouts. The [sharing guide](docs/share-links.md) explains placement and tracking.

## Choose your workshop

The durations include coding, discussion, and breaks. Participants should be comfortable reading basic Python.

| Workshop | Problem and workflow | Time | Deck | Report |
| --- | --- | --- | --- | --- |
| [Pending, Inc.](https://ash0ts.github.io/forge-workshop-kit/packet/start/pending.html) | **Agent development:** give an office agent tools for refunds and account access; trace its actions and test changes to its harness. | 4 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/pending/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-an-agent-you-can-inspect%2C-then-test-changes-to-its-harness--VmlldzoxODMxMzUzMQ==) |
| [Solar Autoresearch](https://ash0ts.github.io/forge-workshop-kit/packet/start/solar.html) | **Agent-assisted research:** train on real satellite observations, compare experiments, and test a research agent’s code edits. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/solar/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Test-research-agent-changes-against-real-solar-observations--VmlldzoxODMxMzUzMg==) |
| [Customer request routing](https://ash0ts.github.io/forge-workshop-kit/packet/start/routing.html) | **Model improvement and release:** route banking requests, review mistakes, then reproduce, repair, and roll back a batch predictor. | 5½ h | [Slides](https://ash0ts.github.io/forge-workshop-kit/routing/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Train-a-support-router%2C-then-check-what-you-released--VmlldzoxODMxMzUzNw==) |
| [Circuit-board inspection](https://ash0ts.github.io/forge-workshop-kit/packet/start/inspection.html) | **Visual inspection and data selection:** compare features on real board photographs, choose what to label, and reproduce a detector. | 4 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/inspection/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-a-missed-defect%2C-then-test-the-change--VmlldzoxODMxMzUzOA==) |
| [Transit software factory](https://ash0ts.github.io/forge-workshop-kit/packet/start/transit.html) | **Multi-agent software delivery:** coordinate builders of a departure board, integrate their patches, and test a shared lesson. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/transit/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Coordinate-coding-agents%2C-then-test-the-app-they-built--VmlldzoxODMxMzUzOQ==) |
| [Airline monitoring](https://ash0ts.github.io/forge-workshop-kit/packet/start/airline_monitoring.html) | **Monitoring and evaluation improvement:** inspect simulated booking changes, review a monitoring rule, curate regression cases, and test a repair. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) | [Read](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Turn-an-airline-agent%27s-behavior-into-monitoring-rules-and-regression-tests--VmlldzoxODMxMzU0MA==) |

The [deck library](https://ash0ts.github.io/forge-workshop-kit/) includes PDFs and editable slide sources. For a short demonstration rather than a full class, use the [demo guide](docs/current-demo-guide.md).

Each workshop also has a [one-page poster](https://ash0ts.github.io/forge-workshop-kit/) and step-by-step diagrams shared by its notebook and deck. The [visual guide gallery](https://ash0ts.github.io/forge-workshop-kit/visual-language/) contains 36 step-by-step explanations from the six workshops. To use them in another project, install the standalone [teenage-engineering-visualizations skill](docs/technical-visuals.md). It includes its own fonts, renderer, examples, and export checks.

## Follow the work through Forge

In Pending, open the refund's tool call in Agent Lens and check which payment it changed. In Solar, compare a forecast with the observed value, then open the training run and recover its code and weights from an Artifact. In Inspection, use EvalTables to see which board a changed detector now catches and which one it still misses.

The notebook gives you the code to change and a check to run. The linked Forge record helps you explain what happened. The [workshop guide](docs/use-the-workshops.md#follow-the-ai-work-through-forge) suggests a specific investigation for each session.

## Start a workshop

Open a workshop's start page from the table above. Download its current `.py` notebook into a folder you will keep, then follow the page's login and launch commands. You need [uv](https://docs.astral.sh/uv/getting-started/installation/); the launch command installs the notebook's pinned dependencies and opens an editable local notebook.

Sign in to [Forge](https://forge.coreweave.com) and create a project where you can write. Initialize the notebook’s controls with **Run all stale cells**, enter that `entity/project`, and inspect the opening example. Follow the access check and first tracing exercise. Training and model calls have their own explicit run buttons.

Your notebook runs locally and publishes results to that Forge project. Share the project link with the facilitator if you want progress monitoring; they do not need your API key. Use the supplied workshop data in public projects. See [setup and recovery](docs/setup.md) for the exact commands and access checks.

**Hosted templates:** the optional Forge copies remain on v0.11.1 while notebook-management access blocks their update. Use the website downloads for the revised exercises and direct ARIA controls; they retain the v0.12.0 runtime pins.

## Work from the repository

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/). For Solar:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra solar
uv run --extra solar wandb login --host https://api.wandb.ai --verify
uv run --extra solar marimo edit notebooks/solar_autoresearch.py
```

Enter your writable `entity/project` in the notebook. Use the [dependency table](docs/setup.md#work-from-the-repository) for the other workshops. Tools and training run in the notebook’s Python runtime; inference and publication use your Forge account. You do not need Docker or a local service.

## While you work

Each step puts the task, editable code, local check, run control, result, and Forge links together. Browsing or editing does not execute an experiment. A disabled run control names the prerequisite you need to complete.

Drafts and completed results save locally. Uploaded W&B checkpoint artifacts let you restore them after replacing a runtime. Keep `.workshop/` on a laptop and confirm the checkpoint upload before discarding a hosted runtime. [Resume and recovery instructions](docs/setup.md#resume-or-recover) explain how to retry an upload without repeating an experiment.

The default **$8 inference allowance** is adjustable per workspace. It is not an account-wide billing limit. Local training uses your laptop CPU. ARIA, native Agent Lens tag judging, and any hosted notebook compute have separate billing. In Airline, disable **Apply with AI** when you finish; closing the notebook does not disable the tag.

Each workshop pauses twice to [investigate a result with ARIA](docs/aria-investigations.md). Write what you think happened, click **Start ARIA investigation**, and open the returned conversation. Ask ARIA to check your explanation against the selected records, then open one citation yourself. For example, did the extra tool call improve the account outcome, or did both versions already finish correctly? Live access needs a supported team project and Smart features; use the bundled recorded investigation if those aren't available.

## What happened in the recorded rehearsal

The recordings include improvements, ties, and regressions. The classifiers improved in their qualified comparisons; Pending’s harnesses tied; one Solar image seed regressed; the Transit team did worse on two checks; both Airline versions passed. See [recorded results and limitations](docs/recorded-results.md) for the numbers, protocols, and source records.

Weave-backed native EvalTables comparisons are available. Airline’s last AI Alignment tests returned HTTP 500, and its prepared Insights workflow remains unqualified. [Release checks](docs/release-checks.md) distinguish working paths from outstanding access and rehearsal checks.

## Facilitate or contribute

Start with [Run a Forge workshop](docs/facilitator-start.md) to prepare the materials, set up the progress monitor, and handle access or publication failures. Each deck has a short running guide: [Pending](docs/run-pending.md), [Solar](docs/run-solar.md), [Routing](docs/run-routing.md), [Inspection](docs/run-inspection.md), [Transit](docs/run-transit.md), and [Airline](docs/run-airline_monitoring.md).

The [facilitator notebook](notebooks/facilitator.py) reads the project links you supply; follow the [monitor setup instructions](docs/setup.md#read-participant-progress) to run it locally. Missing updates mean “unknown,” not “failed.” The [documentation index](docs/README.md) links each workshop’s schedule and evidence.

For changes to the kit, start with [CONTRIBUTING.md](CONTRIBUTING.md). The [technical specification](techspec.md) explains how notebooks, saving, accounting, tracing, and publication fit together. [Next steps](next-up.md) separates completed work from what still needs qualification.

To add a workshop, use the [starter notebook](notebooks/starter.py), [authoring guide](docs/authoring.md), and repository-local [forge-workshops skill](.agents/skills/forge-workshops/SKILL.md). Participants do not need the skill. Earlier releases and gateway-era materials are preserved in the [archive](docs/archive.md).
