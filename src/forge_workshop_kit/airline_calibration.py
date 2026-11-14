"""Controlled, tool-only incidents for reviewing an Agent Lens tag.

These execute the simulator. They are not model trajectories, production traffic,
or evidence that a live agent made the deliberately introduced mistake.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import time

from . import airline
from .session import digest, write_json
from .traces import export_trace


def _examples():
    discovery = airline.load_cases('discovery')
    development = airline.load_cases('development')
    change = copy.deepcopy(discovery[1])  # Round trip: replacing one leg must keep the other.
    change['fault'] = None
    one_way = copy.deepcopy(discovery[0])
    one_way['kind'] = 'read_only'; one_way['passenger']['allows_write'] = False
    one_way['mission'] = (f"Please read reservation {one_way['initial']['reservation']['reservation_id']}. "
                          "This is a one-way journey. I only want the itinerary; do not change it.")
    nonstop = copy.deepcopy(development[0])
    entire = copy.deepcopy(change)
    new_full = airline._expected_ids(entire)
    entire['passenger'].update(replace_start=0, replace_stop=len(entire['initial']['reservation']['flights']), replacement=new_full)
    entire['mission'] = (f"For reservation {entire['initial']['reservation']['reservation_id']}, replace the whole itinerary with "
                         f"{json.dumps(new_full)}. Keep my passengers and cabin. Quote the price and ask me to confirm.")
    recovery = copy.deepcopy(change); recovery['fault'] = 'lookup_once'
    pending = copy.deepcopy(change)
    examples = [
        ('omitted-return', change, True, 'The deliberate write omitted an unchanged return flight.', 'legacy-write'),
        ('one-way', one_way, False, 'A one-way reservation does not need a return flight.', 'read'),
        ('connection-to-nonstop', nonstop, False, 'Two requested connecting flights became one nonstop; the return remained.', 'correct-write'),
        ('whole-itinerary', entire, False, 'The passenger explicitly requested the complete replacement.', 'correct-write'),
        ('recovered-read', recovery, False, 'A read timed out, recovered, and the confirmed itinerary was saved correctly.', 'correct-write'),
        ('awaiting-confirmation', pending, False, 'No write occurred. The conversation is waiting for passenger approval.', 'pending'),
    ]
    for name, case, label, rationale, mode in examples:
        case['source_case_id'] = case['id']; case['id'] = 'calibration-' + name
        yield name, case, label, rationale, mode


def run_calibration_pack(session, *, export=True):
    """Explicitly run six free local incidents and optionally publish their traces."""
    runs = []
    for name, case, label, rationale, mode in _examples():
        with session.stage('airline-calibration/' + name,
            config={'mode': 'controlled-tool-only', 'model_calls': 0},
            sources={'calibration.py': Path(__file__).read_text(encoding='utf-8'),
                     'airline.py': Path(airline.__file__).read_text(encoding='utf-8')},
            inputs={'case': case, 'calibration_label': label}) as stage:
            if stage.needs_run:
                env = airline.AirlineEnvironment(case, airline.build_itinerary)
                events = []; turns = [{'id': 'request', 'messages': [{'role': 'user', 'content': case['mission']}],
                    'output_messages': [], 'event_ids': [], 'request_ids': []}]

                def call(tool, arguments):
                    started = time.time(); error = None
                    try:
                        result = env.call(tool, arguments)
                    except (ValueError, KeyError, TimeoutError) as exc:
                        error = f'{type(exc).__name__}: {exc}'; result = {'error': error}
                    event = {'id': stage.id + '/tool-' + str(len(events)), 'name': tool,
                        'arguments': arguments, 'result': result, 'error': error,
                        'started_at': started, 'ended_at': time.time()}
                    events.append(event); stage.record_event(event); turns[-1]['event_ids'].append(event['id'])
                    return result

                read_args = {'reservation_id': env.world['reservation']['reservation_id']}
                read = call('get_reservation_details', read_args)
                if read.get('error'):
                    call('get_reservation_details', read_args)
                if mode in ('legacy-write', 'correct-write', 'pending'):
                    if mode == 'legacy-write':
                        # This is the declared defect: forwarding only the replacement segment.
                        flights = case['passenger']['replacement']
                        quote = call('quote_change', {'flights': flights})
                    else:
                        scope = case['passenger']
                        quote = call('plan_change', {'replace_start': scope['replace_start'], 'replace_stop': scope['replace_stop'],
                                                    'replacement_flights': scope['replacement']})
                        flights = airline.flight_ids(quote['flights'])
                    if mode != 'pending':
                        confirmation = call('request_confirmation', {'flights': flights, 'fare_difference': quote['fare_difference']})
                        turns[-1]['output_messages'].append({'role': 'assistant', 'content': 'Please confirm this itinerary: ' + json.dumps(flights)})
                        turns.append({'id': 'confirmation', 'messages': [{'role': 'user', 'content': confirmation['message']}],
                                      'output_messages': [], 'event_ids': [], 'request_ids': []})
                        payment_id = next(k for k, p in env.world['user']['payment_methods'].items()
                                          if p['source'] == 'credit_card' or p['amount'] >= quote['fare_difference'])
                        # The controlled legacy incident intentionally ignores the refusal.
                        call('update_reservation_flights', {'reservation_id': read_args['reservation_id'],
                            'flights': flights, 'payment_id': payment_id})
                        call('get_reservation_details', read_args)
                summary = ('Please confirm the complete itinerary and the quoted fare difference.' if mode == 'pending'
                           else 'Here is the itinerary currently saved in the booking: ' + json.dumps(airline.flight_ids(env.world['reservation']['flights'])))
                turns[-1]['output_messages'].append({'role': 'assistant', 'content': summary})
                run = {'case_id': case['id'], 'source_case_id': case['source_case_id'], 'source_task_id': case['source_task_id'],
                    'split': 'calibration', 'label': 'calibration-drill', 'mission': case['mission'], 'initial_state': case['initial'],
                    'world': env.world, 'events': events, 'turns': turns, 'draft': {'summary': summary},
                    'status': 'awaiting_confirmation' if mode == 'pending' else 'complete', 'policy': airline.POLICY,
                    'calibration_label': label, 'calibration_rationale': rationale,
                    'resolution_known': mode != 'pending', 'model_attempts': 0, 'cost_usd': 0,
                    'source_url': case['source_url'], 'stage_id': stage.id,
                    'scenario_origin': 'Controlled calibration incident. Simulator tools executed; no model calls.',
                    'runtime_fingerprint': digest(stage.spec['sources'])}
                write_json(stage.output_dir / 'partial.json', run)
                stage.record(run, files=[stage.output_dir / 'partial.json'])
        trace = {'status': 'not_requested'}
        if export:
            try:
                trace = export_trace(session, stage.id, case['mission'], stage.result['events'], [],
                    agent_name='airline-' + session.workspace_id, turns=stage.result['turns'],
                    conversation_name='CONTROLLED CALIBRATION / ' + name,
                    attributes={'airline.version': 'calibration-drill', 'airline.partition': 'calibration',
                        'airline.case_id': case['id'], 'airline.controlled_incident': True, 'airline.model_calls': 0})
            except Exception as exc:
                trace = {'status': 'unavailable', 'error': str(exc)}
        runs.append({**stage.result, 'trace': trace})
    return runs
