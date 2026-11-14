"""Exercise the authored notebook actions against durable stage caching."""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import importlib.util
import sys

import numpy as np
import pytest

from forge_workshop_kit import WorkshopSession, inspection, inspection_teaching as teaching
from forge_workshop_kit.traces import event


def authored_action(prefix):
    scripts = Path(__file__).resolve().parents[1] / 'scripts'
    sys.path.insert(0, str(scripts))
    try:
        spec = importlib.util.spec_from_file_location('inspection_cells_cache_test', scripts / 'inspection_cells.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return next(cell.code for cell in module.cells if cell.code.startswith(prefix))


def test_new_detector_invalidates_review_training_and_freeze(tmp_path, monkeypatch):
    session = WorkshopSession('test/inspection', 'visual-inspection', state_dir=tmp_path)
    monkeypatch.setattr(session, 'checkpoint', lambda *a, **k: None)
    data = {'records': [{'case_id': str(i), 'partition': partition, 'label': i % 2}
                       for i, partition in enumerate(['fit'] * 4 + ['review'] * 30 + ['validation'] * 4)]}
    source = teaching.FEATURE_SOLUTION
    # The notebook's actual selection, training and freeze actions run. Numerical
    # fitting is replaced with a tiny saved model so this test isolates caching.
    monkeypatch.setattr(teaching, 'model_from_stage', lambda *a: {'threshold': 0.})
    monkeypatch.setattr(inspection, 'score', lambda data, rows, model, **k: np.linspace(-1, 1, len(rows)))
    monkeypatch.setattr(inspection, 'fit_classifier', lambda data, rows, *a, **k: {'rows': list(map(int, rows))})
    def save_model(path, model, threshold):
        content = repr((model, threshold)).encode()
        path.write_bytes(content)
        return hashlib.sha256(content).hexdigest()
    monkeypatch.setattr(inspection, 'save_classifier', save_model)
    scope = dict(mo=SimpleNamespace(stop=lambda condition: (_ for _ in ()).throw(AssertionError('blocked')) if condition else None),
        np=np, get_lab=lambda: {'session': session, 'data': data}, teaching=teaching, inspection=inspection,
        feature_editor=SimpleNamespace(value=source), review_editor=SimpleNamespace(value=teaching.REVIEW_SOLUTION),
        threshold_editor=SimpleNamespace(value=teaching.THRESHOLD_SOLUTION),
        select_inspection_review=SimpleNamespace(value=True), train_reviewed=SimpleNamespace(value=True),
        freeze_inspection=SimpleNamespace(value=True), freeze_choice=SimpleNamespace(value='compare/nearest-patch'),
        freeze_reason=SimpleNamespace(value='Choose using saved validation results.'),
        build_features=lambda *a, **k: None, choose_threshold=lambda *a: 0., event=event,
        instrument_inspection_tool=lambda *a: None, export_trace=lambda *a, **k: {},
        refresh_inspection=lambda: None, feedback=lambda *a: None)
    selection_code = authored_action('mo.stop(not select_inspection_review.value)')
    training_code = authored_action('mo.stop(not train_reviewed.value)')
    freeze_code = authored_action('mo.stop(not freeze_inspection.value)')

    def parent(revision):
        for method in ('whole', 'nearest-patch'):
            with session.stage('compare/' + method, config={'revision': revision}, sources={'features.py': source}) as stage:
                stage.record({'model_file': 'example.npz', 'model_sha256': str(revision)})

    parent(1)
    exec(selection_code, scope)
    first_selection = teaching.saved(session, 'review/selection')
    exec(training_code, scope)
    first_training = teaching.saved(session, 'review/active')
    exec(freeze_code, scope)
    first_freeze = teaching.saved(session, 'freeze')
    exec(selection_code, scope)
    exec(training_code, scope)
    exec(freeze_code, scope)
    assert teaching.saved(session, 'freeze')['id'] == first_freeze['id']

    parent(2)
    with pytest.raises(ValueError, match='select its review batch again'):
        exec(training_code, scope)
    exec(selection_code, scope)
    assert teaching.saved(session, 'review/selection')['id'] != first_selection['id']
    exec(training_code, scope)
    second_training = teaching.saved(session, 'review/active')
    assert second_training['id'] != first_training['id']
    assert second_training['config']['selection_stage'] == teaching.saved(session, 'review/selection')['id']
    assert len(second_training['config']['selected_cases']) == 24
    exec(freeze_code, scope)
    second_freeze = teaching.saved(session, 'freeze')
    assert second_freeze['id'] != first_freeze['id']
    assert second_freeze['result']['versions']['review/active']['stage_id'] == second_training['id']

    with session.stage('evaluate', config={'freeze': second_freeze['id']}) as stage:
        stage.record({'selected': 'compare/nearest-patch'})
    frozen_count = len([r for r in session.read()['stages'].values() if r['name'] == 'freeze'])
    scope['freeze_reason'].value = 'Same tested model; adding explanation must not rerun it.'
    exec(freeze_code, scope)
    assert len([r for r in session.read()['stages'].values() if r['name'] == 'freeze']) == frozen_count
    scope['freeze_choice'].value = 'review/active'
    with pytest.raises(ValueError, match='new teaching-retest workspace'):
        exec(freeze_code, scope)
    scope['freeze_choice'].value = 'compare/nearest-patch'
    parent(3)
    with pytest.raises(ValueError, match='new teaching-retest workspace'):
        exec(freeze_code, scope)

    scope['feature_editor'].value = source + '\n# New feature draft, not trained yet.\n'
    with pytest.raises(ValueError, match='Train both representations'):
        exec(selection_code, scope)
