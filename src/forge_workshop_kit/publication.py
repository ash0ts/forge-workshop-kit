"""Publish saved receipts. None of these functions train a model or call inference."""
from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path

from .session import digest, safe_name, write_json


def credentials():
    import wandb
    key = os.getenv('WANDB_API_KEY') or wandb.Api().api_key
    if not key:
        raise PermissionError('No Forge login. Locally run uv run wandb login. Hosted: reopen your editable notebook session.')
    return key


class Publisher:
    def __init__(self, session):
        import wandb
        self.session = session
        self.entity, self.project = session.project.split('/')
        self.api = wandb.Api(api_key=credentials(), timeout=30)

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
        return wandb.init(entity=self.entity, project=self.project, id=run_id,
            name=name, job_type=job_type, resume='allow', reinit='create_new',
            config={'workshop_id': self.session.workshop, 'workshop_version': self.session.version,
                    'workspace_id': self.session.workspace_id, **(config or {})},
            settings=wandb.Settings(disable_git=True, init_timeout=45))

    def publish_progress(self):
        state = self.session.read()
        progress = {**state['progress'], 'failed_executions':[r['name'] for r in state['stages'].values() if r['status']=='failed']}
        with self.run(self.session.workspace_id[:24], self.session.workshop + ' / progress',
                      'workshop-progress') as run:
            run.summary.update({**progress, 'updated_at': progress.get('updated_at', time.time())})
            return run.url

    def publish_stages(self):
        import wandb
        result = {}
        for stage in self.session.read()['stages'].values():
            if stage['status'] == 'running':
                continue
            if stage.get('published'):
                result[stage['id']] = stage['published']
                continue
            with self.run(stage['id'], stage['name'], 'workshop-experiment', {
                    'stage': stage['name'], 'source_fingerprint': stage['source_fingerprint'],
                    'experiment': stage['config'], 'inputs': stage['inputs']}) as run:
                run.summary.update({'status':stage['status'], 'seconds':stage.get('ended_at', time.time()) - stage['started_at']})
                value = stage.get('result', {})
                if isinstance(value, dict):
                    run.summary.update(value.get('metrics', {}))
                    for step, loss in enumerate(value.get('losses', [])):
                        run.log({'training_step': step, 'training_loss': loss})
                    if value.get('trace'):
                        run.summary['agent_lens'] = value['trace'].get('url')
                artifact = wandb.Artifact('execution-' + stage['id'], type='workshop-execution')
                with artifact.new_file('execution.json') as stream:
                    json.dump(stage, stream, indent=2, allow_nan=False)
                for file in stage['files']:
                    artifact.add_file(str(self.session.file(file)), name=Path(file).name)
                run.log_artifact(artifact).wait()
                result[stage['id']] = run.url
            with self.session.transaction() as state:
                state['stages'][stage['id']]['published'] = result[stage['id']]
        return result

    def publish_checkpoint(self):
        import wandb
        with self.run(self.session.workspace_id[:24], self.session.workshop + ' / progress',
                      'workshop-progress') as run:
            run.summary.update(self.session.read()['progress'])
            artifact = wandb.Artifact('workspace-' + self.session.workspace_id,
                type='workshop-checkpoint', metadata=self.session.identity)
            checksums = {}
            for path in self.session.export_files():
                relative = str(path.relative_to(self.session.root))
                content = path.read_bytes()
                # Never upload a literal credential copied into learner code or receipts.
                key = credentials().encode()
                if len(key) > 15 and key in content:
                    raise ValueError('A selected checkpoint file contains the active credential. Remove it before publishing.')
                import hashlib
                checksums[relative] = hashlib.sha256(content).hexdigest()
                artifact.add_file(str(path), name=relative)
            with artifact.new_file('checksums.json') as stream:
                json.dump(checksums, stream)
            run.log_artifact(artifact, aliases=['latest']).wait()
            return artifact.qualified_name

    def restore(self, artifact=None):
        import hashlib
        import wandb
        name = artifact or f'{self.session.project}/workspace-{self.session.workspace_id}:latest'
        try:
            saved = self.api.artifact(name, type='workshop-checkpoint')
        except wandb.errors.CommError as error:
            if 'not found' in str(error).lower() or 'does not exist' in str(error).lower():
                return {'status': 'new', 'completed': 0}
            raise
        with tempfile.TemporaryDirectory() as directory:
            saved.download(root=directory)
            root = Path(directory).resolve()
            identity = json.loads((root / 'identity.json').read_text())
            if identity != self.session.identity:
                raise ValueError('Checkpoint belongs to another notebook, project, or release.')
            checksums = json.loads((root / 'checksums.json').read_text())
            for name, checksum in checksums.items():
                source = (root / name).resolve()
                if not source.is_relative_to(root) or source.is_symlink():
                    raise ValueError('Unsafe checkpoint path')
                if hashlib.sha256(source.read_bytes()).hexdigest() != checksum:
                    raise ValueError('Checkpoint checksum mismatch')
            for name in checksums:
                self.session.file(name).write_bytes((root / name).read_bytes())
        return {'status': 'restored', 'completed': len(self.session.completed())}


def monitor(projects, workshop_id, *, api=None):
    """Only reads project runs. No writes, agents, tokens, or participant remote control."""
    import wandb
    api = api or wandb.Api(timeout=20)
    rows = []
    for project in projects:
        project = project.strip()
        if project.startswith('https://'):
            from urllib.parse import urlparse
            parts=urlparse(project).path.strip('/').split('/')
            if parts[0]=='wandb' and len(parts)>2: parts=parts[1:]
            project='/'.join(parts[:2])
        if not project:
            continue
        try:
            runs = list(api.runs(project, filters={
                'jobType': 'workshop-progress', 'config.workshop_id': workshop_id}))
            for run in runs:
                summary = dict(run.summary._json_dict)
                rows.append(dict(project=project, workspace=run.config.get('workspace_id'),
                    step=summary.get('step', 'Not started'), status=summary.get('status', 'unknown'),
                    completed=len(summary.get('completed', [])), failed=summary.get('failed_executions',[]), help=summary.get('help_request', ''),
                    updated_at=summary.get('updated_at'), evidence=summary.get('evidence', {}), url=run.url))
            if not runs:
                rows.append(dict(project=project, status='unknown', step='No progress run yet'))
        except Exception as error:
            rows.append(dict(project=project, status='unavailable', error=str(error)[:300]))
    return rows


def publish_comparison(session, name, versions):
    """versions: {label: [{case_id, input, prediction, target, error, ...}]}.

    Stable case_id is the native alignment key. Errors stay numeric and missing stays null.
    """
    import wandb
    import weave
    publisher = session.connect()
    receipt_key = 'comparison/' + digest([name, versions])[:24]
    cached = session.read()['publications'].get(receipt_key, {})
    receipts = dict(cached)
    for label, rows in versions.items():
        run_id = digest([session.workspace_id, name, label, rows])[:32]
        with publisher.run(run_id, name + ' / ' + label, 'workshop-evaluation', {'condition': label}) as run:
            table = wandb.Table(columns=['case_id', 'input', 'prediction', 'target', 'error', 'scores', 'evidence'],
                data=[[r['case_id'], json.dumps(r['input']), json.dumps(r['prediction']),
                       json.dumps(r['target']), r.get('error'), json.dumps(r.get('scores', {})), json.dumps(r.get('evidence', {}))] for r in rows])
            run.log({'comparison': table})
            available=[r['error'] for r in rows if r.get('error') is not None]
            run.summary[name+'/error_mean']=sum(available)/len(available) if available else None
            run.summary['available_scores']=len(available)
            run.summary['planned_scores']=len(rows)
            record = receipts.setdefault(label, {'run': run.url})
            # Separate publication failures. A native outage cannot erase Weave or local results.
            if record.get('weave_status') != 'published':
                try:
                    weave.init(session.project)
                    dataset = weave.Dataset(name=safe_name(name + '-' + label + '-cases'), rows=rows)
                    ref = weave.publish(dataset)
                    @weave.op()
                    def saved_prediction(case_id: str):
                        return next(row for row in rows if row['case_id'] == case_id)['prediction']
                    @weave.op()
                    def saved_score(case_id: str, output):
                        row = next(row for row in rows if row['case_id'] == case_id)
                        if output != row['prediction']:
                            raise ValueError('Saved prediction differs from execution')
                        return {'error': row.get('error'), **row.get('scores',{})}
                    import asyncio
                    evaluation = weave.Evaluation(name=safe_name(name + '-' + label + '-evaluation'), dataset=dataset, scorers=[saved_score])
                    # Publication replays saved outputs, never inference or training.
                    asyncio.run(evaluation.evaluate(saved_prediction))
                    evaluation_ref=weave.publish(evaluation, name=safe_name(name+'-'+label+'-evaluation'))
                    weave.get_client().flush()
                    record.pop('weave_error',None)
                    record.update(weave_status='published', dataset=ref.uri(), evaluation=evaluation_ref.uri())
                except Exception as error:
                    record.update(weave_status='unavailable', weave_error=str(error)[:400])
            if record.get('native_status') != 'published':
                try:
                    native = native_table(run, rows, name)
                    run.log({'eval_table': native})
                    record.update(native_status='published', native=native)
                except Exception as error:
                    record.update(native_status='unavailable', native_error=str(error)[:400])
        with session.transaction() as state:
            state['publications'][receipt_key] = receipts
    return receipts


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
