## 1. Build a transit app with a team of coding agents

0:00

The department and deadline are fictional. The schedule records are real public MBTA data. Participants build a bounded software factory; we do not claim to reproduce an unattended production engineering organization.

## 2. Your team needs a departures board

0:01

Start with the person using the software. Ask what could make a plausible-looking board wrong. Listen for wrong date, wrong stop, missing departures and misleading times. No model or agent count appears before the product is clear.

## 3. Here is the application we want to deliver

0:02

This is a real capture of the reference implementation, not a model outcome. Participants will inspect the app their workers actually produce. Call out the selected Park Street platform, midnight on November 29, and first scheduled departure at 00:08. The next slides explain why that train belongs to November 28 service.

## 4. The inputs are public transit records

0:03

Open the notebook data receipt and read its archive date and checksum. Do not describe the small teaching subset as the complete MBTA system. MBTA describes its feed at https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md .

## 5. The last train can belong to yesterday’s service

0:05

This is an actual retained row: trip 63926435, stop 70076, departure_time 24:08:00, stop_sequence 150, ThanksgivingDay service, headsign Alewife. The civil timestamp is 2024-11-29T00:08:00-05:00. Ask what a parser restricted to 0..23 hours would do. The rule must survive between components.

## 6. Turn the brief into checks

0:07

These are requirements for our product, not a claim that the initial code fails them. Show the concrete acceptance inputs and expected outputs in the notebook. Final cases stay outside the coding-worker context until the versions are frozen.

## 7. A software factory needs a way to finish work

0:08

Software factory is a broad term. This slide states the operational meaning we implement. It includes specification, coordination, verification and release. It is not simply a chat room with several role prompts.

## 8. Add the task board and two workers

0:09

Click once to reveal workers, once to reveal integration, once to reveal the checked lesson. Solid arrows show code or execution flow. The dashed arrow identifies reviewed evidence. The diagram is explanatory, not a recorded run.

## 9. Your project contains the experiment

0:10

Keep the distinction between agents sharing project records and attendees sharing credentials. The latter does not happen. The notebook has an adjustable inference allowance; notebook compute is billed separately. Opening the notebook does not start agents.

## 10. Connect and inspect the source data

0:11

Do not ask participants to paste a key into a code cell. Hosted authentication comes from their own account. Locally use wandb login. Access checks should distinguish a writable project from inference entitlement.

## 11. Write the after-midnight acceptance check

0:15

The scenario is written by the participant and later runs on the integrated app. It is public development evidence, not a hidden final answer. Show how a plausible train list can still use the wrong service day.

## 12. One worker still needs a complete loop

0:20

Start with the familiar single-agent harness. Multiple agents do not remove the need for correct tool observation handling, explicit stopping and independent checks. Model settings stay fixed in the comparisons.

## 13. Give the worker the task it is allowed to solve

0:23

Explain each input before editing: task is the approved contract, sources are the current worker copy, lessons are explicitly retrieved project memory. This excerpt shows the fields that matter; follow the notebook function signature for the executable implementation.

## 14. Return the tool result to the worker

0:26

This participant function controls actual tool dispatch. The runtime supplies bounded file, edit, test and task operations. It records the returned result independently. An unknown action must raise an error rather than invoke arbitrary code.

## 15. Run one worker before adding a team

0:30

Allow participants to read a diff before accepting anything. The tool event and test output must be saved even when the worker fails. A recorded failure is an optional teaching example, not a required live outcome.

## 16. A trace should answer what changed and why

0:40

Open the participant’s real trace rather than a made-up dashboard image. Each model request, tool action, failed check and handoff should be attributable to a worker and build. Trace export can be retried without rerunning the model.

## 17. Inspect the worker’s test in Agent Lens

0:43

Open the actual conversation link. The record proves that the presentation worker read and edited a file and ran a passing component check. It does not prove the whole app works. The sibling query worker exhausted its output budget in this rehearsal; preserve that failed attempt. Do not turn one passing span into a completed product claim.

## 18. Choose work that can happen independently

0:45

The workers own query.py and presentation.py. The query returns the agreed departure records. The display consumes that interface. Use the actual notebook contract to see exactly which fields are required. Click to expose the join, then the whole-product check.

## 19. Ready means its prerequisites passed

0:50

Completed means accepted completion with saved output, not a worker’s progress narration. The local check should reject a task with an unmet dependency. The precise notebook record fields may include richer status metadata; preserve those contracts.

## 20. Make dependencies control the workers

0:55

Do not solve the race with a prompt asking agents to be careful. Claiming must be atomic in the shared task store. Let two local attempts contend for one task in the free exercise.

## 21. Separate working copies protect unfinished changes

1:08

This is a practical reason for independent workspaces, not a guarantee that the generated code is safe. Reviewed local code runs with bounded tools and time limits. Remote Sandboxes remain optional and require their own access.

## 22. Run the ready tasks with two workers

1:10

Keep the concurrency at two for the core exercise. More workers is an optional later experiment. Do not change model or total budget between comparisons and then attribute a difference only to coordination.

## 23. Read the timeline as work and waiting

1:25

Ask which task is on the critical path. Parallel work can reduce elapsed time while increasing aggregate model cost. Queue time, execution time and integration time belong in separate fields.

## 24. Save the checkpoint before the break

1:45

Break runs from 1:45 to 1:55. Integration begins when participants return. Confirm durable local saving. If publication is pending, the work is still complete locally. Reopening or navigating must not start inference.

## 25. Review a patch before it enters the product

1:55

The user explicitly approved human review of task contracts and patches. Keep the actual diff visible next to its test output. Do not represent a review decision as an executed version until integration really runs.

## 26. Test the combined departures board

2:00

Show the combined source identity and acceptance output. If integration fails, preserve it and diagnose the failure before another edit. The facilitator can use the recorded controlled example if the live patches happen to work.

## 27. An integration error can cross a correct boundary

2:12

Do not claim the current agents made this error unless its execution record shows it. This example explains why tests at component boundaries matter. The repair may be to code, task contract, tests or a combination.

## 28. Shared memory needs something worth sharing

2:25

Connect memory to a specific integration incident or verified behavior. Transcripts record what happened. A lesson is an interpretation intended to help a future task.

## 29. Check the lesson before another agent relies on it

2:28

Click to reveal approved memory, then the fresh worker using it. A lesson can describe a successful pattern as well as a failure. Keep claims and verified observations distinct.

## 30. Write a rule with a test attached

2:32

Do not present this as a measured memory success. Explain scope: a rule about schedule times does not mean every display field should print hour 25. Keep the contract version, source evidence and review state visible.

## 31. Save a lesson supported by an execution

2:36

Participants must inspect the evidence rather than approve an agent summary blindly. The retrieval function affects the later actual worker request. A directory listing is not proof that a worker read a lesson.

## 32. Inspect the memory read, then its effect

2:44

This is the trace-to-behavior chain. A citation or read event establishes consultation, not that the memory caused an improvement. The matched follow-up comparison is what tests that question.

## 33. Find the last direct train between two stops

2:50

The follow-up asks for the last direct train between two retained stations, including arrival after midnight, a no-direct-service result and an itinerary download. Each branch uses two workers. Both branches execute; no prerecorded result is substituted for one side. This small paired example teaches the method. One pair cannot establish repeatability or general superiority.

## 34. Run both versions of the follow-up feature

2:55

Keep memory fixed during this matched comparison. Do not edit it after seeing the no-memory result and call the pair controlled. If budget or infrastructure prevents a branch from finishing, retain a missing result and label the pair incomplete.

## 35. The factory has two kinds of state

3:15

This is the distinction between a task ledger and learning. Neither requires sharing a giant conversation among all workers. Both need durable records, clear identities and bounded retrieval.

## 36. Evaluate the product and the process separately

3:25

Avoid a composite score that conceals these tradeoffs. The saved product rows are matched across versions. Missing builds or evaluations remain missing, not silently dropped or converted to ordinary task failures.

## 37. A scenario is an input and an expected behavior

3:27

This is a compact teaching excerpt, not the complete final acceptance scorer. Explain why sorting the identifiers before comparing would hide an ordering defect. Failed execution is not equivalent to a valid empty departure list.

## 38. Compare the frozen builds on matching cases

3:30

Final grading happens after the build choices freeze. Evaluation Tables Preview uses the working Weave-backed publication path. If publication fails, inspect the notebook rows and retry publication only; do not rerun model work.

## 39. Read one comparison row before the average

3:34

Use one scenario to explain the matching inputs, actual outputs and pass criteria before opening the native comparison on the next slide. Keep its source URL and recorded rehearsal identity visible.

## 40. Compare the same departures in Forge

3:35

Actual native Evaluation Tables Preview, verified in a signed-out browser. The saved workspace contains two frozen first-release builds and ten matching scenarios, with all twenty underlying evaluation rows read back. This image does not represent the R4 memory followups, which were incomplete. Open a prediction cell and inspect the service date before treating a matching average as sufficient evidence.

## 41. The faster build missed two final cases

3:37

These are final native scores from R5, a separate engineering rehearsal after context compaction changed. All 56 scenario rows are represented. The first builds passed five public development checks each, but the two-worker final product passed only eight of ten reserved scenarios. Do not treat the earlier R4 native screenshot as this R5 comparison. Builder elapsed excludes human review and integration. Actual provider request counts were 8, 12, 5 and 5 respectively. The no-memory query reached its input bound after writing; the memory query exhausted its output allowance. Both stopped before query tests; presentation was retained unchanged. The lesson proposal cost an additional $0.00143474. Total observed inference was $0.06635800 across 31 provider requests, with zero unknown usage. This single pair cannot establish a general speed or memory effect.

## 42. A timezone assumption selected the wrong train

3:38

The failed cases were departures/utc-input and integrated/departures/utc-input. The two-worker query anchored GTFS service-day midnight to the caller’s timezone. It selected a service-clock 23:03 trip rather than the expected 18:03 Eastern departure after a 23:00 UTC request. The solo query preserved the fixed feed timezone for this historical subset. These are two checks of one defect, not two independent bugs. Both failed follow-up query edits left this earlier bug in place. Ask participants which contract or test they would add before another build.

## 43. More workers can still produce more waiting

3:40

Primary sources: Claude Code agent-team docs, Google Research scaling-agent-systems study and Anthropic compiler report. Do not import their performance numbers as a forecast for this model or task.

## 44. Choose a release using the saved checks

3:45

The release is a versioned workshop artifact, not an automatic public service deployment. Agent-generated recommendations do not bypass required checks. Preserve previous versions for reproduction and rollback.

## 45. Publish the version you can reproduce

3:47

Use the final fifteen minutes for reproduction, the release decision and a short explanation. If a failed build is the only result, the correct output is a blocked release with evidence. That still completes the learning exercise.

## 46. Explain one result to another participant

3:53

Give participants two minutes each. The person explaining should control the notebook and open the relevant record. The facilitator should not take the keyboard or supply the conclusion.

## 47. Take the coordination code to your own project

3:58

Ask each person for one suitable feature, one prerequisite, one acceptance check and one durable project rule from their own team. ARIA is outside the measured comparison and may require additional access.

## 48. Worked answer: select ready tasks



Use the exact notebook task schema. This answer explains the readiness rule; the claim transaction belongs to the supplied store interface. A separate read followed by an unlocked write allows two workers to claim the same task.

## 49. Worked answer: retrieve a checked lesson



Preserve the notebook schema and evidence validation. An approved lesson still has a scope. If the interface changed, retrieve the current rule or ask for review instead of trusting a stale note.

## 50. Worked answer: block an unverified release



This teaching excerpt deliberately blocks missing results and empty check lists. Use the executable notebook record shape for the real decision. A valid release requires the code and checks to refer to the same frozen build.

## 51. Sources for the workflow



These are references for patterns, not required workshop installations. The notebook keeps its coordinator visible in Python and uses the existing Forge Workshop Kit. Software factory has several definitions; use the implemented workshop definition.

## 52. Sources for the data and evaluation



The downloaded dataset manifest is authoritative for archive date, checksums, selected rows and licensing. Do not substitute current live schedule data during a comparison. The software-factory teaching experiment is not a transit reliability benchmark.
