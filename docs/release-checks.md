# Release checks · 0.12.0 technical preview

This revision adds an explicit ARIA request in the notebook, improves Report figures and code explanations, and repairs browser and offline delivery. It preserves workshop execution identities, datasets, budgets, and saved results. Publication is pending while the coordinated build finishes.

## Current validation

- **Direct ARIA:** one saved Routing validation result was sent with native run and Agent Lens conversation attachments. The returned conversation completed, its answer was restored locally, and the native follow-up composer opened in the same thread. The [qualification record](aria-direct-qualification.md) links the actual conversation and a safe receipt. No workshop training or model execution was repeated.
- **Request recovery:** 67 targeted ARIA client, context, and notebook tests passed. They cover duplicate clicks, restored responses, repaired authentication, stale evidence, ambiguous requests, response polling, and separate result controls. An uncertain send cannot trigger an automatic second request. Credentials are sent only to the fixed ARIA service using the cloud login.
- **Package:** the wheel, source distribution, eight notebook sources and HTML previews, twelve recorded investigations, and visual bundles build locally. The final package hashes are refreshed after the remaining documentation and rendering checks; a local build is not a public-release check.
- **Changed slides:** 59 focused frames across all six decks passed their text-bound, console, and asset checks. Full Pending validation covers 102 slides and 151 reveal states, with a 151-page PDF. Full Solar validation covers 131 slides and 244 reveal states, with a 244-page PDF. Both have no reported text-bound, console, or asset failures. Canonical receipts: [Pending browser](../decks/pending/notes/delivery-checks.json), [Pending PDF](../decks/pending/notes/pdf-checks.json), [Solar browser](../decks/solar/notes/delivery-checks.json), and [Solar PDF](../decks/solar/notes/pdf-checks.json).
- **Remaining delivery:** full Routing, Inspection, Transit, and Airline rendering is still running. Public template readback, final downloadable asset hashes, and deployment checks must be recorded after publication.

All six workshops remain technical previews. This ARIA check used the maintainer's enabled team account and one development investigation. External-account access, all twelve live ARIA stops, and participant rehearsal remain unverified. ARIA organization usage was not returned by this request and remains outside the notebook's inference allowance. Native Alignment, Insights, and other existing limitations remain listed in [next-up.md](../next-up.md).

## Previous release · 0.11.1

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

## Deck update · November 16, 2026

All six decks now return to their workshop setting at five points in the lesson. The 30 original SVG illustrations show the work being discussed: an employee and editor in Pending, observations and source code in Solar, requests and labels in Routing, boards and reviewed cases in Inspection, builders and their shared application in Transit, and itineraries and monitoring in Airline. They introduce the existing explanations; no exercises or slides were removed.

The diagram review also corrected Inspection's 14-by-14 patch grid and Routing's matrix layout, marked the enlarged portion of Transit's service-day axis, and distinguished source files, training executions, reviewed diffs, and selected versions in Solar. Larger labels and revised spacing keep those diagrams readable beside their code. Pending's comparison shows all three harnesses. Inspection's recovered and new misses appear beside the matching retest.

Validation covers the full browser decks, Next/Back, original reveal ordering, worked-answer links, image loading, text bounds, and every exported PDF page. The 30 scene SVGs also passed standalone rendering, font-bound checks, and deterministic regeneration outside the checkout. Storyboard and packaging checks passed 39 tests. The download includes the per-deck receipts and the separate scene/component reviews.

The current browser decks and downloads are in the workshop library. The separately named [illustrated deck update](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.11.1/workshop-decks-2026-11-16-illustrated.zip) preserves the original v0.11.1 assets. This update changes presentation only; the readiness limits above still apply.

## Initial meeting packet · November 16, 2026

The first meeting packet collected a two-page brief, Slack copy, short demo routes, six deck PDFs, setup instructions, facilitator notes, and links to the public Reports and editable notebooks. The library also exposed PDF, offline-deck, and source downloads directly. Local setup instructions distinguished the dependency extra from the notebook path. The documentation update below supersedes this initial packet; its validation record remains here for comparison.

All 30 primary deck, PDF, source, Report, and notebook URLs returned HTTP 200; the notebook URLs lead anonymous visitors to Forge sign-in. All six public Reports matched their authored content on anonymous readback. This is a link check, not a fresh-account execution rehearsal.

Packet checks resolved 110 local link targets and 20 anchors across 15 HTML pages. The archive's 49 payloads matched its manifest, and the six deck PDFs matched the already-validated site PDFs byte-for-byte. A temporary rebuild excluded unrelated and stale files. The two-page brief has ten public PDF links and no text outside the page bounds. Desktop and 390-pixel layouts, the Slack-section link, and offline document links were inspected. Related publication, visual, and packaging checks passed 34 tests.

Use this material for recorded demonstrations and pilot invitations. The full-class readiness limits above remain unchanged. No workshop execution, credentials, participant state, or existing release asset was changed.

## Documentation and Report update · November 16, 2026

The README, contributor guidance, facilitator instructions, sharing copy, and six public learning Reports now explain the customer problem, the work participants do, and the relevant Forge records consistently. All six Reports were updated at their existing URLs. Anonymous readback matched the authored blocks, and each Report's updated copy, notebook link, and representative figure were inspected in Forge.

The current [participant materials](https://ash0ts.github.io/forge-workshop-kit/packet/) include an overview, notebook downloads, and setup and facilitator guides. The [recording script](loom-walkthrough.md) remains a contributor document in Git. Separate registered community Slack and video links identify external referral sources; coworker reviews use the untracked library address. Workshop links still identify the workshop across its deck, poster, and other placements. Clicks do not establish attendance or notebook completion; the facilitator's progress records remain separate.

Validation for source revision `55fb582` covered:

- Six Report sources and 150 source-ledger hashes, with no mismatches; all 53 Report images and six linked visual guides were reachable.
- Eight registered redirects matched their declared destinations, and all eight QR images decoded to the correct short URLs. The six workshop QR codes retained their existing destinations.
- 571 relative file and anchor references across 57 active Markdown documents, plus 292 local packet links and anchors, with no broken references.
- All 73 packet payloads matched the archive manifest. The release downloads matched the uploaded files byte-for-byte. All three brief pages were rendered and visually inspected.
- Sixteen focused Report and sharing tests passed. All nine Linux, macOS, and Windows jobs passed in the [cross-platform check](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43824643701).
- The [full deck render, validation, and Pages deployment](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43824643700) passed. Public readback verified the library, packet, Loom script, sharing page, tracking guide, and all 73 files in the deployed packet. The packet-to-script-to-sharing navigation was also exercised in the browser.

The [revised packet ZIP](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.11.1/workshop-meeting-packet-2026-11-16-workflow-guide.zip), [brief PDF](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.11.1/workshop-meeting-brief-2026-11-16-workflow-guide.pdf), and [validation receipt](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.11.1/workshop-docs-reports-validation-2026-11-16.json) are separately named release assets. Earlier downloads, attendee copies, experiment records, and budgets are unchanged. No new inference or training was required. The external-account, native-feature, and human-rehearsal limits in [next-up.md](../next-up.md) still apply.
