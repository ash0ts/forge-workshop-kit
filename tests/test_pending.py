import asyncio
from forge_workshop_kit.pending.cases import CASES
from forge_workshop_kit.pending.loop import mcp_action
from forge_workshop_kit.pending.simulator import execute
from forge_workshop_kit.pending.grading import grade


def test_timeout_committed_and_replayed_once(tmp_path):
    task=next(c for c in CASES if c.id=='missing-seat')
    arguments=dict(account_id='fern',email='alex@example.test',role='member',operation_id='join-alex')
    world,first=asyncio.run(mcp_action(task.initial,task.fault,'provision_member',arguments,tmp_path/'state.json'))
    assert first['error']=='timeout'
    assert len(world['accounts']['fern']['members'])==1
    world,second=asyncio.run(mcp_action(world,task.fault,'provision_member',arguments,tmp_path/'state.json'))
    assert second['replayed'] and len(world['accounts']['fern']['members'])==1
    run={'status':'complete','world':world,'draft':{'resolution':'resolved'}}
    assert grade(task,run)['task_success']


def test_duplicate_refunds_fail_independent_grading():
    task=next(c for c in CASES if c.id=='double-charge')
    world=task.initial
    for operation in ('refund-1','refund-2'):
        world,_=execute(world,'refund_payment',dict(account_id='acme',payment_id='pay-2',operation_id=operation))
    assert not grade(task,{'status':'complete','world':world,'draft':{'resolution':'resolved'}})['task_success']


def test_read_retry_is_recorded_and_bounded(tmp_path, monkeypatch):
    import forge_workshop_kit.pending.loop as loop
    from forge_workshop_kit import WorkshopSession
    from forge_workshop_kit.pending.harness import Harness
    actions=iter([{'action':'lookup_invoice','arguments':{'account_id':'acme','invoice_id':'inv-1'}},
                  {'action':'finish','arguments':{'resolution':'needs_clarification','summary':'Checked'}}])
    monkeypatch.setattr(loop.Provider,'complete',lambda *a,**kw: next(actions))
    monkeypatch.setattr(loop,'output',lambda x:x)
    monkeypatch.setattr(loop,'export_trace',lambda *a,**kw: {})
    calls=[]
    def flaky_lookup(state,account_id,invoice_id):
        calls.append(account_id)
        if len(calls)==1: raise TimeoutError('read timeout')
        return {'payments':[]}
    s=WorkshopSession('user/project','test',state_dir=tmp_path)
    case=next(c for c in CASES if c.id=='double-charge')
    run=loop.run_employee(s,case,Harness(read_retries=1),'test',invoice_tool=flaky_lookup)
    assert len(calls)==2
    assert run['events'][0]['error']=='read timeout'
    assert run['events'][1]['result']=={'payments':[]}


def test_pending_branch_labels_accept_string_decisions(tmp_path):
    from forge_workshop_kit import WorkshopSession,ui
    s=WorkshopSession('user/project','test',state_dir=tmp_path)
    with s.stage('pending/round-1/compose') as stage:
        stage.record({'decision':'KEEP','title':'Retain this harness'})
    assert 'Retain this harness' in ui.branch_graph(s)
