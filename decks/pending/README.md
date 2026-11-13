# Pending, Inc.

A three-hour companion deck for the current gateway-free Pending notebook. It uses the original office scenes and visual language, with instructions for the Workshop Kit's eight steps.

Open the [current notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) and copy it into your own project. Use the [setup guide](../../README.md) and [presenter notes](notes/facilitator-notes.md).

## Build

From the Workshop Kit root:

```sh
python3 scripts/build_decks.py --only pending --install --pdf --validate
```

This generates a browser deck, PDF, and source package. Build and preview make no workshop model calls. For local editing, run `npm run dev` inside this directory after installing its locked dependencies.

The authored source is `scripts/build-storyboard.py`. Regenerate rather than editing `slides.md` or presenter notes by hand. The diagrams are editable Vue/SVG components. Each meaningful build is a separate slide so the PDF keeps the same teaching sequence.

## Evidence

The office and dialogue are fictional. Recorded examples use `evidence/v030-pending-rehearsal.json`, saved harness decisions, and actual Agent Lens spans. All 12 final executions and explanation judgments were available and passed; this rehearsal demonstrates the process without a quality gain.

Native EvalTables publication returned HTTP 500. The deck uses actual saved W&B/Weave/Report records and labels them accurately. Product links can require a Forge login.

The previous 88-slide November 12 deck remains unchanged in its historical release. Its gateway and remote Sandbox instructions are not part of this deck.
