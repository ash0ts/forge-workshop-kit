"""Forge scopes over durable operation records, with stored-span readback."""
from __future__ import annotations
import json
import time
from datetime import datetime, timezone
import httpx
from .publication import credentials
from .session import digest


def stamp(value):
    return datetime.fromtimestamp(value, timezone.utc)


def stored_spans(project, trace_id, *, expected, timeout=25):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        response = httpx.post('https://trace.wandb.ai/agents/spans/query',
            auth=('api', credentials()), timeout=20, json={'project_id': project,
            'query': {'$expr': {'$eq': [{'$getField': 'trace_id'}, {'$literal': trace_id}]}},
            'include_details': True, 'include_costs': True, 'limit': 1000})
        response.raise_for_status()
        rows = response.json().get('spans', [])
        if len(rows) >= expected:
            return rows
        time.sleep(1)
    raise RuntimeError('Stored trace is incomplete. Retry readback/export; do not repeat the execution.')


def export_trace(session, identity, mission, events, requests=(), *, tool_writer=None):
    from coreweave.forge.agentlens import tracing as tracing
    from opentelemetry import trace
    key = 'trace/' + identity
    prior = session.read()['publications'].get(key)
    if prior and prior.get('verified'):
        return prior
    # An interrupted export first checks its original trace. No paid work occurs here.
    if prior and prior.get('trace_id'):
        try:
            return verify_trace(session, key, prior, events, requests)
        except RuntimeError:
            pass
    sdk = tracing.init(session.project, service_name='forge-workshop-kit', autopatch_integrations=False)
    conversation_id = identity
    times = [r['started_at'] for r in requests] + [e['started_at'] for e in events]
    ends = [r['ended_at'] for r in requests] + [e['ended_at'] for e in events]
    with tracing.Conversation(conversation_id=conversation_id,
        conversation_name=f'{session.workshop} / {identity}', attributes={
            'workshop.id': session.workshop, 'workshop.workspace': session.workspace_id,
            'workshop.release': session.version}):
        with tracing.Turn(agent_name='researcher' if requests else 'participant',
            messages=[tracing.Message(role='user', content=mission)],
            started_at=stamp(min(times) if times else time.time()),
            ended_at=stamp(max(ends) if ends else time.time())):
            tid = format(trace.get_current_span().get_span_context().trace_id, '032x')
            receipt = dict(trace_id=tid, conversation_id=conversation_id, verified=False,
                expected=1 + len(events) + len(requests),
                url=f'https://forge.coreweave.com/agent-lens/{session.project}/conversations/{conversation_id}',
                span_ids={})
            with session.transaction() as state:
                state['publications'][key] = receipt
            for record in requests:
                req, res = record['request'], record.get('response') or {}
                choice = (res.get('choices') or [{}])[0]
                llm = tracing.LLM(model=req['model'], provider_name='wandb', response_id=res.get('id',''),
                    response_model=res.get('model',''), request_max_tokens=req['max_tokens'],
                    request_temperature=req['temperature'],
                    system_instructions=[m['content'] for m in req['messages'] if m['role'] == 'system'],
                    input_messages=[tracing.Message(role=m['role'],content=m['content'])
                                    for m in req['messages'] if m['role'] != 'system'],
                    output_messages=[tracing.Message(role='assistant', content=choice.get('message',{}).get('content') or '')],
                    started_at=stamp(record['started_at']), ended_at=stamp(record['ended_at']))
                usage = res.get('usage') or {}
                if all(type(usage.get(k)) is int for k in ('prompt_tokens','completion_tokens')):
                    llm.usage = tracing.Usage(input_tokens=usage['prompt_tokens'], output_tokens=usage['completion_tokens'])
                with llm:
                    llm.set_attributes({'workshop.request_id': record['id'], 'workshop.usage_available': bool(usage)})
                    if record.get('error'):
                        llm.record_error(RuntimeError(record['error']))
            for event in events:
                if tool_writer is not None:
                    receipt['span_ids'][event['id']] = tool_writer(event)
                    continue
                with tracing.Tool(name=event['name'], arguments=event['arguments'], result=event['result'],
                    tool_call_id=event['id'], started_at=stamp(event['started_at']), ended_at=stamp(event['ended_at'])) as tool:
                    receipt['span_ids'][event['id']] = format(trace.get_current_span().get_span_context().span_id, '016x')
                    if event.get('error'):
                        tool.record_error(RuntimeError(event['error']))
            with session.transaction() as state:
                state['publications'][key] = receipt
    if not sdk.force_flush():
        raise RuntimeError('Trace export did not finish. Execution is saved; retry export.')
    return verify_trace(session, key, receipt, events, requests)


def verify_trace(session, key, receipt, events, requests):
    rows = stored_spans(session.project, receipt['trace_id'], expected=receipt['expected'])
    tools = [r for r in rows if r.get('operation_name') == 'execute_tool']
    calls = [r for r in rows if r.get('operation_name') == 'chat']
    if len(tools) != len(events) or len(calls) != len(requests):
        raise RuntimeError('Stored span coverage does not match the independent receipts.')
    for event in events:
        matching = [r for r in tools if r.get('tool_call_id') == event['id']]
        if len(matching) != 1:
            raise RuntimeError('Missing or duplicate tool span')
        for field, value in [('tool_call_arguments', event['arguments']), ('tool_call_result', event['result'])]:
            actual = matching[0].get(field)
            actual = json.loads(actual or '{}') if isinstance(actual, str) else actual
            if actual != value:
                raise RuntimeError('Stored tool arguments/result differ from the actual operation.')
    for request in requests:
        matching = [r for r in calls if r.get('response_id') == request.get('response',{}).get('id')]
        if request.get('response',{}).get('id') and len(matching) != 1:
            raise RuntimeError('Missing provider response span')
        if matching:
            row = matching[0]
            if row.get('request_model') != request['request']['model']:
                raise RuntimeError('Stored model differs')
            for source, dest in [('prompt_tokens','input_tokens'), ('completion_tokens','output_tokens')]:
                usage = request.get('response',{}).get('usage') or {}
                if source in usage and row.get(dest) != usage[source]:
                    raise RuntimeError('Stored usage differs')
    receipt.update(verified=True, stored_spans=len(rows))
    with session.transaction() as state:
        state['publications'][key] = receipt
    return receipt


def event(name, arguments, action, *, event_id=None):
    """Use in visible learner instrumentation; returns both result and independent receipt."""
    started = time.time()
    result = action()
    return result, dict(id=event_id or digest([name, arguments, started])[:24], name=name,
        arguments=arguments, result=result, started_at=started, ended_at=time.time())
