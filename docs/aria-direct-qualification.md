# Direct ARIA qualification

On November 16, 2026, the notebook adapter started one ARIA investigation using a saved Routing validation result. It attached the exact training run and Agent Lens conversation, then opened the returned native conversation. No classifier training or notebook inference was repeated.

[Open the actual conversation](https://forge.coreweave.com/aria/threads/01a1e362-20ec-7b43-8473-cbf67b034ef2). The [safe receipt](aria-direct-qualification.json) preserves the selected case, context identities, actual answer, and checks performed. It excludes credentials, service configuration, and opaque tool output.

## What was checked

- The request used `wandb/forge-workshop-kit` and the existing `routing/baseline/tfidf` execution. Native run and conversation attachments appeared in ARIA.
- ARIA read the selected validation case and cited its saved execution artifact. It distinguished an uncertain top prediction withheld from automatic routing from an unproven vocabulary explanation.
- The native page offered the follow-up composer and **Return to drawer**. Opening the link continued the same conversation.
- Restarting the local notebook restored the answer. **Check ARIA response** and repeated **Start ARIA investigation** preserved the saved handle and the next exercise control.
- The shared handoff drawing fit the notebook panel. The automated client checks cover rejected authentication, ambiguous sends, stale evidence, saved successful responses, and read-only polling.

The client follows the [pinned public MCP implementation](https://github.com/wandb/wandb-mcp-server/blob/7a1f9f629d4977d41d31b7b84a1227bc9da2cb90/src/wandb_mcp_server/mcp_tools/aria.py) and the [live OpenAPI schema](https://wb-agent.wandb.ai/openapi.json), reviewed on the same date. It uses participant authentication directly; it does not install or run an MCP server.

## Limits

This check used the maintainer's enabled team account and one development investigation. It does not establish external-account access, all twelve live activities, or participant usability. ARIA's response is an interpretation to verify, not a reference label. ARIA usage is billed through organization settings outside the notebook allowance.

The [activity contract](aria-investigations.md) describes the controls, evidence boundaries, recordings, and recovery behavior.
