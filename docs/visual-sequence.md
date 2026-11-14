# Follow a record through the workshop

Use the deck to introduce an operation, then let participants inspect the same operation in their notebook. Arrow keys advance the slide's code highlights and callouts. Next and Back in a notebook explanation change the view; they do not execute the agent or train a model.

## Pending: an office ticket

Start with both requests: refund one duplicate charge and grant Alex access when a write succeeds before its response times out. Ask participants to describe the account state they expect, before showing any agent output.

- Follow an actual action through its Python arguments, result, and the observation appended to the model's next request. Point out the same account and invoice in each view.
- Open the linked Agent Lens span and find those arguments and the returned payments. The setup trace checks the environment; it is a different operation from the account lookup.
- Inspect whether the run called `read_skill`. Saving a skill only makes it available. If it was not read, say so.
- In the local timeout exercise, inspect state before deciding whether to retry. Reset restores this practice case; it does not erase workshop runs.
- Compare the instruction diff, subsequent calls, and checked account state. The final case selector aligns the starting, manual, and agent-selected versions. A longer call sequence can end in the same correct result.

Keep four checks separate: `check_work` is a tool the agent can call, the participant writes a development scorer, the final grader checks fresh cases independently, and the explanation judge assesses what the agent said. Valid JSON from the judge only establishes that its response can be read.

## Solar: one forecast timestamp

The lab is preparing for its weekly forecast review. A useful result includes enough information for a colleague to reproduce it.

- Select an accepted GOES window. Show the 60 input samples, latest reading, and separate target 30 minutes later. Toggle standardized inputs and identify the training mean and standard deviation. The target and persistence forecast remain in log-flux units.
- Run the free forward-pass check. Follow the tensor shapes through flattening, temporal convolution, or residual image prediction. This checks model wiring; it does not train weights.
- Use the public scorer fixture to calculate error before averaging it. Move the illustrative pixel error inside and outside the disk mask. Then inspect a real saved forecast.
- Compare persistence, manual, and agent predictions at one common timestamp. Read the target time and per-case errors; use the shared scales to compare the panels.
- Open the saved GOES model's loss history and predictions beside persistence. Its training completed but its forecast was worse. Longer training is a proposed follow-up, not an observed repair.

The recorded image result is from one fixed-seed rehearsal with overlapping windows on two reserved days. Use it to explain the code and comparison, not to promise that every participant will get an improvement.

## Reading branches

Gray identifies the parent, blue Candidate A, and orange Candidate B. Composition has a neutral decision card. These colors do not indicate quality. Solid arrows show code or execution flow; dashed arrows show evidence the editor reviewed. The selection is labeled explicitly.

Select a recorded node to read its intent, diff, result, rationale, and Forge links. “Retain this version” means the selected code is unchanged. A proposed or planned version has no execution or trace until one is recorded.

## If publication is unavailable

Show the saved comparison in the notebook. Agent execution, trace export, W&B publication, Weave, and native EvalTables have separate status records. Retry the failed publication from saved work. Do not rerun an experiment to repair a screenshot or missing link.

The native comparison slides show Evaluation Tables (Preview) in the Forge W&B workspace, backed by saved Weave evaluation calls. Older W&B Table and Weave captures keep their original labels. The separate CES service remains unavailable. See [evaluation setup and recovery](evaluations.md).
