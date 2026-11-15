import json
import numpy as np
import pytest
from forge_workshop_kit import routing, routing_teaching as teaching


def example_data():
    rows=[];features=[]
    for split,count in [('train',8),('validation',2),('review',2),('test',2)]:
        for label,vector in [('card_arrival',[1.,0.]),('card_not_working',[0.,1.])]:
            for n in range(count):
                rows.append({'id':f'{split}/{label}/{n}','text':('where is my card delivery' if vector[0] else 'my broken card declined')+f' {n}','label':label,'split':split})
                features.append(vector)
    return {'rows':rows,'features':np.asarray(features)}


def test_split_is_deterministic_and_training_only():
    rows=[{'id':f'{label}/{n}','text':str(n),'label':label} for label in ('a','b') for n in range(30)]
    a=routing.assign_split(rows)
    b=routing.assign_split(list(reversed(rows)))
    assert {r['id']:r['split'] for r in a}=={r['id']:r['split'] for r in b}
    assert sum(r['split']=='review' for r in a)==20
    assert sum(r['split']=='validation' for r in a)==20
    assert sum(r['split']=='train' for r in a)==20


def test_models_use_no_review_validation_or_test_to_fit():
    data=example_data()
    for kind in ('tfidf','embedding'):
        model=routing.fit_classifier(data,kind)
        assert all(identity.startswith('train/') for identity in model['training_ids'])
        rows=routing.predict(model,data,'test')
        assert routing.score(rows)['macro_f1']==1


def test_review_requires_human_and_rejects_final_cases():
    data=example_data()
    record={'case_id':'review/card_arrival/0','accepted_label':'card_arrival','verified':True,'label_source':'human_review'}
    model=routing.fit_classifier(data,'embedding',reviewed=[record])
    assert record['case_id'] in model['training_ids']
    with pytest.raises(ValueError,match='human'):routing.fit_classifier(data,'embedding',reviewed=[{**record,'label_source':'teacher'}])
    with pytest.raises(ValueError,match='review-pool'):routing.fit_classifier(data,'embedding',reviewed=[{**record,'case_id':'test/card_arrival/0'}])
    with pytest.raises(ValueError,match='more than once'):routing.fit_classifier(data,'embedding',reviewed=[record,record])


def test_review_selection_never_uses_target():
    rows=[{'case_id':'b','margin':.1,'split':'review','target':'a'},{'case_id':'a','margin':.1,'split':'review','target':'b'}]
    assert routing.select_review(rows,1)[0]['case_id']=='a'
    with pytest.raises(ValueError):routing.select_review([{**rows[0],'split':'test'}])


def test_abstention_keeps_task_quality_separate():
    rows=[{'target':'a','prediction':'a','abstained':False,'latency_seconds':.1}, {'target':'b','prediction':'a','abstained':True,'latency_seconds':.1}]
    values=routing.score(rows)
    assert values['accuracy']==.5 and values['coverage']==.5 and values['selective_accuracy']==1
    assert routing.score([{**r,'abstained':True} for r in rows])['selective_accuracy'] is None


def test_route_validation_and_prompt_exclude_reference_labels():
    good={'intent':'card_arrival','needs_review':False,'reason':'The customer is asking about delivery.'}
    assert routing.validate_route(good,['card_arrival'])==good
    for bad in ({**good,'needs_review':'false'},{**good,'intent':'refund'}, {'intent':'card_arrival'}):
        with pytest.raises(ValueError):routing.validate_route(bad,['card_arrival'])
    prompt=routing.route_messages('Where is it?',['card_arrival'])
    assert prompt[-1]['content']=='Where is it?'
    with pytest.raises(ValueError):routing.prompted_route(None,'test',{'split':'test'},[])


def test_unavailable_judgments_remain_missing():
    human=[{'case_id':'a','failed':True},{'case_id':'b','failed':False}]
    result=routing.judge_alignment(human,{'a':{'failed':False},'b':None})
    assert result['available']==1 and result['unavailable']==1 and result['missed_failures']==1
    assert routing.judge_alignment(human,{})['agreement'] is None


def test_exercises_require_the_missing_behavior():
    assert teaching.check_classifier(teaching.CLASSIFIER_SOLUTION)['status']=='complete'
    assert teaching.check_policy(teaching.POLICY_SOLUTION)['status']=='complete'
    assert teaching.check_validator(teaching.VALIDATOR_SOLUTION)['status']=='complete'
    for check,source in ((teaching.check_classifier,teaching.CLASSIFIER_STARTER),(teaching.check_policy,teaching.POLICY_STARTER),(teaching.check_validator,teaching.VALIDATOR_STARTER)):
        with pytest.raises(NotImplementedError):check(source)


def test_manifest_tampering_and_encoder_mismatch(tmp_path):
    (tmp_path/'cases.json').write_text(json.dumps([{'id':'official-test/0','split':'train'}]))
    (tmp_path/'manifest.json').write_text(json.dumps({'encoder_revision':routing.ENCODER_REVISION,'files':{'cases.json':routing.checksum(tmp_path/'cases.json')}}))
    with pytest.raises(ValueError,match='Official test'):routing.verify_data(tmp_path)
    (tmp_path/'cases.json').write_text('[]')
    with pytest.raises(ValueError,match='checksum'):routing.verify_data(tmp_path)


def test_participant_head_settings_are_recorded():
    from sklearn.linear_model import LogisticRegression
    fitted = routing.fit_classifier(example_data(), 'embedding',
        factory=lambda: LogisticRegression(C=3, random_state=23, max_iter=1000))
    assert fitted['C'] == 3 and fitted['seed'] == 23
    assert fitted['head_parameters']['C'] == fitted['model'].get_params()['C']


def test_final_freeze_requires_judge_attempt_not_routing_sample(tmp_path):
    from forge_workshop_kit import WorkshopSession
    session = WorkshopSession("test/routing", "banking-routing", state_dir=tmp_path)
    for kind in ("tfidf", "embedding"):
        with session.stage("routing/baseline/" + kind, sources={"classifier.py": teaching.CLASSIFIER_SOLUTION}) as stage:
            stage.record({"model_sha256": "test"})
    with session.stage("routing/judge/prompted/case-a") as stage:
        stage.record({"intent": "card_arrival"})
    assert teaching.freeze_prerequisite(session)
    assert "judge" not in teaching.completed_steps(session)
    with session.stage("routing/judge/summary") as stage:
        stage.record({"human_reviews": [{"case_id": "a", "failed": False}],
                      "predictions": {"a": None}, "attempts": [{"case_id": "a", "status": "unavailable"}],
                      "metrics": {"available": 0, "unavailable": 1, "agreement": None}})
    assert teaching.freeze_prerequisite(session) is None
    assert "judge" in teaching.completed_steps(session)
    assert teaching.judge_summary(session)["result"]["metrics"]["agreement"] is None


def test_download_resolves_temporary_directory_alias(tmp_path, monkeypatch):
    """macOS /var aliases /private/var; valid archive entries remain inside it."""
    import contextlib
    import hashlib
    import io
    import tarfile
    from types import SimpleNamespace

    real = tmp_path / 'real'
    real.mkdir()
    alias = tmp_path / 'alias'
    alias.symlink_to(real, target_is_directory=True)
    payload = b'[]'
    manifest = {'encoder_revision': routing.ENCODER_REVISION, 'dataset_revision': routing.DATA_REVISION,
                'files': {'cases.json': hashlib.sha256(payload).hexdigest()}}
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as bundle:
        for name, body in [('cases.json', payload), ('manifest.json', json.dumps(manifest).encode())]:
            entry = tarfile.TarInfo('banking77-v1/' + name)
            entry.size = len(body)
            bundle.addfile(entry, io.BytesIO(body))
    archive = buffer.getvalue()
    monkeypatch.setattr(teaching.tempfile, 'TemporaryDirectory', lambda: contextlib.nullcontext(str(alias)))
    monkeypatch.setattr(teaching.httpx, 'get', lambda *a, **k: SimpleNamespace(
        text=hashlib.sha256(archive).hexdigest(), raise_for_status=lambda: None))
    monkeypatch.setattr(teaching.httpx, 'stream', lambda *a, **k: contextlib.nullcontext(SimpleNamespace(
        raise_for_status=lambda: None, iter_bytes=lambda: iter([archive]))))
    destination = teaching.download(tmp_path / 'downloaded')
    assert (destination / 'cases.json').read_bytes() == payload
