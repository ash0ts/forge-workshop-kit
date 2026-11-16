"""Explicit ARIA requests using participant authentication and durable handles.

Protocol reference: wandb/wandb-mcp-server at
7a1f9f629d4977d41d31b7b84a1227bc9da2cb90, mcp_tools/aria.py, and the public
https://wb-agent.wandb.ai/openapi.json schema reviewed on 2026-11-16.
This adapter has no background thread, startup hook, or implicit POST retry.
"""
from __future__ import annotations

import json
import os
import time
from urllib.parse import quote, unquote, urlparse

import httpx

from .session import digest

BASE_URL = 'https://wb-agent.wandb.ai'
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
MAX_PROMPT_BYTES = 32 * 1024
STATES = {'queued', 'in_progress', 'completed', 'errored', 'cancelled'}
TERMINAL = {'completed', 'errored', 'cancelled'}
# A timeout/conflict response can follow an accepted operation. Only these
# definite request/auth/rate rejections allow a later explicit POST retry.
REJECTED_STATUSES = {400, 401, 403, 404, 405, 413, 415, 422, 429}


class AriaError(RuntimeError):
    def __init__(self, message, *, status=None, outcome_unknown=False):
        super().__init__(message)
        self.status = status
        self.outcome_unknown = outcome_unknown


def _key(context):
    return 'aria/request/' + context['stop_id'] + '/' + context['id']


def saved_investigation(session, context):
    """Read the local receipt only. Reopening a notebook never contacts ARIA."""
    return session.get_draft(_key(context), {}) if session else {}


def _current_context(session, context):
    from .aria import build_aria_context
    current = build_aria_context(session, context['stop_id'],
        [row['identity'] for row in context['records']], case_ids=context.get('case_ids'))
    if current['id'] != context['id'] or not current['records']:
        raise ValueError('Select completed evidence from this workspace before starting ARIA.')
    return current


def native_context_parts(context):
    """Attach only exact run/conversation identities already in the allowlisted context.

    Artifact URLs stay in the prompt: a collection attachment would be broader
    than the exact saved version. A conversation ID is never used as a call ID.
    """
    entity, project = context['project'].split('/', 1)
    parts = []
    for row in context['records']:
        for link in row['links']:
            path = unquote(urlparse(link['url']).path).strip('/')
            suffix = None
            for prefix in (f'{entity}/{project}/runs/', f'wandb/{entity}/{project}/runs/'):
                if path.startswith(prefix):
                    suffix = path[len(prefix):].split('/')[0]
            if suffix:
                part = dict(type='wandb_run', entity_name=entity, project_name=project, run_name=suffix)
            elif path.startswith(f'agent-lens/{entity}/{project}/conversations/'):
                identity = path.split('/conversations/', 1)[1].split('/')[0]
                part = dict(type='wandb_conversation', entity_name=entity, project_name=project, conversation_id=identity)
            else:
                continue
            if part not in parts:
                parts.append(part)
    return parts


class AriaClient:
    """Small synchronous HTTP adapter; submission returns an asynchronous handle."""
    def __init__(self, *, api_key=None, transport=None):
        if os.getenv('WANDB_BASE_URL', 'https://api.wandb.ai').rstrip('/') != 'https://api.wandb.ai':
            raise PermissionError('This direct ARIA path supports W&B Multi-tenant Cloud. Use your deployment’s native ARIA or the recorded activity.')
        try:
            # Resolve the cloud host explicitly. A saved W&B setting for a
            # self-hosted deployment must never supply its key to cloud ARIA.
            key = api_key or os.getenv('WANDB_API_KEY')
            if not key:
                import wandb
                key = wandb.Api(overrides={'base_url': 'https://api.wandb.ai'}).api_key
            if not key:
                raise PermissionError('No cloud credentials available.')
        except Exception as error:
            raise PermissionError('Forge authentication is unavailable. Sign in again, then explicitly start ARIA, or use the recording.') from error
        self.http = httpx.Client(base_url=BASE_URL, transport=transport,
            headers={'Authorization': 'Bearer ' + key, 'Accept': 'application/json',
                     'Accept-Encoding': 'identity', 'Content-Type': 'application/json'},
            timeout=httpx.Timeout(15, connect=5), follow_redirects=False)

    def close(self):
        self.http.close()

    def request(self, method, path, *, payload=None):
        sending = method == 'POST'
        try:
            with self.http.stream(method, path, json=payload) as response:
                status = response.status_code
                if not 200 <= status < 300:
                    messages = {401: 'Forge authentication expired. Sign in again, then explicitly retry.',
                        403: 'This account or project cannot use ARIA. Check Smart features and team access, or use the recording.',
                        404: 'The ARIA service or saved conversation is unavailable to this account.',
                        422: 'ARIA rejected this request. Use the manual prompt or recording.',
                        429: 'ARIA is rate limited. Wait before explicitly trying again.'}
                    raise AriaError(messages.get(status, f'ARIA returned HTTP {status}. Open ARIA to inspect the request.'),
                        status=status, outcome_unknown=sending and status not in REJECTED_STATUSES)
                if response.headers.get('content-encoding', 'identity') not in ('', 'identity'):
                    raise AriaError('ARIA returned an unsupported compressed response.', outcome_unknown=sending)
                content = bytearray()
                for chunk in response.iter_bytes():
                    content.extend(chunk)
                    if len(content) > MAX_RESPONSE_BYTES:
                        raise AriaError('ARIA response exceeds the local read limit. Open the conversation in Forge.', outcome_unknown=sending)
                value = json.loads(content)
                if not isinstance(value, dict):
                    raise ValueError('expected an object')
                return value
        except (httpx.RequestError, ValueError) as error:
            # Exception text can contain a request header or server body. Store
            # only this fixed explanation, never a credential-bearing exception.
            raise AriaError('ARIA did not return a readable response. Inspect the saved conversation before sending again.',
                outcome_unknown=sending) from error

    def submit(self, payload):
        return self.request('POST', '/api/v1/turns', payload=payload)

    def get(self, turn_id):
        return self.request('GET', '/api/v1/turns/' + quote(turn_id, safe=''))

    def name_thread(self, thread_id, title):
        return self.request('PATCH', '/api/v1/threads/' + quote(thread_id, safe=''), payload={'title': title[:255]})


def _snapshot(turn, receipt):
    if (not isinstance(turn.get('id'), str) or not turn['id'] or len(turn['id']) > 512
            or turn.get('state') not in STATES):
        raise AriaError('ARIA did not return a valid turn handle.', outcome_unknown=True)
    if receipt.get('turn_id') and turn['id'] != receipt['turn_id']:
        raise AriaError('ARIA returned a different turn. The saved handle has been retained.')
    entity, project = receipt['project'].split('/', 1)
    if turn.get('wandb_entity') != entity or turn.get('wandb_project') != project:
        raise AriaError('ARIA returned another project. Do not use this answer for the selected evidence.', outcome_unknown=True)
    thread = turn.get('thread_id')
    if not isinstance(thread, str) or not thread or len(thread) > 512:
        raise AriaError('ARIA did not return a conversation identity.', outcome_unknown=True)
    if receipt.get('thread_id') and thread != receipt['thread_id']:
        raise AriaError('ARIA returned a different conversation. The saved handle has been retained.')
    latest = ''
    for messages in (turn.get('messages'), turn.get('updated_messages')):
        if not isinstance(messages, list):
            continue
        for item in reversed(messages):
            if not isinstance(item, dict):
                continue
            message = item.get('message') if isinstance(item.get('message'), dict) else {}
            role = item.get('role') or message.get('role')
            content = item.get('content') or message.get('content')
            if role == 'assistant' and isinstance(content, str):
                latest = content
                break
        if latest:
            break
    return {**receipt, 'status': turn['state'], 'turn_id': turn['id'], 'thread_id': thread,
        'conversation_url': 'https://forge.coreweave.com/aria/threads/' + quote(thread, safe=''),
        'latest_response': latest[:120_000], 'response_truncated': len(latest) > 120_000,
        'needs_attention': bool(turn.get('permission_requests') or turn.get('agent_questions')),
        'updated_at': time.time(), 'error': None, 'last_check_error': None,
        'server_updated_at': turn.get('updated_at'),
        'billing': 'ARIA organization usage; outside the notebook inference allowance'}


def start_investigation(session, context, *, interpretation='', client=None):
    """Send at most once for these selected records. Requires an explicit UI action.

    Persist ``submitting`` before POST. If the process stops before saving the
    handle, reopening cannot silently send a second request. Server-side ARIA
    keeps working after this function returns; the notebook needs no worker.
    """
    from .aria import investigation_prompt
    current = _current_context(session, context)
    prompt = investigation_prompt(current, interpretation)
    if len(prompt.encode('utf-8')) > MAX_PROMPT_BYTES:
        raise ValueError('This ARIA question is over 32 KiB. Select fewer saved records or use the manual prompt.')
    previous = saved_investigation(session, current)
    if previous and previous.get('status') != 'rejected':
        # A changed interpretation belongs in the same native conversation,
        # rather than creating another paid turn from a double click.
        return previous
    entity, project = session.project.split('/', 1)
    parts = [{'type': 'text', 'text': prompt}, *native_context_parts(current),
        {'type': 'wandb_client', 'platform': 'agent'}]
    receipt = {'context_id': current['id'], 'workshop': session.workshop, 'workspace_id': session.workspace_id,
        'project': session.project, 'stop_id': current['stop_id'], 'record_ids': [row['identity'] for row in current['records']],
        'prompt': prompt, 'prompt_sha256': digest(prompt), 'interpretation': interpretation,
        'native_context': parts[1:-1], 'status': 'submitting', 'submitted_at': time.time(),
        'billing': 'ARIA organization usage; outside the notebook inference allowance'}
    owns_client = client is None
    client = client or AriaClient()  # Resolve authentication before any possible send.
    try:
        # Claim inside the session lock so two notebook callbacks cannot POST
        # the same context even if they both read an empty receipt above.
        with session.transaction() as state:
            old = state.get('drafts', {}).get(_key(current), {}).get('value', {})
            if old and old.get('status') != 'rejected':
                return old
            state.setdefault('drafts', {})[_key(current)] = {
                'value': receipt, 'fingerprint': digest(receipt), 'updated_at': time.time()}
        try:
            turn = client.submit({'entity': entity, 'project': project, 'user_prompt': parts})
            receipt = _snapshot(turn, receipt)
        except AriaError as error:
            receipt.update(status='outcome_unknown' if error.outcome_unknown else 'rejected',
                error=str(error), http_status=error.status, updated_at=time.time())
        session.save_draft(_key(current), receipt)
        if receipt.get('thread_id'):
            # Naming is a separate request after the durable handle is saved.
            # Failure here must never hide a successfully created turn.
            title = f"{session.workshop}: {current['title']}"
            try:
                client.name_thread(receipt['thread_id'], title)
                receipt['title'] = title[:255]
            except AriaError:
                receipt['title_status'] = 'unavailable; open the saved conversation'
            session.save_draft(_key(current), receipt)
        return receipt
    finally:
        if owns_client:
            client.close()


def check_investigation(session, context, *, client=None):
    """One read-only status request for the existing turn; never creates a turn."""
    _current_context(session, context)
    receipt = saved_investigation(session, context)
    if not receipt.get('turn_id'):
        return receipt
    if receipt.get('status') in TERMINAL and (receipt.get('latest_response') or receipt.get('status') != 'completed'):
        return receipt
    owns_client = client is None
    client = client or AriaClient()
    try:
        try:
            receipt = _snapshot(client.get(receipt['turn_id']), receipt)
        except AriaError as error:
            receipt.update(last_check_error=str(error), checked_at=time.time())
        session.save_draft(_key(context), receipt)
        return receipt
    finally:
        if owns_client:
            client.close()
