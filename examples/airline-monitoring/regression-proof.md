# A reviewed booking becomes a regression check

This is a free local adapter comparison using two saved, controlled simulator incidents. It is not another agent run and does not change the live workshop's 40/40 result. The reviews were supplied as canonical worked answers for a technical check, not collected in a human-participant rehearsal.

The first passenger asked to replace outbound HAT007 with HAT061 on May 19 while retaining return HAT174 on May 29. The source calibration incident deliberately submitted only HAT061 and ignored the passenger's refusal. Its API call succeeded, leaving the return missing. The second passenger asked only to read a one-way itinerary; that is the unflagged control.

The canonical `case_from_reviewed_turn` saved each original request, booking state, reviewed expectation, and source event. `run_regressions` then executed the omission adapter and `my_itinerary_builder` against those same cases, using the simulator's independent state checks. The repair returns the unchanged prefix, requested replacement, and unchanged suffix.

| Reviewed case | Omission adapter | Learner repair |
| --- | --- | --- |
| Change HAT007; retain HAT174 | Proposed only HAT061. Passenger refused; booking remained unchanged and requested-change check failed. | Proposed HAT061 and HAT174. Passenger approved; both flights were saved and all booking checks passed. |
| Read a one-way itinerary | Booking unchanged; checks passed. | Booking unchanged; checks passed. |

The regression replay respects confirmation even for the faulty adapter. Its failed proposal therefore leaves the request unresolved rather than repeating the controlled incident's unauthorized write. That difference is visible in the saved tool receipts.

The proof made **zero model requests and zero publication calls**. Running it again reused the same completed stage. Neither case is reserved evaluation data. The learner scorer's results are saved separately from the independent booking checks.

Open the [full proof](regression-proof.json), [original controlled incidents](calibration.json), or the [positive source conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/de37d1e213a2dbae8135bf67e769909c). The [one-way control](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/eb1d81f473b0ae773c833d5332493dbd) records the unchanged booking.

To reproduce from a restored qualification workspace containing those source stages:

```sh
uv run python scripts/prove_airline_regression.py \
  --state PATH_TO_RESTORED_WORKSPACE \
  --output regression-proof.json
```

The script refuses model execution and verifies that the request ledger is unchanged. It does not authenticate or publish. The notebook performs this same check on the participant's own saved reviews.
