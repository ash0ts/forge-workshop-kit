# Pending, Inc.

A four-hour Python workshop about an employee agent handling duplicate charges and account access at a fictional company. Participants implement its tools and observation handoff, trace the work in Agent Lens, score the account separately from the reply, then test manual and agent-written harness changes.

[Browser deck](https://ash0ts.github.io/forge-workshop-kit/pending/) · [Copy the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) · [Facilitator runbook](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/pending-facilitator.md) · [Presenter notes](notes/facilitator-notes.md)

## Edit and check

Edit `scripts/build-storyboard.py`; it generates `slides.md`, the slide map, and presenter notes. The diagrams are Vue/SVG components. Follow the [shared deck instructions](../README.md) to preview, build, and validate. The [authored notebook cells](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/pending_cells.py) own the learner function names and controls.

## Recorded examples

The office and dialogue are fictional. Recorded examples use the [rehearsal record](https://github.com/ash0ts/forge-workshop-kit/blob/main/evidence/v030-pending-rehearsal.json), saved harness decisions, and actual Agent Lens spans. All twelve final account checks and explanation judgments passed. The changed harnesses therefore show a tie on these cases. The deterministic timeout-retry repair demonstrates a separate implementation improvement.

Native comparison slides use saved Weave-backed Evaluation Tables Preview results. [Evaluation publication](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/evaluations.md) distinguishes this path from the earlier failed CES attempt. The two ARIA investigations preserve the response and checked source; they do not supply another score.

[Source notes](notes/sources.md) identify captures and examples. [Earlier visual-design notes](notes/visual-upgrade.md) retain historical mappings and checks. The November 12 deck remains in its original release; its gateway and remote Sandbox setup does not apply here.
