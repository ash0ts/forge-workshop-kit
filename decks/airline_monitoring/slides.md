---
theme: default
title: Monitor an airline service agent and build better evaluations
author: Anish Shah
class: cover workshop-setting-slide
clicks: 1
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

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="airline_monitoring/start"><img :src="&quot;/scenes/airline_monitoring/start.svg&quot;" alt="Airline booking operations: Keep both journeys visible while changing the booking. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="sub">Investigate booking mistakes, test a monitoring rule, and turn reviewed incidents into checks for the next version.</div><div class="bottom-note">Six hours · Basic Python · Simulated airline data · Your own Forge project<br>Technical preview: native Alignment judging and prepared Insights remain unqualified.</div></div>

<!--
Set the situation before introducing products. Participants operate a simulated airline customer-service agent. They will distinguish a request completing, a booking being correct, and a monitor detecting a problem. Those are three separate observations.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
class: technical-manual
name: technical-overview
clicks: 4
---

<div class="kicker">0:03 · Airline service monitoring</div>

# What you will build and inspect

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;booking&quot;, &quot;label&quot;: &quot;Booking&quot;, &quot;svg&quot;: &quot;01-booking.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/overview/slide/01-booking.svg&quot;}, {&quot;id&quot;: &quot;observe&quot;, &quot;label&quot;: &quot;Observe&quot;, &quot;svg&quot;: &quot;02-observe.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/overview/slide/02-observe.svg&quot;}, {&quot;id&quot;: &quot;monitor&quot;, &quot;label&quot;: &quot;Monitor&quot;, &quot;svg&quot;: &quot;03-monitor.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/overview/slide/03-monitor.svg&quot;}, {&quot;id&quot;: &quot;test&quot;, &quot;label&quot;: &quot;Test&quot;, &quot;svg&quot;: &quot;04-test.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/overview/slide/04-test.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/overview/slide/05-complete.svg&quot;}]" :step="$clicks" />

<!--
Introduce the real task, the data available, and the outcome participants will check. Point to each Forge product at the operation it helps investigate.
Visual guide: airline_monitoring/overview. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
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
class: technical-manual
name: replace-semantics
clicks: 3
---

<div class="kicker">0:09 · Airline service monitoring</div>

# Replace the requested flights and keep the rest

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;before&quot;, &quot;label&quot;: &quot;Before&quot;, &quot;svg&quot;: &quot;01-before.svg&quot;, &quot;caption&quot;: &quot;What must the booking update contain?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/itinerary/slide/01-before.svg&quot;}, {&quot;id&quot;: &quot;replace&quot;, &quot;label&quot;: &quot;Replace&quot;, &quot;svg&quot;: &quot;02-replace.svg&quot;, &quot;caption&quot;: &quot;What must the booking update contain?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/itinerary/slide/02-replace.svg&quot;}, {&quot;id&quot;: &quot;after&quot;, &quot;label&quot;: &quot;After&quot;, &quot;svg&quot;: &quot;03-after.svg&quot;, &quot;caption&quot;: &quot;What must the booking update contain?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/itinerary/slide/03-after.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;What must the booking update contain?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/itinerary/slide/04-complete.svg&quot;}]" :step="$clicks" />

<!--
A successful write says the replacement was accepted. It does not establish that the proposed replacement respected the passenger’s request. Read the upstream implementation and the workshop adapter together.

Visual sequence: Trace HAT174 through both candidate API inputs. The assignment replaces the list, so the missing-return branch cannot preserve a flight it did not receive. This is an illustrative failure mechanism; the live qualification handled its bookings correctly.
Visual guide: airline_monitoring/itinerary. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
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
clicks: 2
---

<div class="kicker">0:18 · Airline service monitoring</div>

# Keep related bookings in the same data group

<AirlineMechanism mode="families" :reveal="$clicks + 1" />

<!--
These are the approved execution counts, totalling 40 conversations. Development and final comparisons run the same requests once on each version. Upstream task identities overlap, so splitting task rows alone would leak related bookings.

Visual sequence: Start with the family bracket, not the batch counts. The connected dots stand for related records, not three named passengers. Reveal the assigned groups, then show why putting a related task in final evaluation leaks the family across partitions. The counts are the actual frozen plan.
-->

---
class: workshop-sharing
name: setup
---

<div class="kicker">0:21 · Airline service monitoring</div>

# Open the materials and copy the notebook

<div class="workshop-share-layout"><div class="workshop-share-instructions"><ol><li><strong>Open this workshop’s page.</strong> Scan the code or type the short link.</li><li><strong>Choose the notebook.</strong> Sign in to Forge, then choose <strong>Copy to project</strong>.</li><li><strong>Open your copy in Edit.</strong> Run all stale cells once to initialize the controls.</li><li><strong>Check the destination.</strong> Use your own writable project and account.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuIab" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuIab">utm.io/uuIab</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The $8 adjustable allowance covers notebook inference. Notebook compute is billed separately. Native tag judging has separate charges.</p>

<!--
Leave this QR code visible while participants open the workshop page. It links the current notebook, Report, deck, and run guide. Choose Notebook, sign in, then copy into a writable project. Continue to the existing setup exercise. The short link is managed in docs/share-links.json; do not reuse a historical event QR.
-->

---
class: exercise
name: booking
---

<div class="kicker">0:25 · Airline service monitoring</div>

# Try the replacement API, then connect your project

<p class="where">Notebook → Inspect the booking</p><div class="task-target">Edit your expected booking explanation</div><ol><li>The notebook starts with Sofia: New York → Phoenix → Las Vegas, reservation 4BMN53. Replace HAT201 with HAT002; keep HAT173.</li><li>Try the local booking change. Compare approval and the complete trip; this controlled API drill bypasses confirmation.</li><li>Connect your project, then save what should change and what must remain.</li></ol><div class="done"><b>Run:</b> Try the booking change locally → Connect and restore my work → Save my expected booking<br><b>Finished when:</b> You can name the changed range and the flight that must survive.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
class: technical-manual
name: trace-shape
clicks: 3
---

<div class="kicker">0:29 · Airline service monitoring</div>

# Follow the passenger’s request through the write

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;request&quot;, &quot;label&quot;: &quot;Request&quot;, &quot;svg&quot;: &quot;01-request.svg&quot;, &quot;caption&quot;: &quot;Where can you see what the tool actually changed?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/traces/slide/01-request.svg&quot;}, {&quot;id&quot;: &quot;tool&quot;, &quot;label&quot;: &quot;Tool&quot;, &quot;svg&quot;: &quot;02-tool.svg&quot;, &quot;caption&quot;: &quot;Where can you see what the tool actually changed?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/traces/slide/02-tool.svg&quot;}, {&quot;id&quot;: &quot;state&quot;, &quot;label&quot;: &quot;State&quot;, &quot;svg&quot;: &quot;03-state.svg&quot;, &quot;caption&quot;: &quot;Where can you see what the tool actually changed?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/traces/slide/03-state.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Where can you see what the tool actually changed?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/traces/slide/04-complete.svg&quot;}]" :step="$clicks" />

<!--
A conversation may contain several turns. Do not collapse unrelated requests into a single conversation. The passenger’s clarification and confirmation belong with the relevant turn evidence. Use native session and span identities from execution.

Visual sequence: Read the parent tree alongside operation order. Both model calls and both tool attempts remain children of their turn. Bar width is schematic, not measured latency. Ask participants which event needs the error and which needs the returned reservation; then map them to my_model_span and my_tool_span.
Visual guide: airline_monitoring/traces. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
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

# Instrument the agent and inspect one request

<p class="where">Notebook → Run discovery traffic</p><div class="task-target">Edit my_model_span and my_tool_span</div><ol><li>Add version and traffic-batch attributes to the scopes.</li><li>Keep tool arguments, result, error, and actual timing.</li><li>Run Sofia’s request, then find the preserved Phoenix–Las Vegas connection in its trace.</li></ol><div class="done"><b>Run:</b> Check my tracing code → Send my first Agent Lens trace → Run the first discovery request<br><b>Finished when:</b> Find the same itinerary in the tool receipt and its stored Agent Lens span.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: read-tool
clicks: 3
---

<div class="kicker">0:48 · Airline service monitoring</div>

# Read the booking returned by the tool

<AirlineMechanism mode="loop" :reveal="$clicks + 1" />

<!--
Give everyone several minutes on one conversation. For the first request, ask them to find Sofia’s PHX–LAS connection, HAT173. The earlier diagram used a separate round-trip discovery booking, 59XX6W. In either case, inspect the untouched flight rather than merely an exception field. If the agent was correct, record that success and continue with the labeled calibration drill for the diagnostic exercise.

Visual sequence: Follow one chosen action through arguments, the state write, the observation, and the next request. The returned booking must be appended before the next model call. Ask participants to locate that exact observation in Agent Lens; the final reply alone cannot prove what the model received.
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
class: exercise
name: remaining-discovery
---

<div class="kicker">0:57 · Airline service monitoring</div>

# Continue with the other seven requests

<p class="where">Notebook → Run discovery traffic</p><div class="task-target">Reuse the saved tracing functions</div><ol><li>Inspect the first booking and the API arguments before continuing.</li><li>Run the remaining seven cases with the saved tracing implementation.</li><li>Compare an ordinary outcome with a recovered error or unresolved request.</li></ol><div class="done"><b>Run:</b> Run the remaining seven discovery requests<br><b>Finished when:</b> Eight case identities are saved. Reopening reuses completed requests.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
class: workshop-setting-slide
name: three-questions
clicks: 1
---

<div class="kicker">0:58 · Airline service monitoring</div>

# Keep three questions separate

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="airline_monitoring/inspect"><img :src="&quot;/scenes/airline_monitoring/inspect.svg&quot;" alt="Airline booking operations: Tool execution, booking quality, and monitor detection differ. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><table class="monitor-table "><thead><tr><th>Question</th><th>Evidence</th><th>Possible outcome</th></tr></thead><tbody><tr><td>Did the tool execute?</td><td>Tool result, error, duration</td><td>Returned normally</td></tr><tr><td>Did it do the requested work?</td><td>Original and final booking</td><td>Return flight was removed</td></tr><tr><td>Did the monitor detect that?</td><td>Reviewed tag result</td><td>Missed, found, or not processed</td></tr></tbody></table></div>

<!--
Use the same example across all three questions. A lower tool-error rate does not prove higher booking quality. A high tag count may mean more failures, broader criteria, or a different processing denominator.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
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
class: exercise
name: review
---

<div class="kicker">1:36 · Airline service monitoring</div>

# Review the booking before asking a tag to judge it

<p class="where">Notebook → Review booking outcomes</p><div class="task-target">Edit your human turn review</div><ol><li>Read the selected passenger request and before/after booking together.</li><li>Label an unrequested change, no unrequested change, or insufficient evidence.</li><li>Save the exact supporting operation, reason, and expected behavior.</li></ol><div class="done"><b>Run:</b> Save my turn review<br><b>Finished when:</b> A reviewed label links to the same turn and operation. Saving it does not complete monitoring.</div>

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
class: aria-investigation
name: aria-investigate
---

<div class="kicker">1:50 · 8 minutes across these three frames · Airline service monitoring</div>

# Investigate this result

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">Does this turn establish an unrequested itinerary change?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae" target="_blank" rel="noopener">airline-discovery-02 ↗</a></li></ul></div></div><p class="aria-foot">Use only the selected development or validation records. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-investigate-response
---

<div class="kicker">1:50 · 8 minutes across these three frames · Airline service monitoring</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-response.png" target="_blank"><img src="/aria/investigate/investigate-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>no unrequested itinerary change observed</blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/investigate/investigate-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e072-9033-7900-836d-bc3c4f5cc719" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-investigate-verify
---

<div class="kicker">1:50 · 8 minutes across these three frames · Airline service monitoring</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-verification.png" target="_blank"><img src="/aria/investigate/investigate-verification.png" alt="The returned reservation contains the new HAT061 outbound and the unchanged HAT174 return."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="648.0" y="423.0" width="580.0" height="101.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="634.0" cy="436.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="634.0" y="440.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="648.0" y="548.0" width="580.0" height="100.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="634.0" cy="561.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="634.0" y="565.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> Changed outbound flight</span><span><b>2</b> Return flight retained</span></figcaption></figure><div><b>Citation check: supported</b><p>The saved airline-discovery-02 booking starts with HAT007 outbound and HAT174 return; its update_reservation_flights result contains HAT061 on May 19 and HAT174 on May 29. The native verification capture shows these returned flights. The actual trace also has confirmation before the write. This supports the reviewed booking outcome, not a claim that native monitoring processed the turn.</p><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/3673f9ec7c917166a808d6473195a2ae" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/investigate/investigate-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
name: tag-definition
---

<div class="kicker">1:58 · Airline service monitoring</div>

# Define a behavior that a reviewer can check

<div class="callout"><b>Unrequested itinerary change</b><br>The agent changed or removed a flight outside the passenger’s approved change.</div><p>Judge the requested scope, the action, and the resulting reservation together. A shorter itinerary alone is not enough.</p>

<!--
The initial proposed criterion is intentionally a starting hypothesis for alignment, not a validated native rule. Participants must review what evidence exists in each turn. Requests may authorize replacing the entire itinerary.
-->

---
name: counterexample-nonstop
clicks: 2
---

<div class="kicker">1:59 · Airline service monitoring</div>

# Fewer flights can be the correct result

<AirlineMechanism mode="nonstop" :reveal="$clicks + 1" />

<!--
This is the central counterexample to a naive flight-count rule. Ask the room whether changing three segments to two is sufficient evidence of failure. It is not.

Visual sequence: The connecting point disappears while the origin, destination, and return remain. Ask whether fewer segments is a failure before revealing the approved nonstop. The answer depends on the request, not the count. These segment names and airport positions are illustrative.
-->

---
name: counterexamples
---

<div class="kicker">2:00 · Airline service monitoring</div>

# Add counterexamples before trusting the rule

<table class="monitor-table "><thead><tr><th>Example</th><th>What the criterion must account for</th></tr></thead><tbody><tr><td>A one-way booking</td><td>There was never a return flight to preserve.</td></tr><tr><td>An explicitly approved full-itinerary change</td><td>All original flights may legitimately be replaced.</td></tr><tr><td>A failed write followed by successful recovery</td><td>Judge the resolved state and the turn’s scope.</td></tr><tr><td>A request waiting for confirmation</td><td>No write has been approved yet.</td></tr><tr><td>Missing original booking</td><td>Insufficient evidence is not a negative finding.</td></tr></tbody></table>

<!--
Human review comes before this optional calibration pack. Create six controlled calibration traces only after saving a booking review. Use actual reviewed turns when available. The calibration pack is a labeled teaching fallback, not a claim about the learner’s live failure rate. Keep all disagreements and their reasons.
-->

---
class: technical-manual
name: tag-lifecycle
clicks: 5
---

<div class="kicker">2:05 · Airline service monitoring</div>

# Test the monitoring rule against reviewed turns

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;review&quot;, &quot;label&quot;: &quot;Review&quot;, &quot;svg&quot;: &quot;01-review.svg&quot;, &quot;caption&quot;: &quot;Would the rule distinguish an omission from a valid itinerary change?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/01-review.svg&quot;}, {&quot;id&quot;: &quot;criteria&quot;, &quot;label&quot;: &quot;Criteria&quot;, &quot;svg&quot;: &quot;02-criteria.svg&quot;, &quot;caption&quot;: &quot;Would the rule distinguish an omission from a valid itinerary change?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/02-criteria.svg&quot;}, {&quot;id&quot;: &quot;alignment&quot;, &quot;label&quot;: &quot;Alignment&quot;, &quot;svg&quot;: &quot;03-alignment.svg&quot;, &quot;caption&quot;: &quot;Would the rule distinguish an omission from a valid itinerary change?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/03-alignment.svg&quot;}, {&quot;id&quot;: &quot;status&quot;, &quot;label&quot;: &quot;Status&quot;, &quot;svg&quot;: &quot;04-status.svg&quot;, &quot;caption&quot;: &quot;Would the rule distinguish an omission from a valid itinerary change?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/04-status.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;Would the rule distinguish an omission from a valid itinerary change?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/05-complete.svg&quot;}, {&quot;id&quot;: &quot;native-capture&quot;, &quot;label&quot;: &quot;Tag criteria and judging&quot;, &quot;svg&quot;: &quot;06-native-capture.svg&quot;, &quot;caption&quot;: &quot;Read the criteria, automatic-judging switch, and agent filter. This recorded tag was disabled after qualification.&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/alignment/slide/06-native-capture.svg&quot;}]" :step="$clicks" />

<!--
Walk through native Tags and Alignment. Creating or editing a notebook rubric is not the same action as saving native tag criteria. Use the native identities in the readback record.

Visual sequence: Keep the right-hand saved criterion in place while the Alignment draft is tested. Only the final explicit-save arrow changes live criteria. A failed Alignment test produces no judgment; it does not silently disable, update, or validate the saved live rule.
Visual guide: airline_monitoring/alignment. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
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
clicks: 2
---

<div class="kicker">2:10 · Airline service monitoring</div>

# Turn context limits what the judge can know

<AirlineMechanism mode="context" :reveal="$clicks + 1" />

<!--
Native judges see turn-level evidence. Do not assume every model span contains the entire conversation. The context inspection is part of the exercise; a fluent judge reason does not create missing evidence.

Visual sequence: The selected turn has a write and a reply but lacks the earlier booking. Ask which evidence establishes a return was removed. In this illustrated context it is unavailable. A reviewer with the full conversation knows more than the turn-level judge; keep that context difference in the review record.
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
clicks: 2
---

<div class="kicker">2:35 · Airline service monitoring</div>

# Measure the monitor on reviewed cases

<AirlineMechanism mode="confusion" :reveal="$clicks + 1" />

<!--
Walk through one cell at a time. The human review is the reference for this calculation; disagreement remains open to correction. Unavailable judgments are excluded from these eight processed rows and reported separately.

Visual sequence: Reveal the true positives, false positive, and remaining cells in place. Human review supplies the reference labels. These eight rows are illustrative arithmetic and not a successful native Alignment result. No unavailable prediction enters this matrix.
-->

---
name: precision
clicks: 1
---

<div class="kicker">2:39 · Airline service monitoring</div>

# Precision asks whether an alert deserves review

<AirlineMechanism mode="precision" :reveal="$clicks + 1" />

<!--
The denominator is the tagged turns with a reviewed label, not all requests. Alert count cannot tell us how many failures were missed. Ask which example produced the false positive.

Visual sequence: The outlined row is the denominator: all four reviewed alerts. Three are reviewed failures. The faded second row is irrelevant to precision but needed for recall. If there are no alerts, leave precision unavailable. This graphic does not describe native workshop outcomes.
-->

---
name: recall
clicks: 1
---

<div class="kicker">2:42 · Airline service monitoring</div>

# Recall asks which failures the monitor missed

<AirlineMechanism mode="recall" :reveal="$clicks + 1" />

<!--
Precision and recall happen to match in this arithmetic example, but they use different denominators. Show the missed failure cell. Review sampling affects whether these values estimate the wider traffic population.

Visual sequence: The outlined column is the denominator: all four reviewed failures. One was not alerted. The same 75 percent hides a different question from precision. Review unflagged controls so this missed-failure cell can be populated. The arithmetic remains illustrative.
-->

---
class: technical-manual
name: coverage
clicks: 3
---

<div class="kicker">2:45 · Airline service monitoring</div>

# Count what the monitor has actually processed

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;incoming&quot;, &quot;label&quot;: &quot;Incoming&quot;, &quot;svg&quot;: &quot;01-incoming.svg&quot;, &quot;caption&quot;: &quot;What is the denominator of each monitoring number?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/coverage/slide/01-incoming.svg&quot;}, {&quot;id&quot;: &quot;coverage&quot;, &quot;label&quot;: &quot;Coverage&quot;, &quot;svg&quot;: &quot;02-coverage.svg&quot;, &quot;caption&quot;: &quot;What is the denominator of each monitoring number?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/coverage/slide/02-coverage.svg&quot;}, {&quot;id&quot;: &quot;agreement&quot;, &quot;label&quot;: &quot;Agreement&quot;, &quot;svg&quot;: &quot;03-agreement.svg&quot;, &quot;caption&quot;: &quot;What is the denominator of each monitoring number?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/coverage/slide/03-agreement.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;What is the denominator of each monitoring number?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/coverage/slide/04-complete.svg&quot;}]" :step="$clicks" />

<!--
A missing tag is not enough to identify a completed negative judgment. Read processing status and identities. Keep pending, failed, insufficient-context, and scored states separate as supported by the recorded events.

Visual sequence: Count the eight completed predictions, then divide by all ten eligible turns. Only after that do we join completed predictions to human reviews for the agreement matrix. The two question marks remain unknown. Positive live assignments by themselves cannot establish this denominator.
Visual guide: airline_monitoring/coverage. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---
class: exercise
name: monitor
---

<div class="kicker">2:50 · Airline service monitoring</div>

# Calculate monitor quality and send new traffic

<a class="answer-link" href="/79">Worked answer ↗</a>

<p class="where">Notebook → Check monitoring on new requests</p><div class="task-target">Edit my_monitor</div><ol><li>Compute precision and recall using reviewed, processed turns.</li><li>Compute coverage over eligible turns, retaining missing judgments.</li><li>Enable the saved tag for this workspace’s agent and run the monitor-check batch.</li></ol><div class="done"><b>Run:</b> Check my monitoring calculations → Run four new requests → Read tag results → Calculate agreement with my reviews<br><b>Finished when:</b> You can explain every denominator and name any turns still awaiting judgment.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
name: live-missingness
clicks: 2
---

<div class="kicker">3:00 · Airline service monitoring</div>

# A missing live tag does not establish a negative judgment

<AirlineMechanism mode="missing" :reveal="$clicks + 1" />

<!--
Keep the live assignment view separate from the explicit Alignment-test result set. Do not infer processing coverage from positive assignments alone. Record the denominator and native result source beside any calculated rate.

Visual sequence: All three branches can produce the same absent live tag. Ask what readback distinguishes them. Explicit native test outcomes can establish known positive and negative predictions; a blank assignment cannot. Keep pending, failed, and missing context separate where native records support them.
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
class: workshop-setting-slide
name: curation
clicks: 3
---

<div class="kicker">3:10 · Airline service monitoring</div>

# A reviewed turn becomes a regression case

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="airline_monitoring/build"><img :src="&quot;/scenes/airline_monitoring/build.svg&quot;" alt="Airline booking operations: Keep the initial booking, request, policy, and reviewed expectation. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><AirlineMechanism mode="curation" :reveal="(Math.max(0, $clicks - 1)) + 1" /></div>

<!--
Make curation an explicit code exercise. The case contains the original booking, not the already-mutated booking that caused the complaint. Keep the exact request and constraints with it.

Visual sequence: The arrow into the regression case comes from before the write. The crossed arrow from the mutated booking explains a common reconstruction error. Keep the request, policy, approved scope, human review, and source identities with the initial state. This omission incident is a labeled illustration, not an invented live failure.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
class: technical-manual
name: case-fields
clicks: 3
---

<div class="kicker">3:15 · Airline service monitoring</div>

# Reconstruct an incident as an executable test

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;source&quot;, &quot;label&quot;: &quot;Source&quot;, &quot;svg&quot;: &quot;01-source.svg&quot;, &quot;caption&quot;: &quot;What must be saved to replay the same situation?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/regression/slide/01-source.svg&quot;}, {&quot;id&quot;: &quot;case&quot;, &quot;label&quot;: &quot;Case&quot;, &quot;svg&quot;: &quot;02-case.svg&quot;, &quot;caption&quot;: &quot;What must be saved to replay the same situation?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/regression/slide/02-case.svg&quot;}, {&quot;id&quot;: &quot;checks&quot;, &quot;label&quot;: &quot;Checks&quot;, &quot;svg&quot;: &quot;03-checks.svg&quot;, &quot;caption&quot;: &quot;What must be saved to replay the same situation?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/regression/slide/03-checks.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;What must be saved to replay the same situation?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/regression/slide/04-complete.svg&quot;}]" :step="$clicks" />

<!--
Ask what happens if someone saves only the final reply. They cannot reconstruct the original itinerary or determine what was unrequested. These records are public simulated examples; the same technique with real passengers needs an appropriate privacy review.
Visual guide: airline_monitoring/regression. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---
class: exercise
name: curate
---

<div class="kicker">3:22 · Airline service monitoring</div>

# Build a regression case from the reviewed turn

<a class="answer-link" href="/80">Worked answer ↗</a>

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

<a class="answer-link" href="/81">Worked answer ↗</a>

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
clicks: 2
---

<div class="kicker">4:10 · Airline service monitoring</div>

# Walk through the values before running the model

<AirlineMechanism mode="slice" :reveal="$clicks + 1" />

<!--
This is a free, simplified arithmetic check. It establishes the list transformation, not whether the model selected the correct segment range or received passenger confirmation.

Visual sequence: Point to index two: the half-open replacement stops before return-1. First expose the index range, then the empty prefix, replacement, and untouched suffix. The last line is the participant function’s list operation. Their free check also validates bounds and copies the data.
-->

---
class: exercise
name: repair
---

<div class="kicker">4:15 · Airline service monitoring</div>

# Test the repair on matched development bookings

<a class="answer-link" href="/82">Worked answer ↗</a>

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

<a class="answer-link" href="/78">Worked answer ↗</a>

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
class: technical-manual
name: aligned-comparison
clicks: 4
---

<div class="kicker">4:54 · Airline service monitoring</div>

# Compare the agent and monitor on matching requests

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;freeze&quot;, &quot;label&quot;: &quot;Freeze&quot;, &quot;svg&quot;: &quot;01-freeze.svg&quot;, &quot;caption&quot;: &quot;Did the repair improve bookings, monitoring, or both?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/comparison/slide/01-freeze.svg&quot;}, {&quot;id&quot;: &quot;matched&quot;, &quot;label&quot;: &quot;Matched&quot;, &quot;svg&quot;: &quot;02-matched.svg&quot;, &quot;caption&quot;: &quot;Did the repair improve bookings, monitoring, or both?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/comparison/slide/02-matched.svg&quot;}, {&quot;id&quot;: &quot;traffic&quot;, &quot;label&quot;: &quot;Traffic&quot;, &quot;svg&quot;: &quot;03-traffic.svg&quot;, &quot;caption&quot;: &quot;Did the repair improve bookings, monitoring, or both?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/comparison/slide/03-traffic.svg&quot;}, {&quot;id&quot;: &quot;recorded&quot;, &quot;label&quot;: &quot;Recorded&quot;, &quot;svg&quot;: &quot;04-recorded.svg&quot;, &quot;caption&quot;: &quot;Did the repair improve bookings, monitoring, or both?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/comparison/slide/04-recorded.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;Did the repair improve bookings, monitoring, or both?&quot;, &quot;src&quot;: &quot;/guides/airline_monitoring/comparison/slide/05-complete.svg&quot;}]" :step="$clicks" />

<!--
Teach the alignment before opening EvalTables. Compare the complete booking state; do not substitute a tag result for deterministic correctness. Match source IDs and execution fingerprints.

Visual sequence: The same case forks into two isolated initial bookings. Each uses its own recorded source and trace. The dashed link means aligned comparison, not shared mutable state or a handoff. Keep booking-state checks, explanation judgments, and monitor outcomes in separate fields.
Visual guide: airline_monitoring/comparison. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
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
clicks: 2
---

<div class="kicker">5:05 · Airline service monitoring</div>

# The recorded agent comparison was a tie

<AirlineMechanism mode="results" :reveal="$clicks + 1" />

<!--
Preserve the successful baseline. Do not describe the helper as improving task quality on this rehearsal. The controlled drill is a real code repair, but it is not a spontaneous agent failure. These small simulated batches do not estimate production reliability.

Visual sequence: Reveal the starting row first, then the repair row. All six case outcomes match; there is no passing case unique to the repair. Both versions also pass four subsequent requests. Native monitoring accuracy is unavailable. The local omission drill demonstrates a repair independently of this observed tie.
-->

---
class: workshop-setting-slide
name: report-measures
clicks: 1
---

<div class="kicker">5:08 · Airline service monitoring</div>

# Report denominators and unresolved work

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="airline_monitoring/compare"><img :src="&quot;/scenes/airline_monitoring/compare.svg&quot;" alt="Airline booking operations: Report denominators and missing judgments beside each measure. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><table class="monitor-table "><thead><tr><th>Measure</th><th>Report together</th></tr></thead><tbody><tr><td>Requested changes completed</td><td>Passed cases / scored cases; unavailable cases</td></tr><tr><td>Unrequested changes</td><td>Count and the affected segment</td></tr><tr><td>Monitoring accuracy</td><td>Reviewed precision, recall, and coverage</td></tr><tr><td>Explanation quality</td><td>Judged rows and missing judgments</td></tr><tr><td>Operational cost</td><td>Known cost, bounded unknown usage, native tag cost status</td></tr></tbody></table></div>

<!--
A six-case comparison has limited reach. Show each failure and avoid a general claim that monitoring improves all agents. If all cases tie, inspect whether behavior or cost changed while correctness stayed equal.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
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
class: aria-investigation
name: aria-conclusion
---

<div class="kicker">5:45 · 7 minutes across these three frames · Airline service monitoring</div>

# Check our conclusion

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">What changed in booking correctness, monitoring agreement, and coverage?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/6e61f9742d2bd73de556495259b40011" target="_blank" rel="noopener">final/baseline ↗</a></li><li><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/b76342ec86c76151084f51ba07c330ec" target="_blank" rel="noopener">final/repaired ↗</a></li><li><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/c786194dbc62194080e2c8f713e82095" target="_blank" rel="noopener">subsequent/baseline ↗</a></li></ul></div></div><p class="aria-foot">Keep the compared versions frozen. Suggest a future experiment without running it. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-conclusion-response
---

<div class="kicker">5:45 · 7 minutes across these three frames · Airline service monitoring</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-response.png" target="_blank"><img src="/aria/conclusion/conclusion-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>not a measured improvement over baseline</blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/conclusion/conclusion-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e073-5631-72e1-a4dd-563ddc9353dd" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-conclusion-verify
---

<div class="kicker">5:45 · 7 minutes across these three frames · Airline service monitoring</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-verification.png" target="_blank"><img src="/aria/conclusion/conclusion-verification.png" alt="Six paired final requests: both versions preserve passengers and booking details, while their execution-error counts differ."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="388.0" y="350.0" width="275.0" height="95.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="374.0" cy="363.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="374.0" y="367.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="678.0" y="350.0" width="568.0" height="95.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="664.0" cy="363.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="664.0" y="367.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> Execution errors</span><span><b>2</b> Booking checks: both 100%</span></figcaption></figure><div><b>Citation check: supported</b><p>Saved qualification comparisons and live execution records match the native summaries: task_success=1.0 for six final cases and four subsequent cases per version. The local qualification separately records 40 booking passes, 40 unobserved monitoring rows, null processing coverage, and six unavailable Alignment tests. Missing predictions cannot supply a monitor-agreement denominator. The native screenshot verifies final booking outcomes only; it does not establish native tag agreement or the total of 40.</p><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/runs/6e61f9742d2bd73de556495259b40011" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/conclusion/conclusion-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/airline_monitoring/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
name: conclusion
---

<div class="kicker">5:52 · Airline service monitoring</div>

# Write down what changed and whether it helped

<div class="timeline-list"><b>Agent</b><span>Which booking outcomes changed on matched requests?</span><b>Monitor</b><span>Which failures did the reviewed rule find or miss?</span><b>Evaluation</b><span>Which new check would catch this problem before release?</span><b>Next test</b><span>What remains uncertain, and which request would test it?</span></div>

<!--
The participant conclusion should cite one actual case and its exact code, booking, trace, and evaluation. Improvements are welcome; a documented tie or regression also completes the lesson.
-->

---
class: exercise
name: report
---

<div class="kicker">5:53 · Airline service monitoring</div>

# Publish the comparison and stop automatic judging

<p class="where">Notebook → Write the conclusion</p><div class="task-target">Edit The saved report and tag readback</div><ol><li>Publish saved comparisons; retry missing exports without rerunning requests.</li><li>Write the conclusion with one supporting case and one remaining failure.</li><li>Disable the workshop tag, then verify its native state.</li></ol><div class="done"><b>Run:</b> Publish saved comparisons → Publish my conclusion → Verify automatic tagging is off<br><b>Finished when:</b> The Report opens its supporting evidence, and automatic judging is confirmed off.</div>

<!--
Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.
-->

---
class: workshop-setting-slide
name: end
clicks: 1
---

<div class="kicker">5:58 · Airline service monitoring</div>

# The next release has a check the first release lacked

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="airline_monitoring/release"><img :src="&quot;/scenes/airline_monitoring/release.svg&quot;" alt="Airline booking operations: Save reviewed incidents so a repair can be tested again. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><p class="principle">You can point to a passenger request, the booking change, the monitoring decision, and the regression check that tests it again.</p><p>The final comparison tells you whether this repair is worth keeping. The next incident may need a different rule.</p></div>

<!--
End by asking someone to reproduce a case from its saved initial state. Do not conclude with a promise of autonomous improvement. Monitoring, human review, and offline evaluation each answered a different question.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
class: workshop-sharing
name: workshop-take-home
---

<div class="kicker">5:58 · Airline service monitoring</div>

# Keep the notebook and workshop materials

<div class="workshop-share-layout"><div class="workshop-share-instructions"><p>Return to your saved notebook copy to continue your work.</p><ol><li><strong>Revisit the example.</strong> The Report links its claims to recorded results.</li><li><strong>Keep the materials.</strong> Open the deck, download the PDF, or get the source.</li><li><strong>Run a session.</strong> Use the short run guide and facilitator notes.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuIab" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuIab">utm.io/uuIab</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The shared page has the template and references. Your executions remain in your own project.</p>

<!--
Keep this slide up during questions. Participants resume their saved notebook copy. The QR page provides the template, Report, downloads, and short facilitator run guide. Use recorded examples for a demo; check the current readiness notes before scheduling live delivery.
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
<p class="source-link"><a href="/60">Return to the explanation-judge exercise ↗</a></p>

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
<p class="source-link"><a href="/43">Return to monitoring calculations ↗</a></p>

<!--
This is the notebook’s actual my_monitor implementation. Review unflagged cases too; an alerts-only sample cannot establish recall across traffic.
-->

---
class: answer
name: answer-case
---

<div class="kicker">Reference · Airline service monitoring</div>

# Worked answer: preserve the original case inputs

<div class="bundle-list"><div>Copy the initial booking<small>A deep copy prevents later mutations changing the test</small></div><div>Keep request and policy<small>Preserve the rules used by this execution</small></div><div>Attach the reviewed expectation<small>Include scope, result, reviewer, and rationale</small></div><div>Retain native identities<small>Link back to the conversation and supporting span</small></div></div><p class="source-link"><a href="/48">Return to the curation exercise ↗</a></p>

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
# The new interval can contain a different number of flights.
requested_change = actual[start:start + len(replacement)] == replacement
# Preserve both untouched sides, including the return journey.
untouched_prefix = actual[:start] == original[:start]
untouched_suffix = actual[start + len(replacement):] == original[stop:]
booking_correct = requested_change and untouched_prefix and untouched_suffix
```
<p>Compare flight identities and relevant fields, not only list length. Keep confirmation and policy checks alongside these state checks.</p><p class="source-link"><a href="/51">Return to the state scorer exercise ↗</a></p>

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
<p class="source-link"><a href="/57">Return to the repair exercise ↗</a></p>

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
