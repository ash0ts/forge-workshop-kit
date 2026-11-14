"""Optional, explicitly budgeted base/checkpoint comparison. No automatic POST retries."""

import json
import math
import re
import time

import httpx
from filelock import FileLock

from .managed_jobs import validate_approval
from .publication import credentials
from .routing import route_messages, score, validate_route
from .session import digest


class ComparisonStopped(RuntimeError):
    pass


def comparison_plan(cases, intents, models, *, max_tokens=512):
    """Freeze matching inputs before either model sees a final case."""
    if not cases or len(cases) > 100 or len({c['case_id'] for c in cases}) != len(cases):
        raise ValueError('Choose 1–100 distinct cases before the comparison.')
    if set(models) != {'base', 'checkpoint'} or not intents or len(set(intents)) != len(intents):
        raise ValueError('Provide base and checkpoint models and the full distinct intent list.')
    if type(max_tokens) is not int or not 1 <= max_tokens <= 2048:
        raise ValueError('Choose an output bound from 1 to 2048 tokens.')
    if models['base']['model'] == models['checkpoint']['model']:
        raise ValueError('The base model and trained checkpoint must be different.')
    if not re.fullmatch(r'wandb-artifact:///[^/]+/[^/]+/[^:]+:(?:v|step)\d+', models['checkpoint']['model']):
        raise ValueError('Pin the trained checkpoint to its returned artifact :vN or :stepN identity.')
    for model in models.values():
        if not isinstance(model['model'], str) or not model['model'].strip():
            raise ValueError('Provide the actual inference model ID.')
        for rate in ('input_usd_per_million', 'output_usd_per_million'):
            value = model.get(rate)
            if type(value) not in (float, int) or not math.isfinite(value) or value < 0:
                raise ValueError('Record finite nonnegative current prices for both models.')
    calls = []
    for index, case in enumerate(cases):
        if case.get('split') not in {'test', 'final'} or case['target'] not in intents:
            raise ValueError('Comparison cases must have final/test split and known target labels.')
        messages = route_messages(case['text'], intents)
        input_bound = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096
        if input_bound > 32768:
            raise ValueError('A case exceeds the 32K input bound.')
        # Alternate which condition runs first; both receive byte-identical messages.
        for label in (('base', 'checkpoint') if index % 2 == 0 else ('checkpoint', 'base')):
            config = models[label]
            request = {'model': config['model'], 'messages': messages, 'max_tokens': max_tokens,
                       'temperature': 0.2, 'response_format': {'type': 'json_object'}}
            bound = (input_bound * config['input_usd_per_million']
                     + max_tokens * config['output_usd_per_million']) / 1e6
            calls.append({'case_id': case['case_id'], 'condition': label, 'request': request,
                          'input_bound': input_bound, 'maximum_usd': bound})
    return {'cases': cases, 'intents': intents, 'models': models, 'calls': calls,
            'maximum_usd': sum(call['maximum_usd'] for call in calls)}


def run_comparison(session, plan, *, forecast, approved_usd, transport=None):
    """Save each response before the next request. Restarting reuses completed responses."""
    maximum = validate_approval(forecast, approved_usd)
    # Reconstruct the plan so edited bounds or messages cannot bypass the allowance.
    expected = comparison_plan(plan['cases'], plan['intents'], plan['models'],
                               max_tokens=plan['calls'][0]['request']['max_tokens'])
    if expected != plan or maximum < plan['maximum_usd']:
        raise ValueError('The forecast must cover every request in the unchanged comparison plan.')
    identity = digest([session.workspace_id, plan])[:32]
    key = 'advanced-sft/' + identity
    with FileLock(str(session.root / ('.comparison-' + identity + '.lock'))):
        saved = session.read().get('advanced_comparisons', {}).get(key)
        if saved and saved.get('stop'):
            raise ComparisonStopped(saved['stop'])
        if saved and saved.get('result'):
            return saved['result']
        api_key = credentials()
        with session.transaction() as state:
            state.setdefault('advanced_comparisons', {}).setdefault(key, {
                'plan': plan, 'forecast': forecast, 'approved_usd': approved_usd, 'requests': {}})
        with httpx.Client(timeout=180, transport=transport) as client:
            for call in plan['calls']:
                request_id = digest([identity, call['condition'], call['case_id']])[:32]
                saved = session.read()['advanced_comparisons'][key]['requests'].get(request_id)
                if saved:
                    if saved['status'] == 'pending':
                        raise ComparisonStopped('A request has an uncertain outcome. Inspect it before further comparison; no automatic retry was sent.')
                    continue
                started = time.time()
                with session.transaction() as state:
                    state['advanced_comparisons'][key]['requests'][request_id] = {
                        'id': request_id, **call, 'status': 'pending', 'started_at': started,
                        'observed_usd': None, 'bounded_unknown_usd': call['maximum_usd']}
                response, error, status, headers, stop = {}, None, None, {}, None
                try:
                    answer = client.post('https://api.inference.wandb.ai/v1/chat/completions',
                        headers={'Authorization': 'Bearer ' + api_key, 'OpenAI-Project': session.project},
                        json=call['request'])
                    status = answer.status_code
                    headers = {k: v for k, v in answer.headers.items() if k in ('x-request-id', 'request-id')}
                    response = answer.json()
                    if not isinstance(response, dict):
                        response = {}
                    if status >= 400 or response.get('error'):
                        error = f'Provider rejected this request (HTTP {status}).'
                except (httpx.HTTPError, ValueError) as exc:
                    error = type(exc).__name__
                    stop = 'A provider response was lost or unreadable. Inspect the saved request; it will not be submitted again.'
                usage = response.get('usage') or {}
                if not isinstance(usage, dict):
                    usage = {}
                measured = all(type(usage.get(k)) is int and usage[k] >= 0
                               for k in ('prompt_tokens', 'completion_tokens'))
                rates = plan['models'][call['condition']]
                observed = ((usage['prompt_tokens'] * rates['input_usd_per_million']
                             + usage['completion_tokens'] * rates['output_usd_per_million']) / 1e6
                            if measured else None)
                if response.get('choices') and response.get('model') != call['request']['model']:
                    stop = 'Returned model differs from the requested exact model/checkpoint. No fallback is allowed.'
                if measured and (usage['prompt_tokens'] > call['input_bound']
                                 or usage['completion_tokens'] > call['request']['max_tokens']
                                 or observed > call['maximum_usd']):
                    stop = 'Provider usage exceeded its reserved maximum; comparison stopped.'
                value = None
                if not error and not stop:
                    try:
                        choice = response['choices'][0]
                        if choice.get('finish_reason') == 'length':
                            raise ValueError('Output was truncated.')
                        value = validate_route(json.loads(choice['message']['content']), plan['intents'])
                    except (KeyError, ValueError, IndexError, TypeError):
                        error = 'Response unavailable or invalid under the frozen routing schema.'
                with session.transaction() as state:
                    row = state['advanced_comparisons'][key]['requests'][request_id]
                    row.update(response=response, http_status=status, headers=headers,
                        ended_at=time.time(), observed_usd=observed,
                        bounded_unknown_usd=0 if measured else call['maximum_usd'],
                        status='complete' if value else 'unavailable', output=value, error=error or stop)
                    if stop:
                        state['advanced_comparisons'][key]['stop'] = stop
                if stop:
                    raise ComparisonStopped(stop)
        receipts = session.read()['advanced_comparisons'][key]['requests']
        result = summarize_comparison(plan, list(receipts.values()))
        result['identity'] = key
        with session.transaction() as state:
            state['advanced_comparisons'][key]['result'] = result
        return result


def summarize_comparison(plan, receipts):
    cases = {case['case_id']: case for case in plan['cases']}
    versions, summaries = {}, {}
    for label in ('base', 'checkpoint'):
        rows, available = [], []
        for receipt in receipts:
            if receipt['condition'] != label:
                continue
            case, value = cases[receipt['case_id']], receipt.get('output')
            correct = int(value['intent'] == case['target']) if value else None
            elapsed = receipt.get('ended_at', receipt['started_at']) - receipt['started_at']
            row = {'case_id': case['case_id'], 'input': {'text': case['text']},
                   'prediction': value, 'target': case['target'],
                   'error': None if correct is None else 1 - correct,
                   'scores': {'accuracy': correct, 'latency_seconds': elapsed},
                   'status': receipt['status'], 'request_id': receipt['id']}
            rows.append(row)
            if value:
                available.append({'target': case['target'], 'prediction': value['intent'],
                                  'abstained': value['needs_review'], 'latency_seconds': elapsed})
        summary = score(available)
        if len(available) != len(cases):
            for metric in ('macro_f1', 'accuracy'):
                summary['available_response_' + metric] = summary[metric]
                summary[metric] = None
        summary.update(planned=len(cases), available=len(available), unavailable=len(cases)-len(available),
                       quality_scope='available responses only; inspect unavailable rows separately',
                       cost_note='Usage-priced estimate at the frozen rates; no cache discount assumed.',
                       observed_usd=sum(r.get('observed_usd') or 0 for r in receipts if r['condition'] == label),
                       bounded_unknown_usd=sum(r.get('bounded_unknown_usd') or 0 for r in receipts if r['condition'] == label))
        versions[label], summaries[label] = rows, summary
    return {'versions': versions, 'summaries': summaries, 'plan_fingerprint': digest(plan)}


def publish_comparison_result(session, identity):
    """Publication only: use saved model responses even when an earlier export failed."""
    from .publication import publish_comparison
    from .traces import export_trace
    saved = session.read()['advanced_comparisons'][identity]
    if not saved.get('result'):
        raise ValueError('Finish the comparison before publishing its result table.')
    # Rebuild publication rows from receipts, including journals written before
    # the adapter used the shared prediction-column contract.
    result = summarize_comparison(saved['plan'], list(saved['requests'].values()))
    result['identity'] = identity
    with session.transaction() as state:
        state['advanced_comparisons'][identity]['result'] = result
    trace = export_trace(session, identity.split('/')[-1],
                         'Compare the base model and trained checkpoint on the frozen banking requests.',
                         [], list(saved['requests'].values()))
    links = publish_comparison(session, 'routing-sft-final', result['versions'], summaries=result['summaries'])
    return {'trace': trace, 'comparison': links}
