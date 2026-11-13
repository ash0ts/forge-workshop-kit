# Forge Workshop Kit

Build an agent or a forecasting experiment in a notebook, then ask an agent to improve the code around it. You’ll write the functions, run them, and use Forge to find out what happened.

Each participant works in their own project. The facilitator can read the progress you publish, but cannot run your notebook. You use your own Forge authentication, inference access, and notebook compute.

## Choose your workshop

| Workshop | What you’ll do |
| --- | --- |
| [Solar Autoresearch · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | Join a research lab working with real satellite observations. Build forecasts, compare training settings, then ask an agent to propose and test code changes. Four hours. |
| [Pending, Inc. · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | Give an office agent tools for refunds and account access. Check its work, edit its instructions, then build an agent that makes and tests further edits. Three hours. |

Use the [Solar browser deck](https://ash0ts.github.io/forge-workshop-kit/solar/) alongside the notebook, or download the [PDF](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.3.0/solar-autoresearch.pdf). The [release package](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.3.0) contains the notebook files and editable deck.

For a short demonstration, follow the [current demo guide](docs/current-demo-guide.md). It takes you from a notebook exercise to a trace, code change, and result in the two recorded rehearsals.

These are technical previews. The [release checks](docs/release-checks.md) describe what we’ve tested and the external-attendee and human rehearsals still needed.

For setup and recovery, follow [Copy the notebook and start](docs/setup.md).

## Start in Forge

1. Sign in to [Forge](https://forge.coreweave.com). Create a public teaching project under your account or a team where you have write access. Its name has two parts, such as `your-name/solar-workshop`.
2. Open a template above and choose **Copy to project**. Select your project and open the editable copy. If the project isn’t offered in the copy dialog, download the notebook’s `.py` file from [notebooks](notebooks) and import it into your project.
3. Use marimo’s **Run all stale cells** control once to initialize the notebook. This creates the controls; it does not press the exercise run buttons or start training or inference.
4. In Solar, click **Connect and restore my work**. In Pending, click **Check my project and restore saved work**. Confirm that the project shown is yours. Follow the first exercise to publish a trace and open it in Agent Lens.
5. Give the facilitator your project link if you want them to see progress and help requests. They don’t need your API key.

Your account needs notebook compute and inference access as well as permission to write to the project. The setup check verifies project access; the first model request checks whether inference is available. Use the supplied public or fictional data: other people can read files and results you publish to a public teaching project.

## Start on your laptop

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git, then run:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra solar
uv run --extra solar wandb login
uv run --extra solar marimo edit notebooks/solar_autoresearch.py
```

For Pending, use `--extra pending` in those commands and open `notebooks/pending_inc.py`. Starter and facilitator need no extra; `uv sync --frozen` installs only their shared dependencies. Enter your `entity/project` in the notebook and follow the same setup exercise. Tools and training run on your laptop; model requests and publication use your Forge account. You don’t need Docker or a local API service.

## Work through an exercise

Each step explains the task, shows the code to edit, and provides a local check before you run it. Afterward, look at the result and follow the **Inspect in Forge** instruction. It might ask you to find a tool’s arguments in Agent Lens or compare two forecasts in a W&B run.

The numbered buttons let you browse without starting work. If a run button is disabled, the message beside it names the step to complete first. App view keeps the exercise editors visible and hides support cells. Switch to code view when you want to follow those calls too.

Drafts save as you edit. Completed runs save the code they used, so changing a draft doesn’t rewrite an earlier result. The notebook also uploads checkpoints as W&B Artifacts: versioned collections of your code, predictions, model weights, and progress. Check that an upload succeeded before discarding the notebook runtime. On your laptop, keep the `.workshop/` directory to resume later.

The default inference allowance is $8 per workspace. You can change it during setup. It includes retries and reserves a maximum cost when a request’s usage is unavailable; it is a notebook stop, not an account-wide billing limit. Notebook compute is billed separately.

<details>
<summary>If a run or upload is interrupted</summary>

Completed work is reused when you reopen the notebook. An interrupted run waits for you to inspect it and choose another attempt. A failed trace or comparison upload can be retried from the saved result without training or calling the model again.

Native EvalTables returned HTTP 500 in our rehearsal. The notebook comparison and Weave records remain available while that publication is unavailable. The notebook shows the upload status separately from the experiment’s result.
</details>

## What happened in the recorded rehearsal

Solar uses GOES-15 X-ray measurements and NASA SDO/AIA images, prepared for small CPU experiments. On the reserved image dates, average error was 0.125762 for persistence, 0.122442 for the manually written model, and 0.110011 for the agent-selected model. The agent proposed a zero-initialized residual head and then a masked absolute-error training loss. Its final version had 10.2% lower error than the manual version under the same training budget.

That comparison covers 199 overlapping windows from two days, with one seed. It shows one completed research loop, not a reliable solar-forecasting result. The short GOES training run did worse than persistence. Both results stay in the workshop so you can inspect what the code produced. [Data and calculation details](docs/solar-evidence.md).

Pending uses fictional accounts and payments, including a tool that changes account state before its response times out. All 12 final runs reached the correct account state; the editor chose to retain the manual harness. An unchanged version is a valid outcome. Recorded examples are labeled separately from your own results.

- [Solar recorded dashboard](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=ogpa6vhy8db)
- [Pending recorded dashboard](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=nkyxiy1o6wn)
- [Solar rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==)
- [Pending rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-51a0006f--VmlldzoxODMwMjcxMA==)

## Run a workshop or build your own

The [facilitator notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view) reads progress and help requests from the project links you supply. A missing update means the participant’s status is unknown. Ask them before assuming a run failed.

The [starter notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzI=/view) shows the saving and tracing pattern for another workshop:

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

Put the experiment, scorer, tracing, and improvement code in the notebook where participants can edit it. The package handles project identity, saving, publication, and progress. See the [framework guide](docs/framework.md) and [source map](docs/source-map.md).

- [Current demo guide: both recorded flows](docs/current-demo-guide.md)
- [Four-hour facilitator guide](docs/facilitator.md)
- [Deck notes and Pending exercise references](docs/deck-guide.md)
- [Solar data and experiment design](docs/solar-contract.md)
- [Release checks and limitations](docs/release-checks.md)
- [Build and publish the kit](docs/maintenance.md)

Previous releases and deployment notes are linked from the [archive](docs/archive.md).
