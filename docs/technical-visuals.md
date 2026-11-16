# Technical visual guides

The six workshops share a visual language defined by the portable [teenage-engineering-visualizations skill](../skills/teenage-engineering-visualizations/SKILL.md). It owns the templates, type, palette, line drawings, rendering, and checks. Other visual skills are not dependencies.

The figures follow one concrete object through code and its effect: an invoice, forecast, support request, board, build, or itinerary. Numbered callouts connect the diagram to the responsible source lines and Forge records. Recorded examples remain separate from participant results.

## Use the skill in another project

From this checkout, install the standalone package:

```sh
python scripts/install_visual_skill.py --default
```

This copies it to the global Codex skills directory and adds a scoped default to global `AGENTS.md`. Existing instructions are preserved. An existing installation is backed up outside the discovery directory. A fresh session can invoke `$teenage-engineering-visualizations`; the default applies to technical explanations unless a different style is requested.

The installed skill does not import Workshop Kit. Its examples, fonts, original SVG components, and rendering commands travel with it. SVG and HTML diagrams require only Python. Poster QR codes and PNG/PDF exports use pinned Node dependencies; install them with `npm ci` inside the installed skill directory. The skill's specification gives the complete export setup.

## Author a workshop figure

Edit the specifications and original drawings in [visual-guides](../visual-guides/). Its index maps figures to notebook steps and deck concepts. The portable skill holds generic templates; domain-specific examples and Forge URLs stay in the workshop repository.

```sh
python scripts/build_visual_guides.py
python scripts/build_visual_guides.py --exports
```

The first command generates packaged notebook frames and deck assets. The second also renders digital and print posters, the reference gallery, and downloadable sources. It does not execute a workshop or publish anything.

Notebook views read bundled frames and use native display controls. The slide adapter reveals those same diagrams beside their source excerpts. Display state is independent of experiment records, so changing a frame or reopening a guide cannot execute or invalidate an experiment.

Posters have two layouts: a digital overview and an A2 print version. The library links the Report, notebook, deck, and poster for each workshop. QR destinations use stable library anchors rather than expiring execution URLs.

## Check and release

Inspect the renderer's validation receipts and rendered output. Check actual text lines, units, code, callout targets, comparisons, and source references. Test keyboard Next/Back, the static alternative, narrow notebook layouts, links, and poster QR destinations.

Build notebooks and decks through the existing [release commands](maintenance.md). Technical previews retain that status; a new visual treatment does not qualify missing native access or replace a participant rehearsal.
