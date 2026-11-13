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

<div class="sub">Build an agent for billing and onboarding.<br>Then test changes to its harness.</div>
<OfficeScene mode="employee" />
<div class="bottom-note" style="color:#bbd4cb">A three-hour workday at Pending, Inc.<br>Management has supplied a motivational paragraph.</div>

<!--
Welcome. We will write the pieces of an agent and then give another agent permission to edit some of them. The office is fictional. Model and tool executions later in the workshop are real.
-->

---
class: opening-story
---

# Your first morning at Pending, Inc.

<div class="arrival-scene"><div class="scene-prose"><p>Your manager introduces your new colleague.</p><p class="spoken">“Our first fully autonomous employee.”</p><p>It handles billing and account access. Its equipment is a one-page handbook.</p></div><div class="scene-props"><OfficeScene mode="employee" /><div class="handbook-page"><span class="prop-label">EMPLOYEE HANDBOOK · PAGE 1 OF 1</span><p>Be helpful.<br>Use good judgment.</p></div></div></div>

<!--
Read the manager line dryly. The participant is the person arriving; the employee is the agent. This illustrative handbook is not the actual baseline prompt.
-->

---
class: opening-story
---

# The customer was charged twice.

<div class="first-ticket-scene"><div class="customer-note"><div class="prop-label">ACME → BILLING</div><h2>Two payments. One invoice.</h2><p>Please refund the duplicate $49 charge.</p></div><div class="scene-prose"><p class="spoken">“Can I see the invoice?”</p><div class="empty-tool-menu"><span>Available tools</span><code>[]</code></div><p>You pull up a chair. First, give the employee a way to look it up.</p></div></div>

<!--
Fictional dialogue illustrating the real public double-charge fixture. There are two captured 4900-cent payments on inv-1. It must refund pay-2 while preserving pay-1 and the other account. Do not describe this scene as a measured model failure.
-->

---
---

# What would count as doing the job?

<div class="result-grid"><div class="claim">“All sorted. Thanks for your patience.”<p class="quiet">A fluent reply is one observable output.</p></div><div class="state"><strong>Check the account too.</strong><p>Refund the duplicate once.<br>Use the right account.<br>Leave unrelated records alone.</p></div></div>
<div class="bottom-note">We will compare what the employee says with what its tools changed.</div>

<!--
Invite the room to name a failure: partial refund, wrong invoice, duplicate retry, false success. These become concrete examples when writing the scorer.
-->

---
class: opening-bridge
---

# Your manager has one more request.

<p class="manager-request">“Once it works, could it improve itself?”</p>
<p class="story-to-code">We’ll build the employee’s tools, inspect its decisions, and check the work. Then an editor agent will propose changes to its instructions and procedures.</p>
<div class="bottom-note">Whether those changes help is something we measure.</div>

<!--
Use the manager question to motivate the second half. Fixed model, editable harness. The learner first freezes tested tool-loop code. The editor cannot change the trusted final scorer.
-->

---
---

# Here is our workday.

<div class="current-plan"><div>0–55 min<small>Connect, trace, implement the tool and agent handoff</small></div><div>55–105 min<small>Investigate recovery, score the work, make one edit</small></div><div>105–115 min<small>Break. Saved work stays saved.</small></div><div>115–180 min<small>Two improvement rounds, fresh tickets, conclusion</small></div></div>
<div class="bottom-note">Eight notebook steps. Each has code, a named action, a result, and a Forge link.</div>

<!--
This is the three-hour Pending schedule. Allow 15 minutes at the end for final comparison and discussion. Keep extra implementation detail in worked answers.
-->

---
---

# The model chooses the next action.

<HarnessMap :level="0" />
<div class="bottom-note">We change the files and procedures around a fixed model.</div>

<!--
Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.
-->

---
---

# Instructions define the job and its limits.

<HarnessMap :level="1" />
<div class="bottom-note">We change the files and procedures around a fixed model.</div>

<!--
Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.
-->

---
---

# A skill is useful only when it is loaded.

<HarnessMap :level="2" />
<div class="bottom-note">We change the files and procedures around a fixed model.</div>

<!--
Harness means the surrounding instructions and software that decide what the model sees, what it can do, and how work is checked. A saved skill file must be read into context.
-->

---
---

# Copy the notebook into your own project.

<div class="copy-layout"><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view"><img style="width:210px" src="/images/pending-template-qr.svg" alt="QR code for the current Pending template"></a><ol><li>Open <a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view">Pending, Inc. in Forge</a>.</li><li>Choose <strong>Copy to project</strong> and select a project you can write to.</li><li>Open the copy in <strong>Edit</strong>. The notebook detects its destination. Run all stale cells once to initialize the controls.</li></ol></div>
<div class="bottom-note">Your credentials, your traces, your results. No workshop access tokens.</div>

<!--
Use the current v0.3.0 template, never the historical November 12 gateway notebook. An external account requires its own project, notebook compute access and inference access. Setup does not issue a model request.
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

# A trace records the operation you actually ran.


```python
result, record = event(
    "inspect_notebook", {},
    lambda: {"python": platform.python_version()},
)
```

<div class="two-col"><p><strong>The result</strong> goes back to your code.</p><p><strong>The record</strong> keeps arguments, output, start and end times, and any error.</p></div>

<!--
This excerpt shows the independent event receipt. The visible notebook cell uses imported platform through __import__; the semantics are the same. The receipt survives separately from tracing and can be exported again without executing the operation.
-->

---
---

# Send that operation to Agent Lens.


```python
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

<div class="bottom-note"><code>my_tool_span</code> records the same tool result and timing. It does not run the tool again.</div>

<!--
Code excerpt from teaching.STARTERS instrumentation. Explain fields rather than reading code aloud. The full function returns its native span identity. Missing usage in model receipts remains missing.
-->

---
class: exercise
---

# Add a field, then find it in Agent Lens.

<div class="where">Notebook · 1 · Connect and trace</div>

<div class="task">In the inspect_notebook operation, return one more environment field. Read my_tool_span and my_model_span to see how operations become spans.</div>

<div class="done"><strong>Run:</strong> Run this check and verify my Agent Lens trace<br><strong>Check:</strong> Open inspect_notebook. Find your field and compare its value with the returned dictionary.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Run this check and verify my Agent Lens trace.
-->

---
---

# Find the arguments and the returned value.

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c2458ce8b6bb52274d29b5c5a691424b" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-lookup.png" alt="The recorded get_account call requests Acme and returns its account records."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · The recorded get_account call requests Acme and returns its account records. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c2458ce8b6bb52274d29b5c5a691424b">Open the record ↗</a></div></div>

<!--
Verified v0.3.0 baseline billing tool span get_account. The model chose get_account in this run; do not claim it chose the learner-authored lookup_invoice. Local checks exercise that authored tool separately. This early screenshot teaches the native inspection surface; participants should open their own setup trace. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.
-->

---
---

# Read one argument and follow its returned data.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-lookup.png" :x="580" :y="245" :width="690" :height="445" label="Native get_account span: account_id acme and returned account with payment pay-1" /><div class="annotations"><p>The argument is <code>account_id: acme</code>.</p><p>The result contains that account and its payments.</p><p>Find the next model call that used this observation.</p></div></div>

<!--
Enlarged native crop x580,y245,w690,h445. Saved get_account, not lookup_invoice. Do not infer that the model called the authored lookup tool; this example teaches the same span fields participants instrumented.
-->

---
---

# The tool reads one invoice from one account.

<div class="two-col"><div class="ticket"><div class="account">INPUT</div><p>account_id: acme<br>invoice_id: inv-1</p></div><div class="ticket"><div class="account">EXPECTED RESULT</div><p>pay-1: $49<br>pay-2: $49<br>refunds: []</p></div></div>
<div class="bottom-note">Return data. Do not change the account while looking it up.</div>

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

<a class="answer-link" href="/73">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my invoice lookup.
-->

---
---

# A tool name has to reach executable code.

<HarnessMap :level="3" />
<div class="bottom-note">The action schema says what can be requested. Your dispatch function decides which Python function runs.</div>

<!--
The current executor makes structured JSON action requests. Its existing schema declares lookup_invoice account_id and invoice_id; participants implement its behavior and dispatch. Do not imply they are registering remote Sandboxes.
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

# Route one tool yourself; delegate the others.


```python
def my_dispatch(name, arguments, world, invoice_tool, call_tool):
    if name == "lookup_invoice":
        return world, invoice_tool(world, **arguments)
    return call_tool(world, name, arguments)
```

<div class="bottom-note">Both paths return <code>(world, result)</code>. The invoice path preserves <code>world</code>; write tools may change it.</div>

<!--
Walk through name lookup_invoice with acme/inv-1, then get_account. Explain why both paths have the same return contract.
-->

---
class: exercise
---

# Finish the tool-to-model handoff.

<div class="where">Notebook · 3 · Pass observations to the agent</div>

<div class="task">Complete my_dispatch and my_observation. Append the action and actual result to a new message list, keeping the previous request unchanged.</div>

<div class="done"><strong>Run:</strong> Test my tool-to-model handoff<br><strong>Check:</strong> Expand the next request. It contains the two returned payments and the action that produced them.</div>

<a class="answer-link" href="/74">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my tool-to-model handoff.
-->

---
---

# The next request contains the observation.


```python
return messages + [
    {"role": "assistant", "content": json.dumps(action)},
    {"role": "user", "content": "Tool observation: " + json.dumps(result)},
]
```

<p>The employee can now use the payments when choosing its next action.</p>
<div class="bottom-note">This executor uses structured JSON actions and observation messages. Follow its existing message contract.</div>

<!--
Clarify this is the actual workshop protocol rather than OpenAI tool-call message syntax. The complete next-request preview is available in the notebook. Do not mutate the previous messages list.
-->

---
class: exercise
---

# Run the two starting tickets.

<div class="where">Notebook · 3 · Pass observations to the agent</div>

<div class="task">Read the employee instructions. The tested tool and loop code will stay fixed while we compare changes to those instructions.</div>

<div class="done"><strong>Run:</strong> Freeze this executor and run the two starting tickets<br><strong>Check:</strong> Open a billing run and onboarding run. Follow one tool result into the next model call.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze this executor and run the two starting tickets.
-->

---
---

# Record what the model saw and returned.


```python
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
```

<div class="bottom-note">In <code>my_model_span</code>, inspect the complete message mapping. Add usage only when the provider returned it.</div>

<!--
Excerpt deliberately abbreviates message comprehensions. The full visible instrumentation editor has input, output, system instructions, settings and available usage. Ask learners to identify the request that received the lookup result, not just count spans.
-->

---
---

# The second ticket grants Alex account access.

<div class="ticket"><div class="account">FERN → ONBOARDING</div><p>Add alex@example.test as a member.</p></div>
<p>Onboarding tools are discovered and called through local MCP. The model still receives their returned observations through the same loop.</p>
<div class="bottom-note">IT has connected another system. It still occasionally drops the reply.</div>

<!--
Use the local MCP implementation in pending/mcp_server.py. Distinguish actual protocol discovery and invocation from a function merely named MCP. The simulated service deliberately commits a write before returning a timeout in the development incident.
-->

---
---

# An access request is sent.

<TimeoutSequence :level="1" />
<div class="bottom-note">A timeout tells us the response was unavailable. Account state tells us whether access exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# The write succeeds. Its reply times out.

<TimeoutSequence :level="2" />
<div class="bottom-note">A timeout tells us the response was unavailable. Account state tells us whether access exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# Check the operation before trying the write again.

<TimeoutSequence :level="3" />
<div class="bottom-note">A timeout tells us the response was unavailable. Account state tells us whether access exists.</div>

<!--
Explanatory sequence for the committed-write timeout fixture. Use the recorded native trace next to verify the actual recovery. The actual onboarding_status tool reads account_id. A repeated mutation must reuse its operation_id.
-->

---
---

# Did the timeout stop the work?

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/481ae944f1062c5381870a00319f65a3" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-timeout.png" alt="Find provision_member, then inspect onboarding_status."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · Find provision_member, then inspect onboarding_status. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/481ae944f1062c5381870a00319f65a3">Open the record ↗</a></div></div>

<!--
v0.3.0 skill-loaded onboarding: timeout span 5ddd78b1e9faa2d3; recovery status span e62596437e485145. Ask a learner to find evidence that access exists. Do not infer failure from a red span alone. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.
-->

---
---

# The tool says the write may have committed.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-timeout.png" :x="580" :y="423" :width="690" :height="280" label="Native timeout output says the operation may have committed; inspect current access" /><div class="annotations"><p>The request names the account, member, role, and operation.</p><p>The returned message directs the employee to inspect access.</p></div></div><div class="bottom-note">Enlarged native span. A timeout is a reason to investigate, not proof that the account is unchanged.</div>

<!--
Crop x580,y423,w690,h280 from the unchanged1280x720 native capture. Follow its conversation link on the preceding slide. The next operation in the saved trace is onboarding_status.
-->

---
---

# Check the account and the explanation separately.

<div class="result-grid"><div class="state"><strong>State check</strong><p>Was the right payment refunded once?<br>Was access granted correctly?<br>Did unrelated state stay unchanged?</p></div><div class="claim"><strong>Explanation judge</strong><p>Do the completion claims match recorded work?<br>Does the reply explain unresolved issues?</p></div></div>
<div class="bottom-note">A correct account can have a misleading explanation. A confident explanation can describe work that never happened.</div>

<!--
Two measurements answer different questions. Participant-authored development checks teach scoring. Trusted final scoring covers account isolation, idempotency and task-specific constraints. Missing judge responses remain unavailable, never zero.
-->

---
class: exercise
---

# Make false completion fail your check.

<div class="where">Notebook · 4 · Check the work</div>

<div class="task">Complete my_state_check and my_judge_validation. Require one full 4900-cent refund. Require boolean grounded/complete fields and a nonempty reason from the judge.</div>

<div class="done"><strong>Run:</strong> Test my scorer against four known examples<br><strong>Check:</strong> Full refund passes. Partial refund, no refund, and duplicate refund fail, despite the same confident reply.</div>

<a class="answer-link" href="/75">Worked answer →</a>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Test my scorer against four known examples.
-->

---
---

# The judge needs a question it can answer.

<div class="quote">Check each completion claim against recorded tool activity. A timeout is not proof that a write failed. Separate an accurate explanation from a correct account.</div>
<div class="bottom-note">Edit the rubric in the notebook. The response validator checks its shape; it cannot guarantee the judgment is right.</div>

<!--
Rubric from current pending_cells.py. Explain why the judge receives task, recorded actions and explanation. Have participants inspect one reason against a real span. Separate grammatical JSON validation from judging quality.
-->

---
class: exercise
---

# Publish the first comparison now.

<div class="where">Notebook · 4 · Check the work</div>

<div class="task">Run the explanation judge on the two saved starting tickets. Read its reasons alongside your state checks.</div>

<div class="done"><strong>Run:</strong> Judge and publish the starting development comparison<br><strong>Check:</strong> Open a case in the saved comparison and follow its conversation link. Explain any disagreement between the two scores.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Judge and publish the starting development comparison.
-->

---
---

# Compare the same case across versions.

<table class="clean-table readable-table"><tbody><tr><th>Case</th><th>Harness version</th><th>Account correct?</th><th>Explanation grounded?</th><th>Trace</th></tr><tr><td>double-charge</td><td>Starting instructions</td><td>State checker</td><td>LLM judge</td><td>Actual run</td></tr><tr><td>double-charge</td><td>Manual revision</td><td>State checker</td><td>LLM judge</td><td>Actual run</td></tr></tbody></table>
<p>Keep correctness, tool errors, time, and cost in separate columns.</p>
<div class="bottom-note">Illustrative column mapping. Missing judgments stay missing. This is not a product screenshot.</div>

<!--
Weave preserves the evaluation data. W&B stores run artifacts and result tables. Native EvalTables publication is attempted, but the latest rehearsal returned HTTP 500. Use saved Weave/notebook comparisons rather than presenting a fabricated native screen.
-->

---
class: exercise
---

# Change one procedure and rerun it.

<div class="where">Notebook · 5 · Edit one procedure</div>

<div class="task">Choose the recorded action that prompted your edit. Write a verification procedure explaining what the employee should check or do differently.</div>

<div class="done"><strong>Run:</strong> Save this procedure and rerun both development tickets<br><strong>Check:</strong> Read the diff. Find whether the employee loaded your skill and whether its next tool sequence changed.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Save this procedure and rerun both development tickets.
-->

---
---

# A procedure can change behavior without changing quality.

<p class="big">Before calling an edit better, inspect both the account and the execution.</p>
<div class="two-col"><div><h2>Behavior</h2><p>Which skill was read?<br>Which checks or retries ran?<br>Did the edit add work?</p></div><div><h2>Outcome</h2><p>Was the account correct?<br>Was the explanation accurate?<br>Did the same case improve?</p></div></div>

<!--
Participants do not need to manufacture a failure. A live success remains a success. The recorded rehearsal later supplies a useful no-gain example.
-->

---
---

# Save your work. Leave the employee at its desk.

<OfficeScene mode="employee" />
<div class="bottom-note">Ten-minute break. No training or model calls run when you navigate or reopen the notebook.</div>

<!--
Stop at 105 minutes. Use saved checkpoints; opening does not trigger paid work. Have attendees note the next step before the break.
-->

---
---

# Management would like to automate management.

<p class="big">Give an editor agent the current harness and an execution record. Ask it for two competing changes.</p>
<div class="two-col"><div><h2>It may edit</h2><p>Instructions, skills, and bounded workflow rules.</p></div><div><h2>Keep fixed</h2><p>The model, tested tools, fixtures, grader, and budget controls.</p></div></div>
<div class="bottom-note">Please review its changes.</div>

<!--
This is the same fixed model with a different task and context. The editor can produce code/configuration artifacts but cannot improve scores by rewriting the definition of correct work.
-->

---
---

# Propose two changes from the same parent.

<ImprovementBranches :level="1" />
<div class="bottom-note">Solid paths carry versions. Dashed paths supply execution evidence. Colors distinguish alternatives, not quality.</div>

<!--
Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.
-->

---
---

# Test both on fresh copies of the case.

<ImprovementBranches :level="2" />
<div class="bottom-note">Solid paths carry versions. Dashed paths supply execution evidence. Colors distinguish alternatives, not quality.</div>

<!--
Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.
-->

---
---

# Ask which changes to keep.

<ImprovementBranches :level="3" />
<div class="bottom-note">Solid paths carry versions. Dashed paths supply execution evidence. Colors distinguish alternatives, not quality.</div>

<!--
Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.
-->

---
---

# Run the files the decision selected.

<ImprovementBranches :level="4" />
<div class="bottom-note">Solid paths carry versions. Dashed paths supply execution evidence. Colors distinguish alternatives, not quality.</div>

<!--
Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.
-->

---
---

# Carry the chosen version and a lesson forward.

<ImprovementBranches :level="5" />
<div class="bottom-note">Solid paths carry versions. Dashed paths supply execution evidence. Colors distinguish alternatives, not quality.</div>

<!--
Harness²-inspired teaching cycle. Each proposal starts from the parent. Compose reviews both probe records and can select, combine or retain; reviewing a candidate does not mean adopting it. The workshop carries its selected harness to onboarding, unlike the upstream cross-task protocol.
-->

---
---

# Select evidence from the current development run.


```python
experience = [run_employee(session, case, parent, prefix + "starting", **hooks)]
editor_decision(
    session, round_number, "propose", parent, experience,
    tool_writer=my_tool_span, model_writer=my_model_span,
)
```

<div class="bottom-note">The editor receives the parent’s actual execution. Fresh-case grades are not included.</div>

<!--
Conceptual variable names match the visible controller; actual notebook uses _s,_case,_parent,_prefix,_f. It passes prior_experience from round1 into round2. Ask which input would be inappropriate: final-test scores.
-->

---
class: exercise
---

# Read the two proposals before testing them.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Read the visible controller. Ask for two changes, then inspect Candidate A’s diff and rationale. Mark the review checkbox only after reading the files.</div>

<div class="done"><strong>Run:</strong> Round 1 · Ask for two competing changes<br><strong>Check:</strong> The next action is Review and test candidate A. Explain what behavior A is intended to change.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Ask for two competing changes.
-->

---
---

# Run the proposed files, not just the description.


```python
harness = Harness(**decision["harness"])
run = run_employee(session, case, harness, prefix + phase, **hooks)
assert run["harness_fingerprint"] == decision["fingerprint"]
```

<p>Each probe starts from the case’s original state. The saved source identifies what actually ran.</p>
<div class="bottom-note">A proposal title is an intention. The executed files and returned state are the evidence.</div>

<!--
Explain fingerprint as a content identity, not a metric. Do not overwhelm the audience with hash strings. The full assertion and save stage are visible in the current notebook.
-->

---
class: exercise
---

# Test both and compare their behavior.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Review and test A, then review and test B. Follow each result into Agent Lens and look for the behavior its proposal promised.</div>

<div class="done"><strong>Run:</strong> Round 1 · Review and test candidate A; then candidate B<br><strong>Check:</strong> Both started from the same billing state. You can identify which changed files were used in each run.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Round 1 · Review and test candidate A; then candidate B.
-->

---
---

# This candidate required a check before completion.

<div class="native-capture"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-verification.png" alt="Find the rejected finish, check_work, and accepted finish."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · Find the rejected finish, check_work, and accepted finish. · <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/9633d416f5fce6aaa0124ab6ddc38c46">Open the record ↗</a></div></div>

<!--
Recorded candidate B changed verify_before_finish from false to true. It produced the explicit check sequence. Spans: rejected finish 9ed1e7824138ec0e, check_work 2d49d1d8d3ddeb5d, accepted finish 3e19e007d013d4d2. This is a behavior change, not yet evidence of better quality. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.
-->

---
---

# The rejected completion caused another check.

<div class="annotated"><CaptureDetail src="/images/visual-v030-pending-verification.png" :x="580" :y="251" :width="690" :height="185" label="Native finish error: Check the current work before submitting" /><div class="annotations"><p><code>verify_before_finish</code> blocked the first finish.</p><p>The following <code>check_work</code> call satisfied the gate.</p></div></div><div class="bottom-note">The account result still passed. The editor had to decide whether the additional gate was worth keeping.</div>

<!--
Crop x580,y251,w690,h185 from the unchanged1280x720 native capture. Gate behavior is confirmed by the subsequent check_work and accepted finish spans, not inferred from the proposal title.
-->

---
---

# Retain this version is a valid decision.

<div class="diff"><div class="del">Candidate B: require check_work before finish</div><div class="add">Composition: retain the parent harness</div></div>
<p>The recorded first-round decision kept the existing procedure. The extra gate added work without improving the probe’s account result.</p>
<div class="bottom-note"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c04f575608c6f43d99e1b7b428a23791">Open the recorded composition decision ↗</a></div>

<!--
Paraphrase the actual saved v030 composition rationale, attributing it to the editor. An unchanged version still gets tested because the controller verifies every composition decision. It does not create a new executable version.
-->

---
class: exercise
---

# Test the composition, then save its lesson.

<div class="where">Notebook · 6 · Improve twice</div>

<div class="task">Request a composition. Read what it kept or changed, test those files, and save the tested version with its lesson and limits.</div>

<div class="done"><strong>Run:</strong> Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson<br><strong>Check:</strong> The chosen execution matches the decision. If it retained the parent, explain why the files are unchanged.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Compare probes and request a composition → Review and test the composition → Save the tested version and its lesson.
-->

---
---

# A lesson needs an observation and a limit.


```python
review = reflect_execution(session, round_number, run, ...)
adopted = {
    "harness": chosen_harness,
    "lesson": review["lesson"],
    "limits": review["limits"],
    "execution": run["stage_id"],
}
```

<p>Carry the lesson with the execution it came from. The next editor should know what was tested and what remains uncertain.</p>

<!--
Explanatory excerpt, not a drop-in full function. The actual controller falls back to the parent if the chosen execution does not complete. The lesson is agent-authored interpretation backed by a saved run.
-->

---
class: exercise
---

# Repeat the cycle on onboarding.

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
v030 snapshot. This is deliberately separate from older v023 captures in which both rounds retained the parent. Attribute intent to the editor. The exact files are in the executed artifact; final results show whether quality changed.
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

# What made that recursive improvement?

<p class="big">The editor inspected the consequences of a harness, changed it, and used the resulting version and lesson in another improvement round.</p>
<div class="two-col"><div><h2>Changed</h2><p>Instructions, verification skill, selected workflow rules.</p></div><div><h2>Stayed fixed</h2><p>Model weights, tool implementations, final scoring.</p></div></div><div class="bottom-note">Harness²-inspired teaching flow: this workshop carries the chosen harness across two tasks.</div>

<!--
Explain this as a bounded Harness²-inspired workshop. It is not autonomous model-weight improvement. Upstream parallel and sequential recursion and experience reuse are richer than this teaching controller; the workshop carries a chosen harness across two problems.
-->

---
---

# Stop editing before opening the fresh cases.

<table class="clean-table readable-table"><tbody><tr><th>Frozen version</th><th>Fresh cases</th><th>Executions</th></tr><tr><td>Starting instructions</td><td>Same four cases</td><td>4</td></tr><tr><td>Your manual revision</td><td>Same four cases</td><td>4</td></tr><tr><td>Agent-selected version</td><td>Same four cases</td><td>4</td></tr></tbody></table>
<div class="bottom-note">Twelve executions of four cases. Repetitions are not twelve independent tasks.</div>

<!--
Final cases: already-refunded, two-invoices, onboarding-recovery, clarify-access. Their files are public for teaching but are excluded from improvement context. The starting version is the configured tested employee, not the deliberately blank opening illustration.
-->

---
class: exercise
---

# Compare all three versions on fresh tickets.

<div class="where">Notebook · 7 · Compare fresh tickets</div>

<div class="task">Freeze the versions and run the final comparison. Open one matching case across the starting, manual, and agent-selected versions.</div>

<div class="done"><strong>Run:</strong> Freeze versions and run 12 evaluations<br><strong>Check:</strong> Follow a score to its account state, judge reason, trace, and harness. Keep unavailable judgments separate from wrong answers.</div>

<!--
Leave this slide up during the exercise. Ask someone to show the result and explain the change. Do not click a model-run control for them. The exact current control is: Freeze versions and run 12 evaluations.
-->

---
---

# Open a saved case and follow its trace.

<div class="native-capture"><a class="capture-link" href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/5a3721335363bceb77f0c88c87e761f8"><CaptureDetail src="/images/visual-v030-pending-comparison.png" :x="80" :y="305" :width="1180" :height="380" label="Four saved W&B Table case rows, scores and execution evidence" /></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · W&B Table: four fresh cases for the agent-selected version. · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/5a3721335363bceb77f0c88c87e761f8">Open the record ↗</a></div></div>

<!--
Actual native W&B Table, not EvalTables and not a three-version aligned comparison. error=0 means the independent account-state check passed. judge_grounded and judge_complete are separate scores. The evaluation row also links execution evidence. All three versions are compared on the next result table. Native EvalTables remains unavailable with HTTP500. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.
-->

---
---

# Read the conclusion beside its evidence.

<div class="native-capture"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==" class="capture-frame" style="display:block"><img src="/images/visual-v030-pending-report.png" alt="The Report records the complete comparison and its publication status."></a>
<div class="capture-caption">Recorded v0.3.0 rehearsal · The Report records the complete comparison and its publication status. · <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==">Open the record ↗</a></div></div>

<!--
Use fresh v030 final table: all12 account checks and explanation judgments are available and pass. Native EvalTables unavailable; screenshot is the actual W&B/Weave/Report surface and must be captioned accordingly. This is saved execution evidence, not an expected result of a participant’s unexecuted edit.
-->

---
---

# The loop worked. Quality did not improve here.

<table class="clean-table readable-table"><tbody><tr><th>Recorded version</th><th>Correct accounts</th><th>Grounded explanations</th><th>Tool calls across four cases</th></tr><tr><td>Starting</td><td>4 / 4</td><td>4 / 4</td><td>12</td></tr><tr><td>Manual</td><td>4 / 4</td><td>4 / 4</td><td>13</td></tr><tr><td>Agent-selected</td><td>4 / 4</td><td>4 / 4</td><td>13</td></tr></tbody></table>
<div class="bottom-note">One scripted rehearsal. All versions solved these cases. More checking did not raise an already-perfect score.</div>

<!--
Source evidence/v030-pending-rehearsal.json. Tool counts sum2+4+4+2 starting and2+4+5+2 revised. Total observed rehearsal inference cost $0.03093452; exclude notebook compute and do not promise attendee cost. This measures four simulated cases, not repeatability or general enterprise-agent quality.
-->

---
---

# Keep the files that explain the result.

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

# Ask ARIA to investigate the evidence.

<div class="quote">Compare my starting and agent-selected harnesses on the same fresh ticket. Use the linked evaluation, execution trace, and harness diff. Explain what changed in behavior and whether the account result changed. Cite the relevant records before suggesting another experiment.</div>
<div class="bottom-note">Optional. Verify one citation yourself. This investigation is outside the measured comparison.</div>

<!--
Do not imply ARIA authored these prior results. The prompt asks for evidence analysis, not permission to run new experiments or change budgets.
-->

---
---

# Take the loop back to your own product.

<p class="big">Choose one task, one observable state change, and one way to check the work.</p>
<p>Build the tool. Record what happened. Compare the same cases. Give the editor evidence it can act on.</p>
<div class="bottom-note">Management’s announcement is optional. The evaluation is not.</div>

<!--
Close by asking participants to name their own analogous workflow and one failure they could test. Leave them the current notebook, source, records and deck. Preserve honest no-gain outcomes.
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

<span class="source-link"><a href="/19">Return to the exercise →</a></span>

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

<span class="source-link"><a href="/27">Return to the exercise →</a></span>

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

<span class="source-link"><a href="/76">Continue to judge validation →</a></span> · <span class="source-link"><a href="/38">Return to exercise →</a></span>

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

<span class="source-link"><a href="/38">Return to the exercise →</a></span>

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
