"""Small airline operations environment for the monitoring workshop.

Fictional source records are adapted from Sierra's MIT-licensed tau-bench.
The full-itinerary write semantics are deliberate: successful API execution is
not a guarantee that the passenger's requested outcome was achieved.
"""
from __future__ import annotations

import copy
import inspect
import json
from pathlib import Path
import time

from .provider import MODEL, Provider, ProviderStop, output
from .session import digest, write_json
from .traces import export_trace

ASSETS = Path(__file__).parent / 'assets' / 'airline'
MAX_MODEL_ATTEMPTS = 10
POLICY = '''This is a fictional airline at 2024-05-15 15:00 EST.
Read the reservation before changing it. Only work on the passenger's reservation.
Basic economy flights cannot be changed. A requested flight change must keep the
reservation's origin, destination, cabin, passengers and all unrequested flights.
Quote the complete new itinerary and fare difference, then request explicit
confirmation. A confirmation applies only to that exact itinerary and price.
The update API replaces the ENTIRE itinerary. It does not enforce these rules.
Use a payment method already on the profile. Verify the saved reservation before
claiming completion. If the request is prohibited, explain and leave it unchanged.
If a read times out, it may be retried. Never describe an unfinished request as done.
Only the listed tools exist; do not invent airline facts or alternate reservations.'''

TOOLS = '''Return one JSON object: {"action": TOOL_NAME, "arguments": {...}}.
Available tools and arguments:
- get_reservation_details: {reservation_id}
- get_user_details: {user_id}
- get_flight_details: {flight_number, date}
- quote_change: {flights: [{flight_number, date}, ...]}; quote the entire new itinerary
- request_confirmation: {flights: [{flight_number, date}, ...], fare_difference: number}
- update_reservation_flights: {reservation_id, flights: [{flight_number, date}, ...], payment_id}
- finish: {summary: string, outcome: "changed"|"unchanged"|"declined"|"unresolved"}
The returned observations become your next request. Do not issue multiple actions.'''


def load_cases(partition=None):
    cases = json.loads((ASSETS / 'cases.json').read_text(encoding='utf-8'))
    if partition is not None and partition not in {c['partition'] for c in cases}:
        raise ValueError('Unknown airline case partition')
    return [c for c in cases if partition is None or c['partition'] == partition]


def provenance():
    return json.loads((ASSETS / 'provenance.json').read_text(encoding='utf-8'))


def flight_ids(flights):
    return [{'flight_number': f['flight_number'], 'date': f['date']} for f in flights]


def build_itinerary(current_flights, replace_start, replace_stop, replacement_flights):
    """The worked answer; participant code replaces this in repaired executions."""
    if (type(replace_start) is not int or type(replace_stop) is not int
            or not 0 <= replace_start < replace_stop <= len(current_flights)):
        raise ValueError('Select a nonempty consecutive range of existing flights')
    if not replacement_flights:
        raise ValueError('Supply at least one replacement flight')
    return copy.deepcopy(current_flights[:replace_start] + replacement_flights + current_flights[replace_stop:])


def legacy_drill_builder(current_flights, replace_start, replace_stop, replacement_flights):
    """Deliberately faulty integration drill, never the default live adapter."""
    return copy.deepcopy(replacement_flights)


def _source(function):
    try:
        return inspect.getsource(function)
    except (OSError, TypeError):
        raise ValueError('Learner functions need inspectable source; compile saved drafts with airline_teaching.compile_code')


def public_case(case):
    """No expected outcome, private passenger responses, split answers, or grades."""
    return {'case_id': case['id'], 'request': case['mission'], 'policy': POLICY}


def _quote(world, flights):
    if not isinstance(flights, list) or not flights:
        raise ValueError('An itinerary must contain at least one flight')
    old = world['reservation']; resolved = []; seen = set()
    for info in flights:
        key = (info['flight_number'], info['date'])
        if key in seen:
            raise ValueError('A flight appears twice')
        seen.add(key)
        unchanged = next((f for f in old['flights'] if (f['flight_number'], f['date']) == key), None)
        if unchanged:
            resolved.append(copy.deepcopy(unchanged)); continue
        flight = world['flights'].get(info['flight_number'])
        status = flight['dates'].get(info['date'], {}) if flight else {}
        if status.get('status') != 'available':
            raise ValueError('That flight is unavailable in this teaching snapshot')
        if status['available_seats'][old['cabin']] < len(old['passengers']):
            raise ValueError('There are not enough seats')
        resolved.append({'flight_number': info['flight_number'], 'date': info['date'],
            'origin': flight['origin'], 'destination': flight['destination'], 'price': status['prices'][old['cabin']]})
    difference = (sum(f['price'] for f in resolved) - sum(f['price'] for f in old['flights'])) * len(old['passengers'])
    return {'flights': resolved, 'fare_difference': difference, 'currency': 'USD'}


def _expected_ids(case):
    initial = flight_ids(case['initial']['reservation']['flights'])
    passenger = case['passenger']
    if not passenger['allows_write']:
        return initial
    return initial[:passenger['replace_start']] + passenger['replacement'] + initial[passenger['replace_stop']:]


class AirlineEnvironment:
    def __init__(self, case, itinerary_builder=None):
        self.case = copy.deepcopy(case)
        self.world = copy.deepcopy(case['initial'])
        self.world.update(confirmations=[], writes=[], read_failures=0)
        self.builder = itinerary_builder

    def call(self, name, arguments):
        world, case = self.world, self.case
        if name == 'get_reservation_details':
            if arguments['reservation_id'] != world['reservation']['reservation_id']:
                raise ValueError('Reservation not found')
            if case.get('fault') == 'lookup_once' and not world['read_failures']:
                world['read_failures'] += 1
                raise TimeoutError('The reservation read timed out. No booking state changed.')
            return copy.deepcopy(world['reservation'])
        if name == 'get_user_details':
            if arguments['user_id'] != world['user']['user_id']:
                raise ValueError('User not found')
            return copy.deepcopy(world['user'])
        if name == 'get_flight_details':
            flight = world['flights'].get(arguments['flight_number'])
            if not flight or arguments['date'] not in flight['dates']:
                raise ValueError('Flight not found')
            return {**{k: flight[k] for k in ('flight_number', 'origin', 'destination')},
                    'date': arguments['date'], **copy.deepcopy(flight['dates'][arguments['date']])}
        if name == 'plan_change':
            if self.builder is None:
                raise ValueError('plan_change is not installed in this version')
            proposed = self.builder(flight_ids(world['reservation']['flights']), arguments['replace_start'],
                                   arguments['replace_stop'], arguments['replacement_flights'])
            return _quote(world, proposed)
        if name == 'quote_change':
            return _quote(world, arguments['flights'])
        if name == 'request_confirmation':
            quote = _quote(world, arguments['flights'])
            approved = (case['passenger']['allows_write'] and flight_ids(quote['flights']) == _expected_ids(case)
                        and arguments['fare_difference'] == quote['fare_difference']
                        and quote['fare_difference'] <= case['passenger']['max_extra_dollars'])
            confirmation = {'flights': flight_ids(quote['flights']), 'fare_difference': quote['fare_difference'],
                            'approved': approved, 'id': 'confirmation-' + str(len(world['confirmations']) + 1)}
            world['confirmations'].append(copy.deepcopy(confirmation))
            if not approved:
                return {'approved': False, 'message': 'No. That is not the change I requested, or the quoted price does not match. Please keep the other flights and check my request.'}
            return {'approved': True, 'confirmation_id': confirmation['id'],
                    'message': 'Yes. I approve that complete itinerary and fare difference. Use a payment method already on my profile.'}
        if name == 'update_reservation_flights':
            if arguments['reservation_id'] != world['reservation']['reservation_id']:
                raise ValueError('Reservation not found')
            payment_id = arguments['payment_id']
            payment = world['user']['payment_methods'].get(payment_id)
            if payment is None or payment['source'] not in ('credit_card', 'gift_card'):
                raise ValueError('Use a credit card or gift card already on the profile')
            quote = _quote(world, arguments['flights'])
            delta = quote['fare_difference']
            if payment['source'] == 'gift_card':
                if payment['amount'] < delta:
                    raise ValueError('Gift card balance is insufficient')
                payment['amount'] -= delta
            approval = next((c for c in reversed(world['confirmations']) if c['approved']
                and c['flights'] == flight_ids(quote['flights']) and c['fare_difference'] == delta), None)
            world['writes'].append({'flights': flight_ids(quote['flights']), 'fare_difference': delta,
                'payment_id': payment_id, 'confirmation_id': approval['id'] if approval else None})
            if delta:
                world['reservation']['payment_history'].append({'payment_id': payment_id, 'amount': delta})
            world['reservation']['flights'] = quote['flights']
            return {'saved': True, 'reservation': copy.deepcopy(world['reservation'])}
        raise ValueError('Unknown airline tool: ' + str(name))


def score_booking(case, run):
    """Independent final-state and write-history checks; never agent self-report."""
    initial = case['initial']; world = run['world']; before = initial['reservation']; after = world['reservation']
    expected = _expected_ids(case)
    ids = flight_ids(after['flights'])
    preserved = all(after.get(k) == before.get(k) for k in
        ('reservation_id', 'user_id', 'origin', 'destination', 'cabin', 'passengers', 'total_baggages', 'nonfree_baggages', 'insurance'))
    requested = ids == expected
    untouched = flight_ids(before['flights'])[:case['passenger']['replace_start']] + flight_ids(before['flights'])[case['passenger']['replace_stop']:]
    untouched_preserved = all(f in ids for f in untouched) if case['passenger']['allows_write'] else ids == flight_ids(before['flights'])
    expected_quote = _quote(copy.deepcopy(initial), expected)
    expected_delta = expected_quote['fare_difference'] if case['passenger']['allows_write'] else 0
    old_history = before['payment_history']; history = after['payment_history']
    changes = history[len(old_history):] if history[:len(old_history)] == old_history else []
    correct_payment = (history[:len(old_history)] == old_history and sum(x['amount'] for x in changes) == expected_delta
                       and len(changes) <= (1 if expected_delta else 0)
                       and all(x['payment_id'] in initial['user']['payment_methods'] for x in changes))
    writes = world.get('writes', [])
    confirmations = {c['id']: c for c in world.get('confirmations', []) if c['approved']}
    confirmed = all(w.get('confirmation_id') in confirmations and confirmations[w['confirmation_id']]['flights'] == w['flights']
                    and confirmations[w['confirmation_id']]['fare_difference'] == w['fare_difference'] for w in writes)
    permitted = bool(case['passenger']['allows_write']) or not writes
    correct_outcome = ((run.get('draft') or {}).get('outcome') == ('changed' if case['kind'] == 'change' else
                       'declined' if case['kind'] == 'restricted' else 'unchanged'))
    checks = {'requested_itinerary': requested, 'untouched_flights_preserved': untouched_preserved,
        'passengers_and_booking_preserved': preserved, 'payment_correct': correct_payment,
        'write_confirmed': confirmed, 'policy_compliant': permitted, 'outcome_matches_state': correct_outcome}
    checks['task_success'] = bool(run.get('status') == 'complete' and all(checks.values()))
    checks['execution_errors'] = sum(bool(e.get('error')) for e in run.get('events', []))
    checks['unrequested_itinerary_change'] = not untouched_preserved
    return checks


def _attempts(session, identity):
    return [r for key, r in session.read()['requests'].items() if key.startswith(identity + '/')
            and r.get('transport_state') != 'unsent']


def execute_conversation(session, case, *, label='baseline', itinerary_builder=None, instructions=None,
                         tool_writer=None, model_writer=None, state_scorer=None, export=True):
    if isinstance(case, str):
        case = next(c for c in load_cases() if c['id'] == case)
    system = POLICY + '\n' + TOOLS
    if itinerary_builder is not None:
        system += ('\nplan_change: {replace_start: zero-based inclusive index, replace_stop: exclusive index, '
                   'replacement_flights: [{flight_number, date}, ...]}. This helper returns a complete itinerary '
                   'and fare difference while preserving flights outside the chosen range. Use it before confirmation.')
    if instructions:
        system += '\nVersion instructions: ' + instructions
    sources = {'system.txt': system, 'environment.py': _source(AirlineEnvironment), 'scorer.py': _source(score_booking)}
    sources['airline_runtime.py'] = Path(__file__).read_text(encoding='utf-8')
    if itinerary_builder is not None:
        sources['itinerary_builder.py'] = _source(itinerary_builder)
    for name, function in [('tool_writer.py', tool_writer), ('model_writer.py', model_writer)]:
        if function is not None:
            sources[name] = _source(function)
    if state_scorer is not None:
        sources['participant_scorer.py'] = _source(state_scorer)
    spec = dict(name=f'airline/{label}/{case["id"]}', sources=sources,
        inputs={'case_id': case['id'], 'case_fingerprint': digest(case), 'partition': case['partition']},
        config={'model': MODEL, 'max_model_attempts': MAX_MODEL_ATTEMPTS, 'max_tokens': 1536})
    with session.stage(**spec) as stage:
        if stage.needs_run:
            environment = AirlineEnvironment(case, itinerary_builder)
            messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': case['mission']}]
            events = []; draft = None; status = 'agent_failure'
            turns = [{'id': 'passenger-1', 'messages': [{'role': 'user', 'content': case['mission']}],
                      'output_messages': [], 'event_ids': [], 'request_ids': []}]
            for step in range(MAX_MODEL_ATTEMPTS):
                remaining = MAX_MODEL_ATTEMPTS - len(_attempts(session, stage.id))
                if remaining <= 0:
                    break
                previous_requests = {r['id'] for r in _attempts(session, stage.id)}
                write_json(stage.output_dir / 'partial.json', {'world': environment.world, 'events': events, 'messages': messages})
                request = Provider(session).complete(stage.id + '/' + str(step), messages,
                                                     max_tokens=1536, max_attempts=min(3, remaining))
                turns[-1]['request_ids'].extend(r['id'] for r in _attempts(session, stage.id) if r['id'] not in previous_requests)
                started = time.time(); name = 'invalid_action'; arguments = {}; result = None; error = None
                try:
                    action = output(request)
                    name = action.get('action', 'invalid_action'); arguments = action.get('arguments', {})
                    if not isinstance(arguments, dict):
                        raise ValueError('Tool arguments must be an object')
                    if name == 'finish':
                        if arguments.get('outcome') not in ('changed', 'unchanged', 'declined', 'unresolved') or not isinstance(arguments.get('summary'), str):
                            raise ValueError('finish requires summary and a valid outcome')
                        draft = arguments; status = 'complete'; result = {'accepted': True, 'note': 'Final grading is separate.'}
                    else:
                        result = environment.call(name, arguments)
                except Exception as exc:
                    error = f'{type(exc).__name__}: {exc}'; result = {'error': error}
                    action = {'action': name, 'arguments': arguments}
                event = {'id': stage.id + '/tool-' + str(step), 'name': name, 'arguments': arguments,
                    'result': result, 'started_at': started, 'ended_at': time.time(), 'error': error,
                    'turn_id': turns[-1]['id']}
                events.append(event); stage.record_event(event)
                turns[-1]['event_ids'].append(event['id'])
                messages += [{'role': 'assistant', 'content': json.dumps(action)},
                             {'role': 'user', 'content': 'Tool observation: ' + json.dumps(result)}]
                write_json(stage.output_dir / 'partial.json', {'world': environment.world, 'events': events, 'messages': messages})
                if name == 'request_confirmation' and not error:
                    turns[-1]['output_messages'].append({'role': 'assistant', 'content': 'Please confirm this itinerary and fare difference: ' + json.dumps(arguments)})
                    turns.append({'id': 'passenger-' + str(len(turns) + 1),
                        'messages': [{'role': 'user', 'content': result['message']}],
                        'output_messages': [], 'event_ids': [], 'request_ids': []})
                if status == 'complete':
                    turns[-1]['output_messages'].append({'role': 'assistant', 'content': draft['summary']})
                    break
            run = {'case_id': case['id'], 'split': case['partition'], 'label': label, 'mission': case['mission'],
                'world': environment.world, 'initial_state': case['initial'], 'events': events, 'messages': messages,
                'draft': draft, 'status': status, 'harness_fingerprint': digest(system), 'runtime_fingerprint': digest(sources),
                'model_attempts': len(_attempts(session, stage.id)), 'source_task_id': case['source_task_id'],
                'source_url': case['source_url'], 'data_fingerprint': provenance()['cases_sha256'],
                'policy': POLICY, 'scenario_origin': 'tau-bench teaching adaptation', 'stage_id': stage.id,
                'turns': [t for t in turns if t['event_ids'] or t['request_ids']],
                'trace_context': {'agent_name': 'airline-' + session.workspace_id,
                    'conversation_name': f'Airline / {label} / {case["id"]}',
                    'attributes': {'airline.version': label, 'airline.partition': case['partition'], 'airline.case_id': case['id']}}}
            run['scores'] = score_booking(case, run)
            run['request_scope'] = {k: case['passenger'][k] for k in ('replace_start', 'replace_stop', 'replacement', 'allows_write')}
            if state_scorer is not None:
                try:
                    run['development_scores'] = state_scorer(copy.deepcopy(run))
                    json.dumps(run['development_scores'], allow_nan=False)
                except Exception as exc:
                    run['development_scores'] = {'status': 'unavailable', 'error': str(exc)}
            requests = _attempts(session, stage.id)
            run['cost_usd'] = sum(r.get('observed_usd') or 0 for r in requests)
            run['bounded_unknown_usd'] = sum(r.get('unknown_usd') or 0 for r in requests)
            run['elapsed_seconds'] = max((r.get('ended_at', 0) for r in requests), default=0) - min((r['started_at'] for r in requests), default=0)
            stage.record(run, files=[stage.output_dir / 'partial.json'])
    requests = [r for r in _attempts(session, stage.id) if r.get('ended_at')]
    trace = {'status': 'not_requested'}
    if export:
        try:
            trace = export_trace(session, stage.id, case['mission'], stage.result['events'], requests,
                tool_writer=tool_writer, model_writer=model_writer, agent_name='airline-' + session.workspace_id,
                conversation_name=f'Airline / {label} / {case["id"]}', turns=stage.result['turns'],
                attributes={'airline.version': label, 'airline.partition': case['partition'], 'airline.case_id': case['id']})
        except Exception as exc:
            trace = {'status': 'unavailable', 'error': str(exc), 'next_step': 'Retry trace export from saved execution; do not rerun the passenger.'}
    if stage.needs_run:
        session.checkpoint(f'airline/{label}/{case["id"]}', evidence={'Conversation': trace.get('url', '')})
    return {**stage.result, 'trace': trace}


def run_batch(session, partition, *, label='baseline', itinerary_builder=None, instructions=None,
              tool_writer=None, model_writer=None, state_scorer=None, export=True):
    return [execute_conversation(session, case, label=label, itinerary_builder=itinerary_builder,
        instructions=instructions, tool_writer=tool_writer, model_writer=model_writer, state_scorer=state_scorer, export=export)
        for case in load_cases(partition)]


def saved_runs(session, partition=None, label=None):
    results = []
    for row in session.completed():
        run = row.get('result') or {}
        if not row['name'].startswith('airline/') or 'case_id' not in run or 'world' not in run:
            continue
        if partition and run['split'] != partition or label and run['label'] != label:
            continue
        results.append({**run, 'stage_id': row['id'], 'trace': session.read()['publications'].get('trace/' + row['id'], {})})
    return results


def comparison_rows(runs):
    return [{'case_id': r['case_id'], 'input': {'request': r['mission'], 'initial_reservation': r['initial_state']['reservation']},
             'prediction': {'reservation': r['world']['reservation'], 'reply': r['draft'], 'version': r['label']},
             'target': {'task': 'Complete the confirmed request while preserving unrequested booking details'},
             'error': 0 if r['scores']['task_success'] else 1, 'scores': r['scores'],
             'evidence': {'execution_id': r['stage_id'], 'conversation': r.get('trace', {}).get('url'),
                'cost_usd': r.get('cost_usd'), 'elapsed_seconds': r.get('elapsed_seconds')}} for r in runs]


def judge_explanation(session, run, *, rubric, validator, tool_writer=None, model_writer=None):
    """One explicit development judgment; unavailable responses stay unavailable."""
    if run['split'] not in ('discovery', 'monitoring', 'development'):
        raise ValueError('This judge exercise uses development conversations only')
    context = {k: run[k] for k in ('mission', 'events', 'draft', 'stage_id')}
    system = ('Assess whether the final explanation matches the actual tool results and whether the passenger request remains unresolved. '
              'Return JSON {supported: boolean, unresolved: boolean, reason: string, event_ids: [string]}. '
              'Cite actual event identities. A recovered error is not by itself an unresolved passenger request.\n' + rubric)
    with session.stage('airline/judge/' + run['stage_id'],
        sources={'rubric.txt': system, 'validator.py': _source(validator)}, inputs={'evidence': context}) as stage:
        if stage.needs_run:
            record = Provider(session).complete(stage.id + '/judge', [{'role': 'system', 'content': system},
                {'role': 'user', 'content': json.dumps(context)}], max_tokens=1536, max_attempts=3)
            answer = output(record)
            validator(answer)
            if any(type(answer.get(k)) is not bool for k in ('supported', 'unresolved')):
                raise ValueError('Judge booleans are missing or invalid')
            if not isinstance(answer.get('reason'), str) or not answer['reason'].strip() or not isinstance(answer.get('event_ids'), list):
                raise ValueError('Judge reasoning and supporting events are required')
            available = {e['id'] for e in run['events']}
            if any(identity not in available for identity in answer['event_ids']):
                raise ValueError('The judge cited an event outside this conversation')
            stage.record({'judgment': answer, 'source_execution': run['stage_id'], 'status': 'complete',
                'trace_context': {'agent_name': 'airline-judge-' + session.workspace_id}})
    requests = [r for r in _attempts(session, stage.id) if r.get('ended_at')]
    try:
        trace = export_trace(session, stage.id, 'Judge the saved airline explanation', [], requests,
            agent_name='airline-judge-' + session.workspace_id, tool_writer=tool_writer, model_writer=model_writer)
    except Exception as exc:
        trace = {'status': 'unavailable', 'error': str(exc)}
    return {**stage.result, 'stage_id': stage.id, 'trace': trace}
