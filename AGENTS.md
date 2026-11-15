# Workshop Kit agent instructions

This is the standalone Forge Workshop Kit repository. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Use [next-up.md](next-up.md) for current status and [techspec.md](techspec.md) for implementation contracts. The repository-local [forge-workshops skill](.agents/skills/forge-workshops/SKILL.md) routes workshop authoring and delivery work.

## Preserve these boundaries

- Edit authored cells and storyboards, then regenerate notebooks and slides. Do not repair generated output alone.
- Keep learner code visible and connected to subsequent execution. The package handles saving, accounting, tracing, publication, and shared presentation.
- Opening, navigation, hints, source editing, restoration, and building must not start training or inference. Execution stays behind explicit controls.
- A completed execution remains completed if export fails. Reuse its saved result on publication retry. Do not automatically resend a request whose outcome is uncertain.
- Preserve workflow identities, stage inputs, dataset partitions, scoring rules, model choices, and budgets unless the task explicitly changes them. Package version and experiment compatibility are separate.
- Keep development context separate from reserved evaluation evidence. Missing judgments stay missing. Recorded results never describe an unexecuted learner edit.
- ARIA investigations are analysis of selected saved records. Their notes do not automatically change measured prompts, labels, lessons, scores, or release decisions. Follow the [ARIA contract](docs/aria-investigations.md) when editing that path.
- The participant owns the project and credentials. The facilitator reads progress. Do not add a gateway, host-issued access token, or shared credentials to the core flow.

## Finish the requested work

Use the checks for the files changed, as described in [CONTRIBUTING.md](CONTRIBUTING.md#check-a-change). Report code, browser, native-access, and human-rehearsal coverage separately. Preserve unsuccessful runs and known access limitations; a successful build is not a readiness upgrade.

Build and publish using [maintenance](docs/maintenance.md). Existing task authorization applies; do not add an approval step to ordinary local edits. If publication was not requested, leave a validated local build. Never overwrite prior release assets or attendee copies to simplify a new release.

Keep one canonical home for each contract. Update or remove inbound links when moving documentation. Check [.github/CODEOWNERS](.github/CODEOWNERS) when paths or ownership change. Keep credentials, `.workshop/`, `.workshop-deployments/`, and downloaded runtime artifacts out of commits.
