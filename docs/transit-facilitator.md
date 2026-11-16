# Transit software-factory facilitator guide

This is a technical preview. Live worker execution and native Forge readback are recorded. Complete the external-account and human-rehearsal checks before using this schedule with attendees.

Use the current Transit notebook and companion deck. This is one six-hour session, including two ten-minute breaks and one twenty-minute break. The extra time is for working through the code and explaining a result. Keep the code exercises visible. Use the notebook’s saved task board and timeline to determine what happened.

## Before the room arrives

- Follow the [Transit start page](https://ash0ts.github.io/forge-workshop-kit/packet/start/transit.html) in a fresh local folder. Enter a project you can write to, then check project access separately from inference access.
- Read the data receipt: this is the November 2024 MBTA schedule, not live arrivals. Find trip 63926435 at stop 70076, with ThanksgivingDay service and departure 24:08:00.
- Confirm the fixed model, adjustable allowance and explicit run controls. Opening the notebook must not start work.
- Run the free local checks. Open a verified Agent Lens trace and native comparison. Have the recorded results available with their rehearsal labels.
- Open the read-only facilitator monitor. Missing progress means unknown; it does not mean a participant failed.
- Use the [captioned walkthrough](../decks/transit/public/walkthrough/index.html) after an attempt or requested hint. Its first recording shows free checks and the instructor-authored reference app. The second follows saved R4 patches into Agent Lens, EvalTables and the exported app. Neither records a new attendee execution.

## Timed script

| Elapsed time | Say and demonstrate | Participant task | Check before moving on |
| --- | --- | --- | --- |
| 0:00–0:30 | “Someone leaving an evening event needs the next train. A list that looks plausible is not enough.” Follow one actual stop-time row through the trip, active service date and civil timestamp. | Run **Show departures from the saved timetable**, then write and check `check_departures()`, before connecting. Explain why 24:08 on Nov 28 service means 00:08 on Nov 29. | They name both dates and the same trip ID. |
| 0:30–0:50 | “Use your own project so you can reopen every result after today.” Show the setup span’s arguments, output and recorded time. | Connect, restore the opening draft and check, edit an attribute in `instrument_tool()`, and send the setup trace. | Their trace is in their project. The real row passes; a missing train and wrong service day fail. |
| 0:50–1:35 | “The model chooses an action. Python runs it. The next request needs the result.” Step through read, hash-checked edit, test and submission. | Complete `build_worker_request()` and `dispatch_action()`. Run the free check, then the single-worker build. Open one request, file edit and test in Agent Lens. Review the patches, click **Review and test the one-builder app**, then **Preview this saved app**. | They show the actual observation supplied to the next request, not just the action the model requested. |
| 1:35–1:45 | “Keep the saved task and source. We’ll add coordination after the break.” | Ten-minute break. | No duplicate requests start when they return. |
| 1:45–2:25 | “Both threads can see pending. That does not give both permission to start.” Show the controlled two-owner race and atomic one-owner repair. | Complete `ready_tasks()` and `claim_task()`. Run the free dependency and claim checks. Inspect permitted files and separate working copies. | Only pending work with integrated dependencies starts. One task has one owner. The lock is released before model execution. |
| 2:25–3:00 | “These modules share an interface. They still need to work together.” Start the two-worker build, then review the actual patches. | Run the team, inspect claims and diffs, confirm review, test integration and preview Park Street after midnight. | The reviewed files match the tested files. The displayed row retains the service date and boarding timestamp. |
| 3:00–3:20 | “Save both builds and their checks. We’ll use them to write a project lesson.” | Twenty-minute break. | The build outcome remains saved even if publication needs a retry. |
| 3:20–4:00 | “A note can be useful-looking and still be wrong or obsolete.” At 3:20–3:28, ask ARIA what the two development integrations establish, and check one cited event. Then filter illustrative notes by acceptance, contract version, scope and tags. | Implement `select_memories()`, run its free check, inspect a lesson proposal and save a rule supported by a development result. | The participant opens the cited check. They explain applicability `version` versus evidence `source_revision`. |
| 4:00–4:45 | “Give fresh teams the same next feature. Only one receives the accepted lesson.” Read the last-direct-train contract. | Run both follow-ups, inspect memory selection and request contents, review the patches and test integration. | Starting source, model and limits match. Both outcomes remain represented. No lesson is edited midway through the pair. |
| 4:45–4:55 | “Stop adding features. Keep the available versions for comparison.” | Ten-minute break. | Failed and incomplete work remains visible. |
| 4:55–5:30 | “Read a prediction before its average.” Explain the participant scorer and independent final checks; follow the recorded UTC defect through query and renderer. | Check `score_scenario()`, freeze the builds, run the final scenarios and open one aligned row in Forge. | They distinguish a wrong output, an unavailable judgment and a publication failure. Two failed checks may expose one bug. |
| 5:30–6:00 | “Which version would you let another person use?” Explain the release rule, then reproduce one saved input. | Check `release_decision()` and choose a tested version. At 5:35–5:42, use ARIA or the recording to check the draft conclusion before publishing its evidence. Reload the app bundle and compare a row. | Failed or missing required checks block release. The released code, data and comparison agree. Each person explains one result. |

## Exact controls to use

Tell participants which notebook step to open before naming a button. A free check saves the current exercise code; editing it afterward requires another check.

| Notebook step | First | Then |
| --- | --- | --- |
| Understand the departures board | **Show departures from the saved timetable**, then **Check my after-midnight scenario**; no account needed | **Connect and restore my work**, then **Send my first Agent Lens trace** |
| Run one builder | **Check my build_worker_request code**, then **Run one worker on the first feature** | Review the actual patches, **Review and test the one-builder app**, then **Preview this saved app** |
| Divide and claim the work | **Check my ready_tasks code** checks readiness, claims and the local race | Explain the two-owner to one-owner result before continuing |
| Run two builders | Confirm the worker and task checks still match the saved code | **Run the ready tasks with two workers** |
| Test the combined app | Read both diffs; tick **I reviewed the two-builder patches and their development checks** | **Test the combined departures board**, then **Preview this saved app** |
| Keep a checked lesson | **Check my select_memories code**; optionally **Ask the agent to propose a lesson** | Choose **Supporting development result**, write the rule, then **Save a checked lesson** |
| Build the next feature | **Run both versions of the follow-up feature** | Review both diffs; tick **I reviewed the no-lesson and shared-lesson patches**; **Integrate the reviewed follow-up patches** |
| Compare frozen builds | **Check my score_scenario code** | **Compare the frozen builds** |
| Reproduce and release | **Check my release_decision code**; select the tested version and write the conclusion | **Publish this release and its evidence** |

Seeing the solo app does not select the source for the memory comparison. That selection still waits for both initial integrations, with the same team-then-solo preference when checks pass. Both follow-ups start from that one saved release.

**Retry saved Forge publications** exports completed work again. **Allow another attempt** authorizes recovery of stopped execution; it does not itself start the builder. Do not confuse these controls.

## Explain the recorded results accurately

Keep the rehearsal identity on the screen:

- **R3:** the captured presentation worker ran a passing component check. Its sibling query worker exhausted its output allowance. This capture teaches trace inspection, not a successful release.
- **R4:** both initial builds passed 10/10 final scenarios. Both follow-ups scored 14/18 after query workers reached an input bound. The recorded walkthrough preserves that outcome.
- **R5:** the one-worker build passed 10/10; the two-worker build passed 8/10. Both had passed five public development checks. The two failed final cases exposed the same UTC-input defect in the query and rendered board. Both follow-ups scored 12/18 after their query workers stopped before testing.

For the UTC example, 23:00 UTC is 18:00 Eastern. The expected next train is trip 63919613 at 18:03 Eastern. The team query used the caller’s timezone as its service-day origin and selected trip 63919759 from service-clock 23:03. That changes the selected train, not merely its display format. The observed two failures concern one bug.

R5 supports releasing the single-worker departures board. The follow-up feature remains blocked. Neither incomplete follow-up establishes a memory benefit. Builder elapsed time excludes human review and integration; keep cost and product correctness separate.

## Keep the class moving

- At 0:50, use the labeled recorded setup trace if an attendee is still repairing access. Never lend the facilitator’s credentials.
- At 1:35, preserve whatever the single worker produced. Use the trace to teach the loop even if the worker stopped.
- If a request has an uncertain outcome, inspect its saved receipt before authorizing recovery. Do not automatically resend it.
- A large generated file can exceed the input bound; a model can also exhaust its output allowance without returning an action. Name which limit stopped the task. See the [runtime recovery guidance](transit-workshop.md#when-a-builder-stops).
- If publication fails, use the saved notebook results and publication-only retry. Do not rerun a successful build to obtain a dashboard.
- If both initial integrations fail, the notebook offers **Continue from the prepared reference app**. Explain that it runs the instructor’s version and preserves both live failures.
- If the live agents succeed, keep the success. Use the labeled contract-mismatch illustration or recorded UTC defect for discussion.
- At 4:45, stop adding features. Freeze the available builds when evaluation begins. A failed branch still belongs in the comparison.
- At 5:30, move to release and reproduction. At 5:48, give each person two minutes to explain one result while controlling their own notebook.

## Questions that reveal understanding

- Why does this departure have different service and boarding dates?
- What result did Python return, and where was it included in the next model request?
- Why does a submitted patch not unblock a task that depends on integrated code?
- What happens between checking a task is free and writing its owner without a lock?
- Which field says where a lesson applies, and which field identifies its original evidence?
- Did this code change improve the departure list, reduce elapsed time, increase cost, or some combination?
- Why can two failed scenarios describe one underlying defect?
- Which exact version would you release, and which check supports that choice?

## Closing script

“You now have a departures board and the Python that assigned its work. Show which version passed your checks, what the workers changed and what you would test next. If the last feature failed, keep that result in the Report. The release decision should follow the checks.”

ARIA investigates development evidence before lesson acceptance and the frozen comparison before Report publication. Use the recorded investigation when live access is unavailable; preserve the UTC final-case finding for the closing stop.

Use the [ARIA investigation guide](aria-investigations.md) for native context attachment, the recorded fallback, citation checks, access requirements, and separate ARIA usage. These stops replace discussion time and do not add execution gates.
