# Airline monitoring workshop

Six hours for participants who can read basic Python. Each person copies the notebook into a writable Forge project and uses their own credentials. The facilitator reads progress; there is no gateway.

Participants investigate a simulated airline service agent, review a native monitoring rule, and turn an observed booking mistake into a regression case. They then compare a repair on matched requests and inspect how the same monitor behaves afterward.

The source is the airline domain from [τ-bench revision `989d3285`](https://github.com/sierra-research/tau2-bench/tree/989d3285ae669e49503324bdb9981bf14fccedeb), distributed under MIT. These are simulated bookings and benchmark requests. This workshop adapts the environment; it does not reproduce a benchmark score.

## Current qualification status

This is a technical preview. The maintainer rehearsal created a scoped native tag and saved native examples and human labels. Six native Alignment tests returned HTTP 500, and the prepared Insights project has no completed clustering run. Do not present either exercise as qualified for attendees. Local code checks, saved conversations, and review arithmetic remain usable; a successful native-feature check and participant rehearsal are still required.

The live qualification completed all 40 conversations with passing task checks. Both versions passed 6/6 final requests and 4/4 subsequent requests. Preserve this tie. The deterministic missing-return drill demonstrates the code repair separately; it is not a recorded spontaneous agent failure. Native monitor precision and recall remain unavailable.

## Before the session

- Open the [hosted participant template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU5MzU=/view) and copy it into your project. The [Workshop Kit hub](https://ash0ts.github.io/forge-workshop-kit/) links the deck and [source/laptop setup](https://github.com/ash0ts/forge-workshop-kit). Use the release's validation record to check which access and rehearsal checks passed.
- Rehearse copying into a participant-owned project. Check trace publication, native Tags and Alignment access, evaluation publication, and the prepared Insights project with an external attendee account.
- Check whether the prepared project has a completed native Insights run. If it does, open the cluster, its representative conversations, and a counterexample. If it reports no completed run, the native exercise remains unavailable; use source-linked turns and say so. A fresh participant batch may not produce a cluster during the session.
- Confirm the frozen data assignments and the supplied local checks. Passenger and reservation families must not cross discovery, monitor-check, development, final, and later-traffic groups.
- Check the fixed model and current inference access. The notebook defaults to an adjustable $8 inference allowance. Notebook compute and native tag judging are separate; show the measured qualification cost rather than promise the limiter caps those services.
- Confirm the native tag can be restricted to this workshop agent and disabled afterward. Do not reuse a broad organization tag for classroom traffic.
- Open the recorded fallback. Label every replay result as recorded. It cannot establish what a learner's unexecuted edit would produce.
- Check the first and last slides, worked-answer links, exact notebook control labels, and screen-sharing readability. Keep the facilitator monitor open with the current participant roster.

## Opening script

“An airline agent has been asked to change a passenger's outbound journey. The return flight should stay. The booking API takes the entire itinerary, so a perfectly successful call can still remove the wrong flight. We will inspect what the agent did, decide what a monitoring rule should catch, and make a test that catches the same problem before a later release.

“These are simulated bookings from a public benchmark. Your live agent may get the request right. If it does, keep that result. We have a labeled local incident for learning the failure mechanism. The point is to connect a claim about behavior to a booking, a trace, and a repeatable check.”

## Timed facilitation

| Elapsed | Lead with | Participant task and completion check |
| --- | --- | --- |
| **0–25** | “What should change, and what must survive?” | Inspect the exact request and booking. Connect the copied notebook. Save the expected change, the segment range, and the flights that must remain. |
| **25–65** | “Record the work before inspecting it.” | Edit model/tool scopes, add version and traffic-batch attributes, run eight discovery conversations, and open one stored tool result. |
| **65–100** | “A chart or cluster gives us somewhere to look.” | Read Overview as project context. In Conversations, filter the exact agent and custom `airline.version = baseline`, save the view, and inspect discovery requests. Investigate prepared Insights only when a completed cluster exists. Save one claim with its supporting event and recovery status. |
| **100–110** | Break | Save the investigation. Do not rerun successful cases to create a failure. |
| **110–155** | “Write a rule that survives a counterexample.” | Review native Alignment turns, including legitimate shorter itineraries. Test revised criteria, save the selected rule, and read back the native identity. |
| **155–190** | “Which cases did we judge, and which did we miss?” | Implement precision, recall, and coverage. Enable the scoped tag and run four monitor checks. Live assignments only establish positive matches; calculate agreement from explicit Alignment results and keep all other turns unknown. |
| **190–230** | “Save the booking before it was changed.” | Implement regression-case construction and state checks. Curate a reviewed incident plus an unflagged control. Keep the explanation judge separate. |
| **230–240** | Break | Save the selected criteria and regression dataset. |
| **240–285** | “Fix the transformation, then see what the agent does with it.” | Implement the complete itinerary builder. Run free fixtures and the saved curated regression cases, then four matched development requests on each version. Inspect confirmation and preserved flights. |
| **285–320** | “Stop choosing before opening these cases.” | Freeze the tested version. Run six reserved requests across both versions. Inspect one aligned case in EvalTables and its two traces. |
| **320–345** | “Use the same rule on later requests.” | Run four subsequent requests across both versions. Compare tags with booking checks and examine coverage before interpreting a changed alert rate. |
| **345–360** | “What would you keep, and what would you test next?” | Publish saved results and a short Report. Reproduce one case. Disable automatic tagging and verify its native state. |

Keep the breaks fixed. If a service is slow, use its saved evidence to explain the result and resume publication separately. Do not cut the comparison by silently dropping failed or missing cases. Record unfinished work and continue with the clearly labeled fallback.

## What to ask at each transition

- **Before tracing:** Which exact passenger request belongs to this conversation? Which work belongs to the current turn?
- **After a tool call:** Did it execute successfully? Did the returned booking satisfy the passenger? Those questions need different evidence.
- **During Insights:** Which actual turns support this description? Which counterexample limits it?
- **During Alignment:** Is the judge wrong, the review wrong, or the evidence insufficient? A judge's explanation is another claim to check.
- **During monitor checks:** What is the denominator? Did an absent tag mean a negative judgment or no judgment yet?
- **During curation:** Can you reconstruct the original booking from this case without relying on a modified live database?
- **During repair:** Did the code preserve the prefix and suffix? Did the agent select the correct range and obtain approval?
- **During final evaluation:** Are these the same starting cases and frozen versions? Which failures remain?
- **During later monitoring:** Did alerts fall because bookings improved, processing coverage changed, or the requests changed?

## Expected implementation lessons

- Native tag criteria, a notebook explanation rubric, and a deterministic booking scorer are separate pieces. Editing one does not update the others.
- Testing criteria in Alignment does not change the live rule. Save the chosen tag criteria explicitly.
- A tag's native turn context may omit evidence needed for a judgment. Keep insufficient evidence explicit.
- A shorter itinerary can be correct: two connecting outbound segments may become one nonstop while preserving the return.
- Unflagged controls are needed to study missed failures. Reviewing alerts alone cannot establish recall across traffic.
- A regression case needs the original state, request, applicable policy, expected scope, review, and source identities. A saved filter is insufficient.
- Completed executions survive failed publication. Retrying an export must not send another model request.
- The deterministic list-repair drill is a worked implementation improvement. Agent outcomes can improve, tie, or regress; preserve what happened.

## Recovery during the session

| What participants see | What to do |
| --- | --- |
| Project or credential error | Repair the participant's access, run the explicit access check again, and resume the failed step. Never lend facilitator credentials. |
| Agent succeeded on every discovery case | Keep the successes. Use the labeled calibration pack for failure investigation and continue the live comparison. |
| Native Insights has no new cluster | Use a verified prepared cluster if one exists. Otherwise inspect saved turns and mark native Insights unavailable. Do not call a notebook grouping “Insights.” |
| Tags or Alignment unavailable to the account | Use source-linked recorded screens and local review exercises. Mark native access incomplete; do not claim the native exercise passed. |
| Tag result has not arrived | Keep the judgment unknown. A missing live assignment alone does not reveal processing status; use explicit test results for known predictions and keep the eligible-turn denominator. |
| Inference is interrupted with an uncertain outcome | Inspect the saved request and accounting receipt. Follow explicit recovery; do not automatically resend it. |
| EvalTables or Report publication fails | Keep the local comparison and saved executions. Retry publication after access or service recovery. |
| The repaired version regresses | Inspect the matched case and retain the prior version if warranted. This remains a completed learning outcome. |
| Tag disabling cannot be verified | Treat cleanup as incomplete. Open the native tag and verify the state before ending the session. |

## What counts as completion

The participant can show one request, its initial and final booking, a supporting Agent Lens event, a reviewed monitoring decision, and a regression case. They can distinguish task correctness, monitoring accuracy, processing coverage, and explanation quality. Their conclusion links the tested code and comparison, includes unresolved failures, and states whether the repair is worth keeping.

Native access, actual qualification outcomes, browser execution, external-account checks, and human usability rehearsal are recorded separately in the release evidence. A generated deck and notebook are not proof that those checks passed.
