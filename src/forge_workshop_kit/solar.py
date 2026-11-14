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


def image_display_scales(predictions, split):
    """Use the notebook comparison's shared intensity/error scale for each timestamp."""
    scales = []
    for i, target in enumerate(split['y'][:, 0]):
        mask = split['mask'][i, 0].astype(bool)
        arrays = [target, *(np.asarray(values)[i, 0] for values in predictions.values())]
        lo = min(float(array.min()) for array in arrays)
        hi = max(float(array.max()) for array in arrays)
        error_hi = max(float(np.abs(array - target)[mask].max()) for array in arrays) or 1.
        scales.append({'intensity_min': lo, 'intensity_max': hi, 'error_max': error_hi})
    return scales


def _array_image(values, directory, caption, *, low, high, cmap, root):
    """Render numeric arrays as immutable media; scoring still uses full precision."""
    from io import BytesIO
    from matplotlib import colormaps
    from PIL import Image
    from .media import image_value

    scaled = (np.asarray(values) - low) / (high - low if high > low else 1.)
    # Notebook imshow uses origin='lower'; ordinary image viewers start at the top.
    rgba = colormaps[cmap](np.flipud(np.clip(scaled, 0, 1)), bytes=True)
    buffer = BytesIO()
    Image.fromarray(rgba).save(buffer, format='PNG')
    content = buffer.getvalue()
    path = Path(directory) / (hashlib.sha256(content).hexdigest() + '.png')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise ValueError('Saved forecast image differs from its content hash.')
    if not path.exists():
        path.write_bytes(content)
    return image_value(path, caption, root=root)


def evaluation_rows(prediction,split,*,evidence=None,media_dir=None,media_root=None,image_scales=None):
    """Publish exact scores and, when requested, images from the same forecast arrays.

    Calls without media_dir preserve the original scalar-summary row format. Image
    comparisons pass scales shared across every version, so a color means the same
    value in each prediction and its error map.
    """
    prediction = np.asarray(prediction)
    scores=errors(prediction,split['y'],split['mask'])
    image=prediction.ndim>2
    rows = [dict(case_id=str(case),input={'forecast_origin':str(case)},
        prediction={'mean':float(prediction[i].mean()),'file_index':i} if image else prediction[i].tolist(),
        target={'mean':float(split['y'][i].mean()),'file_index':i} if image else split['y'][i].tolist(),
        error=float(scores[i]), evidence=evidence or {}) for i,case in enumerate(split['ids'])]
    if image and media_dir is not None:
        if prediction.ndim != 4 or prediction.shape[1] != 1 or split['x'].shape != (len(rows), 2, *prediction.shape[2:]):
            raise ValueError('Image publication expects two input frames and one forecast frame per case.')
        scales = image_scales if image_scales is not None else image_display_scales({'prediction': prediction}, split)
        if len(scales) != len(rows):
            raise ValueError('Image display scales must match the forecast timestamps.')
        for i, row in enumerate(rows):
            scale = scales[i]
            render = lambda array, caption, low=scale['intensity_min'], high=scale['intensity_max'], cmap='magma': _array_image(
                array, media_dir, caption + ' · ' + row['case_id'] + ' UTC', low=low, high=high, cmap=cmap, root=media_root)
            row['input'].update(one_hour_ago=render(split['x'][i, 0], 'Observed one hour before forecast origin'),
                                current_image=render(split['x'][i, 1], 'Observed at forecast origin'))
            row['prediction'].update(image=render(prediction[i, 0], 'Predicted one hour ahead'),
                absolute_error=render(np.abs(prediction[i, 0] - split['y'][i, 0]) * split['mask'][i, 0],
                                      'Absolute error inside the scoring mask; off-disk pixels set to zero',
                                      low=0, high=scale['error_max'], cmap='inferno'),
                display_scale=scale)
            row['target'].update(image=render(split['y'][i, 0], 'Observed one hour ahead'),
                                 disk_mask=render(split['mask'][i, 0], 'Scoring disk mask', low=0, high=1, cmap='Greys'))
    return rows
