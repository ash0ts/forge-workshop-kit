import json
from types import SimpleNamespace

import marimo as mo
import pytest

from forge_workshop_kit import WorkshopSession, aria
from forge_workshop_kit.manifest import list_workshops
from forge_workshop_kit.monitoring import monitor


def session(tmp_path, workshop='banking-routing', project='participant/research'):
    return WorkshopSession(project, workshop, state_dir=tmp_path)


def recorded(s, name, result=None, **kwargs):
    with s.stage(name, **kwargs) as stage:
        if stage.needs_run:
            stage.record(result or {'metrics': {'error': .2}})
    return stage.id


@pytest.mark.parametrize('workshop', list_workshops(), ids=lambda w: w['slug'])
def test_two_stops_preserve_workshop_steps_and_have_exact_duration(workshop):
    stops = workshop['aria_investigations']
    assert [s['id'] for s in stops] == ['investigate', 'conclusion']
    assert [s['minutes'] for s in stops] == [8, 7]
    for stop in stops:
        assert stop['step'] in dict(workshop['steps'])
        assert stop['allowed_stage_patterns']
        assert stop['recorded_example'] == f"aria/{workshop['slug']}/{stop['id']}.json"
        assert stop['deck_anchor'] == 'aria-' + stop['id']


def test_context_has_no_side_effects_and_uses_completed_tfidf_without_embeddings(tmp_path, monkeypatch):
    s = session(tmp_path)
    identity = recorded(s, 'routing/baseline/tfidf', inputs={'split': 'validation'}, sources={'classifier.py':'source'})
    recorded(s, 'routing/final/selected', {'metrics': {'SECRET_FINAL_SCORE': .99}})
    before = s.read()
    monkeypatch.setattr(s, 'transaction', lambda: pytest.fail('Rendering must not save'))
    monkeypatch.setattr(s, 'connect', lambda: pytest.fail('Rendering must not connect'))
    context = aria.build_aria_context(s, 'investigate')
    assert [r['identity'] for r in context['records']] == [identity]
    assert 'SECRET_FINAL_SCORE' not in context['prompt']
    assert context['aria_access'] == 'unverified'
    assert s.read() == before
    assert aria.build_aria_context(s, 'investigate', [])['records'] == []


@pytest.mark.parametrize('location', ['inputs', 'config', 'result'])
def test_early_context_rejects_nested_reserved_values(tmp_path, location):
    s = session(tmp_path, 'solar-autoresearch')
    kwargs = {location: {'nested': [{'partition': 'test', 'secret': 'do-not-use'}]}}
    identity = recorded(s, 'goes/search-0', **kwargs)
    assert aria.eligible_record_ids(s, 'investigate') == []
    with pytest.raises(ValueError, match='permitted stages'):
        aria.build_aria_context(s, 'investigate', [identity])


def test_explicit_identity_must_belong_to_current_workspace(tmp_path):
    s = session(tmp_path / 'one')
    other = session(tmp_path / 'other', project='somebody/else')
    identity = recorded(other, 'routing/baseline/tfidf')
    with pytest.raises(ValueError):
        aria.build_aria_context(s, 'investigate', [identity])
    identity = recorded(s, 'routing/baseline/tfidf')
    with s.transaction() as state:
        state['stages'][identity]['project'] = 'somebody/else'
    with pytest.raises(ValueError):
        aria.build_aria_context(s, 'investigate', [identity])


def test_early_solar_context_excludes_worked_repair_and_final_without_hiding_failure(tmp_path):
    s = session(tmp_path, 'solar-autoresearch')
    baseline = recorded(s, 'goes/persistence', {'metrics': {'error': .19}})
    trained = recorded(s, 'goes/search-0', {'metrics': {'error': 2.46}})
    recorded(s, 'goes/worked-repair', {'metrics': {'error': .1}})
    final = recorded(s, 'goes/final', {'metrics': {'error': 1.2}}, inputs={'split': 'test'})
    assert aria.eligible_record_ids(s, 'investigate') == [baseline, trained]
    assert '2.46' in aria.build_aria_context(s, 'investigate')['prompt']
    assert aria.eligible_record_ids(s, 'conclusion') == [final]


def test_publication_links_are_separate_verified_and_same_project(tmp_path):
    s = session(tmp_path)
    identity = recorded(s, 'routing/baseline/tfidf')
    assert aria.build_aria_context(s, 'investigate')['records'][0]['publication_status'] == 'not published'
    with s.transaction() as state:
        row = state['stages'][identity]
        row['published'] = 'https://wandb.ai/participant/research/runs/' + identity
        row['artifact_url'] = 'https://wandb.ai/wrong/project/artifacts/secret'
        state['publications']['trace/' + identity] = {'url':'https://forge.coreweave.com/agent-lens/participant/research/conversations/abc','verified':False}
    context = aria.build_aria_context(s, 'investigate')
    assert len(context['records'][0]['links']) == 1
    assert 'wrong/project' not in context['prompt']
    assert '/conversations/abc' not in context['prompt']
    with s.transaction() as state:
        state['publications']['trace/' + identity]['verified'] = True
    assert len(aria.build_aria_context(s, 'investigate')['records'][0]['links']) == 2


def test_airline_review_and_its_discovery_turn_allowed_but_monitoring_and_final_are_not(tmp_path):
    s = session(tmp_path, 'airline-monitoring')
    case = recorded(s, 'airline/baseline/airline-discovery-01', {'case_id':'airline-discovery-01','split':'discovery'})
    review = recorded(s, 'airline/review/' + case + '/trace-a', {'reason':'Return flight preserved','human_label':False})
    recorded(s, 'airline/baseline/airline-final-01', {'case_id':'airline-final-01','split':'final'})
    recorded(s, 'airline/baseline/airline-monitoring-01', {'case_id':'airline-monitoring-01','split':'monitoring'})
    context = aria.build_aria_context(s, 'investigate', [case, review])
    assert len(context['records']) == 2
    assert len(aria.eligible_record_ids(s, 'investigate')) == 2
    assert 'Return flight preserved' in context['prompt']


def test_case_selection_is_bound_to_saved_check_and_resumes(tmp_path, monkeypatch):
    s = session(tmp_path)
    identity = recorded(s, 'routing/baseline/tfidf')
    context = aria.build_aria_context(s, 'investigate', [identity], case_ids=['validation-12'])
    monkeypatch.setattr(s, 'queue_progress', lambda: pytest.fail('Saving does not publish'))
    note = aria.save_note(s, context, mode='live', claim='The class probability is not the intent name.',
        assessment='supported', record_url='https://wandb.ai/participant/research/runs/' + identity,
        reason='The selected row has the stated probability.', interpretation='Initial reasoning')
    assert note['case_ids'] == ['validation-12']
    assert aria.report_notes(s) == []
    assert s.read()['progress']['aria_investigations']['investigate'] == {
        'mode':'live','citation_checked':True,'help_requested':False,'updated_at':note['saved_at']}
    assert s.read()['stages'][identity]['status'] == 'complete'
    assert 'completed' not in s.read()['progress']
    reopened = session(tmp_path)
    assert reopened.get_draft('aria/note/investigate/' + context['id']) == note
    other = aria.build_aria_context(s, 'investigate', [identity], case_ids=['validation-13'])
    assert other['id'] != context['id']
    assert reopened.get_draft('aria/note/investigate/' + other['id']) is None


def test_saved_notes_do_not_enter_measured_inputs_and_report_is_opt_in(tmp_path):
    s = session(tmp_path)
    recorded(s, 'routing/baseline/tfidf')
    before = s.read()['stages']
    context = aria.build_aria_context(s, 'investigate')
    kwargs = {'mode': 'live', 'claim': 'Checked claim', 'assessment': 'unresolved', 'record_url': '',
        'reason': 'Access unavailable', 'prompt': 'Private chat instruction must not enter report'}
    aria.save_note(s, context, **kwargs, include_in_report=True)
    notes = aria.report_notes(s)
    assert notes[0]['reason'] == 'Access unavailable'
    assert 'Private chat' not in json.dumps(notes)
    assert s.read()['stages'] == before
    aria.save_note(s, context, **kwargs, include_in_report=False)
    assert aria.report_notes(s) == []


def test_recorded_mode_requires_actual_recording_and_never_substitutes_participant_results(tmp_path, monkeypatch):
    s = session(tmp_path)
    context = aria.build_aria_context(s, 'investigate', [])
    monkeypatch.setattr(aria, 'recorded_investigation', lambda *a: {'status':'unavailable'})
    with pytest.raises(ValueError, match='recorded investigation is unavailable'):
        aria.save_note(s, context, mode='recorded', claim='x', assessment='unresolved', record_url='')
    monkeypatch.setattr(aria, 'recorded_investigation', lambda *a: {'status':'recorded','id':'teacher-recording'})
    note = aria.save_note(s, context, mode='recorded', claim='x', assessment='unresolved', record_url='')
    assert note['mode'] == 'recorded' and note['recorded_example_id'] == 'teacher-recording'
    assert note['record_ids'] == []
    with pytest.raises(ValueError, match='completed participant result'):
        aria.save_note(s, context, mode='live', claim='x', assessment='unresolved', record_url='')


def test_card_is_bound_composite_and_can_show_fallback_before_authentication(tmp_path, monkeypatch):
    monkeypatch.setattr(aria,'recorded_investigation',lambda *a:{'status':'unavailable'})
    card = aria.investigation(mo, None, 'investigate', workshop='banking-routing')
    assert isinstance(card, mo.ui.batch)
    assert 'Use the recorded investigation' in card.text
    assert 'ARIA access is unverified' in card.text
    assert 'No completed participant evidence' in card.text
    s = session(tmp_path)
    recorded(s, 'routing/baseline/tfidf')
    before = s.read()
    aria.investigation(mo,s,'investigate')
    assert s.read() == before


def test_monitor_exposes_small_summary_without_private_notes():
    row = SimpleNamespace(config={'workspace_id':'copy-a'},url='https://wandb.ai/person/project/runs/p',
        summary={'aria_investigations':{'investigate':{'mode':'recorded','citation_checked':True,'help_requested':False}},'updated_at':100})
    api = SimpleNamespace(runs=lambda *a,**k:[row])
    result = monitor(['person/project'],'banking-routing',api=api)
    assert result[0]['aria_investigations']['investigate']['mode'] == 'recorded'
    assert 'prompt' not in result[0]['aria_investigations']


def test_recorded_prompt_json_braces_render_literally(monkeypatch):
    monkeypatch.setattr(aria, 'recorded_investigation', lambda *a: {
        'status':'recorded','prompt':'Inspect {"event": "read_skill"}',
        'response':'The result was {"text": "Skill not installed"}.',
        'records':[{'label':'Source','url':'https://wandb.ai/teacher/project/runs/source'}],
        'citation_check':{'claim':'Skill not loaded','assessment':'supported','reason':'Actual returned text','record_url':''}})
    card = aria.investigation(mo,None,'investigate',workshop='pending-direct-teaching')
    assert 'read_skill' in card.text and 'Skill not installed' in card.text


def test_development_excerpt_preserves_tool_results_without_messages(tmp_path):
    s = session(tmp_path, 'pending-direct-teaching')
    recorded(s,'pending/original/double-charge',{'mission':'Refund only duplicate pay-2', 'split':'development',
        'messages':[{'role':'system','content':'DO_NOT_INCLUDE_MODEL_CONTEXT'}],
        'world':{'refunds':[{'payment':'pay-2'}]},
        'events':[{'id':'tool-0','name':'read_skill','arguments':{'name':'lookup_invoice'},'result':{'text':'Skill not installed'}}]})
    prompt=aria.build_aria_context(s,'investigate')['prompt']
    assert 'Skill not installed' in prompt and 'pay-2' in prompt
    assert 'DO_NOT_INCLUDE_MODEL_CONTEXT' not in prompt


def test_routing_early_context_selects_validation_row_even_with_saved_review_pool(tmp_path):
    s = session(tmp_path)
    recorded(s,'routing/baseline/tfidf',{'validation':[{'case_id':'v1','split':'validation','prediction':'card_arrival'},{'case_id':'v2','split':'validation','prediction':'cash_withdrawal'}],
        'review':[{'case_id':'r1','split':'review','text':'REVIEW_CONTROL'}]})
    prompt=aria.build_aria_context(s,'investigate',case_ids=['v1'])['prompt']
    assert 'card_arrival' in prompt
    assert 'cash_withdrawal' not in prompt and 'REVIEW_CONTROL' not in prompt


def test_one_edited_prompt_supplies_the_saved_interpretation():
    prompt = 'Question\n\nMy interpretation: The refund completed, but the skill was not loaded.\n\nUse only the selected evidence.'
    assert aria._interpretation_from_prompt(prompt) == 'The refund completed, but the skill was not loaded.'
    assert aria._interpretation_from_prompt('No interpretation line') == ''


@pytest.mark.parametrize('workshop,names', [
    ('pending-direct-teaching', ('pending/original/double-charge', 'pending/final-comparison')),
    ('solar-autoresearch', ('goes/search-0', 'images/final-comparison')),
    ('banking-routing', ('routing/baseline/tfidf', 'routing/release/rollback')),
    ('visual-inspection', ('compare/whole', 'evaluate')),
    ('transit-factory', ('factory/integration/team', 'factory/evaluate/team')),
    ('airline-monitoring', ('airline/baseline/discovery-1', 'airline/subsequent-agreement')),
])
@pytest.mark.parametrize('mode', ['live', 'recorded'])
def test_all_twelve_stops_save_locally_without_execution_or_publication(tmp_path, monkeypatch, workshop, names, mode):
    s = session(tmp_path, workshop)
    identities = [recorded(s, name) for name in names]
    before = s.read()
    monkeypatch.setattr(s, 'connect', lambda: pytest.fail('Citation notes must stay offline'))
    monkeypatch.setattr(s, 'checkpoint', lambda *a, **kw: pytest.fail('No automatic checkpoint'))
    monkeypatch.setattr(aria, 'recorded_investigation', lambda *a: {'status':'recorded', 'id':'qualified-recording'})
    for stop, identity in zip(('investigate', 'conclusion'), identities):
        context = aria.build_aria_context(s, stop, [identity])
        aria.save_note(s, context, mode=mode, claim='The exact evidence still needs checking.',
                      record_url='', assessment='unresolved')
    after = s.read()
    for key in ('requests', 'stages', 'publications'):
        assert after.get(key) == before.get(key)
    assert set(after['progress']['aria_investigations']) == {'investigate', 'conclusion'}
    assert len([key for key in after['drafts'] if key.startswith('aria/note/')]) == 2


def test_requested_case_without_saved_values_is_explicitly_unavailable(tmp_path):
    s = session(tmp_path)
    recorded(s, 'routing/baseline/tfidf', {'validation':[{'case_id':'saved-case','prediction':'card_arrival'}]})
    context = aria.build_aria_context(s, 'investigate', case_ids=['missing-case'])
    assert context['case_status']['missing-case'] == 'per-case values unavailable in selected saved records'
    assert 'missing-case: per-case values unavailable' in context['prompt']
    assert 'card_arrival' not in context['prompt']
    pending = session(tmp_path / 'pending', 'pending-direct-teaching')
    recorded(pending, 'pending/original/double-charge', {'case_id':'double-charge'})
    assert aria.build_aria_context(pending, 'investigate', case_ids=['double-charge'])['case_status']['double-charge'] == 'available'


def test_native_links_cannot_escape_the_selected_project():
    assert aria._project_url('https://forge.coreweave.com/agent-lens/person/project/conversations/id','person/project')
    for url in ('https://forge.coreweave.com/person/project/../private',
                'https://forge.coreweave.com/person/project/%2e%2e/private',
                'https://user:secret@forge.coreweave.com/person/project/runs/id',
                'https://forge.coreweave.com:8080/person/project/runs/id',
                'https://forge.coreweave.com/person/project-other/runs/id'):
        assert not aria._project_url(url, 'person/project')
