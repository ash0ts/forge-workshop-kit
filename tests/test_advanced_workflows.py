"""Recovery and comparison contracts; these tests never contact paid services."""

import importlib.util
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.advanced import TrainingClient, sft_examples, sft_request
from forge_workshop_kit.advanced_comparison import (
    ComparisonStopped,
    comparison_plan,
    publish_comparison_result,
    run_comparison,
)
from forge_workshop_kit.managed_jobs import (
    SubmissionNeedsReview,
    poll_job,
    recover_job,
    submit_once,
    validate_approval,
)
from forge_workshop_kit.releases import link_registry, record_release
from forge_workshop_kit.routing import route_messages, validate_route

FORECAST = {'maximum_usd': 1., 'checked_at': '2026-11-14', 'basis': 'Frozen rates and call limits'}


@pytest.fixture
def session(tmp_path):
    return WorkshopSession('test/project', 'banking-routing', state_dir=tmp_path)


@pytest.mark.parametrize('invalid', [float('nan'), float('inf'), -1, True, None])
def test_invalid_cost_never_reaches_submit(session, invalid):
    sent = []
    with pytest.raises(ValueError):
        submit_once(session, 'job', {}, forecast=FORECAST, approved_usd=invalid,
                    submit=lambda request: sent.append(request))
    with pytest.raises(ValueError):
        validate_approval({**FORECAST, 'maximum_usd': invalid}, 1)
    assert sent == [] and session.read().get('managed_jobs', {}) == {}


def test_concurrent_submit_and_recovery_preserve_one_job(session):
    sent, barrier = [], threading.Barrier(2)

    def launch():
        barrier.wait()
        return submit_once(session, 'sft', {'model_id': 'm1'}, forecast=FORECAST,
                           approved_usd=1, submit=lambda body: (sent.append(body) or {'id': 'job-1'}))

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: launch(), range(2)))
    assert results[0] == results[1] and len(sent) == 1
    key = next(iter(session.read()['managed_jobs']))
    with pytest.raises(ValueError, match='different job ID'):
        recover_job(session, key, 'another', lookup=lambda _: {})
    with pytest.raises(ValueError, match='different job'):
        poll_job(session, key, fetch=lambda _: {'id': 'another'})
    assert session.read()['managed_jobs'][key]['job_id'] == 'job-1'


def test_ambiguous_submission_needs_matching_provider_evidence(session):
    def timeout(_):
        raise TimeoutError()
    with pytest.raises(TimeoutError):
        submit_once(session, 'sft', {'model_id': 'm1'}, forecast=FORECAST,
                    approved_usd=1, submit=timeout)
    key, saved = next(iter(session.read()['managed_jobs'].items()))
    with pytest.raises(SubmissionNeedsReview):
        submit_once(session, 'sft', {'model_id': 'm1'}, forecast=FORECAST,
                    approved_usd=1, submit=lambda _: {'id': 'duplicate'})
    with pytest.raises(ValueError, match='does not match'):
        recover_job(session, key, 'known', lookup=lambda _: {'id': 'wrong',
                    'request_fingerprint': saved['request_fingerprint']})
    recovered = recover_job(session, key, 'known', lookup=lambda _: {'id': 'known',
                            'request_fingerprint': saved['request_fingerprint']})
    assert recovered['job_id'] == 'known'


def test_sft_uses_same_prompt_and_typed_answer_and_excludes_unknown_splits():
    cases = {'c1': {'split': 'review', 'label': 'card_arrival', 'text': 'Where is my card?'}}
    reviewed = {'rows': [{'case_id': 'c1', 'split': 'review', 'verified': True,
                          'accepted_label': 'card_arrival'}]}
    example = sft_examples(reviewed, cases)[0]
    assert example['messages'][:2] == route_messages(cases['c1']['text'], ['card_arrival'])
    validate_route(json.loads(example['messages'][-1]['content']), ['card_arrival'])
    for split in ('test', 'final', None):
        with pytest.raises(ValueError, match='split'):
            sft_examples(reviewed, {'c1': {**cases['c1'], 'split': split}})
    with pytest.raises(ValueError, match='known intent'):
        sft_examples(reviewed, cases, intents=['card_not_working'])
    with pytest.raises(ValueError, match='more than once'):
        sft_examples({'rows': reviewed['rows'] * 2}, cases)


def test_training_client_preserves_project_model_and_job_identity(session, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.advanced.credentials', lambda: 'not-a-real-key')
    requests = []
    def respond(request):
        requests.append(request)
        if request.url.path.endswith('/models'):
            return httpx.Response(200, json={'id': 'model-1', 'entity': 'test',
                'project': 'project', 'base_model': 'supported/base'})
        return httpx.Response(200, json={'id': 'job-1'})
    client = TrainingClient(transport=httpx.MockTransport(respond))
    client.register_model(session, 'specialist', 'supported/base')
    request = sft_request('model-1', 'wandb-artifact:///test/project/reviewed:v0', 10)
    first = client.start_sft(session, request, forecast=FORECAST, approved_usd=1)
    assert client.start_sft(session, request, forecast=FORECAST, approved_usd=1) == first
    assert [r.url.path for r in requests] == ['/v1/preview/models', '/v1/preview/sft-training-jobs']
    assert json.loads(requests[-1].content)['config']['learning_rate'] == [5e-5, 5e-5]
    with pytest.raises(ValueError, match='participant project'):
        client.start_sft(session, {**request, 'model_id': 'someone-elses-model'},
                         forecast=FORECAST, approved_usd=1)
    with pytest.raises(ValueError, match='participant project'):
        client.start_sft(session, {**request, 'training_data_url': 'wandb-artifact:///other/p/data:v0'},
                         forecast=FORECAST, approved_usd=1)
    assert len(requests) == 2


def make_plan():
    return comparison_plan([
        {'case_id': 'test-1', 'text': 'Where is my card?', 'target': 'card_arrival', 'split': 'test'},
        {'case_id': 'test-2', 'text': 'My card was declined', 'target': 'card_not_working', 'split': 'test'},
    ], ['card_arrival', 'card_not_working'], {
        'base': {'model': 'supported/base', 'input_usd_per_million': .1, 'output_usd_per_million': .2},
        'checkpoint': {'model': 'wandb-artifact:///test/project/specialist:step2',
                       'input_usd_per_million': .1, 'output_usd_per_million': .2}})


def response(request, *, invalid=False, model=None, usage=True):
    body = json.loads(request.content)
    text = body['messages'][-1]['content']
    answer = {'intent': 'card_arrival' if 'Where' in text else 'card_not_working',
              'needs_review': False, 'reason': 'Route this request to the matching queue.'}
    value = {'id': 'response-' + text, 'model': model or body['model'],
             'choices': [{'finish_reason': 'stop', 'message': {'content': 'not JSON' if invalid else json.dumps(answer)}}]}
    if usage:
        value['usage'] = {'prompt_tokens': 20, 'completion_tokens': 30}
    return httpx.Response(200, json=value)


def test_comparison_freezes_matching_inputs_restarts_without_model_calls(session, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials', lambda: 'fake')
    plan, sent = make_plan(), []
    assert plan['calls'][0]['request']['messages'] == plan['calls'][1]['request']['messages']
    assert [c['condition'] for c in plan['calls']] == ['base', 'checkpoint', 'checkpoint', 'base']
    def send(request):
        sent.append(request)
        assert request.headers['OpenAI-Project'] == session.project
        return response(request)
    result = run_comparison(session, plan, forecast=FORECAST, approved_usd=1,
                            transport=httpx.MockTransport(send))
    second = run_comparison(session, plan, forecast=FORECAST, approved_usd=1,
                            transport=httpx.MockTransport(send))
    assert result == second and len(sent) == 4
    assert result['summaries']['checkpoint']['macro_f1'] == 1
    assert result['summaries']['base']['unavailable'] == 0
    with pytest.raises(ValueError, match='forecast'):
        run_comparison(session, plan, forecast={**FORECAST, 'maximum_usd': 0}, approved_usd=1,
                       transport=httpx.MockTransport(send))
    assert len(sent) == 4


def test_missing_outputs_stay_missing_and_missing_usage_keeps_reservation(session, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials', lambda: 'fake')
    def send(request):
        body = json.loads(request.content)
        return response(request, invalid=body['model'] == 'supported/base', usage=False)
    result = run_comparison(session, make_plan(), forecast=FORECAST, approved_usd=1,
                            transport=httpx.MockTransport(send))
    assert all(row['error'] is None for row in result['versions']['base'])
    assert result['summaries']['base']['macro_f1'] is None
    assert result['summaries']['base']['unavailable'] == 2
    assert result['summaries']['checkpoint']['observed_usd'] == 0
    assert result['summaries']['checkpoint']['bounded_unknown_usd'] > 0


@pytest.mark.parametrize('failure', ['timeout', 'model', 'usage'])
def test_comparison_stops_on_uncertain_response_model_change_or_excess_usage(session, monkeypatch, failure):
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials', lambda: 'fake')
    calls = []
    def send(request):
        calls.append(request)
        if failure == 'timeout':
            raise httpx.ReadTimeout('response lost')
        if failure == 'model':
            return response(request, model='unexpected/fallback')
        value = json.loads(response(request).content)
        value['usage']['completion_tokens'] = 10000
        return httpx.Response(200, json=value)
    with pytest.raises(ComparisonStopped):
        run_comparison(session, make_plan(), forecast=FORECAST, approved_usd=1,
                       transport=httpx.MockTransport(send))
    with pytest.raises(ComparisonStopped):
        run_comparison(session, make_plan(), forecast=FORECAST, approved_usd=1,
                       transport=httpx.MockTransport(send))
    assert len(calls) == 1


def test_publication_reuses_saved_responses_only(session, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials', lambda: 'fake')
    result = run_comparison(session, make_plan(), forecast=FORECAST, approved_usd=1,
                            transport=httpx.MockTransport(response))
    observed = []
    monkeypatch.setattr('forge_workshop_kit.traces.export_trace', lambda *args:
                        observed.append(args[-1]) or {'verified': True})
    monkeypatch.setattr('forge_workshop_kit.publication.publish_comparison',
                        lambda *args, **kwargs: {'status': 'unavailable', 'message': 'native 500'})
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials',
                        lambda: pytest.fail('Publication must not authenticate for inference'))
    links = publish_comparison_result(session, result['identity'])
    assert len(observed[0]) == 4 and links['trace']['verified']
    assert links['comparison']['status'] == 'unavailable'


def test_registry_link_survives_run_close_failure(session):
    linked = []
    class Run:
        url = 'https://example.test/run'
        def use_artifact(self, name):
            return name
        def link_artifact(self, artifact, *, target_path):
            linked.append((artifact, target_path))
            return SimpleNamespace(url='https://example.test/registry/version')
    class Publisher:
        @contextmanager
        def run(self, *args):
            yield Run()
            raise RuntimeError('run close failed after linking')
    session.publisher = Publisher()
    release = record_release(session, artifact='test/project/model:v1', evaluation='https://example.test/eval',
        decision='release', metrics={'macro_f1': .9}, checks={'frozen_threshold': True}, reason='Passed')
    with pytest.raises(RuntimeError, match='run close'):
        link_registry(session, release['id'], 'wandb-registry-Models/routing')
    recovered = link_registry(session, release['id'], 'wandb-registry-Models/routing')
    assert recovered['artifact'].endswith(':v1') and len(linked) == 1


def test_sandbox_snapshot_failure_does_not_repeat_completed_execution(session, monkeypatch):
    path = Path(__file__).resolve().parents[1] / 'examples/advanced/sandbox_candidate.py'
    spec = importlib.util.spec_from_file_location('sandbox_example', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    executions = []
    class Sandbox:
        sandbox_id = 'sandbox-1'
        @classmethod
        @contextmanager
        def run(cls, **kwargs):
            executions.append(kwargs)
            assert 'env' not in kwargs
            yield cls()
        def exec(self, command):
            return SimpleNamespace(result=lambda: SimpleNamespace(stdout='saved prediction', stderr='', returncode=0))
        def snapshot(self):
            def fail():
                raise RuntimeError('storage unavailable')
            return SimpleNamespace(result=fail)
    import sys
    monkeypatch.setitem(sys.modules, 'cwsandbox', SimpleNamespace(Sandbox=Sandbox,
        AuthStrategy=SimpleNamespace(WANDB='wandb'), FileSystemSnapshotOptions=lambda **kwargs: kwargs))
    first = module.run_candidate(session, 'print(1)', forecast=FORECAST, approved_usd=1)
    second = module.run_candidate(session, 'print(1)', forecast=FORECAST, approved_usd=1)
    assert first == second and len(executions) == 1
    assert first['stdout'] == 'saved prediction' and first['snapshot_status'] == 'unavailable'


def test_advanced_result_flows_through_real_trace_and_all_publication_adapters(session, monkeypatch):
    """Exercise row/receipt contracts rather than replacing the public adapters with stubs."""
    import hashlib
    import inspect

    import coreweave_evaluations
    import weave
    from coreweave.forge.agentlens import tracing

    import wandb
    from forge_workshop_kit import traces

    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials', lambda: 'fake')
    sent = []
    def send(request):
        sent.append(request)
        body = json.loads(request.content)
        value = json.loads(response(request, invalid=body['model'] == 'supported/base').content)
        value['id'] = hashlib.sha256(request.content).hexdigest()
        if 'wandb-artifact' in body['model']:
            value['usage'] = (['malformed provider usage retained in raw receipt']
                              if 'Where' in body['messages'][-1]['content']
                              else {'prompt_tokens': 20})
        return httpx.Response(200, json=value)
    result = run_comparison(session, make_plan(), forecast=FORECAST, approved_usd=1,
                            transport=httpx.MockTransport(send))
    # Mimic a saved result from the old output-column implementation.
    with session.transaction() as state:
        for rows in state['advanced_comparisons'][result['identity']]['result']['versions'].values():
            for row in rows:
                row['output'] = row.pop('prediction')

    scope_fields, llms, stored = [], [], []
    llm_signature = inspect.signature(tracing.LLM)
    class Scope:
        def __init__(self, **kwargs):
            self.fields = kwargs
            self.attributes = {}
            scope_fields.append(kwargs)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def set_attributes(self, fields):
            self.attributes.update(fields)
        def record_error(self, error):
            self.error = str(error)
    class LLM(Scope):
        def __init__(self, **kwargs):
            llm_signature.bind(**kwargs)
            super().__init__(**kwargs)
            self.usage = None
            llms.append(self)
        def __exit__(self, *args):
            stored.append({'operation_name': 'chat', 'response_id': self.fields['response_id'],
                'request_model': self.fields['model'],
                'input_tokens': self.usage.input_tokens if self.usage else None,
                'output_tokens': self.usage.output_tokens if self.usage else None})
            return False
    monkeypatch.setattr(tracing, 'init', lambda *args, **kwargs: SimpleNamespace(force_flush=lambda: True))
    monkeypatch.setattr(tracing, 'Conversation', Scope)
    monkeypatch.setattr(tracing, 'Turn', Scope)
    monkeypatch.setattr(tracing, 'LLM', LLM)
    monkeypatch.setattr(traces, 'stored_spans', lambda *args, **kwargs:
                        [{'operation_name': 'turn'}, *stored])

    logged, native_rows, weave_scores = [], [], []
    class Run:
        entity, project = 'test', 'project'
        def __init__(self, identity):
            self.id, self.url, self.summary = identity, 'https://example.test/run/' + identity, {}
        def log(self, value):
            logged.append(value)
    class Publisher:
        @contextmanager
        def run(self, identity, *args):
            yield Run(identity)
    session.publisher = Publisher()
    monkeypatch.setattr(wandb, 'Api', lambda: SimpleNamespace(_service_api=SimpleNamespace(
        execute_graphql=lambda *args: {'project': {'internalId': 'project-internal-id'}})))
    monkeypatch.setattr('forge_workshop_kit.publication.credentials', lambda: 'fake')

    class Dataset:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    class Evaluation:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.evaluate = SimpleNamespace(call=self.evaluate_call)
        async def evaluate_call(self, evaluation, predictor):
            for row in self.dataset.rows:
                prediction = predictor(row['case_id'])
                assert prediction == row['prediction']
                weave_scores.append(self.scorers[0](row['case_id'], prediction))
            return {}, SimpleNamespace(id='weave-' + self.name)
    monkeypatch.setattr(weave, 'Dataset', Dataset)
    monkeypatch.setattr(weave, 'Evaluation', Evaluation)
    monkeypatch.setattr(weave, 'op', lambda: lambda function: function)
    monkeypatch.setattr(weave, 'init', lambda *args: None)
    monkeypatch.setattr(weave, 'publish', lambda value, **kwargs:
                        SimpleNamespace(uri=lambda: 'weave:///test/project/' + value.name))
    monkeypatch.setattr(weave, 'get_client', lambda: SimpleNamespace(flush=lambda: None,
                        get_call=lambda identity: SimpleNamespace(ended_at='finished', exception=None)))

    class NativeClient:
        def __init__(self, **kwargs):
            assert kwargs['scope_id'] == 'project-internal-id'
            self.eval_tables = SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(evaluation_id='eval-id', dataset_id='dataset-id'),
                columns=SimpleNamespace(create=lambda *args, **kwargs: None),
                rows=SimpleNamespace(add=lambda *args, **kwargs: native_rows.extend(kwargs['rows'])),
                versions=SimpleNamespace(create=lambda *args, **kwargs:
                    SimpleNamespace(evaluation_version_id='ev1', dataset_version_id='dv1')))
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
    monkeypatch.setattr(coreweave_evaluations, 'Client', NativeClient)
    monkeypatch.setattr('forge_workshop_kit.advanced_comparison.credentials',
                        lambda: pytest.fail('Publication must not run inference'))

    links = publish_comparison_result(session, result['identity'])
    assert links['trace']['verified'] and links['trace']['stored_spans'] == 5
    assert all(record['wandb_status'] == record['weave_status'] == record['native_status']
               == 'published' for record in links['comparison'].values())
    tables = [item['comparison'] for item in logged if 'comparison' in item]
    assert len(tables) == 2 and tables[0].columns[2] == 'prediction'
    assert tables[0].data[0][2] is None
    assert tables[1].data[0][2]['intent'] == 'card_arrival'
    assert len(native_rows) == 4 and native_rows[0]['output']['prediction'] is None
    assert native_rows[2]['output']['prediction']['intent'] == 'card_arrival'
    assert [row['error'] for row in weave_scores] == [None, None, 0, 0]
    assert len(llms) == 4 and len(sent) == 4
    assert [llm.attributes['workshop.usage_available'] for llm in llms] == [True, False, False, True]
    assert all(llm.fields['started_at'] <= llm.fields['ended_at'] for llm in llms)
    for llm in llms:
        assert llm.fields['model'] == llm.fields['response_model']
    publish_comparison_result(session, result['identity'])
    assert len(logged) == 4 and len(native_rows) == 4 and len(llms) == 4 and len(sent) == 4
