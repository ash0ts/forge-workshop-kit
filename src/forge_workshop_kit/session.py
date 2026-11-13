"""Local receipts plus optional W&B publication. No server and no hidden execution."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import threading
import time
import uuid
from contextlib import contextmanager
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path

from filelock import FileLock, Timeout as FileLockTimeout


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
        # The anchor belongs to the notebook; its collection name changes on rename.
        identity = notebook_identity or os.getenv('WANDB_NOTEBOOK_ANCHOR_RUN') or os.getenv('WANDB_NOTEBOOK_COLLECTION')
        try:
            self.kit_version = package_version('forge-workshop-kit')
        except PackageNotFoundError:
            self.kit_version = 'source'
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
        self._progress_guard = threading.Lock()
        self._progress_thread = None
        self._progress_pending = False
        self.state_path = self.root / 'journal.json'
        if not self.state_path.exists():
            write_json(self.state_path, dict(stages={}, progress={}, publications={}, requests={}))

    @classmethod
    def from_environment(cls, workshop, *, project=None, **kwargs):
        hosted = os.getenv('WANDB_NOTEBOOK_ANCHOR_RUN') or os.getenv('WANDB_NOTEBOOK_COLLECTION')
        environment_project = '/'.join((os.getenv('WANDB_ENTITY', ''), os.getenv('WANDB_PROJECT', '')))
        if not project:
            project = environment_project if hosted and all(environment_project.split('/')) else os.getenv('WORKSHOP_PROJECT')
        if not project and all(environment_project.split('/')):
            project = environment_project
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

    def stage(self, name, *, config=None, sources=None, inputs=None, attempt=None):
        spec = dict(name=name, config=config or {}, sources=sources or {}, inputs=inputs or {})
        if attempt is None:
            base = digest([self.workspace_id, {**spec, 'attempt': 1}])[:32]
            state = self.read()
            previous = [row for row in state['stages'].values() if all(row.get(k) == v for k, v in spec.items())]
            completed = [row for row in previous if row['status'] == 'complete']
            attempt = max((row['attempt'] for row in completed or previous), default=1)
            if not completed:
                attempt = state.get('retries', {}).get(base, {}).get('attempt', attempt)
        return Stage(self, **spec, attempt=attempt)

    def recovery_options(self):
        """Read-only recovery choices. An execution never restarts from rendering this list."""
        state = self.read()
        options = []
        for row in state['stages'].values():
            if row['status'] not in ('failed', 'interrupted', 'running'):
                continue
            spec = {k: row[k] for k in ('name', 'config', 'sources', 'inputs')}
            base = digest([self.workspace_id, {**spec, 'attempt': 1}])[:32]
            route = state.get('retries', {}).get(base, {})
            if route.get('attempt', row['attempt']) > row['attempt']:
                continue
            requests = [r for key, r in state['requests'].items()
                        if key == row['id'] or key.startswith(row['id'] + '/')]
            uncertain = any(r['status'] in ('pending', 'interrupted') for r in requests)
            options.append(dict(id=row['id'], name=row['name'], status=row['status'],
                error=row.get('error', ''), has_uncertain_requests=uncertain,
                next_attempt=row['attempt'] + 1))
        return options

    def retry_stage(self, stage_id, *, reason='Retry requested from notebook', confirm_stopped=False):
        """Authorize one new attempt. The normal Run control starts it, never this method."""
        if not reason.strip():
            raise ValueError('Describe why another execution is needed.')
        with self.transaction() as state:
            row = state['stages'][stage_id]
            if row['status'] == 'complete':
                raise StageNeedsReview('This execution is complete. Retry its publication instead.')
            requests = [r for key, r in state['requests'].items()
                        if key == stage_id or key.startswith(stage_id + '/')]
            uncertain = [r for r in requests if r['status'] in ('pending', 'interrupted')]
            if (uncertain or row['status'] == 'running') and not confirm_stopped:
                raise StageNeedsReview('Confirm the previous execution has stopped before authorizing another attempt. Its unresolved requests remain charged at their full reservation.')
            spec = {k: row[k] for k in ('name', 'config', 'sources', 'inputs')}
            siblings = [s for s in state['stages'].values() if all(s[k] == v for k, v in spec.items())]
            if any(s['status'] == 'complete' for s in siblings):
                raise StageNeedsReview('A matching execution already completed. Reopen its saved result.')
            base = digest([self.workspace_id, {**spec, 'attempt': 1}])[:32]
            attempt = max(s['attempt'] for s in siblings) + 1
            route = state.setdefault('retries', {}).get(base)
            if route and route['attempt'] >= attempt:
                return route
            for request in uncertain:
                request.update(status='interrupted', unknown_usd=request['reserved_usd'],
                               observed_usd=None, ended_at=time.time(), updated_at=time.time(),
                               error='Previous execution confirmed stopped: ' + reason)
            for request in requests:
                if request['status'] == 'reserved':
                    request.update(status='cancelled', observed_usd=0, unknown_usd=0,
                                   ended_at=time.time(), updated_at=time.time(),
                                   error='Unsent reservation replaced by an explicit retry.')
            if row['status'] == 'running':
                row.update(status='interrupted', ended_at=time.time(), error=reason)
            route = dict(attempt=attempt, previous=stage_id, reason=reason, authorized_at=time.time())
            state['retries'][base] = route
            return route

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
        if self.publisher:
            receipt = self._publish_progress_receipt()
            return {**receipt, 'url': receipt.get('result')}
        return self.read()['progress']

    def _publish_progress_receipt(self):
        started = time.time()
        try:
            result = self.publisher.publish_progress()
            receipt = {'status': 'published', 'result': result, 'updated_at': time.time()}
        except FileLockTimeout:
            receipt = {'status': 'queued', 'message': 'A progress update is already in flight.',
                       'updated_at': started}
        except Exception as error:
            receipt = {'status': 'unavailable', 'error': str(error)[:500],
                       'updated_at': time.time()}
        with self.transaction() as state:
            current = state['publications'].get('publish_progress', {})
            if receipt['updated_at'] >= current.get('updated_at', 0):
                state['publications']['publish_progress'] = receipt
            else:
                receipt = dict(current)
        return receipt

    def queue_progress(self):
        """Publish the latest progress in the background; execution never waits for it."""
        if not self.publisher:
            return
        with self._progress_guard:
            self._progress_pending = True
            if self._progress_thread is not None:
                return

            def publish_latest():
                while True:
                    with self._progress_guard:
                        if not self._progress_pending:
                            self._progress_thread = None
                            return
                        self._progress_pending = False
                    try:
                        self._publish_progress_receipt()
                    except Exception:
                        pass  # A failed local receipt write cannot block execution.

            self._progress_thread = threading.Thread(target=publish_latest, daemon=True)
            self._progress_thread.start()

    def retry_publication(self):
        if not self.publisher:
            return {'status': 'local', 'message': 'Connect to publish saved work.'}
        outcomes = {}
        for operation in ('publish_progress', 'publish_stages', 'publish_checkpoint'):
            if operation == 'publish_progress':
                outcomes[operation] = self._publish_progress_receipt()
                continue
            try:
                outcomes[operation] = {'status': 'published', 'result': getattr(self.publisher, operation)()}
            except Exception as error:
                outcomes[operation] = {'status': 'unavailable', 'error': str(error)[:500]}
        with self.transaction() as state:
            state['publications'].update({key: value for key, value in outcomes.items()
                                          if key != 'publish_progress'})
            outcomes['publish_progress'] = dict(state['publications']['publish_progress'])
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

    def save_draft(self, name, value):
        """Save an edit locally. A later checkpoint includes it; no provider call occurs."""
        json.dumps(value, allow_nan=False)
        with self.transaction() as state:
            state.setdefault('drafts', {})[name] = {
                'value': value, 'fingerprint': digest(value), 'updated_at': time.time()}
        return value

    def get_draft(self, name, default=None):
        return self.read().get('drafts', {}).get(name, {}).get('value', default)

    def set_view(self, step):
        """Browsing is separate from completing an exercise."""
        with self.transaction() as state:
            state.setdefault('view', {})['step'] = str(step)
        return step

    def get_view(self, default='setup'):
        return self.read().get('view', {}).get('step', default)

    def mark_interrupted(self, stage_id, reason):
        """Explicit recovery after the operator confirms the old process has stopped."""
        if not reason.strip():
            raise ValueError('Record why this execution is known to have stopped.')
        with self.transaction() as state:
            row=state['stages'][stage_id]
            if row['status']=='complete':
                raise ValueError('Do not interrupt a completed execution.')
            row.update(status='interrupted',error=reason,ended_at=time.time())
            for key,request in state['requests'].items():
                if key.startswith(stage_id+'/') and request['status']=='pending':
                    request.update(status='interrupted',unknown_usd=request['reserved_usd'],
                                   observed_usd=None,error=reason,ended_at=time.time())
            state['progress'].update(status='interrupted',step=row['name'],updated_at=time.time())

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
                started_at=time.time(), source_fingerprint=self.source_fingerprint, files=[],
                kit_version=self.session.kit_version)
            state['progress'].update(step=self.name, status='running', updated_at=time.time())
        self.needs_run = True
        self.session.queue_progress()
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

    def record_event(self, receipt):
        """Keep tool evidence even when the operation raises before a final result exists."""
        json.dumps(receipt, allow_nan=False)
        with self.session.transaction() as state:
            events = state['stages'][self.id].setdefault('events', [])
            if any(row['id'] == receipt['id'] for row in events):
                raise ValueError('An event with this identity is already recorded.')
            events.append(receipt)

    def __exit__(self, kind, error, traceback):
        if not self.needs_run:
            return False
        with self.session.transaction() as state:
            row = state['stages'][self.id]
            if error is not None and row['status'] == 'complete':
                row.setdefault('post_execution_errors', []).append(
                    dict(error=f'{kind.__name__}: {error}'[:1000], at=time.time()))
            elif error is not None:
                row.update(status='failed', error=f'{kind.__name__}: {error}'[:1000], ended_at=time.time())
                # Preserve known local logs without uploading arbitrary participant files.
                row['files'] = sorted(set(row.get('files', []) + [str(p.relative_to(self.session.root)) for p in self.output_dir.iterdir() if p.is_file() and p.name in ('candidate.py','stderr.txt','stdout.txt','partial.json','losses.json','office.json')]))
                state['progress'].update(status='failed', step=self.name, updated_at=time.time())
            elif row['status'] != 'complete':
                row.update(status='interrupted', error='Stage exited without recording a result.',
                           ended_at=time.time())
        self.session.queue_progress()
        return False
