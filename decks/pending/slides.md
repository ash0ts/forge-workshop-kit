---
theme: default
title: Please improve yourself · Pending, Inc.
author: Anish Shah
info: Build, instrument, evaluate and improve an agent in your own Forge project.
class: cover
aspectRatio: 16/9
canvasWidth: 1280
colorSchema: light
transition: fade
fonts:
  sans: IBM Plex Sans
  mono: IBM Plex Mono
  provider: none
mdc: true
highlighter: shiki
lineNumbers: false
drawings:
  enabled: false
exportFilename: pending-inc
---
# Please improve<br>yourself.

<div class="sub">Implement a billing agent, instrument its actions,<br>and test changes proposed by an editor agent.</div>
<OfficeScene mode="employee" />
<div class="bottom-note" style="color:#bbd4cb">A three-hour Python workshop at Pending, Inc.</div>

<!--
We will implement an agent that can inspect an account, refund a duplicate charge, and provision access. Then we will instrument and evaluate its work before asking an editor agent to revise its instructions. Pending, Inc. and its accounts are fictional; the Python tools, model requests, traces, and evaluations run in your own project.
-->

---
class: opening-story
---

# Your first morning at Pending, Inc.

<div class="arrival-scene"><div class="scene-prose"><p>Pending, Inc. is our fictional SaaS company. Your team is adding an agent to billing and account support.</p><p class="spoken">“Our first fully autonomous employee.”</p><p>The manager calls it autonomous. So far, the team has supplied this handbook.</p></div><div class="scene-props"><OfficeScene mode="employee" /><div class="handbook-page"><span class="prop-label">EMPLOYEE HANDBOOK · PAGE 1 OF 1</span><p>Be helpful.<br>Use good judgment.</p></div></div></div>

<!--
Pending, Inc. is a teaching setting for a familiar engineering problem: connecting a model to existing application operations. The handbook is an opening illustration. We will build and test a configured starting harness before comparing any revisions.
-->

---
class: opening-story
---

# The customer was charged twice.

<div class="first-ticket-scene"><div class="customer-note"><div class="prop-label">ACME → BILLING</div><h2>Two $49 payments for invoice inv-1</h2><p>Please refund the duplicate $49 charge.</p></div><div class="scene-prose"><p class="spoken">“Can I see the invoice?”</p><div class="empty-tool-menu"><span>Available tools</span><code>[]</code></div><p>To answer the request, the agent needs account records and a tool that can issue a refund.</p></div></div>

<!--
Read the customer request and ask what the agent must know before issuing a refund. The development fixture contains two captured 4900-cent payments on Acme invoice inv-1. The correct outcome refunds pay-2 once while preserving pay-1 and the other account. The empty tool menu explains what we need to implement; it is an illustration rather than a recorded model failure.
-->

---
---

# Define the account state a correct refund should leave.

<AccountLedger />

<!--
Ask someone to name the account fields they would check after this request. We need to identify the correct payment, refund the full amount once, and preserve unrelated state. We will later use partial refunds, duplicate refunds, and false completion claims to test the scorer. A fluent final reply cannot establish these account facts.
-->

---
---

# The access request has no acknowledgement.

<div class="two-col"><div class="ticket"><div class="account">FERN → ACCOUNT SUPPORT</div><p>Add alex@example.test<br>with the member role.</p></div><div class="ticket"><div class="account">RESPONSE</div><p>Request timed out.</p><p>Did access fail, or did the reply fail?</p></div></div><div class="bottom-note">Second public development ticket. One membership is the required result; account state will tell us whether the write succeeded.</div>

<!--
Introduce the second office task before the protocol details. Billing asks us to choose the right payment and act once. Onboarding asks us to handle uncertainty after a write. Both need tools, readable traces and checks on the resulting account. The injected timeout is a fictional teaching incident implemented in the simulator.
-->

---
class: opening-bridge
---

# Your manager has one more request.

<p class="manager-request">“Once it works, could it improve itself?”</p>
<p class="story-to-code">We’ll first implement the tools and the code that passes their results back to the model. With traces and scoring in place, we can ask an editor agent to propose two changes and test whether they improve the same task.</p>
<div class="bottom-note">The editor changes the harness. The model and the scoring rules remain fixed.</div>

<!--
We will first make the agent executable and observable. Once we can inspect a run and score its outcome, we can give those same records to an editor agent. It changes instructions and selected workflow settings, while our tested tools and final scorer remain fixed. That lets us compare the proposed procedures under the same conditions.
-->

---
---

# Implement the agent, evaluate it, then test harness changes.

<div class="current-plan"><div>0–55 min<small>Connect, trace, implement the tool and agent handoff</small></div><div>55–105 min<small>Investigate recovery, score the work, make one edit</small></div><div>105–115 min<small>Break; resume from your saved checkpoint</small></div><div>115–180 min<small>Two improvement rounds, fresh tickets, conclusion</small></div></div>
<div class="bottom-note">Each exercise names the function to edit, the control to run, and the result to inspect.</div>

<!--
This is the three-hour Pending schedule. Allow 15 minutes at the end for final comparison and discussion. Keep extra implementation detail in worked answers.
-->

---
---

# The executor dispatches the model’s selected action.

<HarnessMap :level="0" />
<div class="bottom-note">The executor sends the request and conversation history to the model, then dispatches its chosen action.</div>

<!--
For this ticket, the model might choose lookup_invoice, then refund_payment. It returns an action name and arguments. Python decides which function handles that action, and the tool changes the simulated account. The model does not directly mutate the account dictionary.
-->

---
---

# Instructions define how the agent should handle the ticket.

<HarnessMap :level="1" />
<div class="bottom-note">The harness supplies task rules, available tools, and the code that passes observations back to the model.</div>

<!--
The harness is the code and instructions around the model. It controls the request we send, the actions we allow, and the checks we require. We can revise these pieces while using the same model. In our comparison, the dispatcher and tools stay fixed after we test them.
-->

---
---

# Reading a skill adds its procedure to the conversation.

<HarnessMap :level="2" />
<div class="bottom-note">The verification skill tells the agent what to inspect before it reports completion.</div>

<!--
A saved skill has no effect until the executor supplies it to the model. Here the agent can call read_skill; the returned procedure enters the same conversation as other tool results. Agent Lens lets us check whether the skill was read and what the model did afterward.
-->

---
---

# Copy the notebook into your own project.

<div class="copy-layout"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view"><img style="width:210px" src="/images/pending-template-qr.svg" alt="QR code for the current Pending template"></a><ol><li>Open <a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view">Pending, Inc. in Forge</a>.</li><li>Choose <strong>Copy to project</strong> and select a project you can write to.</li><li>Open the copy in <strong>Edit</strong>. The notebook detects its destination. Run all stale cells once to initialize the controls.</li></ol></div>
<div class="bottom-note">Runs and traces are published to the copied notebook’s project using your Forge account.</div>

<!--
Use the current template, never the historical November 12 gateway notebook. An external account requires its own project, notebook compute access and inference access. Setup does not issue a model request.
-->

---
---

# The same notebook runs on a laptop.

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra pending
uv run --extra pending wandb login --verify
uv run --extra pending marimo edit notebooks/pending_inc.py
```

Enter `YOUR_ENTITY/YOUR_PROJECT` in the notebook.

<div class="bottom-note">Local Python and local MCP run the office tools. You do not need Docker or remote Sandboxes.</div>

<!--
These commands correspond to the kit README and locked pending extra. Do not send participants to old start.py or office_notebook.py. Inference uses their own access and billing. Windows supports the same uv commands.
-->

---
class: exercise
---

# Check where your work will be saved.

<div class="where">Notebook · 1 · Connect and trace</div>

<div class="task">Check the detected project. Choose your inference allowance, which defaults to $8. Notebook compute is billed separately.</div>

<div class="done"><strong>Run:</strong> Check my project and restore saved work<br><strong>Check:</strong> Your project is correct. Read the separate access, tracing, and publication statuses.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Check my project and restore saved work.
-->

---
---

# Save an operation’s inputs, output, and timing.


```python
result, record = event(
    "inspect_notebook", {},
    lambda: {"python": platform.python_version()},
)
```

<ReceiptFlow />

<!--
The event helper runs the supplied function and returns two objects. result is what the caller needs; record describes the operation with its arguments, output, timing, and any error. We save that record before exporting a trace. If export fails, we can send the saved record again without repeating a refund or another model request.
-->

---
---

# Export the saved operation as an Agent Lens span.


```python {1-3|4-7|8-10|all}
with tracing.Tool(
    name=record["name"],
    arguments=record["arguments"],
    result=record["result"],
    tool_call_id=record["id"],
    started_at=stamp(record["started_at"]),
    ended_at=stamp(record["ended_at"]),
) as span:
    if record.get("error"):
        span.record_error(RuntimeError(record["error"]))
```

<div class="bottom-note"><code>my_tool_span</code> turns this saved record into a tool span. Export can be retried without repeating the operation.</div>

<!--
Map each field to the record from the previous slide. Tool creates a span with the operation name, inputs, output, and timestamps; record_error attaches the recorded failure. This function exports an event that already happened. The full notebook function returns its span identity so the execution can link back to Agent Lens.
-->

---
class: exercise
---

# Add an environment field and inspect it in Agent Lens.

<div class="where">Notebook · 1 · Connect and trace</div>

<div class="task">In the inspect_notebook operation, return one more environment field. Read my_tool_span and my_model_span to see how operations become spans.</div>

<div class="done"><strong>Run:</strong> Run this check and verify my Agent Lens trace<br><strong>Check:</strong> Open inspect_notebook. Find your field and compare its value with the returned dictionary.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Run this check and verify my Agent Lens trace.
-->

---
---

# Inspect the account requested by this tool call.

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c2458ce8b6bb52274d29b5c5a691424b" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-lookup.png" alt="The recorded get_account call requests Acme and returns its account records."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · The recorded get_account call requests Acme and returns its account records. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c2458ce8b6bb52274d29b5c5a691424b">Open the record ↗</a></div></div>

<!--
Verified v0.3.0 baseline billing tool span get_account. The model chose get_account in this run; do not claim it chose the learner-authored lookup_invoice. Local checks exercise that authored tool separately. This early screenshot teaches the native inspection surface; participants should open their own setup trace.
-->

---
---

# Check which account records the model received.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-lookup.png" :x="580" :y="245" :width="690" :height="445" :markers="[{number:1,y:315},{number:2,y:455}]" label="Native get_account span: account_id acme and returned account with payment pay-1" /><div class="annotations numbered"><p><span class="annotation-number">1</span><code>arguments</code> supplied <code>account_id: acme</code>.</p><p><span class="annotation-number">2</span><code>result</code> contains that account and its payments.</p><p>Use the next model span to check whether its input contains this observation.</p></div></div>

<!--
Enlarged native crop x580,y245,w690,h445. Saved get_account, not lookup_invoice. Do not infer that the model called the authored lookup tool; this example teaches the same span fields participants instrumented.
-->

---
---

# The tool reads one invoice from one account.

<div class="two-col"><div class="ticket"><div class="account">INPUT</div><p>account_id: acme<br>invoice_id: inv-1</p></div><div class="ticket"><div class="account">EXPECTED RESULT</div><p>pay-1: $49<br>pay-2: $49<br>refunds: []</p></div></div>
<div class="bottom-note">This lookup returns the selected account’s payments and refunds without changing them.</div>

<!--
The case is simulated but the logic is ordinary application code. Another account also has inv-1, so filtering payments without selecting the account is a real mistake the checks can catch.
-->

---
class: exercise
---

# Write the invoice lookup.

<div class="where">Notebook · 2 · Build an invoice tool</div>

<div class="task">Complete my_invoice_tool(state, account_id, invoice_id). Select the account, filter its payments by invoice_id, and return its refunds too.</div>

<div class="done"><strong>Run:</strong> Test my invoice lookup<br><strong>Check:</strong> The requested invoice, missing invoice, and other-account checks pass. Account state stays unchanged.</div>

<a class="answer-link" href="/78">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my invoice lookup.
-->

---
---

# Connect the action schema to your Python function.

<ActionContract />

<!--
The model sees an action schema that names lookup_invoice and its account_id and invoice_id arguments. That schema alone cannot read an account. Your dispatch function connects the selected name to the Python implementation. This workshop uses local Python for the tool and real local MCP for onboarding.
-->

---
---

# Start with the customer’s request.

<ToolLoop :level="1" />

<!--
Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.
-->

---
---

# The model chooses an action and its arguments.

<ToolLoop :level="2" />

<!--
Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.
-->

---
---

# Your dispatcher calls the Python function.

<ToolLoop :level="3" />

<!--
Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.
-->

---
---

# The function returns the account records.

<ToolLoop :level="4" />

<!--
Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.
-->

---
---

# Put those records into the next request.

<ToolLoop :level="5" />

<!--
Same objects and positions across these five frames. Show the actual action/result connection. This is an explanatory diagram based on the public fixture, not a claimed replay of every recorded run.
-->

---
---

# Dispatch lookup_invoice to your function.


```python {1-3|4|all}
def my_dispatch(name, arguments, world, invoice_tool, call_tool):
    if name == "lookup_invoice":
        return world, invoice_tool(world, **arguments)
    return call_tool(world, name, arguments)
```

<div class="bottom-note">Both paths return <code>(world, result)</code>. The invoice path preserves <code>world</code>; write tools may change it.</div>

<!--
Trace two inputs through this function. lookup_invoice calls the participant function and returns the same world with its lookup result. get_account takes the existing call_tool path. Both return a pair of account state and observation, so the caller can append the observation consistently. A write tool may return changed state.
-->

---
class: exercise
---

# Append the action and its result to the next request.

<div class="where">Notebook · 3 · Pass observations to the agent</div>

<div class="task">Complete my_dispatch and my_observation. Append the action and actual result to a new message list, keeping the previous request unchanged.</div>

<div class="done"><strong>Run:</strong> Test my tool-to-model handoff<br><strong>Check:</strong> Open the four handoff tabs. Match the action, Python arguments, returned payments, and two appended messages.</div>

<a class="answer-link" href="/79">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my tool-to-model handoff.
-->

---
---

# Include the tool observation in the conversation history.


```python {1-2|3|all}
return messages + [
    {"role": "assistant", "content": json.dumps(action)},
    {"role": "user", "content": "Tool observation: " + json.dumps(result)},
]
```

<p>The next model request includes both the action it selected and the returned payments. It can use those records to decide which payment to refund.</p>
<div class="bottom-note">The user-role message carries tool data in this JSON protocol. It is not a new customer instruction.</div>

<!--
The model cannot see a Python return value unless the executor includes it in a later request. Append the chosen action and its result to a new list so the previous request stays available for inspection. This executor uses JSON actions and a user message containing the observation; it is not using the OpenAI tool-message protocol.
-->

---
class: exercise
---

# Test the starting harness on billing and onboarding.

<div class="where">Notebook · 3 · Pass observations to the agent</div>

<div class="task">Read the employee instructions, then run the two development cases. We will keep your tested dispatcher and tools fixed while comparing changes to the harness.</div>

<div class="done"><strong>Run:</strong> Freeze this executor and run the two starting tickets<br><strong>Check:</strong> Open a billing run and onboarding run. Follow one tool result into the next model call.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze this executor and run the two starting tickets.
-->

---
---

# Record each model request and its response.


```python {1-5|6-10|11-12|all}
req = record["request"]
response = record.get("response") or {}
span = tracing.LLM(
    model=req["model"],
    response_model=response.get("model", ""),
    input_messages=[...],
    output_messages=[...],
    started_at=stamp(record["started_at"]),
    ended_at=stamp(record["ended_at"]),
)
with span:
    span.set_attributes({"workshop.request_id": record["id"]})
```

<div class="bottom-note">Message lists are abbreviated. <code>my_model_span</code> exports the saved response; it does not call the model again.</div>

<!--
The LLM span records the requested and returned model identities, input and output messages, timing, settings, and available usage. Entering the span context creates and closes the recorded span; constructing the object alone is insufficient. Open my_model_span for the full message mapping and usage handling; this slide abbreviates the comprehensions. Add usage only when the provider returned it. In Agent Lens, find the request after an account lookup and verify that its input contains the returned payments.
-->

---
---

# Provision Alex’s membership through the MCP tools.

<McpSequence />

<!--
Use the local MCP implementation in pending/mcp_server.py. Distinguish actual protocol discovery and invocation from a function merely named MCP. The simulated service deliberately commits a write before returning a timeout in the development incident.
-->

---
---

# An access request is sent.

<TimeoutSequence :level="1" />
<div class="bottom-note">After a timeout, read the account to determine whether the requested membership already exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# Provisioning commits before its response times out.

<TimeoutSequence :level="2" />
<div class="bottom-note">After a timeout, read the account to determine whether the requested membership already exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# Read account access before retrying the write.

<TimeoutSequence :level="3" />
<div class="bottom-note">After a timeout, read the account to determine whether the requested membership already exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# A stable operation_id prevents a repeated write.

<RetryIdentity />

<!--
In notebook step 3, use the free local timeout practice. Predict the member count, trigger the timeout, and compare reading status with same-ID and new-ID retries. Reset between alternatives. This uses Python only, changes no saved employee run, and makes no model request. Illustration of simulator.execute after a committed provisioning request. The same operation_id and identical arguments return the stored receipt with replayed=true. A new operation_id is a new mutation and can add a duplicate membership. Reusing an ID with different arguments is rejected. The recorded onboarding recovery read status instead of retrying, so this diagram explains tool behavior rather than claiming this branch occurred in that run.
-->

---
---

# Inspect the timeout and the following status check.

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/481ae944f1062c5381870a00319f65a3" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-timeout.png" alt="Find provision_member, then inspect onboarding_status."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · Find provision_member, then inspect onboarding_status. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/481ae944f1062c5381870a00319f65a3">Open the record ↗</a></div></div>

<!--
v0.3.0 skill-loaded onboarding: timeout span 5ddd78b1e9faa2d3; recovery status span e62596437e485145. Ask a learner to find evidence that access exists. Do not infer failure from a red span alone.
-->

---
---

# The tool says the write may have committed.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-timeout.png" :x="580" :y="423" :width="690" :height="280" :markers="[{number:1,y:488},{number:2,y:655}]" label="Native timeout output says the operation may have committed; inspect current access" /><div class="annotations numbered"><p><span class="annotation-number">1</span>The arguments identify Fern, Alex, the member role, and the operation ID.</p><p><span class="annotation-number">2</span>The result reports a timeout and says the write may have committed. Read access before another write.</p></div></div><div class="bottom-note">Enlarged native span. The failed response does not establish whether the membership was created.</div>

<!--
Crop x580,y423,w690,h280 from the unchanged1280x720 native capture. Follow its conversation link on the preceding slide. The next operation in the saved trace is onboarding_status.
-->

---
---

# Check the account and the explanation separately.

<ScoringPaths />

<!--
The state scorer reads the account after execution and checks facts such as payment identity, refund amount, and duplicate effects. The LLM judge reads the request, actions, and final reply to assess whether the explanation is supported. These can disagree: an agent may do the right work and describe it incorrectly. An unavailable judge response stays missing.
-->

---
---

# The same confident reply can accompany four account states.

<RefundChecks />

<!--
These are the four free development fixtures from teaching.check_scorer: one 4900-cent refund, a 100-cent refund, no refund, and two 4900-cent refunds. They share the reply Everything is resolved. The displayed PASS/FAIL values are the required deterministic checks, not inferred LLM judgments. Ask which fields my_state_check must read before participants implement it.
-->

---
class: exercise
---

# Write checks for full, partial, missing, and duplicate refunds.

<div class="where">Notebook · 4 · Check the work</div>

<div class="task">Complete my_state_check and my_judge_validation. Require one full 4900-cent refund. Require boolean grounded/complete fields and a nonempty reason from the judge.</div>

<div class="done"><strong>Run:</strong> Test my scorer against four known examples<br><strong>Check:</strong> Full refund passes. Partial refund, no refund, and duplicate refund fail, despite the same confident reply.</div>

<a class="answer-link" href="/80">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my scorer against four known examples.
-->

---
---

# Ask the judge to compare the reply with recorded actions.

<div class="quote">Check each completion claim against recorded tool activity. A timeout is not proof that a write failed. Separate an accurate explanation from a correct account.</div>
<div class="bottom-note">Edit the rubric in the notebook. The response validator checks its shape; it cannot guarantee the judgment is right.</div>

<!--
Rubric from current pending_cells.py. Explain why the judge receives task, recorded actions and explanation. Have participants inspect one reason against a real span. Separate grammatical JSON validation from judging quality.
-->

---
class: exercise
---

# Publish development results with both kinds of score.

<div class="where">Notebook · 4 · Check the work</div>

<div class="task">Run the explanation judge on the two saved starting tickets. Find your state check, the independent check, and the judge reason in the saved table.</div>

<div class="done"><strong>Run:</strong> Judge and publish the starting development comparison<br><strong>Check:</strong> Open a case in the saved comparison and follow its conversation link. Explain any disagreement between the two scores.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Judge and publish the starting development comparison.
-->

---
---

# Know which check produced the score.

<FourChecks />

<!--
The public check_work result can influence the employee. The participant-written scorer teaches a bounded account check. The independent final grader checks complete expected state and the resolution. The explanation judge compares the reply with recorded actions. Its validator checks structure, not correctness. Ask a participant which check an improver is allowed to see.
-->

---
class: exercise
---

# Revise the verification skill and rerun both tickets.

<div class="where">Notebook · 5 · Edit one procedure</div>

<div class="task">Choose the recorded action that prompted your edit. Write a verification procedure explaining what the employee should check or do differently.</div>

<div class="done"><strong>Run:</strong> Save this procedure and rerun both development tickets<br><strong>Check:</strong> Read the diff. Find whether the employee loaded your skill and whether its next tool sequence changed.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Save this procedure and rerun both development tickets.
-->

---
---

# An installed skill must be read before it can guide the model.

<SkillRead />

<!--
build_messages lists installed skill names. read_skill returns the file contents, and my_observation appends that result to the next request. The notebook checks the actual read event and later saved request. No read means we cannot claim the skill influenced this execution. Loading it still does not prove the agent followed it; inspect the subsequent tools.
-->

---
---

# Take a ten-minute break after saving your progress.

<OfficeScene mode="employee" />
<div class="bottom-note">Resume at 6 · Improve twice. Reopening the notebook restores saved work without making model calls.</div>

<!--
Stop at 105 minutes. Use saved checkpoints; opening does not trigger paid work. Have attendees note the next step before the break.
-->

---
---

# Management would like to automate management.

<p class="big">Give the editor the current instructions, verification skill, and execution record. It will propose two alternative harnesses for us to review and test.</p>
<div class="two-col"><div><h2>It may edit</h2><p>Instructions, skills, and bounded workflow rules.</p></div><div><h2>Keep fixed</h2><p>The model, tested tools, fixtures, grader, and budget controls.</p></div></div>
<div class="bottom-note">The notebook controller runs the tests and records which harness the editor chose.</div>

<!--
The editor uses the same fixed model, but its request is to revise the harness rather than resolve a customer ticket. We supply the current configuration and a saved execution. The permitted edits are instructions, the verification skill, and bounded workflow rules. Tools and scoring stay fixed so any measured difference concerns the harness we changed.
-->

---
---

# Propose two edits to the same starting harness.

<ImprovementBranches :level="1" />
<div class="bottom-note">Both candidates receive the parent harness and the same starting execution. Read each diff before testing it.</div>

<!--
Propose asks the editor for two competing changes, such as clearer verification instructions or a mandatory completion check. A and B start from the same parent. Neither receives the other candidate’s test result at this point. We review their saved configurations before allowing the probes.
-->

---
---

# Run each candidate from the original account state.

<ImprovementBranches :level="2" />
<div class="bottom-note">Probe executes A and B separately. Each starts with the same ticket and an unchanged copy of its account.</div>

<!--
If candidate A has already issued a refund, B must not inherit that refunded account. The controller resets the case before each probe. Compare the actions and returned state of both runs; a successful tool response alone does not tell us the ticket was handled correctly.
-->

---
---

# Compare the probe results before selecting a harness.

<ImprovementBranches :level="3" />
<div class="bottom-note">The dashed paths carry test records to Compose, which can select, combine, or retain the parent.</div>

<!--
Compose receives the proposed configurations and both execution records. It can choose A or B, combine parts of them, or retain the parent. Its rationale explains that choice, but the choice still needs an execution. The solid paths show versions; colors identify alternatives rather than scores.
-->

---
---

# Execute the harness returned by the composition decision.

<ImprovementBranches :level="4" />
<div class="bottom-note">The controller constructs the selected harness and runs it before saving it for the next task.</div>

<!--
A combination may differ from both tested candidates, so we run the returned configuration as its own probe. A Retain decision also runs through this step without inventing a new executable version. We can then inspect the specific execution associated with the decision.
-->

---
---

# Save the selected harness and a lesson for onboarding.

<RoundTransfer />
<div class="bottom-note">The next round receives the selected version, its execution record, and the lesson’s stated limits.</div>

<!--
Reflect asks the editor what it learned from the selected run and where that conclusion may not apply. We keep the lesson with that run, then execute the selected harness on onboarding before proposing more changes. This carried-harness teaching protocol differs from the full upstream Harness² cross-task procedure.
-->

---
---

# Give the editor the starting execution and harness.


```python {1|2-4|all}
experience = [run_employee(session, case, parent, prefix + "starting", **hooks)]
editor_decision(
    session, round_number, "propose", parent, experience,
    tool_writer=my_tool_span, model_writer=my_model_span,
)
```

<div class="bottom-note"><code>experience</code> contains the starting run’s actions and results. Final-case grades are excluded from the editor’s request.</div>

<!--
Conceptual variable names match the visible controller; actual notebook uses _s,_case,_parent,_prefix,_f. It passes prior_experience from round1 into round2. Ask which input would be inappropriate: final-test scores.
-->

---
class: exercise
---

# Review the proposed instruction and workflow changes.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Read the visible controller. Ask for two changes, then inspect Candidate A’s diff and rationale. Mark the review checkbox only after reading the files.</div>

<div class="done"><strong>Run:</strong> Round 1 · Ask for two competing changes<br><strong>Check:</strong> The next action is Review and test candidate A. Explain what behavior A is intended to change.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Ask for two competing changes.
-->

---
---

# Construct and execute the proposed harness.


```python {1|2-3|all}
harness = Harness(**decision["harness"])
run = run_employee(session, case, harness, prefix + phase, **hooks)
assert run["harness_fingerprint"] == decision["fingerprint"]
```

<p>Each probe receives a fresh copy of the account state. The fingerprint check verifies that it used the harness returned in the saved decision.</p>
<div class="bottom-note">This tests the proposed configuration; reading its rationale alone cannot establish its effect.</div>

<!--
The editor returns a structured harness in its decision. The controller constructs that harness, executes it on a reset case, and checks the recorded content fingerprint against the decision. That comparison catches running the wrong version. It says nothing about whether the selected instructions are good; the account scorer answers that separately.
-->

---
class: exercise
---

# Run both candidates and inspect their tool sequences.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Review and test A, then review and test B. Follow each result into Agent Lens and look for the behavior its proposal promised.</div>

<div class="done"><strong>Run:</strong> Round 1 · Review and test candidate A; then candidate B<br><strong>Check:</strong> Both started from the same billing state. You can identify which changed files were used in each run.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Review and test candidate A; then candidate B.
-->

---
---

# Require a passing check of the current state before finish.

<CompletionGuard />

<!--
The loop stores last_check with passed and the digest of world. With verify_before_finish true, finish is rejected if that check is absent, failed, or no longer matches the current state. This is a runtime completion rule. check_work gives public development feedback; the independent final scorer separately checks entire expected accounts and the required resolution.
-->

---
---

# This candidate required a check before completion.

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-verification.png" alt="Find the rejected finish, check_work, and accepted finish."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · Find the rejected finish, check_work, and accepted finish. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46">Open the record ↗</a></div></div>

<!--
Recorded candidate B changed verify_before_finish from false to true. It produced the explicit check sequence. Spans: rejected finish 9ed1e7824138ec0e, check_work 2d49d1d8d3ddeb5d, accepted finish 3e19e007d013d4d2. This is a behavior change, not yet evidence of better quality.
-->

---
---

# The completion gate required a check_work call.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-verification.png" :x="580" :y="251" :width="690" :height="185" label="Native finish error: Check the current work before submitting" /><div class="annotations"><p><code>verify_before_finish</code> blocked the first finish.</p><p>The following <code>check_work</code> call satisfied the gate.</p></div></div><div class="bottom-note">The account result still passed. The editor had to decide whether the additional gate was worth keeping.</div>

<!--
Crop x580,y251,w690,h185 from the unchanged1280x720 native capture. Gate behavior is confirmed by the subsequent check_work and accepted finish spans, not inferred from the proposal title.
-->

---
---

# Compare the added checks with the resulting account state.

<ProbeComparison />

<!--
Recorded first-round probe A used the parent harness: get_account, refund_payment, get_account, finish. Probe B used verify_before_finish=true: the same first three calls, a rejected finish, check_work, and an accepted finish. Both independent account checks passed. Tool-call counts are four and six for these development probes, distinct from the later final-evaluation totals. Source: the v0.3.0 rehearsal journal pending/round-1/probe-a and probe-b, linked through the native conversations on the preceding slides.
-->

---
---

# The editor retained the parent after comparing the probes.

<RetainExecution />
<div class="bottom-note"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c04f575608c6f43d99e1b7b428a23791">Read the recorded composition rationale ↗</a></div>

<!--
Open this saved composition if time allows. The editor’s rationale was that the mandatory gate added work while the parent already produced a correct billing outcome. It retained the parent. The controller still runs the selected configuration because every composition receives a confirming execution, including KEEP. The executable content remains unchanged.
-->

---
class: exercise
---

# Test the selected harness before carrying it forward.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Request a composition. Read what it kept or changed, test those files, and save the tested version with its lesson and limits.</div>

<div class="done"><strong>Run:</strong> Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson<br><strong>Check:</strong> The chosen execution matches the decision. If it retained the parent, explain why the files are unchanged.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson.
-->

---
---

# Save the lesson with the run that supports it.


```python {1-4|5-8|all}
review = reflect_execution(
    session, round_number, run,
    tool_writer=my_tool_span, model_writer=my_model_span,
)
adopted = {
    "harness": chosen_harness,
    "lesson": review["lesson"],
    "limits": review["limits"],
    "execution": run["stage_id"],
}
```

<p>The next round receives this selected harness and the saved lesson. Keeping the execution reference lets us inspect the observation behind the editor’s conclusion.</p>

<!--
Explanatory excerpt, not a drop-in full function. The actual controller falls back to the parent if the chosen execution does not complete. The lesson is agent-authored interpretation backed by a saved run.
-->

---
class: exercise
---

# Use the selected harness to start the onboarding round.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Round 2 starts with the version and lesson kept after billing. Propose, review, test, compose, test again, and save the result.</div>

<div class="done"><strong>Run:</strong> Round 2 · Ask for two competing changes; follow the current action<br><strong>Check:</strong> Explain what the previous lesson influenced and what the new execution showed. Do not assume a billing lesson transfers.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 2 · Ask for two competing changes; follow the current action.
-->

---
---

# The second round changed the verification skill.

<div class="two-col"><div><h2>Recorded edit</h2><p>Check that the intended account change exists exactly once and that unrelated state stayed unchanged.</p></div><div><h2>Recorded choice</h2><p>Keep the completion gate off. Use the revised skill with the existing workflow.</p></div></div>
<div class="bottom-note"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a39aede201a0fe7320092976c0501e42">Decision ↗</a> · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/d641da20ff5e553866a93a3c12bee913">Execution of the chosen files ↗</a></div>

<!--
In the recorded onboarding round, the editor selected a more specific verification skill while leaving verify_before_finish off. Open the decision to read its rationale, then the chosen execution to inspect how the agent used those files. The next slide shows the exact changed sentence.
-->

---
---

# The skill makes the final check more specific.

<div class="diff"><div class="del">− Verify the account before claiming completion.</div><div class="add">+ Verify the account before claiming completion: confirm the intended change is present exactly once (no duplicate side effects) and that unrelated payments, memberships, and subscriptions are unchanged.</div></div><div class="bottom-note">Actual changed sentence in the recorded verification skill. The timeout and operation_id instructions above it stayed unchanged.</div>

<!--
Source .workshop/v030-pending/journal.json, pending/round-1/compose and pending/round-2/compose verification_skill. Display is an exact excerpt of the changed sentence. Round2 selected that skill with verify_before_finish=false. Link to preceding decision and execution; no attribution of final-quality gain.
-->

---
---

# The next round tests changes to the previous selection.

<RoundTransfer :recorded="true" />

<!--
Recursive self-improvement here means that an agent evaluates executions of a harness, proposes revisions, and later examines work done under the selected revision. The retained lesson supplies context for the next attempt. The language model’s weights never change. Our workshop carries a selected harness between two tasks; the upstream Harness² procedure has a broader recursion and experience-library design.
-->

---
---

# Freeze three harnesses for the fresh-case comparison.

<EvaluationMatrix />

<!--
Final cases: already-refunded, two-invoices, onboarding-recovery, clarify-access. Their files are public for teaching but are excluded from improvement context. The starting version is the configured tested employee, not the deliberately blank opening illustration.
-->

---
class: exercise
---

# Compare all three versions on fresh tickets.

<div class="where">Notebook · 7 · Compare fresh tickets</div>

<div class="task">Freeze the versions and run the final comparison. Use the saved-ticket selector to align the starting, manual, and agent-selected outputs.</div>

<div class="done"><strong>Run:</strong> Freeze versions and run 12 evaluations<br><strong>Check:</strong> Follow a score to its account state, judge reason, trace, and harness. Keep unavailable judgments separate from wrong answers.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze versions and run 12 evaluations.
-->

---
---

# Open the execution behind a saved evaluation row.

<div class="native-capture"><a class="capture-link" href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/5a3721335363bceb77f0c88c87e761f8"><CaptureDetail src="/images/visual-v030-pending-comparison.png" :x="80" :y="305" :width="1180" :height="380" label="Four saved W&B Table case rows, scores and execution evidence" /></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · W&B Table: four fresh cases for the agent-selected version. · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/5a3721335363bceb77f0c88c87e761f8">Open the record ↗</a></div></div>

<!--
Actual native W&B Table, not EvalTables and not a three-version aligned comparison. error=0 means the independent account-state check passed. judge_grounded and judge_complete are separate scores. The evaluation row also links execution evidence. All three versions are compared on the next result table. Native EvalTables remains unavailable with HTTP500.
-->

---
---

# Link the Report’s conclusion to its runs and traces.

<div class="native-capture"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-report.png" alt="The Report records the complete comparison and its publication status."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · The Report records the complete comparison and its publication status. · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==">Open the record ↗</a></div></div>

<!--
Use fresh v030 final table: all12 account checks and explanation judgments are available and pass. Native EvalTables unavailable; screenshot is the actual W&B/Weave/Report surface and must be captioned accordingly.
-->

---
---

# All three harnesses passed the four final cases.

<EvaluationMatrix :recorded="true" />

<!--
Read the account and explanation columns before the tool-call totals. All versions passed all four cases in this scripted rehearsal, so neither revision increased the measured pass rate. Each revised version made one additional tool call overall. These four cases do not establish repeatability or performance on other workflows. The source is evidence/v030-pending-rehearsal.json.
-->

---
---

# Save the case, harness, execution, and scoring records.

<div class="sequence"><div class="step">Case<small>request + initial state</small></div><div class="arrow">→</div><div class="step">Harness<small>instructions + skill</small></div><div class="arrow">→</div><div class="step">Execution<small>trace + final state</small></div><div class="arrow">→</div><div class="step">Evaluation<small>checks + judge reason</small></div></div>
<p>W&B Artifacts save the exact files as versions. The Report links the explanation to these saved records.</p>

<!--
Artifacts are versioned file bundles. Trace export, result publication and execution have separate statuses. A publication retry uses saved work and must not make another model request.
-->

---
class: exercise
---

# Write down what changed and whether it helped.

<div class="where">Notebook · 8 · Explain the result</div>

<div class="task">Name the edit, the behavior you observed, and the final comparison. Link one trace and one matching case. Suggest the next test.</div>

<div class="done"><strong>Run:</strong> Publish my conclusion with the comparison and evidence<br><strong>Check:</strong> Someone else can open the records behind your conclusion. No higher score is required.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Publish my conclusion with the comparison and evidence.
-->

---
---

# Ask ARIA to compare one case across harness versions.

<div class="quote">Compare my starting and agent-selected harnesses on the same fresh ticket. Use the linked evaluation, execution trace, and harness diff. Explain what changed in behavior and whether the account result changed. Cite the relevant records before suggesting another experiment.</div>
<div class="bottom-note">Optional. Verify one citation yourself. This investigation is outside the measured comparison.</div>

<!--
Do not imply ARIA authored these prior results. The prompt asks for evidence analysis, not permission to run new experiments or change budgets.
-->

---
---

# Choose a workflow with an observable result to test.

<p class="big">Start with a task whose result you can inspect independently: an account update, an access change, or another completed operation.</p>
<p>Record the agent’s actions and define the success checks before asking it to revise its own procedures. Test the revised harness on the same cases, then on cases it has not seen.</p>
<div class="bottom-note">Write down a development case and a different case to hold back for evaluation.</div>

<!--
Ask participants to name one workflow in their product with observable output and a check they can run independently of the agent. Have them specify a development case, a likely failure, and a fresh case for testing transfer. They can reuse the instrumentation and improvement controller, but must define what correct work means for that workflow.
-->

---
class: answer
---

# Worked answer · invoice lookup


```python
def my_invoice_tool(state, account_id, invoice_id):
    account = state["accounts"][account_id]
    return {
        "payments": [p for p in account["payments"]
                     if p["invoice_id"] == invoice_id],
        "refunds": account["refunds"],
    }
```

Select the account first. Filter its payments. The returned value does not mutate state.

<span class="source-link"><a href="/20">Return to the exercise →</a></span>

<!--
Exact semantics of teaching.ANSWERS tool. Keep optional so participants attempt the gap first.
-->

---
class: answer
---

# Worked answer · observation handoff


```python
def my_dispatch(name, arguments, world, invoice_tool, call_tool):
    if name == "lookup_invoice":
        return world, invoice_tool(world, **arguments)
    return call_tool(world, name, arguments)

def my_observation(messages, action, result):
    return messages + [
        {"role": "assistant", "content": json.dumps(action)},
        {"role": "user", "content": "Tool observation: " + json.dumps(result)},
    ]
```

<span class="source-link"><a href="/28">Return to the exercise →</a></span>

<!--
Exact answer contract from teaching.py. Both dispatch paths return state/result. Handoff creates a new list.
-->

---
class: answer
---

# Worked answer · inspect the refund


```python
if run["case_id"] == "double-charge":
    refunds = run["world"]["accounts"]["acme"]["refunds"]
    return len(refunds) == 1 and refunds[0]["amount_cents"] == 4900
```

This development check distinguishes the four public examples. The trusted final scorer also checks the target payment and unrelated account state.

<span class="source-link"><a href="/81">Continue to judge validation →</a></span> · <span class="source-link"><a href="/41">Return to exercise →</a></span>

<!--
The learner check is deliberately limited. Do not describe it as the full final scorer.
-->

---
class: answer
---

# Worked answer · validate the judge response


```python
def my_judge_validation(answer):
    if any(type(answer.get(k)) is not bool
           for k in ("grounded", "complete")):
        raise ValueError("grounded and complete must be booleans")
    if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
        raise ValueError("The judge must explain its answer")
    return answer
```

Valid JSON can still contain an incorrect judgment. Compare the reason with the recorded work.

<span class="source-link"><a href="/41">Return to the exercise →</a></span>

<!--
Exact semantics of teaching.ANSWERS scorer validation. Boolean strings are invalid. Empty reasons are invalid. Missing judgments stay unavailable.
-->

---
---

# Source, notebook, and recorded example

<div class="sources"><p><a href="https://github.com/ash0ts/forge-workshop-kit">Workshop Kit source and setup</a><br><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view">Copy the current Pending notebook</a><br><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==">Recorded v0.3.0 rehearsal Report</a><br><a href="https://docs.coreweave.com/products/agent-lens">Agent Lens documentation</a><br><a href="https://docs.coreweave.com/products/wandb/evaltables/compare-runs">Native EvalTables comparison guide</a><br><a href="https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335">Pinned Harness² upstream</a></p></div>

<!--
The product evidence in this deck uses the v030 rehearsal. Native EvalTables returned HTTP500; W&B and Weave records are saved. Current authored notebook source scripts/pending_cells.py. Historical deck preserved outside current attendee path.
-->
