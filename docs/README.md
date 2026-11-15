# Documentation

Start with the [repository README](../README.md) to choose a workshop. Use this index when you need setup help, a teaching schedule, or the implementation behind an exercise.

## Participate or facilitate

| Need | Read |
| --- | --- |
| Choose materials for a reader, demo, hands-on pilot, or new workshop | [Use the workshop materials](use-the-workshops.md) |
| Learn from a worked example before opening the notebook | [Public learning Reports](../reports/README.md) |
| Copy a template, run locally, or recover saved work | [Setup](setup.md) |
| Give a short demonstration using saved results | [Demo guide](current-demo-guide.md) |
| Present the companion slides | [Deck guide](deck-guide.md) |
| Ask ARIA about a result and check its answer | [ARIA investigations](aria-investigations.md) |
| Compare cases or retry evaluation publication | [Evaluations](evaluations.md) |
| Understand the reported gains, ties, and failures | [Recorded results](recorded-results.md) |
| Check whether the workshop is ready for your audience | [Current status and next steps](../next-up.md), [release checks](release-checks.md) |

The [facilitator setup](setup.md#read-participant-progress) explains the saved roster and read-only progress monitor. It does not control participant executions.

## Workshop runbooks and evidence

| Workshop | Schedule and teaching guidance | Data, design, and recorded evidence |
| --- | --- | --- |
| Pending, Inc. | [Four-hour runbook](pending-facilitator.md) | [Exercise reference and recorded tie](deck-guide.md#pending-inc), [simulator source](../src/forge_workshop_kit/pending) |
| Solar Autoresearch | [Six-hour runbook](facilitator.md) | [Experiment contract](solar-contract.md), [data and first rehearsal](solar-evidence.md), [qualification across seeds](solar-qualification.md) |
| Customer request routing | [Five-and-a-half-hour workshop](routing-workshop.md) | Same guide covers Banking77, classifier results, and the release/rollback drill. |
| Circuit-board inspection | [Four-hour workshop](inspection-workshop.md) | Same guide covers VisA PCB1, feature preparation, and both qualification recipes. |
| Transit software factory | [Six-hour runbook](transit-facilitator.md) | [Data, coordinator, and build results](transit-workshop.md) |
| Airline monitoring | [Six-hour runbook](airline_monitoring-runbook.md) | [Qualification and native monitoring limitations](airline-monitoring-qualification.md), [data provenance](../src/forge_workshop_kit/assets/airline/provenance.json) |

[Data preparation](../data/README.md) links acquisition tools and immutable teaching bundles. [Advanced modules](advanced/README.md) cover optional training, release, and remote execution; their access checks are separate from the core workshops.

## Contribute or maintain

| Document | Owns |
| --- | --- |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Local contributor setup and the edit/check workflow |
| [techspec.md](../techspec.md) | Architecture, source map, identities, saving, accounting, and publication contracts |
| [Authoring](authoring.md) | Scaffolding, manifests, exercise references, and rehearsal adapters |
| [Teaching sequence](teaching-sequence.md) | How to explain a concept, show its effect, and ask participants to investigate it |
| [Deck sources](../decks/README.md) | Shared Slidev installation and local presentation commands |
| [Maintenance](maintenance.md) | Packaging, destination-verified publication, and release recovery |
| [AGENTS.md](../AGENTS.md) | Repository instructions for coding agents |
| [forge-workshops skill](../.agents/skills/forge-workshops/SKILL.md) | How an assistant should use these guides when authoring or rehearsing |

Keep implementation contracts in these guides and unfinished work in [next-up.md](../next-up.md). [Release notes](release-notes.md) describe changes between versions; the [archive](archive.md) preserves earlier checks and workshop releases. Historical evidence is not current setup guidance.
