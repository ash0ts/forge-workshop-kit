"""Create named demo views from existing rehearsal runs. Default: print the plan.

This changes view configuration only. It never edits runs, creates evaluations,
trains a model, calls inference, or changes the project's default workspace.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import wandb
from wandb_workspaces import workspaces as ws
from wandb_workspaces.reports import v2 as panel

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "wandb/forge-workshop-kit"
BASE = "https://forge.coreweave.com/wandb/" + PROJECT
LENS = "https://forge.coreweave.com/agent-lens/" + PROJECT + "/conversations/"
COLORS = {"baseline": "#828b91", "manual": "#287e91", "agent": "#ca7924"}
SOLAR_WORKSPACE = "2d92533d2cff4e249b56748dec707b6e"
PENDING_WORKSPACE = "51a0006f750c4083b2506a997097db83"
SOLAR = {
    "5e2ee7e46e9a3ab976807a2c8b6d8a10": ("Manual residual model", "validation_error", 0.12211618815677268),
    "48984045d222b74c7636d08398fa8031": ("Round 1: zero-init head", "validation_error", 0.11143358542213977),
    "f5e5d198bc9479f78d9a4b1c8c8979e3": ("Round 2: zero-init + L1", "validation_error", 0.11091556898305115),
    "8c856d156876537764dcfcdb011296d7": ("Copy latest image", "solar-images-final/error_mean", 0.12576198700564592),
    "d1191aacb659276c00de67cd4653bb43": ("Manual image model", "solar-images-final/error_mean", 0.1224417336622075),
    "03ab9f82b09eb4106199216e99df1fce": ("Agent-selected image model", "solar-images-final/error_mean", 0.11001095193834161),
    "6a22bd3384f475b87781c40f49ad62cc": ("Copy latest GOES reading", "solar-measurements-final/error_mean", 0.19270602844340234),
    "3cc3758de39ae8a8e3afdaba625b8252": ("Selected GOES model", "solar-measurements-final/error_mean", 2.468974582071028),
}
PENDING = {
    "8fd15200fa51635dd30e76869dfd2a30": ("Starting harness", "pending-final/error_mean", 0.0),
    "f3cd39e83f9d9bf727142045e1057d90": ("Manual edit", "pending-final/error_mean", 0.0),
    "2cbedcd43422774411bfb08d91c82fcf": ("Agent-selected harness", "pending-final/error_mean", 0.0),
}


def note(markdown, height=5):
    return panel.MarkdownPanel(markdown=markdown, layout=panel.Layout(w=24, h=height))


def bar(title, metric, records, *, xlabel, xmax=None):
    return panel.BarPlot(title=title, metrics=[metric], orientation="h",
        title_x=xlabel, range_x=(0, xmax), aggregate=False, max_runs_to_show=12,
        max_bars_to_show=12, font_size="large", layout=panel.Layout(w=12, h=7),
        line_titles={f"{run_id}:{metric}": title for run_id, (title, key, _) in records.items() if key == metric})


def section(name, *panels, columns=2):
    return ws.Section(name=name, panels=list(panels), is_open=True,
        layout_settings=ws.SectionLayoutSettings(columns=columns, rows=1))


def build(kind):
    entity, project = PROJECT.split("/")
    if kind == "solar":
        records, workspace = SOLAR, SOLAR_WORKSPACE
        name = "Solar Forecasting Lab - recorded research loop"
        sections = [
            section("Start here: one recorded research loop", note(
                "## Can an agent improve the forecasting code?\n"
                "In this rehearsal, two tested edits lowered reserved-date image error by **10.15% against the manual model**. "
                "The GOES neural forecast failed to beat persistence. Both results are below.\n\n"
                "[Open the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzU=/view) · "
                f"[Six-configuration GOES Sweep]({BASE}/sweeps/pr1xsoaw) · "
                f"[Read the result]({BASE}/reports/solar-autoresearch:-2d92533d--VmlldzoxODMwMjY4OQ==)\n\n"
                "These are saved November 13 rehearsal results, not results from your notebook. "
                "One seed; two reserved dates; 199 overlapping image windows. The dates are not independent trials.", 7), columns=1),
            section("1. Validation: test the code edits before selecting a version",
                bar("Image validation error - lower is better", "validation_error", records,
                    xlabel="Mean disk-masked absolute error (standardized log1p image units)"),
                note("### Follow the selected change\n"
                     f"1. [Read the first proposal in Agent Lens]({LENS}ef590522f1af377a0bc04bd63eea23e4).\n"
                     "2. Zero-initialize the residual output layer: the model starts by copying the latest image.\n"
                     f"3. [Inspect the round-two decision]({LENS}1c8586a9e445da02a96803d435192200): use masked L1 training loss.\n"
                     f"4. [Open the adopted code, weights and losses]({BASE}/artifacts/workshop-execution/execution-f5e5d198bc9479f78d9a4b1c8c8979e3/v0).\n\n"
                     "All candidate and rejected branches remain in the notebook and linked Report. These bars show the selected sequence only.", 7)),
            section("2. Reserved image dates: did the selected model transfer?",
                bar("Final image error - lower is better", "solar-images-final/error_mean", records,
                    xlabel="Mean disk-masked absolute error (standardized log1p image units)"),
                note("### Compare the same future image\n"
                     "Copy latest image: **0.125762** · Manual: **0.122442** · Agent-selected: **0.110011**.\n\n"
                     "The agent-selected model has 10.15% lower mean error than the manual model in this one rehearsal. "
                     "Inspect individual errors before describing what improved.\n\n"
                     f"[Final prediction files]({BASE}/artifacts/workshop-execution/execution-f2175d5e34e78b67005f5a219c127949/v0) · "
                     f"[Frozen execution trace]({LENS}f2175d5e34e78b67005f5a219c127949) · "
                     f"[199 case records]({BASE}/runs/03ab9f82b09eb4106199216e99df1fce)\n\n"
                     "Native EvalTables publication was unavailable (HTTP 500). The case records are an ordinary W&B Table; Weave evaluations and notebook comparisons remain available.", 7)),
            section("3. Reserved GOES dates: the best search run still lost",
                bar("Final GOES log-flux MAE - lower is better", "solar-measurements-final/error_mean", records,
                    xlabel="Mean absolute error in log10 XRS-B flux (W/m² before log10)"),
                note("### Keep the unsuccessful forecast visible\n"
                     "Persistence: **0.192706**. Selected MLP: **2.468975**.\n\n"
                     "Winning a six-run search did not make this short-trained model useful. "
                     "The search used 60 training steps. Investigate scaling or optimization as new hypotheses; do not choose another model using these reserved dates.\n\n"
                     f"[Open the selected run]({BASE}/runs/ec725581ccce58fd968a64b40c935223) · "
                     f"[Inspect its execution]({LENS}ec725581ccce58fd968a64b40c935223)\n\n"
                     "GOES has 2,694 overlapping windows. Its scores use different units from image error and are never averaged with them.", 7)),
        ]
        pinned = ["run:displayName", "summary:validation_error", "summary:solar-images-final/error_mean", "summary:solar-measurements-final/error_mean"]
    else:
        records, workspace = PENDING, PENDING_WORKSPACE
        name = "Pending, Inc. - recorded agent comparison"
        sections = [
            section("Start here: check the work, then inspect the explanation", note(
                "## The agent retained the manual edit. That is a valid result.\n"
                "All three version labels passed all four fictional final cases. Both editor rounds retained the manual harness, "
                "so this rehearsal shows **no observed task-quality gain**.\n\n"
                "[Open the notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view) · "
                f"[Read the result]({BASE}/reports/pending-direct-teaching:-51a0006f--VmlldzoxODMwMjcxMA==)\n\n"
                "The twelve executions are three harness labels on four cases, not twelve independent problems. "
                "Manual and agent-selected use the same executable harness.", 6), columns=1),
            section("1. State checks: did the office actually change correctly?",
                bar("Final state error - 0 is correct, 1 is incorrect", "pending-final/error_mean", records,
                    xlabel="Mean state error across four cases", xmax=1),
                panel.BarPlot(title="State-check coverage - four tickets per version", metrics=["available_scores", "planned_scores"],
                    orientation="h", title_x="Tickets checked or planned (state checks only)", range_x=(0, 4), aggregate=False,
                    max_runs_to_show=3, max_bars_to_show=6, layout=panel.Layout(w=12, h=7),
                    line_titles={f"{rid}:{metric}": f"{label} · {meaning}"
                        for rid, (label, _, _) in records.items()
                        for metric, meaning in [("available_scores", "checked"), ("planned_scores", "planned")]})),
            section("2. Explanation judgments: keep unavailable separate from failure", note(
                "| Harness | State correct | Explanation passes | Unavailable explanations |\n"
                "|---|---:|---:|---:|\n| Starting | 4/4 | 3/3 available | 1 |\n"
                "| Manual edit | 4/4 | 4/4 available | 0 |\n| Agent-selected | 4/4 | 4/4 available | 0 |\n\n"
                "Available explanation judgments passed both groundedness and completion. "
                "The starting harness's two-invoices explanation hit the judge output limit; its state check still passed. "
                f"[Open that execution]({LENS}61b58dc4c65c20bd54f83ae44ab3aeab).\n\n"
                "The coverage bars above count state scores, not LLM judgments. Missing judgment is not zero.", 7), columns=1),
            section("3. Inspect a recovery and the decision to retain a version", note(
                f"1. [Invoice lookup and refund]({LENS}a5e6d591a1e0a977954efd67bae60ecc): follow the tool arguments and returned account state.\n"
                f"2. [The write that timed out but committed]({LENS}911e3062cf37ac66f5b9944464a27fae): find the error, then the recovery.\n"
                f"3. [Round-two composition]({LENS}308a82196e70910f970a2ae41e900cd4): inspect the reason for retaining the tested manual harness.\n\n"
                "Every harness encountered one recoverable tool error on the onboarding-recovery case. "
                "A tool error is not automatically a failed task. No run has been repeated for this view.", 6), columns=1),
            section("4. All twelve cases - ordinary W&B Table fallback",
                note("Match the same case_id across the three versions. Open scores for state and explanation checks, "
                     "and evidence for the exact trace. Native EvalTables publication was unavailable (HTTP 500); "
                     "this is the saved ordinary W&B Table, not native EvalTables.", 3),
                panel.MediaBrowser(title="Saved case comparisons", media_keys=["comparison"], num_columns=1,
                    layout=panel.Layout(w=24, h=10)), columns=1),
        ]
        pinned = ["run:displayName", "config:condition", "summary:pending-final/error_mean", "summary:available_scores", "summary:planned_scores"]
    filters = f'Config("workspace_id") == "{workspace}" and ID in {json.dumps(list(records))}'
    colors = {rid: ws.RunSettings(color=COLORS["baseline" if "persistence" in title.lower() or "starting" in title.lower() or "copy latest" in title.lower() else "agent" if "round" in title.lower() or "agent" in title.lower() else "manual"]) for rid, (title, _, _) in records.items()}
    view = ws.Workspace(entity=entity, project=project, name=name, sections=sections,
        settings=ws.WorkspaceSettings(max_runs=12, smoothing_type="none", ignore_outliers=False),
        runset_settings=ws.RunsetSettings(filters=filters, pinned_columns=pinned, run_settings=colors),
        auto_generate_panels=False)
    return view, records, workspace


def forge_url(url):
    parsed=urlparse(url)
    path=parsed.path if parsed.path.startswith('/wandb/wandb/') else '/wandb'+parsed.path
    return urlunparse(('https','forge.coreweave.com',path,'',parsed.query,''))


def sdk_url(url):
    parsed=urlparse(url)
    path=parsed.path[6:] if parsed.path.startswith('/wandb/wandb/') else parsed.path
    return urlunparse(('https','wandb.ai',path,'',parsed.query,''))


def describe(kind, view, records, workspace):
    return {'study':kind, 'name':view.name, 'workspace':workspace, 'filters':view.runset_settings.filters,
        'runs':[{'id':rid,'label':label,'metric':metric,'expected':expected} for rid,(label,metric,expected) in records.items()],
        'sections':[{'title':s.name,'panels':[getattr(p,'title',None) or 'Explanation and evidence links' for p in s.panels]} for s in view.sections],
        'auto_generate_panels':False, 'changes_runs':False, 'changes_default_workspace':False}


def verify_runs(api, records, workspace):
    rows=[]
    for rid,(label,metric,expected) in records.items():
        run=api.run(PROJECT+'/'+rid)
        actual=run.summary.get(metric)
        if run.config.get('workspace_id')!=workspace or actual is None or abs(actual-expected)>1e-12:
            raise ValueError(f'Saved run does not match the rehearsal: {rid}')
        rows.append({'id':rid,'name':run.name,'metric':metric,'actual':actual,'state':run.state})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save',action='store_true',help='Save only these named view configurations.')
    parser.add_argument('--verify',action='store_true',help='Read the source runs before producing the plan.')
    parser.add_argument('--only',choices=['solar','pending'])
    parser.add_argument('--receipt',type=Path,default=ROOT/'evidence/demo-workspaces.json')
    args=parser.parse_args()
    receipt=json.loads(args.receipt.read_text()) if args.receipt.exists() else {}
    api=wandb.Api(timeout=40) if args.save or args.verify else None
    plans=[]
    for kind in [args.only] if args.only else ['solar','pending']:
        view,records,workspace=build(kind)
        plan=describe(kind,view,records,workspace)
        # Serializing before any write catches invalid filters and panel settings.
        view._to_model().spec.model_dump(mode='json',by_alias=True)
        if api: plan['source_readback']=verify_runs(api,records,workspace)
        if args.save:
            if kind in receipt:
                old=ws.Workspace.from_url(sdk_url(receipt[kind]['url']))
                if old.name!=view.name:
                    raise ValueError('Refusing to overwrite a view with a different name.')
                view._internal_name=old._internal_name
                view._internal_id=old._internal_id
            view.save()
            url=forge_url(view.url)
            readback=ws.Workspace.from_url(sdk_url(url))
            if readback.name!=view.name or readback.auto_generate_panels is not False:
                raise RuntimeError('Saved workspace readback differs.')
            actual_ids=[leaf['value'] for leaf in readback._to_model().spec.section.run_sets[0].filters['filters'] if leaf.get('op')=='IN']
            if actual_ids!=[list(records)]:
                raise RuntimeError('Saved run filter differs from the exact run set.')
            plan.update(url=url,readback='verified',internal_name=view._internal_name)
            receipt[kind]=plan
            args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
        plans.append(plan)
    print(json.dumps(plans,indent=2))


if __name__=='__main__':
    main()
