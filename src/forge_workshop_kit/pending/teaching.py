"""Presentation state and free checks for the direct Pending notebook.

The editable functions are ordinary Python, not a security sandbox. Runtime
fingerprints bind comparisons to the tested executor; the editor only edits
the harness. No function in this module calls a model.
"""
import copy
import json
import linecache

from ..session import digest
from .cases import CASES
from .harness import Harness
from .loop import runtime_sources


from forge_workshop_kit.manifest import get_workshop
STEPS = tuple(tuple(step) for step in get_workshop("pending-direct-teaching")["steps"])

STARTERS = {
    'tool': '''def my_invoice_tool(state, account_id, invoice_id):
    account = state["accounts"][account_id]
    # Return payments for this invoice, plus the account's refunds.
    # Reading an invoice must not change the account.
    raise NotImplementedError("Filter account['payments'] by invoice_id")
''',
    'loop': '''def my_dispatch(name, arguments, world, invoice_tool, call_tool):
    # Route lookup_invoice to your function. Delegate other names to call_tool.
    # Both paths return (world, result).
    raise NotImplementedError("Connect the chosen action to its Python tool")

def my_observation(messages, action, result):
    # Return a new message list with the action and its actual result appended.
    # json.dumps is available. Do not mutate the earlier request.
    raise NotImplementedError("Put the tool observation into the next request")
''',
    'scorer': '''def my_state_check(run):
    # Inspect account state, never the employee's claim of success.
    if run["case_id"] == "double-charge":
        refunds = run["world"]["accounts"]["acme"]["refunds"]
        raise NotImplementedError("Require exactly one full 4900-cent refund")
    return run["world"]["accounts"]["fern"]["members"] == [
        {"email": "alex@example.test", "role": "member"}]

def my_judge_validation(answer):
    # Require boolean grounded/complete and a nonempty string reason.
    # Raise ValueError for an invalid answer. Return the valid dictionary.
    raise NotImplementedError("Validate the judge's structured answer")
''',
    'instrumentation': '''def my_tool_span(record):
    from coreweave.forge.agentlens import tracing
    from opentelemetry import trace
    from forge_workshop_kit.traces import stamp
    with tracing.Tool(name=record["name"], arguments=record["arguments"],
        result=record["result"], tool_call_id=record["id"],
        started_at=stamp(record["started_at"]), ended_at=stamp(record["ended_at"])) as span:
        if record.get("error"):
            span.record_error(RuntimeError(record["error"]))
        return format(trace.get_current_span().get_span_context().span_id, "016x")

def my_model_span(record):
    from coreweave.forge.agentlens import tracing
    from forge_workshop_kit.traces import stamp
    req, response = record["request"], record.get("response") or {}
    choice = (response.get("choices") or [{}])[0]
    span = tracing.LLM(model=req["model"], provider_name="wandb",
        response_id=response.get("id", ""), response_model=response.get("model", ""),
        request_max_tokens=req["max_tokens"], request_temperature=req["temperature"],
        system_instructions=[m["content"] for m in req["messages"] if m["role"] == "system"],
        input_messages=[tracing.Message(role=m["role"], content=m["content"])
            for m in req["messages"] if m["role"] != "system"],
        output_messages=[tracing.Message(role="assistant", content=choice.get("message", {}).get("content") or "")],
        started_at=stamp(record["started_at"]), ended_at=stamp(record["ended_at"]))
    usage = response.get("usage") or {}
    if all(type(usage.get(k)) is int for k in ("prompt_tokens", "completion_tokens")):
        span.usage = tracing.Usage(input_tokens=usage["prompt_tokens"], output_tokens=usage["completion_tokens"])
    with span:
        span.set_attributes({"workshop.request_id": record["id"], "workshop.usage_available": bool(usage)})
        if record.get("error"):
            span.record_error(RuntimeError(record["error"]))
''',
}

ANSWERS = {
    'tool': '''def my_invoice_tool(state, account_id, invoice_id):
    account = state["accounts"][account_id]
    return {"payments": [p for p in account["payments"] if p["invoice_id"] == invoice_id],
            "refunds": account["refunds"]}
''',
    'loop': '''def my_dispatch(name, arguments, world, invoice_tool, call_tool):
    if name == "lookup_invoice":
        return world, invoice_tool(world, **arguments)
    return call_tool(world, name, arguments)

def my_observation(messages, action, result):
    return messages + [{"role": "assistant", "content": json.dumps(action)},
        {"role": "user", "content": "Tool observation: " + json.dumps(result)}]
''',
    'scorer': '''def my_state_check(run):
    if run["case_id"] == "double-charge":
        refunds = run["world"]["accounts"]["acme"]["refunds"]
        return len(refunds) == 1 and refunds[0]["amount_cents"] == 4900
    return run["world"]["accounts"]["fern"]["members"] == [
        {"email": "alex@example.test", "role": "member"}]

def my_judge_validation(answer):
    if any(type(answer.get(k)) is not bool for k in ("grounded", "complete")):
        raise ValueError("grounded and complete must be booleans")
    if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
        raise ValueError("The judge must explain its answer")
    return answer
''',
}


def compile_code(source):
    """Preserve source for inspect.getsource and execution fingerprinting."""
    filename = '<pending-learner-' + digest(source)[:24] + '>'
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    namespace = {'json': json}
    exec(compile(source, filename, 'exec'), namespace)
    return namespace


def functions(session):
    namespace = {}
    for name in ('tool', 'loop', 'instrumentation', 'scorer'):
        namespace.update(compile_code(session.get_draft('pending/'+name, STARTERS[name])))
    return namespace


def hooks(namespace):
    return {'invoice_tool': namespace['my_invoice_tool'], 'dispatch': namespace['my_dispatch'],
            'append': namespace['my_observation'], 'tool_writer': namespace['my_tool_span'],
            'model_writer': namespace['my_model_span']}


def check_tool(function):
    world = copy.deepcopy(next(c for c in CASES if c.id == 'double-charge').initial)
    before = copy.deepcopy(world)
    rows = []
    for account, invoice, expected in [('acme','inv-1',2), ('acme','missing',0), ('other-account','inv-1',2)]:
        result = function(world, account, invoice)
        assert len(result['payments']) == expected, f'{account}/{invoice}: expected {expected} payments'
        assert result['refunds'] == world['accounts'][account]['refunds'], 'Return the selected account refunds'
        assert world == before, 'A lookup must not change account state'
        rows.append({'Account': account, 'Invoice': invoice, 'Payments': expected, 'Check': 'Passed'})
    return rows


def check_loop(dispatch, append, invoice_tool):
    world = copy.deepcopy(next(c for c in CASES if c.id == 'double-charge').initial)
    observed = []
    def other(current, name, arguments):
        observed.append(name)
        return current, {'delegated': name}
    action = {'action':'lookup_invoice','arguments':{'account_id':'acme','invoice_id':'inv-1'}}
    after, result = dispatch(action['action'], action['arguments'], world, invoice_tool, other)
    assert len(result['payments']) == 2 and after == world, 'Dispatch must execute your invoice function'
    _, delegated = dispatch('get_account', {'account_id':'acme'}, world, invoice_tool, other)
    assert observed == ['get_account'] and delegated == {'delegated':'get_account'}, 'Delegate other tools'
    messages = [{'role':'user','content':'Inspect this invoice'}]
    updated = append(messages, action, result)
    assert messages == [{'role':'user','content':'Inspect this invoice'}], 'Preserve the previous request'
    assert len(updated) == 3 and updated[:1] == messages, 'Append action and observation'
    assert json.loads(updated[-2]['content']) == action, 'Include the selected action'
    assert updated[-1]['role'] == 'user' and json.dumps(result) in updated[-1]['content'], 'Include the actual tool result'
    return {'action':action, 'result':result, 'next_request':updated}


def check_scorer(check, validate):
    world = copy.deepcopy(next(c for c in CASES if c.id == 'double-charge').initial)
    def example(refunds):
        state = copy.deepcopy(world)
        state['accounts']['acme']['refunds'] = refunds
        return {'case_id':'double-charge','world':state,'draft':{'summary':'Everything is resolved.'}}
    samples = [('Full refund',[{'amount_cents':4900}],True),
               ('Partial refund',[{'amount_cents':100}],False),('False completion claim',[],False),
               ('Duplicate refund',[{'amount_cents':4900},{'amount_cents':4900}],False)]
    rows = []
    for label, refunds, expected in samples:
        actual = check(example(refunds))
        assert type(actual) is bool and actual == expected, f'{label}: expected {expected}'
        rows.append({'Example':label,'State check':actual})
    validate({'grounded':True,'complete':False,'reason':'Missing a final state check.'})
    for invalid in ({'grounded':'yes','complete':True,'reason':'Looks good'}, {'grounded':True,'complete':True,'reason':''}):
        try:
            validate(invalid)
        except (ValueError, TypeError):
            continue
        raise AssertionError('Reject invalid structured judge answers')
    return rows


def freeze_runtime(session, namespace):
    check_tool(namespace['my_invoice_tool'])
    check_loop(namespace['my_dispatch'], namespace['my_observation'], namespace['my_invoice_tool'])
    sources = runtime_sources(namespace['my_invoice_tool'], namespace['my_dispatch'], namespace['my_observation'])
    prior = latest(session, 'pending/runtime')
    if prior and prior['result']['fingerprint'] != digest(sources):
        raise ValueError('Runtime already frozen. Restore the saved tool and loop source for the comparison.')
    with session.stage('pending/runtime', sources=sources) as stage:
        if stage.needs_run:
            stage.record({'fingerprint':digest(sources)})
    return stage.result


def latest(session, name):
    rows = [s for s in session.completed() if s['name'] == name]
    return max(rows, key=lambda s:s.get('ended_at',s.get('started_at',0)), default=None)


def saved(session, name):
    row = latest(session, name)
    if row is None:
        raise ValueError('Complete '+name+' first')
    return row['result']


def trace_receipt(session, identity):
    return session.read()['publications'].get('trace/'+identity, {'status':'not exported'})


def setup_verified(session):
    row=latest(session,'pending/setup-trace')
    return bool(row and row['sources'].get('instrumentation.py') == session.get_draft('pending/instrumentation',STARTERS['instrumentation'])
                and trace_receipt(session,row['id']).get('verified'))


def check_status(session, name, sources=None):
    """A passed check only applies to exactly the source it checked."""
    if session is None: return {'passed':False,'state':'Not checked'}
    if sources is None:
        sources={
            'tool':{'lookup_invoice.py':session.get_draft('pending/tool',STARTERS['tool'])},
            'loop':{'lookup_invoice.py':session.get_draft('pending/tool',STARTERS['tool']),
                    'loop.py':session.get_draft('pending/loop',STARTERS['loop'])},
            'scorer':{'scorer.py':session.get_draft('pending/scorer',STARTERS['scorer'])},
        }[name]
    row=latest(session,'pending/check-'+name)
    if not row: return {'passed':False,'state':'Not checked'}
    matches=row['sources']==sources
    return {**row['result'],'passed':matches,'state':'Passed for this code' if matches else 'Code changed; run the check again',
            'stage_id':row['id']}


def execution(session, row):
    return {**row['result'], 'stage_id':row['id'], 'trace':trace_receipt(session,row['id'])}


def restore(session):
    result = {'session':session,'checks':{name:check_status(session,name) for name in ('tool','loop','scorer')}}
    for label, key in [('original','original'),('manual','manual_runs')]:
        rows = []
        for case in (c for c in CASES if c.split == 'development'):
            row = latest(session, f'pending/{label}/{case.id}')
            if row: rows.append(execution(session,row))
        if rows: result[key] = rows
        if len(rows) == 2: result['starting' if label=='original' else 'manual'] = Harness(**rows[0]['harness'])
    for key,name in [('final','pending/final-comparison'),('evaluation','pending/development-evaluation'),('report','pending/report')]:
        row=latest(session,name)
        if row: result[key]=row['result']
    return result


PHASES = [('propose','Ask for two competing changes'),('probe-a','Review and test candidate A'),
          ('probe-b','Review and test candidate B'),('compose','Compare probes and request a composition'),
          ('composition-test','Review and test the composition'),('adopted','Save the tested version and its lesson')]


def next_phase(session):
    for number in (1,2):
        prefix=f'pending/round-{number}/'
        if latest(session,prefix+'adopted'): continue
        for phase,label in PHASES:
            if not latest(session,prefix+phase): return number,phase,label
    return 2,'done','Both improvement rounds are complete'


def active_decision(session, number, phase):
    prefix=f'pending/round-{number}/'
    if phase in ('probe-a','probe-b'):
        return saved(session,prefix+'propose')['candidates'][0 if phase=='probe-a' else 1]
    if phase=='composition-test': return saved(session,prefix+'compose')
    return None


def review_decision(session, decision):
    fingerprint=Harness(**decision['harness']).fingerprint
    if fingerprint != decision['fingerprint']: raise ValueError('Decision fingerprint differs from its files')
    review_key=digest({'fingerprint':fingerprint,'decision':decision})
    with session.stage('pending/review/'+review_key,inputs={'decision':decision}) as stage:
        if stage.needs_run: stage.record({'fingerprint':fingerprint,'reviewed':True})
    return review_key


def comparison_rows(executions):
    versions={}
    for label,runs in executions.items():
        rows=[]
        for run in runs:
            judgment=run.get('explanation_judgment',{})
            rows.append({'case_id':run['case_id'],'input':run['mission'],'prediction':run['draft'],
                'target':'Independent account-state check','error':None if run['scores']['task_success'] is None else 1-int(run['scores']['task_success']),
                'scores':{k:None if k not in judgment else int(judgment[k]) for k in ('grounded','complete')},
                'explanation_judgment':judgment,
                'evidence':{'conversation':run['trace'],'fingerprint':run['harness_fingerprint'],'stage':run['stage_id']}})
        versions[label]=rows
    return versions


def summary_rows(runs, label=None):
    return [{'Version':label or 'Starting harness','Case':r['case_id'],'Execution':r['status'],
             'Correct account':r['scores'].get('task_success'),'Tool calls':len(r['events']),
             'Grounded explanation':r.get('explanation_judgment',{}).get('grounded'),
             'Harness':r['harness_fingerprint'][:12],
             'Conversation':r.get('trace',{}).get('url','Not exported')} for r in runs]


def tool_rows(run):
    rows=[]
    for index,event in enumerate(run['events']):
        result=event['result']
        if event.get('error'):
            detail=event['error']
        elif 'payments' in result:
            detail=f"{len(result['payments'])} payments; {len(result.get('refunds',[]))} refunds"
        elif result.get('accepted'):
            detail='Final explanation saved; correctness is checked separately'
        elif result.get('replayed'):
            detail='Previously committed operation returned without another write'
        elif 'text' in result:
            detail='Installed skill loaded'
        elif 'tools' in result:
            detail=f"{len(result['tools'])} MCP tools discovered"
        elif 'members' in result:
            detail=f"{len(result['members'])} current members"
        else:
            detail='Observation saved; open this event to inspect the returned state'
        rows.append({'Step':index+1,'Tool':event['name'],'Outcome':'Error' if event.get('error') else 'Returned',
                     'Observation':str(detail)[:160]})
    return rows
