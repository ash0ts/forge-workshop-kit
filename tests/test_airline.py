import copy
import hashlib
import json
import time

import pytest

from forge_workshop_kit import WorkshopSession, airline, airline_teaching as teaching
from forge_workshop_kit.provider import ProviderStop


def complete_case(case, builder=airline.build_itinerary):
    env = airline.AirlineEnvironment(case, builder)
    outcome = 'unchanged' if case['kind'] == 'read_only' else 'declined'
    if case['kind'] == 'change':
        scope = case['passenger']
        plan = env.call('plan_change', {'replace_start': scope['replace_start'], 'replace_stop': scope['replace_stop'],
                                       'replacement_flights': scope['replacement']})
        env.call('request_confirmation', {'flights': airline.flight_ids(plan['flights']), 'fare_difference': plan['fare_difference']})
        payment = next(k for k, p in env.world['user']['payment_methods'].items()
                       if p['source'] == 'credit_card' or p['amount'] >= plan['fare_difference'])
        env.call('update_reservation_flights', {'reservation_id': env.world['reservation']['reservation_id'],
            'flights': airline.flight_ids(plan['flights']), 'payment_id': payment})
        outcome = 'changed'
    run = {'world': env.world, 'status': 'complete', 'events': [], 'draft': {'outcome': outcome, 'summary': 'Checked.'}}
    return run


def test_source_checksum_and_family_disjoint_partitions():
    cases = airline.load_cases()
    assert len(cases) == 26
    assert [len(airline.load_cases(p)) for p in ('discovery', 'monitoring', 'development', 'final', 'subsequent')] == [8, 4, 4, 6, 4]
    families = {}
    for case in cases:
        assert families.setdefault(case['family_id'], case['partition']) == case['partition']
    assert hashlib.sha256((airline.ASSETS / 'cases.json').read_bytes()).hexdigest() == airline.provenance()['cases_sha256']
    assert airline.provenance()['revision'] == '989d3285ae669e49503324bdb9981bf14fccedeb'


def test_all_fixed_cases_have_a_feasible_independently_checked_outcome():
    for case in airline.load_cases():
        result = airline.score_booking(case, complete_case(case))
        assert result['task_success'], (case['id'], result)


def test_full_update_can_succeed_while_unrequested_return_disappears():
    case = airline.load_cases('discovery')[0]
    env = airline.AirlineEnvironment(case)
    original = copy.deepcopy(env.world)
    quote = env.call('quote_change', {'flights': case['passenger']['replacement']})
    confirmation = env.call('request_confirmation', {'flights': case['passenger']['replacement'], 'fare_difference': quote['fare_difference']})
    assert not confirmation['approved']
    result = env.call('update_reservation_flights', {'reservation_id': env.world['reservation']['reservation_id'],
        'flights': case['passenger']['replacement'], 'payment_id': next(iter(env.world['user']['payment_methods']))})
    assert result['saved'] is True
    assert len(env.world['reservation']['flights']) < len(original['reservation']['flights'])
    score = airline.score_booking(case, {'world': env.world, 'status': 'complete', 'events': [], 'draft': {'outcome': 'changed'}})
    assert not score['task_success'] and score['unrequested_itinerary_change'] and not score['write_confirmed']


def test_connection_to_nonstop_is_not_a_lost_return():
    case = next(c for c in airline.load_cases('final') if c['passenger']['replace_stop'] - c['passenger']['replace_start'] == 2)
    run = complete_case(case)
    assert len(run['world']['reservation']['flights']) < len(case['initial']['reservation']['flights'])
    assert airline.score_booking(case, run)['task_success']


def test_scripted_passenger_confirms_exact_plan_not_arbitrary_yes():
    case = airline.load_cases('discovery')[0]; env = airline.AirlineEnvironment(case)
    flights = airline._expected_ids(case); quote = airline._quote(env.world, flights)
    assert not env.call('request_confirmation', {'flights': flights, 'fare_difference': quote['fare_difference'] + 1})['approved']
    assert env.call('request_confirmation', {'flights': flights, 'fare_difference': quote['fare_difference']})['approved']
    wrong = flights[:-1]
    assert not env.call('request_confirmation', {'flights': wrong, 'fare_difference': airline._quote(env.world, wrong)['fare_difference']})['approved']


def test_transient_read_timeout_changes_no_booking_and_can_recover():
    case = next(c for c in airline.load_cases() if c.get('fault'))
    env = airline.AirlineEnvironment(case); before = copy.deepcopy(env.world['reservation'])
    args = {'reservation_id': before['reservation_id']}
    with pytest.raises(TimeoutError): env.call('get_reservation_details', args)
    assert env.world['reservation'] == before
    assert env.call('get_reservation_details', args) == before


def test_free_checks_and_unsolved_starters():
    namespace = {}
    for text in teaching.ANSWERS.values(): namespace.update(teaching.compile_code(text))
    assert teaching.check_itinerary_builder(namespace['my_itinerary_builder'])['passed']
    assert teaching.check_state_scorer(namespace['my_state_scorer'])['passed']
    assert teaching.check_monitor(namespace['my_monitor'])['passed']
    assert teaching.check_curation(namespace['case_from_reviewed_turn'])['passed']
    assert teaching.check_judge_validation(namespace['my_judge_validation'])['passed']
    assert teaching.check_instrumentation(namespace)['passed']
    for key, check, name in [('itinerary_builder', teaching.check_itinerary_builder, 'my_itinerary_builder'),
                             ('state_scorer', teaching.check_state_scorer, 'my_state_scorer'),
                             ('monitor', teaching.check_monitor, 'my_monitor'),
                             ('curation', teaching.check_curation, 'case_from_reviewed_turn')]:
        with pytest.raises(NotImplementedError): check(teaching.compile_code(teaching.STARTERS[key])[name])


def scripted_provider(monkeypatch, actions):
    pending = iter(actions); requests = []
    def complete(self, request_id, messages, **kwargs):
        action = next(pending); requests.append(copy.deepcopy(messages))
        started = time.time()
        record = {'id': request_id + '/0', 'request': {'model': airline.MODEL, 'messages': copy.deepcopy(messages),
            'max_tokens': kwargs['max_tokens'], 'temperature': .2}, 'response': {'model': airline.MODEL,
            'choices': [{'message': {'content': json.dumps(action)}, 'finish_reason': 'stop'}]},
            'started_at': started, 'ended_at': started + .001, 'status': 'complete', 'transport_state': 'response_saved',
            'observed_usd': .0001, 'unknown_usd': 0, 'reserved_usd': .01}
        with self.session.transaction() as state: state['requests'][record['id']] = record
        return record
    monkeypatch.setattr(airline.Provider, 'complete', complete)
    return requests


def test_saved_success_and_export_retry_do_not_repeat_model_calls(tmp_path, monkeypatch):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    case = next(c for c in airline.load_cases('discovery') if c['kind'] == 'read_only')
    actions = [{'action': 'get_reservation_details', 'arguments': {'reservation_id': case['initial']['reservation']['reservation_id']}},
               {'action': 'finish', 'arguments': {'outcome': 'unchanged', 'summary': 'Your itinerary is unchanged.'}}]
    requests = scripted_provider(monkeypatch, actions); exports = []
    def export(*args, **kwargs):
        exports.append(kwargs)
        return {'verified': True, 'url': 'https://forge.example/conversation'}
    monkeypatch.setattr(airline, 'export_trace', export)
    run = airline.execute_conversation(session, case)
    again = airline.execute_conversation(session, case)
    assert run['scores']['task_success'] and again['stage_id'] == run['stage_id']
    assert len(requests) == 2 and len(exports) == 2
    assert exports[0]['agent_name'] == 'airline-' + session.workspace_id
    assert len(exports[0]['turns'][0]['request_ids']) == 2
    assert 'Tool observation:' in requests[1][-1]['content']
    for sent in requests:
        text = json.dumps(sent)
        assert 'allows_write' not in text and 'source_task_id' not in text and 'task_success' not in text


def test_repaired_builder_executes_and_conversation_has_real_passenger_turn(tmp_path, monkeypatch):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    case = airline.load_cases('discovery')[0]; scope = case['passenger']
    expected = airline._expected_ids(case); quote = airline._quote(case['initial'], expected)
    args = {'replace_start': scope['replace_start'], 'replace_stop': scope['replace_stop'], 'replacement_flights': scope['replacement']}
    actions = [{'action': 'plan_change', 'arguments': args},
               {'action': 'request_confirmation', 'arguments': {'flights': expected, 'fare_difference': quote['fare_difference']}},
               {'action': 'update_reservation_flights', 'arguments': {'reservation_id': case['initial']['reservation']['reservation_id'],
                    'flights': expected, 'payment_id': next(iter(case['initial']['user']['payment_methods']))}},
               {'action': 'finish', 'arguments': {'outcome': 'changed', 'summary': 'Changed the requested flight and kept the return.'}}]
    requests = scripted_provider(monkeypatch, actions)
    ns = teaching.compile_code(teaching.ANSWERS['itinerary_builder'] + '\n' + teaching.ANSWERS['state_scorer'])
    run = airline.execute_conversation(session, case, label='repaired', itinerary_builder=ns['my_itinerary_builder'],
        state_scorer=ns['my_state_scorer'], export=False)
    assert run['scores']['task_success'] and run['development_scores']['untouched_preserved']
    assert len(run['turns']) == 2 and len(run['turns'][0]['event_ids']) == 2 and len(run['turns'][1]['event_ids']) == 2
    assert 'Yes. I approve' in run['turns'][1]['messages'][0]['content']
    assert 'plan_change' in requests[0][0]['content']


def test_ten_actual_attempt_cap_counts_transport_retries(tmp_path, monkeypatch):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path); budgets = []
    def complete(self, request_id, messages, **kwargs):
        count = kwargs['max_attempts']; budgets.append(count)
        for n in range(count):
            record = {'id': request_id + '/' + str(n), 'request': {'model': airline.MODEL},
                'response': {'choices': [{'message': {'content': '{"action":"invalid","arguments":{}}'}, 'finish_reason': 'stop'}]},
                'started_at': time.time(), 'ended_at': time.time(), 'status': 'complete' if n == count - 1 else 'failed',
                'transport_state': 'response_saved', 'observed_usd': .0001, 'unknown_usd': 0}
            with self.session.transaction() as state: state['requests'][record['id']] = record
        return record
    monkeypatch.setattr(airline.Provider, 'complete', complete)
    run = airline.execute_conversation(session, airline.load_cases('discovery')[0], export=False)
    assert budgets == [3, 3, 3, 1] and run['model_attempts'] == 10
    assert run['status'] == 'agent_failure'


def test_learner_runtime_error_is_saved_and_returned_as_an_observation(tmp_path, monkeypatch):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    case = airline.load_cases('discovery')[0]
    scope = case['passenger']
    def broken_builder(current_flights, replace_start, replace_stop, replacement_flights):
        raise RuntimeError('Learner itinerary implementation failed')
    actions = [{'action': 'plan_change', 'arguments': {'replace_start': scope['replace_start'],
        'replace_stop': scope['replace_stop'], 'replacement_flights': scope['replacement']}},
        {'action': 'finish', 'arguments': {'outcome': 'unresolved',
            'summary': 'The itinerary helper failed; no booking change was made.'}}]
    requests = scripted_provider(monkeypatch, actions)
    run = airline.execute_conversation(session, case, label='repaired',
        itinerary_builder=broken_builder, export=False)
    failure = run['events'][0]
    assert failure['name'] == 'plan_change'
    assert failure['error'] == 'RuntimeError: Learner itinerary implementation failed'
    assert failure['result'] == {'error': failure['error']}
    assert failure['ended_at'] >= failure['started_at']
    assert session.read()['stages'][run['stage_id']]['events'][0] == failure
    assert failure['error'] in requests[1][-1]['content']
    assert run['model_attempts'] == 2 and run['status'] == 'complete'
    assert run['scores']['task_success'] is False and run['scores']['execution_errors'] == 1
    assert run['world']['reservation'] == case['initial']['reservation']


def test_infrastructure_failure_is_not_a_completed_failed_agent_score(tmp_path, monkeypatch):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    def fail(*args, **kwargs): raise ProviderStop('Inference access denied')
    monkeypatch.setattr(airline.Provider, 'complete', fail)
    with pytest.raises(ProviderStop): airline.execute_conversation(session, airline.load_cases('discovery')[0], export=False)
    stage = next(iter(session.read()['stages'].values()))
    assert stage['status'] == 'failed' and not stage.get('result')
    assert any(path.endswith('partial.json') for path in stage['files'])


def test_controlled_calibration_has_real_tool_effects_and_no_model_calls(tmp_path, monkeypatch):
    from forge_workshop_kit import airline_calibration
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    def forbidden(*args, **kwargs): raise AssertionError('Calibration must not call a model')
    monkeypatch.setattr(airline.Provider, 'complete', forbidden)
    runs = airline_calibration.run_calibration_pack(session, export=False)
    assert len(runs) == 6 and all(r['model_attempts'] == 0 and r['split'] == 'calibration' for r in runs)
    assert all('task_success' not in r and 'scores' not in r for r in runs)
    omitted = next(r for r in runs if r['case_id'] == 'calibration-omitted-return')
    assert omitted['calibration_label'] and len(omitted['world']['reservation']['flights']) == 1
    assert any(e['name'] == 'update_reservation_flights' and e['result']['saved'] for e in omitted['events'])
    recovered = next(r for r in runs if r['case_id'] == 'calibration-recovered-read')
    assert sum(bool(e['error']) for e in recovered['events']) == 1
    assert recovered['world']['writes'][0]['confirmation_id']
    pending = next(r for r in runs if r['case_id'] == 'calibration-awaiting-confirmation')
    assert not pending['resolution_known'] and not pending['world']['writes']
    assert not airline.saved_runs(session)
    again = airline_calibration.run_calibration_pack(session, export=False)
    assert [r['stage_id'] for r in again] == [r['stage_id'] for r in runs]


def test_reviewed_cases_drive_free_regression_check_and_keep_controlled_origin(tmp_path, monkeypatch):
    from forge_workshop_kit import airline_calibration, airline_regression
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    def forbidden(*args, **kwargs): raise AssertionError('Regression checks must not call a model')
    monkeypatch.setattr(airline.Provider, 'complete', forbidden)
    runs = airline_calibration.run_calibration_pack(session, export=False)
    ns = teaching.compile_code(teaching.ANSWERS['curation'] + '\n' + teaching.ANSWERS['itinerary_builder'])
    curated = []
    for run in runs[:2]:
        review = {'decision': 'accepted', 'reviewer': 'participant',
            'expected_behavior': 'Apply only the requested change; keep all other flights.',
            'supporting_event_id': run['events'][0]['id']}
        curated.append(ns['case_from_reviewed_turn'](review, run))
    result = airline_regression.run_regressions(session, curated, itinerary_builder=ns['my_itinerary_builder'])
    assert result['passed'] and result['model_calls'] == 0
    incident, control = result['rows']
    assert not incident['legacy']['scores']['task_success']
    assert incident['repaired']['scores']['task_success']
    assert control['legacy']['scores']['task_success'] and control['repaired']['scores']['task_success']
    assert all('Controlled calibration' in row['origin'] for row in result['rows'])
    assert airline_regression.run_regressions(session, curated,
        itinerary_builder=ns['my_itinerary_builder'])['stage_id'] == result['stage_id']
    broken = airline_regression.run_regressions(session, curated, itinerary_builder=airline.legacy_drill_builder)
    assert not broken['passed'] and broken['stage_id'] != result['stage_id']
    tampered = copy.deepcopy(curated)
    tampered[0]['initial_state']['reservation']['flights'].pop()
    with pytest.raises(ValueError, match='exact source'):
        airline_regression.run_regressions(session, tampered, itinerary_builder=ns['my_itinerary_builder'])
    assert session.read()['requests'] == {}


def test_reserved_requests_never_enter_the_regression_builder(tmp_path):
    from forge_workshop_kit import airline_regression
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    for partition in ('final', 'subsequent'):
        with session.stage('airline/baseline/reserved', config={'partition': partition}) as stage:
            stage.record({'split': partition})
        with pytest.raises(ValueError, match='Reserved or subsequent'):
            airline_regression.run_regressions(session, [{'source_execution': stage.id}],
                itinerary_builder=airline.build_itinerary)


@pytest.mark.parametrize('partition', ['final', 'subsequent'])
def test_reserved_inputs_do_not_expose_passenger_oracle_or_final_grades(tmp_path, monkeypatch, partition):
    session = WorkshopSession('user/project', 'airline', state_dir=tmp_path)
    cases = airline.load_cases(partition)
    sent = scripted_provider(monkeypatch, [{'action': 'finish',
        'arguments': {'outcome': 'unresolved', 'summary': 'I have not changed this booking.'}} for _ in cases])
    for case in cases:
        run = airline.execute_conversation(session, case, export=False)
        assert run['scores']['task_success'] is False
        with pytest.raises(ValueError, match='development conversations only'):
            airline.judge_explanation(session, run, rubric='Not sent', validator=lambda result: result)
    assert len(sent) == len(cases)
    for messages in sent:
        serialized = json.dumps(messages)
        assert all(key not in serialized for key in ('allows_write', 'max_extra_dollars',
            'source_task_id', 'task_success', 'request_scope', 'expected_behavior'))
        assert len(messages) == 2 and messages[0]['role'] == 'system'
