"""Run the participant's worked answers end to end; publication is an explicit flag."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from forge_workshop_kit import WorkshopSession, inspection, inspection_teaching as teaching
from forge_workshop_kit.traces import event, export_trace


class LocalPublisher:
    def publish_progress(self):
        return None


def run(args):
    session = WorkshopSession(args.project, 'visual-inspection', state_dir=args.state,
                              publisher=None if args.publish else LocalPublisher())
    data = inspection.load_data(args.data)
    fit, val, review, test = [inspection.indices(data, p) for p in ('fit','validation','review','test')]
    build_features = teaching.functions(teaching.FEATURE_SOLUTION)['build_features']
    choose_threshold = teaching.functions(teaching.THRESHOLD_SOLUTION)['choose_threshold']
    sources = {'features.py': teaching.FEATURE_SOLUTION, 'threshold.py': teaching.THRESHOLD_SOLUTION}
    if args.publish:
        session.check_access()
    start = time.monotonic()
    names = ['compare/whole','compare/nearest-patch','review/active','review/random']
    selected_rows = {}
    traces = {}
    for name in names:
        method = 'whole' if name == 'compare/whole' else 'nearest-patch'
        rows = fit
        if name.startswith('review/'):
            initial = teaching.model_from_stage(session, 'compare/nearest-patch')
            values = inspection.score(data, review, initial, build_features=build_features)
            selection = name.split('/')[1]
            selected = inspection.select_review(values, review, initial['threshold'], 24, selection, 17)
            selected_rows[name] = [data['records'][i]['case_id'] for i in selected]
            rows = np.concatenate([fit, selected])
        with session.stage(name, config={'method': method, 'C': .03, 'review_budget': 24 if name.startswith('review/') else 0}, sources=sources) as stage:
            if stage.needs_run:
                def train():
                    model = inspection.fit_classifier(data, rows, method, build_features=build_features, C=.03)
                    values = inspection.score(data, val, model, build_features=build_features)
                    threshold = choose_threshold(inspection.labels(data, val), values)
                    path = stage.output_dir / 'classifier.npz'
                    sha = inspection.save_classifier(path, model, threshold)
                    return {'model_file': path.relative_to(session.root).as_posix(), 'model_sha256': sha,
                            'metrics': inspection.metrics(inspection.labels(data, val), values, threshold),
                            'seconds': model['seconds'], 'label_source': 'authors annotations, simulated acquisition'}
                result, observation = event('train_and_validate_classifier', {'method': method, 'fit_boards': len(rows), 'C': .03}, train, on_error=stage.record_event)
                stage.record({**result, 'events': [observation]}, files=[session.file(result['model_file'])])
        if args.publish:
            traces[name] = export_trace(session, stage.id, 'Train PCB1 classifier using development labels', stage.result['events'])
    with session.stage('freeze', config={'selection_rule': 'highest validation AP; ties follow declared version order'}) as stage:
        if stage.needs_run:
            versions = {name: {'stage_id': teaching.saved(session,name)['id'], **{key: teaching.saved(session,name)['result'][key] for key in ('model_file','model_sha256')}, 'feature_source': teaching.saved(session,name)['sources']['features.py']} for name in names}
            chosen = max(names, key=lambda name: teaching.saved(session,name)['result']['metrics']['average_precision'])
            stage.record({'versions': versions, 'selected': chosen})
    frozen = teaching.saved(session, 'freeze')
    with session.stage('evaluate', config={'freeze': frozen['id']}) as stage:
        if stage.needs_run:
            summaries, versions = {}, {}
            for name, entry in frozen['result']['versions'].items():
                path = session.file(entry['model_file'])
                assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['model_sha256']
                model = inspection.load_classifier(path)
                feature_function = teaching.functions(entry['feature_source'])['build_features']
                values = inspection.score(data, test, model, build_features=feature_function)
                summaries[name] = inspection.metrics(inspection.labels(data,test),values,model['threshold'],review_margin=.5)
                versions[name] = inspection.prediction_rows(data,test,model,model['threshold'],build_features=feature_function,destination=stage.output_dir/'media',root=session.root)
            stage.record({'versions': versions,'summaries': summaries,'selected': frozen['result']['selected']}, files=list((stage.output_dir/'media').glob('*')))
    result = teaching.saved(session,'evaluate')['result']
    # Reload from disk and compare every saved score; completed stages must be reused on restart.
    for name, entry in frozen['result']['versions'].items():
        model = inspection.load_classifier(session.file(entry['model_file']))
        values = inspection.score(data,test,model,build_features=teaching.functions(entry['feature_source'])['build_features'])
        np.testing.assert_allclose(values,[row['prediction']['score'] for row in result['versions'][name]],atol=1e-6,rtol=1e-6)
    session.checkpoint('reproduce',publish=args.publish)
    publication = None
    if args.publish:
        from forge_workshop_kit.publication import publish_comparison, publish_report
        publication = publish_comparison(session,'visual-inspection-final',result['versions'],summaries=result['summaries'])
        links = {name: receipt['url'] for name,receipt in traces.items()}
        report = publish_report(session,'This scripted CPU rehearsal used the public worked answers, four frozen classifiers and 442 matching PCB1 boards. Inspect average precision, missed defects and false alarms separately. Additional labels came from the authors, not a live reviewer. The qualification follow-up was a teaching retest of inspected images; this is not independent evidence of generalization.',links)
    else:
        report = None
    summary = {'project': args.project, 'state': Path(args.state).as_posix(), 'seconds': time.monotonic()-start,
               'models': result['summaries'], 'selected': result['selected'], 'review_case_ids': selected_rows,
               'executions': len(session.read()['stages']), 'final_prediction_rows': sum(len(v) for v in result['versions'].values()),
               'reproduction': 'every saved test score matched', 'inference_requests': len(session.read()['requests']),
               'publication': publication, 'traces': traces, 'report': report}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',default='wandb/forge-workshop-kit')
    parser.add_argument('--data',default='data/inspection-v1')
    parser.add_argument('--state',default='.workshop/inspection-v050-rehearsal')
    parser.add_argument('--output',default='evidence/inspection-local-rehearsal.json')
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    summary=run(args)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('publication','traces','review_case_ids')},indent=2))
