# Run Pending, Inc.

**Four hours · basic Python · agent tools, tracing, and harness evaluation**

An office agent must refund a duplicate charge and grant account access after a write times out. Participants implement the tools and observation handoff, then compare manual and agent-written procedures. The customer accounts are fictional; the recorded executions are real runs of the simulator.

[Open deck](https://ash0ts.github.io/forge-workshop-kit/pending/) · [Start notebook](https://ash0ts.github.io/forge-workshop-kit/packet/start/pending.html) · [Full runbook](pending-facilitator.md) · [Facilitator setup](facilitator-start.md)

## Before presenting

Open the invoice preview and the recorded timeout conversation. For a hands-on pilot, complete the [setup check](setup.md) in your own copy and add participant projects to the monitor. The full class remains a technical preview pending external-account and human rehearsal.

## Run the session

| Elapsed | Lead the room through |
| --- | --- |
| 0:00–0:40 | Predict the required account changes, open the saved notebook, and publish a first trace. |
| 0:40–1:10 | Implement invoice lookup, dispatch, and observation handoff; inspect the next model request. |
| 1:10–1:20 | Break. |
| 1:20–2:15 | Repair the timeout retry, implement checks, inspect a skill read, and test a manual procedure. Use the first ARIA investigation after development evaluation. |
| 2:15–2:25 | Break. |
| 2:25–3:30 | Review and test two candidates, choose or compose a version, save the lesson, and repeat for onboarding. |
| 3:30–4:00 | Freeze three versions, compare all 12 final executions, check the conclusion, and publish it. |

Keep account correctness separate from explanation-judge output. In the retry exercise, **Compare the two retry procedures** shows why the original operation ID must survive a retry. Later, inspect whether `read_skill` occurred before claiming an edited skill changed behavior.

## Give an eight-minute demo

Use the [recorded walkthrough](current-demo-guide.md#pending-inc-in-eight-minutes). Show one tool result entering the next request, then open the timeout recovery and matched final accounts. Ask: “Did the extra check change behavior, correctness, or both?”

## If live work stops

Use the saved execution and publication-only retry, or switch to the labeled recording. The deterministic retry repair removes a duplicate membership. The separate recorded harness comparison tied at four passing cases per version. Preserve both conclusions.
