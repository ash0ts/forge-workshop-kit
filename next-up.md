# Current state and next steps

Status as of November 16, 2026. The v0.12.0 package and notebook downloads are published; hosted templates retain their last verified v0.11.1 version because notebook-management access blocked their update. This page tracks unfinished work. The [technical specification](techspec.md) describes implemented behavior; [release checks](docs/release-checks.md) record what was verified.

## What is available

Six participant notebooks, a starter, and a read-only facilitator monitor are published in Forge. Each workshop has a browser deck, PDF, source, exercises, and recorded evidence. The current materials include two ARIA investigations per workshop, twelve recorded responses, and shared technical diagrams across notebooks and decks. Six overview posters introduce the work and link to each notebook. Each deck carries its workshop setting through the opening, implementation, comparison, and conclusion, alongside the technical diagrams. The visual skill can also be used in other projects. Six [public learning Reports](reports/README.md) now explain the examples and link readers directly to the notebooks they can copy.

The [v0.12.0 release downloads](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.12.0) include the new direct ARIA controls. Their source and saved HTML previews are available without waiting for the hosted update. On the current cloud login, the publisher's initial notebook lookup returns `Marimo notebook management is not enabled`; it made no template changes. Restore native management access, then resume the publisher with its existing destination receipt and verify source and preview readback. The [publication receipt](docs/release-publication-v0120.json) records this limit and the verified downloads.

The current setup is participant-owned: copy into your project, use your credentials, and save results locally and as checkpoint artifacts. No gateway is needed. Existing copies and pinned releases remain unchanged. The learning Reports reuse recorded evidence; they do not change notebook code, results, or package version.

The [workshop materials](https://ash0ts.github.io/forge-workshop-kit/packet/) bring the Reports, decks, notebook downloads, and facilitator instructions together. The ten-minute walkthrough follows each customer problem through its code and Forge records: use the [captioned video](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-captioned.mp4) for silent sharing, or the [clean video](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-clean.mp4) and [edit bundle](https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge-workshops-video-edit.zip) to add your voice-over. These are recorded demonstrations, not a new workshop rehearsal. [Tracking instructions](docs/share-links.md) distinguish external Slack and video referrals, workshop QR clicks, and the separate participant progress records; colleague reviews use the direct library link.

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

- **ARIA access and attachments:** the direct notebook path successfully submitted one Routing investigation with native run and Agent Lens conversation references, restored its answer, and opened the same native conversation. Inspection’s earlier recording also used an actual image attachment. External-account use, all twelve direct activities, and Weave/evaluation attachment controls still need qualification. An EvalTables URL does not prove panel interpretation. See the [direct-call receipt](docs/aria-direct-qualification.md) and [activity contract](docs/aria-investigations.md).
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
