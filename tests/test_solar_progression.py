"""Free checks for the authored one-trial/remaining-trials Sweep sequence."""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from forge_workshop_kit import WorkshopSession, solar_teaching as teaching
from forge_workshop_kit.session import digest


def source_cell(prefix):
    sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
    from solar_cells import cells
    return next(cell.code for cell in cells if cell.code.startswith(prefix))


def test_bundled_example_is_real_training_date_and_requires_no_session():
    row = teaching.development_preview()
    assert row['origin'] == '2014-02-01T01:00'
    assert row['target_time'] == '2014-02-01T01:30'
    assert abs(row['latest_log10'] - row['target_log10']) == pytest.approx(.5932660102844238)
    assert len(row['dataset_sha256']) == 64


def test_plan_freezes_every_input_and_survives_restart(tmp_path):
    session = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    plan = teaching.freeze_search_plan(session, 'source', 'metric', 'data')
    assert plan['configurations'] == [
        {'architecture': a, 'width': w, 'learning_rate': lr, 'steps': 60, 'seed': 17, 'batch_size': 32}
        for a in ('mlp', 'cnn') for w, lr in ((16, .001), (32, .001), (16, .003))]
    restored = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    assert teaching.freeze_search_plan(restored, 'source', 'metric', 'data') == plan
    for values in [('edited', 'metric', 'data'), ('source', 'edited', 'data'), ('source', 'metric', 'other')]:
        with pytest.raises(ValueError, match='frozen'):
            teaching.freeze_search_plan(restored, *values)
    plan['configurations'][0]['steps'] = 999
    assert teaching.freeze_search_plan(restored, 'source', 'metric', 'data')['configurations'][0]['steps'] == 60
    assert not restored.read()['requests']


def test_assignment_counts_use_native_jobs_and_preserve_uncertainty():
    assert teaching.sweep_assignments([])['unassigned'] == list(range(6))
    local = [{'trial': 0, 'id': 'a', 'state': 'running'}]
    assert teaching.sweep_assignments([], local)['unassigned'] == [1, 2, 3, 4, 5]
    native = [{'trial': 0, 'id': 'a', 'state': 'finished'}]
    assert teaching.sweep_assignments(native, local)['finished'] == [0]
    assert not teaching.sweep_assignments(native, local)['unresolved']
    with pytest.raises(ValueError, match='multiple'):
        teaching.sweep_assignments([{'trial': 0, 'id': 'b', 'state': 'finished'}], local)


@pytest.mark.parametrize('cached_first', [False, True])
def test_current_action_schedules_one_then_five_and_reuses_training(tmp_path, monkeypatch, cached_first):
    session = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    source, metric = SimpleNamespace(value='source'), SimpleNamespace(value='metric')
    lab = {'session': session, 'dataset': 'data', 'goes': {'train': {}, 'validation': {}}}
    allocated, agent_counts, trained = [], [], []
    selected = {}

    class Config(dict):
        def __getattr__(self, key): return self[key]

    class Run:
        def __init__(self, i):
            self.id, self.config, self.state, self.summary = f'run-{i}', Config(trial=i), 'running', {}
        def __enter__(self): return self
        def __exit__(self, kind, *args): self.state = 'failed' if kind else 'finished'
        def log(self, metrics): self.summary.update(metrics)

    def agent(sweep_id, function, count, **kwargs):
        agent_counts.append(count)
        for _ in range(count):
            i = next(i for i in range(6) if i not in [r.config.trial for r in allocated])
            selected['run'] = Run(i)
            allocated.append(selected['run'])
            function()

    fake = SimpleNamespace(
        sweep=lambda *a, **kw: 'sweep-id',
        agent=agent,
        init=lambda **kw: selected['run'],
        Api=lambda: SimpleNamespace(sweep=lambda path: SimpleNamespace(runs=allocated)),
    )
    monkeypatch.setitem(sys.modules, 'wandb', fake)
    monkeypatch.setattr(teaching, 'check_model', lambda *a: {})
    monkeypatch.setattr(teaching, 'check_flux_metric', lambda *a: {})

    def train(s, name, source, splits, config, dataset, metric):
        with s.stage(name, config=config, sources={'candidate.py': source, 'development_metric.py': metric}, inputs={'dataset': dataset, 'split': 'validation'}) as stage:
            if stage.needs_run:
                trained.append(name)
                stage.record({'metrics': {'validation_error': .2}})
        return {'stage_id': stage.id, 'metrics': stage.result['metrics']}

    if cached_first:
        train(session, 'goes/search-0', 'source', lab['goes'], teaching.measurement_configurations()[0], 'data', 'metric')
        trained.clear()
    import os
    scope = {'teaching': teaching, 'get_lab': lambda: lab, 'measurement_editor': source,
             'flux_metric_editor': metric, 'digest': digest, 'run_training': train,
             'refresh_saved': lambda: None, 'os': os}
    exec(source_cell('def run_measurement_sweep('), scope)
    with pytest.raises(ValueError, match='one tracked Sweep trial first'):
        scope['run_measurement_sweep'](6)
    assert agent_counts == []
    first = scope['run_measurement_sweep'](1)
    assert first['Sweep trial assignments'] == first['Finished Sweep runs'] == 1
    assert 'search' not in teaching.completed_steps(session)
    assert len(trained) == (0 if cached_first else 1)
    source.value = 'different source'
    with pytest.raises(ValueError, match='frozen'):
        scope['run_measurement_sweep'](6)
    assert agent_counts == [1]
    source.value = 'source'
    rest = scope['run_measurement_sweep'](6)
    assert agent_counts == [1, 5]
    assert rest['Complete']
    assert len(teaching.sweep_training_rows(session, teaching.saved(session, 'goes/sweep-plan')['result'])) == 6
    assert 'search' in teaching.completed_steps(session)
    assert scope['run_measurement_sweep'](6)['Complete']
    assert agent_counts == [1, 5]
    assert len(trained) == (5 if cached_first else 6)
    restored = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    assert 'search' in teaching.completed_steps(restored)
    assert not restored.read()['requests']


def test_legacy_search_restores_without_new_sweep_jobs(tmp_path):
    s = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    for i in range(6):
        with s.stage(f'goes/search-{i}') as stage:
            stage.record({'metrics': {'validation_error': .2}})
    before = s.state_path.read_bytes()
    assert 'search' in teaching.completed_steps(s)
    assert teaching.restore_state(s)['session'] is s
    assert s.state_path.read_bytes() == before


def test_training_rows_require_exact_source_settings_and_dataset(tmp_path):
    s = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    plan = teaching.freeze_search_plan(s, 'source', 'metric', 'data')
    for difference in ('source', 'config', 'dataset'):
        config = dict(plan['configurations'][0])
        if difference == 'config': config['steps'] = 999
        with s.stage('goes/search-0', config=config,
                     sources={'candidate.py': 'other' if difference == 'source' else 'source', 'development_metric.py': 'metric'},
                     inputs={'dataset': 'other' if difference == 'dataset' else 'data', 'split': 'validation'}) as stage:
            stage.record({'metrics': {'validation_error': 0}})
    assert teaching.sweep_training_rows(s, plan) == []


def test_sweep_plan_is_not_a_final_selection_candidate(tmp_path):
    s = WorkshopSession('learner/solar', 'solar-autoresearch', state_dir=tmp_path)
    teaching.freeze_search_plan(s, 'source', 'metric', 'data')
    assert not any(row['name'].startswith('goes/search-') for row in s.completed())
