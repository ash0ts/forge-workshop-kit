---
name: teenage-engineering-visualizations
description: Create consistent technical-manual diagrams, process explanations, project overviews, incremental teaching visuals, and posters. Use for technical visuals by default, or when the user requests Teenage Engineering-style guides.
---

# Teenage Engineering visualizations

Explain a concrete system through its parts, operations, and observable results. This skill owns the visual direction, templates, rendering, and checks. Use its bundled assets and compositions. Do not invoke or inherit visual direction from another design, graphics, deck, or animation skill. An explicit request for another style takes precedence.

The name identifies the instructional reference. This is an independent skill with original artwork, not a Teenage Engineering product or endorsement. It works without Forge or a workshop checkout.

## Start with the thing being explained

Read the relevant code, data, or project records. Identify:

- The reader's question and one concrete object to follow.
- What enters the system, what changes it, and the resulting state.
- Which values are observed, recorded, illustrative, planned, or unavailable.
- The requested surface: notebook, slide sequence, web guide, or poster.

Keep the explanation grounded in that object. A deployment diagram follows a build; a classifier explanation follows a request; a forecast explanation follows one timestamp. Name intermediate values and responsibilities before abstracting them.

Inspect one matching bundled example before authoring. Read [the visual rules](references/style.md) when selecting geometry or annotations and [the figure specification](references/specification.md) when writing a source file. [The guide references](references/sources.md) explain the instructional patterns; revisiting the web is unnecessary unless the task requires new research.

## Choose a composition

| Template | Use it to explain |
| --- | --- |
| `overview` | An assembled system, its parts, and their responsibilities. |
| `sequence` | An action, changed state, and subsequent observation. |
| `transformation` | One input passing through intermediate values to an output. |
| `comparison` | Aligned versions with common inputs and explicit differences. |
| `branches` | A parent, proposals, executions, and a separate selection decision. |
| `poster` | A situation, the system participants build, learning outcomes, and a next action. |

Use the templates and token file rather than creating a new visual identity. Keep positions stable across reveals. A detail view enlarges part of the same system. A comparison preserves cases, order, units, and scale.

Use a transformation only when an operation's output feeds the next operation. Supply each input and output explicitly. Alternative methods belong in a comparison or branch drawing; a numbered teaching procedure belongs in a sequence. An arrow must describe an actual relationship, not just the order in which the instructor explains the concepts.

## Author the explanation

1. Put the concrete situation and question above the drawing.
2. Give each part a stable identity and short functional label.
3. Pair an action with its input, relevant code, and visible output.
4. Reveal one meaningful change at a time. Back must reconstruct the preceding state.
5. Use numbered callouts that match the code and supporting capture.
6. Attach sources to the values or claims they support.

Use original line drawings, actual observations, and unchanged screenshot originals. Put annotations in a separate layer. Do not cover the field being explained. A screenshot is evidence of a recorded screen, not a substitute for explaining the mechanism.

Keep prose in ordinary language. Explain an unfamiliar term beside its use. Reserve humor for the situation; keep controls, errors, and technical instructions literal. Include only measured numbers or explicitly labeled illustrative arithmetic.

For a poster, lead with the situation and what someone will build. Use one dominant diagram, three learning outcomes, prerequisites, duration if known, and one main call to action. Reflow for print and digital rather than shrinking a dense page.

## Render

Run commands from this skill directory. All paths may be absolute. Inspect command help for supported options.

```sh
python scripts/render.py examples/sequence.json --output /tmp/te-guide --layout slide --formats svg,html
python scripts/validate.py /tmp/te-guide
```

Use `slide` or `notebook` for explanations, and `digital` or `print` for poster layouts. Request `png,pdf` when sharing raster or print output. SVG and HTML rendering use bundled assets and run without network access. Export prerequisites and pinned versions are described in [the specification](references/specification.md).

Keep the figure specification and editable SVG alongside exports. HTML is a local viewing surface. Next/Back and selectors change the explanation only; they must not launch an experiment, invoke a model, publish data, or send a message.

## Verify the rendered result

Run the validator, then inspect every meaningful frame and requested export. Automated bounds checks do not establish that a diagram teaches its subject.

- Check actual text lines, callout targets, code readability, units, and dimensions.
- Compare visible values with the source. Mark missing results as unavailable.
- Check aligned comparisons, ordering, and unchanged geometry across reveals.
- Try keyboard controls, focus states, narrow layouts, and the static alternative.
- Inspect print and digital layouts at their intended viewing size. Test links and QR destinations.

When a rendering dependency is missing, provide the working SVG/HTML source and report which requested exports remain incomplete. Do not substitute another style, fabricate a successful export, or quietly drop requested formats.

## Deliver

Return the requested visual, editable source, and a brief account of what was verified. Put project-specific files in the user's output location, not in this installed skill. The skill does not authorize publication, spending, or edits to unrelated project settings.

## Success criteria

- The reader can identify an input, the operation applied, and its consequence.
- The drawing uses the bundled visual language consistently.
- Values and states agree with the supplied evidence.
- Requested formats render legibly and preserve the explanation.
- The source remains editable outside the original project.
