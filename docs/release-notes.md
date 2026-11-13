# Forge Workshop Kit 0.2.0 technical preview

The Solar workshop now has a browser deck and PDF, with incremental diagrams, real experiment screens, exact exercise instructions and optional worked answers. Its visual language follows the Pending, Inc. workshop: cream, teal, IBM Plex and a research team whose paperwork has not kept up with its optimism.

Both notebooks now use the same sequence: write code, check it locally, run explicitly, inspect the result, and follow the evidence into Forge. A numbered navigator shows the current step. Prerequisites link back to the required exercise. Drafts, completed runs, selected versions and evidence links survive reopening.

Pending restores exercises for the invoice tool, tool dispatch, observation handoff, tracing, state scorer, explanation judge and improvement controller. Solar separates measurement and image code, adds bounded starter gaps and local checks, and guides each candidate through review, testing, composition and adoption. The branch view keeps rejected and unchanged versions visible.

Browser rehearsal found and repaired two integration problems that standalone scripts missed: local MCP and Weave evaluation needed an event-loop bridge inside marimo, and native Sweep runs needed separation from checkpoint publication. Saved work is reused after recovery. Export and publication retries do not repeat inference or training.

The notebooks use the participant's own project and account. There is no workshop gateway or host token. The $8 inference allowance remains adjustable, and notebook compute is billed separately. Prior releases and attendee copies are unchanged.

Native EvalTables still returns HTTP 500. Weave and notebook comparisons remain available, with the publication status shown explicitly. External-attendee verification and a human usability rehearsal remain before classroom-ready status. See [release checks](release-checks.md) for current evidence and limits.
