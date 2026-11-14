# Pending deck sources

The deck follows the current gateway-free Workshop Kit notebook. The office characters, dialogue, and diagrams are original teaching illustrations. The displayed account records and results come from fictional fixtures executed in the recorded v0.3.0 rehearsal.

## Code and experiment

- [Authored notebook cells](../../../scripts/pending_cells.py): controls, prerequisites, visible controller, and publication flow.
- [Teaching functions](../../../src/forge_workshop_kit/pending/teaching.py): learner starters, worked answers, free checks, and phase names.
- [Executor and editor](../../../src/forge_workshop_kit/pending/loop.py): actual tool dispatch, observations, proposals, composition, reflection, and judge flow.
- [Rehearsal results](../../../evidence/v030-pending-rehearsal.json): all 12 final executions and judgments, harness identities, run links, and publication status.
- [Pinned Harness²](https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335): the underlying Propose–Probe–Compose idea. This workshop carries a chosen harness and lesson between two cases; it is a teaching adaptation.

The final score table is calculated from the rehearsal records, not captured product UI. Each version passed four account-state checks and four explanation judgments. Tool-call totals are 12, 13, and 13. One scripted rehearsal establishes neither repeatability nor a quality gain.

## Product captures

[Capture provenance](../../../evidence/deck-native-captures-v030.json) records the native source URLs, acquisition date, and file hashes. All originals are retained under `public/images`.

| File | What it actually shows | Enlarged crop in source pixels |
| --- | --- | --- |
| `visual-v030-pending-lookup.png` | Baseline billing `get_account`, with Acme input and account output. The agent chose this registered tool; this is not evidence that it called learner-authored `lookup_invoice`. | x=580, y=245, width=690, height=445 |
| `visual-v030-pending-timeout.png` | Skill-loaded onboarding, `provision_member` returning a timeout after the simulated write. | x=580, y=423, width=690, height=280 |
| `visual-v030-pending-recovery.png` | The same conversation's subsequent `onboarding_status` read. Preserved supporting capture. | Original only |
| `visual-v030-pending-verification.png` | Candidate B's rejected `finish`, followed by `check_work` and accepted `finish`. | x=580, y=251, width=690, height=185 |
| `visual-v030-pending-comparison.png` | Native W&B Table containing four final cases for the agent-selected version. `error=0` denotes a passed account-state check; explanation scores remain separate. | x=80, y=305, width=1180, height=380 |
| `visual-v030-pending-report.png` | The saved rehearsal Report and its interpretation. | Original only |

Crops use an SVG viewport over the unchanged image. Captures are not redrawn or retouched. Product links may require a Forge login. The older W&B Table capture remains an ordinary table. New comparison captures show the native Weave-backed Evaluation Tables Preview with aligned saved cases. The separate CES v2 publication attempt still returned HTTP 500; it is not the backend shown by these captures.

The recorded first-round composition retained the parent. The second-round composition changed the verification skill to require exactly-once outcomes and preservation of unrelated records, while keeping the completion gate off. The diff slide quotes the changed sentence from those saved harness decisions; older rehearsal screenshots with different decisions are not used.

## Setup

The QR points to [the current Pending template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view). Attendees copy it into their own writable project. Their project, authentication, inference allowance, and notebook compute apply. The historical November 12 gateway and remote Sandbox setup are outside this deck.
