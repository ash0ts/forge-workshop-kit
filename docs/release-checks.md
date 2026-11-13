# Release checks · 0.3.0 technical preview

This release changes copied-project setup, recovery, installation and publication. The datasets, forecasting settings, agent model and recorded v0.2 examples are unchanged. Workflow compatibility remains version 1.

## What was checked

- Local tests cover notebook identity across renames, isolated copies, explicit recovery, completed sibling reuse, request matching, uncertain request accounting, atomic restore and publication-only retries.
- Both notebooks were driven in a browser through navigation and recovery, including narrow layouts. Authorizing a retry did not execute it. Uncertain requests required confirmation and retained their reservation. The facilitator saved and restored its roster. See [browser checks](../evidence/ux-v030-browser-checks.json).
- Starter and facilitator install without Torch, SunPy or MCP. Pending adds MCP; Solar adds its scientific dependencies. The generated hosted requirements were resolved independently and checked against the local lockfile. See [installation checks](../evidence/packaging-v030.json).
- A fresh workspace restored seven independently published output artifacts with matching bytes. An interrupted or corrupt download cannot install the completed journal first. See [restore check](../evidence/v030-seven-artifact-restore.json).
- Live publication checks saved W&B results, Weave evaluations and a failed tool operation in Agent Lens. Retrying the native comparison left the successful Weave references unchanged. These service checks made no model calls and trained no models. See [service checks](../evidence/v030-services.json).
- All 94 Solar slides and PDF pages rendered. The laptop commands now select the Solar dependency extra; the workshop narrative and recorded results are unchanged.

## Installation and saving overhead

On macOS arm64 with Python 3.13, one warm-cache install per profile measured these installed dependency sizes. These are local cached-install measurements, not cold-download timings or cross-platform performance claims.

| Profile | Installed dependencies | Cached installation |
|---|---:|---:|
| Previous shared environment | 1,272,048 KiB | 1.654 s |
| Starter / facilitator | 328,448 KiB | 0.328 s |
| Pending | 330,320 KiB | 0.331 s |
| Solar | 1,204,152 KiB | 0.654 s |

Preparing a checkpoint from an existing saved Solar workspace required 32.11 MB when it copied every output. Referencing the already-published outputs reduced the new payload to 5.43 MB; the request-only accounting ledger was 248 KB. Snapshot preparation took 0.257, 0.056 and 0.025 seconds respectively in one local check. This used mocked publication metadata and measured no network performance. The separate live seven-output checkpoint uploaded in 4.0 seconds. See [snapshot measurements](../evidence/publication-snapshot-local.json).

## Rehearsals and remaining limits

Fresh Pending and Solar execution rehearsals use separate workspaces and the current authored code. Their final records will be added here after both paths finish. Scripted execution checks and local browser checks do not substitute for watching an attendee follow the lesson.

Native EvalTables still returned HTTP 500 in this release's live check. W&B results, Weave evaluations and notebook comparisons remain available; the failed native publication can be retried from saved records. The hosted read-only preview is also blocked in this verification browser by its public-to-local-network restriction. This was not bypassed. Copy-to-project controls are present, but that observation alone does not establish successful attendee setup.

An external-account copy/restore check and a human usability rehearsal remain outstanding. This is a technical preview, not a claim of classroom readiness. [Previous release checks](archive/release-checks-through-v023.md) preserve the earlier scientific rehearsals and product captures.
