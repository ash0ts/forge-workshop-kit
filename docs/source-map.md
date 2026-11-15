# Source map

- `scripts/solar_cells.py` and `scripts/pending_cells.py`: authored exercise cells; the notebook generator is the source of truth for hosted and laptop templates.
- `scripts/routing_cells.py` and `scripts/inspection_cells.py`: authored review, classification, judge-calibration and visual-inspection exercises.
- `scripts/transit_cells.py`: authored acceptance, worker dispatch, task ownership, memory retrieval and release exercises.
- `scripts/airline_monitoring_cells.py`: authored tracing, native tag review, regression curation, booking comparison, and subsequent-monitoring exercises.
- `.agents/skills/forge-workshops/SKILL.md`: authoring and delivery guidance that links the existing contracts.
- `docs/teaching-sequence.md`: how to order worked examples, code changes, comparisons, and Forge investigations in the notebooks and decks.
- `src/forge_workshop_kit/cli.py`: checkout commands for scaffolding, checking, rehearsal, building, and explicit publication.
- `scripts/build_notebooks.py`: generates the participant, starter and read-only facilitator notebooks.
- `notebooks/solar_autoresearch.py`: editable forecast, instrumentation, search and research controller.
- `notebooks/pending_inc.py`: editable office tool, dispatch, observation, tracing, scorer, judge and improvement exercises.
- `src/forge_workshop_kit/ui.py`: shared navigation, result, branch and Forge evidence views. It never executes an experiment.
- `src/forge_workshop_kit/solar_teaching.py` and `pending/teaching.py`: free development checks, saved draft state, phase prerequisites and optional worked answers.
- `examples/solar/candidate.py`: model, loss and training code the agent can edit.
- `src/forge_workshop_kit/solar.py`: fixed partitions and independent scoring.
- `src/forge_workshop_kit/research.py`: bounded proposal and composition requests, receipts and freeze validation.
- `src/forge_workshop_kit/factory.py`: task claims, isolated worker copies, bounded actions, integration and memory records.
- `src/forge_workshop_kit/transit.py`: historical MBTA data, development checks, independent acceptance cases and app export.
- `src/forge_workshop_kit/transit_workshop.py` and `factory_teaching.py`: exercise prerequisites, learner checks and linked task/timeline/release views.
- `src/forge_workshop_kit/session.py`: stage identity, local saving, resumability and publication retries.
- `src/forge_workshop_kit/traces.py`: public Forge SDK scopes and stored-span verification.
- `src/forge_workshop_kit/publication.py`: W&B runs, artifacts, monitoring, Weave, native EvalTables and Reports.
- `src/forge_workshop_kit/provider.py`: direct inference, request reservations and accounting.
- `src/forge_workshop_kit/review.py`: versioned human review decisions and judge agreement, including unavailable judgments.
- `src/forge_workshop_kit/media.py`: checked image descriptors and typed publication.
- `src/forge_workshop_kit/routing_release.py`: release bundles, controlled label-mapping incident, regression comparison, and rollback for Routing.
- `src/forge_workshop_kit/airline.py` and `airline_teaching.py`: fictional booking tools, scripted passenger confirmations, independent state checks, learner functions, and free checks.
- `src/forge_workshop_kit/airline_calibration.py` and `airline_regression.py`: labeled tool-only incidents and local adapter comparisons using saved reviewed cases. These do not manufacture live model failures.
- `src/forge_workshop_kit/agent_lens.py`: native tag configuration, manual Alignment examples, explicit test requests, and monitoring readback with unavailable results preserved.
- `scripts/prepare_airline_data.py` and `src/forge_workshop_kit/assets/airline/`: pinned acquisition, compact fictional records, source checksums, family-separated partitions, policy, and license.
- `src/forge_workshop_kit/releases.py` and `managed_jobs.py`: exact artifact selection, rollback records, and restart-safe managed training IDs.
- `examples/advanced/`: optional SFT, Registry and remote execution examples, with separate access and cost requirements.
- `src/forge_workshop_kit/pending/`: fictional office tools, MCP server, harness and independent state checks.
- `decks/solar/`: editable Slidev deck, progressive diagrams, interactive inspectors and presenter notes.
- `decks/pending/`, `decks/routing/`, `decks/inspection/`, `decks/transit/`, and `decks/airline_monitoring/`: the corresponding decks and presenter notes.

The notebooks expose the code needed for each exercise. These files provide the complete implementation when you want to follow a call further.
