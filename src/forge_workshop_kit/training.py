"""Execute reviewed code; score predictions independently in the parent process."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
from .solar import score


def train(source, train_split, validation, config, output_dir, *, timeout=180, weights=None):
    output_dir=Path(output_dir).resolve()
    output_dir.mkdir(parents=True,exist_ok=True)
    path=output_dir/'candidate.py'
    path.write_text(source)
    data=output_dir/'inputs.npz'
    payload={'predict_x':validation['x']}
    if weights is None:
        payload.update(train_x=train_split['x'],train_y=train_split['y'],train_mask=train_split['mask'])
    np.savez_compressed(data,**payload)
    request=dict(source=str(path),data=str(data),config=config,
        prediction=str(output_dir/'predictions.npy'),output_weights=str(output_dir/'weights.pt'),
        losses=str(output_dir/'losses.json'),weights=str(Path(weights).resolve()) if weights else None)
    (output_dir/'request.json').write_text(json.dumps(request))
    # Explicit allowlist. This is a teaching subprocess, not adversarial-code isolation.
    env={k:os.environ[k] for k in ('PATH','SYSTEMROOT','WINDIR','TMPDIR','TEMP','TMP') if k in os.environ}
    env.update(PYTHONHASHSEED=str(config.get('seed',17)),OMP_NUM_THREADS='2',MKL_NUM_THREADS='2')
    worker=Path(__file__).with_name('worker.py').resolve()
    started=time.time()
    try:
        result=subprocess.run([sys.executable,str(worker),str(output_dir/'request.json')],
            cwd=output_dir,env=env,text=True,capture_output=True,timeout=timeout)
    except subprocess.TimeoutExpired as error:
        (output_dir/'stderr.txt').write_text('Execution exceeded '+str(timeout)+' seconds.')
        raise RuntimeError('Training timed out; the failed attempt is retained.') from error
    (output_dir/'stdout.txt').write_text(result.stdout)
    (output_dir/'stderr.txt').write_text(result.stderr)
    if result.returncode:
        raise RuntimeError('Candidate failed: '+result.stderr[-1500:])
    prediction=np.load(output_dir/'predictions.npy',allow_pickle=False)
    metrics=score(prediction,validation)
    metrics.update(validation_error=metrics['error'],seconds=time.time()-started)
    return dict(metrics=metrics,losses=json.loads((output_dir/'losses.json').read_text()),
                exit_code=result.returncode),prediction
