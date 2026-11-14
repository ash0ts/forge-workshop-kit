"""The release drill changes a loader, never the trained classifier or held-out results."""
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

import joblib
import numpy as np
import pytest

from forge_workshop_kit import WorkshopSession, routing, routing_release as lab
from forge_workshop_kit.routing_teaching import completed_steps, saved


def data_fixture():
    rows, vectors = [], []
    for split, count in [('train', 8), ('review', 3), ('test', 2)]:
        for label, vector in [('card_arrival', [1., 0.]), ('card_not_working', [0., 1.])]:
            for n in range(count):
                rows.append({'id': f'{split}/{label}/{n}', 'text': label+f' request {n}', 'label': label, 'split': split})
                vectors.append(vector)
    return {'rows': rows, 'features': np.asarray(vectors), 'manifest': {'dataset': 'public-practice', 'encoder_revision': 'test-features'}}


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path/'state')
    data = data_fixture()
    fitted = routing.fit_classifier(data, 'embedding')
    with session.stage('routing/baseline/embedding', sources={'classifier.py': 'def make_classifier():\n    return "public test"\n'}) as model:
        path = model.output_dir/'classifier.joblib'
        joblib.dump(fitted, path)
        model.record({'model_file': str(path.relative_to(session.root)), 'model_sha256': routing.checksum(path)}, files=[path])
    with session.stage('routing/freeze') as freeze:
        freeze.record({'selected_stage': model.id, 'threshold': .5, 'model_sha256': model.result['model_sha256'],
                       'policy_source': 'def needs_review(confidence, threshold):\n    return confidence < threshold\n'})
    with session.stage('routing/final/selected') as final:
        final.record({'predictions': routing.predict(fitted, data, 'test')})
    original_final = session.read()['stages'][final.id]
    registry = {}
    publications = []
    def publish(session, record):
        artifact = 'test/routing/'+record['id']+':v0'
        if artifact not in registry:
            registry[artifact] = session.file(record['result']['bundle_directory'])
            publications.append(artifact)
        return {'artifact': artifact, 'url': 'https://example.test/'+record['id'], 'stage': record['id']}
    class API:
        def artifact(self, identity):
            def download(root):
                shutil.copytree(registry[identity], root, dirs_exist_ok=True)
                return str(root)
            return SimpleNamespace(download=download)
    monkeypatch.setattr(lab, 'publish_bundle', publish)
    return session, data, API(), original_final, publications


def test_cohort_freezes_review_cases_without_scores_and_is_order_independent():
    data = data_fixture()
    selected = lab.cohort(data)
    reversed_data = {**data, 'rows': list(reversed(data['rows']))}
    assert lab.cohort(reversed_data) == selected
    assert all(row['split'] == 'review' and row['id'].endswith('/0') for row in selected)
    assert len(selected) == 2
    assert not any('prediction' in row for row in selected)


def test_free_checks_require_both_order_and_membership():
    assert lab.check_exercises(lab.LOADER_SOLUTION, lab.CHECK_SOLUTION)['status'] == 'complete'
    with pytest.raises(NotImplementedError):
        lab.check_exercises(lab.LOADER_STARTER, lab.CHECK_SOLUTION)
    with pytest.raises(AssertionError):
        lab.check_exercises(lab.FAULTY_LOADER, lab.CHECK_SOLUTION)
    with pytest.raises(AssertionError):
        lab.check_exercises('def label_names(model_classes):\n    return sorted(model_classes)', lab.CHECK_SOLUTION)
    with pytest.raises(AssertionError):
        lab.check_exercises(lab.LOADER_SOLUTION, 'def check_release(model_classes, loaded_labels):\n    return {"label_set": True, "label_order": True}')


def test_complete_drill_reproduces_repairs_and_rolls_back(prepared, monkeypatch):
    session, data, api, final, publications = prepared
    bundle = lab.prepare(session, data)
    assert 'release' not in completed_steps(session)
    assert bundle['result']['metadata']['model_stage']
    selected = saved(session, 'routing/release/cohort')
    assert selected['ended_at'] <= bundle['started_at']
    healthy = lab.reproduce_selected(session, data, api=api)
    # Every capstone operation uses only the already fitted artifact.
    monkeypatch.setattr(routing, 'fit_classifier', lambda *a, **kw: pytest.fail('Capstone trained a model.'))
    faulty = lab.run_variant(session, data, variant='incident')
    repaired = lab.run_variant(session, data, variant='repair', loader_source=lab.LOADER_SOLUTION, check_source=lab.CHECK_SOLUTION)
    assert healthy['result']['metrics']['accuracy'] == 1
    assert faulty['result']['metrics']['accuracy'] == 0
    assert faulty['result']['checks'] == {'label_set': True, 'label_order': False, 'prediction_parity': False}
    assert all(repaired['result']['checks'].values())
    assert [r['confidence'] for r in faulty['result']['predictions']] == [r['confidence'] for r in healthy['result']['predictions']]
    release = lab.decide(session, decision='release', reason='Checks preserve the model label columns.')
    assert 'release' not in completed_steps(session)
    assert release['previous'] == healthy['result']['artifact']
    restored = lab.rollback(session, data, api=api)
    assert restored['result']['release']['decision'] == 'rollback'
    assert restored['result']['checks']['prediction_parity']
    assert 'release' in completed_steps(session)
    assert session.read()['stages'][final['id']] == final
    assert session.read()['requests'] == {}
    # A restart reuses completed stages; it does not predict or publish again.
    restarted = WorkshopSession('test/routing', 'banking-routing', state_dir=session.root)
    monkeypatch.setattr(lab, 'batch', lambda *a: pytest.fail('Completed prediction repeated.'))
    assert lab.reproduce_selected(restarted, data, api=api)['id'] == healthy['id']
    assert lab.run_variant(restarted, data, variant='repair', loader_source=lab.LOADER_SOLUTION, check_source=lab.CHECK_SOLUTION)['id'] == repaired['id']
    assert lab.rollback(restarted, data, api=api)['id'] == restored['id']
    assert len(publications) == 2


def test_changed_release_files_or_dataset_are_rejected(prepared):
    session, data, api, _, _ = prepared
    bundle = lab.prepare(session, data)
    healthy = lab.reproduce_selected(session, data, api=api)
    root = session.file(healthy['result']['bundle_directory'])
    with pytest.raises(ValueError, match='preprocessing'):
        lab.batch(root, {**data, 'manifest': {'changed': True}}, lab.cohort(data))
    (root/'loader.py').write_text(lab.FAULTY_LOADER)
    with pytest.raises(ValueError, match='checksum'):
        lab.load_bundle(root)
    cases = lab.cohort(data)
    cases[0] = {**cases[0], 'split': 'test'}
    with pytest.raises(ValueError, match='review cases'):
        lab.batch(session.file(bundle['result']['bundle_directory']), data, cases)


def test_changed_installed_runtime_blocks_new_predictions_but_keeps_saved_batches(prepared, monkeypatch, tmp_path):
    session, data, api, _, _ = prepared
    lab.prepare(session, data)
    healthy = lab.reproduce_selected(session, data, api=api)
    changed_runtime = tmp_path/'changed_runtime.py'
    changed_runtime.write_text('# a different predictor implementation\n', encoding='utf-8')
    monkeypatch.setattr(routing, '__file__', str(changed_runtime))
    with pytest.raises(ValueError, match='prediction code differs.*Install forge-workshop-kit=='):
        lab.batch(session.file(healthy['result']['bundle_directory']), data, lab.cohort(data))
    assert lab.reproduce_selected(session, data, api=api)['id'] == healthy['id']


def test_reject_preserves_previous_release(prepared):
    session, data, api, _, _ = prepared
    lab.prepare(session, data)
    lab.reproduce_selected(session, data, api=api)
    lab.run_variant(session, data, variant='incident')
    lab.run_variant(session, data, variant='repair', loader_source=lab.LOADER_SOLUTION, check_source=lab.CHECK_SOLUTION)
    decision = lab.decide(session, decision='reject', reason='Keep the existing release for this exercise.')
    assert decision['decision'] == 'reject'
    assert 'release' in completed_steps(session)
    with pytest.raises(ValueError, match='Release the tested repair'):
        lab.rollback(session, data, api=api)
    assert 'earlier release remains' in saved(session, 'routing/release/decision')['result']['next']


def test_false_rollback_parity_never_records_success(prepared, monkeypatch):
    session, data, api, _, _ = prepared
    lab.prepare(session, data)
    lab.reproduce_selected(session, data, api=api)
    lab.run_variant(session, data, variant='incident')
    lab.run_variant(session, data, variant='repair', loader_source=lab.LOADER_SOLUTION, check_source=lab.CHECK_SOLUTION)
    lab.decide(session, decision='release', reason='Check the repaired loader.')
    monkeypatch.setattr(lab, 'prediction_parity', lambda *a: False)
    with pytest.raises(ValueError, match='checks'):
        lab.rollback(session, data, api=api)
    assert saved(session, 'routing/release/rollback') is None
    assert 'Rollback reloaded' not in lab.report_text(session)


def test_completed_upload_survives_run_close_failure(tmp_path, monkeypatch):
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path/'state')
    root = tmp_path/'bundle'; root.mkdir()
    (root/'release.json').write_text('{}')
    record = {'id': 'teststage', 'name': 'routing/release/prepare', 'result': {'bundle_directory': 'bundle', 'metadata': {'controlled_drill': False}}}
    calls = []
    logged = SimpleNamespace(qualified_name='test/routing/router:v0', url='https://example.test/artifact')
    class Run:
        url = 'https://example.test/run'
        def __enter__(self): return self
        def log_artifact(self, artifact): calls.append(artifact); return SimpleNamespace(wait=lambda **kw: logged)
        def __exit__(self, *args): raise RuntimeError('Finish failed after upload')
    import wandb
    monkeypatch.setattr(wandb, 'Artifact', lambda *a, **kw: SimpleNamespace(add_file=lambda *a, **kw: None))
    monkeypatch.setattr(lab, '_directory', lambda *a: root)
    monkeypatch.setattr(lab, 'load_bundle', lambda *a: ({}, {}))
    monkeypatch.setattr(session, 'connect', lambda: SimpleNamespace(run=lambda *a, **kw: Run()))
    with pytest.raises(RuntimeError, match='Finish'):
        lab.publish_bundle(session, record)
    receipt = lab.publish_bundle(session, record)
    assert receipt['artifact'].endswith(':v0') and len(calls) == 1


def test_comparison_rows_keep_identity_when_later_exports_add_links(prepared):
    session, data, api, _, _ = prepared
    lab.prepare(session, data)
    healthy = lab.reproduce_selected(session, data, api=api)
    first = lab.comparison_rows(session, healthy)
    assert first[0]['evidence']['agent_lens'] is None
    assert first[0]['evidence']['release_artifact'] == healthy['result']['artifact']
    with session.transaction() as state:
        state['publications']['trace/'+healthy['id']] = {'verified': True, 'url': 'https://example.test/native-trace'}
        state['stages'][healthy['id']]['artifact_url'] = 'https://example.test/saved-execution'
    restarted = WorkshopSession('test/routing', 'banking-routing', state_dir=session.root)
    assert lab.comparison_rows(restarted, healthy) == first
    links = lab.evidence_links(restarted)
    assert links['healthy release batch in Agent Lens'] == 'https://example.test/native-trace'
    assert links['healthy saved batch and source'] == 'https://example.test/saved-execution'
    assert restarted.read()['requests'] == {}


def test_refresh_does_not_subscribe_an_action_to_its_own_revision():
    """A state read inside refresh re-executes a still-true run button in marimo."""
    import ast
    import sys
    sys.path.insert(0, str(Path(__file__).parents[1]/'scripts'))
    from routing_cells import cells
    helper = next(cell for cell in cells if 'def refresh():' in cell.code)
    definition = next(node for node in ast.parse(helper.code).body if isinstance(node, ast.FunctionDef) and node.name == 'refresh')
    values = [3]
    def read_forbidden():
        raise AssertionError('Executing refresh must not subscribe this action to revision updates.')
    def update(fn):
        values.append(fn(values[-1]))
    scope = {'get_revision': read_forbidden, 'set_revision': update}
    exec(compile(ast.Module(body=[definition], type_ignores=[]), '<refresh-check>', 'exec'), scope)
    scope['refresh']()
    assert values == [3, 4]


def test_notebook_revision_updates_never_read_the_same_state():
    """Recovery and completion can refresh displays without restarting their actions."""
    import ast
    import importlib
    import sys
    sys.path.insert(0, str(Path(__file__).parents[1]/'scripts'))
    for name in ('pending', 'solar', 'routing', 'inspection', 'transit'):
        module = importlib.import_module(name+'_cells')
        for cell in module.cells:
            for node in ast.walk(ast.parse(cell.code)):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id.startswith('set_') and 'revision' in node.func.id:
                    getter = node.func.id.replace('set_', 'get_', 1)
                    reads = [child for arg in node.args for child in ast.walk(arg) if isinstance(child, ast.Name) and child.id == getter]
                    assert not reads, f'{name} completion/recovery reads {getter} while writing it; use a functional state update.'
