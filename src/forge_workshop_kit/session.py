"""Local receipts plus optional W&B publication. No server and no hidden execution."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from filelock import FileLock


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def safe_name(value):
    return re.sub(r'[^a-zA-Z0-9_.-]', '-', value)[:80]


class StageNeedsReview(RuntimeError):
    pass


class WorkshopSession:
    def __init__(self, project, workshop, *, version='1', state_dir=None, budget_usd=8,
                 publisher=None, notebook_identity=None):
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', project):
            raise ValueError('Use entity/project, for example your-name/solar-research.')
        if not 0 < float(budget_usd) < float('inf'):
            raise ValueError('The inference allowance must be a positive finite amount.')
        self.project, self.workshop, self.version = project, workshop, version
        self.budget_usd = float(budget_usd)
        # Collection identifies a copied hosted notebook, not its short-lived session.
        identity = notebook_identity or os.getenv('WANDB_NOTEBOOK_COLLECTION')
        self.root = Path(state_dir or Path('.workshop') / safe_name(workshop) /
                         (digest([project, identity])[:20] if identity else 'local')).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = FileLock(str(self.root / '.lock'))
        with self.lock:
            path = self.root / 'identity.json'
            if path.exists():
                saved = json.loads(path.read_text())
                if (saved['project'], saved['workshop'], saved['version']) != (
                        project, workshop, version):
                    raise ValueError('This workspace belongs to another project or release. Use a new state_dir.')
                if saved.get('notebook_identity') != identity:
                    raise ValueError('Notebook identity changed. Use a new state_dir for this copy.')
            else:
                saved = dict(project=project, workshop=workshop, version=version,
                             workspace_id=digest([project, workshop, version, identity])[:24]
                             if identity else uuid.uuid4().hex,
                             notebook_identity=identity)
                write_json(path, saved)
        self.identity = saved
        self.workspace_id = saved['workspace_id']
        self.publisher = publisher
        self.state_path = self.root / 'journal.json'
        if not self.state_path.exists():
            write_json(self.state_path, dict(stages={}, progress={}, publications={}, requests={}))

    @classmethod
    def from_environment(cls, workshop, *, project=None, **kwargs):
        project = project or os.getenv('WORKSHOP_PROJECT')
        if not project and os.getenv('WANDB_ENTITY') and os.getenv('WANDB_PROJECT'):
            project = os.environ['WANDB_ENTITY'] + '/' + os.environ['WANDB_PROJECT']
        if not project:
            raise ValueError('Choose a writable entity/project. Locally, set WORKSHOP_PROJECT before opening the notebook.')
        if os.getenv('WORKSHOP_STATE_DIR'):
            kwargs.setdefault('state_dir',os.environ['WORKSHOP_STATE_DIR'])
        return cls(project, workshop, **kwargs)

    @contextmanager
    def transaction(self):
        with self.lock:
            state = self.read()
            yield state
            write_json(self.state_path, state)

    def read(self):
        return json.loads(self.state_path.read_text())

    def connect(self):
        from .publication import Publisher
        self.publisher = self.publisher or Publisher(self)
        return self.publisher

    def check_access(self):
        return self.connect().check_access()

    def stage(self, name, *, config=None, sources=None, inputs=None, attempt=1):
        return Stage(self, name, config or {}, sources or {}, inputs or {}, attempt)

    def checkpoint(self, step, *, evidence=None, publish=True):
        with self.transaction() as state:
            progress = state['progress']
            progress.update(step=step, status='complete', updated_at=time.time())
            progress['completed'] = sorted(set(progress.get('completed', []) + [step]))
            progress['evidence'] = {**progress.get('evidence', {}), **(evidence or {})}
        if publish and self.publisher:
            return self.retry_publication()
        return self.read()['progress']

    def request_help(self, message):
        with self.transaction() as state:
            state['progress'].update(help_request=message, updated_at=time.time())
        return self.retry_publication() if self.publisher else self.read()['progress']

    def retry_publication(self):
        if not self.publisher:
            return {'status': 'local', 'message': 'Connect to publish saved work.'}
        outcomes = {}
        for operation in ('publish_stages', 'publish_progress', 'publish_checkpoint'):
            try:
                outcomes[operation] = {'status': 'published', 'result': getattr(self.publisher, operation)()}
            except Exception as error:
                outcomes[operation] = {'status': 'unavailable', 'error': str(error)[:500]}
        with self.transaction() as state:
            state['publications'].update(outcomes)
        return outcomes

    def restore(self, *, artifact=None):
        """Explicitly restore receipts; never execute or automatically retry interrupted work."""
        if self.read()['stages'] or self.read()['requests']:
            return {'status': 'local', 'completed': len(self.completed())}
        if not self.publisher:
            return {'status': 'local', 'completed': 0}
        return self.publisher.restore(artifact)

    def completed(self):
        return [s for s in self.read()['stages'].values() if s['status'] == 'complete']

    def file(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('File must belong to this workspace.')
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def export_files(self):
        """An explicit set, never a recursive upload of the runtime or home directory."""
        paths = [self.root / 'identity.json', self.state_path]
        for stage in self.read()['stages'].values():
            for relative in stage.get('files', []):
                path = self.file(relative)
                if path.is_file():
                    paths.append(path)
        return sorted(set(paths))


class Stage:
    def __init__(self, session, name, config, sources, inputs, attempt):
        self.session, self.name = session, name
        self.spec = dict(name=name, config=config, sources=sources, inputs=inputs, attempt=attempt)
        self.id = digest([session.workspace_id, self.spec])[:32]
        self.source_fingerprint = digest(sources)
        self.output_dir = session.file('outputs/' + self.id)
        self.needs_run = False
        self.result = None

    def __enter__(self):
        with self.session.transaction() as state:
            previous = state['stages'].get(self.id)
            if previous:
                if previous['status'] == 'complete':
                    self.result = previous['result']
                    return self
                raise StageNeedsReview(
                    f'{self.name} has a saved {previous["status"]} attempt. Inspect it; '
                    'choose an explicit new attempt only if another execution is intended.')
            self.output_dir.mkdir(parents=True, exist_ok=True)
            state['stages'][self.id] = dict(id=self.id, **self.spec, status='running',
                started_at=time.time(), source_fingerprint=self.source_fingerprint, files=[])
            state['progress'].update(step=self.name, status='running', updated_at=time.time())
        self.needs_run = True
        if self.session.publisher:
            try:
                self.session.publisher.publish_progress()
            except Exception:
                pass  # Monitoring never blocks participant work.
        return self

    def record(self, result, *, files=()):
        if not self.needs_run:
            raise StageNeedsReview('This completed stage is cached. Do not run or record it again.')
        copies = []
        for path in map(Path, files):
            if not path.is_file():
                raise ValueError(f'Missing output file: {path}')
            if path.resolve().is_relative_to(self.output_dir):
                destination = path.resolve()
            else:
                destination = self.output_dir / path.name
                if destination.exists() and destination.read_bytes() != path.read_bytes():
                    raise ValueError('Two outputs have the same filename.')
                shutil.copy2(path, destination)
            copies.append(str(destination.relative_to(self.session.root)))
        # Serialize before changing completion state. NaN is not a missing score.
        json.dumps(result, allow_nan=False)
        self.result = result
        with self.session.transaction() as state:
            state['stages'][self.id].update(result=result, files=copies, status='complete',
                                           ended_at=time.time())

    def __exit__(self, kind, error, traceback):
        if not self.needs_run:
            return False
        with self.session.transaction() as state:
            row = state['stages'][self.id]
            if error is not None:
                row.update(status='failed', error=f'{kind.__name__}: {error}'[:1000], ended_at=time.time())
                # Preserve known local logs without uploading arbitrary participant files.
                row['files'] = sorted(set(row.get('files', []) + [str(p.relative_to(self.session.root)) for p in self.output_dir.iterdir() if p.is_file() and p.name in ('candidate.py','stderr.txt','stdout.txt','partial.json','losses.json')]))
                state['progress'].update(status='failed', step=self.name, updated_at=time.time())
            elif row['status'] != 'complete':
                row.update(status='interrupted', error='Stage exited without recording a result.',
                           ended_at=time.time())
        if self.session.publisher:
            try:
                self.session.publisher.publish_progress()
            except Exception:
                pass
        return False
