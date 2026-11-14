"""Free adapter checks made from participants' reviewed airline examples.

The two adapters consume the same reviewed starting booking and requested range.
They are deterministic local exercises, not new agent conversations or evidence
that an agent selected a particular action.
"""
from __future__ import annotations

import copy
from pathlib import Path
import time

from . import airline
from .session import digest


def _source_case(session, reviewed):
    source = session.read()['stages'].get(reviewed['source_execution'])
    if not source or source['status'] != 'complete':
        raise ValueError('A regression needs a completed source execution in this workspace')
    run = source.get('result') or {}
    if run.get('split') not in ('discovery', 'monitoring', 'development', 'calibration'):
        raise ValueError('Reserved or subsequent requests cannot enter regression development')
    if run['split'] == 'calibration':
        if run.get('label') != 'calibration-drill' or not source['name'].startswith('airline-calibration/'):
            raise ValueError('Controlled calibration examples must retain their origin')
        case = copy.deepcopy(source['inputs']['case'])
    else:
        case = next((c for c in airline.load_cases() if c['id'] == run.get('case_id')), None)
        if case is None:
            raise ValueError('The source case is unavailable')
    if (reviewed['case_id'] != run['case_id'] or reviewed['request'] != run['mission']
            or reviewed['initial_state'] != run['initial_state'] or reviewed['policy'] != run['policy']
            or case['initial'] != reviewed['initial_state'] or case['mission'] != reviewed['request']):
        raise ValueError('Keep the exact source request, initial state and policy in the reviewed case')
    review = reviewed.get('review') or {}
    if (review.get('decision') != 'accepted' or not review.get('reviewer')
            or not reviewed.get('expected_behavior')
            or review.get('supporting_event_id') not in {event['id'] for event in run['events']}):
        raise ValueError('The accepted review must cite an event from its source execution')
    return case, run


def _execute_adapter(case, builder, scorer):
    environment = airline.AirlineEnvironment(case, builder)
    receipts = []

    def call(name, arguments):
        started = time.time()
        try:
            result = environment.call(name, arguments)
        except Exception as error:
            receipts.append({'id': 'local-regression/' + str(len(receipts)), 'name': name,
                'arguments': arguments, 'result': None, 'error': str(error),
                'started_at': started, 'ended_at': time.time()})
            raise
        receipts.append({'id': 'local-regression/' + str(len(receipts)), 'name': name,
            'arguments': arguments, 'result': result, 'error': None,
            'started_at': started, 'ended_at': time.time()})
        return result

    planned = None
    outcome = 'unchanged' if case['kind'] == 'read_only' else 'declined'
    error = None
    try:
        if case['passenger']['allows_write']:
            scope = case['passenger']
            proposal = call('plan_change', {'replace_start': scope['replace_start'],
                'replace_stop': scope['replace_stop'], 'replacement_flights': scope['replacement']})
            planned = airline.flight_ids(proposal['flights'])
            confirmation = call('request_confirmation', {'flights': planned,
                'fare_difference': proposal['fare_difference']})
            if confirmation['approved']:
                payment_id = next(key for key, payment in environment.world['user']['payment_methods'].items()
                    if payment['source'] == 'credit_card' or
                    (payment['source'] == 'gift_card' and payment['amount'] >= proposal['fare_difference']))
                call('update_reservation_flights', {'reservation_id': environment.world['reservation']['reservation_id'],
                    'flights': planned, 'payment_id': payment_id})
                outcome = 'changed'
            else:
                outcome = 'unresolved'
    except Exception as caught:
        error = f'{type(caught).__name__}: {caught}'
        outcome = 'unresolved'
    result = {'world': environment.world, 'initial_state': copy.deepcopy(case['initial']),
        'request_scope': copy.deepcopy(case['passenger']), 'events': receipts,
        'draft': {'outcome': outcome, 'summary': 'Local adapter check; no agent generated this explanation.'},
        'status': 'adapter_error' if error else 'complete', 'planned_flights': planned, 'error': error}
    result['scores'] = airline.score_booking(case, result)
    if scorer is not None:
        try:
            result['development_scores'] = scorer(copy.deepcopy(result))
        except Exception as caught:
            result['development_scores'] = {'status': 'unavailable', 'error': str(caught)}
    return result


def run_regressions(session, cases, *, itinerary_builder, state_scorer=None):
    """Run both adapters on saved reviewed cases without inference or publication."""
    if not cases:
        raise ValueError('Save at least one reviewed regression case first')
    resolved = [_source_case(session, case) for case in cases]
    sources = {'itinerary_builder.py': airline._source(itinerary_builder),
        'regression.py': Path(__file__).read_text(encoding='utf-8'),
        'airline.py': Path(airline.__file__).read_text(encoding='utf-8')}
    if state_scorer is not None:
        sources['participant_scorer.py'] = airline._source(state_scorer)
    with session.stage('airline/regression-replay', sources=sources,
        inputs={'reviewed_cases': cases}, config={'execution': 'local-adapter', 'model_calls': 0}) as stage:
        if stage.needs_run:
            rows = []
            for reviewed, (case, run) in zip(cases, resolved):
                rows.append({'case_id': reviewed['case_id'], 'source_execution': reviewed['source_execution'],
                    'origin': run.get('scenario_origin', 'Live simulator agent'),
                    'expected_behavior': reviewed['expected_behavior'], 'source_links': reviewed['source_links'],
                    'legacy': _execute_adapter(case, airline.legacy_drill_builder, state_scorer),
                    'repaired': _execute_adapter(case, itinerary_builder, state_scorer)})
            stage.record({'rows': rows, 'passed': all(row['repaired']['scores']['task_success'] for row in rows),
                'dataset_fingerprint': digest(cases), 'builder_fingerprint': digest(sources['itinerary_builder.py']),
                'origin': 'Free deterministic adapter comparison. No agent ran; excluded from live quality scores.',
                'model_calls': 0})
    return {**stage.result, 'stage_id': stage.id}
