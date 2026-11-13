"""Direct W&B Inference with a durable per-workspace allowance."""
from __future__ import annotations
import json
import time
import httpx
from .publication import credentials

MODEL = 'zai-org/GLM-5.3-Flash'
# Published W&B prices previously qualified for Pending; live qualification rechecks them.
PRICES = {'input': 0.12, 'output': 0.38, 'cache_hit': 0.02}
PRICE_SOURCE = 'https://www.coreweave.com/forge-pricing/inference-agents'
PRICE_DATE = '2026-11-13'


class ProviderStop(RuntimeError):
    pass


class Provider:
    def __init__(self, session, *, transport=None, sleeper=time.sleep):
        self.session = session
        self.http = httpx.Client(timeout=180, transport=transport)
        self.sleep = sleeper

    def summary(self):
        requests = self.session.read()['requests'].values()
        return {'observed_usd': sum(r.get('observed_usd') or 0 for r in requests),
                'bounded_unknown_usd': sum(r.get('unknown_usd', 0) for r in requests),
                'inflight_usd': sum(r['reserved_usd'] for r in requests if r['status'] == 'pending')}

    def complete(self, request_id, messages, *, max_tokens=8192):
        if not 1 <= max_tokens <= 16384:
            raise ValueError('Output limit must be 1–16384 tokens.')
        request = dict(model=MODEL, messages=messages, max_tokens=max_tokens,
                       temperature=0.2, response_format={'type': 'json_object'})
        # Conservative bytes-plus-overhead bound. This is separate from context capacity.
        input_bound = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096
        if input_bound > 32768:
            raise ProviderStop('Evidence exceeds the 32K input bound. Select a smaller evidence set.')
        reserved = (input_bound * PRICES['input'] + max_tokens * PRICES['output']) / 1e6
        for attempt in range(3):
            key = request_id + '/' + str(attempt)
            with self.session.transaction() as state:
                existing = state['requests'].get(key)
                if existing:
                    if existing['status'] == 'complete':
                        return existing
                    raise ProviderStop('This request has a saved uncertain/failed attempt. Inspect it before explicitly starting another request.')
                if state.get('accounting_stop'):
                    raise ProviderStop(state['accounting_stop'])
                if state.get('provider_cooldown', 0) > time.time():
                    raise ProviderStop('Provider cooling down after repeated failures. No request sent.')
                used = sum(r['reserved_usd'] if r['status'] == 'pending' else
                           (r.get('observed_usd') or 0) + r.get('unknown_usd', 0)
                           for r in state['requests'].values())
                if used + reserved > self.session.budget_usd:
                    raise ProviderStop('Inference allowance exhausted. Saved work remains available.')
                state['requests'][key] = dict(id=key, request=request, status='pending',
                                              reserved_usd=reserved, prices=PRICES, price_date=PRICE_DATE, started_at=time.time())
            # In a hosted runtime, preserve the reservation before sending money-bearing work.
            if self.session.publisher and self.session.identity.get('notebook_identity'):
                self.session.publisher.publish_checkpoint()
            response, status, headers, error = {}, None, {}, None
            try:
                answer = self.http.post('https://api.inference.wandb.ai/v1/chat/completions',
                    headers={'Authorization': 'Bearer ' + credentials(), 'OpenAI-Project': self.session.project},
                    json=request)
                status = answer.status_code
                headers = {k:v for k,v in answer.headers.items() if k in ('x-request-id', 'request-id', 'retry-after')}
                response = answer.json()
                if not isinstance(response, dict):
                    response = {}
                if status >= 400 or response.get('error'):
                    error = str(response.get('error', f'HTTP {status}'))[:500]
            except Exception as exc:
                error = f'{type(exc).__name__}: {exc}'[:500]
            usage = response.get('usage') or {}
            measured = all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('prompt_tokens', 'completion_tokens'))
            cached=(usage.get('prompt_tokens_details') or {}).get('cached_tokens',0)
            if type(cached) is not int or cached<0 or (measured and cached>usage['prompt_tokens']):
                cached=0
            observed = (((usage['prompt_tokens']-cached) * PRICES['input'] + cached*PRICES['cache_hit'] + usage['completion_tokens'] * PRICES['output']) / 1e6) if measured else None
            stop = None
            if response.get('model') is not None and response['model'] != MODEL:
                stop = 'Returned model differs from the frozen model.'
            if response.get('choices') and response.get('model') is None:
                stop = 'Successful provider response has no model identity.'
            if measured and (usage['prompt_tokens'] > input_bound or usage['completion_tokens'] > max_tokens or observed > reserved):
                stop = 'Usage exceeded its reservation; inference is stopped.'
            with self.session.transaction() as state:
                row = state['requests'][key]
                row.update(response=response, http_status=status, headers=headers, error=error,
                    ended_at=time.time(), observed_usd=observed, unknown_usd=0 if measured else reserved,
                    status='complete' if not error and response.get('choices') and not stop else 'failed')
                state['provider_failures'] = state.get('provider_failures', 0) + 1 if row['status'] == 'failed' else 0
                if state['provider_failures'] >= 3:
                    state['provider_cooldown'] = time.time() + 30
                    state['provider_failures'] = 0
                if stop:
                    state['accounting_stop'] = stop
                record = dict(row)
            if stop:
                raise ProviderStop(stop)
            if self.session.publisher and self.session.identity.get('notebook_identity'):
                self.session.publisher.publish_checkpoint()
            if record['status'] == 'complete':
                return record
            if status in (401, 403):
                raise ProviderStop(f'Inference access denied (HTTP {status}). Check this account’s credentials and inference billing.')
            if attempt == 2 or (status is not None and status != 429 and status < 500):
                raise ProviderStop(error or 'Provider returned no completion.')
            self.sleep(2 ** attempt)
        raise ProviderStop('Provider unavailable')


def output(record):
    choice = record['response']['choices'][0]
    if choice.get('finish_reason') == 'length':
        raise ValueError('Incomplete response: output limit reached.')
    content = choice['message'].get('content') or ''
    if content.startswith('```'):
        content = content.split('\n', 1)[1].rsplit('```', 1)[0]
    value = json.loads(content)
    if not isinstance(value, dict):
        raise ValueError('Expected a structured JSON object.')
    return value


def validated_json(session, request_id, messages, validate, *, max_tokens=8192):
    """At most one schema-repair request; every attempt remains charged and saved."""
    context=list(messages)
    for attempt in range(2):
        record=Provider(session).complete(request_id+'/schema-'+str(attempt),context,max_tokens=max_tokens)
        try:
            value=output(record)
            validate(value)
            return value,record
        except (ValueError,KeyError,TypeError,SyntaxError) as error:
            if attempt: raise
            # Keep original evidence; ask only for correction of the explicit validation failure.
            context.append({'role':'user','content':'Your previous answer failed validation: '+str(error)[:600]+'. Return a complete corrected answer using the requested schema.'})
