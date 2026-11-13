import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from forge_workshop_kit import WorkshopSession, training


def test_candidate_source_and_subprocess_logs_use_utf8(tmp_path, monkeypatch):
    source = '# Forecast café — Ω 東京\nVALUE = "solar ☀"\n'
    directory = tmp_path / 'prévisions'
    seen = []

    def run(command, **kwargs):
        seen.append(command)
        assert kwargs['encoding'] == 'utf-8'
        assert kwargs['env']['PYTHONUTF8'] == '1'
        assert kwargs['env']['PYTHONIOENCODING'] == 'utf-8'
        request = json.loads(Path(command[-1]).read_text(encoding='utf-8'))
        assert Path(request['source']).read_bytes() == source.encode('utf-8')
        np.save(request['prediction'], np.zeros((2, 1)))
        Path(request['losses']).write_text('[]', encoding='utf-8')
        return SimpleNamespace(returncode=0, stdout='résultat Ω\n', stderr='注記\n')

    monkeypatch.setattr(training.subprocess, 'run', run)
    split = {'x': np.zeros((2, 1)), 'y': np.zeros((2, 1)),
             'mask': np.ones((2, 1)), 'persistence': np.ones((2, 1))}
    result, _ = training.train(source, split, split, {'seed': 17}, directory)
    assert len(seen) == 1 and result['exit_code'] == 0
    assert (directory / 'stdout.txt').read_bytes() == 'résultat Ω\n'.encode('utf-8')
    assert (directory / 'stderr.txt').read_bytes() == '注記\n'.encode('utf-8')


def test_unicode_draft_and_record_survive_session_restart(tmp_path):
    session = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    source = '# Prédiction — 東京\ndef forecast(x):\n    return x\n'
    session.save_draft('model', source)
    with session.stage('source', sources={'candidate.py': source}) as stage:
        path = stage.output_dir / 'candidate.py'
        path.write_text(source, encoding='utf-8', newline='\n')
        stage.record({'note': '☀ validation seulement'}, files=[path])
    restarted = WorkshopSession('person/lab', 'test', state_dir=tmp_path)
    assert restarted.get_draft('model') == source
    with restarted.stage('source', sources={'candidate.py': source}) as cached:
        assert not cached.needs_run
        assert cached.result['note'] == '☀ validation seulement'
    assert restarted.file(restarted.read()['stages'][stage.id]['files'][0]).read_bytes() == source.encode('utf-8')
