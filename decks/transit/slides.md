---
theme: default
title: Build a transit app with a team of coding agents
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

<div class="kicker">0:00</div>

# Build a transit app<br>with a team of coding agents

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="transit/start"><img :src="&quot;/scenes/transit/start.svg&quot;" alt="Transit build room: Two builders share one departure-board problem. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="sub">Assign two builders, combine their patches, and try the departure board.<br>Check what the next builders should remember.</div><div class="bottom-note">Six hours · Real MBTA schedule data · Your own Forge project</div></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>1 / 104</span></div>

<!--
Begin with the person leaving the event who needs to catch a train. The builders will implement a query and a screen; participants write the coordinator and decide whether the combined app meets the request. Follow worker patches and tests in Agent Lens, then inspect the actual departures. The saved MBTA feed is historical, so this app shows scheduled service for those dates. The single session includes three breaks. The extra time is for tracing one concrete input through the implementation, writing the coordinator and explaining the recorded failures.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
class: technical-manual
name: technical-overview
clicks: 4
---

<div class="kicker">0:02</div>

# What you will build and inspect

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;schedule&quot;, &quot;label&quot;: &quot;Schedule&quot;, &quot;svg&quot;: &quot;01-schedule.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/transit/overview/slide/01-schedule.svg&quot;}, {&quot;id&quot;: &quot;build&quot;, &quot;label&quot;: &quot;Build&quot;, &quot;svg&quot;: &quot;02-build.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/transit/overview/slide/02-build.svg&quot;}, {&quot;id&quot;: &quot;integrate&quot;, &quot;label&quot;: &quot;Integrate&quot;, &quot;svg&quot;: &quot;03-integrate.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/transit/overview/slide/03-integrate.svg&quot;}, {&quot;id&quot;: &quot;lesson&quot;, &quot;label&quot;: &quot;Lesson&quot;, &quot;svg&quot;: &quot;04-lesson.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/transit/overview/slide/04-lesson.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;What will you build, and how will you know it works?&quot;, &quot;src&quot;: &quot;/guides/transit/overview/slide/05-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>2 / 104</span></div>

<!--
Introduce the real task, the data available, and the outcome participants will check. Point to each Forge product at the operation it helps investigate.
Visual guide: transit/overview. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">0:02</div>

# Your team needs a departures board

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="transit/inspect"><img :src="&quot;/scenes/transit/inspect.svg&quot;" alt="Transit build room: The departure board must handle trips after midnight. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><div class="quote">The demo is Friday. Someone has already promised a second feature.</div><p>A rider selects a stop and a service date. The app must show the right departures, in order, with the route and destination.</p><p class="caption">Fictional product brief. The app uses a saved historical schedule, so it does not predict live arrivals.</p></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>3 / 104</span></div>

<!--
Start with the person using the software. Ask what could make a plausible-looking board wrong. Listen for wrong date, wrong stop, missing departures and misleading times. No model or agent count appears before the product is clear.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---

<div class="kicker">0:05</div>

# Here is the application we want to deliver

<div class="reference-app-layout"><div class="reference-app-image"><img src="/images/reference-departures.png" alt="Reference app with Park Street, a historical midnight timestamp, and five scheduled Alewife departures"/><span class="eval-native-pin" style="left:42%;top:21%">1</span><span class="eval-native-pin" style="left:82%;top:31%">2</span><span class="eval-native-pin" style="left:72%;top:60%">3</span></div><div class="eval-native-notes"><p><b>1.</b> Choose a boarding platform.</p><p><b>2.</b> Ask what departs after this historical timestamp.</p><p><b>3.</b> Read the ordered departures and destinations.</p></div></div><p class="eval-native-caption">Reference implementation running locally. Actual archived schedule rows; not an agent-produced result. <a href="https://github.com/ash0ts/forge-workshop-kit/tree/main/examples/transit">Source and data receipt ↗</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>4 / 104</span></div>

<!--
This is a real capture of the reference implementation, not a model outcome. Participants will inspect the app their workers actually produce. Call out the selected Park Street platform, midnight on November 29, and first scheduled departure at 00:08. The next slides explain why that train belongs to November 28 service.
-->

---
clicks: 2
---

<div class="kicker">0:08</div>

# The inputs are public transit records

<TransitMechanism mode="joins" :stage="$clicks"/><p class="caption">Follow trip_id to the service rule, then convert its departure time. 10 platforms, 1,252 trips and 6,260 stop times in this teaching subset.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>5 / 104</span></div>

<!--
Open the notebook data receipt and read its archive date and checksum. Do not describe the small teaching subset as the complete MBTA system. MBTA describes its feed at https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md . Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">0:10</div>

# Start with the row for the platform

<TransitMechanism mode="joins" :stage="0"/><p class="caption">The stop-time row identifies the trip and platform. It does not contain the date on which that trip runs.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>6 / 104</span></div>

<!--
Keep the same trip visible through the next three slides. Read the actual identifiers aloud once. The product uses these joins, not an LLM guess about the next train. Ask which table must tell us whether this trip runs on Thanksgiving. Timeline spacing is illustrative; timestamps are actual. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">0:13</div>

# Join the trip to its service calendar

<TransitMechanism mode="joins" :stage="2"/><p class="caption">The shared trip_id identifies ThanksgivingDay service. Its calendar exception adds service on November 28.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>7 / 104</span></div>

<!--
The service ID is a join key. The active dates come from the calendar and exception records. Explain that calendar_dates overrides the weekly rule. This is a historical snapshot and fixed test date, not today’s schedule. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">0:15</div>

# Keep the service date and boarding date

<TransitMechanism mode="service-day" :stage="2"/><p class="caption">This train belongs to November 28 service and departs on November 29. The result needs both facts.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>8 / 104</span></div>

<!--
Ask the room to name the two different dates before revealing the timestamp. The train is eight minutes after the next midnight. Explain why hour modulo 24 without carrying the day loses information.
-->

---
class: technical-manual
clicks: 3
---

<div class="kicker">0:17</div>

# Keep the GTFS service day after midnight

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;join&quot;, &quot;label&quot;: &quot;Join&quot;, &quot;svg&quot;: &quot;01-join.svg&quot;, &quot;caption&quot;: &quot;Which date belongs to this departure?&quot;, &quot;src&quot;: &quot;/guides/transit/service-time/slide/01-join.svg&quot;}, {&quot;id&quot;: &quot;gtfs&quot;, &quot;label&quot;: &quot;Gtfs&quot;, &quot;svg&quot;: &quot;02-gtfs.svg&quot;, &quot;caption&quot;: &quot;Which date belongs to this departure?&quot;, &quot;src&quot;: &quot;/guides/transit/service-time/slide/02-gtfs.svg&quot;}, {&quot;id&quot;: &quot;civil&quot;, &quot;label&quot;: &quot;Civil&quot;, &quot;svg&quot;: &quot;03-civil.svg&quot;, &quot;caption&quot;: &quot;Which date belongs to this departure?&quot;, &quot;src&quot;: &quot;/guides/transit/service-time/slide/03-civil.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Which date belongs to this departure?&quot;, &quot;src&quot;: &quot;/guides/transit/service-time/slide/04-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>9 / 104</span></div>

<!--
This is an actual retained row: trip 63926435, stop 70076, departure_time 24:08:00, stop_sequence 150, ThanksgivingDay service, headsign Alewife. The civil timestamp is 2024-11-29T00:08:00-05:00. Ask what a parser restricted to 0..23 hours would do. The rule must survive between components. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
Visual guide: transit/service-time. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---

<div class="kicker">0:20</div>

# Convert elapsed service time into a timestamp

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

origin = datetime(2024, 11, 28, tzinfo=ZoneInfo("America/New_York"))
departure = origin + timedelta(hours=24, minutes=8)
assert departure.isoformat() == "2024-11-29T00:08:00-05:00"
```
<p class="caption">Walkthrough for this retained record. Keep service_date="2024-11-28" beside the converted timestamp.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>10 / 104</span></div>

<!--
Explain the datetime origin, timezone and timedelta separately. This example has no daylight-saving transition; it does not replace the full GTFS time specification. The learners write the acceptance check, while the coding worker implements the general query.
-->

---

<div class="kicker">0:23</div>

# Check the joined behavior, not just the parser

<div class="three-checks"><div><b>Input</b><p>Park Street<br>Nov 29 at 00:05 Eastern</p></div><div><b>Required row</b><p>Trip 63926435<br>Departs 00:08 Eastern</p></div><div><b>Required dates</b><p>Service: Nov 28<br>Boarding: Nov 29</p></div></div><p>Now remove that train, or change its service date. Your check should reject either result.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>11 / 104</span></div>

<!--
These deliberate mutations test the participant’s assertion. They are local examples, not recorded agent mistakes. Explain why a checker that always returns True would pass the first example and fail to teach anything.
-->

---

<div class="kicker">0:24</div>

# Turn the brief into checks

<table class="clean-table"><tbody><tr><th>Rider action</th><th>Observable requirement</th></tr><tr><td>Choose a stop</td><td>Every departure belongs to that stop</td></tr><tr><td>Choose a service date</td><td>Calendar rules and exceptions agree</td></tr><tr><td>Look after midnight</td><td>Keep the intended service day</td></tr><tr><td>Read the board</td><td>Departures are ordered and labeled</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>12 / 104</span></div>

<!--
These are requirements for our product, not a claim that the initial code fails them. Show the concrete acceptance inputs and expected outputs in the notebook. Final cases stay outside the coding-worker context until the versions are frozen.
-->

---

<div class="kicker">0:26</div>

# A software factory needs a way to finish work

<p class="definition">We will turn an approved feature into tasks, run coding workers, test their changes together, and save a release that someone can reproduce.</p><FactoryFlow :stage="0"/><p class="caption">In this workshop, people approve the feature contract and patches before integration.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>13 / 104</span></div>

<!--
Software factory is a broad term. This slide states the operational meaning we implement. It includes specification, coordination, verification and release. It is not simply a chat room with several role prompts.
-->

---

<div class="kicker">0:29</div>

# Two workers means two contexts around the same model

<div class="two-col"><div class="ticket"><small>Query worker</small>Task: return departure records<p>Own conversation, assigned file and checks.</p></div><div class="ticket"><small>Presentation worker</small>Task: render those records<p>Own conversation, assigned file and checks.</p></div></div><p>The model weights stay fixed. The coordinator changes which task and evidence each request receives.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>14 / 104</span></div>

<!--
The worker is a Python loop plus model requests and allowed tools. Two workers do not mean training two new models. Model settings match across the sequential and parallel builds. The comparison asks what the coordination design changes for this task.
-->

---
class: exercise
name: acceptance-exercise
---

<div class="kicker">0:22</div>

# Write the after-midnight acceptance check

<a class="answer-link" href="102">Worked answer ↗</a>


<p class="where">Notebook → Understand the departures board</p><ol><li>Click <strong>Show departures from the saved timetable</strong>. Find the real Park Street departure.</li><li>Complete <code>check_departures(rows)</code>: check its trip ID, November 28 service date and November 29 departure together.</li><li>Run the free check. It must reject a missing train and an incorrect service date.</li></ol><div class="done"><strong>Run:</strong> Check my after-midnight scenario<br><strong>Check:</strong> The real row passes. A missing train and a wrong service date fail.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>15 / 104</span></div>

<!--
The scenario is written by the participant and later runs on the integrated app. It is public development evidence, not a hidden final answer. Show how a plausible train list can still use the wrong service day. Run the reference query and acceptance check before authentication. The reference output is supplied code, not an agent build. The notebook saves this draft and passing check when the participant later connects.
-->

---

<div class="kicker">0:30</div>

# Your project contains the experiment

<div class="flow"><div>Forge Notebook<small>Edit and run the coordinator</small></div><b class="arrow">→</b><div>Agent Lens<small>Follow each worker and handoff</small></div><b class="arrow">→</b><div>Evaluations and Artifacts<small>Compare results; keep exact code</small></div></div><p>Each attendee uses a separate project. Shared memory belongs to the agents in that project.</p><p class="caption">No workshop gateway or facilitator token. The facilitator only reads progress you publish.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>16 / 104</span></div>

<!--
Keep the distinction between agents sharing project records and attendees sharing credentials. The latter does not happen. The notebook has an adjustable inference allowance; notebook compute is billed separately. Opening the notebook does not start agents.
-->

---
class: workshop-sharing
name: workshop-start
clicks: 0
---

<div class="kicker">0:33</div>

# Open the materials and download the notebook

<div class="workshop-share-layout"><div class="workshop-share-instructions"><ol><li><strong>Open this workshop’s page.</strong> Scan the code or type the short link.</li><li><strong>Download the current notebook.</strong> Save the Python file in a folder you will keep.</li><li><strong>Follow the two commands.</strong> Sign in, then open the saved file in marimo.</li><li><strong>Check the destination.</strong> Use your own writable project and account.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuIaa" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuIaa">utm.io/uuIaa</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The $8 adjustable allowance covers notebook inference. Notebook compute is billed separately.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>17 / 104</span></div>

<!--
Leave this QR code visible while participants open the workshop page. It links the current notebook, Report, deck, and run guide. Download the v0.12.0 Python file to a persistent folder. The page provides the pinned W&B sign-in and marimo launch commands. Enter a writable Forge project in notebook setup. The older hosted template is an optional path, not the current download. Continue to the existing setup exercise. The short link is managed in docs/share-links.json; do not reuse a historical event QR.
-->

---
class: exercise
---

<div class="kicker">0:33</div>

# Connect and inspect the source data



<p class="where">Notebook → Understand the departures board</p><ol><li><a href="https://ash0ts.github.io/forge-workshop-kit/packet/start/transit.html">Open the Transit start page ↗</a>, save the notebook, and follow its login and launch commands.</li><li>Read the destination project and inference allowance.</li><li>Add a task attribute in <code>instrument_tool()</code>, send the setup trace, and open one source row.</li></ol><div class="done"><strong>Run:</strong> Connect and restore my work → Send my first Agent Lens trace<br><strong>Check:</strong> The project is yours, and the source receipt identifies the historical GTFS snapshot.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>18 / 104</span></div>

<!--
Use the start page’s pinned login and local launch commands. Initialize the controls once with Run all stale cells, then enter the participant’s writable project. The project check and inference access are separate. The downloadable reference app demonstrates the finished board; it is not the editable workshop notebook.
-->

---

<div class="kicker">0:38</div>

# Record the operation that you just ran

```python
task_id = observation.get(
    "task_id", observation.get("arguments", {}).get("task_id", "setup")
)
with tracing.Tool(
    name=observation["name"], arguments=observation["arguments"],
    result=observation["result"], tool_call_id=observation["id"],
    started_at=stamp(observation["started_at"]),
    ended_at=stamp(observation["ended_at"]),
) as span:
    span.set_attributes({"factory.task_id": task_id})
```
<p class="caption">Excerpt from instrument_tool(). The same function exports later worker tools. Copy the recorded times; export time is different.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>19 / 104</span></div>

<!--
Identify the name, inputs, actual result and time boundaries. Participants add or edit the attribute in the full notebook function and find it in their own setup span. This operation reads the teaching dataset, so it does not spend inference allowance.
-->

---
class: technical-manual
clicks: 4
---

<div class="kicker">0:50</div>

# Return a tool result to the coding worker

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;request&quot;, &quot;label&quot;: &quot;Request&quot;, &quot;svg&quot;: &quot;01-request.svg&quot;, &quot;caption&quot;: &quot;How does an agent know what happened after it edits a file?&quot;, &quot;src&quot;: &quot;/guides/transit/worker/slide/01-request.svg&quot;}, {&quot;id&quot;: &quot;operation&quot;, &quot;label&quot;: &quot;Operation&quot;, &quot;svg&quot;: &quot;02-operation.svg&quot;, &quot;caption&quot;: &quot;How does an agent know what happened after it edits a file?&quot;, &quot;src&quot;: &quot;/guides/transit/worker/slide/02-operation.svg&quot;}, {&quot;id&quot;: &quot;next&quot;, &quot;label&quot;: &quot;Next&quot;, &quot;svg&quot;: &quot;03-next.svg&quot;, &quot;caption&quot;: &quot;How does an agent know what happened after it edits a file?&quot;, &quot;src&quot;: &quot;/guides/transit/worker/slide/03-next.svg&quot;}, {&quot;id&quot;: &quot;submit&quot;, &quot;label&quot;: &quot;Submit&quot;, &quot;svg&quot;: &quot;04-submit.svg&quot;, &quot;caption&quot;: &quot;How does an agent know what happened after it edits a file?&quot;, &quot;src&quot;: &quot;/guides/transit/worker/slide/04-submit.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;How does an agent know what happened after it edits a file?&quot;, &quot;src&quot;: &quot;/guides/transit/worker/slide/05-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>20 / 104</span></div>

<!--
Start with the familiar single-agent harness. Multiple agents do not remove the need for correct tool observation handling, explicit stopping and independent checks. Model settings stay fixed in the comparisons. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
Visual guide: transit/worker. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---

<div class="kicker">0:53</div>

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
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>21 / 104</span></div>

<!--
Explain each input before editing: task is the approved contract, sources are the current worker copy, lessons are explicitly retrieved project memory. This excerpt shows the fields that matter; follow the notebook function signature for the executable implementation.
-->

---

<div class="kicker">0:56</div>

# The first action reads the assigned file

<TransitMechanism mode="worker" :stage="0"/><p class="caption">read_file returns the current text and its SHA256. The next edit must refer to that hash.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>22 / 104</span></div>

<!--
This is an explanatory sequence using the implemented tool contract, not an additional live execution. Keep model, Python tool and observation separate. A model choosing read_file is not the same thing as Python executing it.
-->

---

<div class="kicker">0:59</div>

# The edit includes the version it was based on

<TransitMechanism mode="worker" :stage="1"/><p class="caption">write_file rejects a path the task does not own, or a file that changed since the read.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>23 / 104</span></div>

<!--
Explain optimistic conflict detection: before_sha256 identifies the old file, while the returned hash identifies the new one. A rejected write should produce an observation that the next request can inspect.
-->

---

<div class="kicker">1:02</div>

# Run the checks against the changed files

<TransitMechanism mode="worker" :stage="2"/><p class="caption">A passing test for an earlier file does not authorize completion after another edit.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>24 / 104</span></div>

<!--
The board clears the old test receipt when a file changes. The current files are what run in a child Python process. That process has restricted imports, a timeout and no inherited Forge credentials; it is reviewed code execution, not a security sandbox.
-->

---

<div class="kicker">1:05</div>

# Return the tool result to the worker

```python {1-2|3-5|all}
def dispatch_action(action, tools):
    name = action["action"]
    if name not in tools:
        raise ValueError("Unknown builder operation: " + name)
    return tools[name](action)
```
<div class="flow"><div>Chosen action<small>For example, read_file</small></div><b class="arrow">→</b><div>Allowed Python tool<small>Execute the selected operation</small></div><b class="arrow">→</b><div>Returned result<small>The next model request can use it</small></div></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>25 / 104</span></div>

<!--
This participant function controls actual tool dispatch. The runtime supplies bounded file, edit, test and task operations. It records the returned result independently. An unknown action must raise an error rather than invoke arbitrary code.
-->

---

<div class="kicker">1:07</div>

# Append the actual observation to the next request

```python
result = dispatch_action(action, tools)
messages.append({
    "role": "user",
    "content": json.dumps({
        "observation": result,
        "messages": inbox,
        "remaining_actions": max_steps - number - 1,
    }),
})
```
<p class="caption">Runtime excerpt. The notebook function chooses one allowed tool and must return that tool’s actual result.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>26 / 104</span></div>

<!--
The agent action has already been appended as an assistant message. The following user message supplies the observation, any directed messages and remaining action count. The runtime records actual tool execution independently of the learner’s return value. Do not add a second model call here.
-->

---

<div class="kicker">1:09</div>

# Finish submits a patch for review

<TransitMechanism mode="worker" :stage="3"/><p class="caption">finish requires passing development checks for the current source. It does not release the app.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>27 / 104</span></div>

<!--
Point out the status change to review. Human review and integration remain separate. If a worker reaches its action limit without this tested completion, the unfinished file is retained as evidence, not silently merged.
-->

---
class: exercise
name: worker-exercise
---

<div class="kicker">1:13</div>

# Run one worker before adding a team

<a class="answer-link" href="103">Worked answer ↗</a>


<p class="where">Notebook → Run one builder</p><ol><li>Read <code>build_worker_request()</code> and add the missing task context.</li><li>Complete <code>dispatch_action()</code> and inspect the allowed tools.</li><li>Click <strong>Check my build_worker_request code</strong>. It also checks your dispatcher. Then run the first feature.</li></ol><div class="done"><strong>Run:</strong> Run one worker on the first feature<br><strong>Check:</strong> The free check passes; then the actual model request, file edit and test are visible in Agent Lens.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>28 / 104</span></div>

<!--
Allow participants to read a diff before accepting anything. The tool event and test output must be saved even when the worker fails. A recorded failure is an optional teaching example, not a required live outcome.
-->

---

<div class="kicker">1:23</div>

# A trace should answer what changed and why

<table class="clean-table"><tbody><tr><th>In the code</th><th>Find it in Agent Lens</th></tr><tr><td>Task and worker identifiers</td><td>The correct conversation and role</td></tr><tr><td>Tool arguments</td><td>The file read or test requested</td></tr><tr><td>Tool result and timing</td><td>The actual output and duration</td></tr><tr><td>Parent build identifier</td><td>The other conversations in this build</td></tr></tbody></table>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>29 / 104</span></div>

<!--
Open the participant’s real trace rather than a made-up dashboard image. Each model request, tool action, failed check and handoff should be attributable to a worker and build. Trace export can be retried without rerunning the model.
-->

---

<div class="kicker">1:27</div>

# Inspect the worker’s test in Agent Lens

<div class="eval-native"><div class="eval-native-image"><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c3c5ad393c98e294c667ab04f3a018c1/spans/turns/f95c96cf7b6c19aa29123342250297aa/spans/e2f00d23857411df"><img src="/images/agent-lens-worker-test.png" alt="Recorded Agent Lens builder-2 conversation with read_file, write_file and run_tests; presentation task test returned passed true"/></a><span class="eval-native-pin" style="left:44%;top:38%">1</span><span class="eval-native-pin" style="left:44%;top:65%">2</span><span class="eval-native-pin" style="left:97%;top:76%">3</span><span class="eval-native-pin" style="left:97%;top:92%">4</span></div><div class="eval-native-notes"><p><b>1.</b> Builder 2 has its own conversation.</p><p><b>2.</b> Follow the read, write and test operations.</p><p><b>3.</b> The task is <code>order-1-presentation</code>.</p><p><b>4.</b> Its component check returned <code>passed: true</code>.</p></div></div><p class="eval-native-caption">Recorded rehearsal R3 · 11 stored spans verified. This component passed; the query worker hit its output limit. Integration still needs checking.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>30 / 104</span></div>

<!--
Open the actual conversation link. The record proves that the presentation worker read and edited a file and ran a passing component check. It does not prove the whole app works. The sibling query worker exhausted its output budget in this rehearsal; preserve that failed attempt. Do not turn one passing span into a completed product claim.
-->

---
class: exercise
name: solo-integration-exercise
---

<div class="kicker">1:28</div>

# Review and run the one-builder app

<p class="where">Notebook → Run one builder</p><ol><li>Read the query and presentation patches and their development checks.</li><li>Tick <strong>I reviewed the one-builder patches and their development checks</strong>.</li><li>Test the files together, then preview the actual departures board.</li></ol><div class="done"><strong>Run:</strong> Review and test the one-builder app → Preview this saved app<br><strong>Check:</strong> Explain one returned trip, its service date, and its boarding time.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>31 / 104</span></div>

<!--
A solo worker can produce both components. This integration uses the same saved solo stage and files as the later comparison. It does not select the follow-up starting release yet: that choice waits for both integrations. Failed checks remain visible. Reviewing and previewing uses no model requests.
-->

---

<div class="kicker">1:31</div>

# The request has a size limit even when files are saved

<div class="context-strip"><span>Task + contract</span><span>Current source</span><span>Lessons</span><span>Observations</span></div><p>The coordinator keeps current source once and replaces superseded copies with hashes. Complete files and raw histories remain saved.</p><p class="caption">Input: serialized messages + 4096 bytes of overhead must fit 32768 bytes. Output: at most 32768 tokens. These are different units.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>32 / 104</span></div>

<!--
Explain why storing a complete file is different from resending it with every action. R5 still hit a bound after a long write, so this policy is not a guarantee that any generated module will fit. Do not imply that a higher output allowance fixes an oversized input.
-->

---

<div class="kicker">1:32</div>

# Use the local preview to follow a returned row

<p class="where">Notebook → Run one builder</p><ol><li>Select the saved <strong>One builder</strong> integration.</li><li>Choose Park Street and <code>2024-11-29T00:05:00-05:00</code>.</li><li>Click <strong>Preview this saved app</strong> and find trip 63926435.</li></ol><p class="caption">This executes the reviewed app locally. It makes no model calls.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>33 / 104</span></div>

<!--
If a live build is wrong, keep the output visible and name the failed requirement. The prepared reference continuation appears only if neither initial build passes development integration; it is labeled and never replaces live results. First preview the solo integration. Repeat this same inspection after the team integration. The dropdown contains only saved integrations.
-->

---
class: break
---

<div class="kicker">1:35</div>

# Break until 1:45

<p class="sub">Keep the saved source, task record and trace. When we return, we’ll decide which tasks can run at the same time.</p><p>Browsing and reopening the notebook do not restart workers.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>34 / 104</span></div>

<!--
Ten-minute break, 1:35–1:45. Use the read-only monitor to find participants who requested help. Do not treat missing progress as failure.
-->

---
class: workshop-setting-slide
clicks: 4
---

<div class="kicker">1:45</div>

# Add the task board and two workers

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="transit/build"><img :src="&quot;/scenes/transit/build.svg&quot;" alt="Transit build room: Two builders need clear ownership and a shared test contract. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><FactoryFlow :stage="(Math.max(0, $clicks - 1)) + 1"/><p class="caption">Workers have separate conversations and working copies. The shared records tell them what is ready and who owns it.</p></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>35 / 104</span></div>

<!--
Click once to reveal workers, once to reveal integration, once to reveal the checked lesson. Solid arrows show code or execution flow. The dashed arrow identifies reviewed evidence. The diagram is explanatory, not a recorded run.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
clicks: 1
---

<div class="kicker">1:45</div>

# Choose work that can happen independently

<TransitMechanism mode="tasks" :stage="$clicks"/><p class="caption">The query and presentation tasks can start independently. The combined check waits for both reviewed outputs.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>36 / 104</span></div>

<!--
The workers own query.py and presentation.py. The query returns the agreed departure records. The display consumes that interface. Use the actual notebook contract to see exactly which fields are required. Click to expose the join, then the whole-product check. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">1:50</div>

# Ready means its prerequisites passed

```python {1-3|4-6|all}
def ready_tasks(tasks):
    return [key for key, task in tasks.items()
            if task["status"] == "pending"
            and all(tasks[parent]["status"] == "integrated"
                    for parent in task.get("depends_on", []))]
```
<div class="status-row"><span>Query: ready</span><span>Display: ready</span><span class="blocked">Integration: waiting for both</span></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>37 / 104</span></div>

<!--
Completed means accepted completion with saved output, not a worker’s progress narration. The local check should reject a task with an unmet dependency. The precise notebook record fields may include richer status metadata; preserve those contracts.
-->

---
class: technical-manual
clicks: 3
---

<div class="kicker">1:53</div>

# Claim each task once

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;race&quot;, &quot;label&quot;: &quot;Race&quot;, &quot;svg&quot;: &quot;01-race.svg&quot;, &quot;caption&quot;: &quot;What stops two ready workers from editing the same component?&quot;, &quot;src&quot;: &quot;/guides/transit/claims/slide/01-race.svg&quot;}, {&quot;id&quot;: &quot;atomic&quot;, &quot;label&quot;: &quot;Atomic&quot;, &quot;svg&quot;: &quot;02-atomic.svg&quot;, &quot;caption&quot;: &quot;What stops two ready workers from editing the same component?&quot;, &quot;src&quot;: &quot;/guides/transit/claims/slide/02-atomic.svg&quot;}, {&quot;id&quot;: &quot;dependency&quot;, &quot;label&quot;: &quot;Dependency&quot;, &quot;svg&quot;: &quot;03-dependency.svg&quot;, &quot;caption&quot;: &quot;What stops two ready workers from editing the same component?&quot;, &quot;src&quot;: &quot;/guides/transit/claims/slide/03-dependency.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;What stops two ready workers from editing the same component?&quot;, &quot;src&quot;: &quot;/guides/transit/claims/slide/04-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>38 / 104</span></div>

<!--
Use the local two-thread fixture, not a theoretical timing claim. Ask learners what changes if both read at the same time. A polite prompt does not make two Python operations atomic.
Visual guide: transit/claims. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---

<div class="kicker">1:56</div>

# A separate check and write permits two owners

<TransitMechanism mode="claim" :stage="1"/><p class="caption">The free exercise forces both reads before either assignment. Both callers think they claimed the task.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>39 / 104</span></div>

<!--
The controlled race uses a barrier to reproduce the condition. This two-owner outcome measures coordination code, not model intelligence. Show the broken if-pending then set-owner snippet in the notebook.
-->

---

<div class="kicker">2:00</div>

# One short transaction assigns one owner

<TransitMechanism mode="claim" :stage="2"/><p class="caption">board.claim checks readiness and assigns the owner while holding the lock. Model work happens after the lock is released.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>40 / 104</span></div>

<!--
The same two local threads now have one successful claim. The other gets a not-ready or already-claimed error. Holding the lock for the entire model call would serialize the work and block other claims.
-->

---

<div class="kicker">2:03</div>

# Keep the model call outside the claim transaction

```python
def claim_task(board, task_id, worker_id):
    return board.claim(task_id, worker_id)

# Inside the supplied board, simplified:
with board.transaction() as state:
    assert task_id in ready_tasks(state["tasks"])
    state["tasks"][task_id]["status"] = "running"
    state["tasks"][task_id]["worker_id"] = worker_id
```
<p class="caption">The participant calls the supplied atomic operation. The lower excerpt explains its critical section.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>41 / 104</span></div>

<!--
This is simplified teaching code; the actual store raises FactoryStop and also records dispatch identity, source and timing. Do not instruct participants to replace the store with this excerpt. The required code change is claim_task in the notebook.
-->

---
class: exercise
name: tasks-exercise
---

<div class="kicker">2:05</div>

# Make dependencies control the workers

<a class="answer-link" href="97">Worked answer ↗</a>

<p class="where">Notebook → Divide and claim the work</p><ol><li>Complete <code>ready_tasks()</code>.</li><li>Try the free check with one prerequisite still open.</li><li>Complete <code>claim_task()</code> so two workers cannot claim the same task.</li></ol><div class="done"><strong>Run:</strong> Check my ready_tasks code<br><strong>Check:</strong> Only unclaimed tasks with satisfied prerequisites can start.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>42 / 104</span></div>

<!--
Do not solve the race with a prompt asking agents to be careful. Claiming must be atomic in the shared task store. Let two local attempts contend for one task in the free exercise.
-->

---
clicks: 2
---

<div class="kicker">2:15</div>

# Separate working copies protect unfinished changes

<TransitMechanism mode="copies" :stage="$clicks"/><p class="caption">Ownership limits which file each worker can edit. The shared return schema still needs a combined application test.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>43 / 104</span></div>

<!--
This is a practical reason for independent workspaces, not a guarantee that the generated code is safe. Reviewed local code runs with bounded tools and time limits. Remote Sandboxes remain optional and require their own access. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">2:16</div>

# Each worker starts from the same source

<TransitMechanism mode="copies" :stage="0"/><p class="caption">Separate directories let both workers inspect the initial interface without overwriting one another.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>44 / 104</span></div>

<!--
Separate working files do not imply separate authority to change every file. Keep the common starting version visible. This is diagrammatic code flow, not a claim that all future tasks are independent.
-->

---

<div class="kicker">2:19</div>

# Each task can edit only its assigned module

<TransitMechanism mode="copies" :stage="1"/><p class="caption">The query task owns query.py. The presentation task owns presentation.py. Neither can change the trusted grader.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>45 / 104</span></div>

<!--
Point out which files are readable and which are editable. Both task contracts name the same return schema. The worker cannot repair a failing test by changing the evaluator.
-->

---
class: technical-manual
clicks: 3
---

<div class="kicker">2:22</div>

# Test the combined application

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;copies&quot;, &quot;label&quot;: &quot;Copies&quot;, &quot;svg&quot;: &quot;01-copies.svg&quot;, &quot;caption&quot;: &quot;Do the two components use the same interfaces and time conventions?&quot;, &quot;src&quot;: &quot;/guides/transit/integration/slide/01-copies.svg&quot;}, {&quot;id&quot;: &quot;patches&quot;, &quot;label&quot;: &quot;Patches&quot;, &quot;svg&quot;: &quot;02-patches.svg&quot;, &quot;caption&quot;: &quot;Do the two components use the same interfaces and time conventions?&quot;, &quot;src&quot;: &quot;/guides/transit/integration/slide/02-patches.svg&quot;}, {&quot;id&quot;: &quot;combined&quot;, &quot;label&quot;: &quot;Combined&quot;, &quot;svg&quot;: &quot;03-combined.svg&quot;, &quot;caption&quot;: &quot;Do the two components use the same interfaces and time conventions?&quot;, &quot;src&quot;: &quot;/guides/transit/integration/slide/03-combined.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Do the two components use the same interfaces and time conventions?&quot;, &quot;src&quot;: &quot;/guides/transit/integration/slide/04-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>46 / 104</span></div>

<!--
Explain why different files still need a combined test: both modules can disagree about a field or timezone. The hash guards against stale file replacement; it does not prove the interface is correct.
Visual guide: transit/integration. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---
class: exercise
---

<div class="kicker">2:25</div>

# Run the ready tasks with two workers



<p class="where">Notebook → Run two builders</p><ol><li>Review the task cards and file ownership.</li><li>Start the bounded run once.</li><li>Select a worker in the timeline and inspect its first task claim.</li></ol><div class="done"><strong>Run:</strong> Run the ready tasks with two workers<br><strong>Check:</strong> Each task has one owner. The trace identifies that worker’s starting code and resulting patch.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>47 / 104</span></div>

<!--
Keep the concurrency at two for the core exercise. More workers is an optional later experiment. Do not change model or total budget between comparisons and then attribute a difference only to coordination.
-->

---

<div class="kicker">2:35</div>

# Read the timeline as work and waiting

<div class="frame"><svg class="diagram" viewBox="0 0 1100 250" role="img" aria-label="Illustrative timeline: workers A and B run concurrently. Integration waits for both, then tests the merged application."><text x="0" y="58" style="font-size:24px">Worker A</text><text x="0" y="138" style="font-size:24px">Worker B</text><text x="0" y="218" style="font-size:24px">Integration</text><rect x="180" y="25" width="360" height="45" fill="#4382a6"/><rect x="180" y="105" width="500" height="45" fill="#c17b40"/><path d="M540 75V180M680 155V180" stroke="#61746e" stroke-dasharray="6 5" stroke-width="2"/><rect x="680" y="185" width="310" height="45" fill="#7c9e8a"/><text x="710" y="217" style="font-size:22px">Combined checks</text></svg></div><p class="caption">Illustrative durations. The live timeline uses saved timestamps and shows failures and unfinished work explicitly.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>48 / 104</span></div>

<!--
Ask which task is on the critical path. Parallel work can reduce elapsed time while increasing aggregate model cost. Queue time, execution time and integration time belong in separate fields.
-->

---

<div class="kicker">2:40</div>

# Find both submitted patches before integration

<p>In the saved task board, open each task’s diff and development-check result.</p><p>Confirm the task owner, changed file and tested source belong to the same attempt. A failed worker remains visible beside a successful one.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>49 / 104</span></div>

<!--
This is a checkpoint at 2:40, not a break. Integration starts at 2:45. If one worker is unfinished, keep that outcome and inspect the available record rather than inventing a completed patch.
-->

---

<div class="kicker">2:42</div>

# Review a patch before it enters the product

<TransitMechanism mode="copies" :stage="2"/><p class="caption">Read the actual diff, check its base hash, then apply it. A hash check prevents stale replacement; it cannot prove the two modules agree.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>50 / 104</span></div>

<!--
The user explicitly approved human review of task contracts and patches. Keep the actual diff visible next to its test output. Do not represent a review decision as an executed version until integration really runs. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---
class: exercise
---

<div class="kicker">2:45</div>

# Test the combined departures board



<p class="where">Notebook → Test the combined app</p><ol><li>Read both diffs and their test results.</li><li>Check <strong>I reviewed the two-builder patches and their development checks</strong>.</li><li>Run the combined checks. Then click <strong>Preview this saved app</strong> to inspect a departure.</li></ol><div class="done"><strong>Run:</strong> Test the combined departures board<br><strong>Check:</strong> The board’s result comes from the combined code you reviewed.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>51 / 104</span></div>

<!--
Show the combined source identity and acceptance output. If integration fails, preserve it and diagnose the failure before another edit. The facilitator can use the recorded controlled example if the live patches happen to work. This button now integrates only the two-worker build. The solo integration remains saved and is reused; after both results exist, the unchanged selection rule chooses the follow-up starting source.
-->

---

<div class="kicker">2:53</div>

# An integration error can cross a correct boundary

<div class="two-col"><div><h2>The parser returns</h2><p>Elapsed seconds from the service-day origin.</p></div><div><h2>The consumer assumes</h2><p>A time restricted to the current calendar day.</p></div></div><p>Both functions may pass narrow tests. The joined behavior loses an after-midnight departure.</p><p class="caption">Teaching example of a contract mismatch. Use the live check to determine whether this actually occurred.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>52 / 104</span></div>

<!--
Do not claim the current agents made this error unless its execution record shows it. This example explains why tests at component boundaries matter. The repair may be to code, task contract, tests or a combination.
-->

---
class: break
---

<div class="kicker">3:00</div>

# Break until 3:20

<p class="sub">Save the reviewed builds and their checks. After the break, we’ll decide what a future worker should remember from them.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>53 / 104</span></div>

<!--
Twenty-minute break, 3:00–3:20. Resume the same project. Do not change source or model settings to make the live result match the prepared example.
-->

---
class: aria-investigation
name: aria-investigate
---

<div class="kicker">3:20 · 8 minutes across these three frames</div>

# Investigate this result

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">Which development observation could support a useful project lesson?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/467e83bf4626e7fb910763fe0d55127c" target="_blank" rel="noopener">factory/integration/solo ↗</a></li><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/284f7f1dc00adf6c96f712568f19113c" target="_blank" rel="noopener">factory/integration/team ↗</a></li></ul></div></div><p class="aria-foot">Use only the selected development or validation records. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>54 / 104</span></div>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-investigate-response
---

<div class="kicker">3:20 · 8 minutes across these three frames</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-response.png" target="_blank"><img src="/aria/investigate/investigate-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>each also has a passing <code>participant_acceptance_check</code> for <code>departures/previous-service-day</code></blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/investigate/investigate-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e06f-16ab-7811-b1a9-35c56202d344" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>55 / 104</span></div>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-investigate-verify
---

<div class="kicker">3:20 · 8 minutes across these three frames</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/investigate/investigate-verification.png" target="_blank"><img src="/aria/investigate/investigate-verification.png" alt="The integrated team build passes its public development checks; weekday-evening is one visible checked case."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="622.0" y="267.0" width="635.0" height="105.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="608.0" cy="280.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="608.0" y="284.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="647.0" y="420.0" width="575.0" height="108.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="633.0" cy="433.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="633.0" y="437.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> Integrated team build</span><span><b>2</b> Public development checks</span></figcaption></figure><div><b>Citation check: supported</b><p>The saved solo and team integration results both pass departures/previous-service-day. Their matched expected and actual first departure is trip 63926435, service_date 2024-11-28, departure_time 2024-11-29T00:08:00-05:00. The native team capture confirms public integrated checks passed; the complete date values come from the supplied saved result. Passing these cases does not establish parser causality or coverage of all timezones.</p><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/467e83bf4626e7fb910763fe0d55127c" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/investigate/investigate-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>56 / 104</span></div>

<!--
Allocate 8 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/investigate.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---

<div class="kicker">3:28</div>

# Shared memory needs something worth sharing

<TransitMechanism mode="records" :stage="0"/><p class="caption">Store coordination, interfaces and experience separately. A task status does not establish that a general lesson is true.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>57 / 104</span></div>

<!--
Connect memory to a specific integration incident or verified behavior. Transcripts record what happened. A lesson is an interpretation intended to help a future task. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---
clicks: 2
---

<div class="kicker">3:29</div>

# Check the lesson before another agent relies on it

<MemoryFlow :stage="$clicks + 1"/><p class="caption">A checked lesson records its scope and supporting execution. A new contract can make it obsolete.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>58 / 104</span></div>

<!--
Click to reveal approved memory, then the fresh worker using it. A lesson can describe a successful pattern as well as a failure. Keep claims and verified observations distinct.
-->

---

<div class="kicker">3:30</div>

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
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>59 / 104</span></div>

<!--
Do not present this as a measured memory success. Explain scope: a rule about schedule times does not mean every display field should print hour 25. Keep the contract version, source evidence and review state visible.
-->

---
class: technical-manual
clicks: 3
---

<div class="kicker">3:31</div>

# Retrieve a lesson with evidence and scope

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;collections&quot;, &quot;label&quot;: &quot;Collections&quot;, &quot;svg&quot;: &quot;01-collections.svg&quot;, &quot;caption&quot;: &quot;Should this note enter the next worker’s request?&quot;, &quot;src&quot;: &quot;/guides/transit/memory/slide/01-collections.svg&quot;}, {&quot;id&quot;: &quot;filter&quot;, &quot;label&quot;: &quot;Filter&quot;, &quot;svg&quot;: &quot;02-filter.svg&quot;, &quot;caption&quot;: &quot;Should this note enter the next worker’s request?&quot;, &quot;src&quot;: &quot;/guides/transit/memory/slide/02-filter.svg&quot;}, {&quot;id&quot;: &quot;context&quot;, &quot;label&quot;: &quot;Context&quot;, &quot;svg&quot;: &quot;03-context.svg&quot;, &quot;caption&quot;: &quot;Should this note enter the next worker’s request?&quot;, &quot;src&quot;: &quot;/guides/transit/memory/slide/03-context.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;04-complete.svg&quot;, &quot;caption&quot;: &quot;Should this note enter the next worker’s request?&quot;, &quot;src&quot;: &quot;/guides/transit/memory/slide/04-complete.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>60 / 104</span></div>

<!--
The examples are illustrative records matching the retrieval schema, not four observations from R5. Ask which one a fresh worker should receive and which fields justify that choice.
Visual guide: transit/memory. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---

<div class="kicker">3:32</div>

# First exclude the unchecked interpretation

<TransitMechanism mode="memory" :stage="1"/><p class="caption">Only status="accepted" passes the review filter. Saving a proposal does not approve it.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>61 / 104</span></div>

<!--
The agent can propose a lesson. The participant checks its evidence and writes the accepted rule. This gate reduces propagation of guesses; it cannot guarantee the rule is correct in every context.
-->

---

<div class="kicker">3:33</div>

# Then check the applicable contract version

<TransitMechanism mode="memory" :stage="2"/><p class="caption">version identifies the contract where the rule applies. source_revision identifies the source that supplied its evidence.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>62 / 104</span></div>

<!--
Do not compare source_revision to the current code fingerprint. A lesson may be relevant to new code while citing an earlier version. The accepted contract version is the applicability check.
-->

---

<div class="kicker">3:35</div>

# Finally match the task’s scope and tags

<TransitMechanism mode="memory" :stage="3"/><p class="caption">The transit service-day task receives the reviewed transit rule. The billing rule remains stored but is not supplied.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>63 / 104</span></div>

<!--
select_memories performs these checks. No vector database is needed for this small project record. Let a participant explain why status alone would retrieve too much.
-->

---
class: exercise
name: memory-exercise
---

<div class="kicker">3:40</div>

# Save a lesson supported by an execution

<a class="answer-link" href="98">Worked answer ↗</a>

<p class="where">Notebook → Keep a checked lesson</p><ol><li>Click <strong>Check my select_memories code</strong>, then optionally <strong>Ask the agent to propose a lesson</strong>.</li><li>Choose a <strong>Supporting development result</strong>. Write the rule and its limits.</li><li>Click <strong>Save a checked lesson</strong>. Inspect the saved source and evidence.</li></ol><div class="done"><strong>Run:</strong> Save a checked lesson<br><strong>Check:</strong> The saved lesson opens its supporting event, and unrelated or superseded lessons are excluded.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>64 / 104</span></div>

<!--
Participants must inspect the evidence rather than approve an agent summary blindly. The retrieval function affects the later actual worker request. A directory listing is not proof that a worker read a lesson.
-->

---

<div class="kicker">3:50</div>

# Inspect the memory read, then its effect

<div class="flow"><div>Memory selected<small>Which rule matched this task?</small></div><b class="arrow">→</b><div>Worker request<small>Was that text actually supplied?</small></div><b class="arrow">→</b><div>Code and test<small>What did the worker do with it?</small></div></div><p>Open the Agent Lens memory event and the next model request. Then inspect the resulting patch.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>65 / 104</span></div>

<!--
This is the trace-to-behavior chain. A citation or read event establishes consultation, not that the memory caused an improvement. The matched follow-up comparison is what tests that question.
-->

---

<div class="kicker">4:00</div>

# Find the last direct train between two stops

<TransitMechanism mode="matched" :stage="0"/><p class="caption">Both teams receive the identical follow-up feature. Freeze the selected lesson before running either condition.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>66 / 104</span></div>

<!--
The follow-up asks for the last direct train between two retained stations, including arrival after midnight, a no-direct-service result and an itinerary download. Each branch uses two workers. Both branches execute; no prerecorded result is substituted for one side. This small paired example teaches the method. One pair cannot establish repeatability or general superiority. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">4:02</div>

# Start both follow-ups from the same release

<TransitMechanism mode="matched" :stage="0"/><p class="caption">Both teams add last_departure and render_journey. Only one receives the accepted project lesson.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>67 / 104</span></div>

<!--
Each build has two workers. The coordinator invokes the two builds in order, while each build may run its two workers concurrently. Do not describe the two conditions as synchronized or simultaneous. Compare saved initial fingerprints.
-->

---

<div class="kicker">4:05</div>

# Keep both sets of patches and checks

<TransitMechanism mode="matched" :stage="1"/><p class="caption">Review both outcomes before running the independent comparison. An unsuccessful branch remains part of the result.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>68 / 104</span></div>

<!--
The specification, starting code, fixed research model, limits and tool implementation are held the same. The lesson cannot be edited after inspecting the first outcome and still count as a matched pair.
-->

---

<div class="kicker">4:07</div>

# The follow-up returns a journey, not a list of guesses

```python
journey = last_departure(
    tables, origin_id, destination_id, service_date
)
# Return one direct trip with departure and arrival timestamps.
# Return None when no direct service exists in the retained feed.
html = render_journey(journey, title="Last direct train")
```
<p class="caption">Contract excerpt. A valid arrival may occur after midnight. The itinerary download must preserve the returned journey.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>69 / 104</span></div>

<!--
Explain the function inputs and two valid output shapes. The retained dataset is small, so None concerns this schedule subset. It is not a statement that no real-world route exists. The renderer cannot invent a trip when the query returns None.
-->

---
class: exercise
---

<div class="kicker">4:10</div>

# Run both versions of the follow-up feature



<p class="where">Notebook → Build the next feature</p><ol><li>Review the follow-up contract and the selected lesson.</li><li>Confirm the starting code is identical for both runs.</li><li>Run both branches. Read their diffs and check <strong>I reviewed the no-lesson and shared-lesson patches</strong> before integrating.</li></ol><div class="done"><strong>Run:</strong> Run both versions of the follow-up feature → Integrate the reviewed follow-up patches<br><strong>Check:</strong> The comparison includes both actual outputs, costs and trace links, even if one fails.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>70 / 104</span></div>

<!--
Keep memory fixed during this matched comparison. Do not edit it after seeing the no-memory result and call the pair controlled. If budget or infrastructure prevents a branch from finishing, retain a missing result and label the pair incomplete.
-->

---

<div class="kicker">4:27</div>

# The factory has two kinds of state

<TransitMechanism mode="records" :stage="0"/><p class="caption">Task records resume the current build. Contracts and checked lessons inform future work. None requires one giant shared chat.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>71 / 104</span></div>

<!--
This is the distinction between a task ledger and learning. Neither requires sharing a giant conversation among all workers. Both need durable records, clear identities and bounded retrieval. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">4:32</div>

# Find where the lesson entered the request

<p>In Agent Lens, open the follow-up query worker. Find its memory-read result, then inspect the next model request.</p><div class="three-checks"><div><b>Retrieved</b><p>Which accepted rule?</p></div><div><b>Supplied</b><p>Which text reached the model?</p></div><div><b>Executed</b><p>Which edit and check followed?</p></div></div><p class="caption">A recorded read establishes consultation. The matched outputs determine what happened to the product.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>72 / 104</span></div>

<!--
If no explicit read_memory action is present, distinguish the initial read_shared_memory selection from an agent-initiated read. Do not claim peer messaging unless the saved events contain it. The R5 workers were coordinated through task records and supplied lessons.
-->

---

<div class="kicker">4:38</div>

# Keep a stopped worker’s files and error

<p>Open the failed task. Inspect the last successful operation, saved source and failed request.</p><p>Retrying publication only exports saved work. Retrying execution is a separate action and can incur cost.</p><p class="caption">After freezing the comparison, preserve its failure. A changed coordinator or limit belongs in a new workspace.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>73 / 104</span></div>

<!--
Use Recover stopped work only after confirming the earlier execution stopped. A request with an uncertain outcome remains conservatively charged. A bound error is not fixed merely by clicking again. The six-hour schedule includes time to interpret an incomplete build, not unlimited retries.
-->

---
class: break
---

<div class="kicker">4:45</div>

# Break until 4:55

<p class="sub">Keep both follow-up outcomes. We will freeze the available versions and compare their actual outputs when we return.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>74 / 104</span></div>

<!--
Ten-minute break, 4:45–4:55. Stop adding features. The final comparison must include failed or incomplete branches.
-->

---
class: technical-manual
clicks: 5
---

<div class="kicker">4:55</div>

# Measure delivery, coordination, and memory separately

<TechnicalGuide :frames="[{&quot;id&quot;: &quot;match&quot;, &quot;label&quot;: &quot;Match&quot;, &quot;svg&quot;: &quot;01-match.svg&quot;, &quot;caption&quot;: &quot;Which outcome supports the claim that the team or lesson helped?&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/01-match.svg&quot;}, {&quot;id&quot;: &quot;initial&quot;, &quot;label&quot;: &quot;Initial&quot;, &quot;svg&quot;: &quot;02-initial.svg&quot;, &quot;caption&quot;: &quot;Which outcome supports the claim that the team or lesson helped?&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/02-initial.svg&quot;}, {&quot;id&quot;: &quot;memory&quot;, &quot;label&quot;: &quot;Memory&quot;, &quot;svg&quot;: &quot;03-memory.svg&quot;, &quot;caption&quot;: &quot;Which outcome supports the claim that the team or lesson helped?&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/03-memory.svg&quot;}, {&quot;id&quot;: &quot;release&quot;, &quot;label&quot;: &quot;Release&quot;, &quot;svg&quot;: &quot;04-release.svg&quot;, &quot;caption&quot;: &quot;Which outcome supports the claim that the team or lesson helped?&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/04-release.svg&quot;}, {&quot;id&quot;: &quot;complete&quot;, &quot;label&quot;: &quot;Complete view&quot;, &quot;svg&quot;: &quot;05-complete.svg&quot;, &quot;caption&quot;: &quot;Which outcome supports the claim that the team or lesson helped?&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/05-complete.svg&quot;}, {&quot;id&quot;: &quot;native-capture&quot;, &quot;label&quot;: &quot;The exact solo release and its files&quot;, &quot;svg&quot;: &quot;06-native-capture.svg&quot;, &quot;caption&quot;: &quot;Find sources, source_fingerprint, and checksums. Download the artifact because long source lines are truncated in this view.&quot;, &quot;src&quot;: &quot;/guides/transit/comparison/slide/06-native-capture.svg&quot;}]" :step="$clicks" />
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>75 / 104</span></div>

<!--
Avoid a composite score that conceals these tradeoffs. The saved product rows are matched across versions. Missing builds or evaluations remain missing, not silently dropped or converted to ordinary task failures. Repeated task claims include explicit recovery; overlapping reasoning and semantically duplicated code are not measured. Coverage is separate from passed-case rate.
Visual guide: transit/comparison. Advance one state at a time; Back restores the preceding state. The notebook uses the same source figure beside its exercise. Follow the intermediate value to the matching code. These are explanatory frames; they do not execute an experiment or imply a learner result.
-->

---

<div class="kicker">4:58</div>

# A scenario is an input and an expected behavior

```python {1-2|4-6|all}
def score_scenario(actual, expected):
    return actual == expected

expected = ["trip-1", "trip-2"]
assert score_scenario(["trip-1", "trip-2"], expected)
assert not score_scenario(["trip-2", "trip-1"], expected)
```
<p class="caption">The exercise uses public development cases. The independent final grader checks the complete required fields and order.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>76 / 104</span></div>

<!--
This is a compact teaching excerpt, not the complete final acceptance scorer. Explain why sorting the identifiers before comparing would hide an ordering defect. Failed execution is not equivalent to a valid empty departure list.
-->

---
class: exercise
name: evaluate-exercise
---

<div class="kicker">5:03</div>

# Compare the frozen builds on matching cases

<a class="answer-link" href="104">Worked answer ↗</a>


<p class="where">Notebook → Compare frozen builds</p><ol><li>Complete <code>score_scenario()</code>. Click <strong>Check my score_scenario code</strong>.</li><li>Freeze the reviewed build versions.</li><li>Run final scenarios and open the comparison in Forge.</li></ol><div class="done"><strong>Run:</strong> Compare the frozen builds<br><strong>Check:</strong> Each row uses the same input across versions. A score links to the executed code and actual output.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>77 / 104</span></div>

<!--
Final grading happens after the build choices freeze. Evaluation Tables Preview uses the working Weave-backed publication path. If publication fails, inspect the notebook rows and retry publication only; do not rerun model work.
-->

---

<div class="kicker">5:08</div>

# Read one comparison row before the average

<div class="frame"><p><strong>Input:</strong> the same stop, service date and requested time.</p><p><strong>Outputs:</strong> each frozen build’s departure list.</p><p><strong>Scores:</strong> whether each requirement passed.</p><p><strong>Links:</strong> the worker trace, reviewed diff and code artifact.</p></div><p>In EvalTables, set the starting build as reference. Open a difference and explain it using the actual departures.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>78 / 104</span></div>

<!--
Use one scenario to explain the matching inputs, actual outputs and pass criteria before opening the native comparison on the next slide. Keep its source URL and recorded rehearsal identity visible.
-->

---

<div class="kicker">5:10</div>

# Compare the same departures in Forge

<div class="native-wide"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=5lkijosxo9y"><img src="/images/native-comparison-r4-detail.png" alt="Actual Forge Evaluation Tables Preview comparison with one-builder reference, two-builder output, equal pass rates and aligned departure cases"/></a><span class="eval-native-pin" style="left:15%;top:3%">1</span><span class="eval-native-pin" style="left:9%;top:44%">2</span><span class="eval-native-pin" style="left:34%;top:40%">3</span></div><p class="eval-native-caption"><strong>1.</strong> One builder is the reference. <strong>2.</strong> Each row uses the same case. <strong>3.</strong> Read both outputs. Earlier rehearsal R4: both first builds passed 10 / 10.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>79 / 104</span></div>

<!--
Actual native Evaluation Tables Preview, verified in a signed-out browser. The saved workspace contains two frozen first-release builds and ten matching scenarios, with all twenty underlying evaluation rows read back. This image does not represent the R4 memory followups, which were incomplete. Open a prediction cell and inspect the service date before treating a matching average as sufficient evidence.
-->

---

<div class="kicker">5:13</div>

# The faster build missed two final cases

<TransitMechanism mode="outcomes" :stage="0"/><p class="caption">Both first builds passed development checks. The reserved UTC cases exposed a wrong train in the team output. Follow-up results appear separately below.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>80 / 104</span></div>

<!--
These are final native scores from R5, a separate engineering rehearsal after context compaction changed. All 56 scenario rows are represented. The first builds passed five public development checks each, but the two-worker final product passed only eight of ten reserved scenarios. Do not treat the earlier R4 native screenshot as this R5 comparison. Builder elapsed excludes human review and integration. Actual provider request counts were 8, 12, 5 and 5 respectively. The no-memory query reached its input bound after writing; the memory query exhausted its output allowance. Both stopped before query tests; presentation was retained unchanged. The lesson proposal cost an additional $0.00143474. Total observed inference was $0.06635800 across 31 provider requests, with zero unknown usage. This single pair cannot establish a general speed or memory effect. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">5:15</div>

# Open the two failing rows in the final comparison

<div class="native-wide"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=dg2ogm6wp3z"><img src="/images/native-comparison-r5-detail.png" alt="R5 native comparison showing one-builder pass rate 1, two-builder 0.8, and the UTC-input rows with different trip IDs"/></a><span class="eval-native-pin" style="left:36%;top:14%">1</span><span class="eval-native-pin" style="left:2%;top:88%">2</span><span class="eval-native-pin" style="left:35%;top:88%">3</span></div><p class="eval-native-caption"><b>1.</b> 10/10 versus 8/10. <b>2.</b> The two UTC-input cases. <b>3.</b> The selected trip differs. Recorded R5, separate from the R4 comparison.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>81 / 104</span></div>

<!--
Use the actual saved native view. The bottom two rows show the query and integrated application cases. Both select 63919613 in the solo output and 63919759 in the team output. The screenshot is preserved; numbered annotations sit beside the relevant fields. Capture provenance is in notes/r5-capture-receipt.json.
-->

---
clicks: 2
---

<div class="kicker">5:16</div>

# A timezone assumption selected the wrong train

<TransitMechanism mode="timezone" :stage="$clicks"/><p class="caption">Follow the request, selected GTFS row and rendered board. These are two failed checks of one timezone bug, not two independent defects.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>82 / 104</span></div>

<!--
The failed cases were departures/utc-input and integrated/departures/utc-input. The two-worker query anchored GTFS service-day midnight to the caller’s timezone. It selected a service-clock 23:03 trip rather than the expected 18:03 Eastern departure after a 23:00 UTC request. The solo query preserved the fixed feed timezone for this historical subset. These are two checks of one defect, not two independent bugs. Both failed follow-up query edits left this earlier bug in place. Ask participants which contract or test they would add before another build. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---

<div class="kicker">5:18</div>

# Interpret the request as one instant

<TransitMechanism mode="timezone" :stage="0"/><p class="caption">The R5 final case sends 23:00 UTC. The next departure is 18:03 in the feed’s Eastern timezone.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>83 / 104</span></div>

<!--
Recorded R5 case: departures/utc-input. This is a same-instant conversion. The feed clock defines the origin of GTFS elapsed service time; the caller is allowed to express the request using another offset. The paired clock positions show matching instants, with nonuniform spacing for legibility. The third position is five hours after the expected departure.
-->

---

<div class="kicker">5:20</div>

# The team used the caller’s clock for service time

<TransitMechanism mode="timezone" :stage="1"/><p class="caption">The code selected trip 63919759 from service-clock 23:03. It should have selected trip 63919613 at 18:03 Eastern.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>84 / 104</span></div>

<!--
Recorded behavior, not a hypothesized defect. The team anchored service-day midnight to the request timezone. This changed the chosen record, not only its formatted text. Inspect the source and actual prediction beside the expected row. The paired clock positions show matching instants, with nonuniform spacing for legibility. The third position is five hours after the expected departure.
-->

---

<div class="kicker">5:22</div>

# The renderer carried the same wrong trip into the board

<TransitMechanism mode="timezone" :stage="2"/><p class="caption">departures/utc-input and integrated/departures/utc-input failed for the same reason. Count two failed scenarios and one observed bug.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>85 / 104</span></div>

<!--
The independent suite checks both the query and the complete application. Avoid describing these correlated cases as two independent coding errors. Learners should propose a public UTC-input regression case for a future experiment, after retaining the current outcome. The paired clock positions show matching instants, with nonuniform spacing for legibility. The third position is five hours after the expected departure.
-->

---

<div class="kicker">5:24</div>

# Neither follow-up completed the query change

<TransitMechanism mode="matched" :stage="2"/><p class="caption">Open both failed requests in Agent Lens. Neither branch reached query testing, so this pair cannot establish a memory benefit.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>86 / 104</span></div>

<!--
Without memory: oversized input after a saved write. With memory: output allowance exhausted before a complete first action. Both query tasks stopped before testing. The existing query remained; these outcomes do not establish that shared memory caused either failure. Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">5:25</div>

# More workers can still produce more waiting

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="transit/compare"><img :src="&quot;/scenes/transit/compare.svg&quot;" alt="Transit build room: Extra workers can wait on the same shared resource. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><p>Compare the actual time spent coding with time spent waiting, reviewing and repairing integration.</p><p>Then compare the cost of the completed product. A faster worker trace does not mean a cheaper or better delivered application.</p><p class="caption">Research and production reports find coordination gains depend on task structure. This workshop measures its own runs.</p></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>87 / 104</span></div>

<!--
Primary sources: Claude Code agent-team docs, Google Research scaling-agent-systems study and Anthropic compiler report. Do not import their performance numbers as a forecast for this model or task.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---

<div class="kicker">5:30</div>

# Choose a release using the saved checks

<div class="flow"><div>Frozen build<small>Exact code and data</small></div><b class="arrow">→</b><div>Release decision<small>Required scenarios passed?</small></div><b class="arrow">→</b><div>Versioned artifact<small>Can another run reproduce it?</small></div></div><p>If a required check fails, keep the previous version and explain the failed condition.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>88 / 104</span></div>

<!--
The release is a versioned workshop artifact, not an automatic public service deployment. Agent-generated recommendations do not bypass required checks. Preserve previous versions for reproduction and rollback.
-->

---
class: aria-investigation
name: aria-conclusion
---

<div class="kicker">5:35 · 7 minutes across these three frames</div>

# Check our conclusion

<div class="aria-sequence-wrap"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:#f4f3ef;max-width:100%"><title>Start once, open the same conversation, check its source</title><desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc><rect x="8" y="8" width="320" height="183" fill="white" stroke="#242522"/><path d="M8 42h320" stroke="#242522"/><text x="22" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">01  Notebook · your saved result</text><text x="24" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Question + your explanation</text><rect x="24" y="81" width="139" height="29" fill="#e8e9e3" stroke="#242522"/><text x="34" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">selected run</text><rect x="172" y="81" width="138" height="29" fill="#e8e9e3" stroke="#242522"/><text x="180" y="101" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">conversation</text><rect x="24" y="128" width="286" height="43" fill="#e8e9e3" stroke="#242522"/><text x="40" y="155" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Start ARIA investigation</text><path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2"/><text x="336" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">send</text><rect x="393" y="8" width="330" height="183" fill="white" stroke="#242522"/><path d="M393 42h330" stroke="#242522"/><text x="407" y="31" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">02  ARIA · the same conversation</text><text x="409" y="67" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">turn_id</text><text x="534" y="67" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">saved locally</text><text x="409" y="93" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:16px">queued → in progress</text><path d="M410 106h296" stroke="#242522"/><text x="410" y="130" fill="#ec5b28" style="font-family:IBM Plex Sans,sans-serif;font-size:17px">Open ARIA conversation</text><rect x="410" y="142" width="296" height="32" fill="#f4f3ef" stroke="#242522"/><text x="421" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Ask a follow-up in Forge</text><path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="#242522" stroke-width="2" stroke-dasharray="5 4"/><text x="732" y="84" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:14px">cite</text><path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="#242522"/><text x="807" y="34" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:18px">03  Check the saved source</text><text x="809" y="68" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">ARIA claim → exact field</text><rect x="809" y="80" width="271" height="32" fill="#e8e9e3" stroke="#ec5b28" stroke-width="2"/><text x="820" y="102" fill="#242522" style="font-family:IBM Plex Mono,monospace;font-size:15px">value / event / code line</text><text x="809" y="140" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Supported? Disputed?</text><text x="809" y="164" fill="#242522" style="font-family:IBM Plex Sans,sans-serif;font-size:16px">Unresolved is a valid answer.</text></svg></div><div class="aria-question">Did coordination or the accepted lesson improve the delivered application?</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Click Start ARIA investigation in the notebook, then Open ARIA conversation.</p></div><div><b>Selected instructor records</b><ul class="aria-records"><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/e11ffa49b71896fb877e2a7c821fa2e1" target="_blank" rel="noopener">factory/evaluate/solo ↗</a></li><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/a8d73a215bf11c9ae267956656f05caa" target="_blank" rel="noopener">factory/evaluate/team ↗</a></li><li><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/6c7b7b6daeb47890999aa69754554369" target="_blank" rel="noopener">factory/evaluate/without-memory ↗</a></li></ul></div></div><p class="aria-foot">Keep the compared versions frozen. Suggest a future experiment without running it. The saved request carries this project and selected native references. Open its conversation while ARIA works.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>89 / 104</span></div>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-conclusion-response
---

<div class="kicker">5:35 · 7 minutes across these three frames</div>

# Read one claim in the recorded response

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-response.png" target="_blank"><img src="/aria/conclusion/conclusion-response.png" alt="Actual ARIA response. Check its distinction between retrieved native records and supplied evidence excerpts."></a></figure><div><b>Recorded instructor investigation</b><blockquote>no follow-up pass-count increase</blockquote><p>Does this statement follow from the records, or is it a possible explanation?</p><p><a href="/aria/conclusion/conclusion-transcript.html" target="_blank">Read the full transcript without sign-in ↗</a></p><a href="https://forge.coreweave.com/aria/threads/01a1e070-7cf7-7943-9cb1-46e6662df358" target="_blank" rel="noopener">Open the recorded conversation ↗</a></div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>90 / 104</span></div>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: aria-investigation
name: aria-conclusion-verify
---

<div class="kicker">5:35 · 7 minutes across these three frames</div>

# Open the source and check that claim

<div class="aria-response"><figure class="aria-screen"><a href="/aria/conclusion/conclusion-verification.png" target="_blank"><img src="/aria/conclusion/conclusion-verification.png" alt="First-release native comparison: one builder passes 10/10 scenarios; two coordinated builders pass 8/10."><svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true"><rect x="388.0" y="350.0" width="275.0" height="95.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="374.0" cy="363.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="374.0" y="367.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">1</text><rect x="1090.0" y="672.0" width="160.0" height="30.0" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="1076.0" cy="685.0" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="1076.0" y="689.0" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">2</text></svg></a><figcaption><span><b>1</b> 1.0 versus 0.8 pass rate</span><span><b>2</b> Ten matching cases</span></figcaption></figure><div><b>Citation check: supported</b><p>The saved factory/evaluate/solo, team, without-memory, and with-memory results contain passed_count/total values 10/10, 8/10, 12/18, and 12/18. These match the native independent_acceptance events reported by ARIA. The first native EvalTables capture shows the separate 10-case comparison only. The UTC case has different trip IDs despite timestamps representing the same instant; a propagated defect is a hypothesis, not an established root cause.</p><a href="https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/e11ffa49b71896fb877e2a7c821fa2e1" target="_blank" rel="noopener">Open the checked source ↗</a><p><a href="/aria/conclusion/conclusion-source-records.html" target="_blank">Check the supplied source values offline ↗</a></p></div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>91 / 104</span></div>

<!--
Allocate 7 minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. The notebook agent still produces the measured changes. ARIA only investigates saved records. Use Start ARIA investigation, then Open ARIA conversation. The explicit click sends one question with native run and Agent Lens conversation references. ARIA works asynchronously while the participant inspects the selected result. Check ARIA response reads that saved turn; opening and restoration never resend it. Verify the source ARIA actually read. Exact artifact-version URLs remain in the question; excerpt-only analysis must stay labeled. ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. Recording: src/forge_workshop_kit/assets/aria/transit_factory/conclusion.json. Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.
-->

---
class: exercise
name: release-exercise
---

<div class="kicker">5:42</div>

# Publish the version you can reproduce

<a class="answer-link" href="99">Worked answer ↗</a>

<p class="where">Notebook → Reproduce and release</p><ol><li>Complete <code>release_decision()</code> and click <strong>Check my release_decision code</strong>.</li><li>Write the decision in your own words, including any regression.</li><li>Publish the code, data reference, checks and conclusion together.</li></ol><div class="done"><strong>Run:</strong> Publish this release and its evidence<br><strong>Check:</strong> Reload a saved case from the release artifact and reproduce its departure list.</div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>92 / 104</span></div>

<!--
Use the last half-hour for reproduction, release and a short explanation. R5 supports releasing the one-worker departures board. Failed required checks block the follow-up. The output is an artifact and Report, not automatic production deployment.
-->

---

<div class="kicker">5:44</div>

# Reload the selected app and repeat one case

<ol><li>Open the released artifact and identify its source and dataset versions.</li><li>Extract the app bundle and run <code>uv run --with marimo marimo edit app.py</code>.</li><li>Choose the same stop and timestamp. Compare the returned trip ID and dates with the saved case.</li></ol><p class="caption">Use the app from your selected release. The separately labeled reference download is instructor-authored.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>93 / 104</span></div>

<!--
This is a local inference-free reproduction. It shows that the delivered source and data yield the saved behavior. It is not a rerun of the stochastic coding agents. Verify one row, not merely that the app opens.
-->

---

<div class="kicker">5:48</div>

# Explain one result to another participant

<ol><li>Show the feature and the departure list it produced.</li><li>Open one worker’s change and its acceptance result.</li><li>Show a shared lesson that was read, or explain why none applied.</li><li>State what you would change in the next factory run.</li></ol><p class="caption">A faster build, a better build, a tie and a regression are different outcomes. Report the one you observed.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>94 / 104</span></div>

<!--
Give participants two minutes each. The person explaining should control the notebook and open the relevant record. The facilitator should not take the keyboard or supply the conclusion.
-->

---
class: workshop-setting-slide
clicks: 1
---

<div class="kicker">5:58</div>

# Take the coordination code to your own project

<figure v-if="$clicks === 0" class="workshop-setting-frame" data-workshop-scene="transit/release"><img :src="&quot;/scenes/transit/release.svg&quot;" alt="Transit build room: Carry a lesson forward only after checking its effect. Illustrative setting." /><figcaption><span>Next → explanation and evidence</span></figcaption></figure>
<div v-else class="workshop-setting-detail"><p>Start with a feature whose acceptance behavior you can check. Split independent work, give each task an owner, and test the changes together.</p><p>Keep lessons that another task can use, with their evidence and limits. Then measure whether the team improves the work enough to justify its coordination cost.</p></div>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>95 / 104</span></div>

<!--
Ask each person for one suitable feature, one prerequisite, one acceptance check and one durable project rule from their own team. ARIA is outside the measured comparison and may require additional access.
Setting frame: point to the active work object, then advance to the complete explanation. This is an illustrated situation, not an execution screenshot. Back restores the scene; the following diagram reveals keep their original order.
-->

---
class: workshop-sharing
name: workshop-take-home
clicks: 0
---

<div class="kicker">5:58</div>

# Keep the notebook and workshop materials

<div class="workshop-share-layout"><div class="workshop-share-instructions"><p>Reopen your saved notebook file to continue your work.</p><ol><li><strong>Revisit the example.</strong> The Report links its claims to recorded results.</li><li><strong>Keep the materials.</strong> Open the deck, download the PDF, or get the source.</li><li><strong>Run a session.</strong> Use the short run guide and facilitator notes.</li></ol></div><div class="workshop-share-code"><a href="https://utm.io/uuIaa" aria-label="Open this workshop’s materials"><img src="/images/workshop-qr.svg" width="280" height="280" alt="QR code opening this workshop’s notebook, deck, Report, and run guide"></a><a class="workshop-share-url" href="https://utm.io/uuIaa">utm.io/uuIaa</a><p>Notebook · Report · Deck · Run guide</p></div></div><p class="workshop-share-footer">The shared page has the current download and references. Your Forge records remain in your own project.</p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>96 / 104</span></div>

<!--
Keep this slide up during questions. Participants resume their saved notebook file. The QR page provides the current notebook, Report, downloads, and short facilitator run guide. Use recorded examples for a demo; check the current readiness notes before scheduling live delivery.
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
    # Read readiness and assign the owner inside the same locked transaction.
    return board.claim(task_id, worker_id)
```
<p>Make the claim atomic in the task store. Recheck status while holding its lock, then assign one owner.</p><p class="answer-nav source-link"><a href="42">Return to the task exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>97 / 104</span></div>

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
<p class="answer-nav source-link"><a href="64">Return to the memory exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>98 / 104</span></div>

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
    # Empty or missing checks must not become a passing release.
    return bool(rows) and all(
        row.get("passed") is True for row in rows
    )
```
<p class="answer-nav source-link"><a href="92">Return to the release exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>99 / 104</span></div>

<!--
This teaching excerpt deliberately blocks missing results and empty check lists. Use the executable notebook record shape for the real decision. A valid release requires the code and checks to refer to the same frozen build.
-->

---
name: workflow-sources
---

<div class="kicker">Reference</div>

# Sources for the workflow

<ul class="source-list"><li><a href="https://factory.strongdm.ai/">StrongDM: software factory concepts and scenarios</a></li><li><a href="https://www.anthropic.com/research/building-c-compiler">Anthropic: independent workspaces, task claims and integration</a></li><li><a href="https://code.claude.com/docs/en/agent-teams">Claude Code: shared tasks, messages and coordination limits</a></li><li><a href="https://github.com/gastownhall/gastown">Gas Town: durable work state and merge verification</a></li><li><a href="https://github.com/gastownhall/beads">Beads: dependency-aware tasks and project memory</a></li></ul>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>100 / 104</span></div>

<!--
These are references for patterns, not required workshop installations. The notebook keeps its coordinator visible in Python and uses the existing Forge Workshop Kit. Software factory has several definitions; use the implemented workshop definition.
-->

---

<div class="kicker">Reference</div>

# Sources for the data and evaluation

<ul class="source-list"><li><a href="https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md">MBTA feed documentation</a></li><li><a href="https://gtfs.org/documentation/schedule/reference/">GTFS schedule reference</a></li><li><a href="https://www.anthropic.com/research/components-of-agent-memory">Anthropic: memory notes, validation and correction</a></li><li><a href="https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/">Google Research: when coordination helps and hurts</a></li><li><a href="https://github.com/ash0ts/forge-workshop-kit">Workshop code, source receipts and current access instructions</a></li></ul>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>101 / 104</span></div>

<!--
The downloaded dataset manifest is authoritative for archive date, checksums, selected rows and licensing. Do not substitute current live schedule data during a comparison. The software-factory teaching experiment is not a transit reliability benchmark.
-->

---
class: answer
name: acceptance-answer
---

<div class="kicker">Reference</div>

# Worked answer: check the after-midnight departure

```python
def check_departures(rows):
    return any(
        row["trip_id"] == "63926435"
        and row["service_date"] == "2024-11-28"
        and row["departure_time"] == "2024-11-29T00:08:00-05:00"
        for row in rows
    )
```
<p class="caption source-link"><a href="15">Return to the acceptance exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>102 / 104</span></div>

<!--
Reveal only after an attempt or requested hint. This checks one public scenario; it does not replace the independent final scorer.
-->

---
class: answer
name: worker-answer
---

<div class="kicker">Reference</div>

# Worked answer: dispatch one allowed tool

```python
def dispatch_action(action, tools):
    name = action["action"]
    if name not in tools:
        raise ValueError("Unknown builder operation: " + name)
    return tools[name](action)
```
<p class="caption source-link"><a href="28">Return to the worker exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>103 / 104</span></div>

<!--
Read action["action"], select the provided callable, invoke it exactly once and return the observation unchanged. The free check rejects an unavailable shell action.
-->

---
class: answer
name: evaluate-answer
---

<div class="kicker">Reference</div>

# Worked answer: check the departure order

```python
def score_scenario(actual, expected):
    return actual == expected

assert score_scenario(["trip-1", "trip-2"], ["trip-1", "trip-2"])
assert not score_scenario(["trip-2", "trip-1"], ["trip-1", "trip-2"])
```
<p class="caption source-link"><a href="77">Return to the comparison exercise ↩</a></p>
<div class="footer"><span>Forge Workshop Kit · Transit software factory</span><span>104 / 104</span></div>

<!--
This participant development check tests exact ordered trip IDs. The independent final scorer also checks the other required fields. A missing judgment is not False.
-->
