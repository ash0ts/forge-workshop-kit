import numpy as np
import pytest
from forge_workshop_kit.solar import errors,score,partition
from forge_workshop_kit.research import validate_decision,freeze
from forge_workshop_kit import WorkshopSession


def test_known_scores_and_invalid_predictions():
    split={'y':np.array([[1.,2.],[3.,4.]]),'mask':np.array([[1,0],[1,1]]),
           'persistence':np.array([[0.,2.],[2.,3.]])}
    assert score(split['y'],split)['skill_vs_persistence']==1
    assert score(split['persistence'],split)['skill_vs_persistence']==0
    assert score(np.zeros((2,2)),split)['skill_vs_persistence']<0
    with pytest.raises(ValueError): errors(np.array([[np.nan,0],[0,0]]),split['y'],split['mask'])


def test_windows_cannot_cross_partitions():
    times=np.array(['2014-02-10T23:30','2014-02-11T00:00','2014-02-11T00:30'],dtype='datetime64[m]')
    assert partition(times,0,2) is None
    assert partition(times,1,2)=='validation'


def test_keep_is_exact_and_freeze_needs_executed_source(tmp_path):
    validate_decision({'decision':'KEEP','rationale':'No evidence for change'},'original')
    with pytest.raises(ValueError): validate_decision({'decision':'KEEP','rationale':'keep','source':'other'},'original')
    s=WorkshopSession('person/lab','test',state_dir=tmp_path)
    with s.stage('train',sources={'candidate.py':'original'}) as stage: stage.record({'metrics':{'error':1}})
    with pytest.raises(ValueError): freeze(s,{'manual':{'stage_id':stage.id,'source':'other'}},'data')
