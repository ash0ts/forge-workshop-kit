import copy
import json

import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.pending import loop, teaching
from forge_workshop_kit.pending.cases import CASES
from forge_workshop_kit.pending.harness import Harness
from forge_workshop_kit.session import digest


def learner(session):
    for name in ('tool','loop','scorer'):
        session.save_draft('pending/'+name,teaching.ANSWERS[name])
    return teaching.functions(session)


def test_free_checks_require_the_actual_missing_behaviors(tmp_path):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    f=learner(s)
    assert len(teaching.check_tool(f['my_invoice_tool']))==3
    assert teaching.check_loop(f['my_dispatch'],f['my_observation'],f['my_invoice_tool'])['next_request'][-1]['role']=='user'
    assert len(teaching.check_scorer(f['my_state_check'],f['my_judge_validation']))==4
    with pytest.raises(NotImplementedError):
        teaching.check_tool(teaching.compile_code(teaching.STARTERS['tool'])['my_invoice_tool'])
    broken=teaching.compile_code('def my_observation(messages, action, result):\n    return messages\n')['my_observation']
    with pytest.raises(AssertionError,match='Append action'):
        teaching.check_loop(f['my_dispatch'],broken,f['my_invoice_tool'])


def test_check_receipts_restore_and_edited_source_invalidates_pass(tmp_path):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    learner(s)
    sources={'lookup_invoice.py':s.get_draft('pending/tool'),'loop.py':s.get_draft('pending/loop')}
    assert teaching.check_status(s,'loop')['state']=='Not checked'
    with s.stage('pending/check-loop',sources=sources) as stage:
        stage.record({'next_request':[{'role':'user','content':'actual observation'}]})
    assert teaching.restore(s)['checks']['loop']['passed']
    changed={**sources,'loop.py':sources['loop.py']+'\n# edited\n'}
    assert not teaching.check_status(s,'loop',changed)['passed']
    assert teaching.check_status(s,'loop',changed)['state']=='Code changed; run the check again'
    s.save_draft('pending/loop',changed['loop.py'])
    assert not teaching.restore(s)['checks']['loop']['passed']


def test_learner_handoff_reaches_next_real_request_and_writers_are_used(tmp_path,monkeypatch):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    f=learner(s)
    teaching.freeze_runtime(s,f)
    requests=[]
    actions=iter([{'action':'lookup_invoice','arguments':{'account_id':'acme','invoice_id':'inv-1'}},
                  {'action':'finish','arguments':{'resolution':'needs_clarification','summary':'Need a decision.'}}])
    def complete(self,identity,messages,**kwargs):
        requests.append(copy.deepcopy(messages))
        return next(actions)
    monkeypatch.setattr(loop.Provider,'complete',complete)
    monkeypatch.setattr(loop,'output',lambda value:value)
    writers=[]
    def export(*args,**kwargs):
        writers.append(kwargs)
        return {'verified':True,'url':'https://forge.example/conversation'}
    monkeypatch.setattr(loop,'export_trace',export)
    case=next(c for c in CASES if c.id=='double-charge')
    run=loop.run_employee(s,case,Harness(),'starting',**teaching.hooks(f))
    assert len(requests)==2
    assert json.dumps(run['events'][0]['result']) in requests[1][-1]['content']
    assert writers[0]['tool_writer'] is f['my_tool_span']
    assert writers[0]['model_writer'] is f['my_model_span']
    assert run['runtime_fingerprint']==teaching.saved(s,'pending/runtime')['fingerprint']
    assert run['instrumentation_fingerprint']==digest(loop.instrumentation_sources(f['my_tool_span'],f['my_model_span']))
    # Revisiting the same execution may retry export, but never requests another model response.
    loop.run_employee(s,case,Harness(),'starting',**teaching.hooks(f))
    assert len(requests)==2
    changed=teaching.compile_code(teaching.ANSWERS['loop'].replace('Tool observation: ','Actual observation: '))
    with pytest.raises(ValueError,match='executor changed'):
        loop.run_employee(s,case,Harness(),'manual',**{**teaching.hooks(f),'append':changed['my_observation']})


def test_resume_keeps_trace_links_final_results_and_missing_judgments(tmp_path):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    h=Harness()
    run={'case_id':'double-charge','harness':__import__('dataclasses').asdict(h),
         'harness_fingerprint':h.fingerprint,'status':'complete','events':[],
         'mission':'Fix it','draft':{},'scores':{'task_success':True}}
    with s.stage('pending/original/double-charge') as stage:
        stage.record(run)
    with s.transaction() as state:
        state['publications']['trace/'+stage.id]={'verified':True,'url':'https://forge.example/actual-trace'}
    with s.stage('pending/final-comparison') as final:
        final.record({'runs':{'starting':[{**run,'stage_id':stage.id,'trace':{'url':'https://forge.example/actual-trace'},'explanation_judgment':{'status':'unavailable'}}]},'rows':{}})
    restored=teaching.restore(s)
    assert restored['original'][0]['trace']['url'].endswith('actual-trace')
    rows=teaching.comparison_rows(restored['final']['runs'])['starting']
    assert rows[0]['scores']=={'grounded':None,'complete':None}
    assert rows[0]['error']==0


def test_reviews_bind_to_decision_and_split_probes_keep_progress(tmp_path):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    h=Harness()
    decision={'decision':'KEEP','harness':__import__('dataclasses').asdict(h),'fingerprint':h.fingerprint,'rationale':'The probe recovered.'}
    key=teaching.review_decision(s,decision)
    assert teaching.saved(s,'pending/review/'+key)['fingerprint']==h.fingerprint
    with pytest.raises(ValueError,match='fingerprint'):
        teaching.review_decision(s,{**decision,'fingerprint':'wrong'})
    with s.stage('pending/round-1/propose') as stage:
        stage.record({'candidates':[decision,decision]})
    assert teaching.next_phase(s)[1]=='probe-a'
    with s.stage('pending/round-1/probe-a') as stage: stage.record({'run':{}})
    assert teaching.next_phase(s)[1]=='probe-b'
    assert teaching.active_decision(s,1,'probe-b')==decision


def test_judge_calls_learner_validation_and_rejects_invalid_output(tmp_path,monkeypatch):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    called=[]
    def custom_validation(value):
        called.append(value)
        raise ValueError('The participant rejects this answer')
    monkeypatch.setattr(loop.Provider,'complete',lambda *args,**kwargs:{'grounded':'yes','complete':True,'reason':'No evidence'})
    monkeypatch.setattr(loop,'output',lambda value:value)
    with pytest.raises(ValueError,match='participant rejects'):
        loop.judge_explanation(s,{'stage_id':'execution','mission':'Do work','events':[],'draft':{}},'Use evidence',validate=custom_validation)
    assert len(called)==1
    assert next(iter(s.read()['stages'].values()))['status']=='failed'


def test_reflection_rejects_final_evidence_without_provider(tmp_path):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    with pytest.raises(ValueError,match='Final cases'):
        loop.reflect_execution(s,1,{'split':'heldout'})
    assert not s.read()['requests']


def test_judge_trace_includes_request_keyed_by_exact_stage_id(tmp_path,monkeypatch):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    answer={'grounded':True,'complete':True,'reason':'The actions support the explanation.'}
    def complete(self,identity,*args,**kwargs):
        with s.transaction() as state:
            state['requests'][identity]={'id':identity,'started_at':1,'ended_at':2}
        return answer
    captured=[]
    monkeypatch.setattr(loop.Provider,'complete',complete)
    monkeypatch.setattr(loop,'output',lambda value:value)
    monkeypatch.setattr(loop,'export_trace',lambda session,identity,mission,events,requests,**kwargs:captured.extend(requests) or {})
    loop.judge_explanation(s,{'stage_id':'execution','mission':'Do work','events':[],'draft':{}},'Use evidence')
    assert len(captured)==1
    assert captured[0]['id']==next(iter(s.read()['stages']))


def test_mcp_bridge_runs_inside_notebook_event_loop(tmp_path):
    import asyncio
    case=next(c for c in CASES if c.id=='missing-seat')
    async def notebook_cell():
        world,result=loop.call_mcp(case.initial,case.fault,'discover_onboarding',{},tmp_path/'office.json')
        assert any(t['name']=='provision_member' for t in result['tools'])
        assert world==case.initial
    asyncio.run(notebook_cell())


def test_explicit_retry_preserves_failed_attempt_and_reuses_completed(tmp_path,monkeypatch):
    from forge_workshop_kit.session import StageNeedsReview
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    f=learner(s)
    calls=[]
    def complete(*args,**kwargs):
        calls.append(1)
        if len(calls)==1: raise RuntimeError('temporary runtime failure')
        return {'action':'finish','arguments':{'resolution':'needs_clarification','summary':'No change.'}}
    monkeypatch.setattr(loop.Provider,'complete',complete)
    monkeypatch.setattr(loop,'output',lambda x:x)
    monkeypatch.setattr(loop,'export_trace',lambda *a,**kw:{})
    case=next(c for c in CASES if c.id=='double-charge')
    with pytest.raises(RuntimeError,match='temporary runtime'):
        loop.run_employee(s,case,Harness(),'original',**teaching.hooks(f))
    with pytest.raises(StageNeedsReview):
        loop.run_employee(s,case,Harness(),'original',**teaching.hooks(f))
    loop.run_employee(s,case,Harness(),'original',retry_failed=True,**teaching.hooks(f))
    loop.run_employee(s,case,Harness(),'original',retry_failed=True,**teaching.hooks(f))
    assert len(calls)==2
    assert [(r['attempt'],r['status']) for r in s.read()['stages'].values()]==[(1,'failed'),(2,'complete')]


def test_editor_and_reflection_prompts_keep_mission_and_separate_prior_experience(tmp_path,monkeypatch):
    from dataclasses import asdict
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    h=Harness()
    run={'split':'development','case_id':'missing-seat','mission':'Provision the explicitly requested member.',
         'stage_id':'current-execution','events':[],'draft':{},'status':'complete',
         'harness':asdict(h),'harness_fingerprint':h.fingerprint,'scores':{'SECRET_GRADE':True},
         'prior_experience':{'source_execution':'earlier-billing-execution','case_id':'double-charge',
                             'lesson':'Read back writes.','limits':'Only one earlier case.', 'SECRET_GRADE':'excluded'}}
    context=loop.editor_context(h,[run])
    assert context['current_executions'][0]['mission']==run['mission']
    assert 'prior_experience' not in context['current_executions'][0]
    assert context['prior_experience'][0]['source_execution']=='earlier-billing-execution'
    assert 'SECRET_GRADE' not in json.dumps(context)
    calls=[]
    def validated(session,identity,messages,validate,**kwargs):
        calls.append(messages)
        decision={'decision':'KEEP','title':'Retain the tested harness','rationale':'No supported change.', 'harness':asdict(h)}
        value={'candidates':[decision.copy(),decision.copy()]} if len(calls)==1 else {'lesson':'Read the result.','limits':'One development execution.'}
        validate(value)
        return value,{}
    monkeypatch.setattr(loop,'validated_json',validated)
    monkeypatch.setattr(loop,'export_trace',lambda *a,**kw:{})
    loop.editor_decision(s,2,'propose',h,[run])
    loop.reflect_execution(s,2,run)
    assert 'same starting execution' in calls[0][0]['content']
    assert 'Office rules' in calls[1][0]['content']
    assert json.loads(calls[1][1]['content'])['mission']==run['mission']
    assert all('SECRET_GRADE' not in json.dumps(messages) for messages in calls)
    for row in s.completed():
        assert row['inputs']['prompt_version']==2
        assert any(path.endswith('-system.txt') for path in row['sources'])
    with pytest.raises(ValueError,match='Final cases'):
        loop.editor_context(h,[{**run,'split':'heldout'}])


def test_judge_retry_is_explicit_bounded_and_reuses_success(tmp_path, monkeypatch):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    run={'stage_id':'saved-execution','mission':'Do work','events':[],'draft':{}}
    calls=[]
    answer={'grounded':True,'complete':True,'reason':'Recorded actions support the explanation.'}
    def complete(self, identity, *args, **kwargs):
        calls.append(identity)
        if len(calls)==1: raise ValueError('Incomplete response: output limit reached.')
        return answer
    monkeypatch.setattr(loop.Provider,'complete',complete)
    monkeypatch.setattr(loop,'output',lambda value:value)
    monkeypatch.setattr(loop,'export_trace',lambda *args,**kwargs:{'verified':True})
    with pytest.raises(ValueError,match='output limit'):
        loop.judge_explanation(s,run,'Use evidence')
    with pytest.raises(RuntimeError):
        loop.judge_explanation(s,run,'Use evidence')
    assert len(calls)==1
    result=loop.judge_explanation(s,run,'Use evidence',retry_failed=True)
    assert result['grounded']
    assert len(calls)==2
    assert [row['status'] for row in s.read()['stages'].values()]==['failed','complete']
    loop.judge_explanation(s,run,'Use evidence',retry_failed=True)
    assert len(calls)==2
    assert all(row['name'].startswith('pending/judge/') for row in s.read()['stages'].values())


def test_judge_retry_stops_after_second_failed_attempt(tmp_path,monkeypatch):
    s=WorkshopSession('user/project','teaching',state_dir=tmp_path)
    calls=[]
    def fail(self,identity,*args,**kwargs):
        calls.append(identity)
        raise ValueError('output limit')
    monkeypatch.setattr(loop.Provider,'complete',fail)
    monkeypatch.setattr(loop,'export_trace',lambda *args,**kwargs:{'verified':True})
    run={'stage_id':'saved-execution','mission':'Do work','events':[],'draft':{}}
    for retry in (False,True):
        with pytest.raises(ValueError,match='output limit'):
            loop.judge_explanation(s,run,'Use evidence',retry_failed=retry)
    with pytest.raises(ValueError,match='Two explanation-judge attempts failed'):
        loop.judge_explanation(s,run,'Use evidence',retry_failed=True)
    assert len(calls)==2


def test_raised_mcp_error_has_a_durable_event_before_propagation(tmp_path, monkeypatch):
    s = WorkshopSession('user/project', 'teaching', state_dir=tmp_path)
    f = learner(s)
    action = {'action': 'onboarding_status', 'arguments': {'account_id': 'fern'}}
    monkeypatch.setattr(loop.Provider, 'complete', lambda *args, **kwargs: action)
    monkeypatch.setattr(loop, 'output', lambda value: value)
    def unavailable(*args, **kwargs):
        raise ConnectionError('MCP process stopped')
    monkeypatch.setattr(loop, 'call_mcp', unavailable)
    exported = []
    monkeypatch.setattr(loop, 'export_trace', lambda session, identity, mission, events, *args, **kwargs: exported.extend(events) or {})
    case = next(c for c in CASES if c.id == 'missing-seat')
    with pytest.raises(ConnectionError, match='MCP process stopped'):
        loop.run_employee(s, case, Harness(), 'starting', **teaching.hooks(f))
    failed = next(row for row in s.read()['stages'].values() if row['status'] == 'failed')
    event = failed['events'][0]
    assert event['name'] == 'onboarding_status'
    assert event['arguments'] == action['arguments']
    assert event['result'] is None and event['error_type'] == 'ConnectionError'
    assert event['ended_at'] >= event['started_at']
    assert exported == [event]
    assert any(path.endswith('/partial.json') for path in failed['files'])
