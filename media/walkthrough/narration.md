# Forge Workshop Kit: narration for the ten-minute tour

Read this over the clean video. The captioned version uses these same words. The recording shows saved work and display-only interactions; it is not a new live experiment.

## 00:00:00–00:00:50 · Why these workshops exist

**00:00:00–00:00:25 — Show:** The six workshop cards.

I built these workshops for engineers who want to understand the work around an AI application after its first demo succeeds. A refund agent can finish an API call and leave the account wrong. A forecast can have a score nobody can reproduce. Two coding agents can finish assignments whose parts disagree.

**00:00:25–00:00:40 — Show:** The published Report introduction.

The Reports introduce each problem through a worked example, with code and recorded results. You can read the explanation first, then try the same exercise in your own project.

**00:00:40–00:00:50 — Show:** The complete account comparison in the published Report.

Here, the customer wants one duplicate payment refunded. The account before and after tells us what success means. That gives the agent something concrete to satisfy.

## 00:00:50–00:01:30 · How someone starts

**00:00:50–00:01:15 — Show:** The public notebook start page and setup instructions.

The start page links the Forge template, a notebook download, and laptop instructions. Participants use their own credentials. The current source is version 0.12.0. Hosted templates remain on the previous revision while Forge publication access is blocked. The adjustable notebook inference allowance defaults to eight dollars. Compute and ARIA usage are separate.

**00:01:15–00:01:30 — Show:** The running guide.

The running guide helps you choose a short demo, one exercise, or a full pilot. The notebook keeps editable code beside a free check, explicit run control, and result. Opening saved work launches no training or model request.

## 00:01:30–00:02:25 · Pending: inspect and change an agent

**00:01:30–00:01:53 — Show:** The invoice dispatch and observation sequence.

Pending is an office handling billing and account access. A customer has been charged twice and needs the duplicate refunded. The participant writes an invoice tool, dispatches an action, and appends its returned observation to the next model request. This drawing follows the same invoice through those operations.

**00:01:53–00:02:25 — Show:** Actual arguments and returned account data.

In Agent Lens, we inspect the actual tool arguments, returned result, timing, and next model action. The account check tests the customer outcome. The timeout exercise repairs a committed write whose response was lost. Reusing its operation ID prevents a duplicate membership. Participants then compare manual and agent-written harness changes on matching cases. The recorded final comparison tied: extra checking changed behavior, but did not improve the pass count.

## 00:02:25–00:03:25 · Solar: test a research change

**00:02:25–00:02:49 — Show:** One forecast window and its target.

Solar puts you in a lab preparing its weekly forecast review, using real GOES X-ray measurements and AIA images. One timestamp stays visible as we construct the history window and keep the future target separate. Persistence copies the latest reading forward. This baseline gives every trained model a result to beat.

**00:02:49–00:03:10 — Show:** Six configurations, validation error and runtime.

Participants train small models, inspect loss curves in runs, and use a Sweep to compare six existing configurations. A research agent later proposes image-model code changes. Participants review diffs and train candidates before selecting one. The language model stays fixed while forecasting weights train.

**00:03:10–00:03:25 — Show:** The exact source saved with the selected Solar image model.

This saved Solar source contains a zero-initialized residual layer and absolute-error loss: the tested code. The failed GOES recipe and mixed image outcomes remain visible. Artifacts also keep settings, weights, and predictions for investigating those results.

## 00:03:25–00:04:20 · Routing: train, release and recover

**00:03:25–00:03:56 — Show:** The same probability columns with different intent mappings.

Routing starts with a banking support queue: a missing card needs a different workflow from a card that does not work. This release drill deliberately moves the intent names while leaving probability columns unchanged. The same confident score now sends the request to the wrong queue. Participants write a regression check, repair the loader, and restore a previous version. The repair fixes release behavior, not the trained classifier.

**00:03:56–00:04:20 — Show:** Matching requests and evaluated predictions.

The classifier exercise uses Banking77. Participants fit a baseline, inspect validation mistakes, and test a different text representation. EvalTables aligns the same requests, predictions, labels, and errors across versions. Runs record the model comparison; Artifacts preserve preprocessing, intent order, and the classifier. The release target is a notebook batch predictor.

## 00:04:20–00:05:15 · Inspection: investigate a missed defect

**00:04:20–00:04:50 — Show:** One patch and its normal reference.

Inspection asks which circuit boards need attention before leaving the line. We use real VisA PCB photographs. Participants investigate a missed defect before changing the representation. A whole-image vector can lose a small local change. This calculation follows one patch to its closest normal reference. The distance becomes a feature; the distance image is not a causal explanation. Supplied defect masks remain inspection aids, not classifier inputs.

**00:04:50–00:05:15 — Show:** Actual board images, scores and labels.

EvalTables displays the actual boards beside scores and labels. Participants examine a corrected miss and a new mistake, not only an average. They compare active and random review under the same labeling budget. More labels helping does not prove the selection method was better. Artifacts retain the feature code, reference bank, classifier, and threshold needed to reproduce that detector.

## 00:05:15–00:06:10 · Transit: coordinate two coding workers

**00:05:15–00:05:40 — Show:** The claim race and atomic repair.

Transit is the software-factory workshop. Two coding agents build a departure board from a real, historical MBTA schedule. Participants implement dependencies, atomic claims, ownership, and integration. This exercise shows why two workers must not claim the same task. The task board separates submitted, tested, and integrated work. Finishing assignments does not establish that the combined application works.

**00:05:40–00:06:10 — Show:** Matching solo and team acceptance cases.

The saved R5 acceptance comparison puts solo and team builds against matching scenarios. The team did worse on two checks. After-midnight service times make integration concrete: twenty-four-oh-eight belongs to the previous service day. Agent Lens records assignments, edits, tests, and handoffs. Artifacts retain source and releases. A later matched comparison starts fresh workers with and without a verified lesson. It did not establish a memory advantage. Reading a note proves retrieval; the delivered application tells us whether it helped.

## 00:06:10–00:07:10 · Airline: connect monitoring to evaluations

**00:06:10–00:06:35 — Show:** Original, incomplete and preserved itineraries.

Airline follows a passenger changing part of a round trip. These bookings and requests are simulated benchmark data. The update API replaces the whole itinerary. Sending only the changed outbound flight can remove the return journey. This controlled example shows the original, incomplete, and preserved itineraries together. The API can succeed while the booking becomes wrong.

**00:06:35–00:07:10 — Show:** A recoverable tool timeout and the passenger request.

The native conversation shows a recoverable read timeout. Participants inspect individual turns and write their own review before calibrating a monitoring rule. Agent Lens activities cover Conversations, Insights, Tags, and Alignment. Reviewed incidents become versioned regression cases; repairs are compared in EvalTables. Monitor agreement stays separate from agent correctness. The recorded live agent passed its requests. The itinerary defect is taught as a controlled example. Native AI Alignment and prepared Insights still need qualification. Missing judgments stay unavailable, not passes.

## 00:07:10–00:08:00 · ARIA: investigate a result, then verify a claim

**00:07:10–00:07:30 — Show:** The actual shared ARIA controls with a restored response.

At each ARIA stop, participants inspect a result and explain what they think happened. Start ARIA investigation sends that question with selected published records. The notebook saves the returned conversation; Check ARIA response retrieves its answer. Opening the notebook sends no hidden request.

**00:07:30–00:07:48 — Show:** The actual ARIA answer to a development question.

Open ARIA conversation continues that same discussion in Forge. Here, ARIA distinguishes a supported observation from an untested explanation. It does not become the scorer or approve a repair. Live access follows organization settings and is outside the notebook inference allowance.

**00:07:48–00:08:00 — Show:** The cited execution artifact opened from the answer.

Open the cited record and check the claim. Mark it supported, disputed, or unresolved. The recorded fallback teaches the same verification when live access is unavailable.

## 00:08:00–00:09:20 · Use the material and measure the entry path

**00:08:00–00:08:30 — Show:** Setup, timing and fallbacks.

Each deck has a running guide. The facilitator instructions cover preparation, timing, saved-result fallbacks, and participant progress. Full sessions remain technical previews while external-account and participant rehearsals are outstanding. For a customer conversation, choose the closest problem. One five-minute investigation can be more useful than a tour of every product. The guide helps you choose what to show and what participants should inspect.

**00:08:30–00:08:55 — Show:** Public entry link and tracking explanation.

Registered UTM.io links identify external entry paths. Video and community Slack have separate tags. Workshop QR links identify the workshop. A shared deck-and-poster link cannot distinguish those surfaces. Coworker reviews use the direct library address, outside the acquisition campaign. A visit is not a notebook copy or a completed exercise. Previews and repeat visits can add visits.

**00:08:55–00:09:20 — Show:** Workshop entry points.

The library lets someone read a Report, inspect an example, open a deck, or follow the notebook instructions without prior context. Participant progress is separate: projects in the facilitator roster publish completed checkpoints. Missing updates mean unknown. We do not join anonymous visits to participant identities. For a pilot, also ask what people tried, where they got stuck, and what helped.

## 00:09:20–00:10:00 · Choose one example to try

**00:09:20–00:09:40 — Show:** Choose a relevant workshop.

The useful output is a result someone can explain, its code, and a Forge record another person can check. Notebooks hold the implementation. Agent Lens exposes behavior. Runs and Sweeps compare experiments. Artifacts preserve files. EvalTables aligns cases. Reports explain what the evidence supports.

**00:09:40–00:10:00 — Show:** The public notebook start page and setup instructions.

Choose a situation that resembles your work. Read its Report, use a short demo, or copy or download the notebook and try an exercise. The accompanying link opens the materials and running instructions. Feedback on confusing setup or explanations, and partners for a full rehearsal, would help.

## Link accompanying the recording

External video viewers: https://utm.io/uuIan. External community Slack: https://utm.io/uuIaS. Internal reviews: https://ash0ts.github.io/forge-workshop-kit/. Link visits measure entry paths, not notebook copies or completion.
