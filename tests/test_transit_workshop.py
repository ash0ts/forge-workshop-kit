import json
import time

import pytest

from forge_workshop_kit import WorkshopSession, factory, factory_teaching, transit, transit_workshop
from forge_workshop_kit.provider import MODEL, Provider, ProviderStop
from forge_workshop_kit.session import digest


@pytest.fixture
def workshop(tmp_path, monkeypatch):
    session = WorkshopSession('participant/transit', 'transit-factory', state_dir=tmp_path)
    calls = []

    def complete(provider, request_id, messages, max_tokens):
        calls.append({'request_id': request_id, 'messages': json.loads(json.dumps(messages))})
        if request_id.endswith('/proposal'):
            action = {'text': 'A trip after midnight can belong to the previous service day.',
                      'supporting_case': 'departures/previous-service-day',
                      'limits': 'Only checked against the historical teaching timetable.'}
        else:
            payload = next(json.loads(row['content']) for row in messages if row['role'] == 'user')
            task = payload['task']
            path = task['editable_files'][0]
            number = int(request_id.rsplit('-', 1)[-1])
            if number == 0:
                action = {'action': 'read_file', 'path': path}
            elif number == 1:
                value = transit.worked_sources()[path]
                stage = session.read()['stages'][request_id.split('/')[0]]
                if '/solo/' in stage['name']:
                    value += '\n# Sequential builder execution.\n'
                action = {'action': 'write_file', 'path': path, 'content': value,
                          'before_sha256': json.loads(messages[-1]['content'])['observation']['sha256']}
            elif number == 2:
                action = {'action': 'run_tests'}
            else:
                action = {'action': 'finish', 'rationale': 'Public checks pass for the assigned function.'}
        now = time.time()
        record = {'id': request_id + '/0', 'status': 'complete', 'request': {'model': MODEL,
            'messages': json.loads(json.dumps(messages)), 'max_tokens': max_tokens, 'temperature': 0.2},
            'response': {'id': request_id, 'model': MODEL, 'choices': [{'message': {'content': json.dumps(action)}}]},
            'started_at': now, 'ended_at': now, 'observed_usd': 0.001, 'unknown_usd': 0}
        with session.transaction() as state:
            state['requests'][record['id']] = record
        return record

    monkeypatch.setattr(Provider, 'complete', complete)
    acceptance = factory_teaching.ACCEPTANCE_SOLUTION
    session.save_draft('factory/acceptance', acceptance)
    transit_workshop.save_check(session, 'acceptance', acceptance, factory_teaching.check_acceptance(acceptance))
    for name in ('worker', 'tasks', 'memory', 'evaluate', 'release'):
        source = factory_teaching.EXERCISES[name]['solution']
        session.save_draft('factory/' + name, source)
        transit_workshop.save_check(session, name, source, factory_teaching.check_exercise(name, source))
    return session, calls


def first_release(session):
    worker = session.get_draft('factory/worker')
    scheduler = session.get_draft('factory/tasks')
    solo = transit_workshop.run_initial(session, 'solo', worker)
    team = transit_workshop.run_initial(session, 'team', worker, workers=2, task_code=scheduler)
    assert len(solo['pending_review']) == len(team['pending_review']) == 2, {
        'solo_outcomes': solo['outcomes'], 'team_outcomes': team['outcomes']}
    assert 'query.py proposed' in transit_workshop.patch_review(session)
    results = transit_workshop.integrate_initial(session)
    assert all(result['passed'] and result['all_tasks_integrated'] for result in results.values())
    assert all(result['participant_acceptance']['participant_authored'] for result in results.values())
    assert transit_workshop._state(session)['base_release']['label'] == 'team'
    return results


def complete_workflow(session):
    first_release(session)
    transit_workshop.propose_lesson(session)
    evidence = next(value for value in transit_workshop.lesson_evidence_options(session).values()
                    if value.startswith('solo/'))
    lesson = transit_workshop.accept_lesson(session, 'Preserve service-day hours above 24.', evidence)
    transit_workshop.run_followups(session, session.get_draft('factory/worker'),
        session.get_draft('factory/tasks'), session.get_draft('factory/memory'))
    transit_workshop.integrate_followups(session)
    return lesson, transit_workshop.evaluate_builds(session)


def test_full_free_workflow_uses_scopes_and_publishes_saved_results(workshop, monkeypatch):
    session, calls = workshop
    lesson, results = complete_workflow(session)
    assert set(results) == {'solo', 'team', 'without-memory', 'with-memory'}
    assert all(result['passed'] and result['passed_count'] == result['total'] for result in results.values())
    costs = transit_workshop.cost_summary(session)
    assert costs['total']['provider_attempts'] == len(calls)
    assert costs['groups']['lesson preparation']['provider_attempts'] == 1
    assert {row['request']['max_tokens'] for row in session.read()['requests'].values()} == {32768}
    worker_stages = [row for row in session.read()['stages'].values() if row['name'].startswith('factory/build/')]
    assert all(row['config']['action_dispatch'] == 'participant' for row in worker_stages)
    assert sum(row['observed_usd'] for row in costs['groups'].values()) == pytest.approx(costs['total']['observed_usd'])
    state = transit_workshop._state(session)
    assert lesson['source_revision'] == state['integrations']['solo']['source_fingerprint']
    assert lesson['source_revision'] != state['base_release']['fingerprint']
    assert lesson['evidence'][0]['execution'] == state['integrations']['solo']['stage_id']
    baseline = factory.load_board(session, 'without-memory').snapshot()
    treatment = factory.load_board(session, 'with-memory').snapshot()
    assert baseline['config']['initial'] == treatment['config']['initial']
    assert baseline['memory'] == []
    assert treatment['memory'][0]['id'] == lesson['id']
    reads = [row for row in treatment['events'] if row['name'] == 'read_shared_memory']
    assert any(row['result']['entries'] for row in reads)
    assert all(row['result'] == {'entries': []} for row in baseline['events'] if row['name'] == 'read_shared_memory')
    published = []
    def publish(session, name, versions, *, summaries):
        published.append((name, versions, summaries))
        return {'status': 'published'}
    monkeypatch.setattr(transit_workshop, 'publish_comparison', publish)
    count = len(calls)
    assert len(transit_workshop.publish_results(session)) == 2
    assert len(published) == 2 and len(calls) == count
    for _, versions, _ in published:
        left, right = versions.values()
        assert [row['input'] for row in left] == [row['input'] for row in right]
    report_links = []
    def report(session, conclusion, links):
        assert isinstance(links, dict)
        report_links.append(links)
        return 'https://example.test/report'
    monkeypatch.setattr(transit_workshop, 'publish_report', report)
    with session.transaction() as journal:
        journal['publications']['comparison/saved'] = {'with-memory': {
            'comparison_name': 'transit-memory-followup', 'native_verified': True,
            'native_status': 'published', 'native_comparison_url': 'https://example.test/compare-followups'}}
        journal['publications']['trace/' + results['with-memory']['stage_id']] = {
            'verified': True, 'url': 'https://example.test/followup-acceptance'}
    released = transit_workshop.release(session, 'with-memory', session.get_draft('factory/release'),
                                       'Both versions passed; this run did not establish a memory gain.')
    assert released['decision'] == 'Release' and report_links
    assert report_links[-1]['Compare follow-ups with and without lessons'] == 'https://example.test/compare-followups'
    assert report_links[-1]['Acceptance checks: Team with checked lessons'] == 'https://example.test/followup-acceptance'
    retained = transit_workshop.release(session, 'with-memory', 'def release_decision(rows):\n    return False\n',
                                       'Retain the previous version for this exercise.')
    assert retained['decision'] == 'Retain the previous version'
    assert report_links[-1] == report_links[-2]
    assert len(calls) == count
    output = session.read()['stages'][released['stage_id']]
    assert any(path.endswith('transit-app.zip') for path in output['files'])
    assert any(path.endswith('release.json') for path in output['files'])


def test_final_cases_do_not_enter_any_worker_or_lesson_request(workshop):
    session, calls = workshop
    complete_workflow(session)
    context = json.dumps(calls)
    for case in transit._cases(2):
        assert case['case_id'] not in context
    assert 'expected' in context  # Public development answers are intentionally available.
    count = len(calls)
    again = transit_workshop.evaluate_builds(session)
    assert len(again) == 4 and len(calls) == count
    with pytest.raises(ValueError, match='frozen'):
        transit_workshop.run_followups(session, session.get_draft('factory/worker'),
            session.get_draft('factory/tasks'), session.get_draft('factory/memory'))


def test_changed_learner_scorer_affects_its_score_without_replacing_trusted_grades(workshop):
    session, _ = workshop
    first_release(session)
    evidence = next(iter(transit_workshop.lesson_evidence_options(session).values()))
    transit_workshop.accept_lesson(session, 'Use the service date.', evidence)
    transit_workshop.run_followups(session, session.get_draft('factory/worker'),
        session.get_draft('factory/tasks'), session.get_draft('factory/memory'))
    transit_workshop.integrate_followups(session)
    source = 'def score_scenario(actual, expected):\n    return False\n'
    session.save_draft('factory/evaluate', source)
    # An unchecked edit cannot run; the source identity is part of the checkpoint.
    assert not transit_workshop.can_run(session, 'evaluate')
    with session.transaction() as state:
        state['factory_checks']['evaluate'].update(source_fingerprint=digest(source))
    results = transit_workshop.evaluate_builds(session)
    scored = [row for result in results.values() for row in result['rows']
              if 'participant_departure_check' in row['scores']]
    assert scored and all(row['scores']['participant_departure_check'] == 0 for row in scored)
    assert all(result['scenario_pass_rate'] == 1 for result in results.values())


def test_publication_failure_and_retry_do_not_repeat_execution(workshop, monkeypatch):
    session, calls = workshop
    complete_workflow(session)
    count = len(calls)
    def unavailable(*args, **kwargs):
        raise RuntimeError('Service unavailable')
    monkeypatch.setattr(transit_workshop, 'publish_comparison', unavailable)
    assert all(row['status'] == 'publication unavailable'
               for row in transit_workshop.publish_results(session).values())
    monkeypatch.setattr(transit_workshop, 'publish_comparison', lambda *args, **kwargs: {'status': 'published'})
    assert all(row['status'] == 'published' for row in transit_workshop.publish_results(session).values())
    assert len(calls) == count


def test_participant_public_acceptance_runs_on_actual_integrated_output(workshop):
    session, calls = workshop
    first_release(session)
    count = len(calls)
    original = transit_workshop._state(session)['integrations']['team']['stage_id']
    source = 'def check_departures(rows):\n    return False\n'
    session.save_draft('factory/acceptance', source)
    assert not transit_workshop.can_run(session, 'solo')
    # Inspecting an edited development check does not repeat the builder's model calls.
    changed = transit_workshop.integrate_initial(session)
    assert len(calls) == count
    assert changed['team']['stage_id'] != original
    assert changed['team']['native_development_passed']
    assert not changed['team']['passed']
    assert changed['team']['participant_acceptance']['source_fingerprint'] == digest(source)


def test_prepared_continuation_preserves_failed_live_builds(workshop, monkeypatch):
    session, calls = workshop
    complete = Provider.complete
    def failed_initial_query(provider, request_id, messages, max_tokens):
        task = next(json.loads(row['content'])['task'] for row in messages if row['role'] == 'user')
        if task['id'] == 'order-1-query':
            raise ProviderStop('The initial query builder exceeded its output limit.')
        return complete(provider, request_id, messages, max_tokens)
    monkeypatch.setattr(Provider, 'complete', failed_initial_query)
    worker, scheduler = session.get_draft('factory/worker'), session.get_draft('factory/tasks')
    transit_workshop.run_initial(session, 'solo', worker)
    transit_workshop.run_initial(session, 'team', worker, workers=2, task_code=scheduler)
    live = transit_workshop.integrate_initial(session)
    assert all(not row['passed'] for row in live.values())
    before = {label: digest(factory.load_board(session, label).snapshot()) for label in ('solo', 'team')}
    assert transit_workshop.can_run(session, 'prepared-reference')
    count = len(calls)
    prepared = transit_workshop.use_prepared_reference(session)
    assert prepared['passed'] and prepared['origin'] == 'prepared reference'
    assert len(calls) == count
    assert transit_workshop.use_prepared_reference(session) == prepared
    assert {label: digest(factory.load_board(session, label).snapshot()) for label in ('solo', 'team')} == before
    assert transit_workshop._state(session)['integrations'] == live
    assert not transit.development_check(prepared['sources'], order=2)['passed']
    options = transit_workshop.lesson_evidence_options(session)
    assert all(value.startswith('prepared-reference/') for value in options.values())
    lesson = transit_workshop.accept_lesson(session, 'Keep the original service date after midnight.', next(iter(options.values())))
    assert lesson['evidence'][0]['origin'] == 'prepared reference'
    transit_workshop.run_followups(session, worker, scheduler, session.get_draft('factory/memory'))
    transit_workshop.integrate_followups(session)
    results = transit_workshop.evaluate_builds(session)
    assert not results['solo']['passed'] and not results['team']['passed']
    assert results['without-memory']['passed'] and results['with-memory']['passed']
    published_rows = transit_workshop._comparison_rows(session, 'with-memory', results['with-memory'])
    assert all(row['evidence']['starting_point'] == 'prepared-reference' for row in published_rows)


def test_lesson_context_is_bounded_and_saves_exact_selected_evidence(workshop):
    session, calls = workshop
    first_release(session)
    with session.transaction() as state:
        base = state['factory_workshop']['base_release']
        base['sources']['query.py'] += '\n' + '# irrelevant extra line\n' * 3000
        base['fingerprint'] = digest(base['sources'])
        for integration in state['factory_workshop']['integrations'].values():
            integration['checks'].append({'case_id': 'presentation/large', 'passed': True, 'output': '<p>large</p>' * 20000})
    value = transit_workshop.propose_lesson(session)
    request = calls[-1]
    assert len(json.dumps(request['messages'], ensure_ascii=False).encode()) + 4096 <= 32768
    selection = value['evidence_selection']
    assert selection['query_source']['excerpted']
    assert all(row['case_id'].startswith('departures/') for row in selection['checks'])
    assert 'presentation/large' not in json.dumps(request['messages'])
    stage = next(row for row in session.read()['stages'].values() if row['name'] == 'factory/memory/proposal')
    assert stage['inputs'] == selection


def test_interrupted_build_freezes_controller_before_dispatch(workshop, monkeypatch):
    session, calls = workshop
    worker = session.get_draft('factory/worker')
    real_build = factory.run_build

    def interrupted(*args, **kwargs):
        original_ready = kwargs.get('ready_hook') or factory.ready_tasks
        kwargs['ready_hook'] = lambda tasks: original_ready(tasks)[:1]
        real_build(*args, **kwargs)
        raise RuntimeError('Notebook stopped before saving the build summary.')

    monkeypatch.setattr(factory, 'run_build', interrupted)
    with pytest.raises(RuntimeError, match='Notebook stopped'):
        transit_workshop.run_initial(session, 'solo', worker)
    assert len(calls) == 4
    assert 'solo' not in transit_workshop._state(session).get('builds', {})
    assert transit_workshop._state(session)['build_configurations']['solo']['authored']['worker'] == worker
    monkeypatch.setattr(factory, 'run_build', real_build)
    with pytest.raises(ValueError, match='different coordinator'):
        transit_workshop.run_initial(session, 'solo', worker + '\n# Changed after interruption.\n')
    assert len(calls) == 4
    resumed = transit_workshop.run_initial(session, 'solo', worker)
    assert set(resumed['pending_review']) == {'order-1-query', 'order-1-presentation'}
    assert len(calls) == 8  # The completed first task did not execute again.


def test_completed_legacy_build_can_restore_without_repeating_calls(workshop):
    session, calls = workshop
    worker = session.get_draft('factory/worker')
    transit_workshop.run_initial(session, 'solo', worker)
    count = len(calls)
    with session.transaction() as state:
        del state['factory_workshop']['build_configurations']
    resumed = transit_workshop.run_initial(session, 'solo', worker)
    assert len(resumed['pending_review']) == 2 and len(calls) == count
    assert transit_workshop._state(session)['build_configurations']['solo']['authored']['worker'] == worker
    with pytest.raises(ValueError, match='different coordinator'):
        transit_workshop.run_initial(session, 'solo', worker + '\n# A new controller.\n')
    assert len(calls) == count


def test_unverifiable_partial_legacy_build_cannot_silently_adopt_new_controller(workshop):
    session, calls = workshop
    board = factory.TaskBoard(session.file('factory/solo'), transit.task_specs(), transit.starter_sources(),
                              max_model_calls=16, session=session)
    board.claim('order-1-query', 'builder-1')
    with pytest.raises(ValueError, match='without a saved coordinator identity'):
        transit_workshop.run_initial(session, 'solo', session.get_draft('factory/worker'))
    assert not calls


def test_operational_summary_counts_recovery_and_keeps_missing_cases_separate(tmp_path):
    session = WorkshopSession('participant/transit', 'transit-factory', state_dir=tmp_path)
    def result(case, passed):
        return {'case_id': case, 'inputs': {'function': 'query.departures', 'arguments': [case]},
                'scores': {'scenario_pass': passed}, 'status': 'completed' if passed is not None else 'unavailable'}
    spec = {'name': 'factory/integration/with-memory', 'sources': {'query.py': 'first'}, 'inputs': {}, 'config': {}}
    with session.transaction() as state:
        state['factory_workshop'] = {'base_release': {'label': 'team'}, 'evaluations': {
            'team': {'rows': [result('a', 1), result('b', 1), result('c', None)]},
            'with-memory': {'rows': [result('a', 0), result('b', 1), result('c', 1), result('new', 1)]}}}
        state['factory_boards'] = {'with-memory': {'tasks': {'query': {'spec': {'id': 'query'},
            'dispatch_id': 'retry', 'status': 'integrated', 'history': [
                {'spec': {'id': 'query'}, 'dispatch_id': 'first', 'status': 'failed'}]}}}}
        state['stages'] = {
            'first': {**spec, 'attempt': 1, 'status': 'failed'},
            'retry': {**spec, 'attempt': 2, 'status': 'complete'},
            'changed': {**spec, 'sources': {'query.py': 'second'}, 'attempt': 1, 'status': 'complete'},
        }
    before = session.read()
    summary = transit_workshop.operational_summary(session)
    assert session.read() == before
    measured = summary['builds']['with-memory']
    assert measured['task_claim_attempts'] == 2 and measured['repeated_task_claims'] == 1
    assert measured['integration_executions'] == 3
    assert measured['integration_retries'] == measured['integration_retests'] == 1
    assert measured['judgments_available'] == measured['judgments_expected'] == 4
    assert measured['inherited_cases']['status'] == 'partial'
    assert measured['inherited_cases']['compared_cases'] == 2
    assert measured['inherited_cases']['regression_cases'] == ['a']
    assert measured['inherited_cases']['unavailable_cases'] == ['c']
    assert measured['broader_duplicate_work']['status'] == 'unmeasured'
    assert summary['builds']['team']['task_claim_attempts'] is None
    assert summary['builds']['team']['judgments_unavailable'] == 1


def test_report_links_use_named_verified_comparisons_and_the_selected_stage(tmp_path):
    session = WorkshopSession('participant/transit', 'transit-factory', state_dir=tmp_path)
    def comparison(name, url, verified=True):
        return {'comparison_name': name, 'native_verified': verified,
                'native_status': 'published', 'native_comparison_url': url}
    with session.transaction() as state:
        state['factory_workshop'] = {'evaluations': {'team': {'stage_id': 'team-evaluation'}}}
        state['stages'] = {'team-evaluation': {'name': 'factory/evaluate/team'},
                           'team-release': {'name': 'factory/release/team'},
                           'solo-release': {'name': 'factory/release/solo'}}
        state['publications'] = {
            'comparison/first': {'team': comparison('transit-first-release', 'https://example.test/first')},
            'comparison/followup': {'with-memory': comparison('transit-memory-followup', 'https://example.test/memory')},
            'comparison/unverified': {'team': comparison('transit-first-release', 'https://example.test/unverified', False)},
            'comparison/other': {'team': comparison('some-other-workshop', 'https://example.test/unrelated')},
            'trace/team-evaluation': {'verified': True, 'url': 'https://example.test/checks'},
            'trace/team-release': {'verified': False, 'url': 'https://example.test/release'},
            'trace/solo-release': {'verified': True, 'url': 'https://example.test/wrong-build'},
        }
    before = session.read()
    links = transit_workshop.saved_evidence_links(session, 'team', 'solo-release')
    assert links == {
        'Workshop source': 'https://github.com/ash0ts/forge-workshop-kit',
        'Compare one and two builders': 'https://example.test/first',
        'Compare follow-ups with and without lessons': 'https://example.test/memory',
        'Acceptance checks: Two builders': 'https://example.test/checks',
    }
    assert session.read() == before
    assert transit_workshop.saved_evidence_links(session, 'team', 'team-release') == links
    with session.transaction() as state:
        state['publications']['trace/team-release']['verified'] = True
    links = transit_workshop.saved_evidence_links(session, 'team', 'team-release')
    assert links['Release execution'] == 'https://example.test/release'
    assert 'Acceptance checks: Two builders' not in links
