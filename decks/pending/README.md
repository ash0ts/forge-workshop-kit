# Pending, Inc.

A four-hour Python workshop about an agent that handles duplicate charges and account access at a fictional company. Participants implement a tool and its observation handoff, trace the execution in Agent Lens, and score account state separately from the final reply. They then test manual and agent-written harness changes on the same cases.

The deck follows the current notebook’s eight steps. Each code exercise explains the inputs, the change to make, and the output to inspect. Presenter notes work through the control flow and the reasons for resetting cases, testing composition decisions, and holding back final cases.

Open the [current notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) and copy it into your own project. Use the [setup guide](../../README.md) and [four-hour runbook](../../docs/pending-facilitator.md). The [presenter notes](notes/facilitator-notes.md) explain each slide.

## Build

From the Workshop Kit root:

```sh
python3 scripts/build_decks.py --only pending --install --pdf --validate
```

This generates a browser deck, PDF, and source package. Build and preview make no workshop model calls. For local editing, run `npm run dev` inside this directory after installing its locked dependencies.

The authored source is `scripts/build-storyboard.py`. Regenerate rather than editing `slides.md` or presenter notes by hand. The diagrams are editable Vue/SVG components. Each meaningful build is a separate slide so the PDF keeps the same teaching sequence. The [visual guide](notes/visual-upgrade.md) maps the explanations to their code, fixtures, and recorded results.

## Evidence

The office and dialogue are fictional. Recorded examples use `evidence/v030-pending-rehearsal.json`, saved harness decisions, and actual Agent Lens spans. All 12 final executions and explanation judgments were available and passed; this rehearsal demonstrates the process without a quality gain.

The native comparison slides show Weave-backed Evaluation Tables Preview using saved rehearsal records. The separate CES v2 API still returns HTTP 500; publication details preserve that failure. Product links can require a Forge login.

The previous 88-slide November 12 deck remains unchanged in its historical release. Its gateway and remote Sandbox instructions are not part of this deck.
