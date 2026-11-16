# Download the notebook and start

Choose a workshop in the [public library](https://ash0ts.github.io/forge-workshop-kit/). Its start page has the current `.py` notebook and the exact commands for that file. Save it in a folder you will keep; that folder also holds your local progress.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then open a terminal in that folder. For Solar, run:

```sh
uvx --from wandb==0.31.0 wandb login --host https://api.wandb.ai --verify
uvx --from marimo==0.25.2 marimo edit --sandbox solar_autoresearch.py
```

Replace `solar_autoresearch.py` with your downloaded filename. Pass the saved file, not its download URL. Here, `--sandbox` installs the notebook's pinned Python dependencies in a separate local environment; it does not create a remote Forge Sandbox.

<details>
<summary>If dependency installation reports a certificate error</summary>

On a managed laptop, uv may need to use your operating system's trusted certificates. Run `export UV_SYSTEM_CERTS=true` in macOS or Linux, or `$env:UV_SYSTEM_CERTS = "true"` in PowerShell, then repeat the launch command. This keeps certificate verification enabled. If the error continues, check your organization's Python package and certificate setup.

</details>

1. Sign in to [Forge](https://forge.coreweave.com) and create a project in your own account or a team where you can write. Use a public project if the facilitator needs to read progress without an invitation. Files published there are public, so use the workshop data.
2. In the notebook, use marimo’s **Run all stale cells** control to create the exercise controls. This does not press their Run buttons. Inspect the supplied example: identify the request, look at the data, and work out what should happen before running your own code.
3. Enter your `entity/project`. Click **Connect and restore my work** in Solar, Routing, or Transit, **Check my project and restore saved work** in Pending, or **Connect and restore my inspection work** in Inspection. Airline's setup step also checks the project before you instrument and send its first trace.
4. Complete the first tracing exercise and open its Agent Lens conversation. Send the facilitator your project link if you want them to see progress and help requests. They do not need your credentials.

Current website downloads include the latest exercise explanations and use the v0.12.0 runtime. Optional hosted templates remain on v0.11.1 while notebook-management access blocks their update. If your project supports notebook import, you can import the downloaded `.py` file there. See [current delivery status](../next-up.md) before relying on hosted copying for a class.

The setup table separates project writes, stored traces, inference, Weave evaluations, and native EvalTables. A successful project check does not establish access to all five. The check makes no model calls. Your first explicit model run checks inference access and billing; your first evaluation publication checks the evaluation services.

The default inference allowance is $8 for this workspace. Change it during setup if needed. It counts retries and reserves a maximum for requests whose usage is unknown. Local training uses your laptop’s CPU. If you import the notebook into a hosted runtime, its compute charges are separate. No workshop gateway, host token, or remote Sandbox entitlement is required.

## Use ARIA during the investigations

Use the current notebook from its start page for the direct ARIA controls. The [v0.12.0 release](https://github.com/ash0ts/forge-workshop-kit/releases/tag/v0.12.0) preserves the original release files.

Each workshop pauses twice to ask ARIA about a result you have just inspected. Write your explanation in the investigation card, then click **Start ARIA investigation**. The notebook sends that question with the selected records. Click **Open ARIA conversation** to read the answer and ask a follow-up in Forge. Open one cited record and check the claim against its actual values. **Check ARIA response** retrieves the saved answer without starting another request.

Live ARIA requires a supported team project with Smart features and has usage charges outside the notebook’s $8 inference allowance. If it is unavailable, use the bundled recorded investigation and check its cited record instead. You can continue the coding exercises either way. The [investigation instructions](aria-investigations.md) explain the context sent to ARIA, billing, and how the saved question is restored.

## Work from the repository

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/), then clone this repository. Install the dependencies for your workshop:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra pending
uv run --extra pending wandb login --host https://api.wandb.ai --verify
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

Save the [facilitator notebook source](https://raw.githubusercontent.com/ash0ts/forge-workshop-kit/main/notebooks/facilitator.py) as `facilitator.py` in a folder you will keep. Use the same login command above, then run `uvx --from marimo==0.25.2 marimo edit --sandbox facilitator.py`. Initialize the controls with **Run all stale cells**, add one public project link per line, choose the workshop, and click **Save roster and filters**. Then click **Refresh progress**. The roster is saved in the monitor’s runtime under `.workshop/facilitator/roster.json`; keep or download that file if replacing the runtime.

Each notebook workspace has its own row. Optional UTC date filters use the last published update. Workspace and notebook-copy filters accept exact IDs from the rows. Older progress runs may lack a notebook-copy ID. Leave that filter empty to include them.

Automatic refresh is off until you enable it. The monitor reads several projects concurrently and shows its refresh time separately from each participant’s last update. An absent update is **unknown**. A read error is **unavailable**. Neither means the participant’s experiment failed, and the monitor cannot start or block their work.
