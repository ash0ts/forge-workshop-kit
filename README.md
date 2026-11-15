# Forge Workshop Kit

Six Python workshops for people learning to build, evaluate, and improve agents and models in Forge. Each includes an editable notebook, a companion deck, exercises with local checks, and recorded results you can inspect when a live service is unavailable.

Participants copy a notebook into their own project and use their own credentials. The facilitator can read published progress and help requests. There is no workshop gateway or shared account.

**These are technical previews.** The notebooks and decks are published, but external-account checks and participant rehearsals are still outstanding. See [current status and next steps](next-up.md) before scheduling a class.

## Choose your workshop

The durations include coding, discussion, and breaks. Participants should be comfortable reading basic Python.

| Workshop | What you build and investigate | Time | Deck |
| --- | --- | --- | --- |
| [Pending, Inc.](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) | Give an office agent tools for refunds and account access, then test manual and agent-written changes to its harness. | 4 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/pending/) |
| [Solar Autoresearch](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) | Train forecasts on real satellite observations, compare experiments, and test a research agent’s code edits. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/solar/) |
| [Customer request routing](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) | Compare classifiers, review mistakes, then release the selected router and repair a controlled loading defect. | 5½ h | [Slides](https://ash0ts.github.io/forge-workshop-kit/routing/) |
| [Circuit-board inspection](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) | Compare image features on real board photographs, choose what to label, and reproduce a detector. | 4 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/inspection/) |
| [Transit software factory](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) | Coordinate coding agents building a departure board, integrate their patches, and test whether a shared lesson helps the next build. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/transit/) |
| [Airline monitoring](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) | Inspect simulated booking changes, review a monitoring rule, curate regression cases, and test an itinerary repair. | 6 h | [Slides](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) |

The [deck library](https://ash0ts.github.io/forge-workshop-kit/) includes PDFs and editable slide sources. For a short demonstration rather than a full class, use the [demo guide](docs/current-demo-guide.md).

## Start in Forge

1. Sign in to [Forge](https://forge.coreweave.com) and create a teaching project where you have write access. Use a public project if the facilitator should read progress without an invitation. Only publish the supplied public or fictional data there.
2. Open a notebook above, choose **Copy to project**, and open your editable copy.
3. Use marimo’s **Run all stale cells** once to create the controls. It does not press the exercise Run buttons or start training or inference. Inspect the opening example, then follow the notebook’s access check and first tracing exercise.
4. Confirm the displayed project is yours. Share its link with the facilitator if you want progress monitoring. They do not need your API key.

You need project write access, notebook compute, and inference access for the model-call exercises. A successful project check does not establish all three. The [setup guide](docs/setup.md) covers import alternatives, access checks, and recovery.

## Start on your laptop

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/). For Solar:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra solar
uv run --extra solar wandb login
uv run --extra solar marimo edit notebooks/solar_autoresearch.py
```

Enter your writable `entity/project` in the notebook. Use the [local setup table](docs/setup.md#work-locally) for the other workshops. Tools and training run in the notebook’s Python runtime; inference and publication use your Forge account. You do not need Docker or a local service.

## While you work

Each step puts the task, editable code, local check, run control, result, and Forge links together. Browsing or editing does not execute an experiment. A disabled run control names the prerequisite you need to complete.

Drafts and completed results save locally. Uploaded W&B checkpoint artifacts let you restore them after replacing a runtime. Keep `.workshop/` on a laptop and confirm the checkpoint upload before discarding a hosted runtime. [Resume and recovery instructions](docs/setup.md#resume-or-recover) explain how to retry an upload without repeating an experiment.

The default **$8 inference allowance** is adjustable per workspace. It is not an account-wide billing limit. Notebook compute, ARIA, and native Agent Lens tag judging have separate billing. In Airline, disable **Apply with AI** when you finish; closing the notebook does not disable the tag.

Each workshop has two [ARIA investigations](docs/aria-investigations.md). Participants explain a result, ask ARIA about selected records, and check a citation. Live access needs a supported team project and Smart features. The bundled recordings support the same exercise without ARIA access. Copying a prompt does not attach records or send a message.

## What happened in the recorded rehearsal

The recordings include improvements, ties, and regressions. The classifiers improved in their qualified comparisons; Pending’s harnesses tied; one Solar image seed regressed; the Transit team did worse on two checks; both Airline versions passed. See [recorded results and limitations](docs/recorded-results.md) for the numbers, protocols, and source records.

Weave-backed native EvalTables comparisons are available. Airline’s last AI Alignment tests returned HTTP 500, and its prepared Insights workflow remains unqualified. [Release checks](docs/release-checks.md) distinguish working paths from outstanding access and rehearsal checks.

## Facilitate or contribute

The [facilitator notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view) reads the project links you supply. Missing updates mean “unknown,” not “failed.” The [documentation index](docs/README.md) links each workshop’s schedule and evidence.

For changes to the kit, start with [CONTRIBUTING.md](CONTRIBUTING.md). The [technical specification](techspec.md) explains how notebooks, saving, accounting, tracing, and publication fit together. [Next steps](next-up.md) separates completed work from what still needs qualification.

To add a workshop, use the [starter notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzI=/view), [authoring guide](docs/authoring.md), and repository-local [forge-workshops skill](.agents/skills/forge-workshops/SKILL.md). Participants do not need the skill. Earlier releases and gateway-era materials are preserved in the [archive](docs/archive.md).
