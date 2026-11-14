# Pending, Inc. presenter notes

## 1. Please improve yourself.

We will implement an agent that can inspect an account, refund a duplicate charge, and provision access. Then we will instrument and evaluate its work before asking an editor agent to revise its instructions. Pending, Inc. and its accounts are fictional; the Python tools, model requests, traces, and evaluations run in your own project.

## 2. Your first morning at Pending, Inc.

Pending, Inc. is a teaching setting for a familiar engineering problem: connecting a model to existing application operations. The handbook is an opening illustration. We will build and test a configured starting harness before comparing any revisions.

## 3. The customer was charged twice.

Read the customer request and ask what the agent must know before issuing a refund. The development fixture contains two captured 4900-cent payments on Acme invoice inv-1. The correct outcome refunds pay-2 once while preserving pay-1 and the other account. The empty tool menu explains what we need to implement; it is an illustration rather than a recorded model failure.

## 4. Define the account state a correct refund should leave.

Ask someone to name the account fields they would check after this request. We need to identify the correct payment, refund the full amount once, and preserve unrelated state. We will later use partial refunds, duplicate refunds, and false completion claims to test the scorer. A fluent final reply cannot establish these account facts.

## 5. Your manager has one more request.

We will first make the agent executable and observable. Once we can inspect a run and score its outcome, we can give those same records to an editor agent. It changes instructions and selected workflow settings, while our tested tools and final scorer remain fixed. That lets us compare the proposed procedures under the same conditions.

## 6. Implement the agent, evaluate it, then test harness changes.

This is the three-hour Pending schedule. Allow 15 minutes at the end for final comparison and discussion. Keep extra implementation detail in worked answers.

## 7. The executor dispatches the model’s selected action.

For this ticket, the model might choose lookup_invoice, then refund_payment. It returns an action name and arguments. Python decides which function handles that action, and the tool changes the simulated account. The model does not directly mutate the account dictionary.

## 8. Instructions define how the agent should handle the ticket.

The harness is the code and instructions around the model. It controls the request we send, the actions we allow, and the checks we require. We can revise these pieces while using the same model. In our comparison, the dispatcher and tools stay fixed after we test them.

## 9. Reading a skill adds its procedure to the conversation.

A saved skill has no effect until the executor supplies it to the model. Here the agent can call read_skill; the returned procedure enters the same conversation as other tool results. Agent Lens lets us check whether the skill was read and what the model did afterward.

## 10. Copy the notebook into your own project.

Use the current template, never the historical November 12 gateway notebook. An external account requires its own project, notebook compute access and inference access. Setup does not issue a model request.

## 11. The same notebook runs on a laptop.

These commands correspond to the kit README and locked pending extra. Do not send participants to old start.py or office_notebook.py. Inference uses their own access and billing. Windows supports the same uv commands.

## 12. Check where your work will be saved.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Check my project and restore saved work.

## 13. Save an operation’s inputs, output, and timing.

The event helper runs the supplied function and returns two objects. result is what the caller needs; record describes the operation with its arguments, output, timing, and any error. We save that record before exporting a trace. If export fails, we can send the saved record again without repeating a refund or another model request.

## 14. Export the saved operation as an Agent Lens span.

Map each field to the record from the previous slide. Tool creates a span with the operation name, inputs, output, and timestamps; record_error attaches the recorded failure. This function exports an event that already happened. The full notebook function returns its span identity so the execution can link back to Agent Lens.

## 15. Add an environment field and inspect it in Agent Lens.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Run this check and verify my Agent Lens trace.

## 16. Inspect the account requested by this tool call.

Verified v0.3.0 baseline billing tool span get_account. The model chose get_account in this run; do not claim it chose the learner-authored lookup_invoice. Local checks exercise that authored tool separately. This early screenshot teaches the native inspection surface; participants should open their own setup trace.

## 17. Check which account records the model received.

Enlarged native crop x580,y245,w690,h445. Saved get_account, not lookup_invoice. Do not infer that the model called the authored lookup tool; this example teaches the same span fields participants instrumented.

## 18. The tool reads one invoice from one account.

The case is simulated but the logic is ordinary application code. Another account also has inv-1, so filtering payments without selecting the account is a real mistake the checks can catch.

## 19. Write the invoice lookup.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my invoice lookup.

## 20. Connect the action schema to your Python function.

The model sees an action schema that names lookup_invoice and its account_id and invoice_id arguments. That schema alone cannot read an account. Your dispatch function connects the selected name to the Python implementation. This workshop uses local Python for the tool and real local MCP for onboarding.

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

## 26. Dispatch lookup_invoice to your function.

Trace two inputs through this function. lookup_invoice calls the participant function and returns the same world with its lookup result. get_account takes the existing call_tool path. Both return a pair of account state and observation, so the caller can append the observation consistently. A write tool may return changed state.

## 27. Append the action and its result to the next request.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my tool-to-model handoff.

## 28. Include the tool observation in the conversation history.

The model cannot see a Python return value unless the executor includes it in a later request. Append the chosen action and its result to a new list so the previous request stays available for inspection. This executor uses JSON actions and a user message containing the observation; it is not using the OpenAI tool-message protocol.

## 29. Test the starting harness on billing and onboarding.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze this executor and run the two starting tickets.

## 30. Record each model request and its response.

The LLM span records the requested and returned model identities, input and output messages, timing, settings, and available usage. Entering the span context creates and closes the recorded span; constructing the object alone is insufficient. Open my_model_span for the full message mapping and usage handling; this slide abbreviates the comprehensions. Add usage only when the provider returned it. In Agent Lens, find the request after an account lookup and verify that its input contains the returned payments.

## 31. Provision Alex’s membership through the MCP tools.

Use the local MCP implementation in pending/mcp_server.py. Distinguish actual protocol discovery and invocation from a function merely named MCP. The simulated service deliberately commits a write before returning a timeout in the development incident.

## 32. An access request is sent.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 33. Provisioning commits before its response times out.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 34. Read account access before retrying the write.

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 35. A stable operation_id prevents a repeated write.

Illustration of simulator.execute after a committed provisioning request. The same operation_id and identical arguments return the stored receipt with replayed=true. A new operation_id is a new mutation and can add a duplicate membership. Reusing an ID with different arguments is rejected. The recorded onboarding recovery read status instead of retrying, so this diagram explains tool behavior rather than claiming this branch occurred in that run.

## 36. Inspect the timeout and the following status check.

v0.3.0 skill-loaded onboarding: timeout span 5ddd78b1e9faa2d3; recovery status span e62596437e485145. Ask a learner to find evidence that access exists. Do not infer failure from a red span alone.

## 37. The tool says the write may have committed.

Crop x580,y423,w690,h280 from the unchanged1280x720 native capture. Follow its conversation link on the preceding slide. The next operation in the saved trace is onboarding_status.

## 38. Check the account and the explanation separately.

The state scorer reads the account after execution and checks facts such as payment identity, refund amount, and duplicate effects. The LLM judge reads the request, actions, and final reply to assess whether the explanation is supported. These can disagree: an agent may do the right work and describe it incorrectly. An unavailable judge response stays missing.

## 39. The same confident reply can accompany four account states.

These are the four free development fixtures from teaching.check_scorer: one 4900-cent refund, a 100-cent refund, no refund, and two 4900-cent refunds. They share the reply Everything is resolved. The displayed PASS/FAIL values are the required deterministic checks, not inferred LLM judgments. Ask which fields my_state_check must read before participants implement it.

## 40. Write checks for full, partial, missing, and duplicate refunds.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my scorer against four known examples.

## 41. Ask the judge to compare the reply with recorded actions.

Rubric from current pending_cells.py. Explain why the judge receives task, recorded actions and explanation. Have participants inspect one reason against a real span. Separate grammatical JSON validation from judging quality.

## 42. Publish development results with both kinds of score.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Judge and publish the starting development comparison.

## 43. Compare the same case across versions.

Weave preserves the evaluation data. W&B stores run artifacts and result tables. Native EvalTables publication is attempted, but the latest rehearsal returned HTTP 500. Use saved Weave/notebook comparisons rather than presenting a fabricated native screen.

## 44. Revise the verification skill and rerun both tickets.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Save this procedure and rerun both development tickets.

## 45. Compare account correctness with the added tool calls.

Ask participants to identify the changed instruction and the corresponding tool calls. If both versions leave the account correct, report that result. An extra check may change cost or latency without improving the outcome on this case.

## 46. Take a ten-minute break after saving your progress.

Stop at 105 minutes. Use saved checkpoints; opening does not trigger paid work. Have attendees note the next step before the break.

## 47. Management would like to automate management.

The editor uses the same fixed model, but its request is to revise the harness rather than resolve a customer ticket. We supply the current configuration and a saved execution. The permitted edits are instructions, the verification skill, and bounded workflow rules. Tools and scoring stay fixed so any measured difference concerns the harness we changed.

## 48. Propose two edits to the same starting harness.

Propose asks the editor for two competing changes, such as clearer verification instructions or a mandatory completion check. A and B start from the same parent. Neither receives the other candidate’s test result at this point. We review their saved configurations before allowing the probes.

## 49. Run each candidate from the original account state.

If candidate A has already issued a refund, B must not inherit that refunded account. The controller resets the case before each probe. Compare the actions and returned state of both runs; a successful tool response alone does not tell us the ticket was handled correctly.

## 50. Compare the probe results before selecting a harness.

Compose receives the proposed configurations and both execution records. It can choose A or B, combine parts of them, or retain the parent. Its rationale explains that choice, but the choice still needs an execution. The solid paths show versions; colors identify alternatives rather than scores.

## 51. Execute the harness returned by the composition decision.

A combination may differ from both tested candidates, so we run the returned configuration as its own probe. A Retain decision also runs through this step without inventing a new executable version. We can then inspect the specific execution associated with the decision.

## 52. Save the selected harness and a lesson for onboarding.

Reflect asks the editor what it learned from the selected run and where that conclusion may not apply. We keep the lesson with that run, then execute the selected harness on onboarding before proposing more changes. This carried-harness teaching protocol differs from the full upstream Harness² cross-task procedure.

## 53. Give the editor the starting execution and harness.

Conceptual variable names match the visible controller; actual notebook uses _s,_case,_parent,_prefix,_f. It passes prior_experience from round1 into round2. Ask which input would be inappropriate: final-test scores.

## 54. Review the proposed instruction and workflow changes.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Ask for two competing changes.

## 55. Construct and execute the proposed harness.

The editor returns a structured harness in its decision. The controller constructs that harness, executes it on a reset case, and checks the recorded content fingerprint against the decision. That comparison catches running the wrong version. It says nothing about whether the selected instructions are good; the account scorer answers that separately.

## 56. Run both candidates and inspect their tool sequences.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Review and test candidate A; then candidate B.

## 57. Require a passing check of the current state before finish.

The loop stores last_check with passed and the digest of world. With verify_before_finish true, finish is rejected if that check is absent, failed, or no longer matches the current state. This is a runtime completion rule. check_work gives public development feedback; the independent final scorer separately checks entire expected accounts and the required resolution.

## 58. This candidate required a check before completion.

Recorded candidate B changed verify_before_finish from false to true. It produced the explicit check sequence. Spans: rejected finish 9ed1e7824138ec0e, check_work 2d49d1d8d3ddeb5d, accepted finish 3e19e007d013d4d2. This is a behavior change, not yet evidence of better quality.

## 59. The completion gate required a check_work call.

Crop x580,y251,w690,h185 from the unchanged1280x720 native capture. Gate behavior is confirmed by the subsequent check_work and accepted finish spans, not inferred from the proposal title.

## 60. Compare the added checks with the resulting account state.

Recorded first-round probe A used the parent harness: get_account, refund_payment, get_account, finish. Probe B used verify_before_finish=true: the same first three calls, a rejected finish, check_work, and an accepted finish. Both independent account checks passed. Tool-call counts are four and six for these development probes, distinct from the later final-evaluation totals. Source: the v0.3.0 rehearsal journal pending/round-1/probe-a and probe-b, linked through the native conversations on the preceding slides.

## 61. The editor retained the parent after comparing the probes.

Open this saved composition if time allows. The editor’s rationale was that the mandatory gate added work while the parent already produced a correct billing outcome. It retained the parent. The controller still runs the selected configuration because every composition receives a confirming execution, including KEEP. The executable content remains unchanged.

## 62. Test the selected harness before carrying it forward.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson.

## 63. Save the lesson with the run that supports it.

Explanatory excerpt, not a drop-in full function. The actual controller falls back to the parent if the chosen execution does not complete. The lesson is agent-authored interpretation backed by a saved run.

## 64. Use the selected harness to start the onboarding round.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 2 · Ask for two competing changes; follow the current action.

## 65. The second round changed the verification skill.

In the recorded onboarding round, the editor selected a more specific verification skill while leaving verify_before_finish off. Open the decision to read its rationale, then the chosen execution to inspect how the agent used those files. The next slide shows the exact changed sentence.

## 66. The skill makes the final check more specific.

Source .workshop/v030-pending/journal.json, pending/round-1/compose and pending/round-2/compose verification_skill. Display is an exact excerpt of the changed sentence. Round2 selected that skill with verify_before_finish=false. Link to preceding decision and execution; no attribution of final-quality gain.

## 67. The next round tests changes to the previous selection.

Recursive self-improvement here means that an agent evaluates executions of a harness, proposes revisions, and later examines work done under the selected revision. The retained lesson supplies context for the next attempt. The language model’s weights never change. Our workshop carries a selected harness between two tasks; the upstream Harness² procedure has a broader recursion and experience-library design.

## 68. Freeze three harnesses for the fresh-case comparison.

Final cases: already-refunded, two-invoices, onboarding-recovery, clarify-access. Their files are public for teaching but are excluded from improvement context. The starting version is the configured tested employee, not the deliberately blank opening illustration.

## 69. Compare all three versions on fresh tickets.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze versions and run 12 evaluations.

## 70. Open the execution behind a saved evaluation row.

Actual native W&B Table, not EvalTables and not a three-version aligned comparison. error=0 means the independent account-state check passed. judge_grounded and judge_complete are separate scores. The evaluation row also links execution evidence. All three versions are compared on the next result table. Native EvalTables remains unavailable with HTTP500.

## 71. Link the Report’s conclusion to its runs and traces.

Use fresh v030 final table: all12 account checks and explanation judgments are available and pass. Native EvalTables unavailable; screenshot is the actual W&B/Weave/Report surface and must be captioned accordingly.

## 72. All three harnesses passed the four final cases.

Read the account and explanation columns before the tool-call totals. All versions passed all four cases in this scripted rehearsal, so neither revision increased the measured pass rate. Each revised version made one additional tool call overall. These four cases do not establish repeatability or performance on other workflows. The source is evidence/v030-pending-rehearsal.json.

## 73. Save the case, harness, execution, and scoring records.

Artifacts are versioned file bundles. Trace export, result publication and execution have separate statuses. A publication retry uses saved work and must not make another model request.

## 74. Write down what changed and whether it helped.

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Publish my conclusion with the comparison and evidence.

## 75. Ask ARIA to compare one case across harness versions.

Do not imply ARIA authored these prior results. The prompt asks for evidence analysis, not permission to run new experiments or change budgets.

## 76. Choose a workflow with an observable result to test.

Ask participants to name one workflow in their product with observable output and a check they can run independently of the agent. Have them specify a development case, a likely failure, and a fresh case for testing transfer. They can reuse the instrumentation and improvement controller, but must define what correct work means for that workflow.

## 77. Worked answer · invoice lookup

Exact semantics of teaching.ANSWERS tool. Keep optional so participants attempt the gap first.

## 78. Worked answer · observation handoff

Exact answer contract from teaching.py. Both dispatch paths return state/result. Handoff creates a new list.

## 79. Worked answer · inspect the refund

The learner check is deliberately limited. Do not describe it as the full final scorer.

## 80. Worked answer · validate the judge response

Exact semantics of teaching.ANSWERS scorer validation. Boolean strings are invalid. Empty reasons are invalid. Missing judgments stay unavailable.

## 81. Source, notebook, and recorded example

The product evidence in this deck uses the v030 rehearsal. Native EvalTables returned HTTP500; W&B and Weave records are saved. Current authored notebook source scripts/pending_cells.py. Historical deck preserved outside current attendee path.
