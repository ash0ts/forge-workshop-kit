from copy import deepcopy
from types import SimpleNamespace

from forge_workshop_kit import ui, visuals
from forge_workshop_kit.session import digest


def row(identity, name, result, *, status='complete', sources=None, inputs=None, time=1):
    return {'id': identity, 'name': name, 'result': result, 'status': status,
            'sources': sources or {}, 'source_fingerprint': digest(sources or {}),
            'inputs': inputs or {}, 'started_at': time}


def journal(*rows):
    return {'stages': {r['id']: r for r in rows}, 'publications': {}, 'requests': {}}


def node(state, key, group=0):
    return next(n for n in visuals.branch_records(state)[group]['nodes'] if n['key'] == key)


def test_contract_is_portable_and_cannot_be_mutated_by_a_view():
    value = visuals.contract()
    assert value['colors']['candidate_a'] != value['colors']['candidate_b']
    assert value['edges']['evidence']['dash'] == '6 5'
    assert value['edges']['code']['dash'] is None
    assert value['edges']['selection']['requires_record']
    value['labels']['keep'] = 'Changed'
    assert visuals.contract()['labels']['keep'] == 'Retain this version'


def test_proposed_candidates_are_not_executions_or_selections():
    source = 'def model(): return 1'
    proposal = row('p', 'images/round-1/propose', {'candidates': [
        {'title': 'Use a residual model', 'source': source, 'decision': 'CHANGE',
         'fingerprint': digest({'candidate.py': source})}]}, sources={'candidate.py': 'old'})
    state = journal(proposal)
    candidate = node(state, 'candidate-a')
    assert candidate['status'] == 'proposed'
    assert candidate['execution'] is None
    assert candidate['selected'] is False
    assert node(state, 'probe-a')['status'] == 'not_run'
    assert visuals.branch_records(state)[0]['edges'] == []
    assert [n['key'] for n in visuals.branch_records(state)[0]['nodes']] == [
        'proposal', 'candidate-a', 'probe-a', 'candidate-b', 'probe-b',
        'compose', 'composition-test', 'selection']


def test_solar_wrappers_resolve_real_training_and_reviewed_evidence_only():
    source = 'new'; fingerprint = digest({'candidate.py': source})
    proposal = row('p', 'images/round-1/propose', {'candidates': [
        {'source': source, 'fingerprint': fingerprint, 'decision': 'CHANGE'}]},
        sources={'candidate.py': 'old'})
    executed = row('e', 'images/round-1/probe-0', {'metrics': {'validation_error': .4}},
                   sources={'candidate.py': source})
    receipt = row('w', 'images/round-1/probe-result-0',
                  {'stage_id': 'e', 'source': source, 'metrics': {'validation_error': .4}})
    compose = row('c', 'images/round-1/compose', {'decision': {'source': source}},
                  inputs={'candidates': [{'stage_id': 'e'}]})
    state = journal(proposal, executed, receipt, compose)
    tested = node(state, 'probe-a')
    assert tested['execution']['id'] == 'e'
    assert tested['status'] == 'complete'
    assert tested['fingerprint_match'] is True
    kinds = [edge['kind'] for edge in visuals.branch_records(state)[0]['edges']]
    assert kinds == ['code', 'evidence']
    compose['inputs'] = {'files': ['results.json'], 'metrics': {'validation_error': .4}}
    assert [e['kind'] for e in visuals.branch_records(journal(proposal, executed, receipt, compose))[0]['edges']] == ['code']


def test_keep_can_be_tested_again_without_creating_a_new_version():
    composed = row('c', 'pending/round-1/compose', {'decision': 'KEEP', 'fingerprint': 'parent',
        'title': 'Keep the existing verification procedure', 'diff': ''})
    executed = row('e', 'pending/round-1/composition-test-execution/case',
                   {'harness_fingerprint': 'parent', 'scores': {'task_success': True}})
    probe = row('p', 'pending/round-1/composition-test', {'run': {'stage_id': 'e'}})
    adopted = row('a', 'pending/round-1/adopted', {'fingerprint': 'parent', 'execution': 'e',
                  'retained_parent': True})
    state = journal(composed, executed, probe, adopted)
    selected = node(state, 'selection')
    assert selected['retained'] and selected['selected']
    assert selected['execution']['id'] == 'e'
    assert selected['fingerprint_match'] is True
    assert selected['title'] == 'Retain this version'
    assert [e['kind'] for e in visuals.branch_records(state)[0]['edges']] == ['code', 'selection']


def test_failed_composition_does_not_become_evidence_for_selected_parent():
    executed = row('e', 'pending/round-1/composition-test-execution/case',
                   {'harness_fingerprint': 'new', 'scores': {}}, status='failed')
    selected = row('s', 'pending/round-1/adopted', {'fingerprint': 'parent',
        'execution': 'e', 'retained_parent': True, 'failure_fallback': True})
    state = journal(executed, selected)
    value = node(state, 'selection')
    assert value['selection_execution_mismatch'] is True
    assert value['execution']['metrics'] == {}
    assert not any(e['kind'] == 'selection' for e in visuals.branch_records(state)[0]['edges'])


def test_rounds_and_attempts_stay_separate_and_successful_retry_is_found():
    failed = row('f', 'images/round-1/propose', {}, status='failed')
    success = row('s', 'images/round-1/propose', {'candidates': [{'title': 'A'}]}, time=2)
    other = row('o', 'images/round-2/propose', {'candidates': [{'title': 'B'}]}, time=3)
    state = journal(failed, success, other)
    assert node(state, 'candidate-a')['title'] == 'A'
    assert node(state, 'candidate-a', 1)['title'] == 'B'
    assert [r['id'] for r in node(state, 'proposal')['attempts']] == ['f', 's']
    assert visuals.branch_records(state)[0]['other_records'][0]['id'] == 'f'


def test_workbench_is_read_only_accessible_and_escapes_authored_text():
    candidate = {'title': '<script>bad</script>', 'rationale': 'Review & compare',
                 'decision': 'CHANGE', 'source': '<script>source</script>'}
    state = journal(row('p', 'images/round-1/propose', {'candidates': [candidate]},
                        sources={'candidate.py': 'old'}))
    before = deepcopy(state)
    session = SimpleNamespace(project='learner/project', workspace_id='copy-1', read=lambda: state)
    html = ui.branch_workbench_html(session, key='test')
    assert 'type="radio"' in html and 'aria-controls=' in html
    assert ':checked~.wk-grid .wk-panel' in html
    assert 'No work runs when you select a step.' in html
    assert '<script>' not in html and '&lt;script&gt;' in html
    assert 'No Forge link is saved' in html
    assert '<form' not in html and '<script' not in html
    assert ui.branch_workbench(SimpleNamespace(Html=lambda x: x), session, key='test') == html
    assert state == before
    session.workspace_id = 'copy-2'
    assert ui.branch_workbench_html(session, key='test') != html


def test_trace_link_is_taken_from_saved_receipt_not_constructed_from_stage_id():
    state = journal(row('p', 'pending/round-1/propose', {'candidates': [{'title': 'A'}]}))
    state['publications']['trace/p'] = {'url': 'https://forge.coreweave.com/exact-recorded-child',
                                       'verified': False}
    session = SimpleNamespace(project='learner/project', workspace_id='copy', read=lambda: state)
    html = ui.branch_workbench_html(session)
    assert 'exact-recorded-child' in html
    assert 'upload not yet verified' in html
    assert '/conversations/p' not in html


def test_incomplete_restore_with_only_review_record_stays_inspectable():
    state = journal(row('review', 'images/round-1/review-0', {'reviewed_fingerprint': 'saved'}))
    session = SimpleNamespace(project='learner/project', workspace_id='copy', read=lambda: state)
    html = ui.branch_workbench_html(session)
    assert 'This step has no saved result yet.' in html
    assert 'Reviews and other saved events' in html
    assert 'review' in html
