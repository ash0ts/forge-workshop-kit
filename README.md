# Forge Workshop Kit

Copy a notebook into your own Forge project. Write code, run experiments, inspect traces, and save the evidence. The facilitator watches progress through normal W&B project access.

There is no workshop gateway, attendee token, or service to deploy. The same notebook runs on a laptop. Hosted notebooks use Forge's existing authentication and compute; inference and compute are billed to the participant's account.

## Choose a notebook

| Notebook | What you build |
| --- | --- |
| [Solar Autoresearch · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | Forecast solar measurements, move to images, then let a research agent edit and test model/training code. |
| [Pending, Inc. · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | Give an office agent tools, evaluate its work, and improve its instructions across two rounds. |
| [Starter · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzI=/view) | A small starting point for another workshop. |
| [Facilitator · open monitor](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view) | Read checkpoint progress, help requests, failed runs, and evidence links from public projects. |

Sign in to Forge to copy a template. [Source notebooks](notebooks) and the [downloadable kit](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.2.0) are public. This is a technical preview; [remaining release checks](docs/release-checks.md) include an external-attendee and human rehearsal.

The **Solar companion deck** follows the notebook exercises: [browser deck](https://ash0ts.github.io/forge-workshop-kit/solar/), [PDF](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.2.0/solar-autoresearch.pdf), and [editable Slidev source](decks/solar). [Presenter notes and the current Pending deck guide](docs/deck-guide.md) explain where to pause for code and investigation.

## Hosted setup

1. Sign in to [Forge](https://forge.coreweave.com). Create a public teaching project in your own entity or a team where you can write.
2. Open the workshop template and choose **Copy to project**. Select your project and open its editable copy. If the copy picker does not offer your project, download the notebook's `.py` file and import it into your project.
3. Initialize the notebook cells once with marimo’s **Run all stale cells** control. Exercise run buttons remain unpressed, so initialization does not train or call inference. In Solar, click **Connect and restore my work**. In Pending, click **Check my project and restore saved work**. Check that the project shown is yours, then send the first trace.
4. Give the facilitator your `entity/project` link. They need no credential or token from you.

A writable project alone does not supply inference credits or notebook compute access. Check those before the session. Public teaching projects expose their published code and results; use only the supplied public or fictional data.

## Laptop setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git, then:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen
uv run wandb login
uv run marimo edit notebooks/solar_autoresearch.py
```

Enter your `entity/project` in the notebook. Use `notebooks/pending_inc.py` for Pending. No Docker, Node, Electron, or local API service is needed.

## Saving and spending

Each notebook presents one current step: a task, editable code, a free local check, an explicit run, its result, and an **Inspect in Forge** question. Use the numbered navigator to browse. A disabled run names its prerequisite; browsing and editing do not execute the task. Marimo's app view hides support cells while retaining the exercise editors. Switch to code view to inspect the authored notebook itself.

Opening a notebook does not train a model or send inference. Run controls do. Completed stages are reused. An interrupted stage stays interrupted until you inspect it and explicitly choose another attempt.

The default inference allowance is $8 per workspace, including retries and bounded unknown usage. Set another allowance in the connection step. This is a participant-controlled stop, not an account billing limit. Notebook compute charges are separate.

Local receipts live under `.workshop/`. Drafts save as you edit; completed runs retain the exact executed source. Checkpoints in your project preserve drafts, selected source, model weights, predictions, and progress across fresh hosted runtimes. Publishing or retrying a trace never reruns the experiment. Keep a local copy until the checkpoint reports a successful upload.

## What belongs in the framework

```python
from forge_workshop_kit import WorkshopSession

session = WorkshopSession.from_environment("my-workshop", project="me/my-project")
session.check_access()
session.restore()

with session.stage("baseline", config=config, sources={"model.py": source}) as stage:
    if stage.needs_run:
        result = train_model(data, config)
        stage.record(result)

session.checkpoint("baseline", evidence={"Run": run_url})
```

Identity, receipts, publication and progress belong in the package. The experiment, scorer, instrumentation and improvement controller remain visible in the notebook. [Framework contract](docs/framework.md).

## Recorded teaching example

The revised notebooks were run in a browser against real data and services. On the two held-out image days, error was 0.125762 for persistence, 0.122442 for the manual residual model, and 0.110011 for the agent-selected model. The researcher proposed a zero-initialized residual head, then added a masked absolute-error training loss. Each adopted version had its own test. These are one-seed teaching results, not a solar forecasting benchmark.

The short GOES training budget produced a poor forecast, and persistence won. Pending reached the correct account state in all 12 final executions; the editor retained the manual harness. Both outcomes remain visible. Recorded results are labeled and cannot be attributed to a learner's unexecuted edit.

- [Solar Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==)
- [Pending Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-51a0006f--VmlldzoxODMwMjcxMA==)
- [Measured costs, browser checks and remaining limits](docs/release-checks.md)

## Materials

- [Solar experiment and data contract](docs/solar-contract.md)
- [Four-hour facilitator runbook](docs/facilitator.md)
- [Source map](docs/source-map.md)
- [Decks, worked answers and exercise references](docs/deck-guide.md)
- [Release checks and known limitations](docs/release-checks.md)

The prior Pending workshop is preserved in [its original repository](https://github.com/ash0ts/pending-inc-workshop).
