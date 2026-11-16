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

Edit the specifications and original drawings in [visual-guides](../visual-guides/). Its index maps figures to notebook steps and deck concepts. The `scripts/illustrate_*.py` files author the workshop drawings; each specification points to a complete SVG for each reveal. These show the object, the part being changed, and the consequence. A row of labeled cards is not the target for a finished teaching figure.

The portable skill supplies tokens, fonts, geometry helpers, rendering, and a local release example. Workshop objects, recorded values, and Forge URLs stay in this repository. Illustration generators read versioned snapshots and do not train, run inference, or fetch live results.

```sh
python scripts/build_visual_guides.py
python scripts/build_visual_guides.py --exports
```

The first command generates packaged notebook frames and deck assets. The second also renders digital and print posters, the reference gallery, and downloadable sources. It does not execute a workshop or publish anything.

Notebook views read bundled frames and use native display controls. The slide adapter reveals the same drawings and code excerpts. On a narrow notebook screen, the drawing remains available in a scrollable region with a text explanation below. Display state is independent of experiment records, so changing a frame or reopening a guide cannot execute or invalidate an experiment.

Posters have two layouts: a digital overview and an A2 print version. The library links the Report, notebook, deck, and poster for each workshop. QR codes use the [managed sharing links](share-links.md), which open the corresponding workshop card in the public packet.

## Recurring workshop settings

Each deck also uses an original setting illustration at five transitions: the opening, inspection, implementation, comparison, and conclusion. The office, research lab, support desk, PCB station, transit team, and airline operations desk use recognizable objects from their exercises. The illustrated setting introduces the task; the following reveal retains the full authored explanation, code, or recorded result.

Edit [illustrate_workshop_scenes.py](../scripts/illustrate_workshop_scenes.py) for the drawings and [scene_storyboard.py](../scripts/scene_storyboard.py) for their placement. The generator writes thirty editable SVGs and an object/callout index under [visual-guides/scenes](../visual-guides/scenes/). Fonts are embedded. Each scene has a text alternative and identifies its illustrative status. Scenes do not represent participant executions.

The shared slide stylesheet gives the drawing a full frame and preserves its aspect ratio. Existing diagrams keep their own reveals after the scene. The deck validator checks scene loading, frame bounds, minimum displayed size, and forward/back navigation. The generated `notes/scene-coverage.json` records placements for each deck. These assets are included in the deck source archives; rebuilding them requires no service access.

## Check and release

Inspect the renderer's validation receipts and rendered output. Check actual text lines, units, code, callout targets, comparisons, and source references. Cover the paragraphs and check whether the drawing still shows the input, operation, and changed state. Validate one representative illustration before repeating it across the other lessons. Test keyboard Next/Back, the static alternative, narrow notebook layouts, links, and poster QR destinations. Bounds checks establish legibility, not teaching quality.

Build notebooks and decks through the existing [release commands](maintenance.md). Technical previews retain that status; a new visual treatment does not qualify missing native access or replace a participant rehearsal.
