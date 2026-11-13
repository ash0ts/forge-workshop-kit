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
from ..execution import run_async
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
    env.update(OFFICE_STATE=str(path),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
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
    return json.loads(path.read_text(encoding="utf-8"))['world'],result


def call_mcp(world, fault, name, arguments, path):
    """Notebook kernels already run an event loop; give stdio MCP its own loop."""
    return run_async(lambda: mcp_action(world, fault, name, arguments, path))


def dispatch_tool(name, arguments, world, invoice_tool, call_tool):
    """The learner may replace this handoff; call_tool owns the other office tools."""
    if name == 'lookup_invoice':
        return world, invoice_tool(world, **arguments)
    return call_tool(world, name, arguments)


def append_observation(messages, action, result):
    return messages + [{'role': 'assistant', 'content': json.dumps(action)},
                       {'role': 'user', 'content': 'Tool observation: ' + json.dumps(result)}]


def runtime_sources(invoice_tool, dispatch, append):
    return {'lookup_invoice.py': inspect.getsource(invoice_tool),
            'dispatch_tool.py': inspect.getsource(dispatch),
            'append_observation.py': inspect.getsource(append)}


def instrumentation_sources(tool_writer, model_writer):
    return {name:inspect.getsource(function) for name,function in
            (('tool_span.py',tool_writer),('model_span.py',model_writer)) if function is not None}


def run_employee(session, case, harness, label, *, invoice_tool=lookup_invoice, max_steps=10,
                 dispatch=dispatch_tool, append=append_observation, tool_writer=None, model_writer=None, retry_failed=False):
    sources=runtime_sources(invoice_tool, dispatch, append)
    freezes=[s for s in session.completed() if s['name']=='pending/runtime']
    if freezes and freezes[-1]['result']['fingerprint'] != digest(sources):
        raise ValueError('The executor changed after it was frozen. Restore its saved source before comparing harnesses.')
    spec=dict(name=label+'/'+case.id,sources={**harness.files(), **sources},
              inputs={'case_id':case.id,'split':case.split},config={'max_steps':max_steps})
    previous=[s for s in session.read()['stages'].values() if all(s.get(k)==v for k,v in spec.items())]
    completed=[s for s in previous if s['status']=='complete']
    failed=[s for s in previous if s['status']=='failed']
    if retry_failed and not completed and failed:
        session.retry_stage(max(failed,key=lambda s:s['attempt'])['id'])
    with session.stage(**spec) as stage:
        if stage.needs_run:
            world=copy.deepcopy(case.initial)
            messages=build_messages({'mission':case.mission},harness)
            messages[0]['content']+='\nlookup_invoice: {account_id, invoice_id} reads invoice payments and refunds.'
            events=[]; draft=None; status='agent_failure'; last_check=None
            def call_tool(current, name, arguments):
                if name in ('discover_onboarding','onboarding_status','provision_member'):
                    return call_mcp(current,case.fault,name,arguments,stage.output_dir/'office.json')
                return execute(current,name,arguments,case.fault)

            def invoke(name, arguments):
                nonlocal world
                try:
                    world, result = dispatch(name, arguments, world, invoice_tool, call_tool)
                    if not isinstance(result, dict):
                        raise TypeError('Tool dispatch must return (world, result_dict).')
                    return result
                except Exception as error:
                    if name != 'lookup_invoice':
                        receipt=dict(id=stage.id+'/tool-'+str(step),name=name,arguments=arguments,
                            result=None,started_at=started,ended_at=time.time(),
                            error=f'{type(error).__name__}: {error}',error_type=type(error).__name__,status='error')
                        events.append(receipt)
                        stage.record_event(receipt)
                        write_json(stage.output_dir/'partial.json',{'world':world,'events':events,'messages':messages})
                        requests=[r for key,r in session.read()['requests'].items()
                            if key.startswith(stage.id+'/') and r.get('ended_at')]
                        try:
                            export_trace(session,stage.id,case.mission,events,requests,
                                tool_writer=tool_writer,model_writer=model_writer)
                        except Exception:
                            pass  # The failed event is durable even when trace publication is down.
                        raise  # Preserve MCP/runtime failures as unavailable executions.
                    return {'ok':False,'error':str(error)}
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
                elif name=='read_skill':
                    result={'text':{'verify-operation':harness.verification_skill,'office-tools':harness.tool_skill}.get(arguments.get('name'),'Skill not installed')}
                elif name=='check_work':
                    result=check_work(world,case.objective) if case.split=='development' else {'passed':True,'observation':'Review account state against the customer request. Final grading is separate.'}
                    last_check={'state':digest(world),'passed':result['passed']}
                else:
                    result=invoke(name, arguments)
                # Retry only reads. A timed-out write can already have committed.
                if harness.read_retries and result.get('error') and name in ('lookup_invoice','get_account','list_payments','onboarding_status'):
                    events.append(dict(id=stage.id+'/tool-'+str(step)+'-first',name=name,arguments=arguments,
                        result=result,started_at=started,ended_at=time.time(),error=result.get('error')))
                    stage.record_event(events[-1])
                    started=time.time()
                    result=invoke(name, arguments)
                events.append(dict(id=stage.id+'/tool-'+str(step),name=name or 'invalid_action',arguments=arguments,
                    result=result,started_at=started,ended_at=time.time(),error=result.get('error')))
                stage.record_event(events[-1])
                write_json(stage.output_dir/'partial.json',{'world':world,'events':events,'messages':messages})
                messages=append(messages,action,result)
                if not isinstance(messages,list) or any(not isinstance(m,dict) for m in messages):
                    raise TypeError('append_observation must return a list of message dictionaries.')
                write_json(stage.output_dir/'partial.json',{'world':world,'events':events,'messages':messages})
                if status=='complete': break
            run={'world':world,'events':events,'draft':draft,'status':status,'mission':case.mission,
                 'case_id':case.id,'split':case.split,'harness':asdict(harness),'harness_fingerprint':harness.fingerprint,
                 'runtime_fingerprint':digest(sources),'messages':messages,
                 'instrumentation_fingerprint':digest(instrumentation_sources(tool_writer,model_writer))}
            run['scores']=grade(case,run)
            stage.record(run,files=[stage.output_dir/'partial.json'])
    requests=[r for k,r in session.read()['requests'].items() if (k==stage.id or k.startswith(stage.id+'/')) and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,case.mission,stage.result['events'],requests,
                           tool_writer=tool_writer,model_writer=model_writer)
    except Exception as error:
        trace={'status':'unavailable','error':str(error)}
    if stage.needs_run:
        session.checkpoint(label+'/'+case.id,evidence={'Conversation':trace.get('url','')})
    return {**stage.result,'trace':trace,'stage_id':stage.id}


def editor_context(parent, evidence):
    """Separate current observations from lessons learned on earlier tasks."""
    if any(r['split']!='development' for r in evidence):
        raise ValueError('Final cases cannot enter improvement context.')
    executions=[]
    previous=[]
    for run in evidence:
        executions.append({k:run[k] for k in ('case_id','mission','stage_id','events','draft','status','harness','harness_fingerprint') if k in run})
        if run.get('prior_experience'):
            experience=run['prior_experience']
            if not experience.get('source_execution'):
                raise ValueError('Prior experience must identify its source execution.')
            previous.append({k:experience[k] for k in ('source_execution','case_id','lesson','limits') if k in experience})
    return {'parent':asdict(parent),'current_executions':executions,'prior_experience':previous}


def editor_decision(session,number,phase,parent,evidence, *, tool_writer=None, model_writer=None):
    context=editor_context(parent,evidence)
    schema='{"candidates":[DECISION,DECISION]}' if phase=='propose' else 'DECISION'
    mission=('Propose two competing changes using the same starting execution evidence. Candidates do not have separate executions yet; their probes happen next. Retaining the parent remains valid when evidence does not justify an edit.' if phase=='propose' else 'Compare the candidate executions and compose a version to test next. Retain, combine, or reject changes according to the observed evidence.')
    system=mission+' Edit an office agent harness, never the case or tools. Prior experience comes from separately identified earlier tasks; it is a hypothesis to check against this task, not an observation of this execution. Return JSON '+schema+'. DECISION is {decision:CHANGE|KEEP,title,rationale,harness:{instructions,verification_skill,tool_skill,verify_before_finish,read_retries},lesson,limits}. KEEP uses the parent harness exactly. No task-specific account IDs in reusable instructions. '+RULES+TOOL_GUIDE+'\nlookup_invoice: {account_id, invoice_id} reads invoice payments and refunds.'
    name=f'pending/round-{number}/{phase}'
    with session.stage(name,sources={**parent.files(),'editor-system.txt':system},inputs={'prompt_version':2,'evidence':context}) as stage:
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
                {'role':'user','content':json.dumps(context)}],validate,max_tokens=16384)
            decisions=value.get('candidates',[]) if phase=='propose' else [value]
            if len(decisions)!=(2 if phase=='propose' else 1): raise ValueError('Incomplete editing decision')
            for d in decisions:
                if d.get('decision') not in ('CHANGE','KEEP') or not d.get('rationale'): raise ValueError('Need CHANGE/KEEP and rationale')
                proposed=Harness(**d['harness'])
                if d['decision']=='KEEP' and proposed!=parent: raise ValueError('KEEP changed the harness')
                if d['decision']=='CHANGE' and proposed==parent: raise ValueError('No executable change; use KEEP')
                d.update(diff=harness_diff(parent,proposed),fingerprint=proposed.fingerprint)
            stage.record(value)
    requests=[r for k,r in session.read()['requests'].items() if (k==stage.id or k.startswith(stage.id+'/')) and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,mission,[],requests,tool_writer=tool_writer,model_writer=model_writer)
        result={**stage.result,'trace':trace}
    except Exception as error:
        result={**stage.result,'trace':{'status':'unavailable','error':str(error)},'stage_id':stage.id}
    return result


def validate_judgment(judgment):
    if any(type(judgment.get(k)) is not bool for k in ('grounded','complete')) or not isinstance(judgment.get('reason'),str) or not judgment['reason'].strip():
        raise ValueError('Judge returned an invalid structured answer')
    return judgment


def reflect_execution(session, number, run, *, tool_writer=None, model_writer=None):
    """The lesson sees the tested composition, without independent grades."""
    if run['split'] != 'development':
        raise ValueError('Final cases cannot enter reflection context.')
    evidence={k:run[k] for k in ('case_id','mission','events','draft','status','harness','harness_fingerprint')}
    system='Inspect this completed office execution against its actual task and the public rules below. Return JSON {lesson: string, limits: string}. State what the actions support and what they do not. Do not invent unavailable tool fields or additional requirements. Do not infer a quality gain from a procedure name. No grading evidence is supplied.\n'+RULES+TOOL_GUIDE
    def validate(value):
        if any(not isinstance(value.get(k),str) or not value[k].strip() for k in ('lesson','limits')):
            raise ValueError('Reflection needs a lesson and its limits')
    with session.stage(f'pending/round-{number}/reflection',sources={'reflection-system.txt':system},inputs={'execution':run['stage_id'],'prompt_version':2,'evidence':evidence}) as stage:
        if stage.needs_run:
            result,_=validated_json(session,stage.id,[{'role':'system','content':system},
                {'role':'user','content':json.dumps(evidence)}],validate,max_tokens=4096)
            stage.record(result)
    requests=[r for k,r in session.read()['requests'].items() if (k==stage.id or k.startswith(stage.id+'/')) and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,'Reflect on the tested office procedure',[],requests,tool_writer=tool_writer,model_writer=model_writer)
    except Exception as error:
        trace={'status':'unavailable','error':str(error)}
    return {**stage.result,'trace':trace}


def judge_explanation(session,run,rubric, *, validate=validate_judgment, tool_writer=None, model_writer=None, retry_failed=False):
    spec=dict(name='pending/judge/'+run['stage_id'],inputs={'execution':run['stage_id'],'rubric':rubric},
              sources={'validate_judgment.py':inspect.getsource(validate)})
    previous=[s for s in session.read()['stages'].values() if all(s.get(k)==v for k,v in spec.items())]
    completed=[s for s in previous if s['status']=='complete']
    failed=[s for s in previous if s['status']=='failed']
    if retry_failed and not completed and failed:
        if len(failed)>=2:
            raise ValueError('Two explanation-judge attempts failed. Keep this judgment unavailable and inspect its evidence.')
        session.retry_stage(max(failed,key=lambda s:s['attempt'])['id'])
        # Retain the unavailable judgment's native trace before requesting another one.
        for row in failed:
            requests=[r for k,r in session.read()['requests'].items() if (k==row['id'] or k.startswith(row['id']+'/')) and r.get('ended_at')]
            try: export_trace(session,row['id'],'Judge the saved explanation; prior failed attempt',[],requests,tool_writer=tool_writer,model_writer=model_writer)
            except Exception: pass  # Raw failed requests remain saved even when export is unavailable.
    with session.stage(**spec) as stage:
        if stage.needs_run:
            call=Provider(session).complete(stage.id,[{'role':'system','content':'Judge explanation against actual recorded actions. Return JSON {grounded: boolean, complete: boolean, reason: string}. '+rubric},
                {'role':'user','content':json.dumps({'mission':run['mission'],'events':run['events'],'draft':run['draft']})}],max_tokens=4096)
            judgment=output(call)
            validate(judgment)
            validate_judgment(judgment)
            stage.record(judgment)
    requests=[r for k,r in session.read()['requests'].items() if (k==stage.id or k.startswith(stage.id+'/')) and r.get('ended_at')]
    try:
        trace=export_trace(session,stage.id,stage.name,[],requests,tool_writer=tool_writer,model_writer=model_writer)
        result={**stage.result,'trace':trace,'stage_id':stage.id}
    except Exception as error:
        result={**stage.result,'trace':{'status':'unavailable','error':str(error)},'stage_id':stage.id}
    return result
