# Author and rehearse a workshop

Use this checkout to maintain the notebook, companion deck, and facilitator guide together. Participants only need their copied notebook. They do not need the authoring commands or an agent skill.

The repository-local [forge-workshops skill](../.agents/skills/forge-workshops/SKILL.md) guides a coding agent through this work. It links to the kit's existing contracts rather than maintaining another runtime or copies of SDK instructions.

## Start with an exercise

Write down the audience, duration, learning outcome, dataset and license, change participants will test, comparison, metric, and budget. Choose a concrete input that can be followed through the code and output. Each exercise should name the function to edit, the free check, the execution button, the expected output, and a specific field or result to inspect in Forge.

The workshop manifest owns titles, workflow identities, dependency extras, entry points, and exercise references. Authored cells own learner code and explanations. Storyboards own diagrams, presenter notes, and slide sequence. See the [source map](source-map.md) for their locations.

```sh
uv sync --frozen --all-extras
uv run --all-extras forge-workshop --help
uv run --all-extras forge-workshop new my_workshop --title "My workshop"
uv run --all-extras forge-workshop check my_workshop
uv run --all-extras forge-workshop build my_workshop --install
uv run --all-extras forge-workshop open my_workshop
```

The scaffold is a starting point, not a qualified workshop. Complete its lesson and validation before adding it to the participant catalog. Existing workshop files are never overwritten by scaffolding.

## Use the same code in checks and rehearsals

Stable action-cell IDs connect the manifest to the authored notebook. Rehearsals use those cells, their current configuration, learner hooks, and review gates. They must not substitute an old domain script and call that a notebook rehearsal.

Keep these kinds of coverage separate:

| Check | What it establishes |
| --- | --- |
| Free checks | The small exercises accept the intended values and reject the demonstrated mistakes |
| Domain execution | The model, tool, or comparison implementation runs under its tested inputs |
| Authored-cell execution | The current notebook action, hooks, stage identities, and publication path ran |
| Browser interactions | Controls, prerequisites, navigation, and results worked in the rendered notebook |
| External-account access | A separate attendee account could copy and use the required products |
| Human rehearsal | A participant could follow the exercises without the facilitator operating the notebook |

A replay reads saved records. It does not train, send inference, prepare data, or retry publication. A live rehearsal uses a separate state directory, the current manifest identity, and an explicit project and allowance. Missing adapters or incomplete coverage must remain visible. Worked answers may be supplied for a technical check, but that does not establish participant usability.

```sh
uv run --all-extras forge-workshop rehearse request_routing --list-actions
uv run --all-extras forge-workshop rehearse request_routing --mode replay --state .workshop/my-routing
uv run --all-extras forge-workshop rehearse request_routing --mode live \
  --project YOUR_ENTITY/YOUR_PROJECT --state .workshop/routing-rehearsal --budget-usd 8
```

Live mode is an interactive runner. Use `list` to see the current controls, `inputs` to list editable values, `show NAME` to read one, `step` to navigate, `set NAME JSON` to supply an input, and `run` with an exact action-cell ID. It does not choose candidates, accept diffs, or release a version for you. Use `status` to inspect coverage and `quit` to save the receipt. Browser and human checks still need their own rehearsals.

## Check setup without starting an experiment

`forge-workshop doctor` checks the local environment by default. Add `--services --project ENTITY/PROJECT` to request service access checks. Neither path sends a model request. Project access alone does not establish inference billing, trace readback, or evaluation publication.

Use [setup and recovery](setup.md) for participant-facing instructions. Keep the facilitator [monitor](../notebooks/facilitator.py) read-only. It shows published progress and explicit help requests; an absent update remains unknown.

## Build and publish separately

`forge-workshop build` generates notebooks, packages, and the mapped deck. PDF and browser validation are explicit options. `forge-workshop publish` requires a destination project and verifies the release before updating templates. Follow [maintenance](maintenance.md) for release assets, publication readback, and prior-version preservation.

The CLI runs from a source checkout. Installing the participant wheel alone does not install storyboards, maintainer tools, or unpublished data. This keeps participant installation smaller and avoids implying that a wheel contains the full authoring environment.

For product-specific help, the [official W&B skills](https://github.com/wandb/skills) cover tracing, evaluations, and experiment work. Their helper dependencies can differ from this kit's pins. Review that compatibility before using them; attendees do not need them installed.
