---
name: forge-workshops
description: Create, revise, rehearse, and publish Forge Workshop Kit notebooks and decks. Use when authoring a workshop or preparing its delivery from this repository.
---

# Forge workshops

Work in the standalone Workshop Kit checkout. Read [AGENTS.md](../../../AGENTS.md) for its execution and compatibility boundaries, then [CONTRIBUTING.md](../../../CONTRIBUTING.md) for source locations and local checks. Participants copy notebooks into their own projects; this skill is for contributors, not a participant dependency.

## Choose the relevant guide

Load only the material needed for the requested change:

| Task | Read |
| --- | --- |
| Understand current readiness or choose follow-up work | [next-up.md](../../../next-up.md) |
| Change runtime behavior, saving, accounting, or recovery | [Technical specification](../../../techspec.md) |
| Add a workshop, bind exercises, or rehearse action cells | [Authoring](../../../docs/authoring.md) |
| Change lesson order or explanations | [Teaching sequence](../../../docs/teaching-sequence.md) |
| Revise diagrams, slide reveals, posters, or product captures | [Technical visuals](../../../docs/technical-visuals.md), the standalone [teenage-engineering-visualizations skill](../../../skills/teenage-engineering-visualizations/SKILL.md), and the affected storyboard |
| Change ARIA context, citation notes, or recordings | [ARIA investigations](../../../docs/aria-investigations.md) |
| Change evaluation rows or publication | [Evaluation publication](../../../docs/evaluations.md) |
| Build or publish a release | [Maintenance](../../../docs/maintenance.md) and [release checks](../../../docs/release-checks.md) |
| Write or update public learning Reports | [Report sources](../../../reports/README.md) and [Report publication](../../../docs/maintenance.md#publish-learning-reports) |

## Establish the work

Read the affected notebook source, storyboard, and runbook before editing. For a new lesson, identify the audience, learning outcome, dataset and license, intervention, comparison, metric, duration, and budget. Recover those decisions from existing material or the request before asking for missing choices.

Follow a concrete input through its intermediate values, code, output, participant exercise, and Forge investigation. A participant should change code that affects the next execution. Keep implementation explanations beside the code and put humor in the setting, not in controls or errors.

Edit authored sources and manifest references together, then regenerate their outputs. Use `forge-workshop --help` and the command's own help to verify flags. Do not invent a parallel build system or copy SDK instructions into this skill. Product-specific guidance may come from the [official W&B skills](https://github.com/wandb/skills), after checking compatibility with the kit's pinned dependencies.

## Stance

Reading source, editing local materials, running free checks, and building are ordinary contributor work. Live rehearsals and publication use the task's existing authorization, explicit run controls, project, and allowance. If the request only asks for local changes, return the checked local result without publishing it.

When credentials or a native feature are unavailable, preserve completed work and report the affected check. Use an existing recorded exercise where the workshop supports one. Do not fabricate a recording, introduce shared credentials, or rerun an experiment to replace a failed upload.

## Success criteria

- The lesson identifies a concrete change, output, and record to inspect.
- Notebook, deck, runbook, and manifest refer to the same functions and controls.
- Results and captures match saved code, inputs, and outputs; unsuccessful and missing results remain visible.
- Validation states which source, browser, native-access, and human checks actually ran.
- Requested deliverables are complete, with publication status and remaining limitations stated.

## Not this skill

This skill does not authorize experiment spending, external publication, or messages to others beyond the user's task. It does not replace the product's SDK documentation or the participant's workshop instructions. Use the linked contracts for those details rather than adding another copy here.
