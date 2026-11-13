import json
import hashlib
from pathlib import Path
import pytest
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.publication import Publisher,monitor

class Artifact:
    def __init__(self,files):self.files=files
    def download(self,root):
        for name,content in self.files.items():
            p=Path(root)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
class Api:
    def __init__(self,files):self.files=files
    def artifact(self,*args,**kwargs):return Artifact(self.files)

def test_destroyed_hosted_runtime_restores_exact_source_results_and_uncertain_requests(tmp_path):
    s=WorkshopSession('test/project','lab',state_dir=tmp_path/'before',notebook_identity='copy-a')
    with s.stage('train',sources={'model.py':'weights=3'}) as stage:
        output=stage.output_dir/'weights.txt';output.write_text('trained-once')
        stage.record({'error':0.2},files=[output])
    with s.transaction() as state:state['requests']['pending/0']={'status':'pending','reserved_usd':.01}
    files={str(p.relative_to(s.root)):p.read_bytes() for p in s.export_files()}
    files['checksums.json']=json.dumps({k:hashlib.sha256(v).hexdigest() for k,v in files.items()}).encode()
    restored=WorkshopSession('test/project','lab',state_dir=tmp_path/'after',notebook_identity='copy-a')
    publisher=Publisher.__new__(Publisher);publisher.session=restored;publisher.api=Api(files);restored.publisher=publisher
    assert restored.restore()['completed']==1
    with restored.stage('train',sources={'model.py':'weights=3'}) as cached:assert not cached.needs_run
    assert restored.read()['requests']['pending/0']['status']=='pending'
    assert restored.file('outputs/'+stage.id+'/weights.txt').read_text()=='trained-once'
    other=WorkshopSession('test/project','lab',state_dir=tmp_path/'other',notebook_identity='copy-b')
    publisher.session=other;other.publisher=publisher
    with pytest.raises(ValueError,match='another notebook'):other.restore()

def test_monitor_reads_only_and_missing_is_unknown():
    class ReadOnly:
        def runs(self,project,filters):
            assert project=='person/project'
            return []
    assert monitor(['https://forge.coreweave.com/wandb/person/project'],'lab',api=ReadOnly())[0]['status']=='unknown'

def test_monitor_uses_notebook_step_names_for_intermediate_checkpoints():
    from types import SimpleNamespace
    class ReadOnly:
        def runs(self, project, filters):
            return [SimpleNamespace(config={'workspace_id': 'copy-a'}, url='https://example.test/run',
                summary=SimpleNamespace(_json_dict={'step': 'images/round-2/review-0',
                    'completed': ['setup'], 'status': 'complete'}))]
    row = monitor(['person/project'], 'solar-autoresearch', api=ReadOnly())[0]
    assert row['step'] == 'Research agent'
    assert row['checkpoint'] == 'images/round-2/review-0'

def test_training_inputs_exclude_validation_labels_and_child_has_no_credentials(tmp_path,monkeypatch):
    import numpy as np
    from forge_workshop_kit import training
    observed={}
    def run(command,**kwargs):
        request=json.loads(Path(command[-1]).read_text());data=np.load(request['data'])
        observed.update(keys=list(data.keys()),env=kwargs['env'])
        np.save(request['prediction'],np.array([[2.]],dtype='float32'))
        Path(request['losses']).write_text('[0.2]')
        return type('Result',(),dict(returncode=0,stdout='',stderr=''))()
    monkeypatch.setattr(training.subprocess,'run',run)
    monkeypatch.setenv('WANDB_API_KEY','SECRET-NOT-IN-CHILD')
    train=dict(x=np.array([[1.]]),y=np.array([[1.]]),mask=np.ones((1,1)))
    val=dict(x=np.array([[2.]]),y=np.array([[2.]]),mask=np.ones((1,1)),persistence=np.array([[1.]]))
    training.train('example',train,val,{},tmp_path)
    assert set(observed['keys'])=={'predict_x','train_x','train_y','train_mask'}
    assert 'WANDB_API_KEY' not in observed['env']

def test_confirmed_interruption_counts_the_full_unknown_reservation(tmp_path):
    from forge_workshop_kit.provider import Provider
    s=WorkshopSession('test/project','lab',state_dir=tmp_path)
    with pytest.raises(RuntimeError):
        with s.stage('request') as stage:
            with s.transaction() as state:
                state['requests'][stage.id+'/0']={'status':'pending','reserved_usd':.02}
            raise RuntimeError('process stopped')
    s.mark_interrupted(stage.id,'Confirmed old process stopped')
    assert Provider(s).summary()=={'observed_usd':0,'bounded_unknown_usd':.02,'inflight_usd':0}


def test_cpu_training_produces_loadable_frozen_weights(tmp_path):
    import numpy as np
    from forge_workshop_kit.training import train
    source=(Path(__file__).resolve().parents[1]/'examples/solar/candidate.py').read_text()
    split=dict(x=np.ones((4,2,8,8),dtype='float32'),y=np.ones((4,1,8,8),dtype='float32'),
               mask=np.ones((4,1,8,8),dtype=bool),persistence=np.ones((4,1,8,8),dtype='float32'))
    config=dict(architecture='residual',width=2,steps=2,batch_size=2,seed=17)
    result,prediction=train(source,split,split,config,tmp_path/'train')
    frozen,again=train(source,None,split,config,tmp_path/'frozen',weights=tmp_path/'train/weights.pt')
    assert np.array_equal(prediction,again)
    assert frozen['losses']==[] and len(result['losses'])==2
