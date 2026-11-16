# Present and share the workshops

Use the packet to introduce the work, show one recorded example, or invite someone to try an exercise. Each workshop connects a customer or engineering problem to code, a measured outcome, and a specific investigation in Forge. The full sessions remain technical previews; external-account checks and participant rehearsals are still open.

[Open the workshop materials](https://ash0ts.github.io/forge-workshop-kit/packet/) · [Choose a workflow](use-the-workshops.md#choose-the-workflow) · [Watch the ten-minute tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) · [Dubbing script](loom-walkthrough.md) · [Sharing links and tracking](share-links.md)

## A one-minute introduction

I've been building six hands-on workshops for engineers learning how to use Forge in their own work. Each starts with a recognizable problem: an agent needs to refund the right payment, a research team needs to reproduce a forecast, or two coding agents need to deliver one working app.

Participants write Python, inspect the output, make a change, and check whether it helped. They use Forge to follow agent calls, compare training runs, review individual mistakes, and recover the exact code and data behind a result. The examples connect running an application to observing it, curating cases, improving the implementation, and evaluating the change.

Each has an illustrated Report, a deck, recorded results, and a notebook you can run locally and connect to your own Forge project. You can read an example, borrow a short demo, or run a hands-on pilot. I'd like people to try one exercise and tell me where they get stuck or which customer workflow it resembles.

## A ten-minute meeting

| Time | Show | Say or ask |
| --- | --- | --- |
| 0–1 min | The introduction above | Explain who the material is for and what someone can do with it. |
| 1–2 min | The six choices in the packet | Pick one problem relevant to the audience. |
| 2–7 min | One recorded example from the [demo guide](current-demo-guide.md) | Follow one input, a code change, and its output. Identify the recorded execution. |
| 7–9 min | The linked Forge record or its labeled capture | Ask what the result establishes and what remains uncertain. |
| 9–10 min | The notebook link and [setup guide](setup.md) | Ask someone to try the first exercise and report the step where they needed help. |

For a recording that introduces all six workshops, use the separate [ten-minute Loom script](loom-walkthrough.md). It includes the screen sequence, product connections, and tracking explanation.

For a first Agent Lens demonstration, use Pending's refund or timeout. For ML engineers, use a Solar forecast or an Inspection miss. Routing suits a release discussion; Transit suits agent coordination. Airline connects observed behavior to regression cases, using recorded material for its unqualified native monitoring activities.

Use PDFs if a live page is unavailable. Keep captures labeled as recorded. A meeting demonstration does not require training, inference, a live ARIA chat, or automatic tag judging. The [demo guide](current-demo-guide.md) provides the exact records and questions.

## Slack drafts

Start in [#cw-forge](https://coreweave.slack.com/archives/C0BPLUVQM4K). Use the narrower messages below for a concrete review request; do not post the same announcement to every channel. These drafts assume the reader has never heard of Workshop Kit. Internal reviews use direct links, so they do not inflate external campaign traffic.

### Product introduction in #cw-forge

I've been building a set of hands-on examples to answer a question we keep getting about Forge: what would I use the different products for in my own work?

There are six workshops, grouped around three kinds of work:

- **Making agents reliable:** handle a refund without corrupting an account; investigate a booking mistake and turn it into a monitoring rule and regression test.
- **Improving and releasing models:** test changes to a solar forecast; catch small defects in circuit boards; release a request classifier and repair a broken label mapping.
- **Coordinating coding agents:** have two workers build a departure board, integrate their patches, and test whether a shared lesson helps the next build.

People edit Python and inspect what happened. Agent Lens shows the calls and failures, runs and Artifacts preserve experiments, EvalTables aligns outcomes, and ARIA helps investigate selected records. The examples use public data or simulated tasks, with the ties and regressions left in.

[Ten-minute narrated tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) · [Reports, decks, exercises, and facilitator guides](https://ash0ts.github.io/forge-workshop-kit/)

I'd like feedback on which example fits a customer conversation and where the explanation loses you. These are technical previews. Local notebook downloads are available; hosted notebook copying is currently blocked by Forge access and is the next fix.

### Pilot request in #devrel-team-and-friends

I've put together six Forge workshops that start with a concrete engineering problem and follow it through code, a result, and an investigation in the product. They cover agent reliability, model development and release, and coordinated coding agents.

Each has an illustrated Report for reading, a short recorded example for demos, and a deck plus editable Python notebook for a hands-on session. The kit also has facilitator runbooks, free checks, saved progress, and publication retries so people don't have to repeat completed model calls.

[Watch the tour](https://ash0ts.github.io/forge-workshop-kit/walkthrough/) · [Choose an example](https://ash0ts.github.io/forge-workshop-kit/)

Could someone try one exercise with me and flag where they'd need help? I'd also like to know which scenario matches questions you're getting from developers. Local notebooks are available; hosted copying needs an access fix. Fresh-account and participant rehearsals are still open, so I'm looking for pilots rather than announcing finished classes.

### Training review in #wg-ailoop-training

I've built a collection we could use for Forge training. Each workshop follows a specific task, such as preserving a passenger's return flight or reproducing a trained forecast, and shows when to use traces, experiment runs, saved artifacts, and aligned evaluations.

The materials support a short demo, a reading assignment, or a longer Python exercise. There are six decks, Reports, notebooks, and facilitator schedules, plus a [ten-minute overview](https://ash0ts.github.io/forge-workshop-kit/walkthrough/).

I'd like someone to pick a workflow and review whether the product handoffs make sense for a new user. [Materials are here](https://ash0ts.github.io/forge-workshop-kit/). The full classes remain previews; hosted copying and external-account rehearsals still need work.

### Video review in #devrel-content-review

Could I get a review of this [ten-minute Forge walkthrough](https://ash0ts.github.io/forge-workshop-kit/walkthrough/)? It introduces six hands-on examples using the actual notebook, trace, experiment, and evaluation screens. The narration uses ElevenLabs; captions and the transcript are included.

I'm most interested in whether the first minute explains why someone would use this, whether the code and screens are readable, and whether the product transitions are clear without knowing the workshops already. The video links to the Reports, decks, and local exercises; hosted notebook copying is still awaiting an access fix.

### Access follow-up in #coreweave-notebooks-triage

Could someone help check Notebook management access for `ashah1`? Our six Workshop Kit templates used to open. The current API key authenticates, but all six notebook lookups now return HTTP 403: `Marimo notebook management is not enabled`. In the browser under the `wandb` team, the template redirects to Home and the Notebooks launcher redirects to the Forge root.

[One affected template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) · [Verification details](notebook-copy-check-v0120.json)

We haven't changed or deleted the templates. Current source and free checks pass. Read-only replay loads saved results without changing them, including recorded failures. The access error blocks updating and verifying the hosted copy flow. Could you check the account entitlement and what changed? I'll resume publication and test a fresh copy once access is restored.

The channel selection was checked against recent discussions on November 16, 2026. The [developer-research summary in #cw-forge](https://coreweave.slack.com/archives/C0BPLUVQM4K/p1794594168479379) describes uncertainty about how Forge's products fit together and requests for proof on a developer's own work. That is the reason to lead with a task and a concrete investigation. The messages above have not been sent.

## Follow-up for a technical pilot

Pick the project closest to your work and open its notebook from the packet. Save the downloaded file in a folder, follow its login and local launch commands, then initialize the controls and enter your Forge project. Complete the access check and first exercise. You use your own credentials; the facilitator only reads progress you share.

Please send the workshop name, step, expected result, and what happened. Leave keys and tokens out. The [setup guide](setup.md) explains access, local execution, and recovery. The $8 notebook inference allowance is adjustable; notebook compute, ARIA, and native tag judging are billed separately.

Use the [untracked library link](https://ash0ts.github.io/forge-workshop-kit/) for coworker Slack messages, the [video link](https://utm.io/uuIan) for the Loom description, and a workshop-specific link for an invitation to one session. The [sharing guide](share-links.md#how-tracking-works) explains which placements the links identify and why visits are separate from notebook progress.

## What is ready to show

The decks, PDFs, diagrams, public learning Reports, and recorded examples are available for reading and recorded demonstrations. Local checks and maintainer rehearsals cover implementation behavior. They do not establish that every new account can complete a full class.

Use the current website download for the revised explanations and direct ARIA controls. The hosted templates remain v0.11.1 while Forge notebook-management access blocks their update. The notebook start pages give the saved-file download and local launch commands; do not present the hosted refresh as complete.

Before scheduling a hands-on class, finish the external-account and human checks in [current status](../next-up.md). Airline's AI Alignment and prepared Insights activities remain unqualified. ARIA recordings support the investigation when live access is unavailable. In Airline, disable **Apply with AI** when a live tagging activity ends; closing the notebook does not turn off automatic judging.

Keep claims tied to the [recorded outcomes](recorded-results.md). Pending's harness comparison tied, Solar includes a failed measurement recipe and an image-seed regression, Transit did not establish a team or memory advantage, and both live Airline versions passed. The controlled repair exercises are separate from those comparisons.

The participant download includes a workshop guide, all six deck PDFs, editable notebooks, and setup and facilitator instructions. These message drafts and the recording script stay in Git; they are not part of the participant website. Previous releases and attendee copies remain unchanged.

## Public distribution

Internal reviews use the untracked library URL above. When sharing with prospective participants in an external Slack community, use [the public community link](https://utm.io/uuIaS). Its UTM campaign measures incoming visits, not coworker enablement, copied notebooks, or completion. See [tracking conventions](share-links.md).
