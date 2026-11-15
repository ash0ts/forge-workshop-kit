"""The current authored buttons preserve saved comparisons while teaching one run at a time."""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import joblib
import numpy as np
import pytest

from forge_workshop_kit import WorkshopSession, inspection, inspection_teaching, routing, routing_teaching
from forge_workshop_kit.authoring import bind_cells
from forge_workshop_kit.traces import event

ROOT = Path(__file__).resolve().parents[1]


def authored(name):
    sys.path.insert(0, str(ROOT / 'scripts'))
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '_cells.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return bind_cells({'routing': 'request_routing', 'inspection': 'visual_inspection'}[name], module.cells)


def run_cell(cells, identity, scope):
    cell = next(cell for cell in cells if cell.cell_id == identity)
    exec(compile(cell.code, identity, 'exec'), scope)


def stop(value, *_):
    assert not value, 'Test invoked a blocked action.'


def routing_fixture(root):
    rows, features = [], []
    for split, count in [('train', 8), ('validation', 2), ('review', 2), ('test', 2)]:
        for label, vector in [('card_arrival', [1., 0.]), ('card_not_working', [0., 1.])]:
            for number in range(count):
                rows.append(dict(id=f'{split}/{label}/{number}', text=('card delivery' if vector[0] else 'broken card') + f' {number}', label=label, split=split))
                features.append(vector)
    root.mkdir()
    (root / 'manifest.json').write_text(json.dumps({'fixture': True}))
    return dict(rows=rows, features=np.asarray(features), root=root)


def inspection_fixture():
    return dict(records=[dict(case_id=str(i), partition=p, label=i % 2) for i, p in enumerate(['fit'] * 4 + ['review'] * 2 + ['validation'] * 2 + ['test'] * 2)],
                whole=np.random.default_rng(4).normal(size=(10, 3)).astype('float32'),
                patches=np.random.default_rng(5).normal(size=(10, 2, 2, 2)).astype('float32'))


def test_routing_authored_actions_split_existing_stages_and_resume(tmp_path, monkeypatch):
    cells = authored('routing')
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path / 'state')
    data = routing_fixture(tmp_path / 'data')
    calls, results = [], {}
    fit = routing.fit_classifier
    monkeypatch.setattr(routing, 'fit_classifier', lambda data, kind, **kwargs: (calls.append(kind), fit(data, kind, **kwargs))[1])
    scope = dict(mo=SimpleNamespace(stop=stop), teaching=routing_teaching, routing=routing, time=time, joblib=joblib,
                 train_classifiers=SimpleNamespace(value=True), train_embedding=SimpleNamespace(value=True),
                 classifier_editor=SimpleNamespace(value=routing_teaching.CLASSIFIER_SOLUTION),
                 get_context=lambda: {'session': session}, get_data=lambda: data, refresh=lambda: None,
                 trace_saved=lambda stage: {'status': 'test-only export stub'}, show_result=lambda key, value: results.update({key: value}))
    run_cell(cells, 'request_routing/action/train_classifiers', scope)
    first = routing_teaching.saved(session, 'routing/baseline/tfidf')
    assert calls == ['tfidf']
    assert first['config'] == {'kind': 'tfidf', 'seed': 17, 'dataset': routing.checksum(data['root'] / 'manifest.json')}
    assert first['sources'] == {'classifier.py': routing_teaching.CLASSIFIER_SOLUTION}
    assert not routing_teaching.baselines_complete(session)
    assert 'baseline' not in session.read()['progress'].get('completed', [])
    assert 'baseline-tfidf' in session.read()['progress']['completed']
    assert 'One of two' in results['tfidf']['comparison']
    assert routing_teaching.validation_examples(session)
    run_cell(cells, 'request_routing/action/train_embedding', scope)
    assert calls == ['tfidf', 'embedding']
    assert routing_teaching.baselines_complete(session)
    assert 'baseline' in session.read()['progress']['completed']
    ids = set(session.read()['stages'])
    # Same actions also read legacy completed records with these exact specifications.
    restored = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path / 'state')
    scope['get_context'] = lambda: {'session': restored}
    run_cell(cells, 'request_routing/action/train_classifiers', scope)
    run_cell(cells, 'request_routing/action/train_embedding', scope)
    assert calls == ['tfidf', 'embedding']
    assert ids == set(restored.read()['stages'])
    assert restored.read()['requests'] == {}


def test_routing_alternative_requires_saved_baseline_and_same_code(tmp_path):
    cells = authored('routing')
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path)
    scope = dict(mo=SimpleNamespace(stop=stop), teaching=routing_teaching,
                 train_embedding=SimpleNamespace(value=True), classifier_editor=SimpleNamespace(value=routing_teaching.CLASSIFIER_SOLUTION),
                 get_context=lambda: {'session': session}, get_data=lambda: {})
    with pytest.raises(ValueError, match='word-feature baseline'):
        run_cell(cells, 'request_routing/action/train_embedding', scope)
    with session.stage('routing/baseline/tfidf', sources={'classifier.py': routing_teaching.CLASSIFIER_SOLUTION}) as stage:
        stage.record({'validation': []})
    with pytest.raises(ValueError, match='same classifier settings'):
        routing_teaching.check_matched_classifier(session, routing_teaching.CLASSIFIER_SOLUTION.replace('C=10', 'C=3'))
    assert routing_teaching.freeze_prerequisite(session) == 'Train the two baseline classifiers first.'


def test_inspection_authored_actions_preserve_starter_baseline_and_patch_extension(tmp_path, monkeypatch):
    cells = authored('inspection')
    session = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    data = inspection_fixture()
    calls = []
    fit = inspection.fit_classifier
    monkeypatch.setattr(inspection, 'fit_classifier', lambda data, rows, method, **kwargs: (calls.append(method), fit(data, rows, method, **kwargs))[1])
    feature_editor = SimpleNamespace(value=inspection_teaching.FEATURE_STARTER)
    scope = dict(mo=SimpleNamespace(stop=stop), teaching=inspection_teaching, inspection=inspection,
                 train_whole=SimpleNamespace(value=True), train_inspection=SimpleNamespace(value=True),
                 feature_editor=feature_editor, threshold_editor=SimpleNamespace(value=inspection_teaching.THRESHOLD_SOLUTION),
                 get_lab=lambda: {'session': session, 'data': data}, refresh_inspection=lambda: None,
                 event=event, export_trace=lambda *a, **k: {}, instrument_inspection_tool=lambda _: None, feedback=lambda *a: None,
                 build_features=lambda *args, **kwargs: inspection_teaching.functions(feature_editor.value)['build_features'](*args, **kwargs),
                 choose_threshold=inspection_teaching.functions(inspection_teaching.THRESHOLD_SOLUTION)['choose_threshold'])
    run_cell(cells, 'visual_inspection/action/train_whole', scope)
    baseline = inspection_teaching.saved(session, 'compare/whole')
    assert calls == ['whole']
    assert baseline['config'] == {'method': 'whole', 'C': .03, 'threshold_recall': .90}
    assert baseline['sources']['features.py'] == inspection_teaching.FEATURE_STARTER
    assert 'baseline' in inspection_teaching.completed_steps(session)
    assert 'baseline' in session.read()['progress']['completed']
    assert 'compare' not in inspection_teaching.completed_steps(session)
    # No reflection form is required. The new code changes only the patch branch.
    feature_editor.value = inspection_teaching.FEATURE_SOLUTION
    run_cell(cells, 'visual_inspection/action/train_inspection', scope)
    assert calls == ['whole', 'nearest-patch']
    assert inspection_teaching.saved(session, 'compare/whole')['id'] == baseline['id']
    assert 'compare' in inspection_teaching.completed_steps(session)
    ids = set(session.read()['stages'])
    run_cell(cells, 'visual_inspection/action/train_inspection', scope)
    feature_editor.value = inspection_teaching.FEATURE_STARTER
    run_cell(cells, 'visual_inspection/action/train_whole', scope)
    assert calls == ['whole', 'nearest-patch']
    assert ids == set(session.read()['stages'])
    assert session.read()['requests'] == {}


def test_whole_check_accepts_unfinished_patch_branch_and_blocks_changed_inputs(tmp_path):
    teaching = inspection_teaching
    assert teaching.check_whole_features(teaching.FEATURE_STARTER)['status'] == 'complete'
    with pytest.raises(NotImplementedError):
        teaching.check_features(teaching.FEATURE_STARTER)
    session = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    data = inspection_fixture()
    with pytest.raises(ValueError, match='whole-image baseline'):
        teaching.check_matched_settings(session, 'nearest-patch', teaching.FEATURE_SOLUTION, teaching.THRESHOLD_SOLUTION, data)
    with session.stage('compare/whole', sources={'features.py': teaching.FEATURE_STARTER, 'threshold.py': teaching.THRESHOLD_SOLUTION}) as stage:
        stage.record({})
    assert teaching.check_matched_settings(session, 'nearest-patch', teaching.FEATURE_SOLUTION, teaching.THRESHOLD_SOLUTION, data)
    with pytest.raises(ValueError, match='threshold rule'):
        teaching.check_matched_settings(session, 'nearest-patch', teaching.FEATURE_SOLUTION, teaching.THRESHOLD_SOLUTION + '\n# changed', data)
    with pytest.raises(ValueError, match='whole-image branch'):
        teaching.check_matched_settings(session, 'nearest-patch', teaching.FEATURE_SOLUTION.replace('return whole', 'return whole * 2'), teaching.THRESHOLD_SOLUTION, data)


def test_legacy_inspection_completed_stages_restore_without_new_checkpoint(tmp_path):
    session = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    for name in ('whole', 'nearest-patch'):
        with session.stage('compare/' + name, sources={'features.py': inspection_teaching.FEATURE_SOLUTION, 'threshold.py': inspection_teaching.THRESHOLD_SOLUTION}) as stage:
            stage.record({})
    restored = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    assert {'baseline', 'compare'} <= inspection_teaching.completed_steps(restored)
    for name in ('whole', 'nearest-patch'):
        assert inspection_teaching.check_matched_settings(restored, name, inspection_teaching.FEATURE_SOLUTION, inspection_teaching.THRESHOLD_SOLUTION, inspection_fixture())


def test_inspection_freeze_rejects_a_partial_comparison(tmp_path):
    session = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    with session.stage('compare/whole') as stage:
        stage.record({})
    scope = dict(mo=SimpleNamespace(stop=stop), teaching=inspection_teaching,
                 freeze_inspection=SimpleNamespace(value=True), freeze_reason=SimpleNamespace(value='Check validation mistakes.'),
                 get_lab=lambda: {'session': session})
    with pytest.raises(ValueError, match='Complete both representations'):
        run_cell(authored('inspection'), 'visual_inspection/action/freeze_inspection', scope)
    assert inspection_teaching.saved(session, 'freeze') is None


def test_prompted_progress_requires_the_fixed_eight_cases(tmp_path):
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path)
    rows = [dict(case_id=f'validation/{n:02}', text=f'Request {n}', target='card_arrival') for n in reversed(range(10))]
    with session.stage('routing/baseline/embedding') as stage:
        stage.record({'validation': rows})
    assert [row['case_id'] for row in routing_teaching.prompted_examples(session)] == [f'validation/{n:02}' for n in range(8)]
    for number in (*range(7), 9):
        identity = f'validation/{number:02}'
        with session.stage('routing/judge/prompted/' + identity, config={'case_id': identity}) as stage:
            stage.record({'case_id': identity})
    # Eight completed calls do not suffice if one belongs outside the fixed cohort.
    assert not routing_teaching.prompted_complete(session)
    assert 'prompted' not in routing_teaching.completed_steps(session)
    assert 'routing-sample' not in session.read()['progress'].get('completed', [])
    identity = 'validation/07'
    with session.stage('routing/judge/prompted/' + identity, config={'case_id': identity}) as stage:
        stage.record({'case_id': identity})
    assert routing_teaching.prompted_complete(session)
    assert 'prompted' in routing_teaching.completed_steps(session)
    # Legacy completed records require no new checkpoint or model request.
    restored = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path)
    assert 'prompted' in routing_teaching.completed_steps(restored)
    assert restored.read()['requests'] == {}


def test_prompted_action_resumes_only_the_missing_fixed_case(tmp_path):
    session = WorkshopSession('test/routing', 'banking-routing', state_dir=tmp_path)
    rows = [dict(case_id=f'validation/{n:02}', text=f'Request {n}', target='card_arrival') for n in range(10)]
    with session.stage('routing/baseline/embedding') as stage:
        stage.record({'validation': list(reversed(rows))})
    for row in rows[:7]:
        with session.stage('routing/judge/prompted/' + row['case_id'], config={'case_id': row['case_id']}) as stage:
            stage.record({'case_id': row['case_id']})
    requested = []
    def fake_request(session, identity, messages, validate, **kwargs):
        requested.append(messages[-1]['content'])
        return validate({'intent': 'card_arrival', 'needs_review': False, 'reason': 'Fixture response.'}), {}
    scope = dict(mo=SimpleNamespace(stop=stop), teaching=routing_teaching, routing=routing,
                 run_prompted=SimpleNamespace(value=True), get_context=lambda: {'session': session},
                 get_data=lambda: {'rows': [{'split': 'train', 'label': 'card_arrival'}]},
                 validated_json=fake_request, show_result=lambda *a: None, trace_saved=lambda _: {}, refresh=lambda: None)
    run_cell(authored('routing'), 'request_routing/action/run_prompted', scope)
    assert requested == ['Request 7']
    assert 'routing-sample' in session.read()['progress']['completed']
    run_cell(authored('routing'), 'request_routing/action/run_prompted', scope)
    assert requested == ['Request 7']
    assert routing_teaching.prompted_complete(session)


def test_development_previews_have_provenance_and_no_test_record():
    board = inspection_teaching.opening_board()
    assert board['partition'] == 'fit'
    assert board['case_id'] == 'pcb1-anomaly-005'
    for key in ('image', 'mask'):
        assert hashlib.sha256(board[key].read_bytes()).hexdigest() == board[key + '_sha256']
    assert 'CC BY 4.0' in board['license']
    assert routing_teaching.OPENING_REQUEST['split'] == 'review'
    assert routing_teaching.OPENING_REQUEST['case_id'].startswith('official-train/')


def test_authored_cells_remain_valid_and_code_examples_visible():
    from notebook_builder import analyze
    for name in ('routing', 'inspection'):
        cells = authored(name)
        definitions, _, _ = analyze(cells)
        opening = next(cell for cell in cells if cell.cell_id.endswith('/opening_example'))
        assert 'Image' not in definitions[cells.index(opening)], 'A hidden annotation must not return an unbound import.'
        assert 'get_context' not in opening.code and 'get_lab' not in opening.code
        for forbidden in ('Provider(', '.check_access(', '.stage(', '.fit(', 'httpx.'):
            assert forbidden not in opening.code
    cells = authored('routing')
    practice = next(cell for cell in cells if cell.cell_id.endswith('/action/practice_fit'))
    assert not practice.hide and '.fit(' in practice.code and '.predict_proba(' in practice.code
    cells = authored('inspection')
    distance = next(cell for cell in cells if cell.cell_id.endswith('/action/patch_distance'))
    assert not distance.hide and '_distances=np.mean' in distance.code
    assert '"fit"' in distance.code and 'np.isclose' in distance.code
