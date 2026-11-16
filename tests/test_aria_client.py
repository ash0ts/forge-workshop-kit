import json

import httpx
import pytest

from forge_workshop_kit import WorkshopSession, aria
from forge_workshop_kit import aria_client as direct


def selected(tmp_path):
    session = WorkshopSession('learner/research', 'banking-routing', state_dir=tmp_path)
    with session.stage('routing/baseline/tfidf', inputs={'split': 'validation'}) as stage:
        stage.record({'metrics': {'macro_f1': .8}})
    with session.transaction() as state:
        state['stages'][stage.id]['published'] = 'https://wandb.ai/learner/research/runs/' + stage.id
        state['publications']['trace/' + stage.id] = {
            'verified': True, 'url': 'https://forge.coreweave.com/agent-lens/learner/research/conversations/discovery-1'}
    return session, aria.build_aria_context(session, 'investigate')


def turn(state='queued', **kwargs):
    return {'id': 'turn-1', 'thread_id': 'thread-1', 'state': state,
            'wandb_entity': 'learner', 'wandb_project': 'research', **kwargs}


def client(handler):
    return direct.AriaClient(api_key='TEST_SECRET_NEVER_SAVED', transport=httpx.MockTransport(
        lambda request: httpx.Response(200, json={'id': 'thread-1'}) if request.method == 'PATCH' else handler(request)))


def test_explicit_send_is_native_scoped_and_saved_before_post(tmp_path):
    session, context = selected(tmp_path)
    calls = []
    def handler(request):
        calls.append(request)
        receipt = direct.saved_investigation(session, context)
        assert receipt['status'] == 'submitting'
        payload = json.loads(request.content)
        assert payload['entity'] == 'learner' and payload['project'] == 'research'
        assert [item['type'] for item in payload['user_prompt']] == ['text', 'wandb_run', 'wandb_conversation', 'wandb_client']
        assert 'Do not inspect reserved evaluation results' in payload['user_prompt'][0]['text']
        return httpx.Response(202, json=turn())
    api = client(handler)
    receipt = direct.start_investigation(session, context, interpretation='Check the wording.', client=api)
    assert receipt['conversation_url'] == 'https://forge.coreweave.com/aria/threads/thread-1'
    assert receipt['status'] == 'queued'
    assert 'TEST_SECRET' not in json.dumps(session.read())
    assert direct.start_investigation(session, context, interpretation='Edited hypothesis', client=api) == receipt
    assert len(calls) == 1


def test_restoration_and_check_reuse_same_turn(tmp_path):
    session, context = selected(tmp_path)
    calls = []
    def handler(request):
        calls.append(request.method)
        return httpx.Response(202 if request.method == 'POST' else 200, json=turn(
            'queued' if request.method == 'POST' else 'completed',
            messages=[{'message': {'role': 'assistant', 'content': 'Inspect the saved prediction.'}}]))
    api = client(handler)
    direct.start_investigation(session, context, client=api)
    reopened = WorkshopSession('learner/research', 'banking-routing', state_dir=tmp_path)
    assert direct.saved_investigation(reopened, context)['status'] == 'queued'
    receipt = direct.check_investigation(reopened, context, client=api)
    assert receipt['status'] == 'completed'
    assert receipt['latest_response'] == 'Inspect the saved prediction.'
    direct.check_investigation(reopened, context, client=api)
    assert calls == ['POST', 'GET']


@pytest.mark.parametrize('failure', ['timeout', '500', 'invalid', 'scope'])
def test_uncertain_submission_cannot_resend(tmp_path, failure):
    session, context = selected(tmp_path)
    calls = []
    def handler(request):
        calls.append(request.method)
        if failure == 'timeout':
            raise httpx.ReadTimeout('TEST_SECRET_NEVER_SAVED', request=request)
        if failure == 'invalid':
            return httpx.Response(202, text='invalid JSON TEST_SECRET_NEVER_SAVED')
        if failure == 'scope':
            return httpx.Response(202, json=turn(wandb_project='other'))
        return httpx.Response(500, text='TEST_SECRET_NEVER_SAVED')
    api = client(handler)
    result = direct.start_investigation(session, context, client=api)
    assert result['status'] == 'outcome_unknown'
    direct.start_investigation(session, context, client=api)
    direct.check_investigation(session, context, client=api)
    assert calls == ['POST']
    assert 'TEST_SECRET' not in json.dumps(session.read())


def test_interrupted_save_blocks_duplicate_and_known_auth_failure_can_retry(tmp_path):
    session, context = selected(tmp_path)
    calls = []
    def handler(request):
        calls.append(request.method)
        return httpx.Response(401, json={'detail': 'expired'}) if len(calls) == 1 else httpx.Response(202, json=turn())
    api = client(handler)
    assert direct.start_investigation(session, context, client=api)['status'] == 'rejected'
    assert direct.start_investigation(session, context, client=api)['status'] == 'queued'
    assert len(calls) == 2
    session.save_draft(direct._key(context), {'status': 'submitting'})
    assert direct.start_investigation(session, context, client=api)['status'] == 'submitting'
    assert len(calls) == 2


def test_poll_failure_preserves_handle_and_partial_answer_is_not_complete(tmp_path):
    session, context = selected(tmp_path)
    calls = []
    def handler(request):
        calls.append(request.method)
        if len(calls) == 2:
            return httpx.Response(503)
        return httpx.Response(202, json=turn('in_progress', messages=[{'role': 'assistant', 'content': 'First observation'}]))
    api = client(handler)
    direct.start_investigation(session, context, client=api)
    result = direct.check_investigation(session, context, client=api)
    assert result['status'] == 'in_progress' and result['turn_id'] == 'turn-1'
    assert result['latest_response'] == 'First observation' and result['last_check_error']
    direct.check_investigation(session, context, client=api)
    assert calls == ['POST', 'GET', 'GET']


def test_selection_and_rendering_never_contact_services(tmp_path, monkeypatch):
    import marimo as mo
    session, context = selected(tmp_path)
    monkeypatch.setattr(direct, 'AriaClient', lambda **kw: pytest.fail('Rendering contacted ARIA'))
    before = session.read()
    card = aria.investigation(mo, session, 'investigate')
    assert 'Start ARIA investigation' in card.text
    assert 'Check ARIA response' in card.text
    assert session.read() == before
    assert direct.saved_investigation(session, context) == {}


def test_changed_evidence_cannot_send_old_context(tmp_path):
    session, context = selected(tmp_path)
    with session.transaction() as state:
        state['stages'][context['records'][0]['identity']]['result']['metrics']['macro_f1'] = .1
    with pytest.raises(ValueError, match='completed evidence'):
        direct.start_investigation(session, context, client=client(lambda request: pytest.fail('sent')))


def test_native_context_does_not_attach_broad_artifact_collection(tmp_path):
    _, context = selected(tmp_path)
    context['records'][0]['links'].append({'label': 'Saved files', 'url': 'https://wandb.ai/learner/research/artifacts/models/version/v3'})
    assert len(direct.native_context_parts(context)) == 2


def test_current_service_message_envelope_uses_normalized_fields(tmp_path):
    session, context = selected(tmp_path)
    api = client(lambda request: httpx.Response(202, json=turn('completed', messages=[{
        'role': 'assistant', 'content': 'This decision abstained.',
        'message': {'type': 'agent_message', 'text': 'opaque driver-specific content'}}])))
    receipt = direct.start_investigation(session, context, client=api)
    assert receipt['latest_response'] == 'This decision abstained.'


def test_card_callback_sends_once_and_returns_same_conversation(tmp_path, monkeypatch):
    import marimo as mo
    session, context = selected(tmp_path)
    calls = []
    api = client(lambda request: calls.append(request.method) or httpx.Response(202, json=turn()))
    monkeypatch.setattr(direct, 'AriaClient', lambda: api)
    card = aria.investigation(mo, session, 'investigate')
    # Invoke the bound form callback, as marimo does after an explicit submit.
    start = card._elements['start']
    start._on_change('The destination needs checking.')
    start._on_change('A second click must reuse the turn.')
    assert calls == ['POST']
    assert direct.saved_investigation(session, context)['turn_id'] == 'turn-1'
    assert 'Open ARIA conversation' in aria.response(mo, card).text


def test_non_cloud_authentication_is_not_forwarded(monkeypatch):
    monkeypatch.setenv('WANDB_BASE_URL', 'https://private.example.test')
    with pytest.raises(PermissionError, match='Multi-tenant Cloud'):
        direct.AriaClient(api_key='DO_NOT_SEND')


def test_saved_login_is_resolved_for_cloud_and_redirects_are_not_followed(monkeypatch):
    import wandb
    monkeypatch.delenv('WANDB_BASE_URL', raising=False)
    monkeypatch.delenv('WANDB_API_KEY', raising=False)
    seen = []
    class CloudLogin:
        api_key = 'CLOUD_TEST_KEY'
    monkeypatch.setattr(wandb, 'Api', lambda *, overrides: seen.append(overrides) or CloudLogin())
    requests = []
    def handler(request):
        requests.append(request)
        return httpx.Response(307, headers={'location': 'https://elsewhere.example.test'})
    api = direct.AriaClient(transport=httpx.MockTransport(handler))
    with pytest.raises(direct.AriaError) as error:
        api.submit({'entity': 'learner', 'project': 'research', 'user_prompt': []})
    assert seen == [{'base_url': 'https://api.wandb.ai'}]
    assert len(requests) == 1
    assert requests[0].url.host == 'wb-agent.wandb.ai'
    assert error.value.outcome_unknown
    api.close()


@pytest.mark.parametrize('status', [408, 409])
def test_http_timeout_or_conflict_does_not_allow_another_send(tmp_path, status):
    session, context = selected(tmp_path)
    calls = []
    api = client(lambda request: calls.append(request.method) or httpx.Response(status))
    receipt = direct.start_investigation(session, context, client=api)
    assert receipt['status'] == 'outcome_unknown'
    direct.start_investigation(session, context, client=api)
    assert calls == ['POST']


def test_poll_cannot_switch_to_another_conversation(tmp_path):
    session, context = selected(tmp_path)
    api = client(lambda request: httpx.Response(200, json=turn(
        thread_id='other-thread' if request.method == 'GET' else 'thread-1')))
    direct.start_investigation(session, context, client=api)
    receipt = direct.check_investigation(session, context, client=api)
    assert receipt['thread_id'] == 'thread-1'
    assert receipt['conversation_url'].endswith('/thread-1')
    assert 'different conversation' in receipt['last_check_error']


def test_unfamiliar_message_envelope_keeps_the_valid_handle(tmp_path):
    session, context = selected(tmp_path)
    api = client(lambda request: httpx.Response(202, json=turn('completed', messages=[
        None, 'unrecognized envelope', {'message': ['opaque content']}])))
    receipt = direct.start_investigation(session, context, client=api)
    assert receipt['turn_id'] == 'turn-1'
    assert receipt['status'] == 'completed'
    assert receipt['latest_response'] == ''
