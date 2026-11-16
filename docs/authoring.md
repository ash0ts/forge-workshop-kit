# Author a workshop

Use [CONTRIBUTING.md](../CONTRIBUTING.md) to set up a checkout and find the source files. This guide covers the lesson structure, manifest references, and rehearsal tools. Participants need none of the authoring commands or repository-local skills.

## Define the lesson

Write down the audience, duration, learning outcome, dataset and license, change participants will test, comparison, metric, and budget. Choose a concrete input that can be followed through the code and output. Read the existing workshop before extending it so the new material uses the same terms and saved records.

Follow the [teaching sequence](teaching-sequence.md): inspect an example, explain its intermediate values, change code, run a free check, execute explicitly, and investigate the result. The notebook and deck should name the same function, button, output, and Forge field. Put longer explanations and worked answers where learners can open them without interrupting the main exercise.

## Scaffold a workshop

```sh
uv run forge-workshop new my_workshop --title "My workshop"
uv run forge-workshop check my_workshop
```

The scaffold creates an authored cell module, storyboard, runbook, and manifest entry with `release_status: draft`. It refuses to overwrite existing destinations. Replace its example and placeholder completion check before adding it to the public catalog. Add the dependencies and tests the lesson actually needs; do not install every workshop's stack by default.

The CLI needs a source checkout. The participant wheel does not include the deck toolchain or the complete authoring environment. To work from another directory, use the global `--root PATH` option before the command.

## Bind exercises to their code

[workshops.json](../src/forge_workshop_kit/workshops.json) owns notebook and deck entry points, dependency extras, workflow compatibility, and exercise references. Each exercise identifies:

- A stable exercise ID and notebook step.
- The action cell, editable function, free-check control, and run control.
- Prerequisites, expected output, and one specific Forge investigation.

Keep prose and learner code in authored cells; metadata is not a second implementation. `forge-workshop check SLUG --write-reference` validates the bindings and writes the exercise reference under `dist/references/`. `--source-only` skips the registered free-check tests.

Action-cell IDs normally derive from their control symbols. Before renaming a control, give its cell an explicit stable ID so saved rehearsal references do not move. A copy edit should not change stage identity, configuration, input references, or workflow compatibility. The [technical specification](../techspec.md) explains those execution contracts.

When splitting a batch into smaller teaching steps, keep each execution's existing inputs and identity. Mark the aggregate checkpoint complete only when all required matching results exist. Test a partial workspace as well as a completed one; a cached result must not conceal an unfinished search trial or missing comparison case.

ARIA stop placement, evidence allowlists, recorded investigations, and citation notes have their own [contract](aria-investigations.md). Use that contract when adding or revising an investigation; do not copy its access and billing instructions into each runbook.

## Rehearse the authored notebook

List the current action IDs without running them:

```sh
uv run --extra routing forge-workshop rehearse request_routing --list-actions
```

Replay reads an existing workspace journal and reports its saved stages. It does not create results, prepare data, train, call a model, or retry publication:

```sh
uv run --extra routing forge-workshop rehearse request_routing --mode replay --state .workshop/my-routing
```

For a live rehearsal, choose a separate state directory, project, and allowance:

```sh
uv run --extra routing forge-workshop rehearse request_routing --mode live \
  --project YOUR_ENTITY/YOUR_PROJECT --state .workshop/routing-rehearsal --budget-usd 8
```

Live mode executes the current authored action cells. It is interactive: `list` shows controls, `inputs` lists editable values, `show NAME` displays one, `step STEP` navigates, `set NAME JSON_VALUE` changes an input, and `run EXACT_CELL_ID` executes an action. Use `status` to inspect coverage and `quit` to save the receipt. It does not fill in answers, accept diffs, or select releases for the operator.

Historical domain scripts can qualify a recipe, but they do not establish that the current notebook works. Record coverage separately:

| Coverage | What was checked |
| --- | --- |
| Free checks | Learner functions accept the intended values and reject the demonstrated mistakes |
| Domain execution | A model, tool, or comparison ran on the stated inputs |
| Authored cells | Current notebook actions, learner hooks, identities, and review controls ran |
| Browser | Rendered controls, prerequisites, navigation, and results worked |
| External account | An attendee account could launch the current notebook and use the required products; hosted import/copy is qualified separately |
| Human rehearsal | A participant completed and explained the exercise without the facilitator operating it |

Worked answers are useful for a technical check, but cannot establish participant usability. Record absent adapters or incomplete checks as limitations. Keep the current findings in [release checks](release-checks.md), with proposed follow-up work in [next-up.md](../next-up.md).

## Use product documentation at the boundary

Use [setup](setup.md) for participant access and recovery, [evaluation publication](evaluations.md) for comparison backends, and [maintenance](maintenance.md) for builds and destination-checked publication. The optional [official W&B skills](https://github.com/wandb/skills) can help with product-specific work; check their dependencies against the kit's lockfile before using their helpers.
