# Copy the notebook and start

1. Sign in to [Forge](https://forge.coreweave.com) and create a teaching project in your own account or a team where you can write. Use public projects if the facilitator needs to read progress without an invitation. Files published there are public, so use the workshop data.
2. Choose a template from the [workshop list](../README.md#choose-your-workshop), choose **Copy to project**, and select your project. Open the editable copy. If copying is unavailable, import the corresponding `.py` file from [notebooks](../notebooks) into your project.
3. Initialize the cells with marimo’s **Run all stale cells** control. This creates the exercise controls. It does not press their Run buttons. Inspect the opening example before connecting: identify the request, the supplied data, and what should happen. Recorded examples are labeled and do not reflect your unexecuted edits.
4. Check the displayed project. An editable hosted copy reads its project and credentials from Forge. Click **Connect and restore my work** in Solar, routing, or transit, **Check my project and restore saved work** in Pending, or **Connect and restore my inspection work** in inspection. Airline's setup step also checks the project before you instrument and send its first trace.
5. Complete the first tracing exercise and open its Agent Lens conversation. Send the facilitator your project link if you want them to see progress and help requests. They do not need your credentials.

If a template link sends you to Forge Home, sign in and reopen the link. If the Notebooks application also redirects or is unavailable, use the workshop's start page in the [public library](https://ash0ts.github.io/forge-workshop-kit/). It provides a direct `.py` download and laptop commands. Import the file if your project offers notebook import; otherwise follow **Work locally** below. A template link does not grant product or compute access. Reading the Report, deck, and recorded example needs no notebook runtime.

The November 16 browser check reproduced a redirect from the Solar template and from Forge's own Notebooks launcher. The fallback is available, but this check does not establish that hosted copying works for a fresh attendee account.

The setup table separates project writes, stored traces, inference, Weave evaluations, and native EvalTables. A successful project check does not establish access to all five. The check makes no model calls. Your first explicit model run checks inference access and billing; your first evaluation publication checks the evaluation services.

The default inference allowance is $8 for this workspace. Change it during setup if needed. It counts retries and reserves a maximum for requests whose usage is unknown. Notebook compute is billed separately. No workshop gateway, host token, or remote Sandbox entitlement is required.

## Use ARIA during the investigations

Each workshop pauses twice to ask ARIA about selected saved results and check a citation. Click **Start ARIA investigation**, then **Open ARIA conversation** to continue in Forge. **Check ARIA response** retrieves the saved answer without starting another request. Live access requires a supported team project with Smart features; personal-project participants use the bundled recorded investigation. A successful project check does not prove ARIA access. ARIA usage is separate from the notebook’s $8 inference allowance. Follow the [investigation instructions](aria-investigations.md) for native attachments, billing, and the no-access path. No ARIA activity blocks the coding exercises.

## Work locally

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/), then clone this repository. Install the dependencies for your workshop:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra pending
uv run --extra pending wandb login
uv run --extra pending marimo edit notebooks/pending_inc.py
```

Choose the extra and notebook below. Replace the `pending` value after `--extra` in each uv command, and replace `notebooks/pending_inc.py` with your workshop's notebook path. For “none,” omit `--extra pending` entirely.

| Workshop | Dependency extra | Notebook |
| --- | --- | --- |
| Pending | `pending` | `notebooks/pending_inc.py` |
| Solar | `solar` | `notebooks/solar_autoresearch.py` |
| Routing | `routing` | `notebooks/request_routing.py` |
| Inspection | `inspection` | `notebooks/visual_inspection.py` |
| Transit | none | `notebooks/transit_factory.py` |
| Airline | none | `notebooks/airline_monitoring.py` |
| Starter / facilitator | none | `notebooks/starter.py` / `notebooks/facilitator.py` |

Use Python 3.11–3.13. Enter your writable `entity/project` in the setup step, or set `WORKSHOP_PROJECT` before launching. Tools and training run in the notebook’s Python runtime. Inference and publication use your Forge credentials. The first command installs the shared dependencies plus only the selected workshop’s stack.

Solar, Routing, and Inspection download checksum-verified teaching bundles through explicit controls. Their required training runs on CPU. Pending’s office simulator, Transit’s historical schedule subset, and Airline’s fictional bookings are included. None requires a live customer or transit service. The required Inspection path makes no model API requests; the other workshops use inference for their agent or judge exercises.

For Airline’s native monitoring access, read the [qualification record](airline-monitoring-qualification.md). Tag configuration and manual labels were verified, but the last AI Alignment tests returned HTTP 500 and the prepared Insights activity remains unqualified. Keep those results unavailable rather than treating them as successful negatives.

Native Agent Lens automatic tag judging has separate billing outside the $8 notebook inference allowance. After the exercise, disable **Apply with AI** on the workshop tag and use the notebook's **Verify automatic tagging is off** control. Read-only tag-result checks do not repeat the airline conversations. Explicit Alignment tests can incur new judging charges; a failed test is not an incorrect booking.

## Resume or recover

Reopen the same notebook copy and connect. Drafts and completed results restore from the local workspace or its last uploaded checkpoint. Keep the `.workshop/` directory on a laptop. Before discarding a hosted runtime, confirm its checkpoint uploaded.

If a run stopped, open **A run stopped? Review recovery** beside the step navigation and click **Check for stopped or failed work**. Read the saved error, select the affected execution, and click **Allow retry of this failed execution**. Then return to the step’s normal Run button. Authorizing a retry does not start work. Completed matching executions are reused.

If an earlier process or provider request may still be running, stop that process before checking the confirmation box. Unresolved provider usage remains charged at its reserved maximum. A fresh attempt can incur another charge.

If the work completed but an upload failed, use the final comparison’s **Retry publication** control instead. It reuses saved results. Native EvalTables may be unavailable while the notebook comparison and Weave records are available; the publication table shows each separately.

## Read participant progress

Open the [facilitator monitor](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view), add one public project link per line, choose the workshop, and click **Save roster and filters**. Then click **Refresh progress**. The roster is saved in the monitor’s runtime under `.workshop/facilitator/roster.json`; keep or download that file if replacing the runtime.

Each notebook workspace has its own row. Optional UTC date filters use the last published update. Workspace and notebook-copy filters accept exact IDs from the rows. Older progress runs may lack a notebook-copy ID. Leave that filter empty to include them.

Automatic refresh is off until you enable it. The monitor reads several projects concurrently and shows its refresh time separately from each participant’s last update. An absent update is **unknown**. A read error is **unavailable**. Neither means the participant’s experiment failed, and the monitor cannot start or block their work.
