import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from filelock import FileLock, Timeout

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit import session as session_module
from forge_workshop_kit.factory import FactoryTask, TaskBoard


@pytest.mark.parametrize('store', ['session', 'board'])
def test_atomic_writes_wait_for_open_reads(tmp_path, monkeypatch, store):
    if store == 'session':
        reader = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
        writer = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
        read = reader.read
        path = reader.state_path
    else:
        tasks = [FactoryTask('query', 'Find departures', 'Implement query', ('query.py',))]
        reader = TaskBoard(tmp_path, tasks, {'query.py': 'value = 0\n'})
        writer = TaskBoard(tmp_path, tasks, {'query.py': 'value = 0\n'})
        read = reader.snapshot
        path = reader.path
    before = read()
    writer.lock.timeout = 0
    entered = threading.Event()
    release = threading.Event()
    original_read = Path.read_text

    def hold_read(opened_path, *args, **kwargs):
        if opened_path == path and threading.current_thread().name.startswith('reader'):
            # Windows may reject replacing a file while this handle is open.
            with opened_path.open(encoding='utf-8') as source:
                entered.set()
                assert release.wait(5), 'Test did not release the file reader.'
                return source.read()
        return original_read(opened_path, *args, **kwargs)

    monkeypatch.setattr(Path, 'read_text', hold_read)
    with ThreadPoolExecutor(max_workers=1, thread_name_prefix='reader') as pool:
        pending_read = pool.submit(read)
        try:
            assert entered.wait(5), 'Reader did not open the saved record.'
            with pytest.raises(Timeout), writer.transaction() as state:
                state['marker'] = 'new receipt'
        finally:
            release.set()
        assert pending_read.result(timeout=5) == before

    with writer.transaction() as state:
        state['marker'] = 'new receipt'
    assert read()['marker'] == 'new receipt'


def test_first_journal_creation_holds_workspace_lock(tmp_path, monkeypatch):
    entered = threading.Event()
    release = threading.Event()
    original_exists = Path.exists

    def hold_creation(path):
        exists = original_exists(path)
        if (path == tmp_path / 'journal.json' and not exists
                and threading.current_thread().name.startswith('initializer')):
            entered.set()
            assert release.wait(5), 'Test did not release journal initialization.'
        return exists

    monkeypatch.setattr(Path, 'exists', hold_creation)
    monkeypatch.setattr(session_module, 'FileLock', lambda path: FileLock(path, timeout=0))
    with ThreadPoolExecutor(max_workers=1, thread_name_prefix='initializer') as pool:
        pending = pool.submit(WorkshopSession, 'person/lab', 'test', state_dir=tmp_path)
        try:
            assert entered.wait(5), 'Journal initialization did not start.'
            with pytest.raises(Timeout):
                WorkshopSession('person/lab', 'test', state_dir=tmp_path)
        finally:
            release.set()
        session = pending.result(timeout=5)

    session.checkpoint('baseline', publish=False)
    reopened = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    assert reopened.read()['progress']['completed'] == ['baseline']
