# Forge Workshop Kit

Six coding workshops for testing changes to agents and models. Build an office agent, train solar forecasts, route customer requests, inspect circuit boards, coordinate coding agents, or investigate an airline agent's work. Each workshop follows an actual result through its code, data, trace, and evaluation. Worked examples distinguish implementation repairs from model improvements; live comparisons can also tie or regress.

Each participant works in their own project. The facilitator can read the progress you publish, but cannot run your notebook. You use your own Forge authentication, inference access, and notebook compute.

## Choose your workshop

| Workshop | What you’ll do |
| --- | --- |
| [Solar Autoresearch · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | Join a research lab working with real satellite observations. Build forecasts, compare training settings, then ask an agent to propose and test code changes. Six hours. |
| [Pending, Inc. · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | Give an office agent tools for refunds and account access. Check its work, edit its instructions, then build an agent that makes and tests further edits. Four hours. |
| [Route customer requests · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) | Compare classifiers on Banking77, review mistakes, check a judge against human labels, then release the router and repair a controlled loading defect. Five and a half hours. |
| [Find defective parts · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) | Compare whole-image and patch features on real VisA circuit-board photographs, spend a fixed review budget, and reproduce the selected detector. Four hours. |
| [Build a transit app · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) | Give two coding agents separate parts of a departure board, review and test their patches, then compare fresh workers with and without a checked lesson. Real historical MBTA schedules. Six hours. |
| [Monitor an airline service agent · open template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) | Inspect booking changes in Agent Lens, review a native tag against labeled turns, turn observations into regression cases, and test an itinerary repair. Six-hour technical preview; native AI tag tests currently return HTTP 500. Copy the template into your project or [run the source locally](notebooks/airline_monitoring.py). |

Use the companion deck alongside your notebook:

| Workshop | Present | Download |
| --- | --- | --- |
| Pending, Inc. | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/pending/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/pending/pending-inc.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/pending/pending-inc-source.zip) |
| Solar Autoresearch | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/solar/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/solar/solar-autoresearch.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/solar/solar-autoresearch-source.zip) |
| Customer request routing | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/routing/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/routing/request-routing.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/routing/request-routing-source.zip) |
| Circuit-board inspection | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/inspection/visual-inspection.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/inspection/visual-inspection-source.zip) |
| Transit software factory | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/transit/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/transit/transit-factory.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/transit/transit-factory-source.zip) |
| Airline monitoring and evaluations | [Browser deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) | [PDF](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/airline-monitoring.pdf) · [Editable source](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/airline-monitoring-source.zip) |

Preview a worked diagram: [forecasting losses](https://ash0ts.github.io/forge-workshop-kit/solar/graphics-preview.png), [routing errors and F1](https://ash0ts.github.io/forge-workshop-kit/routing/graphics-preview.png), [circuit-board patch distances](https://ash0ts.github.io/forge-workshop-kit/inspection/graphics-preview.png), [atomic task claims](https://ash0ts.github.io/forge-workshop-kit/transit/graphics-preview.png), or [itinerary replacement](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/graphics-preview.png). The browser decks reveal the intermediate steps; the PDFs include those states.

These decks follow the current gateway-free notebooks. Version 0.10.0 adds two ARIA investigations to each workshop: question a development result, then check the frozen comparison before writing the Report. Participants form their own explanation first and verify one claim against a saved record. The [ARIA activity guide](docs/aria-investigations.md) describes the live and recorded paths. Experiment results and workflow identities are unchanged. Airline's [qualification record](docs/airline-monitoring-qualification.md) separates completed checks from unavailable product features and remaining rehearsals. Earlier releases and the teaching datasets keep their existing versioned download links.

The [twelve recorded ARIA investigations](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.10.0/aria-investigations-v0.10.0.zip) include exact prompts, actual responses, source excerpts, and annotated captures. Download them for offline use or when your project does not have ARIA access.

For a short demonstration, follow the [current demo guide](docs/current-demo-guide.md). It takes you from a notebook exercise to a trace, code change, and recorded result.

These are technical previews. The [release checks](docs/release-checks.md) describe what we’ve tested and the external-attendee and human rehearsals still needed.

For setup and recovery, follow [Copy the notebook and start](docs/setup.md).

## Start in Forge

1. Sign in to [Forge](https://forge.coreweave.com). Create a public teaching project under your account or a team where you have write access. Its name has two parts, such as `your-name/solar-workshop`.
2. Open a template above and choose **Copy to project**. Select your project and open the editable copy. If the project isn’t offered in the copy dialog, download the notebook’s `.py` file from [notebooks](notebooks) and import it into your project.
3. Use marimo’s **Run all stale cells** control once to initialize the notebook. This creates the controls; it does not press the exercise run buttons or start training or inference. Inspect the opening development example and predict what should happen before connecting.
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

Airline also uses only the shared dependencies: run `uv sync --frozen`, `uv run wandb login`, then `uv run marimo edit notebooks/airline_monitoring.py`. Its bundled bookings are fictional records adapted from a pinned MIT-licensed Sierra tau-bench release. This is a teaching simulator with scripted passenger confirmations, not a benchmark reproduction or live airline integration. See the [source and partitions](src/forge_workshop_kit/assets/airline/provenance.json), [six-hour runbook](docs/airline_monitoring-runbook.md), and [qualification](docs/airline-monitoring-qualification.md).

## Work through an exercise

Each step explains the task, shows the code to edit, and provides a local check before you run it. Afterward, look at the result and follow the **Inspect in Forge** instruction. It might ask you to find a tool’s arguments in Agent Lens or compare two forecasts in a W&B run.

The numbered buttons let you browse without starting work. If a run button is disabled, the message beside it names the step to complete first. App view keeps the exercise editors visible and hides support cells. Switch to code view when you want to follow those calls too.

Use the guided views to follow one ticket or forecast through its code and results. Pending shows the tool arguments, returned observation, and resulting account state. Solar lets you compare forecasts at the same timestamp and calculate what the scorer counts. Selecting a view never launches training or inference. The [visual sequence guide](docs/visual-sequence.md) has the questions to investigate in Forge.

Drafts save as you edit. Completed runs save the code they used, so changing a draft doesn’t rewrite an earlier result. The notebook also uploads checkpoints as W&B Artifacts: versioned collections of your code, predictions, model weights, and progress. Check that an upload succeeded before discarding the notebook runtime. On your laptop, keep the `.workshop/` directory to resume later.

The default inference allowance is $8 per workspace. You can change it during setup. It includes retries and reserves a maximum cost when a request’s usage is unavailable; it is a notebook stop, not an account-wide billing limit. Notebook compute is billed separately.

At each ARIA stop, copy the question, open the selected Forge record, and add the relevant native context where that control is available. Copying the prompt does not attach records or send a message. Check which records ARIA actually read before accepting its explanation. Live ARIA requires a supported team project and enabled Smart features; personal-project participants can use the bundled instructor recordings. ARIA usage follows your organization settings and is outside the notebook allowance. Citation checks save locally and never approve or trigger an experiment.

In the airline workshop, native Agent Lens automatic tagging and Alignment tests use separate service billing. They are outside the notebook's inference allowance. Disable **Apply with AI** for your workshop tag when you finish; closing the notebook does not disable it. A missing tag assignment does not establish that the turn was judged negative.

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
| Airline bookings | All **40/40** live conversations pass independent booking checks. Starting and repaired agents each pass **6/6** reserved and **4/4** subsequent requests. | No live quality gain was observed. A separately labeled local adapter drill demonstrates the itinerary repair; its controlled failures are not counted as live agent mistakes. |

See [transit results and the captioned walkthrough](docs/transit-workshop.md), [routing evidence](docs/routing-workshop.md), [inspection evidence](docs/inspection-workshop.md), and [Solar qualification](docs/solar-qualification.md) for frozen protocols, all outcomes, sources, and limitations. Dataset labels supplied by the authors, participant reviews, and model suggestions remain distinct.

The [airline qualification](docs/airline-monitoring-qualification.md) and [machine-readable results](examples/airline-monitoring/qualification.json) record all 40 conversations. They cost **$0.02330616**; one explanation-judge call brought direct inference to **$0.02401506**, with no unknown usage. Native tag judging and notebook compute are separate. Native tag configuration and manual labels were accessible, but six Alignment test requests returned HTTP 500, and Insights had no completed cluster for the new session. The workshop therefore does not claim demonstrated automatic monitoring accuracy or a ready-to-run classroom experience. External-account and human rehearsals remain outstanding.

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

## Create or run another workshop

The repository includes a [workshop authoring skill](.agents/skills/forge-workshops/SKILL.md) and a shared `forge-workshop` command. They connect the authored notebook, exercise references, deck, and rehearsal records. Participants do not need either to use a copied template.

Start with the [authoring guide](docs/authoring.md). A rehearsal records exactly which current notebook actions ran; browser, external-account, and human checks remain separate. The [maintenance guide](docs/maintenance.md) covers builds and explicit publication.
