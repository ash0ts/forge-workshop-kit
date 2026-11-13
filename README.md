# Forge Workshop Kit

Copy a notebook into your own Forge project. Write code, run experiments, inspect traces, and save the evidence. The facilitator watches progress through normal W&B project access.

There is no workshop gateway, attendee token, or service to deploy. The same notebook runs on a laptop. Hosted notebooks use Forge's existing authentication and compute; inference and compute are billed to the participant's account.

## Choose a notebook

| Notebook | What you build |
| --- | --- |
| [Solar Autoresearch](notebooks/solar_autoresearch.py) | Forecast solar measurements, move to solar images, then let a research agent edit and test model/training code. |
| [Pending, Inc.](notebooks/pending_inc.py) | Give an office agent tools, evaluate its work, and improve its instructions across two rounds. |
| [Starter](notebooks/starter.py) | A small starting point for another workshop. |
| [Facilitator](notebooks/facilitator.py) | Read checkpoint progress, help requests, failed runs, and evidence links from public projects. |

Hosted template links and qualification results are recorded in [the release checks](docs/release-checks.md). Do not confuse a source template with a qualified hosted release.

## Hosted setup

1. Sign in to [Forge](https://forge.coreweave.com). Create a public teaching project in your own entity or a team where you can write.
2. Open the workshop template and choose **Copy to project**. Select your project and open its editable copy. If the copy picker does not offer your project, download the notebook's `.py` file and import it into your project.
3. Run the notebook's dependency setup. Click **Connect and restore my saved work**, then send the first trace. Check that the project shown is yours.
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

Opening a notebook does not train a model or send inference. Run controls do. Completed stages are reused. An interrupted stage stays interrupted until you inspect it and explicitly choose another attempt.

The default inference allowance is $8 per workspace, including retries and bounded unknown usage. Change `budget_usd` in the session initialization if you want another allowance. This is a participant-controlled stop, not an account billing limit. Notebook compute charges are separate.

Local receipts live under `.workshop/`. Checkpoints in your project preserve selected source, model weights, predictions, and progress across fresh hosted runtimes. Publishing or retrying a trace never reruns the experiment. Keep a local copy until the checkpoint reports a successful upload.

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

## Materials

- [Solar experiment and data contract](docs/solar-contract.md)
- [Four-hour facilitator runbook](docs/facilitator.md)
- [Source map](docs/source-map.md)
- [Release checks and known limitations](docs/release-checks.md)

The prior Pending workshop is preserved in [its original repository](https://github.com/ash0ts/pending-inc-workshop).
