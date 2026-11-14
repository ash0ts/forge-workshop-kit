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


def export_trace(session, identity, mission, events, requests=(), *, tool_writer=None,
                 model_writer=None):
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
    stage = session.read()['stages'].get(identity, {})
    stage_name = stage.get('name', mission)
    with tracing.Conversation(conversation_id=conversation_id,
        conversation_name=f'{session.workshop} / {stage_name}', attributes={
            'workshop.id': session.workshop, 'workshop.workspace': session.workspace_id,
            'workshop.release': session.version, 'workshop.stage': stage_name,
            'workshop.source_fingerprint': stage.get('source_fingerprint', '')}):
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
                if model_writer is not None:
                    model_writer(record)
                    continue
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
                if not isinstance(usage, dict):
                    usage = {}
                measured_usage = all(type(usage.get(k)) is int and usage[k] >= 0
                                     for k in ('prompt_tokens','completion_tokens'))
                if measured_usage:
                    llm.usage = tracing.Usage(input_tokens=usage['prompt_tokens'], output_tokens=usage['completion_tokens'])
                with llm:
                    llm.set_attributes({'workshop.request_id': record['id'], 'workshop.usage_available': measured_usage})
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
                        if event.get('error_type'):
                            tool.set_attributes({'error.type': event['error_type']})
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
            if isinstance(actual, str):
                # Forge omits the serialized result when a raised tool call returned nothing.
                actual = json.loads(actual) if actual else (None if field == 'tool_call_result' and value is None else {})
            if actual != value:
                raise RuntimeError('Stored tool arguments/result differ from the actual operation.')
    for request in requests:
        matching = [r for r in calls if r.get('response_id') == (request.get('response') or {}).get('id')]
        if (request.get('response') or {}).get('id') and len(matching) != 1:
            raise RuntimeError('Missing provider response span')
        if matching:
            row = matching[0]
            if row.get('request_model') != request['request']['model']:
                raise RuntimeError('Stored model differs')
            usage = (request.get('response') or {}).get('usage') or {}
            measured_usage = isinstance(usage, dict) and all(
                type(usage.get(key)) is int and usage[key] >= 0
                for key in ('prompt_tokens', 'completion_tokens'))
            for source, dest in [('prompt_tokens','input_tokens'), ('completion_tokens','output_tokens')]:
                if measured_usage and row.get(dest) != usage[source]:
                    raise RuntimeError('Stored usage differs')
    receipt.update(verified=True, stored_spans=len(rows))
    with session.transaction() as state:
        state['publications'][key] = receipt
    return receipt


def saved_trace_inputs(session, stage_or_id):
    """Collect one copy of each saved event and every ended provider attempt."""
    state = session.read()
    row = state['stages'][stage_or_id] if isinstance(stage_or_id, str) else stage_or_id
    result = row.get('result') or {}
    events = {}
    for receipt in [*result.get('events', []), *row.get('events', [])]:
        identity = receipt['id']
        if identity in events and events[identity] != receipt:
            raise ValueError('Conflicting saved tool events share one identity; review the receipts before export.')
        events[identity] = receipt
    requests = [request for key, request in state['requests'].items()
                if (key == row['id'] or key.startswith(row['id'] + '/')
                    or key == result.get('request_id')) and request.get('ended_at') is not None]
    requests.sort(key=lambda request: (request.get('started_at', 0), request.get('id', '')))
    mission = result.get('mission')
    if not mission:
        mission = next((message['content'] for request in requests
                        for message in request['request'].get('messages', [])
                        if message.get('role') == 'user'), row['name'])
    return {'identity': row['id'], 'mission': mission,
            'events': sorted(events.values(), key=lambda event: (event['started_at'], event['id'])),
            'requests': requests}


def event(name, arguments, action, *, event_id=None, on_error=None):
    """Return an independent receipt, or persist a raised error before reraising it."""
    started = time.time()
    receipt = dict(id=event_id or digest([name, arguments, started])[:24], name=name,
                   arguments=arguments, started_at=started)
    try:
        result = action()
    except BaseException as error:
        receipt.update(result=None, ended_at=time.time(), status='error',
                       error=f'{type(error).__name__}: {error}', error_type=type(error).__name__)
        error.workshop_event = receipt
        if on_error is not None:
            try:
                on_error(receipt)
            except Exception as save_error:
                # A storage error must not turn a tool failure into a different exception.
                error.add_note(f'Error receipt could not be saved: {save_error}')
        raise
    receipt.update(result=result, ended_at=time.time(), status='complete')
    return result, receipt
