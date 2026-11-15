# Pending, Inc. facilitator runbook

Run this as one four-hour session. Participants should be able to read basic Python; introduce the agent concepts before asking them to implement them. Use the [current deck](https://ash0ts.github.io/forge-workshop-kit/pending/) and [notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view). Each person copies the notebook into their own writable project.

| Time | Teach and do | Ask someone to demonstrate |
| --- | --- | --- |
| 0:00–0:20 | Introduce Acme's duplicate charge and Fern's access request. Use the bundled invoice preview before anyone signs in. Separate instructions, skills, the model, tool code and conversation history. | Identify the account state that would count as success. |
| 0:20–0:40 | Connect, restore and instrument a small operation. Match Python arguments and results to the Agent Lens fields. | Find their attribute in their own stored tool span. |
| 0:40–1:10 | Implement invoice lookup, dispatch and observation handoff. Run the free checks, then the two starting tickets. | Find the returned payments in the next model request. |
| 1:10–1:20 | Break. Save drafts and leave step 3 selected. | No work runs automatically. |
| 1:20–1:45 | Explain actual MCP discovery and invocation. Inspect the committed-write timeout and repair the retry in Python. | Show two memberships with the new-ID retry and one with the repaired procedure. |
| 1:45–2:15 | Implement account checks and judge validation. Publish development results. At 1:57–2:05, use the ARIA investigation to check your interpretation of the selected starting ticket. Inspect whether the run read a skill before editing one. Use the explicitly labeled local handoff example if it did not, then rerun the cases. | Separate state correctness, valid judge output and an accurate judgment. Find whether the skill was read. |
| 2:15–2:25 | Break. Save the manual comparison. | Note the next action in step 6. |
| 2:25–3:05 | Walk through the editor request, two candidate diffs and matched probes. Ask participants to choose A, B, the parent or a combination before requesting composition, then test the selected version. | Explain which changed files actually ran and why the composition needs testing. |
| 3:05–3:30 | Save the lesson and repeat on onboarding. Explain what carries forward and what resets. | Open the supporting execution for a lesson. Explain its limits. |
| 3:30–3:50 | Freeze three harnesses and run the 12 final evaluations. Compare the same ticket in EvalTables. | Trace one result to its account state, harness and Agent Lens conversation. |
| 3:50–4:00 | At 3:50–3:57, check the frozen comparison with ARIA or the recorded investigation. Publish the conclusion and name the next test in the remaining three minutes. | Describe a behavior change separately from a score change. |

Leave the exercise slide visible while people code. Use its exact button labels, not improvised instructions such as “run the agent.” A free local check and a paid execution are separate controls.

For a basic-Python learner, follow the actual values through each diagram. For an experienced developer, ask what could invalidate the inference: an unused skill, a changed executor, a stale check, or an untested combination. Both discussions refer to the same code and result.

The deterministic retry repair changes simulator behavior. The recorded harness comparison is a separate result: all three versions passed four final cases. Do not promise that a longer procedure or an agent-written edit improves quality.

If publication fails, inspect the saved execution and retry its publication. If a provider prevents live progress, use the clearly labeled recorded example; do not attribute its outcome to a participant's unexecuted edit. Session timing is a facilitation allocation, not a guarantee of provider latency.

Use the [slide-by-slide notes](../decks/pending/notes/facilitator-notes.md) for code explanations, recorded-source references and the worked-answer links.

Candidate-choice notes are optional, saved locally with the workspace, and excluded from the editor request. They do not add a new approval gate. Compare the participant’s reasoning with the editor’s actual rationale.

Use the [ARIA investigation guide](aria-investigations.md) for native context attachment, the recorded fallback, citation checks, access requirements, and separate ARIA usage. These stops replace discussion time and do not add execution gates.
