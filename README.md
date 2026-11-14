# Forge Workshop Kit

Five coding workshops for testing changes to agents and models. Build an office agent, train solar forecasts, route customer requests, inspect circuit boards, or coordinate coding agents building a transit app. Each workshop follows an actual result through its code, data, trace, and evaluation. Worked examples show a measured repair or gain; the live exercise can also tie or regress.

Each participant works in their own project. The facilitator can read the progress you publish, but cannot run your notebook. You use your own Forge authentication, inference access, and notebook compute.

## Choose your workshop

| Workshop | What you’ll do |
| --- | --- |
| [Solar Autoresearch · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | Join a research lab working with real satellite observations. Build forecasts, compare training settings, then ask an agent to propose and test code changes. Six hours. |
| [Pending, Inc. · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | Give an office agent tools for refunds and account access. Check its work, edit its instructions, then build an agent that makes and tests further edits. Four hours. |
| [Route customer requests · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) | Compare two classifiers on Banking77, review mistakes, check a judge against human labels, and freeze a revised router. Four hours. |
| [Find defective parts · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) | Compare whole-image and patch features on real VisA circuit-board photographs, spend a fixed review budget, and reproduce the selected detector. Four hours. |
| [Build a transit app · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) | Give two coding agents separate parts of a departure board, review and test their patches, then compare fresh workers with and without a checked lesson. Real historical MBTA schedules. Six hours. |

Use the companion deck alongside your notebook:

| Workshop | Present | Download |
| --- | --- | --- |
| Pending, Inc. | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/pending/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/pending/pending-inc.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/pending/pending-inc-source.zip) |
| Solar Autoresearch | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/solar/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/solar/solar-autoresearch.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/solar/solar-autoresearch-source.zip) |
| Customer request routing | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/routing/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/routing/request-routing.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/routing/request-routing-source.zip) |
| Circuit-board inspection | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/inspection/visual-inspection.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/inspection/visual-inspection-source.zip) |
| Transit software factory | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/transit/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/transit/transit-factory.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/transit/transit-factory-source.zip) |

These decks follow the current gateway-free notebooks. The [v0.6.2 maintenance release](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.6.2) includes notebooks, PDFs, and editable deck sources. Teaching datasets keep their existing versioned download links.

For a short demonstration, follow the [current demo guide](docs/current-demo-guide.md). It takes you from a notebook exercise to a trace, code change, and recorded result.

These are technical previews. The [release checks](docs/release-checks.md) describe what we’ve tested and the external-attendee and human rehearsals still needed.

For setup and recovery, follow [Copy the notebook and start](docs/setup.md).

## Start in Forge

1. Sign in to [Forge](https://forge.coreweave.com). Create a public teaching project under your account or a team where you have write access. Its name has two parts, such as `your-name/solar-workshop`.
2. Open a template above and choose **Copy to project**. Select your project and open the editable copy. If the project isn’t offered in the copy dialog, download the notebook’s `.py` file from [notebooks](notebooks) and import it into your project.
3. Use marimo’s **Run all stale cells** control once to initialize the notebook. This creates the controls; it does not press the exercise run buttons or start training or inference.
4. In Solar, routing, or transit, click **Connect and restore my work**. In Pending, click **Check my project and restore saved work**. In inspection, click **Connect and restore my inspection work**. Confirm that the project shown is yours. Follow the first exercise to publish a trace and open it in Agent Lens.
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

For routing, use `--extra routing` and `notebooks/request_routing.py`. For inspection, use `--extra inspection` and `notebooks/visual_inspection.py`. Download controls verify the pinned teaching data before loading it. Cached features make the required classifier exercises practical on CPU; inspection also lets you recompute four images.

For transit, run `uv sync --frozen` and `uv run marimo edit notebooks/transit_factory.py`. It uses the shared dependencies, Python's standard library, and a bundled 57 KB timetable subset. There is no live transit API or separate app server. See the [transit exercises](docs/transit-workshop.md), [six-hour facilitator guide](docs/transit-facilitator.md), and [data provenance and prepared repairs](examples/transit/README.md).

## Work through an exercise

Each step explains the task, shows the code to edit, and provides a local check before you run it. Afterward, look at the result and follow the **Inspect in Forge** instruction. It might ask you to find a tool’s arguments in Agent Lens or compare two forecasts in a W&B run.

The numbered buttons let you browse without starting work. If a run button is disabled, the message beside it names the step to complete first. App view keeps the exercise editors visible and hides support cells. Switch to code view when you want to follow those calls too.

Use the guided views to follow one ticket or forecast through its code and results. Pending shows the tool arguments, returned observation, and resulting account state. Solar lets you compare forecasts at the same timestamp and calculate what the scorer counts. Selecting a view never launches training or inference. The [visual sequence guide](docs/visual-sequence.md) has the questions to investigate in Forge.

Drafts save as you edit. Completed runs save the code they used, so changing a draft doesn’t rewrite an earlier result. The notebook also uploads checkpoints as W&B Artifacts: versioned collections of your code, predictions, model weights, and progress. Check that an upload succeeded before discarding the notebook runtime. On your laptop, keep the `.workshop/` directory to resume later.

The default inference allowance is $8 per workspace. You can change it during setup. It includes retries and reserves a maximum cost when a request’s usage is unavailable; it is a notebook stop, not an account-wide billing limit. Notebook compute is billed separately.

<details>
<summary>If a run or upload is interrupted</summary>

Completed work is reused when you reopen the notebook. An interrupted run waits for you to inspect it and choose another attempt. A failed trace or comparison upload can be retried from the saved result without training or calling the model again.

The notebooks publish native **Evaluation Tables (Preview)** through the pinned W&B SDK’s Weave backend. Use **Compare in EvalTables** to open matching cases in a saved Forge W&B workspace. Agent Lens links open the execution behind a result. The separate CES backend still returned HTTP 500 on November 14; this release does not depend on it. [Evaluation setup and recovery](docs/evaluations.md).
</details>

## What happened in the recorded rehearsal

The November 14 qualification adds these worked examples. Scores are not interchangeable across tasks.

| Exercise | Measured outcome | What it establishes |
| --- | --- | --- |
| Pending retry repair | Two memberships with a new operation ID; one with the original ID and an account check | A deterministic implementation repair in the fictional simulator. The later harness comparison remains a 4/4 tie. |
| Banking77 | Macro-F1 **0.879385 → 0.920229** on 3,080 official test requests | Frozen sentence features beat TF–IDF in this fixed classifier comparison. Three deterministic seeds reproduced the same result; they are not three independent experiments. |
| VisA PCB1 | Average precision **0.872900 → 0.885742**; misses **4 → 3**, false alarms **23 → 18** on 442 test boards | The bounded follow-up improved on already-inspected test images. This is a teaching retest; the failed first recipe remains published. |
| GOES | Persistence MAE **0.192706**; residual MLP **0.162878, 0.163880, 0.163760** across seeds 17, 29, 43 | The validation-selected recipe beat persistence in all three teaching retests. Previously inspected final dates are not newly unseen data. |
| AIA images | Changes of **+10.15%, +6.87%, −0.21%** against the manual model across the same seeds | Two improvements and one small regression. The fixed recipe did not pass the all-seed reliability gate. |
| Transit app | One worker **10/10**; two workers **8/10**. Both follow-ups **12/18** | The faster team selected the wrong train for a UTC input. Follow-up query workers stopped at input/output limits; this does not establish a memory benefit or loss. |

See [transit results and the captioned walkthrough](docs/transit-workshop.md), [routing evidence](docs/routing-workshop.md), [inspection evidence](docs/inspection-workshop.md), and [Solar qualification](docs/solar-qualification.md) for frozen protocols, all outcomes, sources, and limitations. Dataset labels supplied by the authors, participant reviews, and model suggestions remain distinct.

For the earlier November 13 results, Reports and dashboards, see the [rehearsal archive](docs/archive.md#november-13-rehearsals). The [demo guide](docs/current-demo-guide.md) identifies which saved run to open for each exercise.

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

- [Current demo guide: exercises and recorded results](docs/current-demo-guide.md)
- [Six-hour facilitator guide](docs/facilitator.md)
- [Deck notes and Pending exercise references](docs/deck-guide.md)
- [Solar data and experiment design](docs/solar-contract.md)
- [Release checks and limitations](docs/release-checks.md)
- [Build and publish the kit](docs/maintenance.md)
- [Optional SFT, release/rollback, and remote research modules](docs/advanced/README.md)

The advanced modules require their own access check and cost approval. Registry links a tested artifact; it does not deploy it. SFT changes model weights, while the core harness exercise keeps the language model fixed. Sandboxes and ARIA/Launch remain optional and are not needed to copy or run the core notebooks.

Previous releases and deployment notes are linked from the [archive](docs/archive.md).
