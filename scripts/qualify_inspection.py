"""Run the frozen PCB1 qualification once; resume from frozen model files."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from forge_workshop_kit import inspection as lab

ROOT = Path(__file__).resolve().parents[1]

def run(data_root, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    protocol_path = ROOT / 'examples/inspection/qualification-v1.json'
    protocol = json.loads(protocol_path.read_text())
    protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    data = lab.load_data(data_root)
    source_hash = hashlib.sha256(Path(lab.__file__).read_bytes()).hexdigest()
    fit, val, review, test = [lab.indices(data, p) for p in ['fit', 'validation', 'review', 'test']]
    start = time.perf_counter()
    frozen_path = output / 'frozen.json'
    if frozen_path.exists():
        frozen = json.loads(frozen_path.read_text())
        if frozen['protocol_sha256'] != protocol_hash or frozen['source_sha256'] != source_hash:
            raise ValueError('Frozen qualification source or protocol changed. Use a new identity.')
    else:
        frozen = {'identity': protocol['identity'], 'protocol_sha256': protocol_hash, 'source_sha256': source_hash,
                  'data_manifest_sha256': hashlib.sha256((Path(data_root) / 'manifest.json').read_bytes()).hexdigest(),
                  'models': {}, 'test_access': 'not evaluated'}
        for method in ['whole', 'patch']:
            model = lab.fit_classifier(data, fit, method)
            validation_scores = lab.score(data, val, model)
            threshold = lab.choose_threshold(lab.labels(data, val), validation_scores)
            path = output / (method + '.npz')
            frozen['models'][method] = {'file': path.name, 'sha256': lab.save_classifier(path, model, threshold),
                                        'validation': lab.metrics(lab.labels(data, val), validation_scores, threshold),
                                        'threshold': threshold, 'seconds': model['seconds']}
        initial = lab.load_classifier(output / 'patch.npz')
        review_scores = lab.score(data, review, initial)
        for seed in protocol['review_seeds']:
            for selection in ['active', 'random']:
                selected = lab.select_review(review_scores, review, initial['threshold'], protocol['review_budget'], selection, seed)
                model = lab.fit_classifier(data, np.concatenate([fit, selected]), 'patch')
                validation_scores = lab.score(data, val, model)
                threshold = lab.choose_threshold(lab.labels(data, val), validation_scores)
                name = f'{selection}-{seed}'
                path = output / (name + '.npz')
                frozen['models'][name] = {'file': path.name, 'sha256': lab.save_classifier(path, model, threshold),
                                         'validation': lab.metrics(lab.labels(data, val), validation_scores, threshold),
                                         'review_case_ids': [data['records'][i]['case_id'] for i in selected],
                                         'review_budget': len(selected), 'threshold': threshold, 'seconds': model['seconds']}
        frozen_path.write_text(json.dumps(frozen, indent=2) + '\n')
    # No official test score is computed until all eight candidate files and thresholds are frozen.
    results = {'identity': protocol['identity'], 'protocol_sha256': protocol_hash, 'source_sha256': source_hash,
               'data_manifest_sha256': frozen['data_manifest_sha256'], 'models': {}, 'partitions': data['manifest']['partition_counts'],
               'cost': {'provider_calls': 0, 'provider_usd': 0, 'compute': 'existing local CPU; not billed by this script'}}
    predictions = []
    for name, row in frozen['models'].items():
        path = output / row['file']
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Frozen model file changed.')
        model = lab.load_classifier(path)
        values = lab.score(data, test, model)
        measured = lab.metrics(lab.labels(data, test), values, model['threshold'], review_margin=.5)
        results['models'][name] = {**row, 'test': measured}
        predictions.extend({'case_id': data['records'][i]['case_id'], 'version': name,
                            'label': int(data['records'][i]['label']), 'score': float(value),
                            'threshold': model['threshold']} for i, value in zip(test, values, strict=True))
    difference = results['models']['patch']['test']['average_precision'] - results['models']['whole']['test']['average_precision']
    results['worked_example'] = {'measure': 'average_precision', 'patch_minus_whole': difference,
                                  'qualified': difference > 0, 'scope': 'one fixed PCB1 split; not an industrial safety certification'}
    results['seconds'] = time.perf_counter() - start
    (output / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    (output / 'predictions.json').write_text(json.dumps(predictions, indent=2) + '\n')
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', default='data/inspection-v1')
    parser.add_argument('--output', default='evidence/private/inspection-v1')
    args = parser.parse_args()
    print(json.dumps(run(args.data, args.output), indent=2))
