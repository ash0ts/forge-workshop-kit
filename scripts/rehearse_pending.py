"""Live rehearsal with durable reuse. Costs belong to the supplied participant project."""
import argparse,json,time
from pathlib import Path
from dataclasses import asdict
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.pending.cases import CASES
from forge_workshop_kit.pending.harness import Harness
from forge_workshop_kit.pending.loop import run_employee,editor_decision,judge_explanation
from forge_workshop_kit.provider import Provider
from forge_workshop_kit.session import digest
from forge_workshop_kit.publication import publish_comparison,publish_report
p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--state',default='.workshop/pending-rehearsal');a=p.parse_args()
s=WorkshopSession(a.project,'pending-direct',state_dir=a.state,budget_usd=4)
s.check_access(); started=time.time()
dev=[c for c in CASES if c.split=='development'];test=[c for c in CASES if c.split=='heldout']
original=Harness(instructions='Resolve the requested billing or onboarding task using the provided tools. Explain what you verified and what remains unresolved.',verification_skill='Read the account after a write. Check that the requested change happened once and unrelated records stayed unchanged.')
manual=Harness(**{**asdict(original),'verification_skill':'Check whether a timed-out write already committed before repeating it. Reuse the same operation_id for the same intended write. Verify the account before claiming completion.'})
for label,h in [('original',original),('manual',manual)]:
 for c in dev:
  r=run_employee(s,c,h,'pending/'+label);print(label,c.id,r['scores'],flush=True)
parent=manual;lesson=None
for n,c in enumerate(dev,1):
 prefix=f'pending/round-{n}/'
 experience=run_employee(s,c,parent,prefix+'starting');experience['lesson']=lesson
 proposals=editor_decision(s,n,'propose',parent,[experience]);print('PROPOSALS',json.dumps(proposals),flush=True)
 # This script is a maintainer rehearsal. Review is performed via --reviewed file on resume.
 approval=s.file(f'review-round-{n}-proposals.json')
 if not approval.exists() or json.loads(approval.read_text()).get('decision_fingerprint')!=digest(proposals['candidates']):
  print('REVIEW REQUIRED:',approval,flush=True);break
 probes=[run_employee(s,c,Harness(**d['harness']),prefix+'candidate-'+str(i)) for i,d in enumerate(proposals['candidates'])]
 decision=editor_decision(s,n,'compose',parent,probes);print('COMPOSITION',json.dumps(decision),flush=True)
 approval=s.file(f'review-round-{n}-composition.json')
 if not approval.exists() or json.loads(approval.read_text()).get('decision_fingerprint')!=digest({k:v for k,v in decision.items() if k!='trace'}): print('REVIEW REQUIRED:',approval,flush=True);break
 parent=Harness(**decision['harness']);run_employee(s,c,parent,prefix+'composition');lesson=decision.get('lesson')
 with s.stage(prefix+'adopted',sources=parent.files()) as stage:
  if stage.needs_run:stage.record({'harness':asdict(parent),'lesson':lesson,'limits':decision.get('limits')})
else:
 versions={'starting':original,'manual':manual,'agent':parent};records={};rows={}
 for label,h in versions.items():
  records[label]=[];rows[label]=[]
  for c in test:
   run=run_employee(s,c,h,'pending/final-'+label)
   try:judge=judge_explanation(s,run,'Completion claims must match recorded work. Distinguish uncertainty from failure.')
   except Exception as error:judge={'status':'unavailable','error':str(error)}
   records[label].append({'case':c.id,'scores':run['scores'],'judge':judge,'trace':run['trace']})
   rows[label].append(dict(case_id=c.id,input=c.mission,prediction=run['draft'],target='Required account state',error=1-int(run['scores']['task_success']),evidence=run['trace']))
 receipts=publish_comparison(s,'pending-final',rows)
 result={'cost':Provider(s).summary(),'seconds_this_resume':time.time()-started,'results':records,'publication':receipts}
 Path('evidence/pending-rehearsal.json').write_text(json.dumps(result,indent=2))
 s.checkpoint('rehearsal-complete',evidence={k:v['run'] for k,v in receipts.items()})
 print(json.dumps(result),flush=True)
print('ACCOUNTING',Provider(s).summary(),flush=True)
