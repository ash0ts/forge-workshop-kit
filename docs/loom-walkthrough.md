# Ten-minute Loom walkthrough

Use this script to introduce the collection to people who have not heard about the workshops. The recording follows one concrete problem per workshop and shows where someone would investigate it in Forge. Allow time for the viewer to read each screen; the timestamps include those pauses.

## Prepare the recording

- Open the [public packet](https://ash0ts.github.io/forge-workshop-kit/packet/), [sharing page](https://ash0ts.github.io/forge-workshop-kit/share/), and [facilitator start guide](facilitator-start.md).
- Preload each workshop's public learning Report from the packet. Use the figures and recorded native captures already in those Reports. For live product navigation, the [demo guide](current-demo-guide.md) provides the exact trace, run, artifact, and comparison links.
- Open Pending's [recorded ARIA conclusion activity](https://ash0ts.github.io/forge-workshop-kit/pending/aria-conclusion/). Keep its cited run available.
- Use a clean browser view without credentials, private project names, or notifications. Check that the text is readable at the recording size.
- Show saved evidence. Do not start training, inference, tag judging, or an ARIA conversation while recording. If a view is unavailable, show its labeled capture and state that it is recorded.

The [recorded-results guide](recorded-results.md) owns the exact scores and qualifications. This tour explains the workflow; it does not replace an evidence review or qualify a full class.

## 0:00–0:50 · Why we made this

**Show:** the packet's six workshop cards.

I’ve been building hands-on workshops for engineers learning to use Forge on problems they might encounter at work.

A refund agent can call the right API and still change the wrong account. A forecast can have a promising score that nobody can reproduce. Two coding agents can finish their tasks and leave you with an application that doesn't work.

We use those situations to teach the work around an AI application: run it, observe what happened, curate examples worth examining, make a change, and evaluate the result. Participants follow that sequence in Python and inspect the records in Forge. I'll show the six examples and how to use the material.

## 0:50–1:30 · What someone can use

**Show:** one card's Report, deck, notebook, and running-guide links. Open its notebook copy control without creating a copy.

Each workshop has an illustrated Report you can read first, a deck for teaching, recorded results for demonstrations, and an editable notebook. The notebook uses the participant’s own project and credentials. The facilitator reads progress from projects people choose to share.

Use one example in a customer conversation, a short demo, or a hands-on pilot. The setup is shared across the collection, and participant code stays visible. There’s no workshop gateway.

## 1:30–2:25 · Pending: change an agent's behavior

**Show:** Pending's ticket, tool-call diagram, and checked account. Then its Agent Lens capture.

Pending is a fictional office handling billing and account access. A customer has been charged twice. The agent needs to find the payment, refund it, and check the account.

Participants build the tools and the code that passes observations back to the model. In Agent Lens, they follow the arguments, returned payment, and next action. Then they edit the instructions and test manual and agent-written harness changes.

The timeout exercise shows a specific repair: a write committed before its response timed out. Reusing the operation ID and checking the account avoids adding a second membership. The later harness comparison tied. We keep those results separate because an extra tool call doesn't automatically mean a better customer outcome.

## 2:25–3:25 · Solar: test research changes

**Show:** the aligned solar images, a learning curve or Sweep, then the recorded code diff and saved weights.

Solar puts you in a lab preparing a forecast review. The observations are real GOES measurements and AIA solar images. Participants start with persistence: predict that the latest observation will remain unchanged.

They train small models, record the settings and loss curves in runs, and use a Sweep to compare existing configurations. Artifacts keep the data, source, trained weights, and predictions together so someone can reproduce a forecast.

Then a research agent proposes code changes. Participants read the diffs, train the candidates, and compare matching observations. The language model stays fixed; the forecasting weights are trained normally. This is a bounded autoresearch exercise. The saved results include a failed measurement recipe and mixed image outcomes across seeds, so the conclusion needs more care than “the agent improved it.”

## 3:25–4:20 · Routing: improve and release a model

**Show:** a Banking77 request, classifier comparison, and the label-mapping drill.

Routing starts with a banking support queue. A card that hasn't arrived needs a different workflow from a card that doesn't work. Participants compare text representations, inspect mistakes, and distinguish a proposed label from one a person has reviewed.

Runs track the classifier comparisons; EvalTables align the same requests so you can inspect the predictions. Artifacts preserve the preprocessing, model, and intent order.

The release exercise deliberately loads those intent names in the wrong order. The probabilities still look confident, but the requests go to the wrong queues. Participants write a regression check, repair the loader, and roll back to the previous version. The release target is a notebook batch predictor. It teaches a concrete failure that aggregate model scores alone would miss.

## 4:20–5:15 · Inspection: find the mistakes an average hides

**Show:** a real PCB photograph, its inspection mask, and the before-and-after predictions for a recovered and a new miss.

Inspection is a manufacturing problem: which circuit boards need attention before they leave the line? We use real VisA photographs and compare whole-image features with local patch features.

Participants examine a missed defect before changing the representation. Then they compare misses, false alarms, and the amount of human review. Supplied masks help us inspect the board; they aren't inputs to the classifier.

The data-selection exercise compares active and random review with the same labeling budget. More labels can help without proving that the selection method was better. Forge keeps the images, outputs, reviewed data, and model versions connected. Showing one corrected miss beside a new mistake makes that tradeoff visible.

## 5:15–6:10 · Transit: coordinate coding agents

**Show:** the departure board, task dependencies, worker timeline, and integrated test results.

Transit is the software-factory example. Coding agents build a departure board from a historical MBTA schedule. Times after midnight give the components a real integration problem: a service time above twenty-four hours still belongs to the original service day.

Participants implement task claims, file ownership, and patch integration. Agent Lens shows what each worker read, edited, and tested. Artifacts preserve the code and the release being evaluated.

They also compare a later build with and without a verified lesson. A worker reading a note is evidence of retrieval; the application checks tell us whether it helped. The recorded team did worse on two checks, and the follow-up did not establish a memory advantage. Those outcomes are part of the coordination lesson.

## 6:10–7:10 · Airline: turn observed behavior into tests

**Show:** the requested itinerary change, the untouched return flight, a trace, and the curated regression case.

Airline connects monitoring to offline evaluation. These are simulated benchmark bookings. A passenger wants to change one part of a round trip, but the update API replaces the entire itinerary. Omitting the unchanged return flight can remove it while the tool call succeeds.

Participants inspect a conversation, review the booking outcome, define a monitoring rule, and turn reviewed incidents into regression cases. The native activities use Agent Lens conversations, Insights, Tags, and Alignment. They then compare the original and repaired code on matching requests in EvalTables.

This workshop still needs native-feature qualification: the last AI Alignment checks failed, and prepared Insights are not qualified. The live agent passed the recorded requests. A separately labeled controlled example teaches the itinerary defect without inventing a spontaneous agent failure.

## 7:10–8:00 · Where ARIA fits

**Show:** Pending's recorded ARIA response, then the cited final-comparison record.

ARIA joins after participants have looked at a result and written down what they think happened. They select the relevant records, ask a specific question, then open a citation and decide whether the answer is supported.

Here, the question is whether different tool behavior improved account correctness. The saved comparison shows a tie. ARIA helps investigate the interpretation; it doesn't become the grader or automatically edit the code.

Across the workshops, Notebooks hold the implementation, Agent Lens explains execution, runs and Sweeps compare experiments, Artifacts preserve files, and EvalTables align cases. The final Report states what changed and what the evidence supports. Each product answers a question about the work we just did.

## 8:00–9:20 · How we share and measure usage

**Show:** the sharing page, one QR destination, then the facilitator guide's progress section. Do not expose UTM.io administration or private rosters.

The packet is the entry point. Someone can read an example without signing in, then choose the deck, running guide, or notebook. The QR codes use registered UTM.io links, so printed materials can continue pointing to the current workshop page.

The workshop links identify which workshop brought someone in. We use the same workshop code in its deck and poster, so those links don't distinguish a slide scan from a poster scan. Slack and this video have separate registered links. Their source and medium tags distinguish those entry paths.

There are two different measures here. Link visits tell us about the entry path. They don't prove someone copied a notebook or finished an exercise, and our own checks and link previews can create visits.

Participant progress comes from published notebook checkpoints in the facilitator’s project roster. Missing updates mean unknown. Anonymous clicks aren’t joined to participant identities or a completion funnel.

For a pilot, I want the practical feedback too: which problem brought someone in, which exercise they tried, and where they needed help. The facilitator guides explain how to collect that without asking for credentials.

## 9:20–10:00 · What to try next

**Show:** the packet and the selected workshop's running guide.

The Reports, decks, and recorded demonstrations are available to use now. The full sessions are technical previews; external-account and participant rehearsals are still open.

Pick one problem that resembles your team's work or a customer conversation. Read its Report, use the short demo, or copy the notebook and try one exercise. I'd like feedback on the point where the explanation or setup stops being clear, and partners for rehearsing a full session.

The link with this recording opens the packet, with the materials and instructions together.

## Description and link placement

Suggested description:

> Six hands-on Forge workshops, from agent debugging and research experiments to model release, coding-agent coordination, and monitoring. This tour shows the customer problem, the code participants change, and the Forge record they inspect. Start with one example or try an exercise in your own project. Full sessions remain technical previews.

Use **https://utm.io/uuIan** in the Loom description. This is the registered video link: `utm_source=loom`, `utm_medium=video`, and `utm_content=kit-walkthrough`. The Slack link remains https://utm.io/uuIac. The [sharing guide](share-links.md) owns the tracking definitions and placement instructions. Keep a direct link to [current readiness](../next-up.md) alongside the packet.

No recording is bundled with this script. Add the actual Loom URL to the sharing materials after recording and checking its public viewing permissions.
