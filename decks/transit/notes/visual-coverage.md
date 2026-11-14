# Transit visual teaching revision

The revision retains 94 slides and the six-hour schedule. It replaces 23 generic sequence frames and adds visual explanations to nine formerly text/card/table slides. There are 42 slides containing a teaching diagram or native capture, up from 33. Component uses rise from 28 to 37; generic flow rows fall from eight to four, and tables from five to three. These counts describe source coverage, not learning effectiveness.

The editable component is `components/TransitMechanism.vue`. `scripts/visual-sequences.py` applies the replacements to the authored storyboard. Opening or building these visuals does not execute the workshop.

| Mechanism | What the learner follows | Evidence and limits |
| --- | --- | --- |
| GTFS joins | `stop_times.trip_id` → `trips.service_id` → the calendar; `stop_id` → Park Street | Actual archived rows in `src/forge_workshop_kit/assets/transit/tables.json.gz`: trip 63926435, stop 70076, ThanksgivingDay service, November 28, 2024 |
| Service time | `24:08:00` from November 28 midnight → November 29 00:08; retain the service date | Actual timestamps; the final eight minutes are visibly enlarged |
| Worker loop | Read source → illustrative diff → current-file test → patch review; observation returns to the next request | Implemented `read_file`, `write_file`, `run_tests` and `finish` contracts in `factory.py`; the displayed modulo repair is illustrative, not a recorded worker patch |
| Task dependencies | Independent query and rendering work → blocked or ready integration | Illustrative graph matching `ready_tasks()` and the participant exercise |
| Claim race | Two pending reads → two assignments; locked check-and-assign → one successful claim | Deterministic local two-thread qualification in `transit.qualify_coordination_repair`; no model calls |
| Working copies | One starting source → two owned files → reviewed patches → combined tests | Implemented file ownership and base-hash checks; small displayed edits are illustrative |
| Shared records | Task owner/status, interface contract, checked rule/evidence | Illustrative record content; work status is not a learned rule |
| Retrieval | Proposed, stale and unrelated notes are excluded; the accepted applicable note enters context | Actual learner `select_memories()` schema; notes are illustrative, not four R5 records |
| Matched follow-ups | Same starting source/task/model/limits → only the lesson input changes → both outputs retained | Recorded R5: both pass 12/18, with different request-bound failures. No observed memory benefit |
| Product/time comparison | Ten scenario marks and separate elapsed-time bars | Recorded R5: 10/10 versus 8/10; 124.78 s versus 94.91 s. Builder time excludes review and integration |
| UTC defect | 23:00 UTC = 18:00 Eastern → expected 18:03 train → later wrong service-clock train → wrong board | Recorded R5: expected trip 63919613, actual trip 63919759. Two failing scenarios expose one underlying defect. Clock spacing is illustrative |

Native captures remain unchanged and source-linked. The R4 equal-pass screenshot and R5 regression screenshot keep their separate rehearsal identities. The later follow-up tie remains visible. Final rendered validation is recorded in `delivery-checks.json` and `pdf-checks.json`; it does not establish participant usability or external-account access.

The shareable preview is `public/graphics-preview.png`: the verified slide 36 atomic-claim diagram. `graphics-preview.json` records its source and hashes. Original native Forge captures are unchanged.
