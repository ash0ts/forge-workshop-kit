import hashlib
import json
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit import publication


def session(tmp_path, name='local'):
    return WorkshopSession('test/project', 'lab', state_dir=tmp_path / name,
                           notebook_identity='notebook-a')


def seal(files):
    files = dict(files)
    files['checksums.json'] = json.dumps({
        key: hashlib.sha256(content).hexdigest() for key, content in files.items()
    }).encode()
    return files


def snapshot(workspace):
    return seal({str(path.relative_to(workspace.root)): path.read_bytes()
                 for path in workspace.export_files()})


def ledger(workspace, state, captured_at=1000):
    return seal({'identity.json': json.dumps(workspace.identity).encode(),
                 'ledger.json': json.dumps({'captured_at': captured_at, 'state': state}).encode()})


class Artifact:
    def __init__(self, files):
        self.files = files

    def download(self, root):
        for relative, content in self.files.items():
            path = Path(root) / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)


class Api:
    def __init__(self, checkpoint=None, requests=None):
        self.saved = {'workshop-checkpoint': checkpoint, 'workshop-request-ledger': requests}

    def artifact(self, name, *, type):
        import wandb
        files = self.saved[type]
        if files is None:
            raise wandb.errors.CommError('not found')
        return Artifact(files)


def publisher(workspace, checkpoint=None, requests=None):
    result = publication.Publisher.__new__(publication.Publisher)
    result.session = workspace
    result.api = Api(checkpoint, requests)
    workspace.publisher = result
    return result


def completed(workspace):
    with workspace.stage('train', sources={'model.py': 'fixed-source'}) as stage:
        path = stage.output_dir / 'weights.txt'
        path.write_text('trained-once')
        stage.record({'error': 0.2}, files=[path])
    return stage


def test_checkpoint_upload_reads_fixed_snapshot_and_ledger_has_no_outputs(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    stage = completed(workspace)
    with workspace.transaction() as state:
        state['requests']['request/0'] = {'status': 'pending', 'reserved_usd': 0.1}
    pub = publisher(workspace)
    monkeypatch.setattr(publication, 'credentials', lambda: 'fake-test-credential')
    captured = {}
    def upload(directory, name, kind, metadata):
        # Mutation after the lock must not change bytes selected for upload.
        with workspace.transaction() as state:
            state['progress']['step'] = 'next'
        root = Path(directory)
        captured[kind] = {p.relative_to(root).as_posix(): p.read_bytes()
                          for p in root.rglob('*') if p.is_file()}
        publication._verify_snapshot(root, workspace.identity)
        return name + ':v0'
    monkeypatch.setattr(pub, '_publish_snapshot', upload)
    pub.publish_checkpoint()
    frozen = json.loads(captured['workshop-checkpoint']['journal.json'])
    assert frozen['progress'].get('step') != 'next'
    assert frozen['stages'][stage.id]['status'] == 'complete'
    pub.publish_request_ledger()
    small = captured['workshop-request-ledger']
    assert set(small) == {'identity.json', 'ledger.json', 'checksums.json'}
    assert json.loads(small['ledger.json'])['state']['requests']['request/0']['reserved_usd'] == 0.1
    assert not any('weights' in path for path in small)


def test_restore_verifies_every_file_before_touching_workspace(tmp_path):
    old = session(tmp_path, 'before')
    stage = completed(old)
    files = snapshot(old)
    files['outputs/' + stage.id + '/weights.txt'] = b'corrupt'
    fresh = session(tmp_path, 'after')
    original = fresh.state_path.read_bytes()
    with pytest.raises(ValueError, match='checksum'):
        publisher(fresh, files).restore()
    assert fresh.state_path.read_bytes() == original
    assert not fresh.file('outputs/' + stage.id + '/weights.txt').exists()


def test_interrupted_restore_commits_journal_last_and_retry_recovers(tmp_path, monkeypatch):
    old = session(tmp_path, 'before')
    stage = completed(old)
    fresh = session(tmp_path, 'after')
    pub = publisher(fresh, snapshot(old))
    original = fresh.state_path.read_bytes()
    write = publication._atomic_bytes
    def fail_after_write(path, content):
        write(path, content)
        raise OSError('disk interrupted')
    monkeypatch.setattr(publication, '_atomic_bytes', fail_after_write)
    with pytest.raises(OSError, match='interrupted'):
        pub.restore()
    assert fresh.state_path.read_bytes() == original
    monkeypatch.setattr(publication, '_atomic_bytes', write)
    assert pub.restore()['completed'] == 1
    assert fresh.read()['stages'][stage.id]['status'] == 'complete'


def test_restore_merges_newer_ledger_without_downgrading_complete_request(tmp_path):
    old = session(tmp_path, 'before')
    completed(old)
    with old.transaction() as state:
        state['requests'] = {
            'a': {'status': 'pending', 'updated_at': 1, 'reserved_usd': .1},
            'b': {'status': 'complete', 'updated_at': 2, 'observed_usd': .02}}
    fresh = session(tmp_path, 'after')
    recent = ledger(old, {'requests': {
        'a': {'status': 'complete', 'updated_at': 3, 'observed_usd': .03},
        'b': {'status': 'failed', 'updated_at': 4, 'unknown_usd': .1},
        'c': {'status': 'pending', 'transport_state': 'sent', 'updated_at': 5, 'reserved_usd': .2}},
        'accounting_stop': 'review request'})
    assert publisher(fresh, snapshot(old), recent).restore()['completed'] == 1
    state = fresh.read()
    assert state['requests']['a']['observed_usd'] == .03
    assert state['requests']['b']['status'] == 'complete'
    assert state['requests']['c']['transport_state'] == 'sent'
    assert state['accounting_stop'] == 'review request'


def test_ledger_only_restore_preserves_a_request_before_first_checkpoint(tmp_path):
    workspace = session(tmp_path)
    requests = {'requests': {'a': {'status': 'pending', 'transport_state': 'sent', 'reserved_usd': .1}}}
    assert publisher(workspace, requests=ledger(workspace, requests)).restore()['completed'] == 0
    assert workspace.read()['requests'] == requests['requests']


def test_restore_rejects_missing_output_and_conflicting_request_identity(tmp_path):
    old = session(tmp_path, 'before')
    stage = completed(old)
    raw = {p: v for p, v in snapshot(old).items() if not p.startswith('outputs/') and p != 'checksums.json'}
    fresh = session(tmp_path, 'after')
    with pytest.raises(ValueError, match='omits an execution output'):
        publisher(fresh, seal(raw)).restore()
    state = {'requests': {'a': {'request_fingerprint': 'first', 'status': 'complete'}}}
    with pytest.raises(ValueError, match='conflicting provider settings'):
        publication._merge_accounting(state, {'requests': {'a': {'request_fingerprint': 'second'}}})


def mock_destinations(monkeypatch, workspace):
    calls = {'comparison': 0, 'native_log': 0, 'evaluate': 0, 'dataset': 0, 'evaluation': 0, 'flush': 0}
    class Run:
        id = 'run-id'
        url = 'https://example.test/run'
        def __init__(self):
            self.summary = {}
        def log(self, value):
            if 'comparison' in value:
                calls['comparison'] += 1
            if 'eval_table' in value:
                calls['native_log'] += 1
    @contextmanager
    def run(*args, **kwargs):
        yield Run()
    workspace.publisher = SimpleNamespace(run=run)
    class Dataset:
        def __init__(self, **kwargs):
            pass
    class Evaluation:
        def __init__(self, **kwargs):
            pass
        async def evaluate(self, fn):
            calls['evaluate'] += 1
            assert fn('case-1') == 'saved'
    def publish(obj, **kwargs):
        kind = 'dataset' if isinstance(obj, Dataset) else 'evaluation'
        calls[kind] += 1
        return SimpleNamespace(uri=lambda: 'weave:///' + kind)
    def flush():
        calls['flush'] += 1
    monkeypatch.setitem(sys.modules, 'wandb', SimpleNamespace(Table=lambda **kwargs: kwargs))
    monkeypatch.setitem(sys.modules, 'weave', SimpleNamespace(
        init=lambda project: None, Dataset=Dataset, Evaluation=Evaluation,
        publish=publish, op=lambda: (lambda fn: fn),
        get_client=lambda: SimpleNamespace(flush=flush)))
    return calls


VERSIONS = {'model': [{'case_id': 'case-1', 'input': 'input', 'prediction': 'saved',
                       'target': 'saved', 'error': None}]}


def test_comparison_retry_skips_each_successful_destination(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    calls = mock_destinations(monkeypatch, workspace)
    attempts = []
    def native(*args):
        attempts.append(1)
        if len(attempts) == 1:
            raise RuntimeError('native unavailable')
        return {'evaluation_id': 'saved-native-id'}
    monkeypatch.setattr(publication, 'native_table', native)
    first = publication.publish_comparison(workspace, 'comparison', VERSIONS)['model']
    assert first['native_status'] == 'unavailable'
    assert first['wandb_status'] == first['weave_status'] == 'published'
    second = publication.publish_comparison(workspace, 'comparison', VERSIONS)['model']
    assert second['native_status'] == 'published'
    assert calls == dict(comparison=1, native_log=1, evaluate=1, dataset=1, evaluation=1, flush=1)
    publication.publish_comparison(workspace, 'comparison', VERSIONS)
    assert len(attempts) == 2 and calls['comparison'] == calls['evaluate'] == 1


def test_comparison_interrupt_retains_finished_channels(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    calls = mock_destinations(monkeypatch, workspace)
    monkeypatch.setattr(publication, 'native_table', lambda *args: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        publication.publish_comparison(workspace, 'comparison', VERSIONS)
    record = next(iter(workspace.read()['publications'].values()))['model']
    assert record['wandb_status'] == record['weave_status'] == 'published'
    monkeypatch.setattr(publication, 'native_table', lambda *args: {'evaluation_id': 'saved-native-id'})
    publication.publish_comparison(workspace, 'comparison', VERSIONS)
    assert calls['comparison'] == calls['evaluate'] == 1


def test_weave_flush_retry_does_not_repeat_saved_evaluation(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    calls = mock_destinations(monkeypatch, workspace)
    monkeypatch.setattr(publication, 'native_table', lambda *args: {'evaluation_id': 'saved-native-id'})
    def flush():
        calls['flush'] += 1
        if calls['flush'] == 1:
            raise RuntimeError('export interrupted')
    sys.modules['weave'].get_client = lambda: SimpleNamespace(flush=flush)
    first = publication.publish_comparison(workspace, 'comparison', VERSIONS)['model']
    assert first['weave_status'] == 'unavailable' and first['weave_evaluated']
    publication.publish_comparison(workspace, 'comparison', VERSIONS)
    assert calls['flush'] == 2 and calls['evaluate'] == calls['dataset'] == calls['evaluation'] == 1


def test_published_outputs_are_referenced_without_reading_them_again(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    stage = completed(workspace)
    pub = publisher(workspace)
    monkeypatch.setattr(publication, 'credentials', lambda: 'fake-test-credential')
    files = {}
    class Uploaded:
        url = 'https://example.test/artifact'
        qualified_name = 'test/project/execution:v0'
        def wait(self, timeout=None):
            return self
        def get_entry(self, name):
            return SimpleNamespace(ref_url=lambda: 'wandb-artifact://immutable-id/' + name)
    class PendingArtifact:
        def __init__(self, name, type):
            pass
        def add_file(self, path, *, name):
            files[name] = Path(path).read_bytes()
    class Run:
        summary = {}
        url = 'https://example.test/run'
        def log_artifact(self, artifact):
            return Uploaded()
    @contextmanager
    def run(*args, **kwargs):
        yield Run()
    monkeypatch.setattr(pub, 'run', run)
    monkeypatch.setitem(sys.modules, 'wandb', SimpleNamespace(Artifact=PendingArtifact))
    pub.publish_stages()
    row = workspace.read()['stages'][stage.id]
    output = stage.output_dir / 'weights.txt'
    reference = row['artifact_files'][str(output.relative_to(workspace.root))]
    assert reference['sha256'] == hashlib.sha256(b'trained-once').hexdigest()
    read_bytes = Path.read_bytes
    def no_output_reread(path):
        if path == output:
            raise AssertionError('Completed outputs were read again')
        return read_bytes(path)
    monkeypatch.setattr(Path, 'read_bytes', no_output_reread)
    def upload(directory, name, kind, metadata):
        root = Path(directory)
        references = json.loads((root / 'output-references.json').read_text())
        assert list(references.values())[0]['artifact'] == row['artifact_ref']
        assert not (root / 'outputs').exists()
        publication._verify_snapshot(root, workspace.identity)
        return 'checkpoint:v0'
    monkeypatch.setattr(pub, '_publish_snapshot', upload)
    assert pub.publish_checkpoint() == 'checkpoint:v0'


def test_stale_complete_ledger_cannot_overwrite_newer_complete_receipt():
    current = {'requests': {'a': {'status': 'complete', 'updated_at': 20, 'observed_usd': .03}}}
    publication._merge_accounting(current, {'requests': {'a': {
        'status': 'complete', 'updated_at': 10, 'observed_usd': .01}}})
    assert current['requests']['a']['observed_usd'] == .03


def test_native_outage_does_not_fail_the_existing_wandb_run(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    mock_destinations(monkeypatch, workspace)
    original_run = workspace.publisher.run
    context_errors = []
    @contextmanager
    def observed_run(*args, **kwargs):
        with original_run(*args, **kwargs) as run:
            try:
                yield run
            except Exception as error:
                context_errors.append(error)
                raise
    workspace.publisher.run = observed_run
    monkeypatch.setattr(publication, 'native_table', lambda *args: (_ for _ in ()).throw(RuntimeError('HTTP 500')))
    result = publication.publish_comparison(workspace, 'comparison', VERSIONS)
    assert result['model']['native_status'] == 'unavailable'
    assert context_errors == []


def test_checkpoint_restores_more_than_five_execution_artifacts(tmp_path, monkeypatch):
    old = session(tmp_path, 'before')
    outputs = {}
    for index in range(7):
        with old.stage(f'train-{index}', sources={'model.py': str(index)}) as stage:
            path = stage.output_dir / 'weights.txt'
            content = f'weights-{index}'.encode()
            path.write_bytes(content)
            stage.record({'error': .2}, files=[path])
        relative = path.relative_to(old.root).as_posix()
        artifact_name = f'test/project/execution-{stage.id}:v0'
        outputs[artifact_name] = {'files/weights.txt': content}
        with old.transaction() as state:
            state['stages'][stage.id].update(artifact_ref=artifact_name, artifact_files={relative: {
                'artifact_path': 'files/weights.txt', 'sha256': hashlib.sha256(content).hexdigest()}})
    pub = publisher(old)
    monkeypatch.setattr(publication, 'credentials', lambda: 'fake-test-credential')
    saved = {}
    def upload(directory, name, kind, metadata):
        saved.update({p.relative_to(directory).as_posix(): p.read_bytes()
                      for p in Path(directory).rglob('*') if p.is_file()})
        assert not any(name.startswith('outputs/') for name in saved)
        assert len(json.loads(saved['output-references.json'])) == 7
        return 'test/project/checkpoint:v0'
    monkeypatch.setattr(pub, '_publish_snapshot', upload)
    pub.publish_checkpoint()
    fresh = session(tmp_path, 'after')
    restored = publisher(fresh, saved)
    lookup = restored.api.artifact
    def artifact(name, *, type):
        if type != 'workshop-execution':
            return lookup(name, type=type)
        def entry(path):
            def download(root):
                destination = Path(root) / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(outputs[name][path])
                return str(destination)
            return SimpleNamespace(download=download)
        return SimpleNamespace(get_entry=entry)
    restored.api.artifact = artifact
    assert restored.restore()['completed'] == 7
    for stage in fresh.read()['stages'].values():
        assert fresh.file(stage['files'][0]).read_bytes().startswith(b'weights-')
    assert not fresh.file('output-references.json').exists()
    # An altered referenced output must not install even the earlier valid files.
    damaged = session(tmp_path, 'damaged')
    damaged_pub = publisher(damaged, saved)
    damaged_pub.api.artifact = artifact
    outputs[next(iter(outputs))]['files/weights.txt'] = b'corrupt'
    before = damaged.state_path.read_bytes()
    with pytest.raises(ValueError, match='output checksum'):
        damaged_pub.restore()
    assert damaged.state_path.read_bytes() == before
    assert not list(damaged.root.glob('outputs/*/weights.txt'))


def test_progress_updates_existing_public_run_without_opening_sdk_stream(tmp_path):
    workspace = session(tmp_path)
    pub = publisher(workspace)
    public_run = SimpleNamespace(url='https://example.test/progress', summary={})
    pub.api.run = lambda path: public_run
    def forbidden(*args, **kwargs):
        raise AssertionError('Existing progress must not reopen an SDK run')
    pub.run = forbidden
    with workspace.transaction() as state:
        state['progress'].update(step='baseline', completed=['baseline'])
    assert pub.publish_progress() == public_run.url
    assert public_run.summary['step'] == 'baseline'


def test_publication_serializes_snapshots_without_locking_execution_journal(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    import threading
    workspace = session(tmp_path)
    pubs = [publisher(workspace), publisher(workspace)]
    monkeypatch.setattr(publication, 'credentials', lambda: 'fake-test-credential')
    entered, release = threading.Event(), threading.Event()
    captured = []
    def upload(directory, name, kind, metadata):
        captured.append(json.loads((Path(directory) / 'ledger.json').read_text()))
        if len(captured) == 1:
            entered.set()
            assert release.wait(3)
        return 'requests:v0'
    for pub in pubs:
        monkeypatch.setattr(pub, '_publish_snapshot', upload)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(pubs[0].publish_request_ledger)
        assert entered.wait(3)
        second = pool.submit(pubs[1].publish_request_ledger)
        # Execution state remains writable while a network publication is blocked.
        with workspace.transaction() as state:
            state['requests']['new'] = {'status': 'pending', 'reserved_usd': .1}
        release.set()
        first.result(timeout=3)
        second.result(timeout=3)
    assert len(captured) == 2
    assert 'new' not in captured[0]['state']['requests']
    assert 'new' in captured[1]['state']['requests']


def test_progress_is_not_queued_behind_artifact_upload_lock(tmp_path):
    from filelock import FileLock
    workspace = session(tmp_path)
    pub = publisher(workspace)
    run = SimpleNamespace(url='https://example.test/progress', summary={})
    pub.api.run = lambda path: run
    with FileLock(str(workspace.root / '.publication.lock')):
        assert pub.publish_progress() == run.url


def test_stage_artifact_receipt_survives_run_finish_failure(tmp_path, monkeypatch):
    workspace = session(tmp_path)
    stage = completed(workspace)
    pub = publisher(workspace)
    monkeypatch.setattr(publication, 'credentials', lambda: 'fake-test-credential')
    uploads = []
    class Uploaded:
        url = 'https://example.test/artifact'
        qualified_name = 'test/project/execution:v0'
        def wait(self, timeout=None):
            return self
        def get_entry(self, path):
            return SimpleNamespace(ref_url=lambda: 'wandb-artifact://id/' + path)
    class PendingArtifact:
        def __init__(self, *args, **kwargs):
            pass
        def add_file(self, *args, **kwargs):
            pass
    class Run:
        url = 'https://example.test/run'
        summary = {}
        def log_artifact(self, artifact):
            uploads.append(artifact)
            return Uploaded()
    @contextmanager
    def run(*args, **kwargs):
        yield Run()
        raise TimeoutError('Finish upload exceeded its deadline')
    monkeypatch.setattr(pub, 'run', run)
    monkeypatch.setitem(sys.modules, 'wandb', SimpleNamespace(Artifact=PendingArtifact))
    with pytest.raises(TimeoutError, match='Finish upload'):
        pub.publish_stages()
    assert workspace.read()['stages'][stage.id]['artifact_ref'].endswith(':v0')
    assert pub.publish_stages() == {stage.id: Run.url}
    assert len(uploads) == 1
