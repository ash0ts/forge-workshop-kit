"""Free exercise checks, durable display reconstruction and public PCB1 download."""
from __future__ import annotations

import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path
import numpy as np
from . import inspection

from .manifest import get_workshop
STEPS = tuple(tuple(step) for step in get_workshop('visual-inspection')['steps'])
RELEASE = 'https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.5.0'
OPENING_ASSETS = Path(__file__).parent / 'assets' / 'inspection'


def opening_board():
    """One bundled fitting example; this performs no download or service request."""
    row = json.loads((OPENING_ASSETS / 'provenance.json').read_text())
    return {**row, 'image': OPENING_ASSETS / 'board.jpg', 'mask': OPENING_ASSETS / 'mask.png'}
FEATURE_STARTER = '''def build_features(data, rows, method, reference=None):
    whole = data["whole"][rows]
    if method == "whole":
        return whole
    # Turn the 14 by 14 patch error map into one row per board.
    # Append these values to whole-image features with np.concatenate.
    raise NotImplementedError("Add the patch features.")
'''
FEATURE_SOLUTION = '''def build_features(data, rows, method, reference=None):
    whole = data["whole"][rows]
    if method == "whole":
        return whole
    errors = inspection.nearest_patch_errors(data, rows, reference) if method == "nearest-patch" else inspection.patch_errors(data["patches"][rows], reference)
    local = np.log1p(errors).reshape(len(rows), -1)
    return np.concatenate([whole, local], axis=1)
'''
THRESHOLD_STARTER = '''def choose_threshold(target, scores, recall=0.90):
    # Keep at least 90% of validation defects above the threshold.
    # Normal-board scores do not determine the required recall.
    raise NotImplementedError("Sort defect scores, then select the cutoff.")
'''
THRESHOLD_SOLUTION = '''def choose_threshold(target, scores, recall=0.90):
    positives = np.sort(scores[target == 1])[::-1]
    position = int(np.ceil(recall * len(positives))) - 1
    return float(positives[position])
'''
REVIEW_STARTER = '''def choose_review(scores, rows, threshold, budget, seed=17):
    # Rank cases by distance from the current decision threshold.
    # Return exactly budget distinct row indices. Do not read labels.
    raise NotImplementedError("Select the most uncertain cases.")
'''
REVIEW_SOLUTION = '''def choose_review(scores, rows, threshold, budget, seed=17):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(rows))
    order = order[np.argsort(np.abs(scores[order] - threshold), kind="stable")]
    return np.asarray(rows)[order[:budget]]
'''


def functions(source):
    scope = {'np': np, 'inspection': inspection}
    exec(compile(source, '<inspection-exercise>', 'exec'), scope)
    return scope


def check_features(source):
    f = functions(source)['build_features']
    data = {'whole': np.ones((3, 2)), 'patches': np.arange(12.).reshape(3, 2, 2, 1)}
    reference = {'mean': np.zeros((2, 2, 1)), 'std': np.ones((2, 2, 1))}
    for method in ['whole', 'patch']:
        actual = f(data, np.array([2, 0]), method, reference)
        np.testing.assert_allclose(actual, inspection.feature_matrix(data, np.array([2, 0]), method, reference))
    data['records'] = [{'case_id': str(i)} for i in range(3)]
    nearest = {'bank': data['patches'][:2], 'case_ids': ['0', '1']}
    np.testing.assert_allclose(f(data, np.array([2, 0]), 'nearest-patch', nearest), inspection.feature_matrix(data, np.array([2, 0]), 'nearest-patch', nearest))
    return {'status': 'complete', 'check': 'Board order and local features match the fixture; no training ran.'}


def check_whole_features(source):
    fn = functions(source)['build_features']
    fixture = {'whole': np.arange(12.).reshape(3, 4)}
    np.testing.assert_array_equal(fn(fixture, np.array([2, 0]), 'whole'), fixture['whole'][[2, 0]])
    return {'status': 'complete', 'check': 'Whole-image rows preserve board order. Patch code is not needed yet.'}


def check_threshold(source):
    f = functions(source)['choose_threshold']
    target = np.array([1, 0, 1, 1, 0])
    scores = np.array([.9, .95, .4, .7, .1])
    assert f(target, scores, 2 / 3) == .7, 'Two of three defects must score at or above the cutoff.'
    assert f(target, scores, 1.) == .4, 'Full validation recall includes the lowest-scoring defect.'
    return {'status': 'complete', 'check': 'The threshold obeys the requested recall on both fixtures.'}


def check_review(source):
    f = functions(source)['choose_review']
    rows = np.array([10, 20, 30, 40])
    selected = f(np.array([.8, -.1, .01, -.9]), rows, 0., 2, 17)
    assert set(selected) == {20, 30}, 'Choose the two cases closest to the threshold.'
    return {'status': 'complete', 'check': 'Selection uses scores rather than hidden labels.'}


def saved(session, name):
    matches = [row for row in session.read()['stages'].values() if row['name'] == name and row['status'] == 'complete']
    return max(matches, key=lambda row: row['ended_at']) if matches else None


def stage_ids(session, *names):
    """Completed records for the visible exercise, including restored traces."""
    if not session:
        return ()
    return tuple(row['id'] for row in session.read()['stages'].values()
                 if row['status'] == 'complete' and (not names or any(row['name'] == name or row['name'].startswith(name + '/') for name in names)))


def model_from_stage(session, name):
    row = saved(session, name)
    if not row:
        raise ValueError(f'Complete {name} first.')
    return inspection.load_classifier(session.file(row['result']['model_file']))


def completed_steps(session):
    if not session:
        return set()
    completed = set(session.read()['progress'].get('completed', []))
    whole = saved(session, 'compare/whole')
    patch = saved(session, 'compare/nearest-patch')
    if whole:
        completed.add('baseline')
    if whole and patch:
        completed.add('compare')
    else:
        completed.discard('compare')
    return completed


def check_matched_settings(session, method, feature_source, threshold_source, data):
    """Only the patch branch may change between the two representation runs."""
    current = saved(session, 'compare/' + method)
    if current and current['sources'] != {'features.py': feature_source, 'threshold.py': threshold_source}:
        raise ValueError('This version is already saved. Restore its source to reuse it; use a new workspace for another recipe.')
    whole = saved(session, 'compare/whole')
    if method == 'nearest-patch' and not whole:
        raise ValueError('Run the whole-image baseline and inspect a validation board first.')
    if method == 'nearest-patch':
        if whole['sources']['threshold.py'] != threshold_source:
            raise ValueError('Restore the baseline threshold rule so the representation comparison uses the same operating rule.')
        rows = np.concatenate([inspection.indices(data, 'fit'), inspection.indices(data, 'validation')])
        old = functions(whole['sources']['features.py'])['build_features'](data, rows, 'whole')
        new = functions(feature_source)['build_features'](data, rows, 'whole')
        if not np.array_equal(old, new):
            raise ValueError('Keep the whole-image branch unchanged. Add patch features without changing the baseline inputs.')
    return True


def download(destination='data/inspection-v1', *, base_url=RELEASE):
    import httpx
    destination = Path(destination)
    if (destination / 'manifest.json').exists():
        inspection.load_data(destination)
        return destination
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        response = httpx.get(base_url + '/inspection-v1.sha256', follow_redirects=True, timeout=60)
        response.raise_for_status()
        expected = response.text.split()[0]
        archive = root / 'inspection-v1.tar.gz'
        with httpx.stream('GET', base_url + '/inspection-v1.tar.gz', follow_redirects=True, timeout=120) as response:
            response.raise_for_status()
            with archive.open('wb') as out:
                for chunk in response.iter_bytes():
                    out.write(chunk)
        if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
            raise ValueError('PCB1 download checksum mismatch. Remove the incomplete download and retry.')
        with tarfile.open(archive) as bundle:
            for member in bundle:
                if member.issym() or member.islnk() or not (root / member.name).resolve().is_relative_to(root):
                    raise ValueError('Unsafe dataset archive member.')
            bundle.extractall(root, filter='data')
        inspection.load_data(root / 'inspection-v1')
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(root / 'inspection-v1', destination)
    return destination


def recompute_batch(root, weights_path):
    from .inspection_encoder import encode
    data = inspection.load_data(root)
    inputs = json.loads((Path(root) / 'encoder-inputs.json').read_text())
    selected = np.array([int(index) for index in inputs])
    whole, patches = encode([Path(root) / path for path in inputs.values()], weights_path)
    np.testing.assert_allclose(whole, data['whole'][selected], atol=.005, rtol=.005)
    np.testing.assert_allclose(patches, data['patches'][selected], atol=.01, rtol=.005)
    return {'boards': len(selected), 'matching_cached_features': True, 'encoder': data['manifest']['encoder']}


def fetch_weights(destination):
    import httpx
    from .inspection_encoder import WEIGHTS_URL, WEIGHTS_SHA256
    path = Path(destination)
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == WEIGHTS_SHA256:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix('.partial')
    with httpx.stream('GET', WEIGHTS_URL, follow_redirects=True, timeout=120) as response:
        response.raise_for_status()
        with partial.open('wb') as output:
            for chunk in response.iter_bytes():
                output.write(chunk)
    if hashlib.sha256(partial.read_bytes()).hexdigest() != WEIGHTS_SHA256:
        raise ValueError('The downloaded encoder weights failed their checksum.')
    partial.replace(path)
    return path
