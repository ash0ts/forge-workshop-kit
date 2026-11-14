import pytest
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.traces import event


def test_raised_tool_error_is_saved_and_original_exception_reraises(tmp_path):
    session = WorkshopSession('test/project', 'lab', state_dir=tmp_path)
    original = TimeoutError('write committed before timeout')
    def action():
        raise original
    with pytest.raises(TimeoutError) as failure:
        with session.stage('tool') as stage:
            event('provision_member', {'operation_id': 'join-alex'}, action,
                  event_id='tool-1', on_error=stage.record_event)
    assert failure.value is original
    saved = session.read()['stages'][stage.id]
    assert saved['status'] == 'failed'
    receipt = saved['events'][0]
    assert receipt['id'] == 'tool-1'
    assert receipt['arguments'] == {'operation_id': 'join-alex'}
    assert receipt['result'] is None and receipt['status'] == 'error'
    assert receipt['error_type'] == 'TimeoutError'
    assert receipt['ended_at'] >= receipt['started_at']
    assert original.workshop_event == receipt


def test_failed_receipt_storage_does_not_replace_tool_error():
    original = ValueError('tool failure')
    def action():
        raise original
    def fail_store(receipt):
        raise OSError('disk unavailable')
    with pytest.raises(ValueError) as failure:
        event('lookup', {}, action, on_error=fail_store)
    assert failure.value is original
    assert 'disk unavailable' in original.__notes__[0]


def test_successful_event_records_actual_result():
    result, receipt = event('lookup', {'invoice': 'a'}, lambda: {'amount': 42})
    assert result == receipt['result'] == {'amount': 42}
    assert receipt['status'] == 'complete'
    assert 'error' not in receipt


def test_saved_trace_inputs_deduplicates_events_and_keeps_failed_requests(tmp_path):
    from forge_workshop_kit.traces import saved_trace_inputs
    session = WorkshopSession('test/project', 'lab', state_dir=tmp_path)
    receipt = {'id': 'tool-0', 'name': 'lookup', 'arguments': {}, 'result': {},
               'started_at': 1, 'ended_at': 2}
    with session.stage('tool') as stage:
        stage.record_event(receipt)
        stage.record({'events': [receipt]})
    with session.transaction() as state:
        state['requests'][stage.id + '/0'] = {'id': stage.id + '/0', 'started_at': 3,
            'ended_at': 4, 'status': 'failed', 'response': None,
            'request': {'messages': [{'role': 'user', 'content': 'Actual request'}]}}
        state['requests'][stage.id + '/1'] = {'id': stage.id + '/1', 'status': 'pending'}
    saved = saved_trace_inputs(session, stage.id)
    assert saved['events'] == [receipt]
    assert len(saved['requests']) == 1 and saved['requests'][0]['status'] == 'failed'
    assert saved['mission'] == 'Actual request'
    with session.transaction() as state:
        state['stages'][stage.id]['events'][0]['result'] = {'different': True}
    with pytest.raises(ValueError, match='Conflicting saved tool events'):
        saved_trace_inputs(session, stage.id)


def test_null_result_from_raised_tool_error_matches_forge_empty_field(tmp_path, monkeypatch):
    from forge_workshop_kit import traces
    session = WorkshopSession('test/project', 'lab', state_dir=tmp_path)
    receipt = {'trace_id': 'trace-id', 'expected': 2}
    observed = {'id': 'tool-0', 'arguments': {'fixture': True}, 'result': None,
                'error': 'TimeoutError: test'}
    monkeypatch.setattr(traces, 'stored_spans', lambda *args, **kwargs: [
        {'operation_name': 'turn'}, {'operation_name': 'execute_tool', 'tool_call_id': 'tool-0',
         'tool_call_arguments': '{"fixture": true}', 'tool_call_result': ''}])
    assert traces.verify_trace(session, 'trace/test', receipt, [observed], [])['verified']


def test_failed_worker_keeps_its_actual_role_and_task_context(tmp_path):
    from forge_workshop_kit.traces import saved_trace_inputs
    session = WorkshopSession('test/project', 'transit-factory', state_dir=tmp_path)
    context = {'agent_name': 'builder-2', 'worker_id': 'builder-2',
               'task_id': 'presentation', 'dispatch_id': 'claim-1'}
    with pytest.raises(TimeoutError):
        with session.stage('factory/build/team/worker/presentation', inputs={
                'mission': 'Render the departure board', 'trace_context': context}) as stage:
            raise TimeoutError('The worker stopped before returning a patch')
    saved = saved_trace_inputs(session, stage.id)
    assert saved['mission'] == 'Render the departure board'
    assert all(saved[key] == value for key, value in context.items())
    assert 'parent_conversation_id' not in saved
