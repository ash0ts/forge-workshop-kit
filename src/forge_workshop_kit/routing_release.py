"""A release drill for a fitted router. No training, hosted service, or inference calls."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import joblib
import numpy as np
from filelock import FileLock

from . import releases, routing
from .routing_teaching import functions, publication_rows as prediction_rows, saved
from .session import digest, write_json
from .traces import event

LOADER_SOLUTION = '''def label_names(model_classes):
    # Probability column i belongs to model_classes[i]. Preserve that order.
    return list(model_classes)
'''
LOADER_STARTER = '''def label_names(model_classes):
    # Return the labels in the same order as the model's probability columns.
    raise NotImplementedError("Keep the classifier's label ordering.")
'''
FAULTY_LOADER = '''def label_names(model_classes):
    # CONTROLLED DRILL: rotate labels while leaving probability columns unchanged.
    labels = list(model_classes)
    return labels[1:] + labels[:1]
'''
CHECK_STARTER = '''def check_release(model_classes, loaded_labels):
    # The same names in the wrong order still route customers incorrectly.
    # Return label_set and label_order, each a Python bool.
    raise NotImplementedError("Check both membership and probability-column order.")
'''
CHECK_SOLUTION = '''def check_release(model_classes, loaded_labels):
    return {"label_set": set(model_classes) == set(loaded_labels),
            "label_order": list(model_classes) == list(loaded_labels)}
'''


def check_exercises(loader_source, check_source):
    loader = functions(loader_source)['label_names']
    checker = functions(check_source)['check_release']
    labels = ['card_not_working', 'card_arrival', 'cash_withdrawal']
    if loader(labels) != labels:
        raise AssertionError('Keep the model order, even when it is not alphabetical.')
    for actual, expected in ((labels, {'label_set': True, 'label_order': True}),
                             (labels[1:]+labels[:1], {'label_set': True, 'label_order': False}),
                             (labels[:-1], {'label_set': False, 'label_order': False})):
        result = checker(labels, actual)
        if result != expected or any(type(v) is not bool for v in result.values()):
            raise AssertionError('Check names and order separately; return Python booleans.')
    return {'status': 'complete', 'examples': 'The original order passes. Rotated or missing labels fail.'}


def cohort(data):
    """Choose one lexical case ID per intent without computing any predictions."""
    review = sorted((r for r in data['rows'] if r['split'] == 'review'), key=lambda r: r['id'])
    first = {}
    for row in review:
        first.setdefault(row['label'], row)
    expected = {r['label'] for r in data['rows'] if r['split'] == 'train'}
    if set(first) != expected:
        raise ValueError('The review pool must contain every training intent.')
    return [first[label] for label in sorted(first)]


def _directory(session, record):
    return session.file(record['result']['bundle_directory'])


def _seal(root, metadata):
    metadata = {**metadata, 'files': {p.name: routing.checksum(p) for p in sorted(root.iterdir())
                                     if p.is_file() and p.name != 'release.json'}}
    write_json(root/'release.json', metadata)
    return metadata


def load_bundle(root):
    """Read a release produced by this learner. Joblib is not safe for untrusted files."""
    root = Path(root)
    metadata = json.loads((root/'release.json').read_text(encoding="utf-8"))
    for name, expected in metadata['files'].items():
        path = (root/name).resolve()
        if path.parent != root.resolve() or not path.is_file() or routing.checksum(path) != expected:
            raise ValueError('Release file failed its checksum: '+name)
    required = {'classifier.joblib', 'classifier_source.py', 'review_policy.py', 'loader.py', 'routing_runtime.py'}
    if not required.issubset(metadata['files']):
        raise ValueError('The release is missing its model, preprocessing, policy, or source.')
    fitted = joblib.load(root/'classifier.joblib')
    if list(map(str, fitted['model'].classes_)) != metadata['probability_labels']:
        raise ValueError('The classifier label columns differ from the saved release metadata.')
    return fitted, metadata


def prepare(session, data):
    frozen = saved(session, 'routing/freeze')
    final = saved(session, 'routing/final/selected')
    if not frozen or not final:
        raise ValueError('Finish the selected classifier comparison before preparing its release.')
    selected = session.read()['stages'][frozen['result']['selected_stage']]
    data_identity = digest(data['manifest'])
    with session.stage('routing/release/cohort', config={'dataset': data_identity, 'selection': 'lexical-first-review-case-per-intent'}) as selection:
        if selection.needs_run:
            selection.record({'cases': cohort(data), 'purpose': 'Regression and reproduction set, not an independent test set.'})
    source = selected.get('sources', {}).get('classifier.py')
    if not source:
        raise ValueError('The selected execution has no saved classifier source. Restore its original record.')
    model_path = session.file(selected['result']['model_file'])
    if routing.checksum(model_path) != frozen['result']['model_sha256']:
        raise ValueError('The selected model changed after the final comparison.')
    with session.stage('routing/release/prepare', config={'freeze': frozen['id'], 'cohort': selection.id},
                       sources={'loader.py': LOADER_SOLUTION, 'classifier_source.py': source,
                                'review_policy.py': frozen['result']['policy_source']}) as stage:
        if stage.needs_run:
            root = stage.output_dir
            shutil.copyfile(model_path, root/'classifier.joblib')
            for name, text in stage.spec['sources'].items():
                (root/name).write_text(text, encoding='utf-8')
            fitted = joblib.load(model_path)
            (root/'routing_runtime.py').write_text(Path(routing.__file__).read_text(encoding='utf-8'), encoding='utf-8')
            metadata = _seal(root, {'schema': 1, 'variant': 'healthy', 'controlled_drill': False,
                'model_stage': selected['id'], 'final_stage': final['id'], 'freeze': frozen['id'],
                'probability_labels': list(map(str, fitted['model'].classes_)), 'kind': fitted['kind'],
                'threshold': frozen['result']['threshold'], 'cohort_stage': selection.id,
                'dataset': data_identity, 'preprocessing': data['manifest'],
                'training_kit_version': selected.get('kit_version'),
                'note': 'TF-IDF preprocessing is inside the fitted pipeline; embedding releases require the pinned cached encoder features.'})
            stage.record({'bundle_directory': str(root.relative_to(session.root)), 'metadata': metadata,
                          'case_count': len(selection.result['cases'])}, files=list(root.iterdir()))
    return session.read()['stages'][stage.id]


def publish_bundle(session, record):
    """Publish an already saved bundle once; no prediction or training happens here."""
    key = 'routing-release-artifact/'+record['id']
    with FileLock(str(session.root/('.release-'+record['id']+'.lock'))):
        prior = session.read()['publications'].get(key)
        if prior:
            return prior
        root = _directory(session, record)
        load_bundle(root)
        import wandb
        pub = session.connect()
        with pub.run(record['id']+'-release', 'Routing release / '+record['name'].rsplit('/',1)[-1], 'workshop-release',
                     {'source_stage': record['id'], 'controlled_drill': record['result']['metadata'].get('controlled_drill', False)}) as run:
            artifact = wandb.Artifact('routing-release-'+record['id'], type='routing-release')
            for path in sorted(root.iterdir()):
                if path.is_file():
                    artifact.add_file(str(path), name=path.name)
            logged = run.log_artifact(artifact).wait(timeout=120)
            receipt = {'artifact': logged.qualified_name, 'url': logged.url, 'run': run.url, 'stage': record['id']}
            # Save before the SDK closes the run: finish errors must not lose a completed upload.
            with session.transaction() as state:
                state['publications'][key] = receipt
        return receipt


def batch(root, data, cases):
    fitted, metadata = load_bundle(root)
    if routing.checksum(Path(routing.__file__)) != metadata['files']['routing_runtime.py']:
        version = metadata.get('training_kit_version')
        instruction = ('Install forge-workshop-kit=='+version if version else 'Restore the Workshop Kit version used to create this release')
        raise ValueError('The installed prediction code differs from this release. '+instruction+
                         ' before running a new batch. Saved predictions remain available.')
    if digest(data['manifest']) != metadata['dataset']:
        raise ValueError('The prediction data/preprocessing do not match this release.')
    indexed = {r['id']: (i, r) for i,r in enumerate(data['rows'])}
    if any(r['id'] not in indexed or indexed[r['id']][1] != r or r['split'] != 'review' for r in cases):
        raise ValueError('Use the frozen review cases, with their original text and labels.')
    subset = {'rows': cases, 'features': np.asarray([data['features'][indexed[r['id']][0]] for r in cases])}
    # The core predictor preserves probabilities; the release loader decides their displayed names.
    rows = routing.predict(fitted, subset, 'review', threshold=metadata['threshold'])
    model_labels = metadata['probability_labels']
    labels = functions((Path(root)/'loader.py').read_text(encoding="utf-8"))['label_names'](model_labels)
    if len(labels) != len(model_labels) or len(set(labels)) != len(labels):
        raise ValueError('The loader must return one unique label per probability column.')
    mapping = dict(zip(model_labels, labels))
    policy = functions((Path(root)/'review_policy.py').read_text(encoding="utf-8"))['needs_review']
    return [{**row, 'prediction': mapping[row['prediction']], 'runner_up': mapping[row['runner_up']],
             'abstained': bool(policy(row['confidence'], metadata['threshold'])),
             'release_variant': metadata['variant']} for row in rows]


def prediction_parity(rows, reference):
    fields = ('prediction', 'runner_up', 'confidence', 'margin', 'abstained')
    a = {r['case_id']: [r[k] for k in fields] for r in rows}
    b = {r['case_id']: [r[k] for k in fields] for r in reference}
    return bool(a) and len(a) == len(rows) and len(b) == len(reference) and a == b


def reproduce_selected(session, data, *, api=None):
    prepared = saved(session, 'routing/release/prepare')
    if not prepared:
        raise ValueError('Prepare the selected release first.')
    receipt = publish_bundle(session, prepared)
    with session.stage('routing/release/reproduce', config={'artifact': receipt['artifact'], 'prepared': prepared['id']}) as stage:
        if stage.needs_run:
            target = stage.output_dir/'download'
            downloaded = releases.reproduce(receipt['artifact'], root=target, api=api)
            load_bundle(downloaded)
            original = _directory(session, prepared)
            if routing.checksum(Path(downloaded)/'release.json') != routing.checksum(original/'release.json'):
                raise ValueError('The downloaded artifact differs from the selected release.')
            cases = session.read()['stages'][prepared['result']['metadata']['cohort_stage']]['result']['cases']
            rows, trace = event('reload_and_predict_release', {'artifact': receipt['artifact'], 'cases': [r['id'] for r in cases]},
                lambda: batch(downloaded, data, cases), on_error=stage.record_event)
            # Keep a flat verified copy so ordinary checkpoint restore includes every file.
            for path in Path(downloaded).iterdir():
                if path.is_file() and path.name in set(prepared['result']['metadata']['files'])|{'release.json'}:
                    shutil.copyfile(path, stage.output_dir/path.name)
            stage.record({'bundle_directory': str(stage.output_dir.relative_to(session.root)), 'artifact': receipt['artifact'],
                'predictions': rows, 'metrics': routing.score(rows), 'events': [trace], 'metadata': prepared['result']['metadata']},
                files=[p for p in stage.output_dir.iterdir() if p.is_file()])
    return session.read()['stages'][stage.id]


def run_variant(session, data, *, variant, loader_source=None, check_source=None):
    if variant not in ('incident', 'repair'):
        raise ValueError('Choose incident or repair.')
    healthy = saved(session, 'routing/release/reproduce')
    if not healthy:
        raise ValueError('Reload the exact healthy artifact first.')
    if variant == 'repair' and not saved(session, 'routing/release/incident'):
        raise ValueError('Run the controlled incident before testing the repair.')
    loader_source = FAULTY_LOADER if variant == 'incident' else loader_source
    if variant == 'repair':
        check_exercises(loader_source, check_source)
    sources = {'loader.py': loader_source}
    if check_source:
        sources['release_check.py'] = check_source
    with session.stage('routing/release/'+variant, config={'healthy': healthy['id']}, sources=sources) as stage:
        if stage.needs_run:
            origin = _directory(session, healthy)
            metadata = healthy['result']['metadata']
            for name in metadata['files']:
                shutil.copyfile(origin/name, stage.output_dir/name)
            for name, source in sources.items():
                (stage.output_dir/name).write_text(source, encoding='utf-8')
            metadata = _seal(stage.output_dir, {**metadata, 'variant': variant, 'controlled_drill': True})
            cases = session.read()['stages'][metadata['cohort_stage']]['result']['cases']
            rows, trace = event('predict_'+variant+'_release', {'controlled_drill': True, 'healthy_artifact': healthy['result']['artifact'],
                'loader_sha256': metadata['files']['loader.py'], 'cases': [r['id'] for r in cases]},
                lambda: batch(stage.output_dir, data, cases), on_error=stage.record_event)
            labels = functions(loader_source)['label_names'](metadata['probability_labels'])
            checks = functions(check_source)['check_release'](metadata['probability_labels'], labels) if check_source else {
                'label_set': set(labels)==set(metadata['probability_labels']), 'label_order': labels==metadata['probability_labels']}
            checks = {**checks, 'prediction_parity': prediction_parity(rows, healthy['result']['predictions'])}
            stage.record({'bundle_directory': str(stage.output_dir.relative_to(session.root)), 'metadata': metadata,
                'predictions': rows, 'metrics': routing.score(rows), 'checks': checks, 'events': [trace]},
                files=list(stage.output_dir.iterdir()))
    return session.read()['stages'][stage.id]


def decide(session, *, decision, reason):
    if decision not in ('release', 'reject'):
        raise ValueError('Choose release or reject for the repaired loader.')
    repaired = saved(session, 'routing/release/repair')
    healthy = saved(session, 'routing/release/reproduce')
    if not repaired or not healthy:
        raise ValueError('Test the repair before deciding.')
    receipt = publish_bundle(session, repaired)
    release = releases.record_release(session, artifact=receipt['artifact'], evaluation='local-stage:'+repaired['id'],
        decision=decision, previous=healthy['result']['artifact'], metrics=repaired['result']['metrics'],
        checks=repaired['result']['checks'], reason=reason)
    with session.stage('routing/release/decision', config={'release': release['id']}) as stage:
        if stage.needs_run:
            stage.record({'release': release, 'next': 'Verify rollback from the exact previous artifact.' if decision=='release' else 'The earlier release remains selected.'})
    return release


def rollback(session, data, *, api=None):
    decision = saved(session, 'routing/release/decision')
    if not decision or decision['result']['release']['decision'] != 'release':
        raise ValueError('Release the tested repair before practicing rollback.')
    healthy = saved(session, 'routing/release/reproduce')
    current = decision['result']['release']
    with session.stage('routing/release/rollback', config={'restore': healthy['result']['artifact'], 'replace': current['artifact']}) as stage:
        if stage.needs_run:
            root = releases.reproduce(healthy['result']['artifact'], root=stage.output_dir/'download', api=api)
            _, metadata = load_bundle(root)
            cases = session.read()['stages'][metadata['cohort_stage']]['result']['cases']
            rows, trace = event('verify_rollback_predictions', {'artifact': healthy['result']['artifact']},
                lambda: batch(root, data, cases), on_error=stage.record_event)
            checks = {'prediction_parity': prediction_parity(rows, healthy['result']['predictions'])}
            record = releases.record_release(session, artifact=healthy['result']['artifact'], previous=current['artifact'],
                evaluation='local-stage:'+stage.id, decision='rollback', metrics=routing.score(rows), checks=checks,
                reason='Rollback drill: reload the previous exact release and reproduce its predictions.')
            stage.record({'predictions': rows, 'metrics': routing.score(rows), 'checks': checks, 'release': record, 'events':[trace]})
    return session.read()['stages'][stage.id]


def comparisons(session):
    return {label: saved(session, 'routing/release/'+name) for label,name in
            (('healthy','reproduce'),('faulty','incident'),('repaired','repair'),('rollback','rollback'))
            if saved(session, 'routing/release/'+name)}


def comparison_rows(session, record):
    """Keep saved evaluation rows stable when later uploads add evidence links."""
    key = 'routing-release-row-evidence/'+record['id']
    with session.transaction() as state:
        if key not in state['publications']:
            current = state['stages'][record['id']]
            publications = state['publications']
            trace = publications.get('trace/'+record['id'], {})
            artifact = publications.get('routing-release-artifact/'+record['id'], {})
            reference = (artifact.get('artifact') or record['result'].get('artifact')
                         or record['result'].get('release', {}).get('artifact'))
            if reference and not artifact:
                artifact = next((receipt for name, receipt in publications.items()
                                 if name.startswith('routing-release-artifact/')
                                 and receipt.get('artifact') == reference), {})
            publications[key] = {
                'stage': record['id'], 'controlled_drill': True,
                'agent_lens': trace.get('url') if trace.get('verified') else None,
                'release_artifact': reference, 'release_artifact_url': artifact.get('url'),
                'execution_artifact': current.get('artifact_ref'),
                'execution_artifact_url': current.get('artifact_url'),
            }
        evidence = dict(state['publications'][key])
    return [{**row, 'evidence': evidence} for row in prediction_rows(record['result']['predictions'])]


def evidence_links(session):
    """Return current verified links, including exports completed after row publication."""
    state = session.read()
    links = {}
    for key, receipt in state['publications'].items():
        if key.startswith('routing-release-artifact/') and receipt.get('url'):
            links['Release artifact '+receipt['artifact']] = receipt['url']
    for label, record in comparisons(session).items():
        trace = state['publications'].get('trace/'+record['id'], {})
        if trace.get('verified') and trace.get('url'):
            links[label+' release batch in Agent Lens'] = trace['url']
        current = state['stages'][record['id']]
        if current.get('artifact_url'):
            links[label+' saved batch and source'] = current['artifact_url']
    return links


def report_text(session):
    records = comparisons(session)
    if not records:
        return ''
    lines = ['\n\nRelease drill', 'This controlled label-order defect uses one review-pool request per intent. These are regression checks, not new independent test results.']
    for label, record in records.items():
        metrics = record['result']['metrics']
        lines.append(f"{label}: accuracy {metrics['accuracy']:.4f}, macro-F1 {metrics['macro_f1']:.4f}, coverage {metrics['coverage']:.4f} on {metrics['count']} requests.")
    decision = saved(session, 'routing/release/decision')
    if decision:
        record=decision['result']['release']
        lines.append(f"Decision: {record['decision']} {record['artifact']}. {record['reason']}")
    if 'rollback' in records:
        lines.append('Rollback reloaded the previous artifact and matched its saved predictions.')
    return '\n\n'.join(lines)
