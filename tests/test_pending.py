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
