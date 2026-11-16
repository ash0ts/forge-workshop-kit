# Workshop visual guides

These are the authored illustrations for the six current workshops. Each workshop contains a system overview, six explanations, and a poster. They use the portable `teenage-engineering-visualizations` skill; no other visual skill supplies their design.

Start with [index.json](index.json). It maps each explanation to the current notebook step, actual exercise and cell identities, code function, control, and deck concept. Editing an illustration does not change an experiment or its saved results.

## Edit an explanation

Edit its JSON specification. A step identifies the object being explained, its input, operation, output, and optional code excerpt or media. Reveal states refer to stable step IDs. Keep an intermediate value consistent across all states and all output formats. Code excerpts are shortened for the figure; full editable functions remain in the notebook and are linked from the source list.

Every specification labels its provenance. An illustrative mechanism can describe implemented behavior without claiming that a learner has executed it. Recorded comparisons belong to instructor executions, and final examples must not enter development prompts. No display interaction starts inference, training, or publication.

The original `hero.svg` drawings establish the situation: a desk and checked account, a solar observation and experiment, a routed message, a PCB inspection station, an integrated departure board, or a preserved return itinerary. Their curves and probability bars are schematic, not measurements. Recorded scientific and inspection panels retain their own labels and scales.

Six explanations include a `native_capture`. Its numbered outlines identify fields in an actual Forge screenshot, with the same numbers attached to the relevant code or operation. The original PNG and native source URL remain available. These captures predate this revision; their capture timestamps were not recorded, so the metadata leaves that date unavailable rather than inventing one.

## Reuse and sources

Source links in each JSON file point to the implementation and the public worked example. [media/sources.json](media/sources.json) records copied asset paths, source URLs, and SHA-256 checksums. PCB photographs come from VisA under CC BY 4.0; preserve that attribution with exported figures. The Solar panels are existing Workshop Kit diagrams grounded in the documented GOES and AIA observations.

Poster destinations use the stable workshop anchors in the public library. Each anchor leads to the current Report, notebook, and deck; a QR code must not point directly to a private execution.

Generated images, HTML, and PDFs are built from these specifications. Fix the specification or shared renderer, then rebuild; do not repair a generated image alone.
