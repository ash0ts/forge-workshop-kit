"""Publish the immutable, checked teaching data to an artifact and anonymous release archive."""
import argparse,hashlib,json,tarfile
from pathlib import Path
from forge_workshop_kit.solar import verify_data,load_aia,load_goes
p=argparse.ArgumentParser();p.add_argument('--project',required=True);a=p.parse_args()
root=Path('data/solar-v1');fingerprint=verify_data(root)
images,image_norm=load_aia(root);goes,goes_norm=load_goes(root)
Path('dist').mkdir(exist_ok=True);archive=Path('dist/solar-v1.tar.gz')
with tarfile.open(archive,'w:gz') as bundle:bundle.add(root,arcname='solar-v1')
assert archive.stat().st_size<100_000_000
sha=hashlib.sha256(archive.read_bytes()).hexdigest();Path('dist/solar-v1.sha256').write_text(sha+'  solar-v1.tar.gz\n')
import wandb
entity,project=a.project.split('/')
with wandb.init(entity=entity,project=project,job_type='workshop-dataset',name='Solar teaching observations · 2014-02-01 to 14',settings=wandb.Settings(disable_git=True)) as run:
 artifact=wandb.Artifact('solar-v1',type='dataset',metadata={'manifest_sha256':fingerprint,'dates':'2014-02-01/2014-02-14','selection':'fixed dates and quality only'})
 artifact.add_dir(str(root));run.log_artifact(artifact).wait();ref=artifact.qualified_name
out=dict(manifest_sha256=fingerprint,archive_sha256=sha,bytes=archive.stat().st_size,artifact=ref,
 goes_windows={k:len(v['ids']) for k,v in goes.items()},aia_windows={k:len(v['ids']) for k,v in images.items()},goes_normalization=goes_norm,aia_normalization=image_norm)
Path('evidence/dataset.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
