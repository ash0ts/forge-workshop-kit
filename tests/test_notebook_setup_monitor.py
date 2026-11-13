import threading
from types import SimpleNamespace

import pytest

from forge_workshop_kit import WorkshopSession, setup, ui
from forge_workshop_kit.monitoring import load_roster, save_roster, monitor, project_name


def test_copied_project_wins_over_operator_default():
    env = {'WANDB_ENTITY': 'attendee', 'WANDB_PROJECT': 'mine',
           'WANDB_NOTEBOOK_ANCHOR_RUN': 'copied-notebook', 'WORKSHOP_PROJECT': 'host/template'}
    assert setup.project_context(env) == {'project': 'attendee/mine', 'hosted': True,
        'detected': True, 'source': 'Copied notebook project'}
    env.pop('WANDB_NOTEBOOK_ANCHOR_RUN')
    assert setup.project_context(env)['project'] == 'host/template'
    assert setup.project_context({})['project'] == ''


def test_capabilities_do_not_claim_inference_or_evaluation_from_access(tmp_path):
    session = WorkshopSession('person/mine', 'starter', state_dir=tmp_path)
    setup.save_access(session, {'write_access': True})
    statuses = {row['Capability']: row['Status'] for row in setup.capabilities(session)}
    assert statuses['Project writes'] == 'Verified'
    assert statuses['Inference'] == 'Not yet called'
    assert statuses['Agent Lens'] == 'Not yet verified'
    with session.transaction() as state:
        state['publications']['trace/x'] = {'verified': True}
        state['publications']['comparison/x'] = {'starting': {'weave_status': 'published', 'native_status': 'unavailable'}}
    statuses = {row['Capability']: row['Status'] for row in setup.capabilities(session)}
    assert statuses['Agent Lens'] == 'Verified from saved work'
    assert statuses['Weave evaluations'] == 'Verified from saved work'
    assert statuses['Native EvalTables'] == 'Upload needs attention'


def test_roster_round_trip_and_project_link_validation(tmp_path):
    path = tmp_path / 'monitor' / 'roster.json'
    assert load_roster(path)['projects'] == []
    saved = save_roster(path, {'projects': ['a/b', 'https://forge.coreweave.com/wandb/a/b', 'https://wandb.ai/c/d'], 'workshop': 'solar-autoresearch', 'since': '2026-11-13'})
    assert saved['projects'] == ['a/b', 'c/d']
    assert load_roster(path) == saved
    with pytest.raises(ValueError):
        project_name('https://not-a-project.test/a/b')
    with pytest.raises(ValueError):
        project_name('Bearer secret-token')


def run(workspace, updated, session='copy-a', checkpoint='images/round-1/propose'):
    return SimpleNamespace(config={'workspace_id': workspace, 'notebook_identity': session}, url='https://example.test/run',
        summary=SimpleNamespace(_json_dict={'step': checkpoint, 'updated_at': updated, 'completed': ['setup'], 'status': 'complete'}))


def test_monitor_keeps_workspaces_separate_and_filters_by_saved_time():
    class Api:
        def runs(self, project, filters):
            return [run('a', 10), run('b', 20), run('c', None)]
    rows = monitor(['person/project'], 'solar-autoresearch', api=Api(), since=15, until=25)
    assert [row['workspace'] for row in rows] == ['b']
    assert rows[0]['step'] == 'Research agent'
    assert rows[0]['last_update'] == '1970-01-01 00:00:20 UTC'
    rows = monitor(['person/project'], 'solar-autoresearch', api=Api(), workspace='c', session='copy-a')
    assert rows[0]['last_update'] == 'Unknown'
    assert rows[0]['status'] == 'complete'
    assert monitor(['person/project'], 'solar-autoresearch', api=Api(), session='other')[0]['status'] == 'unknown'


def test_monitor_reads_independent_projects_concurrently():
    barrier = threading.Barrier(2)
    class Api:
        def runs(self, project, filters):
            barrier.wait(timeout=3)
            return []
    rows = monitor(['a/one', 'b/two'], 'solar-autoresearch', api=Api(), max_workers=2)
    assert [row['project'] for row in rows] == ['a/one', 'b/two']
    assert all(row['status'] == 'unknown' for row in rows)


def test_image_and_measurement_persistence_report_links_do_not_collide():
    links = {}
    for name in ('solar-images-final', 'solar-measurements-final'):
        links.update(ui.comparison_links({'persistence': {'run': 'https://example.test/' + name,
            'dataset': 'weave:///person/project/object/' + name + '-persistence-cases:abc'}}))
    assert len(links) == 4
    assert len([label for label in links if 'Solar images' in label]) == 2
    assert len([label for label in links if 'GOES measurements' in label]) == 2


def test_latest_access_denial_is_visible_after_an_earlier_success(tmp_path):
    session = WorkshopSession('person/mine', 'starter', state_dir=tmp_path)
    setup.save_access(session, {'write_access': True})
    setup.save_access(session, {'write_access': False, 'error': 'No longer allowed'})
    with session.transaction() as state:
        state['requests'] = {'old': {'status': 'complete', 'http_status': 200, 'ended_at': 1},
                             'new': {'status': 'failed', 'http_status': 403, 'ended_at': 2}}
    rows = {row['Capability']: row for row in setup.capabilities(session)}
    assert rows['Project writes']['Status'] == 'Access needs attention'
    assert rows['Inference']['Status'] == 'Latest request denied access'
