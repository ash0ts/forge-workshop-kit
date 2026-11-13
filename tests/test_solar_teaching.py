from pathlib import Path

import pytest

from forge_workshop_kit import WorkshopSession, solar_teaching as teaching


def session(tmp_path):
    return WorkshopSession('learner/research', 'solar-autoresearch', state_dir=tmp_path)


def record(s, name, result, *, source='source', config=None, inputs=None):
    with s.stage(name, sources={'candidate.py': source}, config=config or {}, inputs=inputs or {'split': 'validation'}) as stage:
        stage.record(result)
    return s.read()['stages'][stage.id]


def test_starter_gaps_fail_and_worked_answers_are_executable():
    for starter, answer, check in (
        (teaching.PERSISTENCE_STARTER, teaching.PERSISTENCE_SOLUTION, teaching.check_persistence),
        (teaching.FLUX_STARTER, teaching.FLUX_SOLUTION, teaching.check_flux_metric),
        (teaching.IMAGE_METRIC_STARTER, teaching.IMAGE_METRIC_SOLUTION, teaching.check_image_metric),
        (teaching.EVIDENCE_STARTER, teaching.EVIDENCE_SOLUTION, teaching.check_evidence),
    ):
        with pytest.raises(NotImplementedError):
            check(starter)
        assert check(answer)['checks'] >= 2


def test_evidence_check_rejects_final_records_and_fabricated_scores():
    with pytest.raises(ValueError, match='training/validation'):
        teaching.check_evidence('def select_validation_evidence(record):\n    return record')
    source = teaching.EVIDENCE_SOLUTION.replace('return {name:', 'record["metrics"] = {"validation_error": 999}\n    return {name:')
    with pytest.raises(ValueError, match='recorded values'):
        teaching.check_evidence(source)


def test_local_metrics_detect_signed_and_off_disk_errors():
    with pytest.raises(ValueError):
        teaching.check_flux_metric('def my_flux_mae(prediction,target):\n    return float((prediction-target).mean())')
    with pytest.raises(ValueError):
        teaching.check_image_metric('def my_image_mae(prediction,target,disk_mask):\n    return float(np.abs(prediction-target).mean())')


def test_instrumentation_check_requires_attributes_and_real_error_evidence():
    with pytest.raises(ValueError, match='set_attributes'):
        teaching.check_instrumentation(teaching.INSTRUMENTATION_STARTER)
    assert teaching.check_instrumentation(teaching.INSTRUMENTATION_SOLUTION)['checks'] == 4
    without_errors = teaching.INSTRUMENTATION_SOLUTION.replace('tool.record_error(RuntimeError(observation["error"]))', 'pass')
    with pytest.raises(ValueError, match='supplied error'):
        teaching.check_instrumentation(without_errors)
    invented_result = teaching.INSTRUMENTATION_SOLUTION.replace('result=observation["result"]', 'result={"answer": 999}')
    with pytest.raises(ValueError, match='actual observation'):
        teaching.check_instrumentation(invented_result)


def test_model_gaps_and_solution_preserve_architecture_shapes():
    source = (Path(__file__).parents[1] / 'examples/solar/candidate.py').read_text()
    for task in ('measurement', 'image'):
        with pytest.raises(NotImplementedError):
            teaching.check_model(teaching.model_starter(source, task), task)
        assert teaching.check_model(source, task)['checks'] == 4


def test_guided_order_requires_each_review_before_its_probe(tmp_path):
    s = session(tmp_path)
    expected = ['propose', 'review-0', 'probe-result-0', 'review-1', 'probe-result-1',
                'probe-done', 'compose', 'review-composition', 'composition-result', 'adopt']
    for phase in expected:
        assert teaching.next_action(s)[0:2] == (1, phase)
        record(s, 'images/round-1/' + phase, {})
    assert teaching.next_action(s)[0:2] == (2, 'propose')
    record(s, 'images/round-2/adopt', {'retained_parent': True})
    assert teaching.next_action(s)[1] == 'done'


def test_legacy_completed_rounds_do_not_request_new_execution(tmp_path):
    s = session(tmp_path)
    record(s, 'images/round-1/adopt', {'retained_parent': True})
    record(s, 'images/round-2/adopt', {'retained_parent': True})
    assert teaching.next_action(s)[1] == 'done'


def test_restore_uses_saved_results_and_research_parent(tmp_path):
    s = session(tmp_path)
    old = record(s, 'images/manual-conv', {'metrics': {'validation_error': 0.3}, 'losses': [0.7]}, source='original', config={'architecture': 'conv'})
    record(s, 'images/manual-residual', {'metrics': {'validation_error': 0.2}}, source='original', config={'architecture': 'residual'})
    record(s, 'images/round-1/propose', {'candidates': []}, source='original')
    record(s, 'images/manual-conv', {'metrics': {'validation_error': 0.01}}, source='later-draft')
    final = {'metrics_by_version': {'agent': {'error': 0.4}}, 'rows': {'agent': []}}
    record(s, 'images/final-comparison', final)
    with s.transaction() as journal:
        journal['publications']['trace/' + old['id']] = {'url': 'https://example.test/trace', 'verified': True}
    before = s.state_path.read_bytes()
    restored = teaching.restore_state(s)
    assert restored['manual']['source'] == 'original'
    assert restored['manual']['config']['architecture'] == 'residual'
    assert restored['final'] == final
    assert teaching.training_record(s, old)['trace']['verified']
    assert s.state_path.read_bytes() == before


def test_drafts_remain_separate_and_survive_a_new_session(tmp_path):
    s = session(tmp_path)
    s.save_draft('solar/measurement', 'measurement source')
    s.save_draft('solar/image', 'image source')
    reopened = session(tmp_path)
    assert reopened.get_draft('solar/measurement') == 'measurement source'
    assert reopened.get_draft('solar/image') == 'image source'
    assert not reopened.read()['requests']
    assert not reopened.read()['stages']


def test_authored_training_uses_learner_metric_without_replacing_native_score(tmp_path):
    import sys
    import time
    from types import SimpleNamespace
    import numpy as np
    from forge_workshop_kit import solar
    sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
    from solar_cells import cells
    code = next(cell.code for cell in cells if cell.code.startswith('def run_training('))
    calls = []

    def train(source, train_split, validation, config, output):
        calls.append(source)
        prediction = validation['y'] + 1
        for name in ('candidate.py', 'weights.pt', 'predictions.npy', 'losses.json', 'stderr.txt'):
            (output / name).write_text('fixture')
        metrics = solar.score(prediction, validation)
        return {'metrics': {**metrics, 'validation_error': metrics['error']}, 'losses': [2, 1]}, prediction

    scope = {
        'time': time, 'np': np, 'teaching': teaching, 'training': SimpleNamespace(train=train),
        'plots': SimpleNamespace(forecast=lambda *a, **kw: SimpleNamespace(savefig=lambda path, **kw: path.write_bytes(b'figure'))),
        'export_trace': lambda *a, **kw: {}, 'instrument_tool': lambda observation: 'span',
        'event': __import__('forge_workshop_kit.traces', fromlist=['event']).event,
    }
    exec(code, scope)
    s = session(tmp_path)
    split = {'y': np.zeros((2, 1)), 'mask': np.ones((2, 1)), 'persistence': np.ones((2, 1))}
    metric = teaching.FLUX_SOLUTION
    first = scope['run_training'](s, 'goes/search-0', 'model-code', {'train': split, 'validation': split}, {}, 'dataset', metric)
    second = scope['run_training'](s, 'goes/search-0', 'model-code', {'train': split, 'validation': split}, {}, 'dataset', metric.replace('.mean())', '.mean()) * 2'))
    assert first['metrics']['learner_metric'] == 1
    assert second['metrics']['learner_metric'] == 2
    assert first['metrics']['error'] == second['metrics']['error'] == 1
    assert not second['metrics']['learner_metric_matches']
    assert first['stage_id'] != second['stage_id']
    # Reopening the exact source/metric/config returns the execution, not another train.
    scope['run_training'](s, 'goes/search-0', 'model-code', {'train': split, 'validation': split}, {}, 'dataset', metric)
    assert len(calls) == 2


def test_navigation_widgets_are_registered_as_global_ui_elements():
    import ast
    import sys
    sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
    from solar_cells import cells
    count = 0
    for cell in cells:
        tree = ast.parse(cell.code)
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for call in ast.walk(tree):
            if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
                continue
            if not isinstance(call.func.value, ast.Name) or call.func.value.id != 'ui':
                continue
            if call.func.attr not in ('navigation', 'next_step', 'prerequisite'):
                continue
            assignment = parents[call]
            assert isinstance(assignment, ast.Assign), 'Callbacks need a globally bound UI element in marimo.'
            assert isinstance(assignment.targets[0], ast.Name)
            assert not assignment.targets[0].id.startswith('_')
            count += 1
    assert count >= 15


def test_recorded_example_matches_evidence_and_cannot_execute_work():
    import ast
    import json
    import sys
    root = Path(__file__).parents[1]
    sys.path.insert(0, str(root / 'scripts'))
    from solar_cells import cells
    code = next(cell.code for cell in cells if '**Recorded example' in cell.code)
    evidence = json.loads((root / 'evidence/ux-v020-solar.json').read_text())
    scores = evidence['final_images']
    for label in ('manual', 'agent', 'persistence'):
        assert f"{scores[label]['error']:.5f}" in code
    relative = 100 * (1 - scores['agent']['error'] / scores['manual']['error'])
    assert f'{relative:.2f}% lower' in code
    assert '199 overlapping windows' in code and 'One seed' in code
    assert 'separate from your results' in code
    assert 'GOES measurement model performed worse' in code
    assert evidence['report'] in code
    calls = [node.func for node in ast.walk(ast.parse(code)) if isinstance(node, ast.Call)]
    assert all(isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
               and fn.value.id in ('mo', 'ui') or isinstance(fn, ast.Name)
               and fn.id == 'get_step' for fn in calls)
    authored = '\n'.join(cell.code for cell in cells)
    assert 'theme="lab"' in authored
    assert 'Pending, Inc.' not in authored and 'Management' not in authored
