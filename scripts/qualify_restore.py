"""Real artifact restore into a second empty runtime directory, without inference."""
import argparse,json,tempfile
from pathlib import Path
from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.publication import monitor
parser=argparse.ArgumentParser();parser.add_argument('--project',required=True);args=parser.parse_args()
project=args.project
a=WorkshopSession(project,'restore-qualification',state_dir='.workshop/restore-origin',notebook_identity='qualification-copy-20261113')
a.check_access()
with a.stage('training-receipt',sources={'model.py':'# A tool-only restore fixture, not a trained model.'}) as stage:
 if stage.needs_run:
  p=stage.output_dir/'result.json';p.write_text('{"fixture":true}')
  stage.record({'fixture':True},files=[p])
publication=a.checkpoint('restore-fixture')
b=WorkshopSession(project,'restore-qualification',state_dir=tempfile.mkdtemp(prefix='restore-fresh-',dir='.workshop'),notebook_identity='qualification-copy-20261113')
b.connect();restored=b.restore()
with b.stage('training-receipt',sources={'model.py':'# A tool-only restore fixture, not a trained model.'}) as stage: assert not stage.needs_run
assert a.completed()[0]['source_fingerprint']==b.completed()[0]['source_fingerprint']
rows=monitor([project],'restore-qualification')
Path('evidence/restore.json').write_text(json.dumps({'restore':restored,'publication':publication,'monitor':rows,'paid_requests':0},indent=2))
print(restored)
