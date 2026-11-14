## 1. Monitor an airline service agent and build better evaluations

0:00

Set the situation before introducing products. Participants operate a simulated airline customer-service agent. They will distinguish a request completing, a booking being correct, and a monitor detecting a problem. Those are three separate observations.

## 2. The passenger wants a different outward flight

0:03

Open airline-discovery-02 in the notebook. The reservation is from upstream source task 7. The workshop adapted its request to exercise a bounded segment change. Ask what must change and what must remain untouched.

## 3. A correct change preserves the return flight

0:06

The requested change is HAT007 to HAT061. HAT174 stays. The agent must also check the fare difference and obtain confirmation. The picture describes the intended booking, not an observed live result.

## 4. The API replaces the complete flight list

0:09

A successful write says the replacement was accepted. It does not establish that the proposed replacement respected the passenger’s request. Read the upstream implementation and the workshop adapter together.

Visual sequence: Trace HAT174 through both candidate API inputs. The assignment replaces the list, so the missing-return branch cannot preserve a flight it did not receive. This is an illustrative failure mechanism; the live qualification handled its bookings correctly.

## 5. A successful write can leave the wrong booking

0:12

This is an illustrative failure mechanism, not a claim that the live agent will make it. The deterministic local exercise reproduces this list-replacement defect. Live outcomes remain unedited.

## 6. The data contains bookings, policy, and passenger requests

0:15

Open the provenance file. Explain which records came from upstream and which scripted passenger behavior or local exercise was added for teaching. Do not describe this as a production airline deployment.

## 7. Keep related bookings in the same data group

0:18

These are the approved execution counts, totalling 40 conversations. Development and final comparisons run the same requests once on each version. Upstream task identities overlap, so splitting task rows alone would leak related bookings.

Visual sequence: Start with the family bracket, not the batch counts. The connected dots stand for related records, not three named passengers. Reveal the assigned groups, then show why putting a related task in final evaluation leaks the family across partitions. The counts are the actual frozen plan.

## 8. Your copy owns the runs and saved work

0:21

Open the hosted template and show copying into the participant’s project. Confirm the detected destination before publishing a trace. Opening, browsing, or checking code does not run a model. An unavailable native service is separate from an agent task failure. Server-side tag costs cannot be stopped by the notebook’s local allowance.

## 9. Check access and inspect the starting itinerary

0:25

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 10. Record a conversation around the passenger’s request

0:29

A conversation may contain several turns. Do not collapse unrelated requests into a single conversation. The passenger’s clarification and confirmation belong with the relevant turn evidence. Use native session and span identities from execution.

Visual sequence: Read the parent tree alongside operation order. Both model calls and both tool attempts remain children of their turn. Bar width is schematic, not measured latency. Ask participants which event needs the error and which needs the returned reservation; then map them to my_model_span and my_tool_span.

## 11. The tracing code records the actual tool result

0:33

Name the actual function to edit. The SDK uses the recorded timestamps, not the time an export retry happens. Preserve the saved event if trace publication fails; retry only the export.

## 12. Connect each model request to its response

0:35

Open the editable my_model_span function beside this table. Participants supply these actual fields to tracing.LLM. Tool spans and model spans answer different questions; neither replaces the independent booking check.

## 13. Instrument the agent before sending its first batch

0:39

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 14. Read the booking returned by the tool

0:48

Give everyone several minutes on one conversation. Ask them to point to the actual return flight rather than merely an exception field. If the agent was correct, record that success and continue with the labeled calibration drill for the diagnostic exercise.

Visual sequence: Follow one chosen action through arguments, the state write, the observation, and the next request. The returned booking must be appended before the next model call. Ask participants to locate that exact observation in Agent Lens; the final reply alone cannot prove what the model received.

## 15. The reservation read timed out before any change

0:51

Find the request, full replacement list, returned booking, and final response. Do not infer task success from the tool returning normally. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 16. Follow the agent after the error

0:56

Read the failed tool operation, the next model request, and the subsequent tool result. Then verify the complete booking. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 17. Keep three questions separate

0:58

Use the same example across all three questions. A lower tool-error rate does not prove higher booking quality. A high tag count may mean more failures, broader criteria, or a different processing denominator.

## 18. Use Overview for context, then open Conversations

1:05

The verified version filter is in Conversations. The native Agent Version dropdown was empty during rehearsal; use the recorded custom airline.version attribute. Overview remains project context, not a claim that the saved conversation filter applies to every chart. A saved view is a query, not a snapshot of an evaluation dataset.

## 19. Insights suggests a pattern worth investigating

1:14

A prepared cluster must contain real executions and a completed native clustering run. The current release must report whether that prerequisite was met. A deterministic notebook summary is not Agent Lens Insights. If native access is unavailable, identify the limitation and use only a labeled saved capture.

## 20. An error is not always an unresolved failure

1:26

Review behavior through its outcome. Do not label an appropriate refusal as a failure just because the passenger did not get their first request. The airline policy and allowed request matter.

## 21. Save one claim with the turn that supports it

1:32

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 22. Break until 1:50

1:40

Ten-minute break. Keep the fixed batches and state; do not restart discovery to generate a more convenient failure.

## 23. Define a behavior that a reviewer can check

1:50

The initial proposed criterion is intentionally a starting hypothesis for alignment, not a validated native rule. Participants must review what evidence exists in each turn. Requests may authorize replacing the entire itinerary.

## 24. Fewer flights can be the correct result

1:55

This is the central counterexample to a naive flight-count rule. Ask the room whether changing three segments to two is sufficient evidence of failure. It is not.

Visual sequence: The connecting point disappears while the origin, destination, and return remain. Ask whether fewer segments is a failure before revealing the approved nonstop. The answer depends on the request, not the count. These segment names and airport positions are illustrative.

## 25. Add counterexamples before trusting the rule

2:00

Use actual reviewed turns when available. The calibration pack is a labeled teaching fallback, not a claim about the learner’s live failure rate. Keep all disagreements and their reasons.

## 26. A native tag has criteria, labels, and a live state

2:05

Walk through native Tags and Alignment. Creating or editing a notebook rubric is not the same action as saving native tag criteria. Use the native identities in the readback record.

Visual sequence: Keep the right-hand saved criterion in place while the Alignment draft is tested. Only the final explicit-save arrow changes live criteria. A failed Alignment test produces no judgment; it does not silently disable, update, or validate the saved live rule.

## 27. Save the criteria and check the tag’s scope

2:08

Read the saved criteria, Apply with AI setting, and exact workshop-agent scope. This recorded tag ID is not a participant default. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 28. Turn context limits what the judge can know

2:10

Native judges see turn-level evidence. Do not assume every model span contains the entire conversation. The context inspection is part of the exercise; a fluent judge reason does not create missing evidence.

Visual sequence: The selected turn has a write and a reply but lacks the earlier booking. Ask which evidence establishes a return was removed. In this illustrated context it is unavailable. A reviewer with the full conversation knows more than the turn-level judge; keep that context difference in the review record.

## 29. Test your tag against reviewed turns

2:15

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 30. Test one reviewed turn in native Alignment

2:20

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 31. A saved review is not a completed judge result

2:22

Inspect the saved review and the test status. A failed native test has no prediction to compare; do not turn it into a negative label. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 32. A valid response can contain a wrong judgment

2:29

This is a local structured-response exercise for the explanation judge, separate from the native tag’s server-side implementation. A string false is not a boolean false. Preserve unavailable judgments rather than replace them with false.

## 33. Measure the monitor on reviewed cases

2:35

Walk through one cell at a time. The human review is the reference for this calculation; disagreement remains open to correction. Unavailable judgments are excluded from these eight processed rows and reported separately.

Visual sequence: Reveal the true positives, false positive, and remaining cells in place. Human review supplies the reference labels. These eight rows are illustrative arithmetic and not a successful native Alignment result. No unavailable prediction enters this matrix.

## 34. Precision asks whether an alert deserves review

2:39

The denominator is the tagged turns with a reviewed label, not all requests. Alert count cannot tell us how many failures were missed. Ask which example produced the false positive.

Visual sequence: The outlined row is the denominator: all four reviewed alerts. Three are reviewed failures. The faded second row is irrelevant to precision but needed for recall. If there are no alerts, leave precision unavailable. This graphic does not describe native workshop outcomes.

## 35. Recall asks which failures the monitor missed

2:42

Precision and recall happen to match in this arithmetic example, but they use different denominators. Show the missed failure cell. Review sampling affects whether these values estimate the wider traffic population.

Visual sequence: The outlined column is the denominator: all four reviewed failures. One was not alerted. The same 75 percent hides a different question from precision. Review unflagged controls so this missed-failure cell can be populated. The arithmetic remains illustrative.

## 36. Coverage tells us which turns were judged

2:45

A missing tag is not enough to identify a completed negative judgment. Read processing status and identities. Keep pending, failed, insufficient-context, and scored states separate as supported by the recorded events.

Visual sequence: Count the eight completed predictions, then divide by all ten eligible turns. Only after that do we join completed predictions to human reviews for the agreement matrix. The two question marks remain unknown. Positive live assignments by themselves cannot establish this denominator.

## 37. Calculate monitor quality and send new traffic

2:50

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 38. A missing live tag does not establish a negative judgment

3:00

Keep the live assignment view separate from the explicit Alignment-test result set. Do not infer processing coverage from positive assignments alone. Record the denominator and native result source beside any calculated rate.

Visual sequence: All three branches can produce the same absent live tag. Ask what readback distinguishes them. Explicit native test outcomes can establish known positive and negative predictions; a blank assignment cannot. Keep pending, failed, and missing context separate where native records support them.

## 39. Freeze the rule before comparing agent versions

3:02

The native rule needs the same workspace scope for both versions but enough attributes to filter them independently. The local notebook cannot guarantee the native service has completed processing. Show its readback status.

## 40. A reviewed turn becomes a regression case

3:10

Make curation an explicit code exercise. The case contains the original booking, not the already-mutated booking that caused the complaint. Keep the exact request and constraints with it.

Visual sequence: The arrow into the regression case comes from before the write. The crossed arrow from the mutated booking explains a common reconstruction error. Keep the request, policy, approved scope, human review, and source identities with the initial state. This omission incident is a labeled illustration, not an invented live failure.

## 41. Keep enough information to replay the request

3:15

Ask what happens if someone saves only the final reply. They cannot reconstruct the original itinerary or determine what was unrequested. These records are public simulated examples; the same technique with real passengers needs an appropriate privacy review.

## 42. Build a regression case from the reviewed turn

3:22

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 43. Score the change and the preserved flights separately

3:31

The state scorer is deterministic over recorded state. It does not use the agent’s final assertion as proof. A completion score must fail when the requested change is missing, even if the unchanged return is preserved.

## 44. The explanation judge answers a different question

3:36

The explanation judge receives the recorded work needed for its rubric. Human review and deterministic state checks remain distinct evidence. Missing judgments stay unavailable; do not average them as zero or success.

## 45. Add the booking check the old evaluation missed

3:41

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 46. Save the case and its checks with the checkpoint

3:48

Show the checkpoint link produced by the participant’s session. Ask someone to identify the source case, reviewer, and actual function. A named dataset without its initial booking cannot reproduce this incident.

## 47. Break until 4:00

3:50

Ten-minute break. Do not edit final cases or resample cases based on which version looks better.

## 48. Repair the list operation, then compare the behavior

4:00

Revisit the same concrete request. The implementation change builds a complete replacement itinerary from the requested range and untouched prefix and suffix. It does not depend on a flight-count heuristic.

## 49. Replace a range without dropping its neighbors

4:06

The example replaces original[0:2] with one flight and preserves original[2:]. Do not assume every request changes one flight. A full-itinerary change legitimately has start zero and stop len(original).

## 50. Walk through the values before running the model

4:10

This is a free, simplified arithmetic check. It establishes the list transformation, not whether the model selected the correct segment range or received passenger confirmation.

Visual sequence: Point to index two: the half-open replacement stops before return-1. First expose the index range, then the empty prefix, replacement, and untouched suffix. The last line is the participant function’s list operation. Their free check also validates bounds and copies the data.

## 51. Test the repair on matched development bookings

4:15

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 52. The passenger must approve the proposed change

4:24

Confirm that the scripted passenger enforces the source request’s requirements. A correct refusal or request for clarification may be the right outcome. The code repair cannot compensate for an incorrect approval policy.

## 53. Explain a passing repair without overstating it

4:32

Keep deterministic repair results separate from live stochastic outcomes. A live success remains a success. Never replace it with a failure to improve the story.

## 54. Judge one saved explanation against its evidence

4:33

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 55. Freeze code before opening the reserved requests

4:40

Final expected answers do not enter the solver or rubric-tuning contexts. The local source files are inspectable for teaching, so this is a controlled workshop comparison, not a secure blind benchmark.

## 56. Compare six reserved bookings across both versions

4:46

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 57. Read the same request across the two versions

4:54

Teach the alignment before opening EvalTables. Compare the complete booking state; do not substitute a tag result for deterministic correctness. Match source IDs and execution fingerprints.

Visual sequence: The same case forks into two isolated initial bookings. Each uses its own recorded source and trace. The dashed link means aligned comparison, not shared mutable state or a handoff. Keep booking-state checks, explanation judgments, and monitor outcomes in separate fields.

## 58. Set the starting agent as the comparison reference

4:59

Choose an identical case in the two versions. Read the state scores, output booking, judgment status, and trace links. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 59. Read both outputs for the same request

5:02

Identify the shared input and the separate predictions. Open the underlying booking and native trace before explaining a passing score. Capture identity and original are recorded in data/native-captures.json. This is recorded evidence, not the participant’s live result.

## 60. The recorded agent comparison was a tie

5:05

Preserve the successful baseline. Do not describe the helper as improving task quality on this rehearsal. The controlled drill is a real code repair, but it is not a spontaneous agent failure. These small simulated batches do not estimate production reliability.

Visual sequence: Reveal the starting row first, then the repair row. All six case outcomes match; there is no passing case unique to the repair. Both versions also pass four subsequent requests. Native monitoring accuracy is unavailable. The local omission drill demonstrates a repair independently of this observed tie.

## 61. Report denominators and unresolved work

5:08

A six-case comparison has limited reach. Show each failure and avoid a general claim that monitoring improves all agents. If all cases tie, inspect whether behavior or cost changed while correctness stayed equal.

## 62. Use later traffic to check the frozen monitor

5:20

The subsequent batch is separate from the six final requests. Do not tune the monitor after seeing one version’s outcomes. Read the differences between state outcomes and tag classifications.

## 63. Check what the monitor catches after the repair

5:26

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 64. A falling alert count has several explanations

5:37

Ask participants to rule out each explanation with the records. A workshop that simply celebrates a downward chart has skipped the measurement problem it was meant to teach.

## 65. Write down what changed and whether it helped

5:45

The participant conclusion should cite one actual case and its exact code, booking, trace, and evaluation. Improvements are welcome; a documented tie or regression also completes the lesson.

## 66. Publish the comparison and stop automatic judging

5:50

Give participants time to make the change themselves. Have one person point to the input, the changed line, and the observed output. Opening or checking a function sends no model request. Follow the named run control only after the free check passes.

## 67. The next release has a check the first release lacked

5:58

End by asking someone to reproduce a case from its saved initial state. Do not conclude with a promise of autonomous improvement. Monitoring, human review, and offline evaluation each answered a different question.

## 68. Worked answer: validate a judge response

Reference

This is the notebook’s actual validator. It checks shape and types, not the truth of the judgment.

## 69. Worked answer: keep unknown judgments out of the matrix

Reference

This is the notebook’s actual my_monitor implementation. Review unflagged cases too; an alerts-only sample cannot establish recall across traffic.

## 70. Worked answer: preserve the original case inputs

Reference

Use the actual case_from_reviewed_turn signature in the notebook. Do not synthesize a nonexistent native turn or treat a listing of spans as proof that a specific diagnostic was read.

## 71. Worked answer: check both change and preservation

Reference

Illustrative list-based scorer excerpt. The actual evaluator must use the recorded approved scope and final state, not values inferred from the agent’s final response.

## 72. Worked answer: build the complete replacement list

Reference

This is the notebook’s actual itinerary builder. The deep copy prevents the result from mutating the original booking. The agent must still select the correct range and obtain confirmation.

## 73. Sources and saved evidence

Reference

Consult the release evidence for actual validation coverage. External-account access and human rehearsal are not established by a successful deck build.
