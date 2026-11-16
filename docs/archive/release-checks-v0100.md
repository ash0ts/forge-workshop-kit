# Release checks · 0.10.0 technical preview

This revision adds two scheduled ARIA investigations to each workshop: eight minutes after a development result and seven minutes before the final Report. Participants explain their interpretation, ask ARIA about selected records, and check one cited observation. These activities replace existing discussion time. Datasets, experiment settings, workflow identities, inference allowances, and final comparisons are unchanged.

The [ARIA guide](../aria-investigations.md) describes the activities and access requirements. The [0.9.0 checks](../archive/release-checks-v090.md) preserve validation of the preceding teaching sequence. Existing attendee copies and release assets remain unchanged.

## What this revision checks

| Coverage | Evidence and limits |
| --- | --- |
| Context and saving | Free tests cover development-only stage selection, workspace isolation, unavailable links and cases, exact evidence identity, local note persistence, old journals, Report inclusion, and facilitator summaries. Notes never enter measured prompts or scores. |
| Authored notebooks | All twelve activities are bound to current authored cells and manifest references. Routing's first investigation requires only TF–IDF; development activities precede their interventions; closing activities precede Report publication. |
| Browser interactions | The shared card is checked with saved evidence, including prompt editing, recorded fallback, citation saving, restoration, narrow layout, and light/dark themes. Navigating and saving do not create requests, training stages, or publications. This does not replace an external participant rehearsal. |
| Native ARIA | Actual conversations use the selected records and exact prompts. Each recording retains its answer, source links, access limitations, and a checked citation. Supplied excerpts and records independently retrieved by ARIA are distinguished. |
| Native media | The Inspection development recording attaches the actual validation photograph. ARIA describes visible components but explicitly cannot establish the defect visually. The supplied defect label and reproduced score are identified as separate evidence. |
| Decks and PDFs | The new sequences show the question, a claim from the actual response, and the checked source. Original captures are preserved; annotations identify fields without replacing values. Browser and PDF receipts accompany the release. |
| Packaging and publication | The build checks all eight templates and exports credential-free previews. Publication verifies the destination and reads back source and preview hashes. Maintainer publication does not establish external-account access. |

The [final validation receipt](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.10.0/validation-v0100.json) records test counts, build results, native conversation identities, and outstanding checks. The complete local suite passed 475 tests after the UTF-8 authoring fix. [Windows, Linux, and macOS CI](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43749901938) also passed. The [deck deployment](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43748011053) rendered and checked all six decks and PDFs.

All eight templates passed source/preview readback. The maintainer browser check loaded all six workshop previews and their **Copy to project** controls; it did not create or run external-account copies. The [validation bundle](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.10.0/validation-v0100.zip) preserves detailed receipts and captures. No workshop model was retrained and no underlying agent experiment was repeated to make an ARIA attachment. ARIA conversations are new usage outside the notebook's $8 inference allowance; their cost is marked unavailable where the product did not expose it.

## What the recordings establish

The recordings preserve disagreement and incomplete evidence. Pending's final scores remain tied. Solar's image improvement and worse GOES result remain separate. Routing distinguishes a controlled loader defect from classifier error. Inspection preserves the detector selected before test evaluation even where another detector has fewer test misses. Transit retains its observed coordination and memory outcomes. Airline distinguishes booking correctness from monitoring agreement and processing coverage.

Native URL retrieval worked for the named records in several investigations. The first Pending response relied on supplied excerpts and explicitly said so. The Inspection closing response verified the saved selected identity and metrics but could not independently establish the selection chronology. These are teaching examples of evidence limits, not failed answers replaced with invented successes.

The rehearsed interaction uses exact source links and saved excerpts, plus a native image attachment for Inspection. Pasting a URL or an `@run-name` string is not a native attachment and does not prove retrieval. Native run/Weave attachment controls remain dependent on the available interface; participants must check the actual context and response. The workshop does not claim that ARIA interpreted an EvalTables panel merely because its URL was supplied.

## Outstanding readiness checks

The prioritized work and completion criteria are in [next-up.md](../../next-up.md). Fresh external-team access, a participant without ARIA access, and a human rehearsal remain outstanding. The recording path is tested locally without provider calls; that is not a fresh-account access test. All six workshops remain **technical previews**.

Native EvalTables comparisons were inspected using the existing Weave-backed publication path. Missing metrics are not inferred from unrelated displayed fields. Airline's earlier AI Alignment HTTP 500 responses and unavailable Insights clusters remain explicit limitations; this revision does not claim those services recovered. See [evaluation recovery](../evaluations.md) and [Airline qualification](../airline-monitoring-qualification.md).

ARIA requires suitable team-project access and Smart features. Its usage follows organization settings and is separate from notebook inference and compute. No access check sends an ARIA message automatically. Airline's automatic tag shutdown remains in its closing schedule.

## Materials

The [v0.10.0 release](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.10.0) coordinates the package, current notebook sources and previews, six decks and PDFs, twelve recorded investigations, editable sources, facilitator schedules, and validation receipts. Current template identities stay stable; previously copied notebooks are untouched.
