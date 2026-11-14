"""PCB inspection data, CPU classifiers and independent final measurements.

Dataset masks are for reviewing predictions. They never enter classifier features.
No download, training, inference or publication occurs on import.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np


def load_data(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    for name in ['features.npz', 'records.json', 'encoder-inputs.json']:
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != manifest['files'][name]:
            raise ValueError(f'Dataset file changed: {name}')
    records = json.loads((root / 'records.json').read_text())
    features = np.load(root / 'features.npz', allow_pickle=False)
    if len(records) != len(features['whole']) or len(records) != len(features['patches']):
        raise ValueError('Feature rows and case records do not align.')
    if len({r['case_id'] for r in records}) != len(records):
        raise ValueError('Duplicate case identities.')
    return {'root': root, 'manifest': manifest, 'records': records,
            'whole': features['whole'].astype('float32'),
            'patches': features['patches'].astype('float32')}


def indices(data, partition):
    if partition not in ('fit', 'review', 'validation', 'test'):
        raise ValueError('Unknown data partition.')
    return np.array([i for i, r in enumerate(data['records']) if r['partition'] == partition], dtype=int)


def labels(data, rows):
    return np.array([data['records'][int(i)]['label'] for i in rows], dtype=int)


def fit_patch_reference(patches):
    """Fit one reference at each image location using approved normal training boards."""
    return {'mean': patches.mean(axis=0), 'std': np.maximum(patches.std(axis=0), .1)}


def patch_errors(patches, reference):
    return np.mean(((patches - reference['mean']) / reference['std']) ** 2, axis=-1)


def nearest_patch_errors(data, rows, reference):
    bank = reference['bank'].reshape(len(reference['bank']), -1, reference['bank'].shape[-1])
    query = data['patches'][rows].reshape(len(rows), bank.shape[1], bank.shape[2])
    scale = np.maximum(bank.std(axis=0), .1)
    bank, query = bank / scale, query / scale
    distances = np.empty(query.shape[:2], dtype='float32')
    lookup = {case: i for i, case in enumerate(reference['case_ids'])}
    for p in range(bank.shape[1]):
        a, b = query[:, p], bank[:, p]
        squared = np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * (a @ b.T), 0)
        for k, index in enumerate(rows):
            match = lookup.get(data['records'][int(index)]['case_id'])
            if match is not None:
                squared[k, match] = np.inf
        distances[:, p] = squared.min(axis=1) / bank.shape[2]
    return distances.reshape(len(rows), *data['patches'].shape[1:3])


def feature_matrix(data, rows, method, reference=None):
    whole = data['whole'][rows]
    if method == 'whole':
        return whole
    if method not in ('patch', 'nearest-patch') or reference is None:
        raise ValueError('Patch features require the training reference.')
    error_maps = nearest_patch_errors(data, rows, reference) if method == 'nearest-patch' else patch_errors(data['patches'][rows], reference)
    errors = np.log1p(error_maps).reshape(len(rows), -1)
    return np.concatenate([whole, errors], axis=1)


def fit_classifier(data, fit_rows, method='whole', *, build_features=feature_matrix, C=1.):
    """Only fit/review rows can train. Scorers and test rows cannot enter this call."""
    from sklearn.linear_model import LogisticRegression
    fit_rows = np.array(fit_rows, dtype=int)
    if len(fit_rows) != len(set(fit_rows.tolist())):
        raise ValueError('A reviewed case was counted twice.')
    if any(data['records'][i]['partition'] not in ('fit', 'review') for i in fit_rows):
        raise ValueError('Training can only use the fit and reviewed pools.')
    start = time.perf_counter()
    target = labels(data, fit_rows)
    if set(target.tolist()) != {0, 1}:
        raise ValueError('The classifier needs both normal and defective examples.')
    reference = fit_patch_reference(data['patches'][fit_rows[target == 0]]) if method == 'patch' else None
    if method == 'nearest-patch':
        normal_rows = fit_rows[target == 0]
        reference = {'bank': data['patches'][normal_rows], 'case_ids': [data['records'][i]['case_id'] for i in normal_rows]}
    matrix = build_features(data, fit_rows, method, reference)
    mean, std = matrix.mean(axis=0), np.maximum(matrix.std(axis=0), 1e-5)
    classifier = LogisticRegression(C=C, class_weight='balanced', max_iter=2000, random_state=0)
    classifier.fit((matrix - mean) / std, target)
    return {'method': method, 'mean': mean, 'std': std, 'coef': classifier.coef_[0],
            'intercept': float(classifier.intercept_[0]), 'reference': reference,
            'fit_case_ids': [data['records'][i]['case_id'] for i in fit_rows],
            'seconds': time.perf_counter() - start, 'C': C}


def score(data, rows, classifier, *, build_features=feature_matrix):
    matrix = build_features(data, np.asarray(rows, dtype=int), classifier['method'], classifier['reference'])
    return ((matrix - classifier['mean']) / classifier['std']) @ classifier['coef'] + classifier['intercept']


def choose_threshold(target, scores, recall=.90):
    """Largest threshold that detects at least the requested validation defect fraction."""
    target, scores = np.asarray(target), np.asarray(scores)
    if not len(scores) or not np.isfinite(scores).all() or not np.any(target == 1):
        raise ValueError('A threshold needs finite validation scores and known defects.')
    if not 0 < recall <= 1:
        raise ValueError('Recall target must be in (0, 1].')
    positives = np.sort(scores[target == 1])[::-1]
    return float(positives[int(np.ceil(recall * len(positives))) - 1])


def metrics(target, scores, threshold, *, review_margin=0.):
    from sklearn.metrics import average_precision_score
    target, scores = np.asarray(target), np.asarray(scores)
    if len(target) != len(scores) or not len(target) or not np.isfinite(scores).all():
        raise ValueError('Every case needs a finite score before evaluation.')
    if set(target.tolist()) != {0, 1}:
        raise ValueError('Evaluation needs normal and defective cases.')
    prediction = scores >= threshold
    review = np.abs(scores - threshold) <= review_margin if review_margin > 0 else np.zeros(len(scores), bool)
    positives, negatives = target == 1, target == 0
    misses = int(np.sum(positives & ~prediction))
    false_alarms = int(np.sum(negatives & prediction))
    return {'average_precision': float(average_precision_score(target, scores)),
            'defect_recall': float(np.mean(prediction[positives])),
            'false_alarm_rate': float(np.mean(prediction[negatives])),
            'misses': misses, 'false_alarms': false_alarms,
            'review_fraction': float(review.mean()), 'review_count': int(review.sum()),
            'auto_pass_misses': int(np.sum(positives & ~prediction & ~review)),
            'examples': len(scores), 'defective': int(positives.sum()), 'normal': int(negatives.sum())}


def select_review(scores, rows, threshold, budget, method, seed):
    rows, scores = np.asarray(rows, dtype=int), np.asarray(scores)
    if len(rows) != len(scores) or not 0 < budget <= len(rows):
        raise ValueError('Review budget must fit the pool and scores must align.')
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(rows))
    if method == 'active':
        order = order[np.argsort(np.abs(scores[order] - threshold), kind='stable')]
    elif method != 'random':
        raise ValueError('Choose active or random selection.')
    return rows[order[:budget]]


def save_classifier(path, classifier, threshold):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    reference = classifier['reference']
    np.savez_compressed(path, mean=classifier['mean'], std=classifier['std'], coef=classifier['coef'],
                        reference_mean=reference['mean'] if reference and 'mean' in reference else np.array([]),
                        reference_std=reference['std'] if reference and 'std' in reference else np.array([]),
                        reference_bank=reference['bank'] if reference and 'bank' in reference else np.array([]),
                        reference_cases=np.array(reference['case_ids'] if reference and 'case_ids' in reference else [], dtype=str),
                        metadata=np.array(json.dumps({k: classifier[k] for k in ['method','intercept','fit_case_ids','seconds','C']} | {'threshold': float(threshold)})))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_classifier(path):
    arrays = np.load(path, allow_pickle=False)
    metadata = json.loads(str(arrays['metadata']))
    reference = None if not arrays['reference_mean'].size else {'mean': arrays['reference_mean'], 'std': arrays['reference_std']}
    if 'reference_bank' in arrays and arrays['reference_bank'].size:
        reference = {'bank': arrays['reference_bank'], 'case_ids': arrays['reference_cases'].tolist()}
    return {**metadata, 'mean': arrays['mean'], 'std': arrays['std'], 'coef': arrays['coef'], 'reference': reference}


def render_case(data, index, scores=None, *, reveal_label=True, reference=None):
    """Return actual media as a Matplotlib figure, with common board coordinates."""
    import matplotlib.pyplot as plt
    from PIL import Image
    row = data['records'][int(index)]
    count = 3 if reference is not None else 2
    fig, axes = plt.subplots(1, count, figsize=(4 * count, 4), squeeze=False)
    image = np.array(Image.open(data['root'] / row['image']).convert('RGB'))
    axes[0, 0].imshow(image)
    axes[0, 0].set_title(row['case_id'])
    axes[0, 1].imshow(image)
    if reveal_label and row['mask']:
        mask = np.array(Image.open(data['root'] / row['mask'])) > 0
        if mask.ndim == 3:
            mask = mask.any(axis=-1)
        axes[0, 1].imshow(np.ma.masked_where(~mask, mask), cmap='autumn', alpha=.65, vmin=0, vmax=1)
    axes[0, 1].set_title(('Defective' if row['label'] else 'Normal') + ' · dataset label' if reveal_label else 'Label hidden: make your call first')
    if reference is not None:
        heat = nearest_patch_errors(data, np.array([index]), reference)[0] if 'bank' in reference else patch_errors(data['patches'][[index]], reference)[0]
        axes[0, 2].imshow(heat, cmap='magma')
        axes[0, 2].set_title('Patch distance from normal training boards')
    if scores:
        fig.suptitle(' · '.join(f'{k}: {v:.3f}' for k, v in scores.items()))
    for axis in axes.flat:
        axis.axis('off')
    fig.tight_layout()
    return fig


def mask_preview(source, destination):
    """Display nonzero mask labels as white without changing the source labels."""
    from PIL import Image
    with Image.open(source) as image:
        mask = np.asarray(image) > 0
    if mask.ndim == 3:
        mask = mask.any(axis=-1)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mask.astype('uint8') * 255).save(destination)
    return destination


def prediction_rows(data, rows, classifier, threshold, *, build_features=feature_matrix, destination=None, root=None):
    import shutil

    from .media import image_value
    def media(row, key, caption):
        source = data['root'] / row[key]
        if hashlib.sha256(source.read_bytes()).hexdigest() != row[key + '_sha256']:
            raise ValueError('A dataset image changed after preparation.')
        path = source
        if destination is not None:
            Path(destination).mkdir(parents=True, exist_ok=True)
            if key == 'mask':
                path = mask_preview(source, Path(destination) / (source.stem + '-mask-display.png'))
            else:
                path = Path(destination) / source.name
                shutil.copy2(source, path)
        return image_value(path, caption=caption, root=root)
    values = score(data, rows, classifier, build_features=build_features)
    output = []
    for index, value in zip(rows, values, strict=True):
        row = data['records'][int(index)]
        output.append({'case_id': row['case_id'],
                       'input': media(row, 'image', row['case_id']),
                       'prediction': {'defective': bool(value >= threshold), 'score': float(value), 'threshold': float(threshold)},
                       'target': {'defective': bool(row['label']), 'mask': media(row, 'mask', 'VisA defect mask') if row['mask'] else None},
                       'error': float((value >= threshold) != bool(row['label'])),
                       'scores': {'correct': float((value >= threshold) == bool(row['label'])), 'defect_score': float(value)},
                       'evidence': {'source_image_sha256': row['source_sha256'], 'encoder': data['manifest']['encoder']}})
    return output
