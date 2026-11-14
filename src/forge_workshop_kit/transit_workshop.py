"""Notebook actions over the small factory; display and publication never build code."""
from __future__ import annotations

import difflib
import html
import json
import shutil
from dataclasses import asdict

from . import factory, transit
from . import factory_teaching as teaching
from .provider import Provider, output
from .publication import publish_comparison, publish_report
from .session import digest, write_json
from .traces import event, export_trace, saved_trace_inputs

LABELS = {'solo': 'One builder', 'team': 'Two builders',
          'without-memory': 'Team without lessons', 'with-memory': 'Team with checked lessons',
          'prepared-reference': 'Prepared reference app'}
MEMORY_VERSION = 'transit-v1'


def data_preview():
    data = transit.load_data()
    rows = [row for row in data['stop_times'] if row['stop_id'] == '70076' and int(row['departure_time'].split(':')[0]) >= 24][:4]
    trips = {r['trip_id']: r for r in data['trips']}
    return {'departures': [{**row, 'service_id': trips[row['trip_id']]['service_id']} for row in rows],
            'manifest': data['manifest']}


def work_order(order):
    return {'order': order, 'contract': transit.CONTRACT, 'tasks': transit.task_specs(order),
            'aggregate_model_requests': 16, 'workers': 'One sequential worker or two parallel workers',
            'data': transit.DATASET_ID}


def save_check(session, name, source, result):
    with session.transaction() as state:
        state.setdefault('factory_checks', {})[name] = {**result, 'source': source}
    return result


def _checked(session, name):
    row = session.read().get('factory_checks', {}).get(name, {})
    return row.get('status') == 'passed' and row.get('source_fingerprint') == digest(session.get_draft('factory/'+name, ''))


def _state(session):
    return session.read().get('factory_workshop', {}) if session else {}


def _put(session, key, value):
    with session.transaction() as state:
        state.setdefault('factory_workshop', {})[key] = value
    return value


def can_run(session, action):
    if session is None:
        return False
    state = _state(session)
    if action in ('solo', 'team') and state.get('frozen'):
        return False
    checks = {'solo': _checked(session, 'acceptance') and _checked(session, 'worker'),
              'team': _checked(session, 'acceptance') and _checked(session, 'worker') and _checked(session, 'tasks'),
              'integrate': all(name in state.get('builds', {}) for name in ('solo', 'team')),
              'prepared-reference': all(name in state.get('integrations', {}) for name in ('solo', 'team'))
                  and not state.get('base_release') and not state.get('frozen') and _checked(session, 'acceptance'),
              'preview': bool(state.get('integrations')),
              'memory': bool(state.get('base_release')),
              'followup': bool(state.get('base_release')) and bool(state.get('lesson')) and _checked(session, 'memory') and not state.get('frozen'),
              'integrate-followup': all(name in state.get('builds', {}) for name in ('without-memory', 'with-memory')),
              'evaluate': len(state.get('integrations', {})) == 4 and _checked(session, 'evaluate'),
              'release': bool(state.get('evaluations')) and _checked(session, 'release')}
    return bool(checks.get(action, False))


def blocked(session, action):
    if can_run(session, action):
        return ''
    if session is None:
        return 'Connect to your project in the first step.'
    if _state(session).get('frozen') and action in ('solo', 'team', 'followup'):
        return 'The comparison is frozen. Inspect its saved results; use a new workspace for another build.'
    return {'solo': 'Check your departure acceptance rule and build_worker_request first.',
            'team': 'Check your departure acceptance rule, build_worker_request, ready_tasks, and claim_task first.',
            'integrate': 'Run both the one-builder and two-builder attempts first.',
            'prepared-reference': 'Review both initial attempts and test their integration first. Use this continuation only when neither produces a passing release.',
            'preview': 'Review and integrate the returned patches first.',
            'memory': 'A combined first release must pass its development checks. Inspect the integration results.',
            'followup': 'Save a checked lesson and pass the memory-retrieval exercise first.',
            'integrate-followup': 'Run both follow-up builds before reviewing their patches.',
            'evaluate': 'Review all four builds and check your score_scenario function first.',
            'release': 'Run the frozen comparison and check release_decision first.'}.get(action, 'Complete the previous step.')


def _require(session, action):
    if not can_run(session, action):
        raise ValueError(blocked(session, action))


def example_task_board():
    return {'tasks': {**{r['id']: {**r, 'status': 'pending'} for r in transit.task_specs(1)},
                      'integration': {'title': 'Test the combined application', 'status': 'pending',
                                      'depends_on': [r['id'] for r in transit.task_specs(1)]}}}


def _build(session, label, sources, order, worker_code, task_code=None, memory_code=None, lessons=(), workers=2):
    if _state(session).get('frozen'):
        raise ValueError('The comparison is frozen. Start another workspace to change its builds.')
    worker_functions = teaching.functions(worker_code)
    request_hook = worker_functions['build_worker_request']
    hooks = teaching.functions(task_code) if task_code else {}
    retrieval = teaching.functions(memory_code).get('select_memories') if memory_code else None
    authored = {'worker': worker_code, 'tasks': task_code, 'memory': memory_code}
    configuration = {'authored': authored, 'order': order, 'workers': workers,
        'initial_fingerprint': digest(sources), 'lessons_fingerprint': digest(lessons),
        'model': factory.MODEL, 'max_tokens': factory.WORKER_MAX_TOKENS,
        'context_policy': factory.WORKER_CONTEXT_POLICY, 'max_model_calls': 16, 'max_steps': 8,
        'memory_version': MEMORY_VERSION}
    # Save the controller before dispatch. A stopped notebook may already have a
    # completed sibling task even though run_build never returned its summary.
    with session.transaction() as journal:
        workshop = journal.setdefault('factory_workshop', {})
        prior = workshop.get('builds', {}).get(label)
        frozen = workshop.get('build_configurations', {}).get(label)
        if frozen is not None and frozen != configuration:
            raise ValueError('This build already used different coordinator code or settings. Its completed results are preserved. Use a fresh workspace for a changed comparison.')
        if frozen is None:
            if prior:
                # Completed older releases saved the source in the result summary.
                if (prior['authored'] != authored or prior['order'] != order
                        or prior['initial_fingerprint'] != configuration['initial_fingerprint']
                        or prior['result']['metrics']['workers'] != workers):
                    raise ValueError('This build already used different coordinator code or settings. Its completed results are preserved. Use a fresh workspace for a changed comparison.')
            else:
                board = journal.get('factory_boards', {}).get(label, {})
                if board.get('calls') or any(row['status'] != 'pending' for row in board.get('tasks', {}).values()):
                    raise ValueError('This older build started without a saved coordinator identity. Its existing results remain available, but resuming with unverifiable code is blocked. Start a fresh workspace.')
            workshop.setdefault('build_configurations', {})[label] = configuration
    result = factory.run_build(session, label, sources, transit.task_specs(order),
        test_runner=transit.development_runner, request_hook=request_hook,
        dispatch_hook=worker_functions.get('dispatch_action'),
        ready_hook=hooks.get('ready_tasks'), claim_hook=hooks.get('claim_task'), retrieve_hook=retrieval,
        memory_entries=lessons, workers=workers, max_model_calls=16, max_steps=8, memory_version=MEMORY_VERSION)
    with session.transaction() as state:
        state.setdefault('factory_workshop', {}).setdefault('builds', {})[label] = {
            'order': order, 'authored': authored, 'result': result, 'initial_fingerprint': digest(sources)}
    return result


def run_initial(session, label, worker_code, *, workers=1, task_code=None):
    if label not in ('solo', 'team'):
        raise ValueError('Choose solo or team for the first work order.')
    _require(session, label)
    return _build(session, label, transit.starter_sources(), 1, worker_code, task_code, workers=workers)


def patch_review(session, followup=False):
    state = _state(session)
    parts = []
    for label in (('without-memory', 'with-memory') if followup else ('solo', 'team')):
        if label not in state.get('builds', {}):
            continue
        board = factory.load_board(session, label).snapshot()
        parts.append('<h3>'+html.escape(LABELS[label])+'</h3>'+teaching.task_board(board))
        for task_id, task in board['tasks'].items():
            if task.get('decision') == 'KEEP':
                parts.append('<p>'+html.escape(task_id)+': Retain this version. '
                             +html.escape(task.get('rationale', ''))+'</p>')
            for name, change in task.get('patch', {}).items():
                before = task.get('base_sources', board['config']['initial']).get(name, '')
                patch = ''.join(difflib.unified_diff(before.splitlines(True), change['content'].splitlines(True), fromfile=name+' before', tofile=name+' proposed'))
                parts.append('<details open><summary>'+html.escape(task_id+' / '+name)+'</summary><pre>'+html.escape(patch or 'Retain this file unchanged')+'</pre></details>')
            if task.get('error'):
                parts.append('<p>'+html.escape(task['error'])+'</p>')
    return ''.join(parts) or '<p>No patches have been submitted yet.</p>'


def _integrate(session, labels):
    output_rows = {}
    for label in labels:
        board = factory.load_board(session, label)
        for task_id, row in board.snapshot()['tasks'].items():
            if row['status'] == 'review':
                with session.stage('factory/review/'+label+'/'+task_id, inputs={'patch': row['patch']}) as review:
                    if review.needs_run:
                        accepted, receipt = event('integrate_reviewed_patch',
                            {'build': label, 'task': task_id, 'patch_digest': digest(row['patch'])},
                            lambda task_id=task_id, row=row, board=board: board.integrate(task_id,
                                reviewer='participant', expected_patch_digest=digest(row['patch'])),
                            on_error=review.record_event)
                        review.record({'decision': 'accept', 'result': accepted,
                            'events': [receipt], 'trace_context': {'agent_name': 'participant'},
                            'mission': 'Integrate the participant-reviewed patch for '+task_id})
        sources = board.snapshot()['sources']
        order = _state(session)['builds'][label]['order']
        authored_acceptance = session.get_draft('factory/acceptance', '')
        acceptance_source = authored_acceptance or teaching.ACCEPTANCE_SOLUTION
        with session.stage('factory/integration/'+label, sources=sources, config={'order': order},
                           inputs={'participant_acceptance': acceptance_source,
                                   'participant_authored': bool(authored_acceptance)}) as stage:
            if stage.needs_run:
                result, receipt = event('test_combined_application', {'build': label},
                    lambda sources=sources, order=order: transit.development_check(sources, order=order), on_error=stage.record_event)
                public_rows = next((check.get('actual') for check in result['checks']
                                    if check['case_id'] == 'departures/previous-service-day'), None)
                try:
                    participant_check, learner_receipt = event('participant_acceptance_check',
                        {'build': label, 'source_fingerprint': digest(acceptance_source),
                         'case_id': 'departures/previous-service-day'},
                        lambda source=acceptance_source, rows=public_rows: teaching.check_public_scenario(source, rows),
                        on_error=stage.record_event)
                    events = [receipt, learner_receipt]
                except Exception as error:  # noqa: BLE001 -- Keep a broken learner check separate from the native result.
                    participant_check = {'passed': False, 'status': 'unavailable', 'error': str(error),
                                         'source_fingerprint': digest(acceptance_source)}
                    events = [receipt]
                participant_check['participant_authored'] = bool(authored_acceptance)
                stage.record({**result, 'native_development_passed': result['passed'],
                              'participant_acceptance': participant_check,
                              'passed': result['passed'] and participant_check['passed'],
                              'events': events, 'trace_context': {'agent_name': 'participant'},
                              'mission': 'Test the reviewed query and presentation together for '+LABELS[label]})
            result = stage.result
        output_rows[label] = {**result, 'sources': sources, 'source_fingerprint': digest(sources), 'stage_id': stage.id,
                              'all_tasks_integrated': all(r['status'] == 'integrated' for r in board.snapshot()['tasks'].values())}
    with session.transaction() as state:
        state.setdefault('factory_workshop', {}).setdefault('integrations', {}).update(output_rows)
    return output_rows


def integrate_initial(session):
    _require(session, 'integrate')
    results = _integrate(session, ('solo', 'team'))
    # Fixed preference: two-worker build, otherwise the tested one-worker build.
    # A prepared repair is available separately; it never replaces a failed live build.
    if not _state(session).get('base_release'):
        for label in ('team', 'solo'):
            row = results[label]
            if row['passed'] and row['all_tasks_integrated']:
                _put(session, 'base_release', {'label': label, 'sources': row['sources'], 'fingerprint': row['source_fingerprint']})
                break
    return results


def use_prepared_reference(session):
    """Explicit teaching continuation; preserve every live build and its scores."""
    existing = _state(session).get('prepared_reference')
    if existing and _state(session).get('base_release', {}).get('label') == 'prepared-reference':
        return existing
    _require(session, 'prepared-reference')
    # This supplied version implements departures only. The follow-up functions
    # still need implementing; worked_sources() would already solve both orders.
    sources = transit.starter_sources(order=2)
    acceptance = session.get_draft('factory/acceptance', '')
    with session.stage('factory/prepared-reference', sources=sources,
                       config={'order': 1, 'origin': 'prepared reference'},
                       inputs={'participant_acceptance': acceptance}) as stage:
        if stage.needs_run:
            result, checked = event('test_prepared_reference', {'order': 1},
                lambda: transit.development_check(sources, order=1), on_error=stage.record_event)
            public_rows = next(check['actual'] for check in result['checks']
                               if check['case_id'] == 'departures/previous-service-day')
            participant, authored = event('participant_acceptance_check',
                {'case_id': 'departures/previous-service-day', 'source_fingerprint': digest(acceptance)},
                lambda: teaching.check_public_scenario(acceptance, public_rows), on_error=stage.record_event)
            stage.record({**result, 'passed': result['passed'] and participant['passed'],
                'native_development_passed': result['passed'], 'participant_acceptance': participant,
                'sources': sources, 'source_fingerprint': digest(sources), 'origin': 'prepared reference',
                'events': [checked, authored], 'trace_context': {'agent_name': 'participant',
                    'conversation_name': 'Transit / Prepared reference app / Development checks'},
                'mission': 'Check the supplied departures implementation before using it for the separate follow-up comparison.'})
        record = {**stage.result, 'stage_id': stage.id}
    _put(session, 'prepared_reference', record)
    if not record['passed']:
        raise ValueError('The prepared app did not pass the current development checks. Inspect those results before continuing.')
    _put(session, 'base_release', {'label': 'prepared-reference', 'sources': sources,
        'fingerprint': digest(sources), 'origin': 'prepared reference', 'stage_id': stage.id})
    return record


def stop_choices():
    return {r['stop_name']+' / '+r.get('platform_name', '')+' ('+r['stop_id']+')': r['stop_id']
            for r in transit.load_data()['stops'] if r['location_type'] == '0'}


def preview(session, label, stop_id, at):
    state = _state(session)
    row = state['prepared_reference'] if label == 'prepared-reference' else state['integrations'][label]
    execution = transit.run_sources(row['sources'], [{'call': 'query.departures', 'args': [stop_id, at]}])
    if execution['status'] != 'completed' or not execution['results'][0].get('ok'):
        return execution
    departures = execution['results'][0]['value']
    view = transit.run_sources(row['sources'], [{'call': 'presentation.render_board', 'args': [departures]}])
    return {'departures': departures, 'html': view['results'][0].get('value', ''), 'fingerprint': execution['fingerprint']}


def _lesson_sources(session):
    state = _state(session)
    if state.get('base_release', {}).get('label') == 'prepared-reference':
        return {'prepared-reference': state['prepared_reference']}
    return {label: row for label, row in state.get('integrations', {}).items() if label in ('solo', 'team')}


def lesson_evidence_options(session):
    return {LABELS[label]+' / '+check['case_id']: label+'/'+check['case_id']
            for label, row in _lesson_sources(session).items()
            for check in row['checks'] if check.get('passed') is True}


def propose_lesson(session):
    _require(session, 'memory')
    state = _state(session)
    base = state['base_release']
    supporting = _lesson_sources(session)[base['label']]
    selected_checks = [row for key in ('departures/previous-service-day', 'departures/holiday-addition')
                       for row in supporting['checks'] if row['case_id'] == key]
    lines = base['sources']['query.py'].splitlines(keepends=True)
    excerpt = []
    for line in lines:
        if len((''.join(excerpt) + line).encode()) > 14000:
            break
        excerpt.append(line)
    evidence = {'build': base['label'], 'origin': supporting.get('origin', 'live build'),
        'source_fingerprint': base['fingerprint'], 'checks': selected_checks,
        'query_source': {'path': 'query.py', 'sha256': factory.file_hash(base['sources']['query.py']),
            'text': ''.join(excerpt), 'start_line': 1, 'end_line': len(excerpt),
            'total_lines': len(lines), 'excerpted': len(excerpt) < len(lines)},
        'selection': 'The adopted app only: up to two public checks (previous-service-day, then holiday-addition), plus a bounded query.py excerpt. '
                     'Other builds, rendered HTML, and final acceptance results are excluded.'}
    def lesson_messages():
        return [{'role': 'system', 'content': 'Propose one concise experience note for the next transit feature. Use only the supplied development results and source. Return JSON {"text":str,"supporting_case":str,"limits":str}. A correct implementation does not establish a memory benefit. Do not claim an observed failure unless the evidence records it.'},
                {'role': 'user', 'content': json.dumps({'development': evidence})}]
    # Keep a deterministic, reviewable selection rather than raising the provider's input bound.
    while len(json.dumps(lesson_messages(), ensure_ascii=False).encode()) + 4096 > 32768:
        if len(evidence['checks']) > 1:
            evidence['checks'].pop()
        elif excerpt:
            excerpt.pop()
            evidence['query_source'].update(text=''.join(excerpt), end_line=len(excerpt), excerpted=True)
        else:
            raise ValueError('The selected public check is too large for the lesson request. No model call was sent.')
    with session.stage('factory/memory/proposal', sources=base['sources'], inputs=evidence,
                       config={'model': factory.MODEL, 'max_tokens': factory.WORKER_MAX_TOKENS}) as stage:
        if stage.needs_run:
            messages = lesson_messages()
            response = Provider(session).complete(stage.id+'/proposal', messages, max_tokens=factory.WORKER_MAX_TOKENS)
            value = output(response)
            if not all(isinstance(value.get(k), str) and value[k].strip()
                       for k in ('text','supporting_case','limits')):
                raise ValueError('The proposed lesson did not supply text, a supporting case, and limits.')
            stage.record({**value, 'request_id': response['id'], 'evidence_selection': evidence,
                          'trace_context': {'agent_name': 'lesson-reviewer',
                              'conversation_name': 'Transit / Propose a lesson / Public service-day checks'},
                          'status': 'proposed'})
    return stage.result


def accept_lesson(session, text, evidence_id):
    _require(session, 'memory')
    if not text.strip() or len(text.encode()) > 2000:
        raise ValueError('Write a specific lesson in at most 2 KiB.')
    if evidence_id not in lesson_evidence_options(session).values():
        raise ValueError('Select an actual passing development check as support.')
    source_label, source_case = evidence_id.split('/', 1)
    source = _lesson_sources(session)[source_label]
    supporting_check = next(check for check in source['checks'] if check['case_id'] == source_case)
    lesson = asdict(factory.MemoryEntry(id=digest([text,evidence_id])[:20], text=text.strip(),
        tags=('gtfs','service-day'), scope='transit', version=MEMORY_VERSION,
        source_revision=source['source_fingerprint'], evidence=({'case': evidence_id,
            'execution': source['stage_id'], 'source_fingerprint': source['source_fingerprint'],
            'origin': source.get('origin', 'live build'), 'check': supporting_check},),
        status='accepted', reviewer='participant', limits='Reviewed against this historical MBTA week; not a claim about all transit feeds.'))
    if _state(session).get('builds', {}).get('with-memory') and _state(session).get('lesson') != lesson:
        raise ValueError('The follow-up already used a frozen lesson. Preserve it for this comparison.')
    return _put(session, 'lesson', lesson)


def run_followups(session, worker_code, task_code, memory_code):
    _require(session, 'followup')
    state = _state(session)
    sources = state['base_release']['sources']
    results = {}
    for label, lessons in [('without-memory', ()), ('with-memory', (state['lesson'],))]:
        results[label] = _build(session,label,sources,2,worker_code,task_code,memory_code,lessons,workers=2)
    return results


def integrate_followups(session):
    _require(session, 'integrate-followup')
    return _integrate(session, ('without-memory', 'with-memory'))


def evaluate_builds(session):
    _require(session, 'evaluate')
    state = _state(session)
    frozen = {label: {'sources': row['sources'], 'fingerprint': digest(row['sources'])}
              for label,row in state['integrations'].items()}
    if state.get('frozen') and state['frozen'] != frozen:
        raise ValueError('The source changed after freezing. Preserve the existing comparison.')
    _put(session,'frozen',frozen)
    scorer_code = session.get_draft('factory/evaluate', '')
    learner_score = teaching.functions(scorer_code)['score_scenario']
    results = {}
    for label,item in frozen.items():
        order = state['builds'][label]['order']
        with session.stage('factory/evaluate/'+label, sources=item['sources'], config={'order':order},
                           inputs={'development_scorer':scorer_code}) as stage:
            if stage.needs_run:
                value,receipt = event('independent_acceptance', {'build':label,'source_fingerprint':item['fingerprint']},
                    lambda item=item, order=order: transit.evaluate(item['sources'],order),on_error=stage.record_event)
                for row in value['rows']:
                    prediction=row['outputs'].get('prediction'); target=row['outputs'].get('expected')
                    if isinstance(prediction,list) and isinstance(target,list):
                        try:
                            checked = learner_score([r['trip_id'] for r in prediction], [r['trip_id'] for r in target])
                            if type(checked) is not bool:
                                raise ValueError('The participant scorer must return True or False.')
                            row['scores']['participant_departure_check'] = float(checked)
                        except Exception as error:  # noqa: BLE001 -- Learner code cannot discard trusted results.
                            row['scores']['participant_departure_check'] = None
                            row['outputs']['participant_check_error'] = str(error)
                stage.record({**value,'events':[receipt],'trace_context':{'agent_name':'acceptance-checker'},
                              'source_fingerprint':item['fingerprint']})
            results[label] = {**stage.result, 'stage_id':stage.id}
    return _put(session,'evaluations',results)


def _comparison_rows(session,label,result):
    state=_state(session)
    sources=state['frozen'][label]
    starting_point = state.get('base_release', {}).get('label') if label in ('without-memory','with-memory') else 'public starter'
    trace=session.read()['publications'].get('trace/'+result['stage_id'],{})
    # Scenarios return different Python types (rows, one journey, HTML, or JSON).
    # A stable display schema keeps native table columns comparable. The saved
    # evaluation and linked trace retain the original typed values.
    return [{'case_id':row['case_id'],
             'input':{'function':row['inputs']['function'],
                      'arguments':json.dumps(row['inputs']['arguments'], ensure_ascii=False)},
             'prediction':{'actual':json.dumps(row['outputs'].get('prediction'), ensure_ascii=False),
                           'status':row['status'], 'error':row['outputs'].get('error') or '',
                           'participant_departure_check':json.dumps(row['scores'].get('participant_departure_check'))},
             'target':json.dumps(row['outputs'].get('expected'), ensure_ascii=False),
             'error':1-row['scores']['scenario_pass'] if row['scores']['scenario_pass'] is not None else None,
             'scores':{'pass_rate':row['scores']['scenario_pass']},
             'evidence':{'trace':trace.get('url'),'source_fingerprint':sources['fingerprint'],
                         'starting_point':starting_point,'status':row['status']}}
            for row in result['rows']]


def publish_results(session):
    state=_state(session)
    if not state.get('evaluations'):
        return {'status':'No saved final comparison yet.'}
    receipts={}
    for name,labels in [('transit-first-release',('solo','team')),('transit-memory-followup',('without-memory','with-memory'))]:
        versions={label:_comparison_rows(session,label,state['evaluations'][label]) for label in labels}
        summaries={label:{'pass_rate':state['evaluations'][label]['scenario_pass_rate'],
                          'coverage':sum(r['scores']['scenario_pass'] is not None for r in state['evaluations'][label]['rows'])/state['evaluations'][label]['total'],
                          'seconds':state['builds'][label]['result']['metrics']['build_seconds'],
                          'cost_usd':state['builds'][label]['result']['metrics']['observed_cost_usd']}
                   for label in labels}
        try:
            receipts[name]=publish_comparison(session,name,versions,summaries=summaries)
        except Exception as error:  # noqa: BLE001 -- Publication is independently retryable.
            receipts[name]={'status':'publication unavailable','error':str(error)}
    return receipts


def cost_summary(session):
    """Account for every provider attempt once, including lesson preparation."""
    state = session.read()
    groups = {label: [] for label in LABELS}
    groups.update({'lesson preparation': [], 'other requests': []})
    build_prefixes = {label: tuple(board['calls']) for label, board in state.get('factory_boards', {}).items()}
    lesson_stages = tuple(row['id'] for row in state['stages'].values()
                          if row['name'].startswith('factory/memory/'))
    for identity, request in state['requests'].items():
        label = next((name for name, prefixes in build_prefixes.items()
                      if name in groups and any(identity.startswith(prefix + '/') for prefix in prefixes)), None)
        if label is None:
            label = 'lesson preparation' if any(identity.startswith(prefix + '/') for prefix in lesson_stages) else 'other requests'
        groups[label].append(request)
    def totals(rows):
        sent = [row for row in rows if row['status'] != 'reserved' and row.get('transport_state') != 'unsent']
        return {'provider_attempts': len(sent), 'provider_attempt_records': len(rows),
                'observed_usd': sum(row.get('observed_usd') or 0 for row in rows),
                'bounded_unknown_usd': sum(row.get('unknown_usd') or 0 for row in rows),
                'inflight_usd': sum(row.get('reserved_usd') or 0 for row in rows if row['status'] in ('pending', 'reserved'))}
    return {'groups': {LABELS.get(name, name): totals(rows) for name, rows in groups.items() if rows},
            'total': totals(list(state['requests'].values())),
            'note': 'Lesson preparation is counted once, separately from the four builds. Notebook compute is billed separately.'}


def operational_summary(session):
    """Read saved claims, integration executions, and matching acceptance cases."""
    journal = session.read()
    state = journal.get('factory_workshop', {})
    builds = {}
    labels = [label for label in LABELS if label != 'prepared-reference' and (
        label in state.get('builds', {}) or label in journal.get('factory_boards', {})
        or label in state.get('evaluations', {}))]
    for label in labels:
        board = journal.get('factory_boards', {}).get(label)
        claims = []
        if board is not None:
            claims = [attempt for task in board['tasks'].values()
                      for attempt in [*task.get('history', []), task] if attempt.get('dispatch_id')]
        per_task = {}
        for claim in claims:
            task_id = claim['spec']['id']
            per_task.setdefault(task_id, set()).add(claim['dispatch_id'])
        integrations = [row for row in journal['stages'].values()
                        if row['name'] == 'factory/integration/' + label]
        integration_groups = {}
        for row in integrations:
            identity = digest({key: row.get(key) for key in ('name', 'config', 'sources', 'inputs')})
            integration_groups.setdefault(identity, []).append(row)
        evaluation = state.get('evaluations', {}).get(label)
        rows = evaluation.get('rows', []) if evaluation else []
        available = [row for row in rows if row['scores'].get('scenario_pass') is not None]
        inherited = {'status': 'not applicable', 'compared_cases': None,
                     'regressions': None, 'regression_cases': [], 'unavailable_cases': []}
        if label in ('without-memory', 'with-memory'):
            base_label = state.get('base_release', {}).get('label')
            baseline = state.get('evaluations', {}).get(base_label)
            inherited.update(baseline=base_label, status='unavailable')
            if baseline is not None and evaluation is not None:
                indexed = {row['case_id']: row for row in rows}
                paired, lost, missing = [], [], []
                for previous in baseline['rows']:
                    current = indexed.get(previous['case_id'])
                    if (current is None or previous['inputs'] != current['inputs']
                            or previous['scores'].get('scenario_pass') is None
                            or current['scores'].get('scenario_pass') is None):
                        missing.append(previous['case_id'])
                        continue
                    paired.append(previous['case_id'])
                    if previous['scores']['scenario_pass'] == 1 and current['scores']['scenario_pass'] == 0:
                        lost.append(previous['case_id'])
                inherited.update(status='measured' if not missing else 'partial',
                    compared_cases=len(paired), regressions=len(lost), regression_cases=lost,
                    unavailable_cases=missing)
            else:
                inherited['reason'] = 'No saved reserved evaluation exists for the starting version or this follow-up.'
        builds[label] = {
            'task_claim_attempts': len(claims) if board is not None else None,
            'repeated_task_claims': sum(max(0, len(ids)-1) for ids in per_task.values()) if board is not None else None,
            'tasks_integrated': sum(row['status'] == 'integrated' for row in board['tasks'].values()) if board else None,
            'tasks_total': len(board['tasks']) if board else None,
            'integration_executions': len(integrations),
            'integration_retries': sum(max(0, len(group)-1) for group in integration_groups.values()),
            'integration_retests': max(0, len(integration_groups)-1),
            'judgments_available': len(available) if evaluation is not None else None,
            'judgments_expected': len(rows) if evaluation is not None else None,
            'judgments_unavailable': len(rows)-len(available) if evaluation is not None else None,
            'agent_error_rows': sum(row.get('status') == 'agent_error' for row in rows) if evaluation is not None else None,
            'inherited_cases': inherited,
            'broader_duplicate_work': {'status': 'unmeasured',
                'reason': 'Repeated task claims count retries; they do not measure overlapping reasoning or semantically duplicated code.'},
        }
    return {'builds': builds, 'definitions': {
        'repeated_task_claims': 'Additional saved dispatches for the same task, including explicit recovery attempts.',
        'integration_retries': 'Additional saved integration executions with the same source, configuration, and participant check.',
        'integration_retests': 'Integration executions on a changed source or participant check, after the first distinct set of inputs.',
        'inherited_regressions': 'Matching reserved cases that passed in the chosen starting version and failed in the follow-up.',
        'coverage': 'Available judgments divided by expected saved evaluation rows; unavailable judgments are not failures.',
    }}


def publish_traces(session, tool_writer=None):
    results=[]
    for row in session.read()['stages'].values():
        if row['status'] == 'running':
            continue
        args=saved_trace_inputs(session,row)
        if not args['events'] and not args['requests']:
            continue
        try:
            results.append(export_trace(session,**args,tool_writer=tool_writer))
        except Exception as error:  # noqa: BLE001 -- Trace export must not repeat execution.
            results.append({'stage':row['name'],'status':'publication pending','error':str(error)})
    return results


def release_choices(session):
    return {LABELS[label]:label for label in _state(session).get('evaluations',{})}


def saved_evidence_links(session, label, release_stage_id=None):
    """Link the saved, verified comparisons and the selected build's checks."""
    journal = session.read()
    publications = journal.get('publications', {})
    names = {'transit-first-release': 'Compare one and two builders',
             'transit-memory-followup': 'Compare follow-ups with and without lessons'}
    links = {'Workshop source': 'https://github.com/ash0ts/forge-workshop-kit'}
    for key, versions in publications.items():
        if not key.startswith('comparison/'):
            continue
        for receipt in versions.values():
            name = receipt.get('comparison_name')
            if (name in names and receipt.get('native_verified')
                    and receipt.get('native_status') == 'published'
                    and receipt.get('native_comparison_url')):
                links[names[name]] = receipt['native_comparison_url']
    evaluation = journal.get('factory_workshop', {}).get('evaluations', {}).get(label, {})
    candidates = [(release_stage_id, 'Release execution', 'factory/release/' + label),
                  (evaluation.get('stage_id'), 'Acceptance checks: ' + LABELS[label], 'factory/evaluate/' + label)]
    for stage_id, title, expected_name in candidates:
        receipt = publications.get('trace/' + stage_id, {}) if stage_id else {}
        if (receipt.get('verified') and receipt.get('url')
                and journal.get('stages', {}).get(stage_id, {}).get('name') == expected_name):
            links[title] = receipt['url']
            break
    return links


def release(session,label,code,conclusion):
    _require(session,'release')
    state=_state(session)
    evaluation=state['evaluations'][label]
    rows=[{'passed':r['scores']['scenario_pass']==1 if r['scores']['scenario_pass'] is not None else None} for r in evaluation['rows']]
    decision=teaching.functions(code)['release_decision'](rows)
    if not decision:
        saved = {'decision':'Retain the previous version','reason':conclusion,'label':label}
        _put(session, 'release_decision', saved)
        try:
            saved['report'] = publish_report(session, conclusion, saved_evidence_links(session, label))
        except Exception as error:  # noqa: BLE001 -- Preserve the decision if Report publication fails.
            saved['report'] = {'status': 'publication pending', 'error': str(error)}
        return _put(session, 'release_decision', saved)
    board=factory.load_board(session,label)
    receipt=factory.freeze_release(board,{'passed':all(r['passed'] is True for r in rows),
        'source_fingerprint':state['frozen'][label]['fingerprint'],'rows':rows},reviewer='participant',
        previous_release=state.get('base_release',{}).get('fingerprint'))
    with session.stage('factory/release/'+label,sources=receipt['sources'],inputs={'decision_code':code,'conclusion':conclusion}) as stage:
        if stage.needs_run:
            app=transit.export_app(receipt['sources'],stage.output_dir/'app',order=evaluation['order'])
            write_json(stage.output_dir/'release.json',{**receipt,'lesson':state.get('lesson'),
                'dataset':transit.load_data()['manifest'],'operations':operational_summary(session)})
            archive=shutil.make_archive(str(stage.output_dir/'transit-app'),'zip',stage.output_dir/'app')
            stage.record({'label':label,'conclusion':conclusion,'app':app,'source_fingerprint':receipt['source_fingerprint']},
                         files=[archive,stage.output_dir/'release.json'])
    session.checkpoint('release')
    try:
        report=publish_report(session,conclusion,saved_evidence_links(session,label,stage.id))
    except Exception as error:  # noqa: BLE001 -- Preserve the release if Report publication fails.
        report={'status':'publication pending','error':str(error)}
    return _put(session,'release_decision',{**stage.result,'report':report,'stage_id':stage.id,'decision':'Release'})


def allow_retry(session,stage_id,confirm_stopped):
    row=session.read()['stages'][stage_id]
    if _state(session).get('frozen'):
        raise ValueError('The final comparison is frozen; keep this failure in its results.')
    result=session.retry_stage(stage_id,confirm_stopped=confirm_stopped)
    parts=row['name'].split('/')
    if len(parts)==5 and parts[:2]==['factory','build'] and parts[3]=='worker':
        factory.load_board(session,parts[2]).retry(parts[4],confirm_stopped=confirm_stopped,reason='Participant requested recovery')
    return result


def investigation(step):
    return {'setup':'Open the schedule-inspection span. Find the feed date and an after-midnight departure.',
            'worker':'Open the builder conversation. Find the file it read before editing and its returned test result.',
            'tasks':'Find the task claim and its owner. Which task was still waiting?',
            'team':'Compare the two conversations: assigned files, start times, and any message sent to the other builder.',
            'integrate':'Compare the submitted patch with the integrated source and the combined check.',
            'memory':'Open the proposed lesson and check its cited development case before accepting it.',
            'followup':'Find read_shared_memory in each arm. Confirm only one returned the accepted note.',
            'evaluate':'In EvalTables, compare the same departure case across versions, then open its actual output.',
            'release':'Open the release artifact and find the exact source, dataset checksum, and checked results.'}[step]


def result_views(mo,session,step,outputs):
    state=_state(session); views=[]
    if state.get('base_release', {}).get('label') == 'prepared-reference' and step in ('integrate','memory','followup','evaluate','release'):
        views.append(mo.md('**Follow-up starting point: prepared reference app.** '
            'The initial builder attempts remain in the comparison with their actual results. '
            'The two follow-up builds use the same supplied departures implementation; neither is credited with producing it.'))
    relevant={'worker':['solo'],'team':['team'],'integrate':['solo','team'],'followup':['without-memory','with-memory']}.get(step,[])
    for label in relevant:
        if label not in state.get('builds',{}): continue
        board=teaching.with_evidence(factory.load_board(session,label).snapshot(), session.read())
        views.extend([mo.md('### '+LABELS[label]),mo.Html(teaching.task_board(board)),
                      mo.Html(teaching.timeline(board['events'])),
                      mo.accordion({'Saved build details':mo.json(state['builds'][label]['result']['metrics'])})])
    for key in (step+' check',step,'lesson proposal' if step=='memory' else '', 'app' if step=='integrate' else ''):
        if key and key in outputs:
            value=outputs[key]
            if isinstance(value,dict) and value.get('html'):
                # Candidate HTML is rendered in an opaque, script-disabled frame.
                views.append(mo.Html('<iframe title="Saved transit app" sandbox="" style="width:100%;height:300px;border:1px solid #888" srcdoc="'+html.escape(value['html'],quote=True)+'"></iframe>'))
            else: views.append(mo.accordion({key:mo.json(value)}))
    if step=='integrate' and state.get('integrations'):
        views.append(mo.ui.table([{'build':LABELS[k],'passed':r['passed'],'integrated':r['all_tasks_integrated'],
                                  'checks':len(r['checks'])} for k,r in state['integrations'].items() if k in ('solo','team')],selection=None))
    if step=='memory' and state.get('lesson'): views.append(mo.json(state['lesson']))
    if step in ('evaluate','release') and state.get('evaluations'):
        views.append(mo.ui.table([{'Version':LABELS[k],'All checks passed':'Yes' if r['passed'] else 'No',
                                  'Passing scenarios':f"{r['passed_count']} / {r['total']}",
                                  'Pass rate':f"{r['scenario_pass_rate']:.1%}"} for k,r in state['evaluations'].items()],selection=None))
        costs = cost_summary(session)
        operations = operational_summary(session)
        views.extend([mo.md('**Build operations and coverage**'),
            mo.ui.table([{'Version': LABELS[label],
                'Repeated task claims': row['repeated_task_claims'],
                'Integration executions': row['integration_executions'],
                'Integration retries': row['integration_retries'],
                'Judgments available': (f"{row['judgments_available']} / {row['judgments_expected']}"
                    if row['judgments_expected'] is not None else 'Unavailable'),
                'Previously passing cases now failing': (row['inherited_cases']['regressions']
                    if row['inherited_cases']['status'] in ('measured', 'partial')
                    else row['inherited_cases']['status'].capitalize())}
                for label, row in operations['builds'].items()], selection=None),
            mo.md('Repeated claims count explicit attempts at the same task. Overlapping reasoning or duplicated code is not measured.')])
        views.extend([mo.md('**Inference cost** — '+costs['note']),
                      mo.ui.table([{'Activity': name,'Provider attempts':row['provider_attempts'],
                                    'Observed cost':f"${row['observed_usd']:.5f}",
                                    'Bounded unknown cost':f"${row['bounded_unknown_usd']:.5f}",
                                    'In-flight reservation':f"${row['inflight_usd']:.5f}"}
                                   for name,row in [*costs['groups'].items(),('Total',costs['total'])]],selection=None),
                      mo.accordion({'Exact comparison and accounting records':mo.json({
                          'evaluations':state['evaluations'],'costs':costs,'operations':operations})})])
    if step=='release' and state.get('release_decision'):
        views.append(mo.Html(teaching.release_history([state['release_decision']])))
    # Navigation controls live in the notebook and remain free of side effects.
    return views or [mo.md('Run the step above to see its saved result here.')]
