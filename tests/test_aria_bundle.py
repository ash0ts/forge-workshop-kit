import json
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_release import build_aria_bundle


def recording_checkout(root):
    folder = root / 'src/forge_workshop_kit/assets/aria/example'
    folder.mkdir(parents=True)
    stops = []
    for stop in ('investigate', 'conclusion'):
        record = {'id': 'actual-' + stop, 'workshop': 'example', 'stop_id': stop, 'status': 'recorded',
                  'prompt': 'Actual submitted question', 'response': 'Actual recorded answer',
                  'records': [{'identity':'stage-id'}], 'citation_check': {'assessment':'unresolved'},
                  'captures': [{'role': role, 'path': stop + '-' + role + '.png'} for role in ('response','verification')],
                  'excerpt_path': stop + '-source.json',
                  'transcript_paths': {'html': stop + '-transcript.html', 'markdown': stop + '-transcript.md'}}
        for capture in record['captures']:
            (folder / capture['path']).write_bytes(b'recorded image fixture')
        (folder / record['excerpt_path']).write_text('{"recording_id":"actual-' + stop + '"}')
        for file in record['transcript_paths'].values():
            (folder / file).write_text('Actual captured response with context-access limitation.')
        (folder / (stop + '.json')).write_text(json.dumps(record))
        stops.append({'id':stop,'recorded_example':'aria/example/' + stop + '.json'})
    (root / 'src/forge_workshop_kit/workshops.json').write_text(json.dumps({'templates':[
        {'slug':'example','id':'example-workshop','aria_investigations':stops},
        {'slug':'facilitator','id':'facilitator','aria_investigations':[]}]}))
    for name in ('LICENSE','src/forge_workshop_kit/aria.py','scripts/build_aria_recordings.py','docs/aria-investigations.md'):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('Public kit source or documentation')
    (root / '.env').write_text('NOT_FOR_PUBLICATION')
    return folder


def test_standalone_recording_archive_is_complete_and_reproducible(tmp_path):
    root = tmp_path / 'checkout'
    recording_checkout(root)
    result = build_aria_bundle(tmp_path / 'release', '0.10.0', root=root)
    assert result['recordings'] == 2
    assert result['file'] == 'aria-investigations-v0.10.0.zip'
    with zipfile.ZipFile(tmp_path / 'release' / result['file']) as bundle:
        assert len(bundle.namelist()) == result['files']
        assert 'LICENSE' in bundle.namelist()
        assert 'src/forge_workshop_kit/aria.py' in bundle.namelist()
        assert '.env' not in bundle.namelist()
        assert 'aria/example/investigate-transcript.html' in bundle.namelist()
        assert b'No login is needed' in bundle.read('README.md')
    assert build_aria_bundle(tmp_path / 'release', '0.10.0', root=root)['sha256'] == result['sha256']


def test_recording_archive_preserves_unicode_with_windows_default_encoding(tmp_path, monkeypatch):
    root = tmp_path / 'checkout'
    folder = recording_checkout(root)
    path = folder / 'investigate.json'
    record = json.loads(path.read_text(encoding='utf-8'))
    record['response'] = 'The passenger’s return is unchanged. 検証済み'
    path.write_text(json.dumps(record, ensure_ascii=False), encoding='utf-8')
    expected = build_aria_bundle(tmp_path / 'expected', '0.10.0', root=root)

    original_open = Path.open
    def windows_text_open(path, mode='r', buffering=-1, encoding=None, errors=None, newline=None):
        if 'b' not in mode and encoding in (None, 'locale'):
            encoding = 'cp1252'
        return original_open(path, mode, buffering, encoding, errors, newline)
    monkeypatch.setattr(Path, 'open', windows_text_open)

    actual = build_aria_bundle(tmp_path / 'actual', '0.10.0', root=root)
    assert actual['sha256'] == expected['sha256']
    with zipfile.ZipFile(tmp_path / 'actual' / actual['file']) as bundle:
        saved = json.loads(bundle.read('aria/example/investigate.json'))
        assert saved['response'] == record['response']


@pytest.mark.parametrize('problem', ['response', 'capture', 'path', 'status'])
def test_incomplete_or_escaping_recordings_are_not_packaged(tmp_path, problem):
    root = tmp_path / 'checkout'
    folder = recording_checkout(root)
    path = folder / 'investigate.json'
    record = json.loads(path.read_text())
    if problem == 'response':
        record['response'] = ''
    elif problem == 'capture':
        (folder / 'investigate-response.png').unlink()
    elif problem == 'path':
        record['captures'][0]['path'] = '../../../../../../.env'
    else:
        record['status'] = 'unavailable'
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError):
        build_aria_bundle(tmp_path / 'release', '0.10.0', root=root)
    assert not list((tmp_path / 'release').glob('*.zip'))
