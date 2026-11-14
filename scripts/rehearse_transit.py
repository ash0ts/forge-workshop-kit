"""Explicit maintainer rehearsal. Review returned patches before integrating them."""
import argparse
import json
from pathlib import Path

from forge_workshop_kit import WorkshopSession, factory, transit
from forge_workshop_kit import factory_teaching as teaching, transit_workshop as lab
from forge_workshop_kit.provider import Provider
from forge_workshop_kit.session import digest, write_json
from forge_workshop_kit.traces import event

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('action',choices=['prepare','solo','team','inspect','integrate','lesson','accept','followup','integrate-followup','evaluate','publish','release','status'])
p.add_argument('--project',default='wandb/forge-workshop-kit')
p.add_argument('--state',default='.workshop/transit-v060-live')
p.add_argument('--budget-usd',type=float,default=8)
p.add_argument('--reviewed',help='Digest printed by inspect for the patches you reviewed')
p.add_argument('--note',default='')
p.add_argument('--evidence')
p.add_argument('--version',default='with-memory')
a=p.parse_args()
s=WorkshopSession(a.project,'transit-factory',state_dir=a.state,budget_usd=a.budget_usd)
solutions={key:value['solution'] for key,value in teaching.EXERCISES.items()}
if a.action not in ('inspect','status'):
    s.check_access()

if a.action=='prepare':
    s.save_draft('factory/acceptance',teaching.ACCEPTANCE_SOLUTION)
    lab.save_check(s,'acceptance',teaching.ACCEPTANCE_SOLUTION,teaching.check_acceptance(teaching.ACCEPTANCE_SOLUTION))
    for key,code in solutions.items():
        s.save_draft('factory/'+key,code)
        lab.save_check(s,key,code,teaching.check_exercise(key,code))
    with s.stage('factory/setup',config={'data':transit.data_manifest()}) as stage:
        if stage.needs_run:
            result,receipt=event('inspect_transit_source',{},lab.data_preview,on_error=stage.record_event)
            stage.record({'data':result,'events':[receipt],'mission':'Inspect the historical timetable before building.'})
    result={'checks':'passed','dataset':transit.data_manifest()['dataset_id']}
elif a.action in ('solo','team'):
    result=lab.run_initial(s,a.action,solutions['worker'],workers=1 if a.action=='solo' else 2,task_code=solutions['tasks'])
    result={'outcomes':result['outcomes'],'metrics':result['metrics']}
elif a.action=='inspect':
    patches={name:{task_id:row.get('patch',{}) for task_id,row in factory.load_board(s,name).snapshot()['tasks'].items()}
             for name in lab._state(s).get('builds',{})}
    path=s.file('review-patches.json');write_json(path,patches)
    result={'file':str(path),'review_digest':digest(patches),'builds':list(patches)}
elif a.action in ('integrate','integrate-followup'):
    patches={name:{task_id:row.get('patch',{}) for task_id,row in factory.load_board(s,name).snapshot()['tasks'].items()}
             for name in lab._state(s).get('builds',{})}
    if a.reviewed!=digest(patches): raise SystemExit('Inspect the actual patches, then pass their digest with --reviewed.')
    result=lab.integrate_initial(s) if a.action=='integrate' else lab.integrate_followups(s)
elif a.action=='lesson': result=lab.propose_lesson(s)
elif a.action=='accept': result=lab.accept_lesson(s,a.note,a.evidence)
elif a.action=='followup': result=lab.run_followups(s,solutions['worker'],solutions['tasks'],solutions['memory'])
elif a.action=='evaluate': result=lab.evaluate_builds(s)
elif a.action=='publish': result={'traces':lab.publish_traces(s),'evaluations':lab.publish_results(s)}
elif a.action=='release': result=lab.release(s,a.version,solutions['release'],a.note)
else:
    state=lab._state(s)
    result={'builds':{label:{'tasks':{k:r['status'] for k,r in factory.load_board(s,label).snapshot()['tasks'].items()},'metrics':row['result']['metrics']}
                      for label,row in state.get('builds',{}).items()},
            'results':{label:{k:row[k] for k in ('passed','passed_count','total','scenario_pass_rate')} for label,row in state.get('evaluations',{}).items()}}
print(json.dumps(result,indent=2),flush=True)
print('Accounting:',json.dumps(Provider(s).summary()),flush=True)
