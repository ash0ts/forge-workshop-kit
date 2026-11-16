# Use the workshop materials

These workshops are for engineers who can read basic Python and want to understand how to investigate and change an AI application. Each starts with work someone needs done: preserve a passenger’s return flight, find a small defect, or deliver an application built by two agents. Participants inspect an outcome, change code or data, and compare matching cases.

Choose the problem closest to the audience’s work. The six examples cover agent development, agent-assisted research, model improvement and release, visual inspection, multi-agent delivery, and monitoring. They are independent sessions, not a required course sequence.

## Choose a package

| Use | What to send or open | What to do next |
| --- | --- | --- |
| **Explain a workflow** | One public Report from the table below. It includes diagrams, code, actual results, and a notebook link. | Ask the reader which change affected the outcome and what they would test next. |
| **Introduce the full collection** | The [ten-minute Loom script](loom-walkthrough.md) and [meeting packet](sharing.md). | Show the customer problem and one Forge investigation for each workshop, then invite viewers to try one exercise. |
| **Show a short demo** | The matching deck and [6–10 minute walkthrough](current-demo-guide.md). Use its saved traces, comparisons, and recorded fallback. | Show one input, the change, and the resulting behavior. Open the Forge record that establishes it. |
| **Run a hands-on pilot** | The participant notebook, [setup guide](setup.md), and [facilitator start guide](facilitator-start.md). | Use its per-deck running guide, copy into a writable project, and check the first saved result before running the full session. |
| **Adapt the kit** | The [starter notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzI=/view), [authoring guide](authoring.md), and [workshop skill](../.agents/skills/forge-workshops/SKILL.md). | Define one task, an intervention, and a comparison. Keep the code learners change visible; reuse saving, tracing, publication, and progress. |

The Reports can be read independently. Live exercises use the participant's own project, credentials, and product access. The facilitator reads progress from the supplied project roster; there is no workshop gateway.

## Choose the workflow

These are starting points for a conversation, not a required course sequence.

| Start here when the question is… | Worked example and takeaway | Materials |
| --- | --- | --- |
| **How do we change an agent's behavior and know what happened?** | **Pending:** implement tools and observation handoff for a billing/access agent. Trace a retry, edit the harness, and compare checked account states. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-an-agent-you-can-inspect%2C-then-test-changes-to-its-harness--VmlldzoxODMxMzUzMQ==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/pending/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) |
| **How do we test an agent's proposed research changes?** | **Solar:** train forecasts on real satellite observations, record the experiment, and compare agent-written loss and initialization changes. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Test-research-agent-changes-against-real-solar-observations--VmlldzoxODMxMzUzMg==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/solar/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) |
| **How do we improve a classifier and check the version we release?** | **Routing:** compare representations for banking requests, review mistakes, and investigate a controlled label-mapping defect through repair and rollback. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Train-a-support-router%2C-then-check-what-you-released--VmlldzoxODMxMzUzNw==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/routing/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjg=/view) |
| **How do we decide whether features or more reviewed data help a detector?** | **Inspection:** examine real circuit-board photographs, compare whole-image and patch features, and inspect misses and false alarms under matched review budgets. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-a-missed-defect%2C-then-test-the-change--VmlldzoxODMxMzUzOA==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5Mjk=/view) |
| **How do we coordinate coding agents and verify their combined work?** | **Transit:** assign components of a departure board, integrate patches, test the application, and compare subsequent builds with and without an accepted lesson. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Coordinate-coding-agents%2C-then-test-the-app-they-built--VmlldzoxODMxMzUzOQ==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/transit/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) |
| **How do we turn observed agent behavior into monitoring and regression tests?** | **Airline:** inspect simulated itinerary changes, review a monitoring rule, curate cases, and compare booking outcomes. Native monitoring activities still need qualification. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Turn-an-airline-agent%27s-behavior-into-monitoring-rules-and-regression-tests--VmlldzoxODMxMzU0MA==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) · [Notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) |

For a first introduction to Agent Lens, use Pending's tool-call investigation. For an ML audience, use Solar's saved forecast or Inspection's missed board. Use Routing for a release discussion, Transit for coordination, and Airline for the relationship between monitoring and offline tests.

## Follow the AI work through Forge

The shared sequence follows Forge’s [run → observe → curate → improve → evaluate](https://www.coreweave.com/products/coreweave-forge) workflow. People make the decisions between those operations. A changed implementation may improve a result, tie, or introduce another mistake.

| Operation | Participant’s question | Where the workshop answers it |
| --- | --- | --- |
| **Run** | What code and inputs produced this output? | The editable Notebook runs the exercise explicitly. Runs record settings, measurements, and timing; Artifacts preserve source, data, weights, and outputs. |
| **Observe** | What did the agent, model, or worker do? | Agent Lens exposes requests, tools, errors, and handoffs. Runs and Sweeps show training curves and configuration differences. |
| **Curate** | Which examples deserve review or a regression check? | Participants inspect requests, images, and state changes, then save reviewed cases as versioned data. Airline adds native monitoring and Alignment exercises, whose outstanding access checks remain explicit. |
| **Improve** | Which intervention are we testing? | Participants edit a harness, change a representation, select data, or review an agent’s code proposal. The notebook keeps the change and its execution visible. |
| **Evaluate** | Did the change help on matching cases, and what should we retain? | Weave and native EvalTables compare outputs and scorer results. Artifacts identify the version to reproduce; a Report explains the decision and limitations. |

The research agent or coding workers perform the measured work. **ARIA has a separate role:** investigate selected saved records and challenge the participant’s explanation. Participants check a cited record before accepting a claim. An ARIA answer does not become an evaluation score, a reviewed label, or an automatic code change.

These are teaching examples drawn from public data and fictional tasks, not customer case studies. Solar uses GOES and AIA observations; Routing uses Banking77 requests; Inspection uses VisA PCB1 photographs; Transit uses a historical MBTA schedule. Pending’s accounts and Airline’s benchmark bookings are simulated. Their relevance comes from the decisions being practiced: preserving state, choosing data, comparing changes, and reproducing what ran.

## Run the first exercise

1. Read the selected Report's opening case and look at its recorded outcome.
2. Open its notebook, choose **Copy to project**, and confirm that the displayed destination is your project.
3. Use **Run all stale cells** to initialize the controls. Complete the access check and the first free code check. Training and inference start only through the exercise's explicit run controls.
4. Run the exercise, inspect its result, and open the linked Forge record. Note any confusing instruction or access failure, including the step name and error text. Do not share credentials.

The [setup guide](setup.md) covers laptop use, access requirements, spending controls, and restoration. Each workshop also includes two ARIA investigations: explain a result, ask about selected records, then verify one claim. Recordings are available when live ARIA access is unavailable.

## Before scheduling a class

All six remain **technical previews**. Fresh-account checks and participant rehearsals are outstanding. Use recorded examples for demonstrations and qualify the intended live path before a class. Airline's AI Alignment and prepared Insights activities need further native-feature validation. Check [current status](../next-up.md) rather than assuming access from a screenshot.

The examples preserve improvements, ties, and failures. The [recorded-results guide](recorded-results.md) explains which comparisons support each claim. Session allocations, including breaks, are listed in the [workshop catalog](../README.md#choose-your-workshop).
