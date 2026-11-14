---
theme: default
title: Monitor an airline service agent and build better evaluations
author: Anish Shah
class: cover
layout: default
aspectRatio: 16/9
canvasWidth: 1280
colorSchema: light
transition: fade
wakeLock: false
fonts:
  sans: IBM Plex Sans
  mono: IBM Plex Mono
  provider: none
mdc: true
highlighter: shiki
drawings:
  enabled: false
download: false
---

<div class="kicker">0:00 · Airline service monitoring</div>

# Monitor an airline service agent<br>and build better evaluations

<div class="sub">Investigate booking mistakes, test a monitoring rule, and turn reviewed incidents into checks for the next version.</div><div class="bottom-note">Six hours · Basic Python · Simulated airline data · Your own Forge project<br>Technical preview: native Alignment judging and prepared Insights remain unqualified.</div>

<!--
Set the situation before introducing products. Participants operate a simulated airline customer-service agent. They will distinguish a request completing, a booking being correct, and a monitor detecting a problem. Those are three separate observations.
-->

---
name: passenger-request
---

<div class="kicker">0:03 · Airline service monitoring</div>

# The passenger wants a different outward flight

<div class="quote">Change HAT007 to HAT061 on May 19. Keep the other flight, passengers, and cabin. Quote the fare difference and ask before changing the booking.</div><div class="itinerary"><div class="itinerary-row"><div class="itinerary-label">Current booking</div><div class="segments"><div class="segment untouched"><strong>HAT007</strong><small>LAS → ATL · May 19</small></div><div class="segment untouched"><strong>HAT174</strong><small>ATL → LAS · May 29</small></div><div class="segment ghost"><strong></strong><small></small></div></div></div></div><div class="itinerary-caption">Paraphrased workshop request · source reservation 59XX6W · 2024 dates · airline-discovery-02</div>

<!--
Open airline-discovery-02 in the notebook. The reservation is from upstream source task 7. The workshop adapted its request to exercise a bounded segment change. Ask what must change and what must remain untouched.
-->

---
name: expected-booking
---

<div class="kicker">0:06 · Airline service monitoring</div>

# A correct change preserves the return flight

<div class="itinerary"><div class="itinerary-row"><div class="itinerary-label">Before</div><div class="segments"><div class="segment untouched"><strong>HAT007</strong><small>LAS → ATL · May 19</small></div><div class="segment untouched"><strong>HAT174</strong><small>ATL → LAS · May 29</small></div><div class="segment ghost"><strong></strong><small></small></div></div></div><div class="itinerary-row"><div class="itinerary-label">Requested result</div><div class="segments"><div class="segment changed"><strong>HAT061</strong><small>LAS → ATL · May 19</small></div><div class="segment untouched"><strong>HAT174</strong><small>ATL → LAS · May 29</small></div><div class="segment ghost"><strong></strong><small></small></div></div></div></div><div class="itinerary-caption">Source reservation 59XX6W · same passenger, cabin, and unrequested return flight</div>

<!--
The requested change is HAT007 to HAT061. HAT174 stays. The agent must also check the fare difference and obtain confirmation. The picture describes the intended booking, not an observed live result.
-->

---
name: replace-semantics
---

<div class="kicker">0:09 · Airline service monitoring</div>

# The API replaces the complete flight list

```python {all}
reservation.flights = new_flights
```
<div class="callout">The API receives the itinerary to keep. A flight omitted from that list disappears from the reservation.</div><p class="caption">Abbreviated from the pinned airline implementation. Availability and payment checks are omitted from this excerpt.</p>

<!--
A successful write says the replacement was accepted. It does not establish that the proposed replacement respected the passenger’s request. Read the upstream implementation and the workshop adapter together.
-->

---
name: wrong-state
---

<div class="kicker">0:12 · Airline service monitoring</div>

# A successful write can leave the wrong booking

<div class="itinerary"><div class="itinerary-row"><div class="itinerary-label">Sent to the API</div><div class="segments"><div class="segment changed"><strong>HAT061</strong><small>Requested outward flight</small></div><div class="segment absent"><strong>HAT174 missing</strong><small>Omitted from the API input</small></div><div class="segment ghost"><strong></strong><small>Return not preserved</small></div></div></div></div><div class="itinerary-caption">Illustrative failure on source reservation 59XX6W; not a recorded agent outcome</div><div class="check-row"><span>API operation</span><b>Returned a booking</b></div><div class="check-row"><span>Passenger’s return journey</span><b>Missing</b></div>

<!--
This is an illustrative failure mechanism, not a claim that the live agent will make it. The deterministic local exercise reproduces this list-replacement defect. Live outcomes remain unedited.
-->

---
name: dataset
---

<div class="kicker">0:15 · Airline service monitoring</div>

# The data contains bookings, policy, and passenger requests

<div class="pipeline"><div class="">Booking database<small>Flights, reservations, users</small></div><b v-click="1">→</b><div v-click="1" class="">Passenger request<small>The permitted change and limits</small></div><b v-click="2">→</b><div v-click="2" class="">Airline policy<small>Confirmation and modification rules</small></div></div><p>We use the airline domain from a pinned τ-bench revision. The records and requests are simulated; they are not passenger traffic.</p><p class="caption">MIT license · source checksums and assignments ship with the teaching data · this workshop adapts the environment rather than replicating its benchmark score</p>

<!--
Open the provenance file. Explain which records came from upstream and which scripted passenger behavior or local exercise was added for teaching. Do not describe this as a production airline deployment.
-->

---
name: data-groups
---

<div class="kicker">0:18 · Airline service monitoring</div>

# Keep related bookings in the same data group

<div class="stages"><div>Discovery<strong>8</strong><small>Observe behavior</small></div><div>Monitor check<strong>4</strong><small>Test the saved tag</small></div><div>Development<strong>4 × 2</strong><small>Compare the repair</small></div><div>Final evaluation<strong>6 × 2</strong><small>Score frozen versions</small></div><div>Later traffic<strong>4 × 2</strong><small>Monitor both versions</small></div></div><p>Freeze assignments by passenger and reservation family before qualification. Related upstream training and test tasks cannot cross these groups.</p>

<!--
These are the approved execution counts, totalling 40 conversations. Development and final comparisons run the same requests once on each version. Upstream task identities overlap, so splitting task rows alone would leak related bookings.
-->

---
name: setup
---

<div class="kicker">0:21 · Airline service monitoring</div>

# Your copy owns the runs and saved work

<div class="pipeline"><div class=""><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view">Open the template ↗</a><small>Copy into your Forge project</small></div><b v-click="1">→</b><div v-click="1" class="">Check access<small>Use your own credentials</small></div><b v-click="2">→</b><div v-click="2" class="">Edit and run<small>Explicit controls only</small></div><b v-click="3">→</b><div v-click="3" class="">Return later<small>Restore saved executions</small></div></div><p>The $8 adjustable allowance covers notebook inference. Native tag judging and notebook compute have separate charges.</p><p class="caption">No gateway, shared token, or remote Sandbox requirement. <a href="https://github.com/ash0ts/forge-workshop-kit">Source and laptop setup ↗</a></p>

<!--
Open the hosted template and show copying into the participant’s project. Confirm the detected destination before publishing a trace. Opening, browsing, or checking code does not run a model. An unavailable native service is separate from an agent task failure. Server-side tag costs cannot be stopped by the notebook’s local allowance.
-->

---
class: exercise
name: booking
---

<div class="kicker">0:25 · Airline service monitoring</div>

# Check access and inspect the starting itinerary

<p class="where">Notebook → Inspect the booking</p><div class="task-target">Edit your expected booking explanation</div><ol><li>Open your own copy and confirm the project shown in setup.</li><li>Read the reservation and identify the outbound segment range.</li><li>Save the flights to change and the flights that must remain.</li></ol><div class="done"><b>Run:</b> Connect and restore my work → Save my expected booking<br><b>Finished when:</b> You can name the changed range and the flight that must survive.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: trace-shape
---

<div class="kicker">0:29 · Airline service monitoring</div>

# Record a conversation around the passenger’s request

<div class="pipeline"><div class="">Conversation<small>One booking request</small></div><b v-click="1">→</b><div v-click="1" class="">Turn<small>Passenger input and agent work</small></div><b v-click="2">→</b><div v-click="2" class="">Spans<small>Model requests and tool calls</small></div></div><p>Keep the version and traffic-batch identity on the recorded work. A tag needs to know which behavior it is judging.</p>

<!--
A conversation may contain several turns. Do not collapse unrelated requests into a single conversation. The passenger’s clarification and confirmation belong with the relevant turn evidence. Use native session and span identities from execution.
-->

---
name: tool-tracing
---

<div class="kicker">0:33 · Airline service monitoring</div>

# The tracing code records the actual tool result

```python {1-3|4-5|6-8|all}
with tracing.Tool(
    name=record["name"], arguments=record["arguments"],
    result=record["result"], tool_call_id=record["id"],
    started_at=stamp(record["started_at"]),
    ended_at=stamp(record["ended_at"]),
) as span:
    if record.get("error"):
        span.record_error(RuntimeError(record["error"]))
```
<p class="caption">Excerpt from <code>my_tool_span</code>. Arguments, results, timing, and errors come from the saved operation.</p>

<!--
Name the actual function to edit. The SDK uses the recorded timestamps, not the time an export retry happens. Preserve the saved event if trace publication fails; retry only the export.
-->

---
name: model-tracing
---

<div class="kicker">0:35 · Airline service monitoring</div>

# Connect each model request to its response

<table class="monitor-table "><thead><tr><th>In my_model_span</th><th>Recorded source</th><th>What to inspect</th></tr></thead><tbody><tr><td>model / response_model</td><td>Requested and returned model IDs</td><td>Was the intended model used?</td></tr><tr><td>input_messages / output_messages</td><td>Actual request and reply</td><td>What did the agent know?</td></tr><tr><td>started_at / ended_at</td><td>Request timestamps</td><td>Where was time spent?</td></tr><tr><td>usage</td><td>Provider-reported token counts</td><td>What usage was actually available?</td></tr></tbody></table><p class="caption">Missing usage remains missing. An exporter must not convert an unavailable token count into zero.</p>

<!--
Open the editable my_model_span function beside this table. Participants supply these actual fields to tracing.LLM. Tool spans and model spans answer different questions; neither replaces the independent booking check.
-->

---
class: exercise
name: discovery
---

<div class="kicker">0:39 · Airline service monitoring</div>

# Instrument the agent before sending its first batch

<p class="where">Notebook → Run discovery traffic</p><div class="task-target">Edit my_model_span and my_tool_span</div><ol><li>Add version and traffic-batch attributes to the scopes.</li><li>Keep tool arguments, result, error, and actual timing.</li><li>Run the discovery batch, then follow one returned conversation link.</li></ol><div class="done"><b>Run:</b> Check my tracing code → Send my first Agent Lens trace → Run eight discovery requests<br><b>Finished when:</b> Find the same itinerary in the tool receipt and its stored Agent Lens span.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: read-tool
---

<div class="kicker">0:48 · Airline service monitoring</div>

# Read the booking returned by the tool

<div class="bundle-list"><div>Arguments<small>What did the agent ask the API to replace?</small></div><div>Result<small>Which flights remain in the returned reservation?</small></div><div>Next model request<small>Did the agent receive that observation?</small></div><div>Final response<small>Did the explanation describe the recorded work?</small></div></div>

<!--
Give everyone several minutes on one conversation. Ask them to point to the actual return flight rather than merely an exception field. If the agent was correct, record that success and continue with the labeled calibration drill for the diagnostic exercise.
-->

---
name: capture-conversation
---

<div class="kicker">0:51 · Airline service monitoring</div>

# The reservation read timed out before any change

<div class="native-view " style="grid-template-columns:760px minmax(0,1fr)"><div class="native-image" style="aspect-ratio:690/370"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae/spans/turns/b4ad558d6ba484805a84991dd3f9e7c1/spans/faf64a520e6af500"><img style="position:absolute;width:185.5072463768116%;height:auto;max-width:none;left:-84.05797101449275%;top:-94.5945945945946%;" src="/captures/native-conversation-error.png" alt="Agent Lens tool span for reservation 59XX6W, showing the saved TimeoutError, error status, and reservation ID input."></a><span class="native-pin" style="left:18.898550724637694%;top:28.583783783783783%">1</span><span class="native-pin" style="left:18.898550724637694%;top:43.95675675675678%">2</span><span class="native-pin" style="left:6.4695652173913025%;top:92.4108108108108%">3</span></div><div class="native-notes"><p><b>1 · Tool status</b><br>This operation failed. The booking outcome needs a separate check.</p><p><b>2 · Actual error</b><br>The message says the read timed out and no booking state changed.</p><p><b>3 · Same reservation</b><br>59XX6W connects this span to the flight list we inspected.</p></div></div><p class="caption">Recorded discovery request for reservation 59XX6W. This error concerns a read operation; it does not establish an itinerary violation. <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae/spans/turns/b4ad558d6ba484805a84991dd3f9e7c1/spans/faf64a520e6af500">Open the recorded view ↗</a></p>

<!--
Find the request, full replacement list, returned booking, and final response. Do not infer task success from the tool returning normally. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: capture-recovery
---

<div class="kicker">0:56 · Airline service monitoring</div>

# Follow the agent after the error

<div class="native-view " style="grid-template-columns:420px minmax(0,1fr)"><div class="native-image" style="aspect-ratio:335/368"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae/spans/turns/b4ad558d6ba484805a84991dd3f9e7c1/spans/faf64a520e6af500"><img style="position:absolute;width:382.08955223880594%;height:auto;max-width:none;left:-71.64179104477611%;top:-72.01086956521739%;" src="/captures/native-conversation-error.png" alt="Agent Lens span tree showing a failed reservation read, another model call, and a later successful reservation read before quote and confirmation."></a><span class="native-pin" style="left:16.238805970149265%;top:29.728260869565226%">1</span><span class="native-pin" style="left:16.238805970149265%;top:42.05434782608695%">2</span><span class="native-pin" style="left:16.238805970149265%;top:55.55434782608696%">3</span></div><div class="native-notes"><p><b>1 · Failed read</b><br>The red error belongs to get_reservation_details.</p><p><b>2 · Another model request</b><br>Read what the model received after that tool error.</p><p><b>3 · A later read succeeds</b><br>Continue to the quote, confirmation, and final booking. One failed span is not the whole result.</p></div></div><p class="caption">The saved execution recovered and passed its booking checks. Preserve this success when reviewing the monitoring rule. <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae/spans/turns/b4ad558d6ba484805a84991dd3f9e7c1/spans/faf64a520e6af500">Open the recorded view ↗</a></p>

<!--
Read the failed tool operation, the next model request, and the subsequent tool result. Then verify the complete booking. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: three-questions
---

<div class="kicker">0:58 · Airline service monitoring</div>

# Keep three questions separate

<table class="monitor-table "><thead><tr><th>Question</th><th>Evidence</th><th>Possible outcome</th></tr></thead><tbody><tr><td>Did the tool execute?</td><td>Tool result, error, duration</td><td>Returned normally</td></tr><tr><td>Did it do the requested work?</td><td>Original and final booking</td><td>Return flight was removed</td></tr><tr><td>Did the monitor detect that?</td><td>Reviewed tag result</td><td>Missed, found, or not processed</td></tr></tbody></table>

<!--
Use the same example across all three questions. A lower tool-error rate does not prove higher booking quality. A high tag count may mean more failures, broader criteria, or a different processing denominator.
-->

---
name: overview
---

<div class="kicker">1:05 · Airline service monitoring</div>

# Use Overview for context, then open Conversations

<div class="timeline-list"><b>Overview</b><span>Read project-level trends and the selected time range.</span><b>Conversations</b><span>Filter the exact agent and custom <code>airline.version = baseline</code>.</span><b>Saved view</b><span>Save the filter, then identify the discovery requests.</span><b>Open a case</b><span>Follow an error or slow request through its complete conversation.</span></div>

<!--
The verified version filter is in Conversations. The native Agent Version dropdown was empty during rehearsal; use the recorded custom airline.version attribute. Overview remains project context, not a claim that the saved conversation filter applies to every chart. A saved view is a query, not a snapshot of an evaluation dataset.
-->

---
name: insights
---

<div class="kicker">1:14 · Airline service monitoring</div>

# Insights suggests a pattern worth investigating

<div class="pipeline"><div class="">Native cluster<small>A recurring behavior</small></div><b v-click="1">→</b><div v-click="1" class="">Representative turns<small>Read several examples</small></div><b v-click="2">→</b><div v-click="2" class="">Counterexample<small>Find where the description fails</small></div><b v-click="3">→</b><div v-click="3" class="">Human claim<small>State the behavior you will test</small></div></div><p>Use a verified prepared cluster when available. If the project says “No completed clustering run,” investigate the saved turns and record this native exercise as unavailable.</p>

<!--
A prepared cluster must contain real executions and a completed native clustering run. The current release must report whether that prerequisite was met. A deterministic notebook summary is not Agent Lens Insights. If native access is unavailable, identify the limitation and use only a labeled saved capture.
-->

---
name: outcomes
---

<div class="kicker">1:26 · Airline service monitoring</div>

# An error is not always an unresolved failure

<table class="monitor-table "><thead><tr><th>Observed sequence</th><th>What to inspect</th><th>Review status</th></tr></thead><tbody><tr><td>Tool times out, readback confirms the change</td><td>Final booking and retry behavior</td><td>Recovered</td></tr><tr><td>Tool succeeds, return flight is absent</td><td>Original request and final booking</td><td>Task failure</td></tr><tr><td>Agent asks for confirmation and waits</td><td>Was any unapproved write made?</td><td>Awaiting input</td></tr><tr><td>Turn lacks the original itinerary</td><td>Can the requested change be reconstructed?</td><td>Insufficient evidence</td></tr></tbody></table>

<!--
Review behavior through its outcome. Do not label an appropriate refusal as a failure just because the passenger did not get their first request. The airline policy and allowed request matter.
-->

---
class: exercise
name: investigate
---

<div class="kicker">1:32 · Airline service monitoring</div>

# Save one claim with the turn that supports it

<p class="where">Notebook → Investigate behavior</p><div class="task-target">Edit The trace investigation record</div><ol><li>Open the original request and relevant tool span.</li><li>Write the observed state change and classify recovery or unresolved work.</li><li>Save the native conversation and turn identities with your claim.</li></ol><div class="done"><b>Run:</b> Save this trace investigation<br><b>Finished when:</b> A second person can open the event and check your claim.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: break-one
---

<div class="kicker">1:40 · Airline service monitoring</div>

# Break until 1:50

<p class="sub">Save the investigation before you leave. Completed requests stay saved even if a later export needs a retry.</p>

<!--
Ten-minute break. Keep the fixed batches and state; do not restart discovery to generate a more convenient failure.
-->

---
name: tag-definition
---

<div class="kicker">1:50 · Airline service monitoring</div>

# Define a behavior that a reviewer can check

<div class="callout"><b>Unrequested itinerary change</b><br>The agent changed or removed a flight outside the passenger’s approved change.</div><p>Judge the requested scope, the action, and the resulting reservation together. A shorter itinerary alone is not enough.</p>

<!--
The initial proposed criterion is intentionally a starting hypothesis for alignment, not a validated native rule. Participants must review what evidence exists in each turn. Requests may authorize replacing the entire itinerary.
-->

---
name: counterexample-nonstop
---

<div class="kicker">1:55 · Airline service monitoring</div>

# Fewer flights can be the correct result

<div class="itinerary"><div class="itinerary-row"><div class="itinerary-label">Before</div><div class="segments"><div class="segment untouched"><strong>outbound-1</strong><small>First outward flight</small></div><div class="segment untouched"><strong>outbound-2</strong><small>Connecting flight</small></div><div class="segment untouched"><strong>return-1</strong><small>Return journey</small></div></div></div><div class="itinerary-row"><div class="itinerary-label">Approved change</div><div class="segments"><div class="segment changed"><strong>new-outbound</strong><small>Requested nonstop</small></div><div class="segment untouched"><strong>return-1</strong><small>Keep this flight</small></div><div class="segment ghost"><strong></strong><small>No extra segment</small></div></div></div></div><div class="itinerary-caption">Simplified segment IDs for the list operation. Open the notebook for the source reservation, flight numbers, and dates.</div><p>Two connecting flights became one nonstop. The return remains. This should not be tagged as an unrequested change.</p>

<!--
This is the central counterexample to a naive flight-count rule. Ask the room whether changing three segments to two is sufficient evidence of failure. It is not.
-->

---
name: counterexamples
---

<div class="kicker">2:00 · Airline service monitoring</div>

# Add counterexamples before trusting the rule

<table class="monitor-table "><thead><tr><th>Example</th><th>What the criterion must account for</th></tr></thead><tbody><tr><td>A one-way booking</td><td>There was never a return flight to preserve.</td></tr><tr><td>An explicitly approved full-itinerary change</td><td>All original flights may legitimately be replaced.</td></tr><tr><td>A failed write followed by successful recovery</td><td>Judge the resolved state and the turn’s scope.</td></tr><tr><td>A request waiting for confirmation</td><td>No write has been approved yet.</td></tr><tr><td>Missing original booking</td><td>Insufficient evidence is not a negative finding.</td></tr></tbody></table>

<!--
Use actual reviewed turns when available. The calibration pack is a labeled teaching fallback, not a claim about the learner’s live failure rate. Keep all disagreements and their reasons.
-->

---
name: tag-lifecycle
---

<div class="kicker">2:05 · Airline service monitoring</div>

# A native tag has criteria, labels, and a live state

<div class="pipeline"><div class="">Draft criteria<small>Describe the behavior</small></div><b v-click="1">→</b><div v-click="1" class="">Alignment review<small>People label turns</small></div><b v-click="2">→</b><div v-click="2" class="">Test the judge<small>Compare with the reviews</small></div><b v-click="3">→</b><div v-click="3" class="">Save criteria<small>Update what the live tag uses</small></div></div><p>Alignment experiments do not change live criteria until you save them. Record the chosen criteria and experiment identity.</p>

<!--
Walk through native Tags and Alignment. Creating or editing a notebook rubric is not the same action as saving native tag criteria. Use the native identities in the readback record.
-->

---
name: capture-tag-configuration
---

<div class="kicker">2:08 · Airline service monitoring</div>

# Save the criteria and check the tag’s scope

<div class="native-view " style="grid-template-columns:760px minmax(0,1fr)"><div class="native-image" style="aspect-ratio:700/430"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/tags/01a1dbfc-34e0-7540-a690-0fb598377ae6/edit"><img style="position:absolute;width:182.85714285714286%;height:auto;max-width:none;left:-56.42857142857143%;top:-48.837209302325576%;" src="/captures/native-tag-configuration.png" alt="Actual native Agent Lens tag configuration showing saved criteria, Apply with AI, and an exact airline workspace agent filter."></a><span class="native-pin" style="left:86.20000000000002%;top:7.758139534883718%">1</span><span class="native-pin" style="left:2.817142857142861%;top:32.37209302325581%">2</span><span class="native-pin" style="left:2.817142857142861%;top:85.95348837209302%">3</span></div><div class="native-notes"><p><b>1 · Automatic judging</b><br>Apply with AI is enabled for this rehearsal.</p><p><b>2 · Saved criteria</b><br>Requested scope and resulting booking matter. Flight count alone is insufficient.</p><p><b>3 · Workspace scope</b><br>The exact agent filter limits this tag to the rehearsal.</p></div></div><p class="caption">Recorded maintainer workspace; each participant creates a tag in their own project. <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/tags/01a1dbfc-34e0-7540-a690-0fb598377ae6/edit">Open the recorded view ↗</a></p>

<!--
Read the saved criteria, Apply with AI setting, and exact workshop-agent scope. This recorded tag ID is not a participant default. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: judge-context
---

<div class="kicker">2:10 · Airline service monitoring</div>

# Turn context limits what the judge can know

<div class="pipeline"><div class="">Passenger message<small>Requested scope</small></div><b v-click="1">→</b><div v-click="1" class="">Tool work<small>Arguments and returned state</small></div><b v-click="2">→</b><div v-click="2" class="">Judge context<small>Evidence available in this turn</small></div></div><p>If the original itinerary is absent, the judge may not be able to establish which flight was removed. Mark the review unresolved and inspect the context.</p>

<!--
Native judges see turn-level evidence. Do not assume every model span contains the entire conversation. The context inspection is part of the exercise; a fluent judge reason does not create missing evidence.
-->

---
class: exercise
name: align
---

<div class="kicker">2:15 · Airline service monitoring</div>

# Test your tag against reviewed turns

<p class="where">Notebook → Align the monitoring rule</p><div class="task-target">Edit the tag criteria in Agent Lens</div><ol><li>In native Alignment, review failures and legitimate changes.</li><li>Revise the criteria after inspecting false positives and missed cases.</li><li>Save the criteria, then read back its native identity and state.</li></ol><div class="done"><b>Run:</b> Read back my tag and alignment<br><b>Finished when:</b> The notebook shows the saved criteria, reviewed labels, and the selected native experiment.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
class: exercise
name: alignment-test
---

<div class="kicker">2:20 · Airline service monitoring</div>

# Test one reviewed turn in native Alignment

<p class="where">Notebook → Check monitoring on new requests</p><div class="task-target">Edit the criteria and your turn review</div><ol><li>Refresh the native examples and label a turn with a reason.</li><li>Select the same saved criteria you intend to use on new traffic.</li><li>Run one explicit test and compare its prediction with your review.</li></ol><div class="done"><b>Run:</b> Refresh native Alignment examples → Test the saved criteria on this reviewed turn<br><b>Finished when:</b> You have the exact turn, criteria, reviewed label, and either a prediction or an explicit unavailable result.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: capture-alignment
---

<div class="kicker">2:22 · Airline service monitoring</div>

# A saved review is not a completed judge result

<div class="native-view " style="grid-template-columns:760px minmax(0,1fr)"><div class="native-image" style="aspect-ratio:795/440"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/tags/01a1dbfc-34e0-7540-a690-0fb598377ae6/test"><img style="position:absolute;width:161.00628930817612%;height:auto;max-width:none;left:-61.0062893081761%;top:-25.0%;" src="/captures/native-alignment-unavailable.png" alt="Native Alignment showing human expected labels, unscored turns, selected turn context, and no completed test result."></a><span class="native-pin" style="left:75.52704402515724%;top:16.727272727272727%">1</span><span class="native-pin" style="left:75.52704402515724%;top:70.72727272727273%">2</span><span class="native-pin" style="left:38.01257861635221%;top:20.818181818181824%">3</span></div><div class="native-notes"><p><b>1 · Expected result</b><br>A person supplied this label. It is not a model prediction.</p><p><b>2 · No completed test</b><br>Unscored stays unavailable; no tag must not be read as a negative judgment.</p><p><b>3 · Selected turn</b><br>Inspect its context. The original booking may be outside this turn.</p></div></div><p class="caption">Recorded native Alignment. Six API test attempts returned HTTP 500; this screen still has no completed judgment. <a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/tags/01a1dbfc-34e0-7540-a690-0fb598377ae6/test">Open the recorded view ↗</a></p>

<!--
Inspect the saved review and the test status. A failed native test has no prediction to compare; do not turn it into a negative label. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: judge-validation
---

<div class="kicker">2:29 · Airline service monitoring</div>

# A valid response can contain a wrong judgment

```python {1-2|3-6|all}
if any(type(answer.get(k)) is not bool
       for k in ("supported", "unresolved")):
    raise ValueError("Expected two booleans")
if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
    raise ValueError("Explain the judgment")
if not isinstance(answer.get("event_ids"), list):
    raise ValueError("Cite the supporting events")
```
<p>The validator catches malformed responses. Only a review of the booking and request can establish whether the judgment is right.</p>

<!--
This is a local structured-response exercise for the explanation judge, separate from the native tag’s server-side implementation. A string false is not a boolean false. Preserve unavailable judgments rather than replace them with false.
-->

---
name: confusion
---

<div class="kicker">2:35 · Airline service monitoring</div>

# Measure the monitor on reviewed cases

<div class="confusion"><div class="head"></div><div class="head">Reviewer: failure</div><div class="head">Reviewer: no failure</div><div class="head">Tag: positive</div><div class="positive"><strong>3</strong>True positives</div><div class="incorrect"><strong>1</strong>False positive</div><div class="head">Tag: negative</div><div class="incorrect"><strong>1</strong>False negative</div><div><strong>3</strong>True negatives</div></div><p class="caption">Illustrative arithmetic: eight reviewed, processed turns. These are not workshop results.</p>

<!--
Walk through one cell at a time. The human review is the reference for this calculation; disagreement remains open to correction. Unavailable judgments are excluded from these eight processed rows and reported separately.
-->

---
name: precision
---

<div class="kicker">2:39 · Airline service monitoring</div>

# Precision asks whether an alert deserves review

<div class="formula"><code>3 / (3 + 1) = 0.75</code><div><b>Three of four alerts</b><small>match the reviewed failure label.</small></div></div><p>Low precision creates review work. Read the false positives before widening or narrowing the rule.</p><p class="caption">Illustrative arithmetic from the previous matrix. If there are no alerts, precision is unavailable.</p>

<!--
The denominator is the tagged turns with a reviewed label, not all requests. Alert count cannot tell us how many failures were missed. Ask which example produced the false positive.
-->

---
name: recall
---

<div class="kicker">2:42 · Airline service monitoring</div>

# Recall asks which failures the monitor missed

<div class="formula"><code>3 / (3 + 1) = 0.75</code><div><b>Three of four failures</b><small>were found among reviewed, processed turns.</small></div></div><p>Review unflagged cases too. If we only inspect alerts, we cannot estimate missed failures.</p><p class="caption">Illustrative arithmetic. This small reviewed sample does not establish production recall.</p>

<!--
Precision and recall happen to match in this arithmetic example, but they use different denominators. Show the missed failure cell. Review sampling affects whether these values estimate the wider traffic population.
-->

---
name: coverage
---

<div class="kicker">2:45 · Airline service monitoring</div>

# Coverage tells us which turns were judged

<div class="formula"><code>8 / 10 = 0.80</code><div><b>Eight of ten turns</b><small>have a completed judgment.</small></div></div><div class="comparison-grid"><div><h2>Tag absent</h2><p>A completed judgment may have been negative.</p></div><div><h2>Not processed</h2><p>No completed judgment exists yet. Keep it unknown.</p></div></div><p class="caption">Illustrative arithmetic: two additional turns have unavailable judgments.</p>

<!--
A missing tag is not enough to identify a completed negative judgment. Read processing status and identities. Keep pending, failed, insufficient-context, and scored states separate as supported by the recorded events.
-->

---
class: exercise
name: monitor
---

<div class="kicker">2:50 · Airline service monitoring</div>

# Calculate monitor quality and send new traffic

<a class="answer-link" href="/69">Worked answer ↗</a>

<p class="where">Notebook → Check monitoring on new requests</p><div class="task-target">Edit my_monitor</div><ol><li>Compute precision and recall using reviewed, processed turns.</li><li>Compute coverage over eligible turns, retaining missing judgments.</li><li>Enable the saved tag for this workspace’s agent and run the monitor-check batch.</li></ol><div class="done"><b>Run:</b> Check my monitoring calculations → Run four new requests → Read tag results → Calculate agreement with my reviews<br><b>Finished when:</b> You can explain every denominator and name any turns still awaiting judgment.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: live-missingness
---

<div class="kicker">3:00 · Airline service monitoring</div>

# A missing live tag does not establish a negative judgment

<p class="principle">Live tag assignments identify positive matches. An untagged turn may be negative, pending, or unavailable.</p><p>Use explicit native Alignment test results for known positive and negative predictions. Join those results to your reviews before calculating agreement.</p>

<!--
Keep the live assignment view separate from the explicit Alignment-test result set. Do not infer processing coverage from positive assignments alone. Record the denominator and native result source beside any calculated rate.
-->

---
name: freeze-monitor
---

<div class="kicker">3:02 · Airline service monitoring</div>

# Freeze the rule before comparing agent versions

<div class="pipeline"><div class="">Saved criteria<small>One selected rule</small></div><b v-click="1">→</b><div v-click="1" class="">Starting version<small>Apply that rule</small></div><b v-click="2">→</b><div v-click="2" class="">Repaired version<small>Apply the same rule</small></div></div><p>Record the criteria snapshot and tag identity. Changing the monitor halfway through makes tag rates difficult to compare.</p>

<!--
The native rule needs the same workspace scope for both versions but enough attributes to filter them independently. The local notebook cannot guarantee the native service has completed processing. Show its readback status.
-->

---
name: curation
---

<div class="kicker">3:10 · Airline service monitoring</div>

# A reviewed turn becomes a regression case

<div class="pipeline"><div class="">Reviewed incident<small>A claim with supporting spans</small></div><b v-click="1">→</b><div v-click="1" class="">Reconstruct inputs<small>Request, initial booking, policy</small></div><b v-click="2">→</b><div v-click="2" class="">Define expected behavior<small>What must change or stay</small></div><b v-click="3">→</b><div v-click="3" class="">Save a case<small>Source links and dataset version</small></div></div><p>A saved conversation filter alone does not preserve the input state needed to rerun the incident.</p>

<!--
Make curation an explicit code exercise. The case contains the original booking, not the already-mutated booking that caused the complaint. Keep the exact request and constraints with it.
-->

---
name: case-fields
---

<div class="kicker">3:15 · Airline service monitoring</div>

# Keep enough information to replay the request

<div class="bundle-list"><div>Initial booking<small>All flights before the agent acted</small></div><div>Passenger request<small>Change, constraints, and confirmation rules</small></div><div>Policy version<small>The rule in force for that execution</small></div><div>Expected behavior<small>Requested replacement and preserved segments</small></div><div>Reviewed label<small>Reviewer, rationale, and unresolved questions</small></div><div>Source identities<small>Conversation, turn, span, execution, code</small></div></div>

<!--
Ask what happens if someone saves only the final reply. They cannot reconstruct the original itinerary or determine what was unrequested. These records are public simulated examples; the same technique with real passengers needs an appropriate privacy review.
-->

---
class: exercise
name: curate
---

<div class="kicker">3:22 · Airline service monitoring</div>

# Build a regression case from the reviewed turn

<a class="answer-link" href="/70">Worked answer ↗</a>

<p class="where">Notebook → Curate regression cases</p><div class="task-target">Edit case_from_reviewed_turn</div><ol><li>Copy the initial booking, request, policy, and approved scope.</li><li>Preserve the reviewer’s decision and the exact source identities.</li><li>Add an unflagged control alongside the reported failure.</li></ol><div class="done"><b>Run:</b> Check my regression-case builder → Save reviewed regression cases<br><b>Finished when:</b> Rerunning the case starts from the original booking, not its mutated state.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: state-scoring
---

<div class="kicker">3:31 · Airline service monitoring</div>

# Score the change and the preserved flights separately

<div class="check-row"><span>Requested segment range</span><b>Correct replacement</b></div><div class="check-row"><span>Untouched segments</span><b>Still present</b></div><div class="check-row"><span>Passenger approval</span><b>Before the write</b></div><div class="check-row"><span>Airline policy</span><b>Applicable rules met</b></div>

<!--
The state scorer is deterministic over recorded state. It does not use the agent’s final assertion as proof. A completion score must fail when the requested change is missing, even if the unchanged return is preserved.
-->

---
name: separate-judge
---

<div class="kicker">3:36 · Airline service monitoring</div>

# The explanation judge answers a different question

<div class="two-col"><div><h2>Booking-state check</h2><p>Was the approved itinerary applied without changing unrelated flights?</p></div><div><h2>Explanation judgment</h2><p>Did the final response accurately describe the recorded work and unresolved issues?</p></div></div><div class="callout">“Your return flight is unchanged” can be wrong even when it is polite and well formatted.</div>

<!--
The explanation judge receives the recorded work needed for its rubric. Human review and deterministic state checks remain distinct evidence. Missing judgments stay unavailable; do not average them as zero or success.
-->

---
class: exercise
name: state-check
---

<div class="kicker">3:41 · Airline service monitoring</div>

# Add the booking check the old evaluation missed

<a class="answer-link" href="/71">Worked answer ↗</a>

<p class="where">Notebook → Curate regression cases</p><div class="task-target">Edit my_state_scorer and my_judge_validation</div><ol><li>Implement preservation and confirmation checks; inspect the independent task-success score beside them.</li><li>Try the correct booking, missing return, and unconfirmed-write fixtures.</li><li>Keep the explanation judgment separate from those state checks.</li></ol><div class="done"><b>Run:</b> Check my booking scorer → Check my judge-response validator → Save my development evaluation code<br><b>Finished when:</b> Your scorer rejects the missing return and an unapproved write.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: regression-artifact
---

<div class="kicker">3:48 · Airline service monitoring</div>

# Save the case and its checks with the checkpoint

<div class="pipeline"><div class="">Regression case<small>Original booking and reviewed expectation</small></div><b v-click="1">→</b><div v-click="1" class="">Source files<small>Case builder and evaluation code</small></div><b v-click="2">→</b><div v-click="2" class="">Checkpoint artifact<small>A saved version you can restore</small></div></div><p>A W&B Artifact is a versioned bundle of files. Open the checkpoint artifact and find the case inputs and source used for this exercise.</p><p class="caption">Saving locally and publishing the artifact are separate. If publication fails, retry the upload without rerunning the passenger request.</p>

<!--
Show the checkpoint link produced by the participant’s session. Ask someone to identify the source case, reviewer, and actual function. A named dataset without its initial booking cannot reproduce this incident.
-->

---
name: break-two
---

<div class="kicker">3:50 · Airline service monitoring</div>

# Break until 4:00

<p class="sub">Save the regression dataset and selected criteria. We will test a code repair against them after the break.</p>

<!--
Ten-minute break. Do not edit final cases or resample cases based on which version looks better.
-->

---
name: repair-problem
---

<div class="kicker">4:00 · Airline service monitoring</div>

# Repair the list operation, then compare the behavior

<div class="itinerary"><div class="itinerary-row"><div class="itinerary-label">Current list</div><div class="segments"><div class="segment untouched"><strong>outbound-1</strong><small>First outward flight</small></div><div class="segment untouched"><strong>outbound-2</strong><small>Connecting flight</small></div><div class="segment untouched"><strong>return-1</strong><small>Return journey</small></div></div></div><div class="itinerary-row"><div class="itinerary-label">Repaired result</div><div class="segments"><div class="segment changed"><strong>new-outbound</strong><small>Requested nonstop</small></div><div class="segment untouched"><strong>return-1</strong><small>Keep this flight</small></div><div class="segment ghost"><strong></strong><small>No extra segment</small></div></div></div></div><div class="itinerary-caption">Simplified segment IDs for the list operation. Open the notebook for the source reservation, flight numbers, and dates.</div>

<!--
Revisit the same concrete request. The implementation change builds a complete replacement itinerary from the requested range and untouched prefix and suffix. It does not depend on a flight-count heuristic.
-->

---
name: range-repair
---

<div class="kicker">4:06 · Airline service monitoring</div>

# Replace a range without dropping its neighbors

```python {1-4|5|6|7|all}
def my_itinerary_builder(
    current_flights, replace_start, replace_stop, replacement_flights
):
    return (
        current_flights[:replace_start]
        + replacement_flights
        + current_flights[replace_stop:]
    )
```
<p class="caption">Python uses a half-open range: the start is included; the stop is not. Validate the requested range before use.</p>

<!--
The example replaces original[0:2] with one flight and preserves original[2:]. Do not assume every request changes one flight. A full-itinerary change legitimately has start zero and stop len(original).
-->

---
name: range-values
---

<div class="kicker">4:10 · Airline service monitoring</div>

# Walk through the values before running the model

```python {1-3|5|6|7|all}
original = ["outbound-1", "outbound-2", "return-1"]
start, stop = 0, 2
replacement = ["new-outbound"]

original[:start]   # []
replacement       # ["new-outbound"]
original[stop:]    # ["return-1"]
```
<p>The complete API input becomes <code>["new-outbound", "return-1"]</code>.</p>

<!--
This is a free, simplified arithmetic check. It establishes the list transformation, not whether the model selected the correct segment range or received passenger confirmation.
-->

---
class: exercise
name: repair
---

<div class="kicker">4:15 · Airline service monitoring</div>

# Test the repair on matched development bookings

<a class="answer-link" href="/72">Worked answer ↗</a>

<p class="where">Notebook → Repair itinerary handling</p><div class="task-target">Edit my_itinerary_builder</div><ol><li>Implement the range replacement and validate its bounds.</li><li>Test a one-way case, connecting itinerary, and full replacement.</li><li>Run the curated regression cases, then compare both versions on the development bookings.</li></ol><div class="done"><b>Run:</b> Check my itinerary repair → Run my curated regression cases → Compare on four development bookings<br><b>Finished when:</b> Each pair starts from the same state and records the exact builder that ran.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: confirmation
---

<div class="kicker">4:24 · Airline service monitoring</div>

# The passenger must approve the proposed change

<div class="pipeline"><div class="">Agent proposes<small>Full resulting itinerary</small></div><b v-click="1">→</b><div v-click="1" class="">Scripted passenger checks<small>Request and preserved flights</small></div><b v-click="2">→</b><div v-click="2" class="">Confirmation<small>Only when requirements match</small></div><b v-click="3">→</b><div v-click="3" class="">Write<small>Apply the approved change</small></div></div><p>The passenger script must reject an unrelated change. It cannot blindly approve every proposal to make the exercise complete.</p>

<!--
Confirm that the scripted passenger enforces the source request’s requirements. A correct refusal or request for clarification may be the right outcome. The code repair cannot compensate for an incorrect approval policy.
-->

---
name: repair-boundary
---

<div class="kicker">4:32 · Airline service monitoring</div>

# Explain a passing repair without overstating it

<div class="comparison-grid"><div><h2>Local fixture</h2><p>The repaired function preserves the return in the known list-replacement example.</p></div><div><h2>Agent behavior</h2><p>The agent still has to select the right flights, ask for approval, and report the result.</p></div></div><p>The worked repair establishes a mechanism. The matched evaluations establish how the tested agent behaved.</p>

<!--
Keep deterministic repair results separate from live stochastic outcomes. A live success remains a success. Never replace it with a failure to improve the story.
-->

---
class: exercise
name: judge-execution
---

<div class="kicker">4:33 · Airline service monitoring</div>

# Judge one saved explanation against its evidence

<a class="answer-link" href="/68">Worked answer ↗</a>

<p class="where">Notebook → Build regression cases</p><div class="task-target">Edit my_judge_validation and the explanation rubric</div><ol><li>Choose a saved development execution.</li><li>Read the booking result and the final response together.</li><li>Run one explicit judgment and inspect its cited event IDs.</li></ol><div class="done"><b>Run:</b> Judge this saved explanation<br><b>Finished when:</b> The response validates, and its cited events support or contradict its reason.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: freeze
---

<div class="kicker">4:40 · Airline service monitoring</div>

# Freeze code before opening the reserved requests

<div class="pipeline"><div class="">Development results<small>Read successes and failures</small></div><b v-click="1">→</b><div v-click="1" class="">Select the tested repair<small>Save the exact source</small></div><b v-click="2">→</b><div v-click="2" class="">Freeze versions<small>Keep original and repair</small></div><b v-click="3">→</b><div v-click="3" class="">Reserved evaluation<small>No more choosing on these cases</small></div></div><p>If the repair regresses, retain the earlier version and explain why. A longer instruction or extra check does not earn a release.</p>

<!--
Final expected answers do not enter the solver or rubric-tuning contexts. The local source files are inspectable for teaching, so this is a controlled workshop comparison, not a secure blind benchmark.
-->

---
class: exercise
name: final
---

<div class="kicker">4:46 · Airline service monitoring</div>

# Compare six reserved bookings across both versions

<p class="where">Notebook → Evaluate the frozen versions</p><div class="task-target">Edit The matched evaluation call</div><ol><li>Freeze the tested repair and inspect its source reference.</li><li>Run both versions on the six fixed reserved requests.</li><li>Open one aligned case and follow both rows back to their traces.</li></ol><div class="done"><b>Run:</b> Freeze the tested repair → Evaluate six reserved bookings<br><b>Finished when:</b> All twelve executions have matched case identities, or an explicit unavailable status.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: aligned-comparison
---

<div class="kicker">4:54 · Airline service monitoring</div>

# Read the same request across the two versions

<table class="monitor-table "><thead><tr><th>Same case</th><th>Starting version</th><th>Repaired version</th></tr></thead><tbody><tr><td>Initial state</td><td>Same reservation snapshot</td><td>Same reservation snapshot</td></tr><tr><td>Executed code</td><td>Starting builder source</td><td>Frozen repair source</td></tr><tr><td>Booking outcome</td><td>Read actual final flights</td><td>Read actual final flights</td></tr><tr><td>Explanation</td><td>Inspect its own judge result</td><td>Inspect its own judge result</td></tr><tr><td>Operational measures</td><td>Time, errors, usage</td><td>Time, errors, usage</td></tr></tbody></table>

<!--
Teach the alignment before opening EvalTables. Compare the complete booking state; do not substitute a tag result for deterministic correctness. Match source IDs and execution fingerprints.
-->

---
name: capture-evaltables
---

<div class="kicker">4:59 · Airline service monitoring</div>

# Set the starting agent as the comparison reference

<div class="native-view " style="grid-template-columns:760px minmax(0,1fr)"><div class="native-image" style="aspect-ratio:620/190"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1"><img style="position:absolute;width:206.4516129032258%;height:auto;max-width:none;left:-16.129032258064516%;top:-126.3157894736842%;" src="/captures/native-evaltables.png" alt="Actual native EvalTables development comparison with the starting version marked Reference and task success of 100 percent for both versions."></a><span class="native-pin" style="left:30.941935483870974%;top:11.621052631578939%">1</span><span class="native-pin" style="left:47.04516129032258%;top:74.14736842105263%">2</span></div><div class="native-notes"><p><b>1 · Reference version</b><br>Keep the starting agent selected so the other version is compared with it.</p><p><b>2 · Same task score</b><br>Both passed all four development cases. Read the individual requests before interpreting the average.</p></div></div><p class="caption">Native development comparison, verified by server readback: four matched requests per version. The two 100% bars are a tie. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1">Open the recorded view ↗</a></p>

<!--
Choose an identical case in the two versions. Read the state scores, output booking, judgment status, and trace links. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: capture-evaltables-case
---

<div class="kicker">5:02 · Airline service monitoring</div>

# Read both outputs for the same request

<div class="native-view stacked" style="grid-template-columns:1fr"><div class="native-image" style="aspect-ratio:1160/200"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1"><img style="position:absolute;width:110.34482758620689%;height:auto;max-width:none;left:-8.620689655172415%;top:-237.5%;" src="/captures/native-evaltables.png" alt="Aligned native EvalTables row showing the same case identifier and request, separate starting and repaired replies, and passing task scores."></a><span class="native-pin" style="left:4.400000000000002%;top:79.30000000000001%">1</span><span class="native-pin" style="left:39.04827586206897%;top:70.30000000000001%">2</span><span class="native-pin" style="left:81.64137931034482%;top:79.30000000000001%">3</span></div><div class="native-notes"><p><b>1 · Matching input</b><br>One case ID and request align the two executions.</p><p><b>2 · Separate outputs</b><br>Read each saved reply; matching scores do not mean identical behavior.</p><p><b>3 · Independent task checks</b><br>Both passed. Follow the row to the booking and trace to explain why.</p></div></div><p class="caption">Recorded airline-development-04: a one-way booking lookup. This is a different request from the opening itinerary change. <a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=4wzxelfxod1">Open the recorded view ↗</a></p>

<!--
Identify the shared input and the separate predictions. Open the underlying booking and native trace before explaining a passing score. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.
-->

---
name: recorded-results
---

<div class="kicker">5:05 · Airline service monitoring</div>

# The recorded agent comparison was a tie

<table class="monitor-table "><thead><tr><th>Reserved requests</th><th>Starting agent</th><th>Agent with itinerary builder</th></tr></thead><tbody><tr><td>Final evaluation</td><td>6 / 6 task checks passed</td><td>6 / 6 task checks passed</td></tr><tr><td>Subsequent traffic</td><td>4 / 4 task checks passed</td><td>4 / 4 task checks passed</td></tr></tbody></table><p>All 40 qualification conversations passed their task checks. The live agent did not reproduce the missing-return defect.</p><p class="caption">The labeled local adapter drill demonstrates the repair mechanism separately. Native Alignment judging was unavailable, so this result says nothing about monitor accuracy.</p>

<!--
Preserve the successful baseline. Do not describe the helper as improving task quality on this rehearsal. The controlled drill is a real code repair, but it is not a spontaneous agent failure. These small simulated batches do not estimate production reliability.
-->

---
name: report-measures
---

<div class="kicker">5:08 · Airline service monitoring</div>

# Report denominators and unresolved work

<table class="monitor-table "><thead><tr><th>Measure</th><th>Report together</th></tr></thead><tbody><tr><td>Requested changes completed</td><td>Passed cases / scored cases; unavailable cases</td></tr><tr><td>Unrequested changes</td><td>Count and the affected segment</td></tr><tr><td>Monitoring accuracy</td><td>Reviewed precision, recall, and coverage</td></tr><tr><td>Explanation quality</td><td>Judged rows and missing judgments</td></tr><tr><td>Operational cost</td><td>Known cost, bounded unknown usage, native tag cost status</td></tr></tbody></table>

<!--
A six-case comparison has limited reach. Show each failure and avoid a general claim that monitoring improves all agents. If all cases tie, inspect whether behavior or cost changed while correctness stayed equal.
-->

---
name: subsequent
---

<div class="kicker">5:20 · Airline service monitoring</div>

# Use later traffic to check the frozen monitor

<div class="pipeline"><div class="">Four new requests<small>Reserved from development</small></div><b v-click="1">→</b><div v-click="1" class="">Two isolated versions<small>Same original booking per pair</small></div><b v-click="2">→</b><div v-click="2" class="">Same saved tag<small>Frozen criteria</small></div><b v-click="3">→</b><div v-click="3" class="">Read judgments<small>Coverage and disagreements</small></div></div><p>This is a bounded subsequent traffic batch. It is not a production rollout or proof of performance under changing real traffic.</p>

<!--
The subsequent batch is separate from the six final requests. Do not tune the monitor after seeing one version’s outcomes. Read the differences between state outcomes and tag classifications.
-->

---
class: exercise
name: traffic
---

<div class="kicker">5:26 · Airline service monitoring</div>

# Check what the monitor catches after the repair

<p class="where">Notebook → Monitor subsequent requests</p><div class="task-target">Edit my_monitor</div><ol><li>Run both versions on the subsequent batch.</li><li>Read tag results after native processing completes.</li><li>Inspect at least one tagged and one untagged request.</li></ol><div class="done"><b>Run:</b> Monitor four subsequent requests → Read the subsequent batch's tag results<br><b>Finished when:</b> You can distinguish fewer booking failures from fewer judgments being available.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: alerts
---

<div class="kicker">5:37 · Airline service monitoring</div>

# A falling alert count has several explanations

<div class="bundle-list"><div>Fewer task failures<small>Confirm with reviewed booking states</small></div><div>Lower processing coverage<small>Check pending and failed tag judgments</small></div><div>A changed request mix<small>Compare the batch and reservation families</small></div><div>A changed rule<small>Compare the saved criteria snapshot</small></div></div>

<!--
Ask participants to rule out each explanation with the records. A workshop that simply celebrates a downward chart has skipped the measurement problem it was meant to teach.
-->

---
name: conclusion
---

<div class="kicker">5:45 · Airline service monitoring</div>

# Write down what changed and whether it helped

<div class="timeline-list"><b>Agent</b><span>Which booking outcomes changed on matched requests?</span><b>Monitor</b><span>Which failures did the reviewed rule find or miss?</span><b>Evaluation</b><span>Which new check would catch this problem before release?</span><b>Next test</b><span>What remains uncertain, and which request would test it?</span></div>

<!--
The participant conclusion should cite one actual case and its exact code, booking, trace, and evaluation. Improvements are welcome; a documented tie or regression also completes the lesson.
-->

---
class: exercise
name: report
---

<div class="kicker">5:50 · Airline service monitoring</div>

# Publish the comparison and stop automatic judging

<p class="where">Notebook → Write the conclusion</p><div class="task-target">Edit The saved report and tag readback</div><ol><li>Publish saved comparisons; retry missing exports without rerunning requests.</li><li>Write the conclusion with one supporting case and one remaining failure.</li><li>Disable the workshop tag, then verify its native state.</li></ol><div class="done"><b>Run:</b> Publish saved comparisons → Publish my conclusion → Verify automatic tagging is off<br><b>Finished when:</b> The Report opens its supporting evidence, and automatic judging is confirmed off.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: end
---

<div class="kicker">5:58 · Airline service monitoring</div>

# The next release has a check the first release lacked

<p class="principle">You can point to a passenger request, the booking change, the monitoring decision, and the regression check that tests it again.</p><p>The final comparison tells you whether this repair is worth keeping. The next incident may need a different rule.</p>

<!--
End by asking someone to reproduce a case from its saved initial state. Do not conclude with a promise of autonomous improvement. Monitoring, human review, and offline evaluation each answered a different question.
-->

---
class: answer
name: answer-judge
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: validate a judge response

```python {all}
def my_judge_validation(answer):
    if any(type(answer.get(k)) is not bool for k in ("supported", "unresolved")):
        raise ValueError("supported and unresolved must be booleans")
    if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
        raise ValueError("Explain the judgment")
    if not isinstance(answer.get("event_ids"), list) or any(
        not isinstance(x, str) for x in answer["event_ids"]
    ):
        raise ValueError("Cite event identities as a list of strings")
    return answer
```
<p class="source-link"><a href="/54">Return to the explanation-judge exercise ↗</a></p>

<!--
This is the notebook’s actual validator. It checks shape and types, not the truth of the judgment.
-->

---
class: answer
name: answer-monitor
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: keep unknown judgments out of the matrix

```python {all}
def my_monitor(rows):
    completed = [r for r in rows if r.get("status") == "complete"
        and type(r.get("prediction")) is bool]
    known = [r for r in completed if type(r.get("human_label")) is bool]
    tp = sum(r["prediction"] and r["human_label"] for r in known)
    fp = sum(r["prediction"] and not r["human_label"] for r in known)
    fn = sum(not r["prediction"] and r["human_label"] for r in known)
    return {"total": len(rows), "judged": len(completed), "reviewed": len(known),
        "coverage": len(completed) / len(rows) if rows else None,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "unavailable": len(rows) - len(completed)}
```
<p class="source-link"><a href="/37">Return to monitoring calculations ↗</a></p>

<!--
This is the notebook’s actual my_monitor implementation. Review unflagged cases too; an alerts-only sample cannot establish recall across traffic.
-->

---
class: answer
name: answer-case
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: preserve the original case inputs

<div class="bundle-list"><div>Copy the initial booking<small>A deep copy prevents later mutations changing the test</small></div><div>Keep request and policy<small>Preserve the rules used by this execution</small></div><div>Attach the reviewed expectation<small>Include scope, result, reviewer, and rationale</small></div><div>Retain native identities<small>Link back to the conversation and supporting span</small></div></div><p class="source-link"><a href="/42">Return to the curation exercise ↗</a></p>

<!--
Use the actual case_from_reviewed_turn signature in the notebook. Do not synthesize a nonexistent native turn or treat a listing of spans as proof that a specific diagnostic was read.
-->

---
class: answer
name: answer-state
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: check both change and preservation

```python {all}
requested_change = actual[start:start + len(replacement)] == replacement
untouched_prefix = actual[:start] == original[:start]
untouched_suffix = actual[start + len(replacement):] == original[stop:]
booking_correct = requested_change and untouched_prefix and untouched_suffix
```
<p>Compare flight identities and relevant fields, not only list length. Keep confirmation and policy checks alongside these state checks.</p><p class="source-link"><a href="/45">Return to the state scorer exercise ↗</a></p>

<!--
Illustrative list-based scorer excerpt. The actual evaluator must use the recorded approved scope and final state, not values inferred from the agent’s final response.
-->

---
class: answer
name: answer-builder
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: build the complete replacement list

```python {all}
def my_itinerary_builder(
    current_flights, replace_start, replace_stop, replacement_flights
):
    if type(replace_start) is not int or type(replace_stop) is not int:
        raise ValueError("Flight indices must be integers")
    if not 0 <= replace_start < replace_stop <= len(current_flights) or not replacement_flights:
        raise ValueError("Choose an existing range and a nonempty replacement")
    return copy.deepcopy(
        current_flights[:replace_start] + replacement_flights
        + current_flights[replace_stop:]
    )
```
<p class="source-link"><a href="/51">Return to the repair exercise ↗</a></p>

<!--
This is the notebook’s actual itinerary builder. The deep copy prevents the result from mutating the original booking. The agent must still select the correct range and obtain confirmation.
-->

---
name: sources
---

<div class="kicker">Reference · Airline service monitoring</div>

# Sources and saved evidence

<ul class="reference-list"><li><a href="https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view">Hosted notebook template — copy into your project</a></li><li><a href="https://github.com/sierra-research/tau2-bench/blob/989d3285ae669e49503324bdb9981bf14fccedeb/src/tau2/domains/airline/tools.py">Pinned airline API implementation</a></li><li><a href="https://github.com/sierra-research/tau2-bench/blob/989d3285ae669e49503324bdb9981bf14fccedeb/data/tau2/domains/airline/">Source airline data and policy</a></li><li><a href="https://docs.coreweave.com/products/agent-lens/tags/create-tag">Native Agent Lens tags and judging criteria</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit">Source, data provenance, local checks, and release status</a></li></ul><p class="caption">Recorded captures have their original image, source URL, selected record, and annotations in this deck’s source package. No paid work runs when this deck opens.</p>

<!--
Consult the release evidence for actual validation coverage. External-account access and human rehearsal are not established by a successful deck build.
-->
