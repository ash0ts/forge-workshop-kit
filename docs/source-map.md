# Source map

- `scripts/solar_cells.py` and `scripts/pending_cells.py`: authored exercise cells; the notebook generator is the source of truth for hosted and laptop templates.
- `scripts/routing_cells.py` and `scripts/inspection_cells.py`: authored review, classification, judge-calibration and visual-inspection exercises.
- `scripts/build_notebooks.py`: generates the participant, starter and read-only facilitator notebooks.
- `notebooks/solar_autoresearch.py`: editable forecast, instrumentation, search and research controller.
- `notebooks/pending_inc.py`: editable office tool, dispatch, observation, tracing, scorer, judge and improvement exercises.
- `src/forge_workshop_kit/ui.py`: shared navigation, result, branch and Forge evidence views. It never executes an experiment.
- `src/forge_workshop_kit/solar_teaching.py` and `pending/teaching.py`: free development checks, saved draft state, phase prerequisites and optional worked answers.
- `examples/solar/candidate.py`: model, loss and training code the agent can edit.
- `src/forge_workshop_kit/solar.py`: fixed partitions and independent scoring.
- `src/forge_workshop_kit/research.py`: bounded proposal and composition requests, receipts and freeze validation.
- `src/forge_workshop_kit/session.py`: stage identity, local saving, resumability and publication retries.
- `src/forge_workshop_kit/traces.py`: public Forge SDK scopes and stored-span verification.
- `src/forge_workshop_kit/publication.py`: W&B runs, artifacts, monitoring, Weave, native EvalTables and Reports.
- `src/forge_workshop_kit/provider.py`: direct inference, request reservations and accounting.
- `src/forge_workshop_kit/review.py`: versioned human review decisions and judge agreement, including unavailable judgments.
- `src/forge_workshop_kit/media.py`: checked image descriptors and typed publication.
- `src/forge_workshop_kit/releases.py` and `managed_jobs.py`: exact artifact selection, rollback records, and restart-safe managed training IDs.
- `examples/advanced/`: optional SFT, Registry and remote execution examples, with separate access and cost requirements.
- `src/forge_workshop_kit/pending/`: fictional office tools, MCP server, harness and independent state checks.
- `decks/solar/`: editable Slidev deck, progressive diagrams, interactive inspectors and presenter notes.
- `decks/pending/`, `decks/routing/`, and `decks/inspection/`: the corresponding decks and presenter notes.

The notebooks expose the code needed for each exercise. These files provide the complete implementation when you want to follow a call further.
