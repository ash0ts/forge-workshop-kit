# Pending, Inc. presenter notes

## 1. Please improve yourself.

Welcome. We will write the pieces of an agent and then give another agent permission to edit some of them. The office is fictional. Model and tool executions later in the workshop are real.

## 2. Your first morning at Pending, Inc.

Read the manager line dryly. The participant is the person arriving; the employee is the agent. This illustrative handbook is not the actual baseline prompt.

## 3. The customer was charged twice.

Fictional dialogue illustrating the real public double-charge fixture. There are two captured 4900-cent payments on inv-1. It must refund pay-2 while preserving pay-1 and the other account. Do not describe this scene as a measured model failure.

## 4. What would count as doing the job?

Invite the room to name a failure: partial refund, wrong invoice, duplicate retry, false success. These become concrete examples when writing the scorer.

## 5. Your manager has one more request.

Use the manager question to motivate the second half. Fixed model, editable harness. The learner first freezes tested tool-loop code. The editor cannot change the trusted final scorer.

## 6. Here is our workday.

This is the three-hour Pending schedule. Allow 15 minutes at the end for final comparison and discussion. Keep extra implementation detail in worked answers.

## 7. The model chooses the next action.

Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.

## 8. Instructions define the job and its limits.

Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.

## 9. A skill is useful only when it is loaded.

Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.

## 10. Copy the notebook into your own project.

Use the current v0.3.0 template, never the historical November 12 gateway notebook. An external account requires its own project, notebook compute access and inference access. Setup does not issue a model request.

## 11. The same notebook runs on a laptop.

These commands correspond to the kit README and locked pending extra. Do not send participants to old start.py or office_notebook.py. Inference uses their own access and billing. Windows supports the same uv commands.

## 12. Check where your work will be saved.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Check my project and restore saved work.

## 13. A trace records the operation you actually ran.

This excerpt shows the independent event receipt. The visible notebook cell uses imported platform through __import__; the semantics are the same. The receipt survives separately from tracing and can be exported again without executing the operation.

## 14. Send that operation to Agent Lens.

Code excerpt from teaching.STARTERS instrumentation. Explain fields rather than reading code aloud. The full function returns its native span identity. Missing usage in model receipts remains missing.

## 15. Add a field, then find it in Agent Lens.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Run this check and verify my Agent Lens trace.

## 16. Find the arguments and the returned value.

Verified v0.3.0 baseline billing tool span get_account. The model chose get_account in this run; do not claim it chose the learner-authored lookup_invoice. Local checks exercise that authored tool separately. This early screenshot teaches the native inspection surface; participants should open their own setup trace. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.

## 17. Read one argument and follow its returned data.

Enlarged native crop x580,y245,w690,h445. Saved get_account, not lookup_invoice. Do not infer that the model called the authored lookup tool; this example teaches the same span fields participants instrumented.

## 18. The tool reads one invoice from one account.

The case is simulated but the logic is ordinary application code. Another account also has inv-1, so filtering payments without selecting the account is a real mistake the checks can catch.

## 19. Write the invoice lookup.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my invoice lookup.

## 20. A tool name has to reach executable code.

The current executor makes structured JSON action requests. Its existing schema declares lookup_invoice account_id and invoice_id; participants implement its behavior and dispatch. Do not imply they are registering remote Sandboxes.

## 21. Start with the customer’s request.

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 22. The model chooses an action and its arguments.

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 23. Your dispatcher calls the Python function.

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 24. The function returns the account records.

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 25. Put those records into the next request.

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 26. Route one tool yourself; delegate the others.

Walk through name lookup_invoice with acme/inv-1, then get_account. Explain why both paths have the same return contract.

## 27. Finish the tool-to-model handoff.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my tool-to-model handoff.

## 28. The next request contains the observation.

Clarify this is the actual workshop protocol rather than OpenAI tool-call message syntax. The complete next-request preview is available in the notebook. Do not mutate the previous messages list.

## 29. Run the two starting tickets.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze this executor and run the two starting tickets.

## 30. Record what the model saw and returned.

Excerpt deliberately abbreviates message comprehensions. The full visible instrumentation editor has input, output, system instructions, settings and available usage. Ask learners to identify the request that received the lookup result, not just count spans.

## 31. The second ticket grants Alex account access.

Use the local MCP implementation in pending/mcp_server.py. Distinguish actual protocol discovery and invocation from a function merely named MCP. The simulated service deliberately commits a write before returning a timeout in the development incident.

## 32. An access request is sent.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 33. The write succeeds. Its reply times out.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 34. Check the operation before trying the write again.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 35. Did the timeout stop the work?

v0.3.0 skill-loaded onboarding: timeout span 5ddd78b1e9faa2d3; recovery status span e62596437e485145. Ask a learner to find evidence that access exists. Do not infer failure from a red span alone. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.

## 36. The tool says the write may have committed.

Crop x580,y423,w690,h280 from the unchanged1280x720 native capture. Follow its conversation link on the preceding slide. The next operation in the saved trace is onboarding_status.

## 37. Check the account and the explanation separately.

Two measurements answer different questions. Participant-authored development checks teach scoring. Trusted final scoring covers account isolation, idempotency and task-specific constraints. Missing judge responses remain unavailable, never zero.

## 38. Make false completion fail your check.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my scorer against four known examples.

## 39. The judge needs a question it can answer.

Rubric from current pending_cells.py. Explain why the judge receives task, recorded actions and explanation. Have participants inspect one reason against a real span. Separate grammatical JSON validation from judging quality.

## 40. Publish the first comparison now.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Judge and publish the starting development comparison.

## 41. Compare the same case across versions.

Weave preserves the evaluation data. W&B stores run artifacts and result tables. Native EvalTables publication is attempted, but the latest rehearsal returned HTTP 500. Use saved Weave/notebook comparisons rather than presenting a fabricated native screen.

## 42. Change one procedure and rerun it.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Save this procedure and rerun both development tickets.

## 43. A procedure can change behavior without changing quality.

Participants do not need to manufacture a failure. A live success remains a success. The recorded rehearsal later supplies a useful no-gain example.

## 44. Save your work. Leave the employee at its desk.

Stop at 105 minutes. Use saved checkpoints; opening does not trigger paid work. Have attendees note the next step before the break.

## 45. Management would like to automate management.

This is the same fixed model with a different task and context. The editor can produce code/configuration artifacts but cannot improve scores by rewriting the definition of correct work.

## 46. Propose two changes from the same parent.

Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.

## 47. Test both on fresh copies of the case.

Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.

## 48. Ask which changes to keep.

Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.

## 49. Run the files the decision selected.

Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.

## 50. Carry the chosen version and a lesson forward.

Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.

## 51. Select evidence from the current development run.

Conceptual variable names match the visible controller; actual notebook uses _s,_case,_parent,_prefix,_f. It passes prior_experience from round1 into round2. Ask which input would be inappropriate: final-test scores.

## 52. Read the two proposals before testing them.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Ask for two competing changes.

## 53. Run the proposed files, not just the description.

Explain fingerprint as a content identity, not a metric. Do not overwhelm the audience with hash strings. The full assertion and save stage are visible in the current notebook.

## 54. Test both and compare their behavior.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Review and test candidate A; then candidate B.

## 55. This candidate required a check before completion.

Recorded candidate B changed verify_before_finish from false to true. It produced the explicit check sequence. Spans: rejected finish 9ed1e7824138ec0e, check_work 2d49d1d8d3ddeb5d, accepted finish 3e19e007d013d4d2. This is a behavior change, not yet evidence of better quality. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.

## 56. The rejected completion caused another check.

Crop x580,y251,w690,h185 from the unchanged1280x720 native capture. Gate behavior is confirmed by the subsequent check_work and accepted finish spans, not inferred from the proposal title.

## 57. Retain this version is a valid decision.

Paraphrase the actual saved v030 composition rationale, attributing it to the editor. An unchanged version still gets tested because the controller verifies every composition decision. It does not create a new executable version.

## 58. Test the composition, then save its lesson.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson.

## 59. A lesson needs an observation and a limit.

Explanatory excerpt, not a drop-in full function. The actual controller falls back to the parent if the chosen execution does not complete. The lesson is agent-authored interpretation backed by a saved run.

## 60. Repeat the cycle on onboarding.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 2 · Ask for two competing changes; follow the current action.

## 61. The second round changed the verification skill.

v030 snapshot. This is deliberately separate from older v023 captures in which both rounds retained the parent. Attribute intent to the editor. The exact files are in the executed artifact; final results show whether quality changed.

## 62. The skill makes the final check more specific.

Source .workshop/v030-pending/journal.json, pending/round-1/compose and pending/round-2/compose verification_skill. Display is an exact excerpt of the changed sentence. Round2 selected that skill with verify_before_finish=false. Link to preceding decision and execution; no attribution of final-quality gain.

## 63. What made that recursive improvement?

Explain this as a bounded Harness²-inspired workshop. It is not autonomous model-weight improvement. Upstream parallel and sequential recursion and experience reuse are richer than this teaching controller; the workshop carries a chosen harness across two problems.

## 64. Stop editing before opening the fresh cases.

Final cases: already-refunded, two-invoices, onboarding-recovery, clarify-access. Their files are public for teaching but are excluded from improvement context. The starting version is the configured tested employee, not the deliberately blank opening illustration.

## 65. Compare all three versions on fresh tickets.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze versions and run 12 evaluations.

## 66. Open a saved case and follow its trace.

Actual native W&B Table, not EvalTables and not a three-version aligned comparison. error=0 means the independent account-state check passed. judge_grounded and judge_complete are separate scores. The evaluation row also links execution evidence. All three versions are compared on the next result table. Native EvalTables remains unavailable with HTTP500. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.

## 67. Read the conclusion beside its evidence.

Use fresh v030 final table: all12 account checks and explanation judgments are available and pass. Native EvalTables unavailable; screenshot is the actual W&B/Weave/Report surface and must be captioned accordingly. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.

## 68. The loop worked. Quality did not improve here.

Source evidence/v030-pending-rehearsal.json. Tool counts sum2+4+4+2 starting and2+4+5+2 revised. Total observed rehearsal inference cost $0.03093452; exclude notebook compute and do not promise attendee cost. This measures four simulated cases, not repeatability or general enterprise-agent quality.

## 69. Keep the files that explain the result.

Artifacts are versioned file bundles. Trace export, result publication and execution have separate statuses. A publication retry uses saved work and must not make another model request.

## 70. Write down what changed and whether it helped.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Publish my conclusion with the comparison and evidence.

## 71. Ask ARIA to investigate the evidence.

Do not imply ARIA authored these prior results. The prompt asks for evidence analysis, not permission to run new experiments or change budgets.

## 72. Take the loop back to your own product.

Close by asking participants to name their own analogous workflow and one failure they could test. Leave them the current notebook, source, records and deck. Preserve honest no-gain outcomes.

## 73. Worked answer · invoice lookup

Exact semantics of teaching.ANSWERS tool. Keep optional so participants attempt the gap first.

## 74. Worked answer · observation handoff

Exact answer contract from teaching.py. Both dispatch paths return state/result. Handoff creates a new list.

## 75. Worked answer · inspect the refund

The learner check is deliberately limited. Do not describe it as the full final scorer.

## 76. Worked answer · validate the judge response

Exact semantics of teaching.ANSWERS scorer validation. Boolean strings are invalid. Empty reasons are invalid. Missing judgments stay unavailable.

## 77. Source, notebook, and recorded example

The product evidence in this deck uses the v030 rehearsal. Native EvalTables returned HTTP500; W&B and Weave records are saved. Current authored notebook source scripts/pending_cells.py. Historical deck preserved outside current attendee path.
