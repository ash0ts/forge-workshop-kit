import json
import pytest
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.session import StageNeedsReview


def test_completed_stage_is_reused_and_source_change_is_new(tmp_path):
    session=WorkshopSession('person/lab','test',state_dir=tmp_path)
    calls=[]
    for source in ('v1','v1','v2'):
        with session.stage('train',sources={'model.py':source}) as stage:
            if stage.needs_run:
                calls.append(source)
                stage.record({'metric':1})
    assert calls==['v1','v2']
    assert len(session.completed())==2


def test_interrupted_stage_requires_explicit_attempt(tmp_path):
    session=WorkshopSession('person/lab','test',state_dir=tmp_path)
    with session.stage('train'):
        pass
    with pytest.raises(StageNeedsReview):
        with session.stage('train'):
            pytest.fail('Must not execute')
    with session.stage('train',attempt=2) as stage:
        stage.record({'metric':None})
    assert len(session.read()['stages'])==2


def test_project_binding_and_notebook_copy_identity(tmp_path):
    one=WorkshopSession('person/lab','test',state_dir=tmp_path/'one',notebook_identity='copy-a')
    same=WorkshopSession('person/lab','test',state_dir=tmp_path/'again',notebook_identity='copy-a')
    two=WorkshopSession('person/lab','test',state_dir=tmp_path/'two',notebook_identity='copy-b')
    assert one.workspace_id==same.workspace_id!=two.workspace_id
    with pytest.raises(ValueError):
        WorkshopSession('other/lab','test',state_dir=tmp_path/'one',notebook_identity='copy-a')


def test_publication_outage_does_not_repeat_work(tmp_path):
    class Broken:
        def publish_stages(self): raise ConnectionError('offline')
        def publish_progress(self): raise ConnectionError('offline')
        def publish_checkpoint(self): raise ConnectionError('offline')
    session=WorkshopSession('person/lab','test',state_dir=tmp_path,publisher=Broken())
    with session.stage('run') as stage:
        stage.record({'metric':0})
    assert all(v['status']=='unavailable' for v in session.checkpoint('run').values())
    assert len(session.completed())==1
    assert session.restore()['status']=='local'


def test_export_allowlist_and_traversal(tmp_path):
    session=WorkshopSession('person/lab','test',state_dir=tmp_path)
    (tmp_path/'secret.env').write_text('secret')
    assert (tmp_path/'secret.env') not in session.export_files()
    with pytest.raises(ValueError): session.file('../outside')
