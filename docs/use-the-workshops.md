# Use the workshop materials

These examples teach how to change an agent or model and check what that change did. Each follows a concrete task through Python code, recorded outputs, and the corresponding Forge records. Choose the format that fits the conversation; nobody needs to complete all six workshops.

## Choose a package

| Use | What to send or open | What to do next |
| --- | --- | --- |
| **Explain a workflow** | One public Report from the table below. It includes diagrams, code, actual results, and a notebook link. | Ask the reader which change affected the outcome and what they would test next. |
| **Show a short demo** | The matching deck and [6–10 minute walkthrough](current-demo-guide.md). Use its saved traces, comparisons, and recorded fallback. | Show one input, the change, and the resulting behavior. Open the Forge record that establishes it. |
| **Run a hands-on pilot** | The participant notebook, [setup guide](setup.md), and [facilitator runbook](README.md#workshop-runbooks-and-evidence). | Copy into a writable project, complete the first exercise, and check its saved result before running the full session. |
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

## Run the first exercise

1. Read the selected Report's opening case and look at its recorded outcome.
2. Open its notebook, choose **Copy to project**, and confirm that the displayed destination is your project.
3. Use **Run all stale cells** to initialize the controls. Complete the access check and the first free code check. Training and inference start only through the exercise's explicit run controls.
4. Run the exercise, inspect its result, and open the linked Forge record. Note any confusing instruction or access failure, including the step name and error text. Do not share credentials.

The [setup guide](setup.md) covers laptop use, access requirements, spending controls, and restoration. Each workshop also includes two ARIA investigations: explain a result, ask about selected records, then verify one claim. Recordings are available when live ARIA access is unavailable.

## Before scheduling a class

All six remain **technical previews**. Fresh-account checks and participant rehearsals are outstanding. Use recorded examples for demonstrations and qualify the intended live path before a class. Airline's AI Alignment and prepared Insights activities need further native-feature validation. Check [current status](../next-up.md) rather than assuming access from a screenshot.

The examples preserve improvements, ties, and failures. The [recorded-results guide](recorded-results.md) explains which comparisons support each claim. Session allocations, including breaks, are listed in the [workshop catalog](../README.md#choose-your-workshop).
