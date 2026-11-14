"""Explicit, bounded provider and trace check; uses development cases only."""
import argparse
import json
from pathlib import Path
from forge_workshop_kit import WorkshopSession, routing
from forge_workshop_kit.provider import Provider, validated_json, MODEL
from forge_workshop_kit.routing_teaching import JUDGE_RUBRIC
from forge_workshop_kit.traces import export_trace, saved_trace_inputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='Authorize this bounded live check.')
    parser.add_argument('--project',default='wandb/forge-workshop-kit')
    parser.add_argument('--state',type=Path,default=Path('.workshop/routing-live-v050'))
    parser.add_argument('--data',type=Path,default=Path('data/banking77-v1'))
    parser.add_argument('--budget-usd',type=float,default=8.)
    parser.add_argument('--output',type=Path,default=Path('evidence/routing-live-v050.json'))
    args=parser.parse_args()
    if not args.run:
        parser.exit(message='No inference sent. Pass --run after checking project, allowance, and credentials. Maximum8 routes plus4 judgments, each with at most one schema repair.\n')
    session=WorkshopSession(args.project,'banking-routing',state_dir=args.state,budget_usd=args.budget_usd)
    session.check_access()
    data=routing.load_data(args.data)
    intents=sorted({r['label'] for r in data['rows'] if r['split']=='train'})
    rows=sorted(routing.partition(data,'validation')[0],key=lambda r:r['id'])[:8]
    outcomes=[]
    for row in rows:
        outcome={'kind':'route','case_id':row['id']}
        try:
            with session.stage('routing/live-route/'+row['id'],config={'model':MODEL,'case':row['id']}) as stage:
                if stage.needs_run:
                    value,request=validated_json(session,stage.id,routing.route_messages(row['text'],intents),lambda v:routing.validate_route(v,intents),max_tokens=512)
                    stage.record({'case_id':row['id'],'response':value,'reference':row['label'],'correct':value['intent']==row['label']})
            outcome.update(status='complete',**stage.result)
            try:outcome['trace']=export_trace(session,**saved_trace_inputs(session,stage.id))
            except Exception as error:outcome['trace_error']=str(error)
        except Exception as error:outcome.update(status='unavailable',error=str(error))
        outcomes.append(outcome)
        print(json.dumps({k:v for k,v in outcome.items() if k not in ('trace','response')}),flush=True)
    recorded=json.loads(Path('examples/routing/recorded-review.json').read_text())
    for row in recorded:
        outcome={'kind':'judge','case_id':row['case_id'],'expected_source':'published dataset reference; not a human review'}
        try:
            with session.stage('routing/live-judge/'+row['case_id'],config={'model':MODEL,'case':row['case_id']},sources={'rubric.txt':JUDGE_RUBRIC}) as stage:
                if stage.needs_run:
                    messages=[{'role':'system','content':JUDGE_RUBRIC},{'role':'user','content':json.dumps({'request':row['text'],'proposed_intent':row['prediction'],'needs_review':False})}]
                    value,request=validated_json(session,stage.id,messages,routing.validate_judgment,max_tokens=512)
                    stage.record({'case_id':row['case_id'],'judgment':value,'reference_failed':row['prediction']!=row['target']})
            outcome.update(status='complete',**stage.result)
            try:outcome['trace']=export_trace(session,**saved_trace_inputs(session,stage.id))
            except Exception as error:outcome['trace_error']=str(error)
        except Exception as error:outcome.update(status='unavailable',error=str(error))
        outcomes.append(outcome)
        print(json.dumps({k:v for k,v in outcome.items() if k not in ('trace','judgment')}),flush=True)
    result={'identity':'routing-live-v050','project':args.project,'workspace':session.workspace_id,'model':MODEL,
            'cost':Provider(session).summary(),'outcomes':outcomes,
            'trace_readback_complete':all(o.get('trace',{}).get('verified') for o in outcomes),
            'limitation':'Provider and tracing rehearsal in the maintainer account. Not a fresh external account or human usability rehearsal.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    session.checkpoint('routing-live-qualification')
    print(json.dumps({'cost':result['cost'],'trace_readback_complete':result['trace_readback_complete']}))

if __name__=='__main__':main()
