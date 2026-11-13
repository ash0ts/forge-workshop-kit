import json

import httpx
import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.provider import MODEL, Provider, ProviderStop
from forge_workshop_kit.session import StageNeedsReview


def test_hosted_rename_keeps_identity_and_another_copy_is_isolated(tmp_path, monkeypatch):
    monkeypatch.setenv('WANDB_ENTITY', 'attendee')
    monkeypatch.setenv('WANDB_PROJECT', 'lab')
    monkeypatch.setenv('WORKSHOP_PROJECT', 'host/old-workshop')
    monkeypatch.setenv('WANDB_NOTEBOOK_ANCHOR_RUN', 'notebook-123')
    monkeypatch.setenv('WANDB_NOTEBOOK_COLLECTION', 'Copy of Solar')
    first = WorkshopSession.from_environment('solar', state_dir=tmp_path / 'before')
    monkeypatch.setenv('WANDB_NOTEBOOK_COLLECTION', 'My forecast')
    restarted = WorkshopSession.from_environment('solar', state_dir=tmp_path / 'after')
    assert first.project == 'attendee/lab'
    assert first.identity == restarted.identity
    monkeypatch.setenv('WANDB_NOTEBOOK_ANCHOR_RUN', 'notebook-456')
    copied = WorkshopSession.from_environment('solar', state_dir=tmp_path / 'copy')
    assert copied.workspace_id != first.workspace_id


def test_explicit_retry_runs_only_failed_sibling(tmp_path):
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    calls = []

    def run(name, fail=False):
        with session.stage(name) as stage:
            if stage.needs_run:
                calls.append(name)
                if fail:
                    raise ConnectionError('Access expired')
                stage.record({'passed': True})
            return stage.result

    run('case-a')
    with pytest.raises(ConnectionError):
        run('case-b', fail=True)
    failed = session.recovery_options()[0]
    with pytest.raises(StageNeedsReview):
        run('case-b')
    session.retry_stage(failed['id'])
    assert calls == ['case-a', 'case-b']  # Authorization does not execute.
    run('case-a')
    run('case-b')
    run('case-b')
    assert calls == ['case-a', 'case-b', 'case-b']
    assert len(session.completed()) == 2
    assert not session.recovery_options()


def test_uncertain_request_requires_confirmation_and_stays_charged(tmp_path):
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    with pytest.raises(ConnectionError):
        with session.stage('model') as stage:
            with session.transaction() as state:
                state['requests'][stage.id + '/0'] = {'status': 'pending', 'reserved_usd': .01}
            raise ConnectionError('Connection lost')
    with pytest.raises(StageNeedsReview, match='Confirm'):
        session.retry_stage(stage.id)
    session.retry_stage(stage.id, confirm_stopped=True)
    assert Provider(session).summary()['bounded_unknown_usd'] == .01


def test_post_execution_error_does_not_erase_completed_work(tmp_path):
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    with pytest.raises(ConnectionError):
        with session.stage('model') as stage:
            stage.record({'answer': 42})
            raise ConnectionError('Export unavailable')
    with session.stage('model') as cached:
        assert not cached.needs_run
        assert cached.result == {'answer': 42}
    assert session.read()['stages'][stage.id]['post_execution_errors']


def successful_response():
    return {'model': MODEL, 'choices': [{'message': {'content': '{}'}}],
            'usage': {'prompt_tokens': 10, 'completion_tokens': 2}}


def test_failed_transport_then_success_is_cached_and_changed_payload_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.provider.credentials', lambda: 'fake')
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    calls = []

    def transport(request):
        calls.append(json.loads(request.content))
        return httpx.Response(500, json={'error': 'temporary'}) if len(calls) == 1 else httpx.Response(200, json=successful_response())

    provider = Provider(session, transport=httpx.MockTransport(transport), sleeper=lambda _: None)
    result = provider.complete('request', [{'role': 'user', 'content': 'first'}])
    assert provider.complete('request', [{'role': 'user', 'content': 'first'}]) == result
    assert len(calls) == 2
    with pytest.raises(ProviderStop, match='different inputs'):
        provider.complete('request', [{'role': 'user', 'content': 'changed'}])
    assert len(calls) == 2


@pytest.mark.parametrize('fail_at', [1, 2])
def test_request_ledger_outage_before_or_after_transport(tmp_path, monkeypatch, fail_at):
    monkeypatch.setattr('forge_workshop_kit.provider.credentials', lambda: 'fake')

    class Publisher:
        calls = 0

        def publish_request_ledger(self):
            self.calls += 1
            if self.calls == fail_at:
                raise ConnectionError('Artifact unavailable')
            return 'test/ledger:v1'

    publisher = Publisher()
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path,
                              notebook_identity='copy', publisher=publisher)
    calls = []

    def transport(request):
        calls.append(request)
        return httpx.Response(200, json=successful_response())

    provider = Provider(session, transport=httpx.MockTransport(transport))
    if fail_at == 1:
        with pytest.raises(ProviderStop, match='No request was sent'):
            provider.complete('request', [])
        assert not calls
        assert session.read()['requests']['request/0']['status'] == 'reserved'
    result = provider.complete('request', [])
    assert result['status'] == 'complete'
    assert provider.complete('request', []) == result
    assert len(calls) == 1


def test_help_does_not_wait_for_result_or_checkpoint_uploads(tmp_path):
    class Publisher:
        def publish_progress(self):
            return 'https://example.test/progress'

        def publish_checkpoint(self):
            pytest.fail('Help must not publish a checkpoint')

        def publish_stages(self):
            pytest.fail('Help must not publish outputs')

    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path, publisher=Publisher())
    assert session.request_help('Stuck on my tool')['status'] == 'published'


def test_timeout_is_not_automatically_reissued(tmp_path, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.provider.credentials', lambda: 'fake')
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    calls = []
    def transport(request):
        calls.append(request)
        raise httpx.ReadTimeout('Response lost after sending')
    provider = Provider(session, transport=httpx.MockTransport(transport), sleeper=lambda _: None)
    with pytest.raises(ProviderStop, match='No automatic retry'):
        with session.stage('model') as stage:
            provider.complete(stage.id, [])
    assert len(calls) == 1
    row = session.read()['requests'][stage.id + '/0']
    assert row['status'] == 'interrupted'
    assert row['unknown_usd'] == row['reserved_usd']
    assert session.recovery_options()[0]['has_uncertain_requests']
    with pytest.raises(ProviderStop, match='uncertain'):
        provider.complete(stage.id, [])
    with pytest.raises(StageNeedsReview, match='Confirm'):
        session.retry_stage(stage.id)
    assert len(calls) == 1


def test_missing_authentication_never_reserves_or_sends(tmp_path, monkeypatch):
    def missing():
        raise PermissionError('Sign in first')
    monkeypatch.setattr('forge_workshop_kit.provider.credentials', missing)
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    provider = Provider(session, transport=httpx.MockTransport(lambda _: pytest.fail('No request should be sent')))
    with pytest.raises(PermissionError, match='Sign in'):
        provider.complete('request', [])
    assert not session.read()['requests']


def test_completed_attempt_wins_over_stale_retry_route(tmp_path):
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    with pytest.raises(ValueError):
        with session.stage('case') as first:
            raise ValueError('Interrupted local check')
    session.retry_stage(first.id)
    # A separately resumed original attempt completes before the retry is run.
    with session.transaction() as state:
        state['stages'][first.id].update(status='complete', result={'answer': 42})
    with session.stage('case') as saved:
        assert not saved.needs_run
        assert saved.result == {'answer': 42}


def test_stage_does_not_wait_for_monitor_and_updates_are_coalesced(tmp_path):
    import threading
    entered, release = threading.Event(), threading.Event()
    class Publisher:
        calls = 0
        def publish_progress(self):
            self.calls += 1
            entered.set()
            assert release.wait(3)
    publisher = Publisher()
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path, publisher=publisher)
    with session.stage('first') as stage:
        assert entered.wait(1)
        stage.record({'done': True})
    with session.stage('second') as stage:
        stage.record({'done': True})
    assert len(session.completed()) == 2
    worker = session._progress_thread
    release.set()
    worker.join(3)
    assert not worker.is_alive()
    assert publisher.calls == 2  # First write plus the newest state; no update backlog.
