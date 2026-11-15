# Pending, Inc. presenter notes

One four-hour session, including breaks at 1:10–1:20 and 2:15–2:25.

## 1. Please improve yourself.

Understand the task and harness · 0–20 minutes

We will implement an agent that can inspect an account, refund a duplicate charge, and provision access. Then we will instrument and evaluate its work before asking an editor agent to revise its instructions. Pending, Inc. and its accounts are fictional; the Python tools, model requests, traces, and evaluations run in your own project.

## 2. You’re adding an agent to the support team.

Understand the task and harness · 0–20 minutes

Set the context before naming the harness. We are building a support agent that can change account state, so a plausible reply is not enough. The company and customer accounts are fictional. The Python operations, model requests, traces, and checks are real workshop code. The one-page handbook is an opening illustration, not the measured starting harness. Participants will build and test the starting version before comparing changes.

## 3. Acme wants a duplicate $49 charge refunded.

Understand the task and harness · 0–20 minutes

Source: cases.py, double-charge. Its mission explicitly says to keep pay-1 and refund the duplicate. Both pay-1 and pay-2 are captured 4900-cent payments for inv-1, and refunds starts empty. Ask what must be read before changing anything: the account identity, invoice identity, payment identity and existing refunds. Another account also has inv-1, so searching by invoice alone is insufficient. No real payment service is connected.

## 4. Check the account after the agent says it has finished.

Understand the task and harness · 0–20 minutes

Read the desired outcome from left to right. The tool appends one full 4900-cent refund for pay-2. Both captured payment records remain; there is no modeled account balance or payment deletion. The independent scorer compares the whole resulting account with the expected account and checks that the requested work was completed. A separate LLM judge compares the employee’s explanation with its recorded actions. A reply saying the refund is complete cannot create a missing refund or excuse a duplicate. These are expected fixture states, not recorded performance results.

## 5. Fern needs Alex added to its account.

Understand the task and harness · 0–20 minutes

Source: cases.py, missing-seat, and simulator.py, provision_timeout_after_commit. Fern starts active and paid, with members empty. The requested email is alex@example.test and the requested role is member. The first provisioning write commits before the injected timeout is returned. From the timeout alone, the agent cannot establish whether access exists; onboarding_status can read the account. The expected final state contains exactly one matching membership, with unrelated state unchanged. This is a separate development case from Acme, not the same account continued into another task. The later MCP and timeout exercises show the implementation and recovery choices.

## 6. Our dataset is six tickets with resettable account records.

Understand the task and harness · 0–20 minutes

The dataset is executable teaching fixtures in cases.py, not a collection of historical customer chats. The two development cases let us explain and test the mechanics. The four final cases vary the billing or access situation; their expected outcomes and grader output stay outside improvement prompts. Source files are public, so learners can inspect them, but the final comparison is only informative if we stop choosing edits before running it. Every candidate starts with the same initial account state; one candidate’s refund cannot carry into another candidate’s test. We will first write an instruction change ourselves, then ask an editor agent to propose and test alternatives. The research question in this small workshop is whether those changes affect correct work on fresh tickets. Six cases do not establish production reliability.

## 7. Implement the agent, evaluate it, then test harness changes.

Understand the task and harness · 0–20 minutes

One four-hour session. The schedule includes two ten-minute breaks and hands-on coding. Foundations precede implementation; worked answers are linked for help, not additional required work. Allow final comparisons to finish from saved stages if provider latency is high. Never call a replay the attendee's execution.

## 8. The harness builds the request the model receives.

Understand the task and harness · 0–20 minutes

Point to the system text, tool guide, installed skill names and customer ticket. Ask which item would change if the participant edited instructions. A skill name advertises a procedure; its contents have not yet entered the request.

## 9. Python executes the action and returns its result.

Understand the task and harness · 0–20 minutes

Keep the request in place. Reveal the selected action and the Python dispatcher. The model produces JSON; the runtime decides which function to call. Follow the returning arrow to my_observation. This is the mechanism we will implement, not a provider-native function-calling example.

## 10. Different edits change different parts of the agent.

Understand the task and harness · 0–20 minutes

Use the table to distinguish behavior changes. The model is fixed; it is not retrained when instructions change. The learner develops tools and the loop before the baseline. The later editor cannot rewrite those frozen functions. Ask whether editing an unused skill can explain a changed outcome.

## 11. Copy the notebook into your own project.

Connect and instrument · 20–40 minutes

Use the current template, never the historical November 12 gateway notebook. An external account requires its own project, notebook compute access and inference access. Setup does not issue a model request.

## 12. The same notebook runs on a laptop.

Connect and instrument · 20–40 minutes

These commands correspond to the kit README and locked pending extra. Do not send participants to old start.py or office_notebook.py. Inference uses their own access and billing. Windows supports the same uv commands.

## 13. Check where your work will be saved.

Connect and instrument · 20–40 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Check my project and restore saved work.

## 14. Save an operation’s inputs, output, and timing.

Connect and instrument · 20–40 minutes

The event helper runs the supplied function and returns two objects. result is what the caller needs; record describes the operation with its arguments, output, timing, and any error. We save that record before exporting a trace. If export fails, we can send the saved record again without repeating a refund or another model request.

## 15. Export the saved operation as an Agent Lens span.

Connect and instrument · 20–40 minutes

Map each field to the record from the previous slide. Tool creates a span with the operation name, inputs, output, and timestamps; record_error attaches the recorded failure. This function exports an event that already happened. The full notebook function returns its span identity so the execution can link back to Agent Lens.

## 16. Add an environment field and inspect it in Agent Lens.

Connect and instrument · 20–40 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Run this check and verify my Agent Lens trace.

## 17. Inspect the account requested by this tool call.

Connect and instrument · 20–40 minutes

Verified v0.3.0 baseline billing tool span get_account. The model chose get_account in this run; do not claim it chose the learner-authored lookup_invoice. Local checks exercise that authored tool separately. This early screenshot teaches the native inspection surface; participants should open their own setup trace.

## 18. Check which account records the model received.

Connect and instrument · 20–40 minutes

Enlarged native crop x580,y245,w690,h445. Saved get_account, not lookup_invoice. Do not infer that the model called the authored lookup tool; this example teaches the same span fields participants instrumented.

## 19. The tool reads one invoice from one account.

Implement the tool and observation handoff · 40–70 minutes

The case is simulated but the logic is ordinary application code. Another account also has inv-1, so filtering payments without selecting the account is a real mistake the checks can catch.

## 20. Write the invoice lookup.

Implement the tool and observation handoff · 40–70 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my invoice lookup.

## 21. Connect the action schema to your Python function.

Implement the tool and observation handoff · 40–70 minutes

The model sees an action schema that names lookup_invoice and its account_id and invoice_id arguments. That schema alone cannot read an account. Your dispatch function connects the selected name to the Python implementation. This workshop uses local Python for the tool and real local MCP for onboarding.

## 22. Start with the customer’s request.

Implement the tool and observation handoff · 40–70 minutes

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 23. The model chooses an action and its arguments.

Implement the tool and observation handoff · 40–70 minutes

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 24. Your dispatcher calls the Python function.

Implement the tool and observation handoff · 40–70 minutes

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 25. The function returns the account records.

Implement the tool and observation handoff · 40–70 minutes

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 26. Put those records into the next request.

Implement the tool and observation handoff · 40–70 minutes

Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.

## 27. Dispatch lookup_invoice to your function.

Implement the tool and observation handoff · 40–70 minutes

Trace two inputs through this function. lookup_invoice calls the participant function and returns the same world with its lookup result. get_account takes the existing call_tool path. Both return a pair of account state and observation, so the caller can append the observation consistently. A write tool may return changed state.

## 28. Append the action and its result to the next request.

Implement the tool and observation handoff · 40–70 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my tool-to-model handoff.

## 29. Include the tool observation in the conversation history.

Implement the tool and observation handoff · 40–70 minutes

The model cannot see a Python return value unless the executor includes it in a later request. Append the chosen action and its result to a new list so the previous request stays available for inspection. This executor uses JSON actions and a user message containing the observation; it is not using the OpenAI tool-message protocol.

## 30. A tool result changes the next request, not the weights.

Implement the tool and observation handoff · 40–70 minutes

Ask a participant to locate the returned payments in the saved next request. This is in-context information available to the next model call. No optimizer or weight update occurs. Reuse this distinction when we introduce the editor.

## 31. Test the starting harness on billing and onboarding.

Implement the tool and observation handoff · 40–70 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze this executor and run the two starting tickets.

## 32. Take ten minutes before investigating the timeout.

Break · 70–80 minutes

Save at 70 minutes. The first break occurs after the two starting cases. Leave the project and next step visible. Reopening the notebook does not execute either case again.

## 33. Record each model request and its response.

Inspect MCP and recover from a timeout · 80–105 minutes

The LLM span records the requested and returned model identities, input and output messages, timing, settings, and available usage. Entering the span context creates and closes the recorded span; constructing the object alone is insufficient. Open my_model_span for the full message mapping and usage handling; this slide abbreviates the comprehensions. Add usage only when the provider returned it. In Agent Lens, find the request after an account lookup and verify that its input contains the returned payments.

## 34. The executor starts a local MCP session.

Inspect MCP and recover from a timeout · 80–105 minutes

MCP is the interface between this Python client and the onboarding service. Here the service is a local subprocess communicating over stdio. There is no gateway or remote Sandbox requirement. A new action starts a session against the saved office state.

## 35. Discovery returns tool names and input schemas.

Inspect MCP and recover from a timeout · 80–105 minutes

list_tools returns the actual schema for onboarding_status and provision_member. The discover_onboarding action exposes those records to the model. A schema describes accepted arguments; it does not grant access or execute a write.

## 36. Call the discovered tool with the selected arguments.

Inspect MCP and recover from a timeout · 80–105 minutes

The call supplies account_id, email, role and operation_id. The MCP server calls the same office simulator used in our checks. The simulated write can commit before a timeout result comes back.

## 37. Read the returned observation before deciding what to do next.

Inspect MCP and recover from a timeout · 80–105 minutes

The server returns JSON and saves office.json. The executor reloads that state and my_observation adds the result to the conversation. A timed-out result and unchanged client expectations cannot establish that the server did nothing.

## 38. Discovery and execution are separate client calls.

Inspect MCP and recover from a timeout · 80–105 minutes

This is the exact client control flow inside mcp_action, with the surrounding context managers omitted. Ask which branch can discover tools without invoking a mutation, and which branch parses a tool response. This is explanatory code, not an additional exercise or model call.

## 39. An access request is sent.

Inspect MCP and recover from a timeout · 80–105 minutes

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 40. Provisioning commits before its response times out.

Inspect MCP and recover from a timeout · 80–105 minutes

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 41. Read account access before retrying the write.

Inspect MCP and recover from a timeout · 80–105 minutes

Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.

## 42. A stable operation_id prevents a repeated write.

Inspect MCP and recover from a timeout · 80–105 minutes

In notebook step 3, use the free local timeout practice. Predict the member count, trigger the timeout, and compare reading status with same-ID and new-ID retries. Reset between alternatives. This uses Python only, changes no saved employee run, and makes no model request. Illustration of simulator.execute after a committed provisioning request. The same operation_id and identical arguments return the stored receipt with replayed=true. A new operation_id is a new mutation and can add a duplicate membership. Reusing an ID with different arguments is rejected. The recorded onboarding recovery read status instead of retrying, so this diagram explains tool behavior rather than claiming this branch occurred in that run.

## 43. Repair the retry in Python.

Inspect MCP and recover from a timeout · 80–105 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare the two retry procedures.

## 44. One retry policy changes the account twice.

Inspect MCP and recover from a timeout · 80–105 minutes

Source evidence/pending-retry-repair.json. Both execute the same committed-write timeout from fresh state. Distinguish this participant-written Python repair from the later instructions-only comparison. Ask participants to open their recovery trace and find the repeated operation ID.

## 45. Inspect the timeout and the following status check.

Inspect MCP and recover from a timeout · 80–105 minutes

v0.3.0 skill-loaded onboarding: timeout span 5ddd78b1e9faa2d3; recovery status span e62596437e485145. Ask a learner to find evidence that access exists. Do not infer failure from a red span alone.

## 46. The tool says the write may have committed.

Inspect MCP and recover from a timeout · 80–105 minutes

Crop x580,y423,w690,h280 from the unchanged1280x720 native capture. Follow its conversation link on the preceding slide. The next operation in the saved trace is onboarding_status.

## 47. Check the account and the explanation separately.

Score the work and edit one procedure · 105–135 minutes

The state scorer reads the account after execution and checks facts such as payment identity, refund amount, and duplicate effects. The LLM judge reads the request, actions, and final reply to assess whether the explanation is supported. These can disagree: an agent may do the right work and describe it incorrectly. An unavailable judge response stays missing.

## 48. The same confident reply can accompany four account states.

Score the work and edit one procedure · 105–135 minutes

These are the four free development fixtures from teaching.check_scorer: one 4900-cent refund, a 100-cent refund, no refund, and two 4900-cent refunds. They share the reply Everything is resolved. The displayed PASS/FAIL values are the required deterministic checks, not inferred LLM judgments. Ask which fields my_state_check must read before participants implement it.

## 49. Write checks for full, partial, missing, and duplicate refunds.

Score the work and edit one procedure · 105–135 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my scorer against four known examples.

## 50. The account can contradict a confident reply.

Score the work and edit one procedure · 105–135 minutes

The public partial-refund fixture contains one 100-cent refund, compared with the required 4900 cents. The model's explanation cannot change that state. Read the actual integer comparison before introducing the judge.

## 51. A valid judge response can still contain a wrong judgment.

Score the work and edit one procedure · 105–135 minutes

Work through availability, schema and correctness separately. The validator can reject strings in boolean fields. It cannot prove complete:true is right. For this illustrative partial-refund example it would be wrong. The live judge's actual reason remains the evidence to inspect.

## 52. Ask the judge to compare the reply with recorded actions.

Score the work and edit one procedure · 105–135 minutes

Rubric from current pending_cells.py. Explain why the judge receives task, recorded actions and explanation. Have participants inspect one reason against a real span. Separate grammatical JSON validation from judging quality.

## 53. Publish development results with both kinds of score.

Score the work and edit one procedure · 105–135 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Judge and publish the starting development comparison.

## 54. Know which check produced the score.

Score the work and edit one procedure · 105–135 minutes

The public check_work result can influence the employee. The participant-written scorer teaches a bounded account check. The independent final grader checks complete expected state and the resolution. The explanation judge compares the reply with recorded actions. Its validator checks structure, not correctness. Ask a participant which check an improver is allowed to see.

## 55. An installed skill must be read before it can guide the model.

Score the work and edit one procedure · 105–135 minutes

build_messages lists installed skill names. read_skill returns the file contents, and my_observation appends that result to the next request. Before editing, the notebook shows skill reads from the starting tickets. If there is no read, say so. The optional free example demonstrates the named file, returned text, and next request without pretending that a model chose it. After editing, compare the actual read event and later saved request. No read means we cannot claim the skill influenced this execution. Loading it still does not prove the agent followed it; inspect the subsequent tools.

## 56. Investigate this result

Investigate this result · 117–125 minutes

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 57. Read one claim in the recorded response

Investigate this result · 117–125 minutes

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 58. Open the source and check that claim

Investigate this result · 117–125 minutes

Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 59. Revise the verification skill and rerun both tickets.

Score the work and edit one procedure · 105–135 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Save this procedure and rerun both development tickets.

## 60. Take a ten-minute break after saving your progress.

Break · 135–145 minutes

Second break: 135–145 minutes. Save the manual comparison and return to step 6. Do not start automatic work during the break.

## 61. Management would like to automate management.

Propose, probe and compose · 145–185 minutes

The editor uses the same fixed model, but its request is to revise the harness rather than resolve a customer ticket. We supply the current configuration and a saved execution. The permitted edits are instructions, the verification skill, and bounded workflow rules. Tools and scoring stay fixed so any measured difference concerns the harness we changed.

## 62. Propose two edits to the same starting harness.

Propose, probe and compose · 145–185 minutes

Propose asks the editor for two competing changes, such as clearer verification instructions or a mandatory completion check. A and B start from the same parent. Neither receives the other candidate’s test result at this point. We review their saved configurations before allowing the probes.

## 63. Run each candidate from the original account state.

Propose, probe and compose · 145–185 minutes

If candidate A has already issued a refund, B must not inherit that refunded account. The controller resets the case before each probe. Compare the actions and returned state of both runs; a successful tool response alone does not tell us the ticket was handled correctly.

## 64. Compare the probe results before selecting a harness.

Propose, probe and compose · 145–185 minutes

Compose receives the proposed configurations and both execution records. It can choose A or B, combine parts of them, or retain the parent. Its rationale explains that choice, but the choice still needs an execution. The solid paths show versions; colors identify alternatives rather than scores.

## 65. Execute the harness returned by the composition decision.

Propose, probe and compose · 145–185 minutes

A combination may differ from both tested candidates, so we run the returned configuration as its own probe. A Retain decision also runs through this step without inventing a new executable version. We can then inspect the specific execution associated with the decision.

## 66. Save the selected harness and a lesson for onboarding.

Propose, probe and compose · 145–185 minutes

Reflect asks the editor what it learned from the selected run and where that conclusion may not apply. We keep the lesson with that run, then execute the selected harness on onboarding before proposing more changes. This carried-harness teaching protocol differs from the full upstream Harness² cross-task procedure.

## 67. Give the editor the starting execution and harness.

Propose, probe and compose · 145–185 minutes

Conceptual variable names match the visible controller; actual notebook uses _s,_case,_parent,_prefix,_f. It passes prior_experience from round1 into round2. Ask which input would be inappropriate: final-test scores.

## 68. Review the proposed instruction and workflow changes.

Propose, probe and compose · 145–185 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Ask for two competing changes.

## 69. Construct and execute the proposed harness.

Propose, probe and compose · 145–185 minutes

The editor returns a structured harness in its decision. The controller constructs that harness, executes it on a reset case, and checks the recorded content fingerprint against the decision. That comparison catches running the wrong version. It says nothing about whether the selected instructions are good; the account scorer answers that separately.

## 70. Run both candidates and inspect their tool sequences.

Propose, probe and compose · 145–185 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Review and test candidate A; then candidate B.

## 71. Require a passing check of the current state before finish.

Propose, probe and compose · 145–185 minutes

The loop stores last_check with passed and the digest of world. With verify_before_finish true, finish is rejected if that check is absent, failed, or no longer matches the current state. This is a runtime completion rule. check_work gives public development feedback; the independent final scorer separately checks entire expected accounts and the required resolution.

## 72. This candidate required a check before completion.

Propose, probe and compose · 145–185 minutes

Recorded candidate B changed verify_before_finish from false to true. It produced the explicit check sequence. Spans: rejected finish 9ed1e7824138ec0e, check_work 2d49d1d8d3ddeb5d, accepted finish 3e19e007d013d4d2. This is a behavior change, not yet evidence of better quality.

## 73. The completion gate required a check_work call.

Propose, probe and compose · 145–185 minutes

Crop x580,y251,w690,h185 from the unchanged1280x720 native capture. Gate behavior is confirmed by the subsequent check_work and accepted finish spans, not inferred from the proposal title.

## 74. Compare the added checks with the resulting account state.

Propose, probe and compose · 145–185 minutes

Recorded first-round probe A used the parent harness: get_account, refund_payment, get_account, finish. Probe B used verify_before_finish=true: the same first three calls, a rejected finish, check_work, and an accepted finish. Both independent account checks passed. Tool-call counts are four and six for these development probes, distinct from the later final-evaluation totals. Source: the v0.3.0 rehearsal journal pending/round-1/probe-a and probe-b, linked through the native conversations on the preceding slides.

## 75. The editor retained the parent after comparing the probes.

Propose, probe and compose · 145–185 minutes

Ask learners for their optional A/B/retain reasoning before showing this composition. Their notebook notes are not provided to the editor. Open this saved composition if time allows. The editor’s rationale was that the mandatory gate added work while the parent already produced a correct billing outcome. It retained the parent. The controller still runs the selected configuration because every composition receives a confirming execution, including KEEP. The executable content remains unchanged.

## 76. Test the selected harness before carrying it forward.

Propose, probe and compose · 145–185 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson.

## 77. Save the lesson with the run that supports it.

Propose, probe and compose · 145–185 minutes

Explanatory excerpt, not a drop-in full function. The actual controller falls back to the parent if the chosen execution does not complete. The lesson is agent-authored interpretation backed by a saved run.

## 78. The next task gets the selected procedure and a checked lesson.

Carry a lesson into the next task · 185–210 minutes

A lesson is an agent-written interpretation with a supporting run and limits. It is not a model weight update. We carry the selected harness and lesson into onboarding, while constructing a fresh account state and conversation for that case. The next execution tests whether the lesson transfers.

## 79. Choosing a combination does not test it.

Carry a lesson into the next task · 185–210 minutes

Do not infer that a composition inherits the scores of its ingredients. The combined behavior can differ, so the controller runs it before adoption. The recorded round-one decision retained the parent instead; the previous slides show its reason and execution.

## 80. Use the selected harness to start the onboarding round.

Carry a lesson into the next task · 185–210 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 2 · Ask for two competing changes; follow the current action.

## 81. The second round changed the verification skill.

Carry a lesson into the next task · 185–210 minutes

In the recorded onboarding round, the editor selected a more specific verification skill while leaving verify_before_finish off. Open the decision to read its rationale, then the chosen execution to inspect how the agent used those files. The next slide shows the exact changed sentence.

## 82. The skill makes the final check more specific.

Carry a lesson into the next task · 185–210 minutes

Source .workshop/v030-pending/journal.json, pending/round-1/compose and pending/round-2/compose verification_skill. Display is an exact excerpt of the changed sentence. Round2 selected that skill with verify_before_finish=false. Link to preceding decision and execution; no attribution of final-quality gain.

## 83. The next round tests changes to the previous selection.

Carry a lesson into the next task · 185–210 minutes

Recursive self-improvement here means that an agent evaluates executions of a harness, proposes revisions, and later examines work done under the selected revision. The retained lesson supplies context for the next attempt. The language model’s weights never change. Our workshop carries a selected harness between two tasks; the upstream Harness² procedure has a broader recursion and experience-library design.

## 84. Freeze three harnesses for the fresh-case comparison.

Evaluate frozen harnesses · 210–230 minutes

Final cases: already-refunded, two-invoices, onboarding-recovery, clarify-access. Their files are public for teaching but are excluded from improvement context. The starting version is the configured tested employee, not the deliberately blank opening illustration.

## 85. Compare all three versions on fresh tickets.

Evaluate frozen harnesses · 210–230 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze versions and run 12 evaluations.

## 86. Compare the same ticket in Forge.

Evaluate frozen harnesses · 210–230 minutes

Click Compare in EvalTables beside the notebook result. This opens the native Weave-backed Evaluation Tables Preview in the W&B workspace. The separate CES EvalTables v2 service can still be unavailable; its status does not erase this working comparison. These are saved rehearsal executions, not new model calls.

## 87. Inspect a request that needs clarification.

Evaluate frozen harnesses · 210–230 minutes

Select the same case across versions. A tie is a result: more verification calls can leave account quality unchanged. Blank judgment cells remain missing. Use the Agent Lens URL saved in that row, rather than an unrelated trace.

## 88. Link the Report’s conclusion to its runs and traces.

Evaluate frozen harnesses · 210–230 minutes

Use fresh v030 final table: all12 account checks and explanation judgments are available and pass. The Report screenshot is the actual W&B/Weave/Report surface. The preceding slides show the repaired native Evaluation Tables Preview comparison.

## 89. All three harnesses passed the four final cases.

Evaluate frozen harnesses · 210–230 minutes

Read the account and explanation columns before the tool-call totals. All versions passed all four cases in this scripted rehearsal, so neither revision increased the measured pass rate. Each revised version made one additional tool call overall. These four cases do not establish repeatability or performance on other workflows. The source is evidence/v030-pending-rehearsal.json.

## 90. Save the case, harness, execution, and scoring records.

Evaluate frozen harnesses · 210–230 minutes

Artifacts are versioned file bundles. Trace export, result publication and execution have separate statuses. A publication retry uses saved work and must not make another model request.

## 91. Check our conclusion

Check our conclusion · 230–237 minutes

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 92. Read one claim in the recorded response

Check our conclusion · 230–237 minutes

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 93. Open the source and check that claim

Check our conclusion · 230–237 minutes

Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/pending_inc/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.

## 94. Write down what changed and whether it helped.

Explain the result · 230–240 minutes

Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Publish my conclusion with the comparison and evidence.

## 95. Choose a workflow with an observable result to test.

Explain the result · 230–240 minutes

Ask participants to name one workflow in their product with observable output and a check they can run independently of the agent. Have them specify a development case, a likely failure, and a fresh case for testing transfer. They can reuse the instrumentation and improvement controller, but must define what correct work means for that workflow.

## 96. Worked answer · invoice lookup

Worked answers · 240–240 minutes

Exact semantics of teaching.ANSWERS tool. Keep optional so participants attempt the gap first.

## 97. Worked answer · observation handoff

Worked answers · 240–240 minutes

Exact answer contract from teaching.py. Both dispatch paths return state/result. Handoff creates a new list.

## 98. Worked answer · inspect the refund

Worked answers · 240–240 minutes

The learner check is deliberately limited. Do not describe it as the full final scorer.

## 99. Worked answer · validate the judge response

Worked answers · 240–240 minutes

Exact semantics of teaching.ANSWERS scorer validation. Boolean strings are invalid. Empty reasons are invalid. Missing judgments stay unavailable.

## 100. Source, notebook, and recorded example

Worked answers · 240–240 minutes

The product evidence in this deck uses the v030 rehearsal. The current native comparison uses Weave-backed Evaluation Tables Preview. The separate CES v2 service still returns HTTP500; its unavailable status remains in publication details. Current authored notebook source scripts/pending_cells.py. Historical deck preserved outside current attendee path.
