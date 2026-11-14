import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.review import save_review, reviewed_dataset, judge_agreement
from forge_workshop_kit.releases import record_release
from forge_workshop_kit.managed_jobs import submit_once, poll_job, SubmissionNeedsReview
from forge_workshop_kit.publication import comparison_metrics, _merge_local_work
from forge_workshop_kit.pending import recovery
from forge_workshop_kit.media import image_value, checked_image, weave_value


@pytest.fixture
def session(tmp_path):
    return WorkshopSession('test/project', 'banking-routing', state_dir=tmp_path)


def test_review_withdrawal_and_test_exclusion(session):
    args = dict(case_id='c1', proposed_label='wrong', reviewer='learner', dataset_version='banking@hash')
    good = save_review(session, **args, accepted_label='correct')
    assert reviewed_dataset(session, 'banking@hash')['rows'] == [good]
    save_review(session, **args, accepted_label=None, verified=False)
    assert reviewed_dataset(session, 'banking@hash')['rows'] == []
    with pytest.raises(ValueError, match='final-test'):
        save_review(session, **args, accepted_label='correct', split='test')
    result = judge_agreement([good], {'c1': None})
    assert result['agreement'] is None and result['unavailable'] == 1


def test_job_restart_polls_id_and_never_submits_twice(session):
    calls = []
    args = dict(forecast={'maximum_usd': 2, 'basis': 'current rate x max steps', 'checked_at': '2026-11-14'}, approved_usd=2)
    def submit(request):
        calls.append(request)
        return {'id': 'job-1'}
    first = submit_once(session, 'sft', {'epochs': 1}, submit=submit, **args)
    second = submit_once(session, 'sft', {'epochs': 1}, submit=submit, **args)
    assert first == second and len(calls) == 1
    key = next(iter(session.read()['managed_jobs']))
    assert poll_job(session, key, fetch=lambda identity: {'id': identity, 'status': 'running'})['id'] == 'job-1'
    with pytest.raises(TimeoutError):
        submit_once(session, 'sft', {'epochs': 2}, submit=lambda _: (_ for _ in ()).throw(TimeoutError()), **args)
    with pytest.raises(SubmissionNeedsReview):
        submit_once(session, 'sft', {'epochs': 2}, submit=submit, **args)
    assert len(calls) == 1


def test_release_checks_and_immutable_versions(session):
    args = dict(evaluation='https://example.test/eval', decision='release', metrics={'accuracy': .9}, checks={'accuracy': True}, reason='Meets the frozen check')
    with pytest.raises(ValueError, match='exact artifact'):
        record_release(session, artifact='test/project/model:latest', **args)
    with pytest.raises(ValueError, match='checks'):
        record_release(session, artifact='test/project/model:v1', **{**args, 'checks': {'accuracy': False}})
    saved = record_release(session, artifact='test/project/model:v1', **args)
    assert saved['artifact'].endswith(':v1')


def test_macro_f1_is_not_averaged_from_cases(session):
    rows = [{'error': 0, 'scores': {'macro_f1': 1}}, {'error': None, 'scores': {}}]
    result = comparison_metrics(session, 'banking-routing-final', rows, {'macro_f1': .42})
    assert result['banking-routing-final/macro_f1'] == .42
    assert result['banking-routing-final/coverage'] is None
    assert result['planned_scores'] == 2 and result['available_scores'] == 1


def test_timeout_repair_changes_actual_state():
    broken = recovery.run_recovery(recovery.STARTER)
    fixed = recovery.run_recovery(recovery.ANSWER)
    assert broken['membership_count'] == 2 and not broken['passed']
    assert fixed['membership_count'] == 1 and fixed['passed']
    assert fixed['events'][1]['result']['replayed'] is True


def test_image_values_are_checked_and_weave_media_is_typed(tmp_path):
    from PIL import Image
    path = tmp_path / 'board.png'
    Image.new('RGB', (8, 8), 'red').save(path)
    value = image_value(path, 'A recorded board')
    typed = weave_value({'board': value, 'label': 'normal'})
    assert typed['label'] == 'normal'
    assert isinstance(typed['board'], Image.Image)
    assert typed['board'].getpixel((0, 0)) == (255, 0, 0)
    path.write_bytes(b'changed')
    with pytest.raises(ValueError, match='changed'):
        checked_image(value)


def test_wandb_table_keeps_optional_masks_as_media(tmp_path):
    import wandb
    from PIL import Image
    from forge_workshop_kit.media import wandb_table_data
    path = tmp_path / 'mask.png'
    Image.new('L', (8, 8), 255).save(path)
    mask = image_value(path, 'Supplied defect mask')
    rows = [{'case_id': 'defect', 'input': {'board': mask}, 'prediction': {'defect': True},
             'target': {'defect': True, 'mask': mask}, 'error': 0},
            {'case_id': 'normal', 'input': {'board': mask}, 'prediction': {'defect': False},
             'target': {'defect': False, 'mask': None}, 'error': 0}]
    columns, data = wandb_table_data(rows)
    table = wandb.Table(columns=columns, data=data)
    index = columns.index('target.mask')
    assert isinstance(table.data[0][index], wandb.Image)
    assert table.data[1][index] is None
    assert rows[0]['target']['mask'] == mask


def test_restore_keeps_newer_review_and_known_job_id():
    restored = {'stages': {}, 'managed_jobs': {'j': {'job_id': 'saved'}}}
    local = {'stages': {}, 'reviews': {'r': {'accepted_label': 'card_arrival'}}, 'managed_jobs': {'j': {'status': 'submitting'}}}
    _merge_local_work(restored, local)
    assert restored['managed_jobs']['j']['job_id'] == 'saved'
    assert restored['reviews']['r']['accepted_label'] == 'card_arrival'


def test_restore_keeps_completed_advanced_calls_and_accounting_stop():
    import copy
    plan = {'models': ['base', 'checkpoint']}
    request = {'model': 'base', 'messages': []}
    complete = {'status': 'complete', 'request': request, 'observed_usd': .01}
    pending = {'status': 'pending', 'request': request, 'bounded_unknown_usd': .02}
    restored = {'advanced_comparisons': {'c': {'plan': plan, 'requests': {'a': complete}}}}
    local = {'advanced_comparisons': {'c': {'plan': plan, 'requests': {'a': pending, 'b': complete}, 'stop': 'usage exceeded'}}}
    _merge_local_work(restored, local)
    saved = restored['advanced_comparisons']['c']
    assert saved['requests']['a']['status'] == 'complete'
    assert saved['requests']['b']['observed_usd'] == .01
    assert saved['stop'] == 'usage exceeded'
    conflict = copy.deepcopy(local)
    conflict['advanced_comparisons']['c']['plan'] = {'models': ['different']}
    with pytest.raises(ValueError, match='conflicting request plans'):
        _merge_local_work(restored, conflict)
