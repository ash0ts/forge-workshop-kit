---
theme: default
title: Build a transit app with a team of coding agents
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

<div class="kicker">0:00</div>

# Build a transit app<br>with a team of coding agents

<div class="sub">Write the task coordinator, inspect the handoffs, and test whether shared lessons help the next feature.</div><div class="bottom-note">Four hours · Real MBTA schedule data · Your own Forge project</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>1 / 52</span></div>

<!--
The department and deadline are fictional. The schedule records are real public MBTA data. Participants build a bounded software factory; we do not claim to reproduce an unattended production engineering organization.
-->

---

<div class="kicker">0:01</div>

# Your team needs a departures board

<div class="quote">The demo is Friday. Someone has already promised a second feature.</div><p>A rider selects a stop and a service date. The app must show the right departures, in order, with the route and destination.</p><p class="caption">Fictional product brief. The app uses a saved historical schedule, so it does not predict live arrivals.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>2 / 52</span></div>

<!--
Start with the person using the software. Ask what could make a plausible-looking board wrong. Listen for wrong date, wrong stop, missing departures and misleading times. No model or agent count appears before the product is clear.
-->

---

<div class="kicker">0:02</div>

# Here is the application we want to deliver

<div class="reference-app-layout"><div class="reference-app-image"><img src="/images/reference-departures.png" alt="Reference app with Park Street, a historical midnight timestamp, and five scheduled Alewife departures"/><span class="eval-native-pin" style="left:42%;top:21%">1</span><span class="eval-native-pin" style="left:82%;top:31%">2</span><span class="eval-native-pin" style="left:72%;top:60%">3</span></div><div class="eval-native-notes"><p><b>1.</b> Choose a boarding platform.</p><p><b>2.</b> Ask what departs after this historical timestamp.</p><p><b>3.</b> Read the ordered departures and destinations.</p></div></div><p class="eval-native-caption">Reference implementation running locally. Actual archived schedule rows; not an agent-produced result. <a href="https://github.com/ash0ts/forge-workshop-kit/tree/main/examples/transit">Source and data receipt ↗</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>3 / 52</span></div>

<!--
This is a real capture of the reference implementation, not a model outcome. Participants will inspect the app their workers actually produce. Call out the selected Park Street platform, midnight on November 29, and first scheduled departure at 00:08. The next slides explain why that train belongs to November 28 service.
-->

---

<div class="kicker">0:03</div>

# The inputs are public transit records

<div class="flow"><div>Stops<small>Where a rider can board</small></div><b class="arrow">+</b><div>Trips and stop times<small>Which service visits each stop</small></div><b class="arrow">+</b><div>Service calendars<small>Which trips run on this date</small></div></div><p>We use the MBTA archive dated November 28, 2024. The teaching subset contains 10 platforms at five central Red Line stations.</p><p class="caption">GTFS describes scheduled service. This subset includes 1,252 trips and 6,260 stop-time rows; the source receipt preserves its checksum.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>4 / 52</span></div>

<!--
Open the notebook data receipt and read its archive date and checksum. Do not describe the small teaching subset as the complete MBTA system. MBTA describes its feed at https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md .
-->

---

<div class="kicker">0:05</div>

# The last train can belong to yesterday’s service

<div class="two-col"><div class="ticket"><small>Actual Park Street departure</small><strong>24:08:00</strong><p>Alewife-bound service on November 28 departs at 00:08 on November 29.</p></div><div><h2>What the code needs to preserve</h2><p>The elapsed time may be greater than 24 hours. Reducing it modulo 24 loses which service day it belongs to.</p></div></div><p class="caption">Trip 63926435 · stop 70076 · ThanksgivingDay service · MBTA archive 20241128</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>5 / 52</span></div>

<!--
This is an actual retained row: trip 63926435, stop 70076, departure_time 24:08:00, stop_sequence 150, ThanksgivingDay service, headsign Alewife. The civil timestamp is 2024-11-29T00:08:00-05:00. Ask what a parser restricted to 0..23 hours would do. The rule must survive between components.
-->

---

<div class="kicker">0:07</div>

# Turn the brief into checks

<table class="clean-table"><tbody><tr><th>Rider action</th><th>Observable requirement</th></tr><tr><td>Choose a stop</td><td>Every departure belongs to that stop</td></tr><tr><td>Choose a service date</td><td>Calendar rules and exceptions agree</td></tr><tr><td>Look after midnight</td><td>Keep the intended service day</td></tr><tr><td>Read the board</td><td>Departures are ordered and labeled</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>6 / 52</span></div>

<!--
These are requirements for our product, not a claim that the initial code fails them. Show the concrete acceptance inputs and expected outputs in the notebook. Final cases stay outside the coding-worker context until the versions are frozen.
-->

---

<div class="kicker">0:08</div>

# A software factory needs a way to finish work

<p class="definition">We will turn an approved feature into tasks, run coding workers, test their changes together, and save a release that someone can reproduce.</p><FactoryFlow :stage="0"/><p class="caption">In this workshop, people approve the feature contract and patches before integration.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>7 / 52</span></div>

<!--
Software factory is a broad term. This slide states the operational meaning we implement. It includes specification, coordination, verification and release. It is not simply a chat room with several role prompts.
-->

---
clicks: 3
---

<div class="kicker">0:09</div>

# Add the task board and two workers

<FactoryFlow :stage="$clicks + 1"/><p class="caption">Workers have separate conversations and working copies. The shared records tell them what is ready and who owns it.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>8 / 52</span></div>

<!--
Click once to reveal workers, once to reveal integration, once to reveal the checked lesson. Solid arrows show code or execution flow. The dashed arrow identifies reviewed evidence. The diagram is explanatory, not a recorded run.
-->

---

<div class="kicker">0:10</div>

# Your project contains the experiment

<div class="flow"><div>Forge Notebook<small>Edit and run the coordinator</small></div><b class="arrow">→</b><div>Agent Lens<small>Follow each worker and handoff</small></div><b class="arrow">→</b><div>Evaluations and Artifacts<small>Compare results; keep exact code</small></div></div><p>Each attendee uses a separate project. Shared memory belongs to the agents in that project.</p><p class="caption">No workshop gateway or facilitator token. The facilitator only reads progress you publish.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>9 / 52</span></div>

<!--
Keep the distinction between agents sharing project records and attendees sharing credentials. The latter does not happen. The notebook has an adjustable inference allowance; notebook compute is billed separately. Opening the notebook does not start agents.
-->

---
class: exercise
---

<div class="kicker">0:11</div>

# Connect and inspect the source data



<p class="where">Notebook → Understand the departures board</p><ol><li>Copy the template into a writable Forge project.</li><li>Read the destination project and inference allowance.</li><li>Add a task attribute in <code>instrument_tool()</code>, send the setup trace, and open one source row.</li></ol><div class="done"><strong>Run:</strong> Connect and restore my work → Send my first Agent Lens trace<br><strong>Check:</strong> The project is yours, and the source receipt identifies the historical GTFS snapshot.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>10 / 52</span></div>

<!--
Do not ask participants to paste a key into a code cell. Hosted authentication comes from their own account. Locally use wandb login. Access checks should distinguish a writable project from inference entitlement.
-->

---
class: exercise
---

<div class="kicker">0:15</div>

# Write the after-midnight acceptance check



<p class="where">Notebook → Understand the departures board</p><ol><li>Complete <code>check_departures(rows)</code> using the real Park Street train.</li><li>Check its trip ID, November 28 service date and November 29 departure together.</li><li>Run the free check before asking an agent to build the feature.</li></ol><div class="done"><strong>Run:</strong> Check my after-midnight scenario<br><strong>Check:</strong> The real row passes. A missing train and a wrong service date fail.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>11 / 52</span></div>

<!--
The scenario is written by the participant and later runs on the integrated app. It is public development evidence, not a hidden final answer. Show how a plausible train list can still use the wrong service day.
-->

---

<div class="kicker">0:20</div>

# One worker still needs a complete loop

<div class="flow"><div>Request<small>Task, files, allowed tools</small></div><b class="arrow">→</b><div>Tool action<small>Read, edit or run a test</small></div><b class="arrow">→</b><div>Observation<small>Actual result in the next request</small></div></div><p>The worker stops with a patch and test evidence. It does not mark the product released.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>12 / 52</span></div>

<!--
Start with the familiar single-agent harness. Multiple agents do not remove the need for correct tool observation handling, explicit stopping and independent checks. Model settings stay fixed in the comparisons.
-->

---

<div class="kicker">0:23</div>

# Give the worker the task it is allowed to solve

```python {1-3|4-8|all}
def build_worker_request(task, sources, lessons):
    import json
    return [
        {"role": "system", "content": "Implement your assigned feature."},
        {"role": "user", "content": json.dumps({
            "task": task, "sources": sources, "lessons": lessons
        })},
    ]
```
<p class="caption">The completed notebook function supplies the actual worker request. Keep final evaluation results out of it.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>13 / 52</span></div>

<!--
Explain each input before editing: task is the approved contract, sources are the current worker copy, lessons are explicitly retrieved project memory. This excerpt shows the fields that matter; follow the notebook function signature for the executable implementation.
-->

---

<div class="kicker">0:26</div>

# Return the tool result to the worker

```python {1-2|3-5|all}
def dispatch_action(action, tools):
    name = action["action"]
    if name not in tools:
        raise ValueError("Unknown builder operation: " + name)
    return tools[name](action)
```
<div class="flow"><div>Chosen action<small>For example, read_file</small></div><b class="arrow">→</b><div>Allowed Python tool<small>Execute the selected operation</small></div><b class="arrow">→</b><div>Returned result<small>The next model request can use it</small></div></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>14 / 52</span></div>

<!--
This participant function controls actual tool dispatch. The runtime supplies bounded file, edit, test and task operations. It records the returned result independently. An unknown action must raise an error rather than invoke arbitrary code.
-->

---
class: exercise
---

<div class="kicker">0:30</div>

# Run one worker before adding a team



<p class="where">Notebook → Run one builder</p><ol><li>Read <code>build_worker_request()</code> and add the missing task context.</li><li>Complete <code>dispatch_action()</code> and inspect the allowed tools.</li><li>Run the first feature and open its model and tool spans.</li></ol><div class="done"><strong>Run:</strong> Run one worker on the first feature<br><strong>Check:</strong> Follow the task request to a real file edit and test result in Agent Lens.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>15 / 52</span></div>

<!--
Allow participants to read a diff before accepting anything. The tool event and test output must be saved even when the worker fails. A recorded failure is an optional teaching example, not a required live outcome.
-->

---

<div class="kicker">0:40</div>

# A trace should answer what changed and why

<table class="clean-table"><tbody><tr><th>In the code</th><th>Find it in Agent Lens</th></tr><tr><td>Task and worker identifiers</td><td>The correct conversation and role</td></tr><tr><td>Tool arguments</td><td>The file read or test requested</td></tr><tr><td>Tool result and timing</td><td>The actual output and duration</td></tr><tr><td>Parent build identifier</td><td>The other conversations in this build</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>16 / 52</span></div>

<!--
Open the participant’s real trace rather than a made-up dashboard image. Each model request, tool action, failed check and handoff should be attributable to a worker and build. Trace export can be retried without rerunning the model.
-->

---

<div class="kicker">0:43</div>

# Inspect the worker’s test in Agent Lens

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c3c5ad393c98e294c667ab04f3a018c1/spans/turns/f95c96cf7b6c19aa29123342250297aa/spans/e2f00d23857411df"><img src="/images/agent-lens-worker-test.png" alt="Recorded Agent Lens builder-2 conversation with read_file, write_file and run_tests; presentation task test returned passed true"/></a><span class="eval-native-pin" style="left:44%;top:38%">1</span><span class="eval-native-pin" style="left:44%;top:65%">2</span><span class="eval-native-pin" style="left:97%;top:76%">3</span><span class="eval-native-pin" style="left:97%;top:92%">4</span></div><div class="eval-native-notes"><p><b>1.</b> Builder 2 has its own conversation.</p><p><b>2.</b> Follow the read, write and test operations.</p><p><b>3.</b> The task is <code>order-1-presentation</code>.</p><p><b>4.</b> Its component check returned <code>passed: true</code>.</p></div></div><p class="eval-native-caption">Recorded rehearsal R3 · 11 stored spans verified. This component passed; the query worker hit its output limit. Integration still needs checking.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>17 / 52</span></div>

<!--
Open the actual conversation link. The record proves that the presentation worker read and edited a file and ran a passing component check. It does not prove the whole app works. The sibling query worker exhausted its output budget in this rehearsal; preserve that failed attempt. Do not turn one passing span into a completed product claim.
-->

---
clicks: 2
---

<div class="kicker">0:45</div>

# Choose work that can happen independently

<ContractBoard :stage="$clicks"/><p class="caption">The combined departures list depends on both components. Starting it early does not remove that dependency.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>18 / 52</span></div>

<!--
The workers own query.py and presentation.py. The query returns the agreed departure records. The display consumes that interface. Use the actual notebook contract to see exactly which fields are required. Click to expose the join, then the whole-product check.
-->

---

<div class="kicker">0:50</div>

# Ready means its prerequisites passed

```python {1-3|4-6|all}
def ready_tasks(tasks):
    return [key for key, task in tasks.items()
            if task["status"] == "pending"
            and all(tasks[parent]["status"] == "integrated"
                    for parent in task.get("depends_on", []))]
```
<div class="status-row"><span>Query: ready</span><span>Display: ready</span><span class="blocked">Integration: waiting for both</span></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>19 / 52</span></div>

<!--
Completed means accepted completion with saved output, not a worker’s progress narration. The local check should reject a task with an unmet dependency. The precise notebook record fields may include richer status metadata; preserve those contracts.
-->

---
class: exercise
name: tasks-exercise
---

<div class="kicker">0:55</div>

# Make dependencies control the workers

<a class="answer-link" href="48">Worked answer ↗</a>

<p class="where">Notebook → Divide and claim the work</p><ol><li>Complete <code>ready_tasks()</code>.</li><li>Try the free check with one prerequisite still open.</li><li>Complete <code>claim_task()</code> so two workers cannot claim the same task.</li></ol><div class="done"><strong>Run:</strong> Check my ready_tasks code<br><strong>Check:</strong> Only unclaimed tasks with satisfied prerequisites can start.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>20 / 52</span></div>

<!--
Do not solve the race with a prompt asking agents to be careful. Claiming must be atomic in the shared task store. Let two local attempts contend for one task in the free exercise.
-->

---

<div class="kicker">1:08</div>

# Separate working copies protect unfinished changes

<div class="two-col"><div class="ticket"><small>Worker A</small>Starting revision + owned files<p>Writes one candidate patch.</p></div><div class="ticket"><small>Worker B</small>The same starting revision + its files<p>Writes another candidate patch.</p></div></div><p>Both patches still need to work together. Isolation prevents accidental overwrites; it does not prove compatibility.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>21 / 52</span></div>

<!--
This is a practical reason for independent workspaces, not a guarantee that the generated code is safe. Reviewed local code runs with bounded tools and time limits. Remote Sandboxes remain optional and require their own access.
-->

---
class: exercise
---

<div class="kicker">1:10</div>

# Run the ready tasks with two workers



<p class="where">Notebook → Run two builders</p><ol><li>Review the task cards and file ownership.</li><li>Start the bounded run once.</li><li>Select a worker in the timeline and inspect its first task claim.</li></ol><div class="done"><strong>Run:</strong> Run the ready tasks with two workers<br><strong>Check:</strong> Each task has one owner. The trace identifies that worker’s starting code and resulting patch.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>22 / 52</span></div>

<!--
Keep the concurrency at two for the core exercise. More workers is an optional later experiment. Do not change model or total budget between comparisons and then attribute a difference only to coordination.
-->

---

<div class="kicker">1:25</div>

# Read the timeline as work and waiting

<div class="frame"><svg class="diagram" viewBox="0 0 1100 250" role="img" aria-label="Illustrative timeline: workers A and B run concurrently. Integration waits for both, then tests the merged application."><text x="0" y="58" style="font-size:24px">Worker A</text><text x="0" y="138" style="font-size:24px">Worker B</text><text x="0" y="218" style="font-size:24px">Integration</text><rect x="180" y="25" width="360" height="45" fill="#4382a6"/><rect x="180" y="105" width="500" height="45" fill="#c17b40"/><path d="M540 75V180M680 155V180" stroke="#61746e" stroke-dasharray="6 5" stroke-width="2"/><rect x="680" y="185" width="310" height="45" fill="#7c9e8a"/><text x="710" y="217" style="font-size:22px">Combined checks</text></svg></div><p class="caption">Illustrative durations. The live timeline uses saved timestamps and shows failures and unfinished work explicitly.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>23 / 52</span></div>

<!--
Ask which task is on the critical path. Parallel work can reduce elapsed time while increasing aggregate model cost. Queue time, execution time and integration time belong in separate fields.
-->

---

<div class="kicker">1:45</div>

# Save the checkpoint before the break

<p class="sub">Keep the patches, test outputs and current task board. After the break, we will review the changes and test them together.</p><p class="aside">The team can stop working without forgetting what it was doing.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>24 / 52</span></div>

<!--
Break runs from 1:45 to 1:55. Integration begins when participants return. Confirm durable local saving. If publication is pending, the work is still complete locally. Reopening or navigating must not start inference.
-->

---

<div class="kicker">1:55</div>

# Review a patch before it enters the product

<div class="flow"><div>Worker output<small>Changed source + stated reason</small></div><b class="arrow">→</b><div>Human review<small>Does it implement the contract?</small></div><b class="arrow">→</b><div>Integration check<small>Does it work with the other patch?</small></div></div><p>A passing component test does not establish that the complete departures board is correct.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>25 / 52</span></div>

<!--
The user explicitly approved human review of task contracts and patches. Keep the actual diff visible next to its test output. Do not represent a review decision as an executed version until integration really runs.
-->

---
class: exercise
---

<div class="kicker">2:00</div>

# Test the combined departures board



<p class="where">Notebook → Test the combined app</p><ol><li>Read both diffs and their test results.</li><li>Accept or reject each patch with a reason.</li><li>Run the combined checks and inspect one displayed departure.</li></ol><div class="done"><strong>Run:</strong> Test the combined departures board<br><strong>Check:</strong> The board’s result comes from the combined code you reviewed.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>26 / 52</span></div>

<!--
Show the combined source identity and acceptance output. If integration fails, preserve it and diagnose the failure before another edit. The facilitator can use the recorded controlled example if the live patches happen to work.
-->

---

<div class="kicker">2:12</div>

# An integration error can cross a correct boundary

<div class="two-col"><div><h2>The parser returns</h2><p>Elapsed seconds from the service-day origin.</p></div><div><h2>The consumer assumes</h2><p>A time restricted to the current calendar day.</p></div></div><p>Both functions may pass narrow tests. The joined behavior loses an after-midnight departure.</p><p class="caption">Teaching example of a contract mismatch. Use the live check to determine whether this actually occurred.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>27 / 52</span></div>

<!--
Do not claim the current agents made this error unless its execution record shows it. This example explains why tests at component boundaries matter. The repair may be to code, task contract, tests or a combination.
-->

---

<div class="kicker">2:25</div>

# Shared memory needs something worth sharing

<p>A later worker can reuse a verified project rule. It also should not inherit an unchecked guess as fact.</p><MemoryFlow :stage="0"/>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>28 / 52</span></div>

<!--
Connect memory to a specific integration incident or verified behavior. Transcripts record what happened. A lesson is an interpretation intended to help a future task.
-->

---
clicks: 2
---

<div class="kicker">2:28</div>

# Check the lesson before another agent relies on it

<MemoryFlow :stage="$clicks + 1"/><p class="caption">A checked lesson records its scope and supporting execution. A new contract can make it obsolete.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>29 / 52</span></div>

<!--
Click to reveal approved memory, then the fresh worker using it. A lesson can describe a successful pattern as well as a failure. Keep claims and verified observations distinct.
-->

---

<div class="kicker">2:32</div>

# Write a rule with a test attached

```json
{
  "rule": "Keep elapsed seconds beyond 24 hours",
  "scope": "GTFS schedule-time conversion",
  "status": "proposed",
  "evidence": ["a saved test or tool event"],
  "version": "the reviewed interface"
}
```
<p class="caption">Illustrative record. The notebook links your actual evidence and review decision.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>30 / 52</span></div>

<!--
Do not present this as a measured memory success. Explain scope: a rule about schedule times does not mean every display field should print hour 25. Keep the contract version, source evidence and review state visible.
-->

---
class: exercise
name: memory-exercise
---

<div class="kicker">2:36</div>

# Save a lesson supported by an execution

<a class="answer-link" href="49">Worked answer ↗</a>

<p class="where">Notebook → Keep a checked lesson</p><ol><li>Choose a test or tool event that establishes a project rule.</li><li>Write the rule, its scope and what would invalidate it.</li><li>Complete <code>select_memories()</code> so only relevant approved lessons reach the worker.</li></ol><div class="done"><strong>Run:</strong> Save a checked lesson<br><strong>Check:</strong> The saved lesson opens its supporting event, and unrelated or superseded lessons are excluded.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>31 / 52</span></div>

<!--
Participants must inspect the evidence rather than approve an agent summary blindly. The retrieval function affects the later actual worker request. A directory listing is not proof that a worker read a lesson.
-->

---

<div class="kicker">2:44</div>

# Inspect the memory read, then its effect

<div class="flow"><div>Memory selected<small>Which rule matched this task?</small></div><b class="arrow">→</b><div>Worker request<small>Was that text actually supplied?</small></div><b class="arrow">→</b><div>Code and test<small>What did the worker do with it?</small></div></div><p>Open the Agent Lens memory event and the next model request. Then inspect the resulting patch.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>32 / 52</span></div>

<!--
This is the trace-to-behavior chain. A citation or read event establishes consultation, not that the memory caused an improvement. The matched follow-up comparison is what tests that question.
-->

---

<div class="kicker">2:50</div>

# Find the last direct train between two stops

<div class="two-col"><div class="ticket"><small>Follow-up A</small>Last direct train<p>Fresh team without project lessons.</p></div><div class="ticket"><small>Follow-up B</small>The identical request<p>Fresh team with selected lessons.</p></div></div><p>Start from the same code. Keep model settings and limits the same. Save both attempts.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>33 / 52</span></div>

<!--
The follow-up asks for the last direct train between two retained stations, including arrival after midnight, a no-direct-service result and an itinerary download. Each branch uses two workers. Both branches execute; no prerecorded result is substituted for one side. This small paired example teaches the method. One pair cannot establish repeatability or general superiority.
-->

---
class: exercise
---

<div class="kicker">2:55</div>

# Run both versions of the follow-up feature



<p class="where">Notebook → Build the next feature</p><ol><li>Review the follow-up contract and the selected lesson.</li><li>Confirm the starting code is identical for both runs.</li><li>Run both branches, review their diffs, and inspect their tests.</li></ol><div class="done"><strong>Run:</strong> Run both versions of the follow-up feature → Integrate the reviewed follow-up patches<br><strong>Check:</strong> The comparison includes both actual outputs, costs and trace links, even if one fails.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>34 / 52</span></div>

<!--
Keep memory fixed during this matched comparison. Do not edit it after seeing the no-memory result and call the pair controlled. If budget or infrastructure prevents a branch from finishing, retain a missing result and label the pair incomplete.
-->

---

<div class="kicker">3:15</div>

# The factory has two kinds of state

<table class="clean-table"><tbody><tr><th>Work state</th><th>Project knowledge</th></tr><tr><td>What is ready or blocked?</td><td>What rule has been verified?</td></tr><tr><td>Who owns the task?</td><td>Where does that rule apply?</td></tr><tr><td>Which patch and test finished?</td><td>What evidence supports it?</td></tr><tr><td>Resume the same build</td><td>Help a later task</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>35 / 52</span></div>

<!--
This is the distinction between a task ledger and learning. Neither requires sharing a giant conversation among all workers. Both need durable records, clear identities and bounded retrieval.
-->

---

<div class="kicker">3:25</div>

# Evaluate the product and the process separately

<table class="clean-table"><tbody><tr><th>Product quality</th><th>Coordination and expense</th></tr><tr><td>Acceptance scenarios passed</td><td>Elapsed time and total model cost</td></tr><tr><td>Wrong, missing or misordered departures</td><td>Duplicate work and blocked time</td></tr><tr><td>Regressions in earlier features</td><td>Integration failures and retries</td></tr><tr><td>Usable delivered build</td><td>Memory retrieved and cited</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>36 / 52</span></div>

<!--
Avoid a composite score that conceals these tradeoffs. The saved product rows are matched across versions. Missing builds or evaluations remain missing, not silently dropped or converted to ordinary task failures.
-->

---

<div class="kicker">3:27</div>

# A scenario is an input and an expected behavior

```python {1-2|4-6|all}
def score_scenario(actual, expected):
    return actual == expected

expected = ["trip-1", "trip-2"]
assert score_scenario(["trip-1", "trip-2"], expected)
assert not score_scenario(["trip-2", "trip-1"], expected)
```
<p class="caption">The exercise uses public development cases. The independent final grader checks the complete required fields and order.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>37 / 52</span></div>

<!--
This is a compact teaching excerpt, not the complete final acceptance scorer. Explain why sorting the identifiers before comparing would hide an ordering defect. Failed execution is not equivalent to a valid empty departure list.
-->

---
class: exercise
---

<div class="kicker">3:30</div>

# Compare the frozen builds on matching cases



<p class="where">Notebook → Compare frozen builds</p><ol><li>Complete the development <code>score_scenario()</code> and run its free checks.</li><li>Freeze the reviewed build versions.</li><li>Run final scenarios and open the comparison in Forge.</li></ol><div class="done"><strong>Run:</strong> Compare the frozen builds<br><strong>Check:</strong> Each row uses the same input across versions. A score links to the executed code and actual output.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>38 / 52</span></div>

<!--
Final grading happens after the build choices freeze. Evaluation Tables Preview uses the working Weave-backed publication path. If publication fails, inspect the notebook rows and retry publication only; do not rerun model work.
-->

---

<div class="kicker">3:34</div>

# Read one comparison row before the average

<div class="frame"><p><strong>Input:</strong> the same stop, service date and requested time.</p><p><strong>Outputs:</strong> each frozen build’s departure list.</p><p><strong>Scores:</strong> whether each requirement passed.</p><p><strong>Links:</strong> the worker trace, reviewed diff and code artifact.</p></div><p>In EvalTables, set the starting build as reference. Open a difference and explain it using the actual departures.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>39 / 52</span></div>

<!--
Use one scenario to explain the matching inputs, actual outputs and pass criteria before opening the native comparison on the next slide. Keep its source URL and recorded rehearsal identity visible.
-->

---

<div class="kicker">3:35</div>

# Compare the same departures in Forge

<div class="native-wide"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=5lkijosxo9y"><img src="/images/native-comparison-r4-detail.png" alt="Actual Forge Evaluation Tables Preview comparison with one-builder reference, two-builder output, equal pass rates and aligned departure cases"/></a><span class="eval-native-pin" style="left:15%;top:3%">1</span><span class="eval-native-pin" style="left:9%;top:44%">2</span><span class="eval-native-pin" style="left:34%;top:40%">3</span></div><p class="eval-native-caption"><strong>1.</strong> One builder is the reference. <strong>2.</strong> Each row uses the same case. <strong>3.</strong> Read both outputs. Earlier rehearsal R4: both first builds passed 10 / 10.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>40 / 52</span></div>

<!--
Actual native Evaluation Tables Preview, verified in a signed-out browser. The saved workspace contains two frozen first-release builds and ten matching scenarios, with all twenty underlying evaluation rows read back. This image does not represent the R4 memory followups, which were incomplete. Open a prediction cell and inspect the service date before treating a matching average as sufficient evidence.
-->

---

<div class="kicker">3:37</div>

# The faster build missed two final cases

<table class="clean-table small-table"><tbody><tr><th>Rehearsal R5</th><th>Final scenarios</th><th>Builder elapsed</th><th>Observed model cost</th></tr><tr><td>One worker</td><td>10 / 10</td><td>124.78 s</td><td>$0.01107</td></tr><tr><td>Two workers</td><td>8 / 10</td><td>94.91 s</td><td>$0.01221</td></tr><tr><td>Follow-up without memory</td><td>12 / 18</td><td>212.88 s</td><td>$0.02565</td></tr><tr><td>Follow-up with memory</td><td>12 / 18</td><td>96.13 s</td><td>$0.01600</td></tr></tbody></table><p class="caption">Both initial builds passed their development checks. Independent final cases exposed the team build’s errors. Neither follow-up query finished; this pair does not establish a memory benefit.</p><p class="caption">One paired rehearsal. Elapsed time excludes human review and integration.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>41 / 52</span></div>

<!--
These are final native scores from R5, a separate engineering rehearsal after context compaction changed. All 56 scenario rows are represented. The first builds passed five public development checks each, but the two-worker final product passed only eight of ten reserved scenarios. Do not treat the earlier R4 native screenshot as this R5 comparison. Builder elapsed excludes human review and integration. Actual provider request counts were 8, 12, 5 and 5 respectively. The no-memory query reached its input bound after writing; the memory query exhausted its output allowance. Both stopped before query tests; presentation was retained unchanged. The lesson proposal cost an additional $0.00143474. Total observed inference was $0.06635800 across 31 provider requests, with zero unknown usage. This single pair cannot establish a general speed or memory effect.
-->

---

<div class="kicker">3:38</div>

# A timezone assumption selected the wrong train

<div class="flow"><div>Rider’s request<small>23:00 UTC = 18:00 Eastern</small></div><b class="arrow">→</b><div>Expected next departure<small>18:03 Eastern<br>Trip 63919613</small></div></div><div class="two-col"><div class="ticket"><small>One-worker result</small>Uses the feed’s timezone<p>Finds the expected train.</p></div><div class="ticket"><small>Two-worker result</small>Uses the request’s timezone<p>Selects trip 63919759 from later in the service day.</p></div></div><p class="caption">R5: the query and rendered-board cases caught the same defect. It changed the selected train, not just how the time was displayed.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>42 / 52</span></div>

<!--
The failed cases were departures/utc-input and integrated/departures/utc-input. The two-worker query anchored GTFS service-day midnight to the caller’s timezone. It selected a service-clock 23:03 trip rather than the expected 18:03 Eastern departure after a 23:00 UTC request. The solo query preserved the fixed feed timezone for this historical subset. These are two checks of one defect, not two independent bugs. Both failed follow-up query edits left this earlier bug in place. Ask participants which contract or test they would add before another build.
-->

---

<div class="kicker">3:40</div>

# More workers can still produce more waiting

<p>Compare the actual time spent coding with time spent waiting, reviewing and repairing integration.</p><p>Then compare the cost of the completed product. A faster worker trace does not mean a cheaper or better delivered application.</p><p class="caption">Research and production reports find coordination gains depend on task structure. This workshop measures its own runs.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>43 / 52</span></div>

<!--
Primary sources: Claude Code agent-team docs, Google Research scaling-agent-systems study and Anthropic compiler report. Do not import their performance numbers as a forecast for this model or task.
-->

---

<div class="kicker">3:45</div>

# Choose a release using the saved checks

<div class="flow"><div>Frozen build<small>Exact code and data</small></div><b class="arrow">→</b><div>Release decision<small>Required scenarios passed?</small></div><b class="arrow">→</b><div>Versioned artifact<small>Can another run reproduce it?</small></div></div><p>If a required check fails, keep the previous version and explain the failed condition.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>44 / 52</span></div>

<!--
The release is a versioned workshop artifact, not an automatic public service deployment. Agent-generated recommendations do not bypass required checks. Preserve previous versions for reproduction and rollback.
-->

---
class: exercise
name: release-exercise
---

<div class="kicker">3:47</div>

# Publish the version you can reproduce

<a class="answer-link" href="50">Worked answer ↗</a>

<p class="where">Notebook → Reproduce and release</p><ol><li>Complete <code>release_decision()</code> using the required check results.</li><li>Write the decision in your own words, including any regression.</li><li>Publish the code, data reference, checks and conclusion together.</li></ol><div class="done"><strong>Run:</strong> Publish this release and its evidence<br><strong>Check:</strong> Reload a saved case from the release artifact and reproduce its departure list.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>45 / 52</span></div>

<!--
Use the final fifteen minutes for reproduction, the release decision and a short explanation. If a failed build is the only result, the correct output is a blocked release with evidence. That still completes the learning exercise.
-->

---

<div class="kicker">3:53</div>

# Explain one result to another participant

<ol><li>Show the feature and the departure list it produced.</li><li>Open one worker’s change and its acceptance result.</li><li>Show a shared lesson that was read, or explain why none applied.</li><li>State what you would change in the next factory run.</li></ol><p class="caption">A faster build, a better build, a tie and a regression are different outcomes. Report the one you observed.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>46 / 52</span></div>

<!--
Give participants two minutes each. The person explaining should control the notebook and open the relevant record. The facilitator should not take the keyboard or supply the conclusion.
-->

---

<div class="kicker">3:58</div>

# Take the coordination code to your own project

<p>Start with a feature whose acceptance behavior you can check. Split independent work, give each task an owner, and test the changes together.</p><p>Keep lessons that another task can use, with their evidence and limits. Then measure whether the team improves the work enough to justify its coordination cost.</p><p class="caption">Optional: ask ARIA to inspect a published failure and propose one follow-up test. Verify the cited event before accepting it.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>47 / 52</span></div>

<!--
Ask each person for one suitable feature, one prerequisite, one acceptance check and one durable project rule from their own team. ARIA is outside the measured comparison and may require additional access.
-->

---
class: answer
name: tasks-answer
---

<div class="kicker">Reference</div>

# Worked answer: select ready tasks

```python
def ready_tasks(tasks):
    return [key for key, task in tasks.items()
            if task["status"] == "pending"
            and all(tasks[parent]["status"] == "integrated"
                    for parent in task.get("depends_on", []))]

def claim_task(board, task_id, worker_id):
    return board.claim(task_id, worker_id)
```
<p>Make the claim atomic in the task store. Recheck status while holding its lock, then assign one owner.</p><p class="answer-nav source-link"><a href="20">Return to the task exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>48 / 52</span></div>

<!--
Use the exact notebook task schema. This answer explains the readiness rule; the claim transaction belongs to the supplied store interface. A separate read followed by an unlocked write allows two workers to claim the same task.
-->

---
class: answer
name: memory-answer
---

<div class="kicker">Reference</div>

# Worked answer: retrieve a checked lesson

```python
def select_memories(entries, tags, scope, revision):
    return [entry for entry in entries
            if entry["status"] == "accepted"
            and entry["scope"] == scope
            and entry["version"] == revision
            and set(entry["tags"]) & set(tags)]
```
<p class="answer-nav source-link"><a href="31">Return to the memory exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>49 / 52</span></div>

<!--
Preserve the notebook schema and evidence validation. An approved lesson still has a scope. If the interface changed, retrieve the current rule or ask for review instead of trusting a stale note.
-->

---
class: answer
name: release-answer
---

<div class="kicker">Reference</div>

# Worked answer: block an unverified release

```python
def release_decision(rows):
    return bool(rows) and all(
        row.get("passed") is True for row in rows
    )
```
<p class="answer-nav source-link"><a href="45">Return to the release exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>50 / 52</span></div>

<!--
This teaching excerpt deliberately blocks missing results and empty check lists. Use the executable notebook record shape for the real decision. A valid release requires the code and checks to refer to the same frozen build.
-->

---
name: workflow-sources
---

<div class="kicker">Reference</div>

# Sources for the workflow

<ul class="source-list"><li><a href="https://factory.strongdm.ai/">StrongDM: software factory concepts and scenarios</a></li><li><a href="https://www.anthropic.com/research/building-c-compiler">Anthropic: independent workspaces, task claims and integration</a></li><li><a href="https://code.claude.com/docs/en/agent-teams">Claude Code: shared tasks, messages and coordination limits</a></li><li><a href="https://github.com/gastownhall/gastown">Gas Town: durable work state and merge verification</a></li><li><a href="https://github.com/gastownhall/beads">Beads: dependency-aware tasks and project memory</a></li></ul>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>51 / 52</span></div>

<!--
These are references for patterns, not required workshop installations. The notebook keeps its coordinator visible in Python and uses the existing Forge Workshop Kit. Software factory has several definitions; use the implemented workshop definition.
-->

---

<div class="kicker">Reference</div>

# Sources for the data and evaluation

<ul class="source-list"><li><a href="https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md">MBTA feed documentation</a></li><li><a href="https://gtfs.org/documentation/schedule/reference/">GTFS schedule reference</a></li><li><a href="https://www.anthropic.com/research/components-of-agent-memory">Anthropic: memory notes, validation and correction</a></li><li><a href="https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/">Google Research: when coordination helps and hurts</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit">Workshop code, source receipts and current access instructions</a></li></ul>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>52 / 52</span></div>

<!--
The downloaded dataset manifest is authoritative for archive date, checksums, selected rows and licensing. Do not substitute current live schedule data during a comparison. The software-factory teaching experiment is not a transit reliability benchmark.
-->
