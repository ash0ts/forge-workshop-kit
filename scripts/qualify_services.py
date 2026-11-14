"""Check real product paths without training or model calls."""
import argparse
import json
from pathlib import Path
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.traces import event,export_trace
from forge_workshop_kit.publication import publish_comparison

parser=argparse.ArgumentParser()
parser.add_argument('--project',required=True)
parser.add_argument('--state',default='.workshop/service-check')
args=parser.parse_args()
session=WorkshopSession(args.project,'kit-qualification',state_dir=args.state)
print('access',session.check_access(),flush=True)
with session.stage('tools/check') as stage:
    if stage.needs_run:
        result,receipt=event('check_arithmetic',{'input':3},lambda:{'output':9})
        stage.record({'events':[receipt]})
try:
    trace=export_trace(session,stage.id,'Check a small tool operation before running the workshop',stage.result['events'])
except Exception as error:
    trace={'status':'unavailable','error':str(error)}
print('trace',trace,flush=True)
try:
    evaluation=publish_comparison(session,'kit-qualification',{'reference':[dict(case_id='example',input=3,prediction=9,target=9,error=0)]})
except Exception as error:
    evaluation={'status':'unavailable','error':str(error)}
print('evaluation',evaluation,flush=True)
checkpoint=session.checkpoint('services',evidence={'Agent Lens':trace.get('url','')})
print('checkpoint',checkpoint,flush=True)
Path('evidence/services.json').write_text(json.dumps(dict(trace=trace,evaluation=evaluation,checkpoint=checkpoint),indent=2))
