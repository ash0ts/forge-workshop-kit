"""One predeclared validation search followed by an explicitly labeled teaching retest."""
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from forge_workshop_kit import inspection as lab

ROOT = Path(__file__).resolve().parents[1]

def nearest_features(data, fit, rows):
    normals = fit[lab.labels(data, fit) == 0]
    bank = data['patches'][normals].reshape(len(normals), 196, 64)
    query = data['patches'][rows].reshape(len(rows), 196, 64)
    scale = np.maximum(bank.std(axis=0), .1)
    bank = bank / scale
    query = query / scale
    distances = np.empty((len(rows), 196), dtype='float32')
    # Positions are independent; no test or validation example enters the bank.
    for p in range(196):
        a, b = query[:, p], bank[:, p]
        squared = np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * (a @ b.T), 0)
        if np.array_equal(rows, fit):
            for k, idx in enumerate(rows):
                match = np.where(normals == idx)[0]
                if len(match):
                    squared[k, match] = np.inf  # Normal training examples cannot match themselves.
        distances[:, p] = squared.min(axis=1) / 64
    return np.concatenate([data['whole'][rows], np.log1p(distances)], axis=1)


def run():
    output = ROOT / 'evidence/private/inspection-v2'
    output.mkdir(parents=True, exist_ok=True)
    protocol_path = ROOT / 'examples/inspection/qualification-v2.json'
    contract_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    protocol = json.loads(protocol_path.read_text())
    result_path = output / 'results.json'
    if result_path.exists():
        saved = json.loads(result_path.read_text())
        if saved['protocol_sha256'] != contract_hash:
            raise ValueError('The saved qualification uses a different protocol. Preserve it under its original identity.')
        for row in saved['selected'].values():
            if hashlib.sha256((output / row['file']).read_bytes()).hexdigest() != row['sha256']:
                raise ValueError('A frozen classifier changed; do not silently rerun this qualification.')
        print(json.dumps({**saved, 'reused_saved_result': True}, indent=2))
        return saved
    data = lab.load_data(ROOT / 'data/inspection-v1')
    fit, val, test = [lab.indices(data, p) for p in ['fit','validation','test']]
    start = time.perf_counter()
    selected, all_validation = {}, []
    for method in protocol['methods']:
        train = data['whole'][fit] if method == 'whole' else nearest_features(data, fit, fit)
        validation = data['whole'][val] if method == 'whole' else nearest_features(data, fit, val)
        mean, std = train.mean(0), np.maximum(train.std(0), 1e-5)
        best = None
        for regularization in protocol['C_grid']:
            classifier = LogisticRegression(C=regularization, class_weight='balanced', max_iter=2000, random_state=0)
            classifier.fit((train - mean) / std, lab.labels(data, fit))
            values = classifier.decision_function((validation - mean) / std)
            threshold = lab.choose_threshold(lab.labels(data, val), values)
            result = lab.metrics(lab.labels(data, val), values, threshold)
            row = {'method': method, 'C': regularization, 'threshold': threshold, 'validation': result}
            all_validation.append(row)
            if best is None or result['average_precision'] > best['validation']['average_precision']:
                best = row
                selected[method] = (classifier, mean, std, row)
        classifier, mean, std, row = selected[method]
        path = output / (method + '.npz')
        np.savez_compressed(path, mean=mean, std=std, coef=classifier.coef_, intercept=classifier.intercept_, threshold=row['threshold'])
        row['file'] = path.name
        row['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    frozen = {'protocol_sha256': contract_hash, 'all_validation': all_validation, 'selected': {name: values[-1] for name, values in selected.items()}, 'test_status': protocol['test_status']}
    (output / 'frozen.json').write_text(json.dumps(frozen, indent=2) + '\n')
    results, predictions = {}, []
    for method, (classifier, mean, std, row) in selected.items():
        matrix = data['whole'][test] if method == 'whole' else nearest_features(data, fit, test)
        values = classifier.decision_function((matrix - mean) / std)
        results[method] = lab.metrics(lab.labels(data, test), values, row['threshold'], review_margin=.5)
        predictions.extend({'case_id': data['records'][i]['case_id'], 'version': method, 'label': int(data['records'][i]['label']), 'score': float(value), 'threshold': row['threshold']} for i, value in zip(test, values, strict=True))
    difference = results['nearest-patch']['average_precision'] - results['whole']['average_precision']
    out = {**frozen, 'identity': protocol['identity'], 'test': results, 'qualified': difference > 0, 'patch_minus_whole': difference, 'seconds': time.perf_counter() - start}
    (output / 'results.json').write_text(json.dumps(out, indent=2) + '\n')
    (output / 'predictions.json').write_text(json.dumps(predictions, indent=2) + '\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    run()
