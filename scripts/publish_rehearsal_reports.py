"""Publish conclusions from saved rehearsal evidence, without running experiments."""
import argparse
import json
from pathlib import Path
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.publication import publish_report

p=argparse.ArgumentParser();p.add_argument('--project',required=True);a=p.parse_args()
receipts={}
for workshop,stem in [('pending-direct','pending'),('solar-autoresearch','solar')]:
    session=WorkshopSession(a.project,workshop,state_dir=f'.workshop/{stem}-rehearsal')
    data=json.loads(Path(f'evidence/{stem}-rehearsal.json').read_text())
    if stem=='pending':
        conclusion='Gateway-free Pending completed two harness-improvement rounds and 12 final cases: four each for the starting, manual and agent-revised harnesses. Every version passed all four independent state checks; all 12 explanation judgments were available and passed. This is a working teaching loop, not evidence of a quality gain. The rehearsal used $'+str(data['cost']['observed_usd'])+' in measured inference. A timeout after a committed onboarding write is retained in the traces; the employee recovered by inspecting state.'
    else:
        result=data['results']
        conclusion=('On 199 overlapping image windows from February 13–14, 2014, final disk-masked error was '
            +', '.join(f'{k}: {v["error"]:.6f}' for k,v in result.items())
            +'. The agent-selected masked-L1 model reduced error by 1.37% relative to the manual residual predictor in this single rehearsal. Round two tried cosine learning-rate decay, regressed on validation, and retained the previous source. Forecasting weights were trained; the research-agent model stayed fixed. The short GOES training budget was insufficient: the selected measurement model scored 2.469 log-flux MAE versus 0.193 for persistence. These are separate tasks, not one combined score. Two test days and one seed do not establish solar forecasting performance. Measured inference cost was $'+str(data['cost']['observed_usd'])+'.')
    conclusion+=' Native EvalTables returned HTTP 500. Saved Weave evaluations, W&B tables and local predictions remain available. Publication retries do not repeat training or inference. The complete code, data contract and qualification limits are in https://github.com/ash0ts/forge-workshop-kit.'
    links={label:receipt['run'] for label,receipt in data['publication'].items()}
    links['Source and setup']='https://github.com/ash0ts/forge-workshop-kit'
    receipts[stem]=publish_report(session,conclusion,links)
Path('evidence/reports.json').write_text(json.dumps(receipts,indent=2))
print(json.dumps(receipts))
