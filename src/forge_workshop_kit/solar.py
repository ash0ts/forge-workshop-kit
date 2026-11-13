"""Fixed data partitions and scoring. Candidate code never receives final-test records."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

SPLITS = {'train': ('2014-02-01','2014-02-11'),
          'validation': ('2014-02-11','2014-02-13'), 'test': ('2014-02-13','2014-02-15')}


def verify_data(root):
    root=Path(root)
    manifest=json.loads((root/'manifest.json').read_text(encoding="utf-8"))
    if not manifest['complete']:
        raise ValueError('Data preparation is incomplete.')
    for name,checksum in manifest['files'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=checksum:
            raise ValueError('Dataset checksum mismatch: '+name)
    return hashlib.sha256((root/'manifest.json').read_bytes()).hexdigest()


def partition(times, earliest, latest):
    for name,(begin,end) in SPLITS.items():
        if times[earliest] >= np.datetime64(begin) and times[latest] < np.datetime64(end):
            return name
    return None


def load_goes(root):
    df=pd.read_csv(Path(root)/'goes.csv',parse_dates=['timestamp']).sort_values('timestamp')
    times=df.timestamp.to_numpy(dtype='datetime64[m]')
    values=np.log10(df[['xrsa','xrsb']].to_numpy(dtype='float32'))
    rows={k:[] for k in SPLITS}
    for i in range(59,len(times)-30):
        # Every one-minute sample in the complete input/target interval must exist.
        if np.any(np.diff(times[i-59:i+31])!=np.timedelta64(1,'m')):
            continue
        split=partition(times,i-59,i+30)
        if split:
            rows[split].append((values[i-59:i+1].T,values[i+30,1:2],str(times[i]),values[i,1:2]))
    result={}
    for split,records in rows.items():
        if not records:
            raise ValueError('No valid GOES windows in '+split)
        x,y,ids,persistence=zip(*records)
        result[split]=dict(x=np.array(x),y=np.array(y),ids=np.array(ids),
                          persistence=np.array(persistence),mask=np.ones_like(y,dtype=bool))
    mean=result['train']['x'].mean(axis=(0,2),keepdims=True)
    std=result['train']['x'].std(axis=(0,2),keepdims=True).clip(.01)
    for item in result.values():
        item['x']=(item['x']-mean)/std
    return result,dict(mean=mean.tolist(),std=std.tolist(),target='log10 XRS-B W/m²',horizon_minutes=30)


def load_aia(root):
    raw=np.load(Path(root)/'aia.npz',allow_pickle=False)
    times=raw['timestamps'].astype('datetime64[m]')
    # Log1p rate stabilizes the dynamic range. The target and metric stay fixed across models.
    images=np.log1p(raw['images'])
    masks=raw['masks']
    train=times<np.datetime64(SPLITS['train'][1])
    scale=float(np.std(images[train][masks[train]]))
    center=float(np.mean(images[train][masks[train]]))
    scale=max(scale,.01)
    images=(images-center)/scale
    records={k:[] for k in SPLITS}
    for i in range(5,len(times)-5):
        if np.any(np.diff(times[i-5:i+6]) != np.timedelta64(12,'m')):
            continue
        split=partition(times,i-5,i+5)
        if split:
            records[split].append((np.stack([images[i-5],images[i]]),images[i+5][None],
                                  str(times[i]),images[i][None],masks[i+5][None]))
    result={}
    for split,rows in records.items():
        if not rows:
            raise ValueError('No valid AIA windows in '+split)
        x,y,ids,persistence,mask=zip(*rows)
        result[split]=dict(x=np.array(x),y=np.array(y),ids=np.array(ids),
                          persistence=np.array(persistence),mask=np.array(mask))
    return result,dict(center=center,scale=scale,target='normalized log1p AIA 171 rate',horizon_minutes=60)


def errors(prediction,target,mask):
    prediction=np.asarray(prediction)
    if prediction.shape != target.shape or not np.isfinite(prediction).all():
        raise ValueError('Predictions must match target shape and contain finite values.')
    axes=tuple(range(1,target.ndim))
    return (np.abs(prediction-target)*mask).sum(axis=axes)/mask.sum(axis=axes)


def score(prediction,split):
    per_case=errors(prediction,split['y'],split['mask'])
    persistence=errors(split['persistence'],split['y'],split['mask'])
    baseline=float(persistence.mean())
    return dict(error=float(per_case.mean()),persistence_error=baseline,
                skill_vs_persistence=1-float(per_case.mean())/baseline if baseline else None,
                examples=len(per_case))


def evaluation_rows(prediction,split,*,evidence=None):
    scores=errors(prediction,split['y'],split['mask'])
    image=prediction.ndim>2
    return [dict(case_id=str(case),input={'forecast_origin':str(case)},
        prediction={'mean':float(prediction[i].mean()),'file_index':i} if image else prediction[i].tolist(),
        target={'mean':float(split['y'][i].mean()),'file_index':i} if image else split['y'][i].tolist(),
        error=float(scores[i]), evidence=evidence or {}) for i,case in enumerate(split['ids'])]
