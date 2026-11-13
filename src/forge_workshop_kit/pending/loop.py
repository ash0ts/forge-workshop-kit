"""Gateway-free Pending example: direct inference, local functions and real stdio MCP."""
import asyncio
import copy
import inspect
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

from ..provider import Provider, output, validated_json
from ..session import digest, write_json
from ..traces import export_trace
from .harness import Harness, RULES, TOOL_GUIDE, build_messages, harness_diff
from .simulator import execute, check_work
from .grading import grade


def lookup_invoice(state,account_id,invoice_id):
    account=state['accounts'][account_id]
    return {'payments':[p for p in account['payments'] if p['invoice_id']==invoice_id],
            'refunds':account['refunds']}


async def mcp_action(world, fault, name, arguments, path):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    write_json(path,{'world':world,'fault':fault})
    env={k:os.environ[k] for k in ('PATH','SYSTEMROOT','WINDIR','TMPDIR','TEMP') if k in os.environ}
    env['OFFICE_STATE']=str(path)
    parameters=StdioServerParameters(command=sys.executable,
        args=['-m','forge_workshop_kit.pending.mcp_server'],env=env)
    async with stdio_client(parameters) as (read,write):
        async with ClientSession(read,write) as client:
            await client.initialize()
            tools=await client.list_tools()
            if name=='discover_onboarding':
                result={'tools':[{'name':t.name,'inputSchema':t.inputSchema} for t in tools.tools]}
            else:
                response=await client.call_tool(name,arguments)
                result=json.loads(next(c.text for c in response.content if hasattr(c,'text')))
    return json.loads(path.read_text())['world'],result


def run_employee(session, case, harness, label, *, invoice_tool=lookup_invoice, max_steps=10):
    source=inspect.getsource(invoice_tool)
    with session.stage(label+'/'+case.id, sources={**harness.files(),'lookup_invoice.py':source},
                       inputs={'case_id':case.id,'split':case.split}) as stage:
        if stage.needs_run:
            world=copy.deepcopy(case.initial)
            messages=build_messages({'mission':case.mission},harness)
            messages[0]['content']+='\nlookup_invoice: {account_id, invoice_id} reads invoice payments and refunds.'
            events=[]; draft=None; status='agent_failure'; last_check=None
            for step in range(max_steps):
                request=Provider(session).complete(stage.id+'/'+str(step),messages,max_tokens=4096)
                action=output(request)
                name=action.get('action'); arguments=action.get('arguments',{})
                started=time.time()
                if name=='finish':
                    if harness.verify_before_finish and (not last_check or not last_check['passed'] or last_check['state']!=digest(world)):
                        result={'ok':False,'error':'Check the current work before submitting.'}
                    else:
                        draft=arguments; status='complete'; result={'accepted':True}
                elif name=='lookup_invoice':
                    try: result=invoice_tool(world,**arguments)
                    except Exception as error: result={'ok':False,'error':str(error)}
                elif name=='read_skill':
                    result={'text':{'verify-operation':harness.verification_skill,'office-tools':harness.tool_skill}.get(arguments.get('name'),'Skill not installed')}
                elif name=='check_work':
                    result=check_work(world,case.objective) if case.split=='development' else {'passed':True,'observation':'Review account state against the customer request. Final grading is separate.'}
                    last_check={'state':digest(world),'passed':result['passed']}
                elif name in ('discover_onboarding','onboarding_status','provision_member'):
                    world,result=asyncio.run(mcp_action(world,case.fault,name,arguments,stage.output_dir/'office.json'))
                else:
                    world,result=execute(world,name,arguments,case.fault)
                # Retry only reads. A timed-out write can already have committed.
                if harness.read_retries and result.get('error') and name in ('lookup_invoice','get_account','list_payments','onboarding_status'):
                    events.append(dict(id=stage.id+'/tool-'+str(step)+'-first',name=name,arguments=arguments,
                        result=result,started_at=started,ended_at=time.time(),error=result.get('error')))
                    started=time.time()
                    if name=='lookup_invoice':
                        try: result=invoice_tool(world,**arguments)
                        except Exception as error: result={'ok':False,'error':str(error)}
                    elif name=='onboarding_status':
                        world,result=asyncio.run(mcp_action(world,case.fault,name,arguments,stage.output_dir/'office.json'))
                    else:
                        world,result=execute(world,name,arguments,case.fault)
                events.append(dict(id=stage.id+'/tool-'+str(step),name=name or 'invalid_action',arguments=arguments,
                    result=result,started_at=started,ended_at=time.time(),error=result.get('error')))
                messages.extend([{'role':'assistant','content':json.dumps(action)},
                                 {'role':'user','content':'Tool observation: '+json.dumps(result)}])
                write_json(stage.output_dir/'partial.json',{'world':world,'events':events,'messages':messages})
                if status=='complete': break
            run={'world':world,'events':events,'draft':draft,'status':status,'mission':case.mission,
                 'case_id':case.id,'split':case.split,'harness':asdict(harness),'harness_fingerprint':harness.fingerprint}
            run['scores']=grade(case,run)
            stage.record(run,files=[stage.output_dir/'partial.json'])
    requests=[r for k,r in session.read()['requests'].items() if k.startswith(stage.id+'/') and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,case.mission,stage.result['events'],requests)
    except Exception as error:
        trace={'status':'unavailable','error':str(error)}
    if stage.needs_run:
        session.checkpoint(label+'/'+case.id,evidence={'Conversation':trace.get('url','')})
    return {**stage.result,'trace':trace,'stage_id':stage.id}


def editor_decision(session,number,phase,parent,evidence):
    if any(r['split']!='development' for r in evidence):
        raise ValueError('Final cases cannot enter improvement context.')
    allowed=[{k:r[k] for k in ('case_id','events','draft','status','harness','lesson','limits') if k in r} for r in evidence]
    schema='{"candidates":[DECISION,DECISION]}' if phase=='propose' else 'DECISION'
    system='Edit an office agent harness, never the case or tools. Return JSON '+schema+'. DECISION is {decision:CHANGE|KEEP,title,rationale,harness:{instructions,verification_skill,tool_skill,verify_before_finish,read_retries},lesson,limits}. KEEP uses the parent harness exactly. No task-specific account IDs in reusable instructions. '+RULES+TOOL_GUIDE+'\nlookup_invoice: {account_id, invoice_id} reads invoice payments and refunds.'
    name=f'pending/round-{number}/{phase}'
    failed=[r for r in session.read()['stages'].values() if r['name']==name and r['status']=='failed']
    if len(failed)>1:
        raise ValueError('Two editing attempts failed. Inspect the saved responses before changing the exercise.')
    with session.stage(name,sources=parent.files(),inputs={'evidence':allowed},attempt=1+len(failed)) as stage:
        if stage.needs_run:
            def validate(value):
                decisions=value.get('candidates',[]) if phase=='propose' else [value]
                if len(decisions)!=(2 if phase=='propose' else 1): raise ValueError('Incomplete editing decision')
                for d in decisions:
                    if d.get('decision') not in ('CHANGE','KEEP') or not d.get('rationale'): raise ValueError('Need CHANGE/KEEP and rationale')
                    proposed=Harness(**d['harness'])
                    if d['decision']=='KEEP' and proposed!=parent: raise ValueError('KEEP changed the harness')
                    if d['decision']=='CHANGE' and proposed==parent: raise ValueError('No executable change; use KEEP')
            value,call=validated_json(session,stage.id,[{'role':'system','content':system},
                {'role':'user','content':json.dumps({'parent':asdict(parent),'evidence':allowed})}],validate,max_tokens=16384)
            decisions=value.get('candidates',[]) if phase=='propose' else [value]
            if len(decisions)!=(2 if phase=='propose' else 1): raise ValueError('Incomplete editing decision')
            for d in decisions:
                if d.get('decision') not in ('CHANGE','KEEP') or not d.get('rationale'): raise ValueError('Need CHANGE/KEEP and rationale')
                proposed=Harness(**d['harness'])
                if d['decision']=='KEEP' and proposed!=parent: raise ValueError('KEEP changed the harness')
                if d['decision']=='CHANGE' and proposed==parent: raise ValueError('No executable change; use KEEP')
                d.update(diff=harness_diff(parent,proposed),fingerprint=proposed.fingerprint)
            stage.record(value)
    requests=[r for k,r in session.read()['requests'].items() if k.startswith(stage.id+'/') and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,stage.name,[],requests)
        result={**stage.result,'trace':trace}
    except Exception as error:
        result={**stage.result,'trace':{'status':'unavailable','error':str(error)}}
    return result


def judge_explanation(session,run,rubric):
    with session.stage('pending/judge/'+run['stage_id'],inputs={'execution':run['stage_id'],'rubric':rubric}) as stage:
        if stage.needs_run:
            call=Provider(session).complete(stage.id,[{'role':'system','content':'Judge explanation against actual recorded actions. Return JSON {grounded: boolean, complete: boolean, reason: string}. '+rubric},
                {'role':'user','content':json.dumps({'mission':run['mission'],'events':run['events'],'draft':run['draft']})}],max_tokens=4096)
            judgment=output(call)
            if any(type(judgment.get(k)) is not bool for k in ('grounded','complete')) or not isinstance(judgment.get('reason'),str):
                raise ValueError('Judge returned an invalid structured answer')
            stage.record(judgment)
    requests=[r for k,r in session.read()['requests'].items() if k.startswith(stage.id+'/') and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,stage.name,[],requests)
        result={**stage.result,'trace':trace}
    except Exception as error:
        result={**stage.result,'trace':{'status':'unavailable','error':str(error)}}
    return result
