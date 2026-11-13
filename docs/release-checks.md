# Release checks · 0.2.3 technical preview

The 0.2.3 update adds curated Forge views, clearer Reports, a demo guide, native product captures, and distinct publication links for image and measurement comparisons. It changes no data, training code, model settings, or recorded results. Full live rehearsals below were completed for 0.2.0; presentation and packaging checks are separate.

The revised notebooks were exercised in a browser using fresh local workspaces and real Forge services. They still need an external-attendee check and a human usability rehearsal before classroom-ready status.

| Check | Evidence and outcome |
| --- | --- |
| 0.2.3 named dashboards | The Solar view selects eight current rehearsal runs; Pending selects three final comparison runs. Every displayed metric matches server readback. The default workspace and run records are unchanged. [Configuration and readback](../evidence/demo-workspaces.json). |
| 0.2.3 Reports | Both existing Report IDs now show native comparison charts, complete result tables, and a short trace-to-code path. Conclusions and scores are preserved. [Readback](../evidence/demo-reports.json). |
| 0.2.3 public views | Signed-out browser checks passed for both named dashboards and the selected Solar artifact. Agent Lens captures remain labeled authenticated views. [Checks](../evidence/ux-v023-public-dashboards.json). |
| 0.2.3 deck | All 94 browser frames and PDF pages match their expected headings; no missing images or overflow. All 191 Pages routes, worked-answer returns and native product links passed. [Native frames](../decks/solar/notes/native-v023-render-checks.json), [PDF checks](../decks/solar/notes/pdf-checks.json), [capture provenance](../evidence/ux-v023-native-captures.json). |
| 0.2.3 code and package checks | All 62 tests and four marimo notebook checks pass. Wheel and source archive build offline; packaged UI matches source, fonts and lab artwork are present, and private runtime paths are absent. The lockfile changes only the package version. [Checks](../evidence/ux-v023-package-checks.json). |
| 0.2.3 comparison links | The notebook labels image and GOES persistence separately and preserves all six run/Weave links. Unavailable comparisons remain unavailable. No training or inference was added. |
| 0.2.3 static notebook previews | All four notebooks export with kernel source hidden. Solar and Pending initial screens render directly at 1440px and 430px, with no horizontal page overflow or browser errors. The export environment has no provider credentials or saved workshop state; no model requests or training ran. These are saved previews, not live notebook checks. [Evidence](../evidence/ux-v023-static-exports.json). |
| Current hosted preview limitation | The embedded notebook preview is blank in the tested browser, which reports a public-page-to-local-network error. The native Copy dialog opens; a running copied notebook has not been verified for this revision. Use the [documented fallback](current-demo-guide.md#when-a-product-view-is-unavailable) and retain the external-attendee release gate. |
| 0.2.2 hosted templates | All four originals now use v0.2.2. Downloaded notebook sources match the release byte-for-byte; existing attendee copies were not modified. [Readback](../evidence/ux-v022-template-readback.json). |
| 0.2.2 public deck and downloads | Signed-out checks passed for the final revised instructions, direct links, answer returns, and images. The PDF, source/browser ZIPs, and wheel match the built files. [Readback](../evidence/ux-v022-public-release.json), [deployment](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43487185727). |
| 0.2.2 platform checks | Locked installs, all 60 tests, and all four notebook checks passed on macOS, Windows, and Linux for the release commit. [CI](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43487275912). |
| 0.2.2 deck | All 90 browser frames and PDF pages render. Eight worked-answer links and returns, 183 static routes, and exact notebook-control checks pass. [Copy checks](../decks/solar/notes/copy-v022-checks.json), [final render checks](../decks/solar/notes/render-v022-checks.json). |
| 0.2.2 copy and code checks | All 60 existing tests pass, all four generated notebooks pass marimo checks, and all four static HTML exports render. Model requests and training executions for this revision: zero. [Review](../evidence/ux-v022-copy-review.json). |
| 0.2.2 notebook screens | Pending’s eight steps were checked over a copy of saved rehearsal data; Solar’s setup, data and recorded example were checked without connecting. Both passed 430px layout checks. [Pending](../evidence/ux-v022-pending-browser.json), [Solar](../evidence/ux-v022-solar-copy-checks.json). These are presentation checks, not new live rehearsals. |
| 0.2.1 local validation | 60 tests passed, including candidate isolation, missing judgments, recovery, exact executed code, draft restore and trace links. All four generated notebooks passed marimo checks. |
| Clean platform installs | Locked installation, all 60 tests and all four notebook checks passed on GitHub-hosted macOS, Windows and Linux runners. [CI run](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43476598776). This checks installation and code; it is not an attendee rehearsal. |
| 0.2.1 hosted templates | All four templates now use the released 0.2.1 wheel and notebook source; downloaded artifact sources match byte-for-byte. Existing copies remain unchanged. [Readback](../evidence/ux-v021-template-readback.json). |
| 0.2.0 hosted rehearsal | All four hosted templates were updated for the prior release. Their artifact source files match the released notebooks byte-for-byte. [Readback](../evidence/ux-v020-template-readback.json). Existing copies were not modified. |
| 0.2.1 browser presentation | Both notebooks highlight the active step correctly; narrow layouts have no horizontal overflow. Saved Solar results restore with the new lab heading, provenance and recorded comparison. No new training or inference. [Checks](../evidence/ux-v021-notebook-checks.json). |
| 0.2.1 realism audit | All raw and prepared data checksums verified. Final image scores recomputed from saved predictions; frozen source and weights match. No training or inference rerun. [Review](solar-evidence.md). |
| Guided exercises | Both notebooks expose participant code, free checks, explicit execution, results and Forge links. Navigation and prerequisite links were exercised in the browser. Draft edits survive navigation and restart. |
| Solar browser rehearsal | Six native Sweep configurations, two manual image architectures, both two-candidate research rounds, tested compositions and frozen comparisons completed. [Results](../evidence/ux-v020-solar.json). |
| Pending browser rehearsal | Both improvement rounds and all 12 final executions completed. All 12 reached the correct account state; 11 of 12 explanation judgments were available. The editor retained the manual harness; three labels represent two distinct executable versions. [Results](../evidence/ux-v020-pending.json). |
| Agent Lens | Stored spans were checked against independent execution records. Native screens show [research evidence selection](../evidence/ux-v020-solar-lens-current.png) and the [learner-authored invoice tool](../evidence/ux-v020-pending-lens.png). |
| Recovery | Completed work and evidence links restore from durable records. A failed Pending MCP attempt was retained; recovery reused the saved billing execution. Publication retries do not repeat training or inference. |
| Deck | All 90 frames and PDF pages were rendered and inspected. Exercise function/button contracts, interactive inspectors, worked-answer returns and keyboard navigation passed. [Deck checks](../decks/solar/notes/render-checks.json). |
| Layout | The new lab header, data provenance and recorded-result table were inspected in desktop and narrow layouts. [Lab](../evidence/ux-v021-solar-lab.png), [recorded example](../evidence/ux-v021-solar-recorded-example.png). The prior release also passed light/dark checks. IBM Plex is bundled locally. [Desktop](../evidence/ux-v020-solar-desktop.png), [narrow dark](../evidence/ux-v020-solar-dark-narrow.png). |
| Native products | Sweep runs, artifacts, Weave evaluations and Reports publish. Native EvalTables still returns HTTP 500; its status remains unavailable. [Service checks](../evidence/services.json). |
| Earlier hosted check | A maintainer used native Copy to project, checked its distinct identity, and exported stored spans with hosted authentication. [Receipt](../evidence/hosted-copy.json). This does not establish external-account access to the revised release. |
| Fresh artifact restore | Restored 44 completed Solar stages and 16 drafts into a fresh local runtime. All 96 output files matched byte-for-byte. Loading the saved weights reproduced final error 0.11001095193834161 exactly, with no training updates or new inference. [Receipt](../evidence/ux-v020-restored.json). |
| Public Reports | Both new rehearsal Reports rendered in a signed-out browser. [Readback](../evidence/ux-v020-reports-public.json). Templates still require sign-in to copy. |
| 0.2.1 public deck and downloads | Signed-out checks passed for the lab cover, Agent Lens, matched forecasts, measured result, GOES contrast, answer returns and direct-link reloads. PDF, browser/source ZIPs and wheel match local hashes. [Readback](../evidence/ux-v021-public-release.json), [deployment](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43476598839). |
| 0.2.0 public deck and downloads | The deployed deck passed signed-out direct-link, reload, image and worked-answer return checks with HTTP 200 and no browser errors. PDF, browser ZIP, editable source ZIP and wheel downloads match local hashes. [Readback](../evidence/ux-v020-public-release.json), [deployment](https://github.com/ash0ts/forge-workshop-kit/actions/runs/43473977791). |
| Monitoring | Public progress runs are read-only. Missing updates remain unknown. No classroom-scale load test or human rehearsal has been performed. |

## What the recorded results show

In the revised Solar browser rehearsal, final image error was **0.125762 for persistence, 0.122442 for the manual residual model, and 0.110011 for the agent-selected model**. The agent first proposed a zero-initialized residual head, then combined it with a disk-masked L1 training loss. Each adopted version was tested before selection. Inspect the exact diffs and validation records in the deck's branch explorer.

These 199 overlapping windows come from two reserved days and one seed. The result shows that the workshop can execute and inspect a useful code change; it does not establish a general forecasting gain.

The GOES models remain a useful counterexample: final log-flux error was **2.468975**, versus **0.192706** for persistence. The short 60-step training budget produced a poor forecast. We keep its learning curve and actual predictions in the workshop instead of quietly changing the training budget after seeing the score.

Pending completed the account work in all 12 final executions. The editor's decision to retain the manual harness is valid, and does not demonstrate an additional improvement from automated editing. State correctness and explanation judgments remain separate. One explanation judge exhausted its output limit on both the initial request and one explicit judge-only retry. Its result remains unavailable, never zero. Those attempts are charged and preserved; the employee execution was not repeated.

The Pending rehearsal also exposed an editor-context defect: the prompt did not clearly separate the current mission from prior experience. The revised prompt now does; focused checks verify that separation. Existing decisions and scores were preserved rather than relabeled as runs of that repair.

The recorded results belong to the rehearsal. A learner's unexecuted code edit has no result attached to it.

## Timing and cost

Measured inference was **$0.018331 for Solar** and **$0.036720 for Pending**, including the failed judge requests. Unknown usage and in-flight reservations were zero at completion. The machine-readable rehearsal receipts report actual training time and provider time. These exclude time spent reading code, reviewing diffs and discussing results. They are not classroom timing measurements. Local CPU execution incurred no hosted compute charge; hosted notebook compute is separate from the participant's inference allowance.

## Remaining release gates

- An external attendee must copy the final template into a different account, check its own inference entitlement, train, and restore a destroyed runtime.
- A developer and a less technical participant must complete the code exercises and explain their results without facilitator takeover.
- Recheck native EvalTables when its HTTP 500 is repaired. Until then, teach the labeled Weave/notebook comparison path.

Prior workshop releases and attendee copies are untouched. No core product code changed.
