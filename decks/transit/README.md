# Transit software factory

A six-hour workshop about coding agents building one departure-board application. Participants write a small coordinator, run workers in separate copies, review and integrate patches, then test whether a checked project lesson helps the next feature. The timetable is a frozen historical MBTA schedule, not live arrivals.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/transit/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzI=/view) · [Workshop guide](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/transit-workshop.md) · [Facilitator runbook](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/transit-facilitator.md) · [Presenter notes](notes/presenter.md)

## Edit and check

Edit `scripts/build-storyboard.py`, `scripts/depth-sequences.py`, and `scripts/visual-sequences.py`. They generate slides, notes, and the slide map. Follow the [shared deck instructions](../README.md) to preview, build, and validate.

`TransitMechanism.vue` contains the GTFS joins, service-day clocks, worker edit loop, claim race, dependencies, patch integration, lesson filtering, and comparisons. Objects stay in the same positions across reveals. [Visual provenance](notes/visual-coverage.md) distinguishes illustrative edits from recorded outcomes.

## Recordings and evidence

The [captioned player](public/walkthrough/index.html) has two recordings:

- **Worked example:** code edits and free checks followed by the instructor-authored reference app. It makes no model calls. The separate `transit-reference-app.zip` reproduces that app and its eighteen passing reference scenarios.
- **Recorded result:** saved R4 worker patches, a matching Agent Lens test span, the native comparison, and exported team app. It preserves failed follow-ups and launches no new workers.

The main result table uses the later R5 rehearsal. Earlier R3 and R4 captures keep their own labels. R5 supports the one-worker first release; the follow-up feature remains blocked, and its memory comparison establishes no quality benefit. [Recorded outcomes](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/transit-workshop.md#what-the-final-engineering-rehearsal-showed) explain these differences and measured costs.

The deck is a technical preview. Native readback and maintainer recording do not establish external-account access or participant usability. See the [current release checks](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/release-checks.md).
