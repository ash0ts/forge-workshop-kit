# Investigate a result with ARIA

Each workshop includes two short investigations. First inspect the result yourself and explain what you think happened. Then ask ARIA to examine the selected records and check one claim in its answer. You can disagree with the answer or conclude that the evidence is insufficient.

The first investigation takes eight minutes and uses development or validation records. The second takes seven minutes after the comparison is frozen and before publishing the Report. These replace existing discussion time; they add no training or model calls to the measured experiment.

## Use the investigation card

1. Select the case and versions beside the result. Keep your interpretation brief: what happened, and which observation supports it?
2. Write **My explanation before asking ARIA**, then click **Start ARIA investigation**. The notebook sends one question using your Forge login and the selected project. Run and Agent Lens conversation references are attached as native context. Exact artifact-version links and a bounded saved excerpt remain in the question.
3. Click **Open ARIA conversation** in the receipt. This opens the same conversation in Forge, with its selected context, progress, and follow-up composer. ARIA keeps working after the notebook action returns, so you can inspect the evidence while waiting. The conversation can be returned to the Forge drawer using its native control.
4. Use **Check ARIA response** to read the saved turn back into the notebook. Partial text stays labeled partial until the service reports completion. If ARIA asks a question or requests permission, respond in the native conversation.
5. Read the answer and open one cited record. Find the exact event, value, prediction, or changed line. Does it support the claim, contradict it, or leave the question unresolved?
6. Enter the claim and checked source, then click **Save citation check**. The direct request's exact prompt and conversation link join the note. It saves locally and enters the next normal checkpoint.

A second Start click for the same selected evidence reuses the saved request. Change the question by continuing its native conversation. Opening, navigating, editing, restoring, and saving a note never send a message. There is no automatic preload on notebook startup. The explicit Start action begins asynchronous preparation while participants continue inspecting their result.

**Copy investigation prompt for the manual path** remains available when direct access is unavailable. Open Ask ARIA in Forge, select the right project, and send the question yourself. Native run and conversation attachments are different from pasted `@run-name` text. A reference or pasted URL does not prove that ARIA read its contents: inspect its answer, cited records, and tool activity.

The notebook's agent still proposes or executes the changes being measured. ARIA's answer is not an accepted label, score, approved lesson, or release decision. [Native context instructions](https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation)

## Request and recovery contract

The small [direct client](../src/forge_workshop_kit/aria_client.py) uses the public ARIA turn API. Its request shape was checked against [W&B's MCP client at revision 7a1f9f6](https://github.com/wandb/wandb-mcp-server/blob/7a1f9f629d4977d41d31b7b84a1227bc9da2cb90/src/wandb_mcp_server/mcp_tools/aria.py) and the [published OpenAPI schema](https://wb-agent.wandb.ai/openapi.json). Participants do not install an MCP server.

Before sending, the client verifies the existing evidence allowlist and saves the question, project, workspace, selected records, and a submission receipt locally. The returned turn and conversation identities are saved immediately. Checks use GET on that turn; they never create another turn. Naming the conversation is a separate operation after the handle is saved, so a naming failure cannot discard a successful request.

The receipt lives in the existing draft store and travels with later checkpoints. It does not alter stage inputs, execution fingerprints, the notebook inference ledger, or completed-work status. ARIA charges follow the organization's account settings and are not included in that inference ledger.

| Saved state | Next action |
| --- | --- |
| Queued or in progress | Open the same conversation or click Check ARIA response. |
| Completed | Check one claim; continue questions in the same native conversation. |
| Authentication or access rejected | Fix access, then explicitly click Start again, or use the recording. |
| Check failed after a handle was saved | Retry Check. The request and handle remain saved. |
| Submission outcome unknown or interrupted | Inspect ARIA history. Do not blindly resend; the notebook blocks a duplicate submission. |
| ARIA errored or cancelled | Inspect its native conversation and use the recorded activity if needed. |

Requests use bounded timeouts and response sizes, do not follow redirects with credentials, and never save authentication headers or raw transport exceptions. Native attachments are context selection, not a security boundary. The question asks for analysis only; it does not grant new permissions or change the account's existing ARIA capabilities.

## Keep the question tied to the current decision

| Workshop | Investigate this result | Check our conclusion |
|---|---|---|
| Pending | After the starting development evaluation, check the account outcome and whether the run actually read the skill. | Separate different tool behavior from different account correctness across the three frozen harnesses. |
| Solar | After writing your GOES diagnosis, compare the selected validation forecast, loss history, settings, normalization, and persistence. | Review the measurement and image conclusions separately, including regressions and the limits of teaching retests. |
| Routing | Inspect the TF–IDF prediction for a validation request before introducing embeddings. | Separate classifier quality from the label-order defect, repair, and rollback. |
| Inspection | Investigate a whole-image validation error before implementing patch features. | Compare recovered defects, new misses, false alarms, and additional labeling effort. |
| Transit | Inspect both integrated builds' public development checks before proposing a project lesson. | Review scenario correctness, coordination costs, and what the accepted lesson actually changed. |
| Airline | Save your own turn review before using ARIA to challenge it or calibrating the tag. | Separate booking correctness from monitor agreement, coverage, and unavailable judgments. |

For the first investigation, use only the selected development or validation records. Do not attach the complete journal, final comparison, worked repair, or final rehearsal Report. Attachments guide context selection; they do not restrict ARIA's access to the rest of your project. If the answer uses reserved results, exclude it from development decisions and record why.

At the closing stop, keep the frozen versions fixed. Ask for one future test rather than launching it. If a live run succeeded, keep that result; use a labeled recorded incident when you need to discuss a failure.

## Access, billing, and the recording

Live ARIA requires a supported Multi-tenant Cloud team project with Smart features enabled. A successful notebook write or trace check does not establish ARIA access. Personal-project participants can complete the workshop using **Use the recorded investigation**. Do not move participant work into a facilitator's project or share credentials to enable this activity. [ARIA requirements](https://docs.coreweave.com/products/aria)

The notebook's adjustable $8 inference allowance does not cap ARIA usage. ARIA follows the participant's organization settings, and notebook compute is billed separately. This exercise requests analysis only. It does not launch experiments, create automations, update project memory, or change code.

If access fails, or the answer does not arrive within the activity's timebox, use the recording. It contains the instructor's actual question, selected records, response, captures, and citation check. Its results are not attributed to your unexecuted edits. Keep your live question if you want to return to it later.

Shared ARIA conversations are organization-scoped and still require access to the underlying project. The bundled transcript and captures provide the teaching fallback independently of those permissions. An absent recording or failed response is shown as unavailable, never replaced with a fabricated answer. [Conversation sharing](https://docs.coreweave.com/products/aria/chat#share-a-conversation)

## Facilitate the two stops

For the eight-minute development stop, allow two minutes to inspect and explain, two to start ARIA and open the conversation, and four to check one claim. For the seven-minute closing stop, use one minute for the draft conclusion, two for ARIA, and four for verification and the next question. Switch to the recording when needed rather than extending the session.

Ask what ARIA added to the participant's interpretation. It may identify a useful event, challenge an assumption, or fail to answer. An answer that sounds plausible does not establish causation. A successful tool call does not establish task correctness, and fewer alerts do not establish a better monitor.

The facilitator sees whether the activity used live ARIA or the recording, whether a citation was checked, and whether help was requested. Missing notes mean not recorded. The monitor does not grade agreement with ARIA or retrieve private chat contents. The Report can include a short participant-written account of what they accepted or disputed and the checked evidence link.

The [direct-call qualification](aria-direct-qualification.md) records the native attachment and same-conversation check, including what remains unverified.
