import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from typing import ClassVar

import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.factory import (
    FactoryStop,
    FactoryTask,
    MemoryEntry,
    TaskBoard,
    file_hash,
    freeze_release,
    load_board,
    ready_tasks,
    reproduce_release,
    retrieve_memory,
    run_build,
    worker_context,
)
from forge_workshop_kit.provider import MODEL, ProviderStop
from forge_workshop_kit.session import digest

SOURCES = {'query.py': 'value = 0\n', 'presentation.py': 'value = 0\n',
           'contract.md': 'Keep the interface stable. Public development information only.'}


def tasks(shared=False, dependent=False):
    return [FactoryTask('query', 'Find departures', 'Implement query', ('query.py',), tags=('time',)),
            FactoryTask('view', 'Show departures', 'Implement view',
                        ('query.py' if shared else 'presentation.py',),
                        depends_on=('query',) if dependent else (), tags=('time',))]


def board(tmp_path, **kwargs):
    return TaskBoard(tmp_path / 'board', tasks(**kwargs), SOURCES)


def passing(workspace, task):
    return {'passed': True, 'checks': [{'name': 'public-contract', 'passed': True}]}


def propose(board, task_id, replacement='value = 1\n'):
    claim = board.claim(task_id, task_id + '-worker')
    path = claim['spec']['editable_files'][0]
    source = board.read_file(task_id, claim['dispatch_id'], path)
    board.write_file(task_id, claim['dispatch_id'], path, replacement, source['sha256'])
    board.test(task_id, claim['dispatch_id'], passing)
    return board.submit(task_id, claim['dispatch_id'], 'Implemented and tested the assigned function.')


def accept(board, task_id):
    row = board.snapshot()['tasks'][task_id]
    return board.integrate(task_id, reviewer='participant', expected_patch_digest=digest(row['patch']))


def test_dependencies_require_integration_not_worker_finish(tmp_path):
    b = board(tmp_path, dependent=True)
    assert ready_tasks(b.snapshot()['tasks']) == ['query']
    proposal = propose(b, 'query')
    assert proposal['status'] == 'review'
    assert ready_tasks(b.snapshot()['tasks']) == []
    accept(b, 'query')
    assert ready_tasks(b.snapshot()['tasks']) == ['view']


def test_claim_is_atomic_and_does_not_reclaim_a_live_worker(tmp_path):
    b = board(tmp_path)
    def claim(index):
        try:
            return b.claim('query', 'worker-' + str(index))
        except FactoryStop:
            return None
    with ThreadPoolExecutor(max_workers=4) as pool:
        claims = list(pool.map(claim, range(4)))
    assert sum(row is not None for row in claims) == 1


def test_isolation_and_conflict_preserve_both_patches(tmp_path):
    b = board(tmp_path, shared=True)
    first = propose(b, 'query', 'value = 1\n')
    second = propose(b, 'view', 'value = 2\n')
    assert first['patch']['query.py']['before_sha256'] == second['patch']['query.py']['before_sha256']
    assert b.snapshot()['sources'] == SOURCES
    accept(b, 'query')
    with pytest.raises(FactoryStop, match='conflict'):
        accept(b, 'view')
    assert b.snapshot()['sources']['query.py'] == 'value = 1\n'
    assert b.snapshot()['tasks']['view']['patch']['query.py']['content'] == 'value = 2\n'


def test_paths_before_hash_and_current_test_receipt_are_required(tmp_path):
    b = board(tmp_path)
    claim = b.claim('query', 'builder')
    dispatch = claim['dispatch_id']
    with pytest.raises(ValueError):
        b.write_file('query', dispatch, '../outside.py', 'x', 'bad')
    with pytest.raises(ValueError, match='permit'):
        b.write_file('query', dispatch, 'presentation.py', 'x', file_hash(SOURCES['presentation.py']))
    b.test('query', dispatch, passing)
    b.write_file('query', dispatch, 'query.py', 'value = 2\n', file_hash(SOURCES['query.py']))
    with pytest.raises(FactoryStop, match='current files'):
        b.submit('query', dispatch, 'Done')
    with pytest.raises(FactoryStop, match='changed since'):
        b.write_file('query', dispatch, 'query.py', 'value = 3\n', file_hash(SOURCES['query.py']))
    b.test('query', dispatch, passing)
    assert b.submit('query', dispatch, 'Now tested')['decision'] == 'CHANGE'


def test_keep_is_a_tested_decision_without_a_patch(tmp_path):
    b = board(tmp_path)
    claim = b.claim('query', 'builder')
    b.test('query', claim['dispatch_id'], passing)
    result = b.submit('query', claim['dispatch_id'], 'Existing function meets this task.')
    assert result['decision'] == 'KEEP' and result['patch'] == {}
    accept(b, 'query')
    assert b.snapshot()['sources'] == SOURCES


def test_a_test_runner_cannot_change_the_source_it_approves(tmp_path):
    b = board(tmp_path)
    claim = b.claim('query', 'builder')
    def changing_test(workspace, task):
        (workspace / 'query.py').write_text('value = 8\n')
        return {'passed': True}
    with pytest.raises(FactoryStop, match='Tests changed'):
        b.test('query', claim['dispatch_id'], changing_test)


def lesson(**changes):
    value = asdict(MemoryEntry('hours', 'Preserve hours above 24 in service time.', ('time',),
        'transit', 'transit-v1', 'observed-code-hash', ('execution-1/tool-2',),
        status='accepted', reviewer='participant', limits='Applies to GTFS service-time fields.'))
    return {**value, **changes}


def test_memory_selection_preserves_provenance_and_filters_applicability(tmp_path):
    entries = [lesson(), lesson(id='stale', version='transit-v0'),
               lesson(id='guess', status='proposed', reviewer=''),
               lesson(id='other', scope='banking'), lesson(id='colors', tags=('colors',))]
    b = board(tmp_path)
    for entry in entries:
        b.add_memory(entry)
    chosen = b.memories(tasks()[0])
    assert chosen == [json.loads(json.dumps(entries[0]))]
    assert chosen[0]['source_revision'] == 'observed-code-hash'
    with pytest.raises(ValueError, match='applicable'):
        b.memories(tasks()[0], lambda entries, **kwargs: entries)
    b.review_memory('hours', reviewer='participant', accept=False)
    assert b.memories(tasks()[0]) == []


def test_messages_and_model_calls_have_shared_bounds(tmp_path):
    b = TaskBoard(tmp_path / 'board', tasks(), SOURCES, max_model_calls=2)
    claim = b.claim('query', 'builder')
    for message in ('Use departure_time as ISO.', 'Contract confirmed.'):
        b.send_message('query', claim['dispatch_id'], 'view', message)
    with pytest.raises(FactoryStop, match='two'):
        b.send_message('query', claim['dispatch_id'], 'view', 'Another')
    def reserve(index):
        try:
            b.reserve_call(str(index), [{'role': 'user', 'content': str(index)}])
            return True
        except FactoryStop:
            return False
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(reserve, range(4)))
    assert sum(results) == 2


def test_followup_message_requires_evidence_and_does_not_schedule_work(tmp_path):
    b = TaskBoard(tmp_path / 'board', tasks(), SOURCES)
    claimed = b.claim('query', 'builder')
    with pytest.raises(ValueError, match='cite'):
        b.send_message('query', claimed['dispatch_id'], 'view', 'Handle another time zone.', kind='followup_proposal')
    b.record_event({'id': 'public-check-1', 'name': 'run_tests', 'result': {'passed': True}})
    message = b.send_message('query', claimed['dispatch_id'], 'view', 'Investigate another time zone.',
                            kind='followup_proposal', evidence=['public-check-1'])
    assert message['status'] == 'proposed' and message['evidence'] == ['public-check-1']
    assert set(b.snapshot()['tasks']) == {'query', 'view'}
    assert b.snapshot()['tasks']['view']['status'] == 'pending'


class FakeProvider:
    calls: ClassVar[list] = []
    lock = threading.Lock()

    def __init__(self, session):
        self.session = session

    def complete(self, request_id, messages, max_tokens):
        with self.lock:
            self.calls.append((request_id, messages.copy()))
        task_payload = next(json.loads(row['content']) for row in messages
            if row['role'] == 'user' and 'task' in json.loads(row['content']))
        path = task_payload['task']['editable_files'][0]
        number = int(request_id.rsplit('-', 1)[-1])
        if number == 0:
            action = {'action': 'read_file', 'path': path}
        elif number == 1:
            read = json.loads(messages[-1]['content'])['observation']
            action = {'action': 'write_file', 'path': path, 'before_sha256': read['sha256'],
                      'content': 'value = 1\n'}
        elif number == 2:
            action = {'action': 'run_tests'}
        else:
            action = {'action': 'finish', 'rationale': 'Implemented and passed the public check.'}
        result = {'id': request_id + '/0', 'request': {'model': MODEL, 'messages': messages, 'max_tokens': max_tokens},
                  'response': {'model': MODEL, 'choices': [{'message': {'content': json.dumps(action)}}]},
                  'observed_usd': 0.001, 'unknown_usd': 0, 'status': 'complete'}
        with self.session.transaction() as state:
            state['requests'][result['id']] = result
        return result


def test_real_loop_uses_learner_hooks_and_restart_does_not_repeat_calls(tmp_path):
    FakeProvider.calls = []
    session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / 'session')
    observed = {'ready': 0, 'claim': [], 'request': [], 'memory': 0, 'dispatch': []}
    def ready(rows):
        observed['ready'] += 1
        return list(reversed(ready_tasks(rows)))
    def claim(board, task, worker):
        observed['claim'].append(task)
        return board.claim(task, worker)
    def retrieve(entries, tags, scope, revision):
        observed['memory'] += 1
        return retrieve_memory(entries, tags, scope, revision)
    def request(task, sources, lessons):
        observed['request'].append(task['id'])
        return [{'role': 'user', 'content': json.dumps({'task': task, 'sources': sources,
                                                       'lessons': lessons, 'learner_marker': 'visible'})}]
    def dispatch(action, tools):
        observed['dispatch'].append(action['action'])
        if action['action'] == 'write_file':
            action = {**action, 'content': 'value = 2\n'}
        return tools[action['action']](action)
    kwargs = {'test_runner': passing, 'ready_hook': ready, 'claim_hook': claim, 'retrieve_hook': retrieve,
              'request_hook': request, 'dispatch_hook': dispatch,
              'provider_factory': FakeProvider, 'memory_entries': [lesson()]}
    result = run_build(session, 'team', SOURCES, tasks(), **kwargs)
    assert set(result['pending_review']) == {'query', 'view'}
    assert len(FakeProvider.calls) == 8
    assert observed['ready'] == 1 and len(observed['claim']) == len(observed['request']) == 2
    assert observed['memory'] == 2
    assert observed['dispatch'].count('write_file') == 2 and len(observed['dispatch']) == 8
    assert all(row['config']['action_dispatch'] == 'participant' for row in session.read()['stages'].values())
    assert all(any('learner_marker' in message['content'] for message in messages)
               for _, messages in FakeProvider.calls)
    assert result['metrics']['request_preflights'] == 8
    assert result['metrics']['model_requests'] == 8
    assert result['metrics']['provider_attempts'] == 8
    assert result['metrics']['request_max_tokens'] == 32768
    assert {row['request']['max_tokens'] for row in session.read()['requests'].values()} == {32768}
    assert result['metrics']['observed_cost_usd'] == pytest.approx(0.008)
    assert all(event['worker_id'] and event['task_id'] and event['dispatch_id']
               for event in result['events'])
    claims = [row for row in result['events'] if row['name'] == 'claim_task']
    assert len(claims) == 2
    assert all(row['id'] and row['status'] == 'complete' and row['ended_at'] >= row['started_at'] for row in claims)
    for outcome in result['outcomes']:
        assert outcome['trace_context']['agent_name'] == outcome['worker_id']
        assert outcome['trace_context']['worker_id'] == outcome['worker_id']
        assert 'parent_conversation_id' not in outcome['trace_context']
    shutil.rmtree(session.root / 'factory')
    restored = load_board(session, 'team')
    assert restored.snapshot()['tasks']['query']['patch']['query.py']['content'] == 'value = 2\n'
    again = run_build(session, 'team', SOURCES, tasks(), **kwargs)
    assert again['pending_review'] == result['pending_review']
    assert len(FakeProvider.calls) == 8
    accept(restored, 'query')
    assert session.read()['factory_boards']['team']['sources']['query.py'] == 'value = 2\n'


def test_dispatch_cannot_execute_multiple_tools_or_invent_an_observation(tmp_path):
    def mutate(action, tools):
        result = tools['read_file'](action)
        result['content'] = 'fabricated file contents'
        return result
    for name, dispatch in [('fabricated', lambda action, tools: {'content': 'not read'}),
                          ('twice', lambda action, tools: [tools['read_file'](action), tools['read_file'](action)]),
                          ('mutated', mutate)]:
        session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / name)
        result = run_build(session, name, SOURCES, tasks(), test_runner=passing,
                           provider_factory=FakeProvider, dispatch_hook=dispatch, max_steps=1)
        assert all(row['status'] == 'failed' for row in result['board']['tasks'].values())
        assert result['sources'] == SOURCES
        reads = [row for row in result['events'] if row['name'] == 'read_file']
        assert len(reads) == (0 if name == 'fabricated' else 2)
        assert all(row['result']['content'] == 'value = 0\n' for row in reads)


def test_provider_failure_is_saved_and_not_automatically_retried(tmp_path):
    session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / 'session')
    calls = []
    class FailedProvider:
        def __init__(self, session):
            pass
        def complete(self, *args, **kwargs):
            calls.append(args)
            raise ProviderStop('Outcome uncertain; explicit review required.')
    kwargs = {'test_runner': passing, 'provider_factory': FailedProvider}
    result = run_build(session, 'failed', SOURCES, tasks(), **kwargs)
    assert len(calls) == 2
    assert all(row['status'] == 'failed' for row in result['board']['tasks'].values())
    run_build(session, 'failed', SOURCES, tasks(), **kwargs)
    assert len(calls) == 2
    assert result['metrics']['request_preflights'] == 2
    assert result['metrics']['model_requests'] == result['metrics']['provider_attempts'] == 0


def test_long_source_context_reaches_tests_and_finish_without_losing_raw_history(tmp_path):
    initial = 'value = 0\n' + '# Existing implementation detail.\n' * 320
    updated = 'value = 1\n' + '# Updated implementation detail.\n' * 440
    sources = {'query.py': initial, 'contract.md': 'Preserve service dates.\n' * 100}
    task = FactoryTask('query', 'Query departures', 'Add a direct-trip query.', ('query.py',), tags=('time',))
    session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / 'session')
    sent_bounds = []

    class LongSourceProvider(FakeProvider):
        def complete(self, request_id, messages, max_tokens):
            bound = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096
            sent_bounds.append(bound)
            if bound > 32768:
                raise ProviderStop('Evidence exceeds the 32K input bound.')
            response = super().complete(request_id, messages, max_tokens)
            if request_id.endswith('step-1'):
                action = json.loads(response['response']['choices'][0]['message']['content'])
                action['content'] = updated
                response['response']['choices'][0]['message']['content'] = json.dumps(action)
                with self.session.transaction() as state:
                    state['requests'][response['id']] = response
            return response

    def request(task, sources, lessons):
        return [{'role': 'user', 'content': json.dumps({'task': task, 'sources': sources, 'lessons': lessons})}]

    def check(workspace, task):
        assert (workspace / 'query.py').read_text() == updated
        return {'passed': True, 'checks': [{'name': 'public-service-day', 'passed': True}],
                'earlier_error': 'A timeout was observed and then recovered.'}

    result = run_build(session, 'long-source', sources, [task], test_runner=check,
                       request_hook=request, memory_entries=[lesson()], provider_factory=LongSourceProvider)
    assert result['pending_review'] == ['query']
    assert result['board']['tasks']['query']['patch']['query.py']['content'] == updated
    assert len(sent_bounds) == 4 and max(sent_bounds) <= 32768
    compactions = [row for row in result['events'] if row['name'] == 'compact_worker_context']
    assert len(compactions) == 3
    third = json.loads(session.file(compactions[1]['result']['record']).read_text())
    assert len(json.dumps(third['raw_messages']).encode()) + 4096 > 32768
    raw_payload = json.loads(third['raw_messages'][1]['content'])
    assert raw_payload['sources']['query.py'] == initial
    assert json.loads(third['raw_messages'][-2]['content'])['content'] == updated
    final_request = next(row for row in session.read()['requests'].values() if 'step-3/' in row['id'])
    joined = '\n'.join(row['content'] for row in final_request['request']['messages'])
    assert 'A timeout was observed and then recovered.' in joined
    assert 'Preserve service dates.' in joined and lesson()['text'] in joined
    for row in session.read()['stages'].values():
        assert all(session.file(path).exists() for path in row['files'])


def test_context_keeps_non_source_fields_and_actual_dispatched_content():
    old, proposed, actual = 'old source\n', 'model proposal\n', 'participant-dispatched source\n'
    messages = [
        {'role': 'system', 'content': 'Keep this exact instruction.'},
        {'role': 'user', 'content': json.dumps({'task': {'instructions': 'Keep the contract.'},
            'sources': {'query.py': old, 'contract.md': old}, 'lessons': [{'text': old}]})},
        {'role': 'assistant', 'content': json.dumps({'action': 'write_file', 'path': 'query.py', 'content': proposed})},
        {'role': 'user', 'content': json.dumps({'observation': {'path': 'query.py', 'sha256': file_hash(actual)},
                                             'error': 'Keep this failed-check detail.'})},
    ]
    prepared, details = worker_context(messages, {'query.py': actual, 'contract.md': old})
    assert messages[0] == prepared[0]
    payload = json.loads(next(row['content'] for row in prepared if '"task"' in row['content']))
    assert payload['sources']['contract.md'] == payload['lessons'][0]['text'] == old
    snapshot = next(json.loads(row['content']) for row in prepared if '"current_executed_sources"' in row['content'])
    assert snapshot['current_executed_sources']['query.py'] == actual
    assert details['current_checksums']['query.py'] == file_hash(actual)
    assert json.loads(prepared[-1]['content'])['error'] == 'Keep this failed-check detail.'
    assert worker_context(messages, {'query.py': actual, 'contract.md': old}) == (prepared, details)


def test_context_summarizes_only_large_passing_check_payloads():
    outputs = [{'trip_id': str(n), 'departure_time': '2024-11-29T00:08:00-05:00'} for n in range(40)]
    checks = [
        {'case_id': 'passed', 'passed': True, 'actual': outputs, 'expected': outputs, 'error': None},
        {'case_id': 'failed', 'passed': False, 'actual': outputs, 'expected': [], 'error': 'Wrong service date.'},
    ]
    messages = [{'role': 'user', 'content': json.dumps({'observation': {'checks': checks, 'passed': False}})}]
    prepared, detail = worker_context(messages, SOURCES)
    observed = json.loads(prepared[0]['content'])['observation']['checks']
    assert observed[0]['actual']['sha256'] == digest(outputs)
    assert observed[0]['passed'] is True
    assert observed[1] == checks[1]
    assert len(detail['passed_checks_compacted']) == 2
    assert json.loads(messages[0]['content'])['observation']['checks'] == checks


def test_build_accounting_includes_all_transport_attempts_and_inflight(tmp_path):
    session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / 'session')
    class UncertainProvider:
        def __init__(self, session):
            self.session = session
        def complete(self, request_id, messages, **kwargs):
            with self.session.transaction() as state:
                for number, status in enumerate(('failed', 'interrupted', 'reserved')):
                    key = request_id + '/' + str(number)
                    state['requests'][key] = {'id': key, 'status': status, 'observed_usd': None,
                        'unknown_usd': 0.01 if status != 'reserved' else 0, 'reserved_usd': 0.01}
            raise ProviderStop('Request needs review.')
    result = run_build(session, 'cost', SOURCES, tasks(), test_runner=passing,
                       provider_factory=UncertainProvider)
    assert result['metrics']['request_preflights'] == 2
    assert result['metrics']['model_requests'] == 2
    assert result['metrics']['provider_attempts'] == 4
    assert result['metrics']['provider_attempt_records'] == 6
    assert result['metrics']['bounded_unknown_usd'] == pytest.approx(0.04)
    assert result['metrics']['inflight_usd'] == pytest.approx(0.02)
    assert all(row['status'] == 'failed' for row in result['board']['tasks'].values())


def test_scheduler_cannot_start_blocked_work_and_release_requires_actual_evaluation(tmp_path):
    session = WorkshopSession('person/project', 'factory-test', state_dir=tmp_path / 'session')
    with pytest.raises(ValueError, match='blocked'):
        run_build(session, 'bad-ready', SOURCES, tasks(dependent=True), test_runner=passing,
                  ready_hook=lambda rows: ['view'], provider_factory=FakeProvider)
    b = board(tmp_path)
    for task_id in ('query', 'view'):
        propose(b, task_id)
        accept(b, task_id)
    evaluation = {'passed': True, 'source_fingerprint': 'wrong-files', 'checks': []}
    with pytest.raises(FactoryStop, match='evaluated files'):
        freeze_release(b, evaluation, reviewer='participant')
    evaluation['source_fingerprint'] = digest(b.snapshot()['sources'])
    receipt = freeze_release(b, evaluation, reviewer='participant')
    restored = reproduce_release(receipt, tmp_path / 'reproduced')
    assert restored['source_fingerprint'] == evaluation['source_fingerprint']
    assert (tmp_path / 'reproduced/query.py').read_text() == 'value = 1\n'
    tampered = {**receipt, 'sources': {**receipt['sources'], 'query.py': 'bad'}}
    with pytest.raises(ValueError, match='fingerprint'):
        reproduce_release(tampered, tmp_path / 'bad')


def test_cyclic_dependency_and_changed_build_identity_are_rejected(tmp_path):
    with pytest.raises(ValueError, match='cycle'):
        TaskBoard(tmp_path / 'cycle', [FactoryTask('a', 'A', 'A', ('query.py',), ('b',)),
                                      FactoryTask('b', 'B', 'B', ('presentation.py',), ('a',))], SOURCES)
    b = board(tmp_path)
    with pytest.raises(ValueError, match='different inputs'):
        TaskBoard(b.root, tasks(), {**SOURCES, 'query.py': 'changed'})


@pytest.mark.parametrize('order', [1, 2])
def test_transit_patches_integrate_and_reproduce_against_independent_acceptance(tmp_path, order):
    from forge_workshop_kit import transit
    initial = transit.starter_sources(order)
    worked = transit.worked_sources(order)
    b = TaskBoard(tmp_path / 'transit', transit.task_specs(order), initial)
    claims = [b.claim(spec['id'], 'builder-' + str(index))
              for index, spec in enumerate(transit.task_specs(order))]
    for claim in claims:
        task_id, dispatch = claim['spec']['id'], claim['dispatch_id']
        path = claim['spec']['editable_files'][0]
        read = b.read_file(task_id, dispatch, path)
        b.write_file(task_id, dispatch, path, worked[path], read['sha256'])
        assert b.test(task_id, dispatch, transit.development_runner)['passed']
        b.submit(task_id, dispatch, 'Recorded reference implementation; no model call was made.')
    assert b.snapshot()['sources'] == initial
    for spec in transit.task_specs(order):
        accept(b, spec['id'])
    evaluation = transit.evaluate(b.snapshot()['sources'], order=order)
    assert evaluation['passed']
    receipt = freeze_release(b, evaluation, reviewer='test')
    reproduced = tmp_path / 'reproduced'
    reproduce_release(receipt, reproduced)
    replay = {name: (reproduced / name).read_text(encoding='utf-8') for name in initial}
    assert transit.evaluate(replay, order=order)['passed']
