# Release checks · 0.11.0 technical preview

This release gives the six workshops a shared set of technical diagrams and posters. The portable `teenage-engineering-visualizations` skill supplies the fonts, tokens, compositions, rendering, and checks. The same authored figures appear in notebook controls, deck reveals, and standalone guides.

There are 42 workshop figures, six digital posters, six A2 print posters, and six generic composition examples. Actual, recorded, illustrative, planned, and unavailable information remain distinct. Branch drawings separate the parent, Candidate A, Candidate B, and the selection decision. No result is assigned to an unexecuted proposal.

## What was checked

| Coverage | Evidence and limits |
| --- | --- |
| Portable skill | Three independent examples use only the global installation: a deployment process, a software architecture, and a library return workflow. No Forge or Workshop Kit imports are required. |
| Rendering | All requested SVG, HTML, PNG, and PDF formats are built from local assets. Browser checks measure actual text lines; embedded hero and capture labels receive a separate inspection. A2 exports retain vector text and embedded Plex fonts. |
| Notebook controls | Next, Back, keyboard activation, and guide switching are checked. Returning to a guide preserves its selected reveal within the open notebook. Light and dark narrow layouts retain a readable text explanation. These controls do not call the session, provider, training, or publication code. |
| Deck integration | Six authored storyboards reuse the figures beside code and source references. Browser validation checks slides, reveal states, routes, links, and text bounds; PDF validation checks the exported pages. |
| Packages and templates | Notebook previews build without credentials. Template publication verifies the existing destination and reads back the uploaded source and preview. Previous releases and attendee copies remain unchanged. |

The release's validation receipt contains exact counts, source hashes, and completed build/publication checks. The [visual guide](../technical-visuals.md) explains authoring and installation. The [previous release checks](release-checks-v0100.md) retain ARIA qualification evidence.

## Limits that remain

The rendering checks do not establish that a new participant can complete a class. **All six workshops remain technical previews.** External-account copying and human rehearsals remain the next priorities in [next-up.md](../../next-up.md).

The standalone overview composition can use an original SVG for a system that needs branches or return paths. That drawing stays visible while adjacent explanations change. It does not automatically animate individual SVG components. On narrow screens, the accompanying text provides the readable alternative to a scaled diagram. Without JavaScript, the complete text and final diagram remain available.

Native EvalTables uses the previously verified Weave-backed path. The separate CES HTTP 500, Airline AI Alignment failures, and missing Insights clusters are not reclassified by this visual revision. ARIA recordings retain their existing access and evidence limits. No new model calls or training were required, and no new experiment outcomes are claimed.

## Materials

The [v0.11.0 release](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.11.0) contains the package, templates, decks, PDFs, portable skill, visual sources, posters, and validation receipts. The [workshop library](https://ash0ts.github.io/forge-workshop-kit/) links the current notebook, Report, deck, and poster for each workshop. QR codes point to its stable workshop sections.
