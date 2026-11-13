from forge_workshop_kit import WorkshopSession, ui


def test_drafts_and_navigation_survive_without_executing(tmp_path):
    class NoRemote:
        def __getattr__(self, name):
            raise AssertionError('Draft editing must not contact Forge: ' + name)
    session = WorkshopSession('learner/research', 'solar-autoresearch', state_dir=tmp_path,
                              publisher=NoRemote())
    session.save_draft('measurement', 'def model(): return 1')
    session.save_draft('image', 'def model(): return 2')
    session.set_view('images')
    again = WorkshopSession('learner/research', 'solar-autoresearch', state_dir=tmp_path)
    assert again.get_draft('measurement') == 'def model(): return 1'
    assert again.get_draft('image') == 'def model(): return 2'
    assert again.get_view() == 'images'
    assert again.read()['stages'] == {}
    assert again.read()['requests'] == {}
    assert again.read()['progress'] == {}
    assert again.state_path in again.export_files()


def test_result_links_survive_restore_and_escape_source(tmp_path):
    session = WorkshopSession('learner/research', 'test', state_dir=tmp_path)
    with session.stage('images/round-1/compose', sources={'candidate.py': '<script>bad</script>'}) as stage:
        stage.record({'decision': {'decision': 'KEEP', 'title': 'Keep <script>',
                                  'rationale': 'Measured validation did not improve.'}})
    with session.transaction() as state:
        state['publications']['trace/' + stage.id] = {
            'url': 'https://forge.coreweave.com/example', 'verified': True}
        state['stages'][stage.id]['published'] = 'https://wandb.ai/learner/research/runs/run'
    restored = WorkshopSession('learner/research', 'test', state_dir=tmp_path)
    assert len(ui.stage_links(restored, [stage.id])) == 2
    html = ui.branch_graph(restored)
    assert 'Retain this version' in html
    assert '<script>' not in html
    assert 'href="#branch-' + stage.id in html
    assert 'Measured validation did not improve.' in html
    assert 'javascript:' not in ui.links({'bad': 'javascript:alert(1)'})


def test_missing_results_are_not_successful_zero():
    html = ui.result('Final evaluation', {'error': None}, status='unavailable')
    assert 'Unavailable' in html
    assert 'data-status="unavailable"' in html
    assert 'Retain this version' in ui.diff('same', 'same')
    assert '&lt;script&gt;' in ui.diff('before', '<script>')


def test_span_links_require_stored_identity_and_keep_failed_events(tmp_path):
    session = WorkshopSession('learner/research', 'test', state_dir=tmp_path)
    with session.stage('round-1/probe') as stage:
        stage.record({'events': [{'id': 'event-1', 'name': 'read_state'},
                                 {'id': 'event-2', 'name': 'provision', 'error': 'timeout'},
                                 {'id': 'event-3', 'name': 'unexported'}]})
    with session.transaction() as state:
        state['publications']['trace/' + stage.id] = {
            'url': 'https://forge.coreweave.com/agent-lens/learner/research/conversations/c1',
            'verified': False, 'trace_id': 't1',
            'span_ids': {'event-1': 's1', 'event-2': 's2'}}
    assert ui.span_links(session, stage.id) == {}
    with session.transaction() as state:
        state['publications']['trace/' + stage.id]['verified'] = True
    links = ui.span_links(session, stage.id)
    assert len(links) == 2
    assert links['2 · provision · error'].endswith('/spans/turns/t1/spans/s2')


def test_pending_adoption_links_to_actual_execution_and_attributes_lesson(tmp_path):
    session = WorkshopSession('learner/office', 'test', state_dir=tmp_path)
    with session.stage('pending/round-1/composition-test-execution/case') as execution:
        execution.record({'harness_fingerprint': 'actual-harness', 'scores': {'task_success': True}})
    with session.transaction() as state:
        state['publications']['trace/' + execution.id] = {'verified': True,
            'url': 'https://forge.coreweave.com/agent-lens/learner/office/conversations/execution'}
    with session.stage('pending/round-1/adopted') as adopted:
        adopted.record({'execution': execution.id, 'lesson': 'Try this again',
                        'limits': 'One observed case', 'retained_parent': True})
    rendered = ui.branch_graph(session)
    assert 'actual-harness' in rendered
    assert 'Agent’s proposed lesson' in rendered
    assert 'Stated limits' in rendered
    assert '/conversations/execution' in rendered


def test_legacy_keep_selection_requires_matching_adopted_fingerprint():
    composition = {'name': 'pending/round-1/compose', 'status': 'complete',
                   'result': {'decision': 'KEEP', 'fingerprint': 'parent'}}
    adopted = {'name': 'pending/round-1/adopted',
               'result': {'retained_parent': False, 'fingerprint': 'parent'}}
    assert ui._retained_selection(adopted, [composition])
    adopted['result']['fingerprint'] = 'other'
    assert not ui._retained_selection(adopted, [composition])
