# Current state and next steps

Status as of November 15, 2026, after the v0.10.0 release and its UTF-8 authoring fix. This page tracks unfinished work. The [technical specification](techspec.md) describes implemented behavior; [release checks](docs/release-checks.md) record what was verified.

## What is available

Six participant notebooks, a starter, and a read-only facilitator monitor are published in Forge. Each workshop has a browser deck, PDF, source, exercises, and recorded evidence. The latest release adds two ARIA investigations per workshop, with twelve actual recorded responses and citation checks for participants without live access. Six [public learning Reports](reports/README.md) now explain the examples and link readers directly to the notebooks they can copy.

The current setup is participant-owned: copy into your project, use your credentials, and save results locally and as checkpoint artifacts. No gateway is needed. Existing copies and pinned releases remain unchanged. The learning Reports reuse recorded evidence; they do not change notebook code, results, or package version.

**All six workshops remain technical previews.** Maintainer checks, successful uploads, and recorded executions do not establish that a new participant can complete the class. The priorities below are the remaining qualification work, not promises that the services already work for every account.

## Before running a class

| Priority | Work to do | Evidence needed to close it |
| --- | --- | --- |
| 1 | Use fresh external accounts to copy each template, publish a trace, save work, rename the copy, and restore after replacing its runtime. Check a team account with ARIA and an account using the recorded fallback. | Separate access receipts showing the participant’s project, isolated copy identities, restored files and completed results, and actual live or recorded ARIA use. No facilitator credentials. |
| 2 | Rehearse each workshop with someone who has not used the kit. Ask them to make the code change, explain an intermediate value, and locate the corresponding Forge record. | Measured timing, points where help was needed, and specific control or explanation fixes. The published durations remain session allocations until this is done. |
| 3 | Qualify Airline’s native monitoring activities. Recheck AI Alignment, prepare a completed Insights cluster, and confirm an external attendee can inspect it. | Actual judge processing and criteria readback, reviewed disagreements and coverage, source-linked cluster members, and verified shutdown of automatic tagging. The last six Alignment requests returned HTTP 500; missing results cannot count as negatives. |
| 4 | Complete browser coverage of the current authored steps, particularly Airline’s review, tagging, curation, and recovery path. | A receipt that names the current cells and controls exercised, separate from domain tests and older scripted rehearsals. Forty successful conversations do not cover every notebook interaction. |

Use [setup and recovery](docs/setup.md), the [workshop runbooks](docs/README.md#workshop-runbooks-and-evidence), and [Airline qualification](docs/airline-monitoring-qualification.md). Record failures alongside successes. Do not rerun completed inference merely to repair an export.

## Product access still to qualify

- **ARIA attachments:** exact links and supplied excerpts were exercised; Inspection also used an actual image attachment. Native run and Weave attachment controls need their own successful rehearsal. A pasted URL does not establish that ARIA read the record, and supplying an EvalTables URL does not prove panel interpretation. Follow the [ARIA activity contract](docs/aria-investigations.md).
- **Evaluation services:** the kit uses the verified Weave-backed native EvalTables path. The separate CES backend’s last recorded HTTP 500 remains a limitation. Keep the working path and unavailable service distinct in the UI and documentation. See [evaluation publication and recovery](docs/evaluations.md).
- **Advanced modules:** SFT, Registry release exercises, and remote research need their own access, cost, timing, and reproduction checks before being taught as demonstrated extensions. They are optional and must not become prerequisites for the six core workshops. See [advanced module status](docs/advanced/README.md).

## Research questions, not cleanup bugs

The [recorded results](docs/recorded-results.md) intentionally include outcomes that did not improve. Pending’s final harness comparison tied. Airline’s two versions both passed. Solar’s image recipe regressed on one qualification seed. Transit’s team missed checks the solo builder passed, and its follow-ups did not establish a memory benefit.

If we test a different recipe or broader data, give it a new experiment identity and retain the prior outcomes. Freeze the comparison before looking at its reserved results. Previously inspected data can support a teaching retest, not a claim of newly unseen evaluation.

## Where to pick up the work

- **Fix an explanation or control:** start with [CONTRIBUTING.md](CONTRIBUTING.md). Edit authored cells or storyboards, update exercise references, and regenerate the affected output.
- **Investigate saving, retries, or publication:** follow the source links and state diagrams in [techspec.md](techspec.md). Preserve successful work and conservative accounting for uncertain requests.
- **Add a workshop:** use the [authoring guide](docs/authoring.md) and [forge-workshops skill](.agents/skills/forge-workshops/SKILL.md). Keep the experiment and the code learners change visible.
- **Prepare a release:** use [maintenance](docs/maintenance.md). Build locally first, publish to an explicit verified destination, and keep external-account and human coverage separate from automated checks.

When an item is completed, put its durable behavior in the relevant guide, link the verification record from [release checks](docs/release-checks.md), and remove it from this list. Keep earlier release evidence in the [archive](docs/archive.md).
