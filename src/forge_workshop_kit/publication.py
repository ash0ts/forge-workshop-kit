"""Publish saved receipts. None of these functions train a model or call inference."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import time
import uuid
from pathlib import Path
from functools import wraps

from filelock import FileLock

from .session import digest, safe_name, write_json


def credentials():
    import wandb
    key = os.getenv('WANDB_API_KEY') or wandb.Api().api_key
    if not key:
        raise PermissionError('No Forge login. Locally run uv run wandb login. Hosted: reopen your editable notebook session.')
    return key


def _serialized(method):
    @wraps(method)
    def publish(self, *args, **kwargs):
        # Publication does not hold the journal lock or block execution writes.
        with FileLock(str(self.session.root / '.publication.lock'), timeout=180):
            return method(self, *args, **kwargs)
    return publish


class Publisher:
    def __init__(self, session):
        import wandb
        self.session = session
        self.entity, self.project = session.project.split('/')
        self.api = wandb.Api(api_key=credentials(), timeout=30)

    @_serialized
    def check_access(self):
        result = self.api._service_api.execute_graphql(
            'query($e:String!,$p:String!){project(entityName:$e,name:$p){name internalId}}',
            {'e': self.entity, 'p': self.project})
        if not result.get('project'):
            raise PermissionError('Project is absent or unreadable. Create it in your own Forge account first.')
        # A progress write verifies write access without inference or training.
        with self.run(self.session.workspace_id[:20]+'-access', 'Project access check', 'workshop-access') as run:
            run.summary['write_verified'] = True
        return dict(project=self.session.project, write_access=True, model_calls=0,
                    compute='Notebook CPU; no separate workshop service')

    def run(self, run_id, name, job_type, config=None):
        import wandb
        try:
            return wandb.init(entity=self.entity, project=self.project, id=run_id,
                name=name, job_type=job_type, resume='allow', reinit='create_new',
                config={'workshop_id': self.session.workshop, 'workshop_version': self.session.version,
                        'workspace_id': self.session.workspace_id,
                        'notebook_identity': self.session.identity.get('notebook_identity'), **(config or {})},
                settings=wandb.Settings(disable_git=True, init_timeout=45,
                    finish_timeout=60, finish_timeout_raises=True))
        except Exception as error:
            if 'run id' in str(error).lower() and 'in use' in str(error).lower():
                raise RuntimeError(
                    'The W&B SDK retained a stream after initialization failed. '
                    'Restart the notebook kernel, restore saved work, and choose Retry publication. '
                    'Do not rerun the completed experiment.') from error
            raise

    def publish_progress(self):
        # A slow artifact upload cannot delay a help request or progress update.
        with FileLock(str(self.session.root / '.progress-publication.lock'), timeout=0):
            return self._publish_progress()

    def _publish_progress(self):
        import wandb
        state = self.session.read()
        progress = {**state['progress'], 'failed_executions':[
            r['name'] for r in state['stages'].values() if r['status']=='failed']}
        summary = {**progress, 'updated_at': progress.get('updated_at', time.time())}
        path = self.session.project + '/' + self.session.workspace_id[:24]
        try:
            run = self.api.run(path)
        except (wandb.errors.CommError, ValueError) as error:
            if not any(term in str(error).lower() for term in ('not found', 'could not find', 'does not exist')):
                raise
            with self.run(self.session.workspace_id[:24], self.session.workshop + ' / progress',
                          'workshop-progress') as run:
                run.summary.update(summary)
                return run.url
        run.summary.update(summary)
        return run.url

    @_serialized
    def publish_stages(self):
        import wandb
        result = {}
        for stage in self.session.read()['stages'].values():
            if stage['status'] == 'running':
                continue
            if stage.get('published'):
                result[stage['id']] = stage['published']
                continue
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                files = {}
                with self.session.lock:
                    for index, relative in enumerate(stage['files']):
                        source = _safe_file(self.session.root, relative)
                        content = source.read_bytes()
                        name = f'files/{index}/' + source.name
                        destination = root / name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(content)
                        files[relative] = {'artifact_path': name, 'sha256': hashlib.sha256(content).hexdigest()}
                    write_json(root / 'execution.json', stage)
                _seal_snapshot(root)
                with self.run(stage['id'], stage['name'], 'workshop-experiment', {
                        'stage': stage['name'], 'source_fingerprint': stage['source_fingerprint'],
                        'experiment': stage['config'], 'inputs': stage['inputs']}) as run:
                    run.summary.update({'status': stage['status'], 'seconds': stage.get('ended_at', time.time()) - stage['started_at']})
                    value = stage.get('result', {})
                    if isinstance(value, dict):
                        run.summary.update(value.get('metrics', {}))
                        for step, loss in enumerate(value.get('losses', [])):
                            run.log({'training_step': step, 'training_loss': loss})
                        if value.get('trace'):
                            run.summary['agent_lens'] = value['trace'].get('url')
                    artifact = wandb.Artifact('execution-' + stage['id'], type='workshop-execution')
                    for path in sorted(root.rglob('*')):
                        if path.is_file():
                            artifact.add_file(str(path), name=path.relative_to(root).as_posix())
                    logged = run.log_artifact(artifact).wait(timeout=120)
                    for details in files.values():
                        details['reference'] = logged.get_entry(details['artifact_path']).ref_url()
                    result[stage['id']] = run.url
                    with self.session.transaction() as state:
                        state['stages'][stage['id']].update(published=result[stage['id']],
                            artifact_url=logged.url, artifact_ref=logged.qualified_name, artifact_files=files)
        return result

    def _publish_snapshot(self, directory, name, kind, metadata):
        import wandb
        root = Path(directory)
        artifact = wandb.Artifact(name, type=kind, metadata=metadata)
        for path in sorted(root.rglob('*')):
            if path.is_file():
                artifact.add_file(str(path), name=path.relative_to(root).as_posix())
        with self.run(self.session.workspace_id[:20] + '-files',
                      self.session.workshop + ' / saved files', 'workshop-checkpoint') as run:
            logged = run.log_artifact(artifact, aliases=['latest']).wait(timeout=120)
        return logged.qualified_name

    @_serialized
    def publish_checkpoint(self):
        """Upload immutable copied bytes, not a journal that can change during upload."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.session.lock:
                state = self.session.read()
                references = {}
                paths = {'identity.json': self.session.root / 'identity.json',
                         'journal.json': self.session.state_path}
                for stage in state['stages'].values():
                    for relative in stage.get('files', []):
                        published = stage.get('artifact_files', {}).get(relative)
                        if published and stage.get('artifact_ref') and published.get('sha256'):
                            references[relative] = {
                                'artifact': stage['artifact_ref'],
                                'artifact_path': published['artifact_path'],
                                'sha256': published['sha256']}
                        else:
                            paths[relative] = self.session.file(relative)
                for relative, source in paths.items():
                    _safe_file(self.session.root, relative)
                    destination = _safe_file(root, relative)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(source.read_bytes())
                write_json(root / 'checkpoint.json', {'captured_at': time.time()})
                write_json(root / 'output-references.json', references)
            _seal_snapshot(root)
            return self._publish_snapshot(root, 'workspace-' + self.session.workspace_id,
                'workshop-checkpoint', self.session.identity)

    @_serialized
    def publish_request_ledger(self):
        """Save request recovery and accounting without uploading trained outputs."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.session.lock:
                state = self.session.read()
                ledger = {key: state[key] for key in _ACCOUNTING_KEYS if key in state}
                write_json(root / 'identity.json', self.session.identity)
                write_json(root / 'ledger.json', {'captured_at': time.time(), 'state': ledger})
            _seal_snapshot(root)
            return self._publish_snapshot(root, 'requests-' + self.session.workspace_id,
                'workshop-request-ledger', self.session.identity)

    def _artifact(self, name, kind):
        import wandb
        try:
            return self.api.artifact(name, type=kind)
        except wandb.errors.CommError as error:
            if 'not found' in str(error).lower() or 'does not exist' in str(error).lower():
                return None
            raise

    def _restore_outputs(self, root, checksums, state):
        """Resolve explicit immutable entries without W&B's dependency-count limit."""
        if 'output-references.json' not in checksums:
            return {}  # Older checkpoints embedded files or native artifact references.
        references = json.loads((root / 'output-references.json').read_text())
        allowed = {path for stage in state['stages'].values() for path in stage.get('files', [])}
        artifacts, verified = {}, {}
        for relative, reference in references.items():
            destination = _safe_file(root, relative)
            if relative not in allowed or relative in checksums:
                raise ValueError('Checkpoint references an unexpected output.')
            name = reference['artifact']
            if not re.fullmatch(re.escape(self.session.project) + r'/[^/:]+:v[0-9]+', name):
                raise ValueError('Checkpoint output must use an immutable artifact in this project.')
            entry = reference['artifact_path']
            _safe_file(root, entry)
            if name not in artifacts:
                artifacts[name] = self.api.artifact(name, type='workshop-execution')
            with tempfile.TemporaryDirectory() as directory:
                downloaded = artifacts[name].get_entry(entry).download(root=directory)
                content = Path(downloaded).read_bytes()
            checksum = hashlib.sha256(content).hexdigest()
            if checksum != reference['sha256']:
                raise ValueError('Checkpoint output checksum mismatch')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            verified[relative] = checksum
        return verified

    def restore(self, artifact=None):
        """Verify a complete snapshot, then install files before its completion journal."""
        saved = self._artifact(artifact or
            f'{self.session.project}/workspace-{self.session.workspace_id}:latest',
            'workshop-checkpoint')
        ledger = self._artifact(
            f'{self.session.project}/requests-{self.session.workspace_id}:latest',
            'workshop-request-ledger')
        if saved is None and ledger is None:
            return {'status': 'new', 'completed': 0}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint_root, ledger_root = root / 'checkpoint', root / 'requests'
            checkpoint_state, request_state, checksums = None, None, {}
            checkpoint_time = 0
            if saved is not None:
                saved.download(root=str(checkpoint_root))
                checksums = _verify_snapshot(checkpoint_root, self.session.identity)
                if 'journal.json' not in checksums:
                    raise ValueError('Checkpoint has no verified journal.')
                checkpoint_state = json.loads((checkpoint_root / 'journal.json').read_text())
                checksums.update(self._restore_outputs(checkpoint_root, checksums, checkpoint_state))
                for stage in checkpoint_state['stages'].values():
                    if any(relative not in checksums for relative in stage.get('files', [])):
                        raise ValueError('Checkpoint omits an execution output.')
                if 'checkpoint.json' in checksums:
                    checkpoint_time = json.loads((checkpoint_root / 'checkpoint.json').read_text())['captured_at']
            if ledger is not None:
                ledger.download(root=str(ledger_root))
                ledger_checksums = _verify_snapshot(ledger_root, self.session.identity)
                if 'ledger.json' not in ledger_checksums:
                    raise ValueError('Request artifact has no verified ledger.')
                request_state = json.loads((ledger_root / 'ledger.json').read_text())
            # A failed download or checksum has made no changes to the workspace.
            with self.session.lock:
                local = self.session.read()
                restored = checkpoint_state if checkpoint_state is not None else local
                restored = json.loads(json.dumps(restored))
                _merge_accounting(restored, local)
                if request_state is not None:
                    _merge_accounting(restored, request_state['state'],
                        include_provider_state=request_state['captured_at'] >= checkpoint_time)
                # Existing local work wins over an older downloaded checkpoint.
                if checkpoint_state is not None:
                    _merge_local_work(restored, local)
                    for relative in checksums:
                        if relative in ('identity.json', 'journal.json', 'checkpoint.json', 'output-references.json'):
                            continue
                        destination = _safe_file(self.session.root, relative)
                        content = (checkpoint_root / relative).read_bytes()
                        if destination.exists() and destination.read_bytes() != content:
                            raise ValueError('Restored output conflicts with a local file; no journal was replaced.')
                    for relative in checksums:
                        if relative in ('identity.json', 'journal.json', 'checkpoint.json', 'output-references.json'):
                            continue
                        _atomic_bytes(_safe_file(self.session.root, relative),
                                      (checkpoint_root / relative).read_bytes())
                write_json(self.session.state_path, restored)
        return {'status': 'restored', 'completed': len(self.session.completed())}


_ACCOUNTING_KEYS = ('requests', 'accounting_stop', 'provider_failures', 'provider_cooldown')


def _safe_file(root, relative):
    root = Path(root).resolve()
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Unsafe checkpoint path')
    destination = root / path
    if any(parent.is_symlink() for parent in (destination, *destination.parents) if parent != root):
        raise ValueError('Unsafe checkpoint path')
    if not destination.resolve().is_relative_to(root):
        raise ValueError('Unsafe checkpoint path')
    return destination


def _atomic_bytes(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    try:
        temporary.write_bytes(content)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _seal_snapshot(root, referenced_checksums=None):
    key = credentials().encode()
    checksums = dict(referenced_checksums or {})
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        content = path.read_bytes()
        if len(key) > 15 and key in content:
            raise ValueError('A selected checkpoint file contains the active credential. Remove it before publishing.')
        checksums[path.relative_to(root).as_posix()] = hashlib.sha256(content).hexdigest()
    write_json(root / 'checksums.json', checksums)


def _verify_snapshot(root, identity):
    root = Path(root)
    checksums = json.loads((root / 'checksums.json').read_text())
    if 'identity.json' not in checksums:
        raise ValueError('Checkpoint has no verified identity.')
    for relative, checksum in checksums.items():
        source = _safe_file(root, relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != checksum:
            raise ValueError('Checkpoint checksum mismatch')
    saved_identity = json.loads((root / 'identity.json').read_text())
    stable = ('project', 'workshop', 'version', 'workspace_id', 'notebook_identity')
    if any(saved_identity.get(key) != identity.get(key) for key in stable):
        raise ValueError('Checkpoint belongs to another notebook, project, or release.')
    return checksums


def _request_time(row):
    return row.get('updated_at') or row.get('ended_at') or row.get('started_at') or 0


def _merge_accounting(target, source, *, include_provider_state=True):
    requests = target.setdefault('requests', {})
    for key, incoming in source.get('requests', {}).items():
        current = requests.get(key)
        if current is None:
            requests[key] = incoming
            continue
        for field in ('request_fingerprint', 'envelope_fingerprint'):
            if current.get(field) and incoming.get(field) and current[field] != incoming[field]:
                raise ValueError('Saved request identity has conflicting provider settings.')
        if current.get('status') == 'complete' and incoming.get('status') != 'complete':
            continue
        if ((incoming.get('status') == 'complete' and current.get('status') != 'complete')
                or _request_time(incoming) > _request_time(current)):
            requests[key] = incoming
    if source.get('accounting_stop'):
        target['accounting_stop'] = source['accounting_stop']
    if include_provider_state:
        for key in ('provider_failures', 'provider_cooldown'):
            if key in source:
                target[key] = source[key]


def _merge_local_work(restored, local):
    for key, row in local.get('stages', {}).items():
        previous = restored.setdefault('stages', {}).get(key)
        if previous is None or (previous.get('status') != 'complete' and
                (row.get('status') == 'complete' or _request_time(row) >= _request_time(previous))):
            restored['stages'][key] = row
    for key, row in local.get('drafts', {}).items():
        previous = restored.setdefault('drafts', {}).get(key, {})
        if _request_time(row) >= _request_time(previous):
            restored['drafts'][key] = row
    def merge_receipts(saved, newer):
        merged = dict(saved)
        for key, value in newer.items():
            old = merged.get(key)
            if isinstance(old, dict) and isinstance(value, dict):
                merged[key] = merge_receipts(old, value)
            elif (key.endswith('status') and old == 'published') or (key == 'verified' and old is True):
                continue
            else:
                merged[key] = value
        return merged
    restored['publications'] = merge_receipts(restored.get('publications', {}), local.get('publications', {}))
    if _request_time(local.get('progress', {})) >= _request_time(restored.get('progress', {})) and local.get('progress'):
        restored['progress'] = local['progress']
    if local.get('view'):
        restored['view'] = local['view']
    for key in ('retries', 'recovery'):
        if local.get(key):
            restored.setdefault(key, {}).update(local[key])


def monitor(projects, workshop_id, *, api=None):
    """Compatibility entry point; monitoring has no publication dependencies."""
    from .monitoring import monitor as read_progress
    return read_progress(projects, workshop_id, api=api)


def _save_comparison_receipt(session, key, label, record):
    with session.transaction() as state:
        state['publications'].setdefault(key, {})[label] = dict(record)


def publish_comparison(session, name, versions):
    """Publish saved rows once per destination; retries do not execute predictions."""
    from filelock import FileLock
    publisher = session.connect()
    receipt_key = 'comparison/' + digest([name, versions])[:24]
    # Two notebook cells may retry publication, but must not publish the same rows together.
    with FileLock(str(session.root / ('.' + receipt_key.replace('/', '-') + '.lock'))):
        for label, rows in versions.items():
            run_id = digest([session.workspace_id, name, label, rows])[:32]
            record = dict(session.read()['publications'].get(receipt_key, {}).get(label, {}))
            # Older receipts were saved only after the W&B table had been written.
            if record.get('run') and 'wandb_status' not in record:
                record['wandb_status'] = 'published'
            record.update(comparison_name=name, condition=label, run_id=run_id)
            def save():
                _save_comparison_receipt(session, receipt_key, label, record)
            if record.get('wandb_status') != 'published':
                try:
                    import wandb
                    with publisher.run(run_id, name + ' / ' + label, 'workshop-evaluation', {'condition': label}) as run:
                        table = wandb.Table(columns=['case_id', 'input', 'prediction', 'target', 'error', 'scores', 'evidence'],
                            data=[[r['case_id'], json.dumps(r['input']), json.dumps(r['prediction']),
                                   json.dumps(r['target']), r.get('error'), json.dumps(r.get('scores', {})),
                                   json.dumps(r.get('evidence', {}))] for r in rows])
                        run.log({'comparison': table})
                        available = [r['error'] for r in rows if r.get('error') is not None]
                        run.summary[name + '/error_mean'] = sum(available) / len(available) if available else None
                        run.summary['available_scores'] = len(available)
                        run.summary['planned_scores'] = len(rows)
                        url = run.url
                    record.update(wandb_status='published', run=url)
                    record.pop('wandb_error', None)
                except Exception as error:
                    record.update(wandb_status='unavailable', wandb_error=str(error)[:400])
                save()
            if record.get('weave_status') != 'published':
                try:
                    import weave
                    weave.init(session.project)
                    dataset = weave.Dataset(name=safe_name(name + '-' + label + '-cases'), rows=rows)
                    if not record.get('dataset'):
                        record['dataset'] = weave.publish(dataset).uri()
                        save()
                    @weave.op()
                    def saved_prediction(case_id: str):
                        return next(row for row in rows if row['case_id'] == case_id)['prediction']
                    @weave.op()
                    def saved_score(case_id: str, output):
                        row = next(row for row in rows if row['case_id'] == case_id)
                        if output != row['prediction']:
                            raise ValueError('Saved prediction differs from execution')
                        return {'error': row.get('error'), **row.get('scores', {})}
                    from .execution import run_async
                    evaluation = weave.Evaluation(name=safe_name(name + '-' + label + '-evaluation'), dataset=dataset, scorers=[saved_score])
                    if not record.get('weave_evaluated'):
                        run_async(lambda: evaluation.evaluate(saved_prediction))
                        record['weave_evaluated'] = True
                        save()
                    if not record.get('evaluation'):
                        record['evaluation'] = weave.publish(evaluation, name=safe_name(name + '-' + label + '-evaluation')).uri()
                        save()
                    weave.get_client().flush()
                    record.update(weave_status='published')
                    record.pop('weave_error', None)
                except Exception as error:
                    record.update(weave_status='unavailable', weave_error=str(error)[:400])
                save()
            if record.get('native_status') != 'published':
                try:
                    with publisher.run(run_id, name + ' / ' + label, 'workshop-evaluation', {'condition': label}) as run:
                        try:
                            if not record.get('native'):
                                record['native'] = native_table(run, rows, name)
                                save()
                            run.log({'eval_table': record['native']})
                            record.update(native_status='published')
                            record.pop('native_error', None)
                        except Exception as error:
                            # An optional native destination outage does not fail the saved W&B evaluation.
                            record.update(native_status='unavailable', native_error=str(error)[:400])
                except Exception as error:
                    record.update(native_status='unavailable', native_error=str(error)[:400])
                save()
        return session.read()['publications'][receipt_key]


def native_table(run, rows, name):
    import wandb
    from coreweave_evaluations import Client
    api = wandb.Api()
    scope = api._service_api.execute_graphql(
        'query($e:String!,$p:String!){project(entityName:$e,name:$p){internalId}}',
        {'e': run.entity, 'p': run.project})['project']['internalId']
    def key(operation):
        return digest([run.id, name, operation])
    score_names=sorted({'error'} | {key for row in rows for key in row.get('scores',{})})
    with Client(base_url='https://evaluations.wandb.ai', api_key=credentials(), scope_id=scope) as client:
        table = client.eval_tables.create(name=safe_name(name), idempotency_key=key('create'))
        client.eval_tables.columns.create(table.evaluation_id,
            dataset_fields=[{'source': source, 'name': field, 'value_type': 'string'}
                for source, fields in [('input', ['case_id', 'input']),
                                       ('output', ['prediction', 'target', 'evidence'])] for field in fields],
            scorers=[{'name': key, 'value_type': 'number'} for key in score_names], idempotency_key=key('columns'))
        for i in range(0, len(rows), 100):
            client.eval_tables.rows.add(table.evaluation_id, rows=[{
                'input': {'case_id': r['case_id'], 'input': json.dumps(r['input'])},
                'output': {'prediction': json.dumps(r['prediction']), 'target': json.dumps(r['target']),
                           'evidence': json.dumps(r.get('evidence', {}))},
                'scores': {k:v for k,v in {'error':r.get('error'),**r.get('scores',{})}.items() if v is not None}}
                for r in rows[i:i+100]], idempotency_key=key('rows-' + str(i)))
        version = client.eval_tables.versions.create(table.evaluation_id, idempotency_key=key('version'))
    return dict(_type='eval-table-ces', schema_version=1, ncols=6, nrows=len(rows),
        evaluation_id=table.evaluation_id, evaluation_version_id=version.evaluation_version_id,
        dataset_id=table.dataset_id, dataset_version_id=version.dataset_version_id, log_mode='IMMUTABLE')


def publish_report(session, conclusion, links):
    import wandb_workspaces.reports.v2 as wr
    if not conclusion.strip():
        raise ValueError('Write your conclusion before publishing.')
    receipt_key = 'report-' + digest([conclusion, links])
    saved = session.read()['publications'].get(receipt_key)
    if saved:
        url=saved['url']
        entity=session.project.split('/')[0]
        if url.startswith('https://forge.coreweave.com/') and not url.startswith('https://forge.coreweave.com/wandb/'+entity+'/'):
            url=url.replace('https://forge.coreweave.com/','https://forge.coreweave.com/wandb/',1)
        return url
    entity, project = session.project.split('/')
    report = wr.Report(entity=entity, project=project, title=session.workshop + ': ' + session.workspace_id[:8],
        description='A participant experiment with saved code, predictions, and research-agent traces.')
    report.blocks = [wr.H1(text='What I tested'), wr.P(text=conclusion),
        wr.H2(text='Evidence'), *[wr.P(text=f'{label}: {url}') for label, url in links.items()],
        wr.PanelGrid(runsets=[wr.Runset(entity=entity, project=project,
            filters=f'Config("workspace_id") == "{session.workspace_id}"')],
            panels=[wr.ScalarChart(title='Image final error',metric='solar-images-final/error_mean'),
                    wr.ScalarChart(title='Measurement final error',metric='solar-measurements-final/error_mean')]
                    if session.workshop=='solar-autoresearch' else [wr.ScalarChart(title='Final case error',metric='pending-final/error_mean')])]
    report.save()
    url=report.url
    if url.startswith('https://forge.coreweave.com/') and not url.startswith('https://forge.coreweave.com/wandb/'+entity+'/'):
        url=url.replace('https://forge.coreweave.com/','https://forge.coreweave.com/wandb/',1)
    with session.transaction() as state:
        state['publications'][receipt_key] = {'url': url}
    return url
