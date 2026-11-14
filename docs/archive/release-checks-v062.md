# Release checks · 0.6.2 technical preview

Version 0.6.1 expands the explanations in all five decks. Each sequence follows an example through intermediate values, code, output, a participant exercise, and a specific Forge investigation. The notebooks add matching introductions and companion-deck links. Runtime behavior, datasets, models, budgets, and saved progress are unchanged. This revision makes no new training, inference, or judging calls.

Version 0.6.2 removes unused generator and media-export code, shares file hashing between build and publication, and rejects malformed publication destinations. Saved-state readers now use the same locks as writers, including initial journal creation. EvalTable readback rejects missing or stringified images. The diagrams and recorded experiments remain those of 0.6.1.

## Sessions and materials

| Workshop | Allocated time | Slides | PDF pages, including reveals |
| --- | --- | ---: | ---: |
| Pending, Inc. | 4 hours | 95 | 114 |
| Solar Autoresearch | 6 hours | 123 | 213 |
| Request Routing | 4 hours | 52 | 55 |
| Visual Inspection | 4 hours | 50 | 56 |
| Transit Factory | 6 hours | 94 | 109 |

Durations include exercises and breaks. These are facilitator allocations, not measured guarantees of attendee completion time. The [deck guide](../deck-guide.md) links the schedules, presenter notes, exercise references, and current templates.

The expanded explanations cover harness components and MCP; forecast windows, tensor shapes and gradients; text features and per-intent F1; patch distances and detector thresholds; and GTFS service days, task ownership and shared lessons. The decks retain the same example values across reveals. Worked answers sit outside the main flow and link back to their exercises.

## Validation

Every slide and reveal is rendered in the browser and PDF. Checks cover actual text-line bounds, diagram labels, code clipping, static routes, native screenshot assets, and worked-answer navigation. Visual review also checks image contents: the Pending completion-gate crop was corrected because its earlier view omitted the error it was meant to explain. Original captures remain unchanged.

All five authored notebooks pass marimo dependency checks. The 51 focused tests cover their existing teaching functions, visual helpers, packaging, setup and facilitator behavior. The Python code blocks in the decks parse successfully; abbreviated excerpts remain labeled. Solar and Transit also check their exercise contracts against the actual notebook controls. See each deck’s `notes/delivery-checks.json`, `notes/pdf-checks.json`, and slide map for per-deck receipts.

The package build verifies pinned dependencies, checks all seven templates, and exports previews with provider credentials removed. Opening a preview does not execute exercises. Publication verifies the destination project and reads the uploaded source and HTML back before marking a template complete. Existing attendee copies remain unchanged. All seven current templates passed source and HTML readback; the [hosted-template receipt](../../evidence/hosted-templates-v061.json) records their versions and hashes.

The [teaching-check receipt](../../evidence/v061-teaching-checks.json) records the final slide totals and source hashes. All 33 release downloads passed anonymous checksum verification; see the [download receipt](../../evidence/release-downloads-v061.json). The browser-deck deployment also passed anonymous checks for all five decks, PDFs and source bundles; 107 authored source files matched their local hashes. See the [public-deck receipt](../../evidence/decks-public-v061.json). All 29 public documentation and source links returned the expected pages. The 26 Forge links were reachable, which alone does not establish record permissions.

The 0.6.2 cleanup passed all 305 local tests, the unused-name lint checks, and generation/check/export of all seven templates. The new tests cover open-read contention, first journal creation, malformed publisher destinations, and missing image references. They make no training or inference requests. All seven current Forge templates passed source and preview readback, and all 33 release assets passed anonymous checksum checks. See the [cleanup checks](../../evidence/v062-cleanup-checks.json), [template receipt](../../evidence/hosted-templates-v062.json), and [download receipt](../../evidence/release-downloads-v062.json).

## Results remain unchanged

- **Pending:** the committed-write retry repair prevents a duplicate membership. The later harness comparison remains a 4/4 tie.
- **Solar:** the unsuccessful GOES run stays beside its later teaching retest. The image recipe improves on two seeds and regresses slightly on the third; it did not pass the all-seed reliability gate.
- **Routing:** the full 3,080-request classifier comparison remains separate from eight prompted routing calls and four judge calls.
- **Inspection:** the revised detector improves on previously inspected test images. Both the failed first recipe and the teaching retest remain available.
- **Transit:** one builder passes 10/10 scenarios and the team passes 8/10. Both follow-up builds pass 12/18 after query workers stop at request limits. This does not establish a memory advantage.

The [previous release checks](release-checks-v060.md) retain the execution, cost, trace-readback and evaluation-readback evidence. The [README results table](../../README.md#what-happened-in-the-recorded-rehearsal) links each experiment’s protocol and limits. No scores were changed to fit the expanded teaching sequence.

<a id="windows-parallel-worker-limitation"></a>

## Windows parallel-worker repair

The branch workflow passed all nine jobs on macOS, Windows and Linux. The separate tag workflow on the same commit failed one Windows Transit test: the team returned one proposed patch instead of two. A focused local test passes normally. A simulation of Windows file-sharing contention reproduces the symptom when an unlocked task-board read overlaps an atomic replacement. The CI assertion does not print the worker outcome, so this is a plausible cause rather than a confirmed diagnosis of that CI run. The failed Windows job passed on the one bounded retry. That successful retry does not establish reliability.

Version 0.6.2 repairs the demonstrated read/write race and adds deterministic contention tests. The original CI exception was not saved, so this does not establish that the race was its only cause. The [investigation receipt](../../evidence/v061-windows-review.json) preserves the original reproduction and its limits. All nine jobs in the 0.6.2 branch workflow passed, including the full Windows suite, with no retries. The [cross-platform receipt](../../evidence/v062-ci.json) links the exact jobs. A successful run qualifies this patch; it does not establish that every possible worker failure has been eliminated.

## Remaining release gates

Fresh external-account copying and a human usability rehearsal remain outstanding. Maintainer publication and scripted browser checks do not show that new participants can complete these sessions unaided. The hosted preview has also encountered a browser local-network-policy restriction; source and HTML readback are checked separately, and notebook download/import remains available.

Native comparisons use the verified Weave-backed Evaluation Tables Preview path. The separate CES endpoint’s recorded HTTP 500 remains explicit in [evaluation setup](../evaluations.md). This teaching revision reuses those saved comparisons; it does not rerun evaluation experiments.

Use the release as a technical preview with recorded results available. The participant-adjustable $8 allowance covers inference; notebook compute is separate.
