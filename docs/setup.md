# Copy the notebook and start

1. Sign in to [Forge](https://forge.coreweave.com) and create a teaching project in your own account or a team where you can write. Use public projects if the facilitator needs to read progress without an invitation. Files published there are public, so use the workshop data.
2. Open the [Pending template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) or [Solar template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view), choose **Copy to project**, and select your project. Open the editable copy. If copying is unavailable, import the corresponding `.py` file from [notebooks](../notebooks) into your project.
3. Initialize the cells with marimo’s **Run all stale cells** control. This creates the exercise controls. It does not press their Run buttons.
4. Check the displayed project. An editable hosted copy reads its project and credentials from Forge. Click **Connect and restore my work** in Solar or **Check my project and restore saved work** in Pending.
5. Complete the first tracing exercise and open its Agent Lens conversation. Send the facilitator your project link if you want them to see progress and help requests. They do not need your credentials.

The setup table separates project writes, stored traces, inference, Weave evaluations, and native EvalTables. A successful project check does not establish access to all five. The check makes no model calls. Your first explicit model run checks inference access and billing; your first evaluation publication checks the evaluation services.

The default inference allowance is $8 for this workspace. Change it during setup if needed. It counts retries and reserves a maximum for requests whose usage is unknown. Notebook compute is billed separately. No workshop gateway, host token, or remote Sandbox entitlement is required.

## Work locally

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/), then clone this repository. Install the dependencies for your workshop:

```sh
git clone https://github.com/ash0ts/forge-workshop-kit.git
cd forge-workshop-kit
uv sync --frozen --extra pending
uv run --extra pending wandb login
uv run --extra pending marimo edit notebooks/pending_inc.py
```

For Solar, use `--extra solar` in all three uv commands and open `notebooks/solar_autoresearch.py` instead. Enter your writable `entity/project` in the setup step. You can also set `WORKSHOP_PROJECT` before launching. Tools and training run in the notebook’s Python runtime. Inference and publication use your own Forge credentials.

## Resume or recover

Reopen the same notebook copy and connect. Drafts and completed results restore from the local workspace or its last uploaded checkpoint. Keep the `.workshop/` directory on a laptop. Before discarding a hosted runtime, confirm its checkpoint uploaded.

If a run stopped, open **A run stopped? Review recovery** beside the step navigation and click **Check for stopped or failed work**. Read the saved error, select the affected execution, and click **Allow retry of this failed execution**. Then return to the step’s normal Run button. Authorizing a retry does not start work. Completed matching executions are reused.

If an earlier process or provider request may still be running, stop that process before checking the confirmation box. Unresolved provider usage remains charged at its reserved maximum. A fresh attempt can incur another charge.

If the work completed but an upload failed, use the final comparison’s **Retry publication** control instead. It reuses saved results. Native EvalTables may be unavailable while the notebook comparison and Weave records are available; the publication table shows each separately.

## Read participant progress

Open the [facilitator monitor](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzM=/view), add one public project link per line, choose the workshop, and click **Save roster and filters**. Then click **Refresh progress**. The roster is saved in the monitor’s runtime under `.workshop/facilitator/roster.json`; keep or download that file if replacing the runtime.

Each notebook workspace has its own row. Optional UTC date filters use the last published update. Workspace and notebook-copy filters accept exact IDs from the rows. Older progress runs may lack a notebook-copy ID. Leave that filter empty to include them.

Automatic refresh is off until you enable it. The monitor reads several projects concurrently and shows its refresh time separately from each participant’s last update. An absent update is **unknown**. A read error is **unavailable**. Neither means the participant’s experiment failed, and the monitor cannot start or block their work.
