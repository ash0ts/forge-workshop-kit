"""Small inspectable research operations. The notebook owns their ordering."""
import ast
import difflib
import json
from pathlib import Path

from .provider import validated_json
from .session import digest
from .traces import export_trace, event

SYSTEM = '''You edit a small PyTorch forecasting experiment. Return JSON only.
You receive current source and training/validation evidence. Final test data and scores are unavailable.
Preserve interfaces build_model(input_shape, config), training_loss(prediction,target,mask), and fit(model,x,y,mask,config).
Model input is [batch,2,64,64], output [batch,1,64,64]. The fixed independent metric is disk-masked absolute error.
You may change model, features, loss and training implementation. Use only torch, numpy and Python math.
Respect config steps, batch_size and seed. Do not read files, network, environment, labels outside supplied training tensors, or change evaluation.
Prefer a small, testable change with a concrete rationale. Keep the model and execution CPU-sized.
Code is reviewed before execution. A KEEP decision is valid. Never invent an observed improvement.'''


def validate_source(source):
    if len(source.encode()) > 40000:
        raise ValueError('Candidate source exceeds 40 KB.')
    tree=ast.parse(source)
    functions={node.name for node in tree.body if isinstance(node,ast.FunctionDef)}
    if not {'build_model','training_loss','fit'} <= functions:
        raise ValueError('Candidate must preserve build_model, training_loss and fit.')
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            modules=[node.module] if isinstance(node,ast.ImportFrom) else [a.name for a in node.names]
            if any(not m or m.split('.')[0] not in ('torch','numpy','math') for m in modules):
                raise ValueError('Research code imports must be torch, numpy or math.')
    return source


def diff(before,after):
    return ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                                       fromfile='previous/candidate.py',tofile='proposed/candidate.py'))


def propose(session, number, source, evidence):
    # Structured evidence allowlist, not a directory dump that might contain final results.
    if evidence.get('split') != 'validation':
        raise ValueError('Improvement requires validation evidence, not final-test records.')
    allowed={k:evidence[k] for k in ('split','config','metrics','losses','errors','trace','lessons') if k in evidence}
    events=[]
    if evidence.get('stage_id'):
        def read_validation():
            row=session.read()['stages'][evidence['stage_id']]
            if row['inputs'].get('split')!='validation':
                raise ValueError('The selected execution is not a validation run.')
            return {'config':row['config'],'metrics':row['result']['metrics'],'source_fingerprint':row['source_fingerprint']}
        _,observed=event('read_validation_evidence',{'execution':evidence['stage_id']},read_validation)
        events.append(observed)
    with session.stage(f'images/round-{number}/propose',sources={'candidate.py':source},inputs=allowed) as stage:
        if stage.needs_run:
            prompt={'mission':'Propose two competing code changes. Return candidates: [{title,rationale,decision,source}, ...] with exactly two entries. decision is CHANGE or KEEP; source is complete Python.',
                    'source':source,'evidence':allowed}
            def validate(value):
                if len(value.get('candidates',[]))!=2:
                    raise ValueError('The proposal must contain exactly two candidates.')
                for candidate in value['candidates']:
                    validate_decision(candidate,source)
            proposal,call=validated_json(session,stage.id,[{'role':'system','content':SYSTEM},
                {'role':'user','content':json.dumps(prompt)}],validate,max_tokens=16384)
            candidates=proposal.get('candidates',[])
            if len(candidates)!=2:
                raise ValueError('The proposal must contain exactly two candidates.')
            for candidate in candidates:
                validate_decision(candidate,source)
                candidate['fingerprint']=digest({'candidate.py':candidate['source']})
                candidate['diff']=diff(source,candidate['source'])
            files=[]
            for index,candidate in enumerate(candidates):
                path=stage.output_dir/f'candidate-{index}.py'
                def save_candidate():
                    path.write_text(candidate['source'])
                    return {'file':path.name,'source_fingerprint':candidate['fingerprint']}
                _,observed=event('save_candidate_code',{'candidate':index,'decision':candidate['decision']},save_candidate)
                events.append(observed);files.append(path)
            stage.record({'candidates':candidates,'request_id':call['id'],'mission':prompt['mission'],'events':events},files=files)
    return stage.result,stage.id


def validate_decision(decision,source):
    if decision.get('decision') not in ('KEEP','CHANGE') or not decision.get('rationale'):
        raise ValueError('A completed CHANGE or KEEP decision and rationale are required.')
    if decision['decision']=='KEEP':
        if decision.get('source',source)!=source:
            raise ValueError('KEEP cannot change executed code.')
        decision['source']=source
    else:
        validate_source(decision.get('source',''))
        if decision['source']==source:
            raise ValueError('CHANGE has no code change. Use KEEP.')


def compose(session, number, source, previous, candidates):
    if any(c.get('split')!='validation' for c in candidates):
        raise ValueError('Only validation probes can enter composition.')
    context=dict(previous=previous,candidates=candidates,source=source)
    with session.stage(f'images/round-{number}/compose',sources={'candidate.py':source},inputs=context) as stage:
        if stage.needs_run:
            mission='Retain, select, or combine the tested changes. Return title, decision (CHANGE or KEEP), rationale, source (complete code), lesson and limits. Do not describe an untested composition as an improvement.'
            decision,call=validated_json(session,stage.id,[{'role':'system','content':SYSTEM},
                {'role':'user','content':json.dumps({'mission':mission,**context})}],
                lambda value: validate_decision(value,source),max_tokens=16384)
            validate_decision(decision,source)
            decision['diff']=diff(source,decision['source'])
            decision['fingerprint']=digest({'candidate.py':decision['source']})
            path=stage.output_dir/'composition.py'
            def save_composition():
                path.write_text(decision['source'])
                return {'file':path.name,'source_fingerprint':decision['fingerprint']}
            _,observed=event('save_composed_code',{'decision':decision['decision']},save_composition)
            stage.record({'decision':decision,'request_id':call['id'],'mission':mission,'events':[observed]},files=[path])
    return stage.result,stage.id


def trace_decision(session,stage_id):
    stage=session.read()['stages'][stage_id]
    request_id=stage['result']['request_id']
    # Include every transport attempt for this operation, not just the successful response.
    requests=[r for key,r in session.read()['requests'].items() if key.startswith(stage_id+'/') and r.get('ended_at')]
    return export_trace(session,stage_id,stage['result']['mission'],stage['result'].get('events',[]),requests)


def freeze(session, versions, dataset_fingerprint):
    """Caller supplies tested versions; the freeze verifies their saved training receipts."""
    for label,version in versions.items():
        if label=='persistence':
            continue
        row=session.read()['stages'].get(version['stage_id'])
        if not row or row['status']!='complete' or row['sources'].get('candidate.py')!=version['source']:
            raise ValueError('Freeze requires a completed execution of exactly this source.')
    with session.stage('images/freeze',inputs={'versions':versions,'dataset':dataset_fingerprint}) as stage:
        if stage.needs_run:
            stage.record({'versions':versions,'dataset_fingerprint':dataset_fingerprint})
    return stage.result,stage.id
