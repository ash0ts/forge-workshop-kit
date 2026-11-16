# Use the workshop materials

These workshops are for engineers who can read basic Python. Each starts with a task someone needs done: refund a duplicate charge, find a damaged circuit board, or change a flight without losing the return journey. Participants inspect what the system did, work out what to change, and test whether that change helped.

Choose the problem closest to your audience’s work. You can use one example in a short demonstration or teach the full workshop. The sessions are independent.

## Choose a package

| Use | What to send or open | What to do next |
| --- | --- | --- |
| **Explain a workflow** | One public Report from the table below. It includes diagrams, code, actual results, and a notebook link. | Ask the reader which change affected the outcome and what they would test next. |
| **Introduce the full collection** | The [workshop overview](workshop-overview.md) and [public library](https://ash0ts.github.io/forge-workshop-kit/). | Show the customer problem and one Forge investigation for each workshop, then invite viewers to try one exercise. |
| **Show a short demo** | The matching deck and [6–10 minute walkthrough](current-demo-guide.md). Use its saved traces, comparisons, and recorded fallback. | Show one input, the change, and the resulting behavior. Open the Forge record that establishes it. |
| **Run a hands-on pilot** | The participant notebook, [setup guide](setup.md), and [facilitator start guide](facilitator-start.md). | Follow the workshop's start page to download and launch its current notebook. Connect a writable Forge project and check the first saved result before running the full session. |
| **Adapt the kit** | The [starter source](../notebooks/starter.py), [authoring guide](authoring.md), and [workshop skill](../.agents/skills/forge-workshops/SKILL.md). | Open the starter with `uvx --from marimo==0.25.2 marimo edit --sandbox notebooks/starter.py`. Define one task and a change to test. Reuse the kit's saving and publication code while keeping learner functions visible. |

The Reports can be read independently. Live exercises use the participant's own project, credentials, and product access. The facilitator reads progress from the supplied project roster; there is no workshop gateway.

## Choose the workflow

| Start here when the question is… | Worked example and takeaway | Materials |
| --- | --- | --- |
| **How do we change an agent's behavior and know what happened?** | **Pending:** implement tools and observation handoff for a billing/access agent. Trace a retry, edit the harness, and compare checked account states. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-an-agent-you-can-inspect%2C-then-test-changes-to-its-harness--VmlldzoxODMxMzUzMQ==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/pending/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/pending.html) |
| **How do we test an agent's proposed research changes?** | **Solar:** train forecasts on real satellite observations, record the experiment, and compare agent-written loss and initialization changes. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Test-research-agent-changes-against-real-solar-observations--VmlldzoxODMxMzUzMg==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/solar/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/solar.html) |
| **How do we improve a classifier and check the version we release?** | **Routing:** compare representations for banking requests, review mistakes, and investigate a controlled label-mapping defect through repair and rollback. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Train-a-support-router%2C-then-check-what-you-released--VmlldzoxODMxMzUzNw==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/routing/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/routing.html) |
| **How do we decide whether features or more reviewed data help a detector?** | **Inspection:** examine real circuit-board photographs, compare whole-image and patch features, and inspect misses and false alarms under matched review budgets. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-a-missed-defect%2C-then-test-the-change--VmlldzoxODMxMzUzOA==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/inspection/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/inspection.html) |
| **How do we coordinate coding agents and verify their combined work?** | **Transit:** assign components of a departure board, integrate patches, test the application, and compare subsequent builds with and without an accepted lesson. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Coordinate-coding-agents%2C-then-test-the-app-they-built--VmlldzoxODMxMzUzOQ==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/transit/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/transit.html) |
| **How do we turn observed agent behavior into monitoring and regression tests?** | **Airline:** inspect simulated itinerary changes, review a monitoring rule, curate cases, and compare booking outcomes. Native monitoring activities still need qualification. | [Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Turn-an-airline-agent%27s-behavior-into-monitoring-rules-and-regression-tests--VmlldzoxODMxMzU0MA==) · [Deck](https://ash0ts.github.io/forge-workshop-kit/airline_monitoring/) · [Start the notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/airline_monitoring.html) |

For a first introduction to Agent Lens, use Pending's tool-call investigation. For an ML audience, use Solar's saved forecast or Inspection's missed board. Use Routing for a release discussion, Transit for coordination, and Airline for the relationship between monitoring and offline tests.

## Follow the AI work through Forge

Show a result before introducing the product screen. A participant who has just seen the wrong queue destination has a reason to open the prediction row. Someone who has seen a refund succeed needs to know which payment changed and whether a retry could refund it twice.

| Workshop | What participants investigate and change | What to open in Forge |
| --- | --- | --- |
| **Pending** | An office agent refunds a duplicate charge in a simulated account. Follow the tool arguments and account changes, then repair a retry that can create a duplicate membership. | Open the Agent Lens tool call and find the operation ID. Compare it with the retry and the checked account state. |
| **Solar** | A model trained on GOES satellite readings forecasts worse than copying the latest reading. Inspect the forecasts and training settings before testing a different recipe. Later, review an agent's edits to an image predictor trained on AIA observations. | Open the selected training run to compare loss and validation error, then its Artifact to recover the code and weights that produced the forecast. |
| **Routing** | A Banking77 request about a replacement card goes to the wrong queue. Inspect the words and classifier scores, test sentence embeddings, then check that loading the saved classifier preserves its intent mapping. | Open the same request in EvalTables to compare destinations, probabilities, and review decisions. Use the saved model Artifact to reproduce the selected version. |
| **Inspection** | A detector misses a defect in a VisA circuit-board photograph. Compare whole-image and patch features, adjust the inspection cutoff, and count the misses and false alarms each choice produces. | Open the board's EvalTables row and compare its photograph, score, cutoff, and label across detector versions. |
| **Transit** | Two coding agents build a departure board from a historical MBTA schedule. Review their patches, test the combined app, and decide whether a verified lesson helps with the next feature. | Follow each worker's edits and tests in Agent Lens, then open the matching acceptance scenarios in EvalTables. Check the delivered app as well as the worker's test result. |
| **Airline** | An agent changes simulated bookings. Check that an outbound-flight change preserves the return flight, define a monitoring rule from reviewed turns, and turn an incident into a regression case. | Inspect the returned itinerary in Agent Lens. Compare the human review with the tag judgment in Alignment, then compare original and repaired bookings in EvalTables. See the access limitations below before planning the native monitoring exercise. |

Each workshop also includes two short ARIA investigations. For example, in Inspection you might suspect that a small defect disappeared in the whole-image representation. Ask ARIA to check that explanation against the saved photograph, model score, and cutoff. Open the record it cites and decide whether the result supports testing patch features. The notebook includes the question, selected records, and a recorded investigation for participants without live ARIA access.

## Run the first exercise

1. Read the selected Report's opening case and look at its recorded outcome.
2. Follow the workshop's start page to download and launch the current notebook. Enter your writable Forge project in setup.
3. Use **Run all stale cells** to initialize the controls. Complete the access check and the first free code check. Training and inference start only through the exercise's explicit run controls.
4. Run the exercise, inspect its result, and open the linked Forge record. Note any confusing instruction or access failure, including the step name and error text. Do not share credentials.

The [setup guide](setup.md) covers laptop use, access requirements, spending controls, and returning to saved work.

## Before scheduling a class

All six remain **technical previews**. Fresh-account checks and participant rehearsals are still outstanding. Use the recorded examples for demonstrations, and try the intended exercises with a participant account before scheduling a live class. Airline's AI Alignment and prepared Insights activities have additional access checks to complete. See [current status](../next-up.md).

The examples preserve improvements, ties, and failures. The [recorded-results guide](recorded-results.md) explains which comparisons support each claim. Session allocations, including breaks, are listed in the [workshop catalog](../README.md#choose-your-workshop).
