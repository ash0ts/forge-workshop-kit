"""Rebuild teaching values from frozen public data; no classifier fitting or paid calls."""
import json, hashlib, shutil
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[3]
D=R/'data/inspection-v1';records=json.loads((D/'records.json').read_text());loaded=np.load(D/'features.npz');z={k:loaded[k].astype('float32') for k in loaded.files};query=next(r for r in records if r['partition']=='fit' and r['label']==1);q=records.index(query);bankrows=[i for i,r in enumerate(records) if r['partition']=='fit' and r['label']==0];bank=z['patches'][bankrows];scale=np.maximum(bank.std(axis=0),.1); p=(7,7);d=((z['patches'][q,p[0],p[1]]/scale[p]-bank[:,p[0],p[1]]/scale[p])**2).mean(axis=1); best=int(d.argmin()); selected=[0,1,2,best]
f={'source':'data/inspection-v1/features.npz','source_sha256':hashlib.sha256((D/'features.npz').read_bytes()).hexdigest(),'case_id':query['case_id'],'position':list(p),'normal_bank_size':len(bankrows),'distances':[{'case_id':records[bankrows[i]]['case_id'],'distance':float(d[i]),'closest':i==best} for i in selected],'closest_distance':float(d[best]),'log1p_closest_distance':float(np.log1p(d[best])),'patch_shape':list(z['patches'].shape),'whole_shape':list(z['whole'].shape)}
for name, rec in [('fit-defect',query),('case-corrected',next(r for r in records if r['case_id']=='pcb1-anomaly-048')),('case-regression',next(r for r in records if r['case_id']=='pcb1-anomaly-015'))]:
 for key,ext in [('image','jpg'),('mask','png')]:
  shutil.copyfile(D/rec[key],R/'decks/inspection/public/images'/f'{name}-{key}.{ext}')
rows=json.loads((R/'evidence/inspection-teaching-retest-v2/predictions.json').read_text());f['images']=[{**r, 'license':'VisA CC BY 4.0', 'source_archive':'https://github.com/amazon-science/spot-diff', 'original_record_file':'data/inspection-v1/records.json'} for r in records if r['case_id'] in [query['case_id'],'pcb1-anomaly-048','pcb1-anomaly-015']]
f['mask_display']='Source mask pixels contain integer category IDs (0 background; positive annotation IDs). SVG display multiplies intensity by 255 so positive IDs appear white; original mask files remain unchanged.'
f['prediction_source']='evidence/inspection-teaching-retest-v2/predictions.json'
f['prediction_source_sha256']=hashlib.sha256((R/f['prediction_source']).read_bytes()).hexdigest()
f['outcomes']=[r for r in rows if r['case_id'] in ['pcb1-anomaly-048','pcb1-anomaly-015']]
(R/'decks/inspection/data/feature-example.json').write_text(json.dumps(f,indent=2)+'\n')
