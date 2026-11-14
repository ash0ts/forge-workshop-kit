"""Run the frozen routing qualification; all outcomes survive, including regressions."""
import argparse
import json
import platform
import time
from pathlib import Path

from threadpoolctl import threadpool_limits
from forge_workshop_kit import routing


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=Path('data/banking77-v1'))
    parser.add_argument('--contract',type=Path,default=Path('examples/routing/qualification.json'))
    parser.add_argument('--output',type=Path,default=Path('evidence/routing-qualification-20261114'))
    args=parser.parse_args()
    contract=json.loads(args.contract.read_text())
    args.output.mkdir(parents=True,exist_ok=True)
    contract_hash=routing.checksum(args.contract)
    frozen=args.output/'frozen-contract.json'
    if frozen.exists() and json.loads(frozen.read_text())['sha256'] != contract_hash:
        raise ValueError('Qualification identity already contains a different contract.')
    frozen.write_text(json.dumps({'sha256':contract_hash,'contract':contract},indent=2)+'\n')
    data=routing.load_data(args.data)
    results=[]
    started=time.perf_counter()
    with threadpool_limits(limits=2):
        for seed in contract['qualification_seeds']:
            for kind in ('tfidf','embedding'):
                destination=args.output/f'{kind}-{seed}.json'
                if destination.exists():
                    result=json.loads(destination.read_text())
                else:
                    try:
                        fitted=routing.fit_classifier(data,kind,seed=seed,C=contract['C'])
                        validation=routing.predict(fitted,data,'validation',threshold=contract['abstention_threshold'])
                        # The recipe was frozen before this first use of the test partition.
                        final=routing.predict(fitted,data,'test',threshold=contract['abstention_threshold'])
                        result={'kind':kind,'seed':seed,'status':'complete','training_seconds':fitted['training_seconds'],
                                'validation':routing.score(validation),'final':routing.score(final),
                                'per_intent':routing.per_intent(final),'training_ids':fitted['training_ids'],
                                'validation_predictions':validation,'final_predictions':final}
                    except Exception as error:
                        result={'kind':kind,'seed':seed,'status':'failed','error':str(error)}
                    destination.write_text(json.dumps(result,indent=2)+'\n')
                results.append(result)
                print(json.dumps({k:v for k,v in result.items() if k in ('kind','seed','status','validation','final','training_seconds','error')}),flush=True)
    pairs=[]
    for seed in contract['qualification_seeds']:
        models={r['kind']:r for r in results if r['seed']==seed}
        complete=all(m['status']=='complete' for m in models.values())
        pairs.append({'seed':seed,'macro_f1_difference':models['embedding']['final']['macro_f1']-models['tfidf']['final']['macro_f1'] if complete else None})
    summary={'identity':contract['identity'],'contract_sha256':contract_hash,'data_manifest_sha256':routing.checksum(args.data/'manifest.json'),
             'qualified':all(p['macro_f1_difference'] is not None and p['macro_f1_difference']>0 for p in pairs),
             'pairs':pairs,'runs':[{k:v for k,v in r.items() if k not in ('training_ids','validation_predictions','final_predictions','per_intent')} for r in results],
             'local_seconds':time.perf_counter()-started,'inference_cost_usd':0,'compute':'Local CPU; two BLAS threads; no billed external training.',
             'python':platform.python_version(),'limitation':'One benchmark split. Repeated deterministic classifier fits are reproducibility checks, not independent datasets or confidence intervals.'}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
