# Transit software-factory facilitator guide

This is a technical preview. Live worker execution and native Forge readback are recorded. Complete the external-account and human-rehearsal checks before using this schedule with attendees.

Use the current Transit notebook and companion deck. The session lasts four hours, including a ten-minute break. Keep the code exercises visible. The notebook’s saved task board and timeline are the source for what actually happened.

## Before the room arrives

- Open an attendee-style copy in a project you can write to. Check project access separately from inference access.
- Read the data receipt: this is a November 2024 MBTA schedule, not live arrivals.
- Confirm the fixed model, adjustable allowance and saved retry behavior. Opening the notebook must not start work.
- Check the worked local scenarios, Agent Lens readback and native comparison publication. Keep a recorded replay ready, clearly labeled.
- Open the read-only facilitator monitor. Missing progress means unknown; it does not mean a participant failed.
- Keep the [two-minute captioned code walkthrough](../decks/transit/public/walkthrough/index.html) available. It shows worked answers and free checks, so reveal it after participants have attempted the exercises. The reference app at its end is labeled separately from agent results. The second recording follows actual saved R4 worker patches into Agent Lens, EvalTables and the exported app; it preserves the incomplete follow-ups.

## Timed script

| Elapsed time | Say and demonstrate | Participant task | Check before moving on |
| --- | --- | --- | --- |
| 0:00–0:20 | “We need a departures board. Before we hire several agents, let’s decide how we’ll know the board works.” Show the actual Park Street `24:08:00` row. | Connect, send the setup trace and implement `check_departures()` for the after-midnight scenario. | Their project receives the trace. The real row passes, and a missing train or wrong service date fails. |
| 0:20–0:45 | “The first worker needs a clear task, source files and a way to test its change.” | Complete the worker request and `dispatch_action()`; run one worker; inspect its trace and diff. | They can open the model request, one tool result and the file it changed. |
| 0:45–1:10 | “These components can run in parallel. The board cannot finish until both are ready.” | Complete `ready_tasks()` and `claim_task()`; run the free dependency and competing-claim checks. | Blocked work stays blocked; one task has one owner. |
| 1:10–1:45 | “Watch the tasks, not just the agents talking.” | Review the contracts and run the two-worker build. Follow a claim, source edit and test in the timeline. | The displayed owner, source version, patch and test belong to the same task. |
| 1:45–1:55 | “Save the checkpoint. We will test the patches together after the break.” | Break. | Completed work is saved; pending publication is labeled separately. |
| 1:55–2:25 | “The patches each passed a check. Now let’s test the application they produce together.” | Review both diffs, integrate the accepted patches and run the combined departures board. | They can explain a pass or failure using actual departure rows and their own acceptance check. |
| 2:25–2:50 | “What should the next worker know, and what evidence makes us trust it?” | Write and review one scoped lesson; complete `select_memories()`. | The rule links to a real test or tool event; an unverified or obsolete claim is excluded. |
| 2:50–3:25 | “Now give two fresh teams the same follow-up. Only one gets the lesson.” | Run both versions of the last-direct-train feature; inspect requests, review diffs and integrate the accepted patches. | Same starting code and request; both actual outcomes remain saved. |
| 3:25–3:45 | “Compare the departures first. Then compare time and cost.” | Complete the development scorer; freeze builds; run final cases; open an aligned comparison row. | They distinguish wrong output, incomplete execution and unavailable publication. |
| 3:45–4:00 | “Which build would you release, and which check supports that decision?” | Complete `release_decision()`; reload one saved case; publish the release decision; explain one result to another participant. | Code and evaluation identify the same build. Each person opens a matching record; missing or failed checks block release. |

## Explain the recorded result accurately

R5’s one-worker build passed 10/10 final cases; the two-worker build passed 8/10. Both had passed their public development checks. Use this to show why a component check is not a release decision. Both follow-ups scored 12/18 after their query workers stopped before testing, so the memory comparison remains unresolved. The supported R5 release is the single-worker departures board; the follow-up feature stays blocked. The R4 recording is an earlier rehearsal with its own results.

## Keep the class moving

- If setup is still blocked at 0:20, have the participant inspect the labeled recorded trace while they repair access. Do not substitute the host’s credentials.
- If a paid request has an uncertain outcome, inspect its saved receipt before retrying. Never automatically resend it.
- If a trace or comparison failed to publish, use the saved output and publication-only retry. Do not rerun a successful build just to obtain a dashboard.
- If the live agents succeed, keep that success. Use the labeled contract-mismatch example to teach integration failure.
- If integration fails, let the learner identify the failing condition. Do not quietly replace its patch with a worked answer.
- If the two follow-up versions tie, ask whether the lesson changed the work or simply added context. Do not claim that consulting memory made the output better.
- At 3:25, stop adding features. Freeze and evaluate the available builds, keeping incomplete records explicit.
- At 3:45, move to reproduction and the release decision. Use two minutes each for participants to explain a result; save further feature work for later.

## Questions that reveal understanding

- Which task can start now, and which prerequisite blocks the other one?
- Where is the worker’s claim checked against an actual test?
- What did the second worker know that the first one did not?
- Which source event supports the shared lesson? Where would that lesson stop applying?
- Did the team improve the departure list, reduce elapsed time, increase cost, or some combination?
- What would make you retain the previous release?

## Closing explanation

“You wrote the machinery that turns a feature into coordinated work. You can follow a task into its worker trace, inspect the patch, test the integrated product and save a lesson for another task. The useful question is whether that process delivered a better result for its cost. Your comparison gives you a first answer for this build.”

An optional ARIA exercise comes after the measured comparison: ask it to inspect one published integration failure and propose a follow-up check. Verify its cited event. ARIA access is not required to finish.
