# Teenage Engineering visualizations

A standalone Codex skill for explaining technical systems through numbered operations, stable drawings, and visible results. It uses original artwork inspired by Teenage Engineering's product guides. It is not affiliated with Teenage Engineering.

## Install and use

Copy this entire folder to `~/.codex/skills/teenage-engineering-visualizations/`. Start a new Codex session and ask:

```text
$teenage-engineering-visualizations Explain this system.
$teenage-engineering-visualizations Diagram this deployment process.
$teenage-engineering-visualizations Make a workshop poster.
```

To make it your technical-visual default, add a narrowly scoped instruction to your global `~/.codex/AGENTS.md`: use this skill for technical diagrams, process explanations, and posters unless you explicitly request another style. Keep unrelated instructions and skills in place.

The skill needs no Workshop Kit checkout, Forge account, or external font server. [SKILL.md](SKILL.md) describes its working method. [The specification](references/specification.md) describes the input format and exports.

## Render an example

Python 3.11 or later:

```sh
python scripts/render.py examples/sequence.json --output /tmp/guide --layout slide --formats svg,html
python scripts/validate.py /tmp/guide
```

For PNG, PDF, or QR codes, install the pinned local export dependencies with Node.js 22 or later:

```sh
npm ci
npx playwright install chromium
python scripts/render.py examples/poster.json --output /tmp/poster --layout print --formats svg,html,png,pdf
python scripts/validate.py /tmp/poster --browser
```

The six examples cover a system overview, operation sequence, transformation, controlled comparison, branches and decisions, and a poster. Example values are illustrative. Put your own specifications and outputs in your project, leaving this installed package unchanged.

Original source and drawings use the included MIT license. IBM Plex font files retain their licenses in `assets/fonts/`.
