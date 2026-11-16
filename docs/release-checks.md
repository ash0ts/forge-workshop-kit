# Release checks · 0.11.1 technical preview

This revision replaces the generic card diagrams with drawings of the objects and operations being taught. The figures show record fields, invoice rows, conversation turns, measured forecast windows, image patches, probability columns, source ownership, and flight segments. Each workshop uses the same drawings in its notebook, deck, and poster.

## What was checked

- All 42 figures were reviewed against source code, public fixtures, or saved results. Illustrative calculations are labeled. Review corrected a threshold-indexing excerpt, patch-distance precision, a compressed time axis, and the distinction between valid judge output and a correct judgment.
- All six digital and A2 posters were rendered. Original SVG artwork remains editable. Screenshot originals, evidence links, and scientific image colors are preserved.
- Shared rendering tests cover local media, frame identities, inline style isolation, font bounds, and passive navigation. Notebook guides retain readable diagrams on narrow screens through horizontal scrolling, with text alternatives.
- A separate library-return example exercises the portable skill outside Workshop Kit. It uses book and patron records, a hold queue, shelf state, and four operation states; it imports no Forge or workshop package.
- Packages and saved notebook previews build without credentials. The presentation changes do not alter authored execution cells, stage identities, experiment settings, or saved results.

The release bundle contains detailed build and validation receipts. These checks establish rendering and implementation behavior, not participant understanding. The [technical-visual guide](technical-visuals.md) describes the source and build contracts. [Previous release checks](archive/release-checks-v0110.md) preserve the earlier evidence.

## Limits that remain

**All six workshops remain technical previews.** External-account access and human rehearsals remain open in [next-up.md](../next-up.md). No new inference or training was run for this revision.

Forge source and preview uploads are checked separately from browser display. The hosted preview was blocked in the verification browser by its public-to-local-network security policy. Local notebook controls and the standalone guides were exercised; that does not establish a successful hosted-preview experience.

Native EvalTables retains its previously verified Weave-backed path. The separate CES HTTP 500, Airline AI Alignment failures, and missing Insights clusters are not reclassified by a visual revision. ARIA investigations retain their recorded access limitations.

## Materials

The [v0.11.1 release](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.11.1) contains the package, templates, decks, PDFs, skill, visual sources, posters, and verification receipts. The [workshop library](https://ash0ts.github.io/forge-workshop-kit/) links the current materials. Previous releases and attendee copies are preserved.
