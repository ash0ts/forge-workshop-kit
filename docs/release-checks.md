# Release checks · 0.5.1 technical preview

Version 0.5.1 repairs native evaluation publication and updates the four decks. It reuses saved experiments. Version 0.5.0 added customer-request routing and circuit-board inspection to the gateway-free Workshop Kit. Pending adds an editable retry repair. Solar adds a qualified GOES recipe and publishes the mixed three-seed image result. Previous releases, rehearsal evidence and attendee copies remain unchanged.

## Worked examples

| Exercise | Qualification | Outcome |
| --- | --- | --- |
| Pending | Same simulated committed-write timeout, two recovery functions | New operation ID creates two memberships. Original ID plus account read leaves one. The separate harness comparison remains a 4/4 tie. |
| Banking77 | Frozen official test; TF–IDF versus frozen MiniLM features | Macro-F1 0.879385 → 0.920229. Three seeds reproduce the deterministic classifier result. |
| VisA PCB1 | Frozen supervised split and bounded validation-selected follow-up | AP 0.872900 → 0.885742. Teaching retest after a failed first recipe; both remain published. |
| GOES | Three predeclared seeds; validation selects residual MLP, 1,200 updates | All three beat persistence. Mean MAE 0.163506 versus 0.192706. Inspected final dates are teaching retests. |
| AIA images | Exact image recipe repeated across three seeds | Two gains and one 0.21% regression; the all-seed gate fails. Do not call it a reliable improvement. |

Read the [routing protocol](routing-workshop.md), [inspection protocol](inspection-workshop.md), and [Solar qualification](solar-qualification.md) before using the results as teaching claims. These are distinct experiments with different metrics, not a combined benchmark.

## Service checks

The November 14 live routing rehearsal made eight routing calls and four judge calls. All twelve returned responses with verified stored spans. Observed inference cost was $0.00113494, with no bounded unknown usage or in-flight reservations. The eight routing examples were a small instrumentation check, not a balanced quality evaluation. Judge agreement with the supplied dataset labels is not agreement with human reviewers. The two saved classifier comparisons published 6,160 rows; every prediction and target was read back from W&B and Weave and matched the qualification files. No classifier was retrained for publication.

The new Pending repair exported actual before/after tool events and passed stored-span readback. The publication check saved typed VisA photographs and masks, W&B results, Weave datasets and completed evaluation calls. The full inspection rehearsal published four versions and 1,768 aligned image rows. Missing masks remain missing media values; a publication retry recovered an upload timeout without rerunning training. A silent Weave export failure found during the check now remains unavailable until server readback succeeds; saved execution is never repeated to repair publication.

The CES endpoint still returned HTTP 500 on November 14. The kit now uses the pinned SDK’s native, Weave-backed EvalTable Preview. Check the current [publication evidence](evaluations.md) for row readback and browser verification; historical releases retain their original outage records.

## Native comparison follow-up · November 14

This publication repair reuses saved predictions and scores. It launches no new training, inference or judging. Verified native comparisons include the [Pending retry repair](../evidence/v051-pending-evaltables.json), [all 12 Pending final results](../evidence/v051-pendingfinal-evaltables.json), [6,160 routing predictions](../evidence/v051-routing-evaltables.json), and [1,768 inspection predictions](../evidence/v051-inspection-display-evaltables.json). Each receipt links to its named Forge comparison view; these views leave the project's default workspace unchanged. Solar also publishes 597 image predictions and 5,388 measurement predictions in separate native comparisons; see the [saved publication receipts](../evidence/v051-solar-evaltables.json).

Inspection now displays reference defect masks with white defect pixels. The source masks use labels 0 and 1, which appeared almost black as ordinary grayscale images. Separate previews use 0 and 255; their defect locations, original source files, predictions and scores are unchanged.

Readback checks the completed evaluation, every case identity, non-image input and output, individual scores, and the run's logged EvalTable marker. Media stays typed. Browser checks inspect representative photographs, masks and forecasts; they are not a byte-for-byte download check of every published image. The readback path now uses call JSON directly because the higher-level Weave call reader materializes image objects. The corrected path verified all 199 saved manual Solar forecasts in 0.60 seconds without downloading their image files.

All 237 automated tests pass after the readback repair. They cover saved-marker recovery, ambiguous uploads, missing scores, changed requests, exact row readback and comparison-column visibility. Publication retries reuse saved evaluations. A run-finish timeout remains a publication failure until its marker is read back or reattached; it does not justify repeating the experiment.

## Code and browser checks

The automated checks cover review withdrawal and test exclusion, scorer-owned aggregate metrics, image hashes, exact release versions, ambiguous managed submissions, restoration and publication-only retries. For v0.5.0, the full suite passed 207 tests at its final integration checkpoint. All nine macOS, Windows and Linux CI jobs passed on the published runtime commit; the final maintainer-only publisher fix also passes the local suite. Notebook generation and marimo dependency checks cover all six templates. Starter and facilitator still do not require Torch or SunPy.

Browser checks cover actual learner edits and CPU execution, with live provider/publication rehearsals recorded separately. The inspection browser rehearsal completed nine stages and all 1,768 predictions, followed by reproducing a saved model. Its review-selection and freeze records now include the exact parent model and source; changed choices after final evaluation require a new teaching-retest workspace. Pending’s retry repair was checked in a fresh browser session; routing completed its code-edit, review, retrain and frozen-test path using a clearly identified service fixture. Browser checks distinguish saved-record playback from live service access. A copied rehearsal workspace is not a fresh-account test. Qualification arrays, state changes and local checks use the actual lesson implementation; recorded output is never attributed to an unexecuted learner edit.

Deck validation renders every slide and reveal, checks assets and answer-return links, and renders every PDF page. The new decks use real requests and board photographs, with source links and recorded-result labels. See each deck’s `notes/delivery-checks.json` and `notes/pdf-checks.json` for the machine-readable results.

The v0.5.0 hosted templates passed source and HTML readback against their release hashes. The publisher rereads a notebook after renaming it so uploads use its current artifact collection. See the [hosted-template receipt](../evidence/hosted-templates-v050.json) and [anonymous download checks](../evidence/release-downloads-v050.json). The two new hosted pages show their correct titles and Copy to project controls. In the in-app browser, the embedded previews were blocked by a browser local-network policy; the underlying source and HTML artifacts still passed readback. Download/import and laptop instructions remain available. These checks used the maintainer account for Forge; they do not replace an external-attendee copy test. All four browser decks, PDFs and 28 referenced JavaScript/CSS assets also passed [anonymous HTTP checks](../evidence/decks-anonymous-v050.json).

The early Routing judge comparison is covered by the authored-helper test, including unavailable judgments. Live human-review alignment still needs an attendee rehearsal: the saved session has eight predictions and four judgments against dataset labels, without participant review records. Its 3/4 dataset agreement is not human agreement. [Verification record](../evidence/v051-routing-judge-evaltables.json).

## Remaining release gates

Fresh external-account copying and a human usability rehearsal remain outstanding. The new advanced SFT, Registry and remote-research modules include explicit access checks, cost controls and offline tests; they are not live-qualified training workshops. No paid advanced training or Sandbox job was launched for this release. Registry selection does not deploy a model, and ARIA queued execution still requires an active Launch worker.

Use this as a technical preview, with the recorded fallback available. It is not yet evidence that a room of new participants can finish within the workshop schedule.
