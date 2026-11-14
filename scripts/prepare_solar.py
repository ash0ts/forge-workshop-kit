"""Acquire the predeclared real observations. Never select data using model scores."""
import argparse
import concurrent.futures
import hashlib
import json
import shutil
import time
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
from astropy.io import fits
from sunpy.net import Fido, attrs as a
from sunpy.timeseries import TimeSeries

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT / 'data/solar-v1')
parser.add_argument('--cache', type=Path, default=ROOT / 'data/raw')
parser.add_argument('--workers', type=int, default=4)
parser.add_argument('--part', choices=['all','goes','aia'], default='all')
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
args.cache.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def goes():
    result = Fido.search(a.Time('2014-02-01','2014-02-14 23:59'),a.Instrument('XRS'),
                        a.goes.SatelliteNumber(15),a.Resolution('avg1m'))
    paths = Fido.fetch(result, path=str(args.cache / '{file}'), max_conn=args.workers)
    if len(paths.errors):
        raise RuntimeError(str(paths.errors))
    sources, frames = [], []
    for path in paths:
        path = Path(path)
        ts = TimeSeries(path)
        frame = ts.to_dataframe()
        print('GOES', path.name, len(frame), list(frame.columns), flush=True)
        valid = (frame['xrsa'] > 0) & (frame['xrsb'] > 0)
        for field in ['xrsa_quality','xrsb_quality']:
            if field in frame:
                valid &= frame[field] == 0
        frames.append(frame.loc[valid, ['xrsa','xrsb']])
        sources.append({'file': path.name, 'url': next(str(row['url']) for row in result[0] if str(row['url']).endswith(path.name)), 'sha256': sha(path), 'rows': len(frame),
                        'retained': int(valid.sum()), 'units': {k:str(v) for k,v in ts.units.items()}})
    data = pd.concat(frames).sort_index()
    data = data[~data.index.duplicated()]
    data = data[(data.index >= '2014-02-01') & (data.index < '2014-02-15')]
    data.to_csv(args.output / 'goes.csv', index_label='timestamp')
    (args.output / 'goes-sources.json').write_text(json.dumps(sources,indent=2))
    print('GOES prepared', len(data), flush=True)


def one_aia(timestamp):
    base = 'https://jsoc1.stanford.edu/data/aia/synoptic/'
    filename = timestamp.strftime('AIA%Y%m%d_%H%M_0171.fits')
    url = base + timestamp.strftime('%Y/%m/%d/H%H00/') + filename
    path = args.cache / filename
    for attempt in range(3):
        try:
            if not path.exists():
                response = httpx.get(url, timeout=40)
                if response.status_code == 404:
                    return {'timestamp':str(timestamp), 'url':url, 'excluded':'missing archive image'}, None, None
                response.raise_for_status()
                temporary = path.with_suffix('.part')
                temporary.write_bytes(response.content)
                temporary.replace(path)
            with fits.open(path) as hdus:
                hdu = next(h for h in hdus if h.data is not None and h.data.ndim == 2)
                # Read the required physical metadata only. This archive has an unrelated malformed OSCNMEAN card.
                keys=('DATE-OBS','EXPTIME','BUNIT','CDELT1','CDELT2','CRPIX1','CRPIX2','RSUN_OBS','QUALITY','WAVELNTH','CRVAL1','CRVAL2','CTYPE1','CTYPE2','CUNIT1','CUNIT2')
                header = {k:hdu.header.get(k) for k in keys}
                array = np.asarray(hdu.data,dtype='float32')
            if int(header.get('QUALITY',0)) != 0:
                return {'timestamp':str(timestamp),'url':url,'sha256':sha(path),'excluded':'QUALITY != 0'}, None, None
            if np.isfinite(array).mean() < .99:
                return {'timestamp':str(timestamp),'url':url,'sha256':sha(path),'excluded':'nonfinite pixels > 1%'}, None, None
            exposure = float(header.get('EXPTIME',0))
            if exposure <= 0:
                raise ValueError('Missing positive exposure')
            # Archive README specifies DN/original pixel, not a rate. Normalize by exposure once.
            rate = np.maximum(np.nan_to_num(array),0) / exposure
            small = rate.reshape(64,16,64,16).mean(axis=(1,3)).astype('float32')
            observed = pd.Timestamp(header.get('DATE-OBS',str(timestamp)))
            if observed.tzinfo:
                observed = observed.tz_convert('UTC').tz_localize(None)
            if abs((observed-timestamp).total_seconds()) > 120:
                raise ValueError('Timestamp differs from archive slot by > 120 seconds')
            metadata = {k:header.get(k) for k in ('DATE-OBS','EXPTIME','BUNIT','CDELT1','CDELT2','CRPIX1','CRPIX2','RSUN_OBS','QUALITY','WAVELNTH','CRVAL1','CRVAL2','CTYPE1','CTYPE2','CUNIT1','CUNIT2')}
            radius = float(header['RSUN_OBS']) / abs(float(header['CDELT1'])) / 16
            yy,xx=np.mgrid[:64,:64]
            mask=((xx-(float(header['CRPIX1'])-.5)/16+.5)**2 +
                  (yy-(float(header['CRPIX2'])-.5)/16+.5)**2 <= radius**2)
            return dict(timestamp=str(timestamp), observed_at=str(observed), url=url,
                sha256=sha(path), metadata=metadata), small, mask
        except Exception as error:
            if attempt == 2:
                return dict(timestamp=str(timestamp),url=url,excluded=type(error).__name__+': '+str(error)),None,None
            time.sleep(attempt+1)


def aia():
    times = pd.date_range('2014-02-01', '2014-02-15', inclusive='left',freq='12min')
    sources, arrays, masks, kept = [], [], [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i,(source,array,mask) in enumerate(pool.map(one_aia,times)):
            sources.append(source)
            if array is not None:
                arrays.append(array); masks.append(mask); kept.append(source['timestamp'])
            if (i+1)%50 == 0:
                print(f'AIA {i+1}/{len(times)} processed; {len(kept)} kept',flush=True)
    np.savez_compressed(args.output/'aia.npz', images=np.array(arrays), masks=np.array(masks), timestamps=np.array(kept))
    (args.output/'aia-sources.json').write_text(json.dumps(sources,indent=2))
    good=next(s for s in sources if 'excluded' not in s)
    shutil.copy2(args.cache/Path(good['url']).name,args.output/'sample-aia.fits')
    print('AIA prepared',len(kept),flush=True)

if args.part in ('all','goes'):
    goes()
if args.part in ('all','aia'):
    aia()
files={p.name:sha(p) for p in args.output.iterdir() if p.is_file() and p.name!='manifest.json'}
manifest=dict(version='solar-v1',start='2014-02-01',end_exclusive='2014-02-15',
    train_end='2014-02-11',validation_end='2014-02-13',files=files,
    selection='Fixed dates and quality rules before training; no model-score selection',
    aia_units='DN per original 0.6 arcsec pixel per second',goes_units='W/m^2',
    complete=all(k in files for k in ['goes.csv','aia.npz','sample-aia.fits']),
    acquisition_code_sha256=sha(Path(__file__)))
(args.output/'manifest.json').write_text(json.dumps(manifest,indent=2))
