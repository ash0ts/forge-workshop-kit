## 1. Build a transit app with a team of coding agents

0:00

The department and deadline are fictional. The schedule records are real public MBTA data. Participants build a bounded software factory; we do not claim to reproduce an unattended production engineering organization. The single session includes three breaks. The extra time is for tracing one concrete input through the implementation, writing the coordinator and explaining the recorded failures.

## 2. Your team needs a departures board

0:02

Start with the person using the software. Ask what could make a plausible-looking board wrong. Listen for wrong date, wrong stop, missing departures and misleading times. No model or agent count appears before the product is clear.

## 3. Here is the application we want to deliver

0:05

This is a real capture of the reference implementation, not a model outcome. Participants will inspect the app their workers actually produce. Call out the selected Park Street platform, midnight on November 29, and first scheduled departure at 00:08. The next slides explain why that train belongs to November 28 service.

## 4. The inputs are public transit records

0:08

Open the notebook data receipt and read its archive date and checksum. Do not describe the small teaching subset as the complete MBTA system. MBTA describes its feed at https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md .

## 5. Start with the row for the platform

0:10

Keep the same trip visible through the next three slides. Read the actual identifiers aloud once. The product uses these joins, not an LLM guess about the next train. Ask which table must tell us whether this trip runs on Thanksgiving. Timeline spacing is illustrative; timestamps are actual.

## 6. Join the trip to its service calendar

0:13

The service ID is a join key. The active dates come from the calendar and exception records. Explain that calendar_dates overrides the weekly rule. This is a historical snapshot and fixed test date, not today’s schedule.

## 7. Keep the service date and boarding date

0:15

Ask the room to name the two different dates before revealing the timestamp. The train is eight minutes after the next midnight. Explain why hour modulo 24 without carrying the day loses information.

## 8. The last train can belong to yesterday’s service

0:17

This is an actual retained row: trip 63926435, stop 70076, departure_time 24:08:00, stop_sequence 150, ThanksgivingDay service, headsign Alewife. The civil timestamp is 2024-11-29T00:08:00-05:00. Ask what a parser restricted to 0..23 hours would do. The rule must survive between components.

## 9. Convert elapsed service time into a timestamp

0:20

Explain the datetime origin, timezone and timedelta separately. This example has no daylight-saving transition; it does not replace the full GTFS time specification. The learners write the acceptance check, while the coding worker implements the general query.

## 10. Check the joined behavior, not just the parser

0:23

These deliberate mutations test the participant’s assertion. They are local examples, not recorded agent mistakes. Explain why a checker that always returns True would pass the first example and fail to teach anything.

## 11. Turn the brief into checks

0:24

These are requirements for our product, not a claim that the initial code fails them. Show the concrete acceptance inputs and expected outputs in the notebook. Final cases stay outside the coding-worker context until the versions are frozen.

## 12. A software factory needs a way to finish work

0:26

Software factory is a broad term. This slide states the operational meaning we implement. It includes specification, coordination, verification and release. It is not simply a chat room with several role prompts.

## 13. Add the task board and two workers

0:28

Click once to reveal workers, once to reveal integration, once to reveal the checked lesson. Solid arrows show code or execution flow. The dashed arrow identifies reviewed evidence. The diagram is explanatory, not a recorded run.

## 14. Two workers means two contexts around the same model

0:29

The worker is a Python loop plus model requests and allowed tools. Two workers do not mean training two new models. Model settings match across the sequential and parallel builds. The comparison asks what the coordination design changes for this task.

## 15. Your project contains the experiment

0:30

Keep the distinction between agents sharing project records and attendees sharing credentials. The latter does not happen. The notebook has an adjustable inference allowance; notebook compute is billed separately. Opening the notebook does not start agents.

## 16. Connect and inspect the source data

0:33

Do not ask participants to paste a key into a code cell. Hosted authentication comes from their own account. Locally use wandb login. Access checks should distinguish a writable project from inference entitlement. The workshop list in the README links to the current native Transit template. If copying is unavailable, use its notebook source/import fallback; do not send attendees to the reference app.

## 17. Record the operation that you just ran

0:38

Identify the name, inputs, actual result and time boundaries. Participants add or edit the attribute in the full notebook function and find it in their own setup span. This operation reads the teaching dataset, so it does not spend inference allowance.

## 18. Write the after-midnight acceptance check

0:42

The scenario is written by the participant and later runs on the integrated app. It is public development evidence, not a hidden final answer. Show how a plausible train list can still use the wrong service day.

## 19. One worker still needs a complete loop

0:50

Start with the familiar single-agent harness. Multiple agents do not remove the need for correct tool observation handling, explicit stopping and independent checks. Model settings stay fixed in the comparisons.

## 20. Give the worker the task it is allowed to solve

0:53

Explain each input before editing: task is the approved contract, sources are the current worker copy, lessons are explicitly retrieved project memory. This excerpt shows the fields that matter; follow the notebook function signature for the executable implementation.

## 21. The first action reads the assigned file

0:56

This is an explanatory sequence using the implemented tool contract, not an additional live execution. Keep model, Python tool and observation separate. A model choosing read_file is not the same thing as Python executing it.

## 22. The edit includes the version it was based on

0:59

Explain optimistic conflict detection: before_sha256 identifies the old file, while the returned hash identifies the new one. A rejected write should produce an observation that the next request can inspect.

## 23. Run the checks against the changed files

1:02

The board clears the old test receipt when a file changes. The current files are what run in a child Python process. That process has restricted imports, a timeout and no inherited Forge credentials; it is reviewed code execution, not a security sandbox.

## 24. Return the tool result to the worker

1:05

This participant function controls actual tool dispatch. The runtime supplies bounded file, edit, test and task operations. It records the returned result independently. An unknown action must raise an error rather than invoke arbitrary code.

## 25. Append the actual observation to the next request

1:07

The agent action has already been appended as an assistant message. The following user message supplies the observation, any directed messages and remaining action count. The runtime records actual tool execution independently of the learner’s return value. Do not add a second model call here.

## 26. Finish submits a patch for review

1:09

Point out the status change to review. Human review and integration remain separate. If a worker reaches its action limit without this tested completion, the unfinished file is retained as evidence, not silently merged.

## 27. Run one worker before adding a team

1:13

Allow participants to read a diff before accepting anything. The tool event and test output must be saved even when the worker fails. A recorded failure is an optional teaching example, not a required live outcome.

## 28. A trace should answer what changed and why

1:23

Open the participant’s real trace rather than a made-up dashboard image. Each model request, tool action, failed check and handoff should be attributable to a worker and build. Trace export can be retried without rerunning the model.

## 29. Inspect the worker’s test in Agent Lens

1:27

Open the actual conversation link. The record proves that the presentation worker read and edited a file and ran a passing component check. It does not prove the whole app works. The sibling query worker exhausted its output budget in this rehearsal; preserve that failed attempt. Do not turn one passing span into a completed product claim.

## 30. The request has a size limit even when files are saved

1:31

Explain why storing a complete file is different from resending it with every action. R5 still hit a bound after a long write, so this policy is not a guarantee that any generated module will fit. Do not imply that a higher output allowance fixes an oversized input.

## 31. Break until 1:45

1:35

Ten-minute break, 1:35–1:45. Use the read-only monitor to find participants who requested help. Do not treat missing progress as failure.

## 32. Choose work that can happen independently

1:45

The workers own query.py and presentation.py. The query returns the agreed departure records. The display consumes that interface. Use the actual notebook contract to see exactly which fields are required. Click to expose the join, then the whole-product check.

## 33. Ready means its prerequisites passed

1:50

Completed means accepted completion with saved output, not a worker’s progress narration. The local check should reject a task with an unmet dependency. The precise notebook record fields may include richer status metadata; preserve those contracts.

## 34. Both workers can see a pending task

1:53

Use the local two-thread fixture, not a theoretical timing claim. Ask learners what changes if both read at the same time. A polite prompt does not make two Python operations atomic.

## 35. A separate check and write permits two owners

1:56

The controlled race uses a barrier to reproduce the condition. This two-owner outcome measures coordination code, not model intelligence. Show the broken if-pending then set-owner snippet in the notebook.

## 36. One short transaction assigns one owner

2:00

The same two local threads now have one successful claim. The other gets a not-ready or already-claimed error. Holding the lock for the entire model call would serialize the work and block other claims.

## 37. Keep the model call outside the claim transaction

2:03

This is simplified teaching code; the actual store raises FactoryStop and also records dispatch identity, source and timing. Do not instruct participants to replace the store with this excerpt. The required code change is claim_task in the notebook.

## 38. Make dependencies control the workers

2:05

Do not solve the race with a prompt asking agents to be careful. Claiming must be atomic in the shared task store. Let two local attempts contend for one task in the free exercise.

## 39. Separate working copies protect unfinished changes

2:15

This is a practical reason for independent workspaces, not a guarantee that the generated code is safe. Reviewed local code runs with bounded tools and time limits. Remote Sandboxes remain optional and require their own access.

## 40. Each worker starts from the same source

2:16

Separate working files do not imply separate authority to change every file. Keep the common starting version visible. This is diagrammatic code flow, not a claim that all future tasks are independent.

## 41. Each task can edit only its assigned module

2:19

Point out which files are readable and which are editable. Both task contracts name the same return schema. The worker cannot repair a failing test by changing the evaluator.

## 42. Integration checks the patches against their base

2:22

Explain why different files still need a combined test: both modules can disagree about a field or timezone. The hash guards against stale file replacement; it does not prove the interface is correct.

## 43. Run the ready tasks with two workers

2:25

Keep the concurrency at two for the core exercise. More workers is an optional later experiment. Do not change model or total budget between comparisons and then attribute a difference only to coordination.

## 44. Read the timeline as work and waiting

2:35

Ask which task is on the critical path. Parallel work can reduce elapsed time while increasing aggregate model cost. Queue time, execution time and integration time belong in separate fields.

## 45. Find both submitted patches before integration

2:40

This is a checkpoint at 2:40, not a break. Integration starts at 2:45. If one worker is unfinished, keep that outcome and inspect the available record rather than inventing a completed patch.

## 46. Review a patch before it enters the product

2:42

The user explicitly approved human review of task contracts and patches. Keep the actual diff visible next to its test output. Do not represent a review decision as an executed version until integration really runs.

## 47. Test the combined departures board

2:45

Show the combined source identity and acceptance output. If integration fails, preserve it and diagnose the failure before another edit. The facilitator can use the recorded controlled example if the live patches happen to work.

## 48. An integration error can cross a correct boundary

2:53

Do not claim the current agents made this error unless its execution record shows it. This example explains why tests at component boundaries matter. The repair may be to code, task contract, tests or a combination.

## 49. Use the local preview to follow a returned row

2:56

If a live build is wrong, keep the output visible and name the failed requirement. The prepared reference continuation appears only if neither initial build passes development integration; it is labeled and never replaces live results.

## 50. Break until 3:20

3:00

Twenty-minute break, 3:00–3:20. Resume the same project. Do not change source or model settings to make the live result match the prepared example.

## 51. Shared memory needs something worth sharing

3:20

Connect memory to a specific integration incident or verified behavior. Transcripts record what happened. A lesson is an interpretation intended to help a future task.

## 52. Check the lesson before another agent relies on it

3:23

Click to reveal approved memory, then the fresh worker using it. A lesson can describe a successful pattern as well as a failure. Keep claims and verified observations distinct.

## 53. Write a rule with a test attached

3:26

Do not present this as a measured memory success. Explain scope: a rule about schedule times does not mean every display field should print hour 25. Keep the contract version, source evidence and review state visible.

## 54. A saved note is not automatically accepted

3:29

The examples are illustrative records matching the retrieval schema, not four observations from R5. Ask which one a fresh worker should receive and which fields justify that choice.

## 55. First exclude the unchecked interpretation

3:31

The agent can propose a lesson. The participant checks its evidence and writes the accepted rule. This gate reduces propagation of guesses; it cannot guarantee the rule is correct in every context.

## 56. Then check the applicable contract version

3:33

Do not compare source_revision to the current code fingerprint. A lesson may be relevant to new code while citing an earlier version. The accepted contract version is the applicability check.

## 57. Finally match the task’s scope and tags

3:35

select_memories performs these checks. No vector database is needed for this small project record. Let a participant explain why status alone would retrieve too much.

## 58. Save a lesson supported by an execution

3:40

Participants must inspect the evidence rather than approve an agent summary blindly. The retrieval function affects the later actual worker request. A directory listing is not proof that a worker read a lesson.

## 59. Inspect the memory read, then its effect

3:50

This is the trace-to-behavior chain. A citation or read event establishes consultation, not that the memory caused an improvement. The matched follow-up comparison is what tests that question.

## 60. Find the last direct train between two stops

4:00

The follow-up asks for the last direct train between two retained stations, including arrival after midnight, a no-direct-service result and an itinerary download. Each branch uses two workers. Both branches execute; no prerecorded result is substituted for one side. This small paired example teaches the method. One pair cannot establish repeatability or general superiority.

## 61. Start both follow-ups from the same release

4:02

Each build has two workers. The coordinator invokes the two builds in order, while each build may run its two workers concurrently. Do not describe the two conditions as synchronized or simultaneous. Compare saved initial fingerprints.

## 62. Keep both sets of patches and checks

4:05

The specification, starting code, fixed research model, limits and tool implementation are held the same. The lesson cannot be edited after inspecting the first outcome and still count as a matched pair.

## 63. The follow-up returns a journey, not a list of guesses

4:07

Explain the function inputs and two valid output shapes. The retained dataset is small, so None concerns this schedule subset. It is not a statement that no real-world route exists. The renderer cannot invent a trip when the query returns None.

## 64. Run both versions of the follow-up feature

4:10

Keep memory fixed during this matched comparison. Do not edit it after seeing the no-memory result and call the pair controlled. If budget or infrastructure prevents a branch from finishing, retain a missing result and label the pair incomplete.

## 65. The factory has two kinds of state

4:27

This is the distinction between a task ledger and learning. Neither requires sharing a giant conversation among all workers. Both need durable records, clear identities and bounded retrieval.

## 66. Find where the lesson entered the request

4:32

If no explicit read_memory action is present, distinguish the initial read_shared_memory selection from an agent-initiated read. Do not claim peer messaging unless the saved events contain it. The R5 workers were coordinated through task records and supplied lessons.

## 67. Keep a stopped worker’s files and error

4:38

Use Recover stopped work only after confirming the earlier execution stopped. A request with an uncertain outcome remains conservatively charged. A bound error is not fixed merely by clicking again. The six-hour schedule includes time to interpret an incomplete build, not unlimited retries.

## 68. Break until 4:55

4:45

Ten-minute break, 4:45–4:55. Stop adding features. The final comparison must include failed or incomplete branches.

## 69. Evaluate the product and the process separately

4:55

Avoid a composite score that conceals these tradeoffs. The saved product rows are matched across versions. Missing builds or evaluations remain missing, not silently dropped or converted to ordinary task failures. Repeated task claims include explicit recovery; overlapping reasoning and semantically duplicated code are not measured. Coverage is separate from passed-case rate.

## 70. A scenario is an input and an expected behavior

4:58

This is a compact teaching excerpt, not the complete final acceptance scorer. Explain why sorting the identifiers before comparing would hide an ordering defect. Failed execution is not equivalent to a valid empty departure list.

## 71. Compare the frozen builds on matching cases

5:03

Final grading happens after the build choices freeze. Evaluation Tables Preview uses the working Weave-backed publication path. If publication fails, inspect the notebook rows and retry publication only; do not rerun model work.

## 72. Read one comparison row before the average

5:08

Use one scenario to explain the matching inputs, actual outputs and pass criteria before opening the native comparison on the next slide. Keep its source URL and recorded rehearsal identity visible.

## 73. Compare the same departures in Forge

5:10

Actual native Evaluation Tables Preview, verified in a signed-out browser. The saved workspace contains two frozen first-release builds and ten matching scenarios, with all twenty underlying evaluation rows read back. This image does not represent the R4 memory followups, which were incomplete. Open a prediction cell and inspect the service date before treating a matching average as sufficient evidence.

## 74. The faster build missed two final cases

5:13

These are final native scores from R5, a separate engineering rehearsal after context compaction changed. All 56 scenario rows are represented. The first builds passed five public development checks each, but the two-worker final product passed only eight of ten reserved scenarios. Do not treat the earlier R4 native screenshot as this R5 comparison. Builder elapsed excludes human review and integration. Actual provider request counts were 8, 12, 5 and 5 respectively. The no-memory query reached its input bound after writing; the memory query exhausted its output allowance. Both stopped before query tests; presentation was retained unchanged. The lesson proposal cost an additional $0.00143474. Total observed inference was $0.06635800 across 31 provider requests, with zero unknown usage. This single pair cannot establish a general speed or memory effect.

## 75. Open the two failing rows in the final comparison

5:15

Use the actual saved native view. The bottom two rows show the query and integrated application cases. Both select 63919613 in the solo output and 63919759 in the team output. The screenshot is preserved; numbered annotations sit beside the relevant fields. Capture provenance is in notes/r5-capture-receipt.json.

## 76. A timezone assumption selected the wrong train

5:16

The failed cases were departures/utc-input and integrated/departures/utc-input. The two-worker query anchored GTFS service-day midnight to the caller’s timezone. It selected a service-clock 23:03 trip rather than the expected 18:03 Eastern departure after a 23:00 UTC request. The solo query preserved the fixed feed timezone for this historical subset. These are two checks of one defect, not two independent bugs. Both failed follow-up query edits left this earlier bug in place. Ask participants which contract or test they would add before another build.

## 77. Interpret the request as one instant

5:18

Recorded R5 case: departures/utc-input. This is a same-instant conversion. The feed clock defines the origin of GTFS elapsed service time; the caller is allowed to express the request using another offset.

## 78. The team used the caller’s clock for service time

5:20

Recorded behavior, not a hypothesized defect. The team anchored service-day midnight to the request timezone. This changed the chosen record, not only its formatted text. Inspect the source and actual prediction beside the expected row.

## 79. The renderer carried the same wrong trip into the board

5:22

The independent suite checks both the query and the complete application. Avoid describing these correlated cases as two independent coding errors. Learners should propose a public UTC-input regression case for a future experiment, after retaining the current outcome.

## 80. Neither follow-up completed the query change

5:24

Without memory: oversized input after a saved write. With memory: output allowance exhausted before a complete first action. Both query tasks stopped before testing. The existing query remained; these outcomes do not establish that shared memory caused either failure.

## 81. More workers can still produce more waiting

5:25

Primary sources: Claude Code agent-team docs, Google Research scaling-agent-systems study and Anthropic compiler report. Do not import their performance numbers as a forecast for this model or task.

## 82. Choose a release using the saved checks

5:30

The release is a versioned workshop artifact, not an automatic public service deployment. Agent-generated recommendations do not bypass required checks. Preserve previous versions for reproduction and rollback.

## 83. Publish the version you can reproduce

5:35

Use the last half-hour for reproduction, release and a short explanation. R5 supports releasing the one-worker departures board. Failed required checks block the follow-up. The output is an artifact and Report, not automatic production deployment.

## 84. Reload the selected app and repeat one case

5:44

This is a local inference-free reproduction. It shows that the delivered source and data yield the saved behavior. It is not a rerun of the stochastic coding agents. Verify one row, not merely that the app opens.

## 85. Explain one result to another participant

5:48

Give participants two minutes each. The person explaining should control the notebook and open the relevant record. The facilitator should not take the keyboard or supply the conclusion.

## 86. Take the coordination code to your own project

5:58

Ask each person for one suitable feature, one prerequisite, one acceptance check and one durable project rule from their own team. ARIA is outside the measured comparison and may require additional access.

## 87. Worked answer: select ready tasks



Use the exact notebook task schema. This answer explains the readiness rule; the claim transaction belongs to the supplied store interface. A separate read followed by an unlocked write allows two workers to claim the same task.

## 88. Worked answer: retrieve a checked lesson



Preserve the notebook schema and evidence validation. An approved lesson still has a scope. If the interface changed, retrieve the current rule or ask for review instead of trusting a stale note.

## 89. Worked answer: block an unverified release



This teaching excerpt deliberately blocks missing results and empty check lists. Use the executable notebook record shape for the real decision. A valid release requires the code and checks to refer to the same frozen build.

## 90. Sources for the workflow



These are references for patterns, not required workshop installations. The notebook keeps its coordinator visible in Python and uses the existing Forge Workshop Kit. Software factory has several definitions; use the implemented workshop definition.

## 91. Sources for the data and evaluation



The downloaded dataset manifest is authoritative for archive date, checksums, selected rows and licensing. Do not substitute current live schedule data during a comparison. The software-factory teaching experiment is not a transit reliability benchmark.

## 92. Worked answer: check the after-midnight departure



Reveal only after an attempt or requested hint. This checks one public scenario; it does not replace the independent final scorer.

## 93. Worked answer: dispatch one allowed tool



Read action["action"], select the provided callable, invoke it exactly once and return the observation unchanged. The free check rejects an unavailable shell action.

## 94. Worked answer: check the departure order



This participant development check tests exact ordered trip IDs. The independent final scorer also checks the other required fields. A missing judgment is not False.
