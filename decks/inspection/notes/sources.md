# Sources and recorded evidence

- [VisA authors, pinned repository revision](https://github.com/amazon-science/spot-diff/tree/2a692ab575001cbde74d402d897a7286086c6199). Photos and masks: CC BY 4.0, Zou et al., SPot-the-Difference, ECCV 2022.
- [Official supervised split](https://github.com/amazon-science/spot-diff/blob/2a692ab575001cbde74d402d897a7286086c6199/split_csv/2cls_highshot.csv).
- [First qualification outcomes](https://github.com/ash0ts/forge-workshop-kit/blob/main/evidence/inspection-qualification-v1/results.json). The declared AP improvement gate failed.
- [Follow-up teaching retest](https://github.com/ash0ts/forge-workshop-kit/blob/main/evidence/inspection-teaching-retest-v2/results.json). All validation grid results and both final outcomes; already-inspected test images.
- [Workshop notebook source](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/inspection_cells.py).
- [Preparation, metrics and limits](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/inspection-workshop.md).

The opening factory team is fictional. Numerical results and images are recorded data. Native product screenshots must come from a successful publication; none are fabricated here.

Native Agent Lens training capture: `public/images/agent-lens-training-original.png`, from [the nearest-patch training call](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/ff65c2eaa1cc5c5cf8adb6cb706f5f52). The slide crops the original with CSS and adds numbered callouts. Its AP 0.883923, one miss and four false alarms describe 132 validation boards, not final-test results.

Native evaluation captures: `public/images/evaltables-native*.png`, verified November 14 in [Evaluation Tables Preview](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/panel/workshop-evaluation?nw=h43oxpf30iu). The detail shows `pcb1-anomaly-040` across four saved detector versions. Its next reveal shows the supplied reference mask; white pixels are annotated defects, not a detector heatmap. The underlying scores are unchanged. Capture identities and source URLs are in `data/evaltables-native.json`.
