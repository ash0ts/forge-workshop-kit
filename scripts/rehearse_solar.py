"""Run the fixed CPU lesson; pause before executing every agent-written change."""
import argparse,json,time
from pathlib import Path
import numpy as np
from forge_workshop_kit import WorkshopSession,solar,training,research,plots
from forge_workshop_kit.provider import Provider
from forge_workshop_kit.publication import publish_comparison
from forge_workshop_kit.traces import export_trace
p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--state',default='.workshop/solar-rehearsal');p.add_argument('--data',default='data/solar-v1');a=p.parse_args()
s=WorkshopSession(a.project,'solar-autoresearch',state_dir=a.state,budget_usd=4)
s.check_access();fp=solar.verify_data(a.data);source=Path('examples/solar/candidate.py').read_text()
goes,_=solar.load_goes(a.data);images,_=solar.load_aia(a.data)

def train(name,code,splits,config):
 with s.stage(name,config=config,sources={'candidate.py':code},inputs={'dataset':fp,'split':'validation'}) as stage:
  if stage.needs_run:
   started=time.time();result,prediction=training.train(code,splits['train'],splits['validation'],config,stage.output_dir)
   result['events']=[dict(id=stage.id+'/train',name='train_and_validate',arguments={'config':config,'source_fingerprint':stage.source_fingerprint,'split':'validation'},result=result['metrics'],started_at=started,ended_at=time.time())]
   figure=plots.forecast(prediction,splits['validation'],title=name);figure.savefig(stage.output_dir/'predictions.png',dpi=130)
   stage.record(result,files=[stage.output_dir/f for f in ('candidate.py','weights.pt','predictions.npy','predictions.png','losses.json','stderr.txt')])
 try:trace=export_trace(s,stage.id,'Train exact reviewed code and score validation predictions',stage.result['events'])
 except Exception as error:trace={'status':'unavailable','error':str(error)}
 if stage.needs_run:s.checkpoint(name,evidence={name:trace.get('url','')})
 record=dict(stage_id=stage.id,source=code,config=config,metrics=stage.result['metrics'],losses=stage.result['losses'],split='validation',trace=trace)
 print(name,record['metrics'],flush=True);return record

# This is the same six-trial grid as the notebook. Actual Sweeps integration is checked separately.
grid=[dict(architecture=a,width=w,learning_rate=lr,steps=60,seed=17,batch_size=32) for a in ('mlp','cnn') for w,lr in ((16,.001),(32,.001),(16,.003))]
import wandb
with s.stage('goes/create-sweep',inputs={'source':source,'configurations':grid}) as sweep_stage:
 if sweep_stage.needs_run:
  sweep_id=wandb.sweep({'method':'grid','metric':{'name':'validation_error','goal':'minimize'},'parameters':{'trial':{'values':list(range(6))}}},entity=s.project.split('/')[0],project=s.project.split('/')[1])
  sweep_stage.record({'sweep_id':sweep_id})
def trial():
 with wandb.init(entity=s.project.split('/')[0],project=s.project.split('/')[1],job_type='workshop-sweep') as run:
  i=int(run.config.trial);record=train('goes/search-'+str(i),source,goes,grid[i]);run.log(record['metrics'])
if not any(r['name']=='goes/sweep-finished' for r in s.completed()):
 wandb.agent(sweep_stage.result['sweep_id'],function=trial,count=6,entity=s.project.split('/')[0],project=s.project.split('/')[1])
 with s.stage('goes/sweep-finished',inputs={'sweep':sweep_stage.result['sweep_id']}) as done:
  if done.needs_run:done.record({'trials':6})
goes_runs=[train('goes/search-'+str(i),source,goes,c) for i,c in enumerate(grid)]
manual_runs=[train('images/manual-'+a,source,images,dict(architecture=a,width=8,learning_rate=.001,steps=40,seed=17,batch_size=8)) for a in ('conv','residual')]
manual=min(manual_runs,key=lambda r:r['metrics']['validation_error']);parent=manual
for number in (1,2):
 prefix=f'images/round-{number}/'
 saved=[r for r in s.completed() if r['name']==prefix+'propose']
 if saved:proposal,proposal_id=saved[-1]['result'],saved[-1]['id']
 else:proposal,proposal_id=research.propose(s,number,parent['source'],parent)
 research.trace_decision(s,proposal_id)
 print('PROPOSALS',number,json.dumps(proposal),flush=True)
 review=s.file(f'review-round-{number}-proposals.json')
 if not review.exists() or json.loads(review.read_text()).get('reviewed_stage')!=proposal_id:print('REVIEW REQUIRED proposals',number,flush=True);break
 probes=[]
 for i,candidate in enumerate(proposal['candidates']):
  try:r=train(prefix+'probe-'+str(i),candidate['source'],images,parent['config'])
  except Exception as error:r=dict(source=candidate['source'],split='validation',errors=[str(error)],metrics={})
  probes.append({**r,'title':candidate['title'],'rationale':candidate['rationale']})
 with s.stage(prefix+'probe-done',inputs={'probes':probes}) as stage:
  if stage.needs_run:stage.record({'probes':probes})
 saved=[r for r in s.completed() if r['name']==prefix+'compose']
 if saved:composition,compose_id=saved[-1]['result'],saved[-1]['id']
 else:composition,compose_id=research.compose(s,number,parent['source'],parent,probes)
 research.trace_decision(s,compose_id)
 print('COMPOSITION',number,json.dumps(composition),flush=True)
 review=s.file(f'review-round-{number}-composition.json')
 if not review.exists() or json.loads(review.read_text()).get('reviewed_stage')!=compose_id:print('REVIEW REQUIRED composition',number,flush=True);break
 decision=composition['decision'];tested=train(prefix+'composition-test',decision['source'],images,parent['config'])
 selected=tested if tested['metrics']['validation_error']<parent['metrics']['validation_error'] else parent
 with s.stage(prefix+'adopt',inputs={'tested':tested['stage_id']}) as stage:
  if stage.needs_run:stage.record({'adopted':selected,'decision':decision,'retained_parent':selected is parent,'lesson':decision.get('lesson'),'limits':decision.get('limits')})
 parent={**selected,'lessons':[{'lesson':decision.get('lesson'),'limits':decision.get('limits')}]}
else:
 versions={'manual':manual,'agent':parent};freeze,freeze_id=research.freeze(s,versions,fp)
 rows={'persistence':solar.evaluation_rows(images['test']['persistence'],images['test'])};results={'persistence':solar.score(images['test']['persistence'],images['test'])}
 for label,version in versions.items():
  with s.stage('images/final-'+label,config=version['config'],sources={'candidate.py':version['source']},inputs={'freeze':freeze_id,'split':'test'}) as stage:
   if stage.needs_run:
    result,prediction=training.train(version['source'],None,images['test'],version['config'],stage.output_dir,weights=s.file('outputs/'+version['stage_id']+'/weights.pt'))
    plots.forecast(prediction,images['test'],title=label).savefig(stage.output_dir/'predictions.png',dpi=130)
    stage.record(result,files=[stage.output_dir/'predictions.npy',stage.output_dir/'predictions.png'])
   prediction=np.load(stage.output_dir/'predictions.npy');results[label]=stage.result['metrics'];rows[label]=solar.evaluation_rows(prediction,images['test'],evidence={'stage_id':stage.id,'trace':version['trace']})
 best=min(goes_runs,key=lambda r:r['metrics']['validation_error'])
 with s.stage('goes/final',config=best['config'],sources={'candidate.py':best['source']},inputs={'selected_stage':best['stage_id'],'split':'test'}) as final_goes:
  if final_goes.needs_run:
   gr,gp=training.train(best['source'],None,goes['test'],best['config'],final_goes.output_dir,weights=s.file('outputs/'+best['stage_id']+'/weights.pt'))
   plots.forecast(gp,goes['test'],title='GOES final').savefig(final_goes.output_dir/'predictions.png',dpi=130)
   final_goes.record(gr,files=[final_goes.output_dir/'predictions.npy',final_goes.output_dir/'predictions.png'])
  gp=np.load(final_goes.output_dir/'predictions.npy')
 goes_publication=publish_comparison(s,'solar-measurements-final',{'persistence':solar.evaluation_rows(goes['test']['persistence'],goes['test']),'selected-model':solar.evaluation_rows(gp,goes['test'],evidence={'stage_id':final_goes.id})})
 receipts=publish_comparison(s,'solar-images-final',rows)
 result=dict(measurements={'metrics':final_goes.result['metrics'],'publication':goes_publication},dataset=fp,counts={k:len(v['ids']) for k,v in images.items()},results=results,publication=receipts,cost=Provider(s).summary())
 Path('evidence/solar-rehearsal.json').write_text(json.dumps(result,indent=2));s.checkpoint('rehearsal-complete')
 print(json.dumps(result),flush=True)
print('ACCOUNTING',Provider(s).summary(),flush=True)
