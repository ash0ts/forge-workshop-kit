"""Optional service adapters. Importing this module does not allocate compute."""

import json
import math
import re
from urllib.parse import quote

import httpx

from .managed_jobs import poll_job, submit_once
from .publication import credentials
from .routing import route_messages, validate_route
from .session import digest


class TrainingClient:
    def __init__(self, *, transport=None):
        self.http = httpx.Client(base_url='https://api.training.wandb.ai', timeout=90, transport=transport)

    def request(self, method, path, body=None):
        response = self.http.request(method, path, json=body,
            headers={'Authorization': 'Bearer ' + credentials()})
        response.raise_for_status()
        return response.json()

    def check_access(self):
        return self.request('GET', '/v1/system-check')

    def register_model(self, session, name, base_model):
        entity, project = session.project.split('/')
        request = {'entity': entity, 'project': project, 'name': name, 'base_model': base_model, 'return_existing': True}
        key = 'training-model/' + digest(request)
        saved = session.read()['publications'].get(key)
        if saved:
            return saved
        model = self.request('POST', '/v1/preview/models', request)
        if model['base_model'] != base_model or model['project'] != project or model['entity'] != entity:
            raise ValueError('The returned model does not match this project and base model.')
        with session.transaction() as state:
            state['publications'][key] = model
        return model

    def start_sft(self, session, request, *, forecast, approved_usd):
        registered = [row for key, row in session.read()['publications'].items()
                      if key.startswith('training-model/') and row.get('id') == request.get('model_id')]
        if len(registered) != 1 or '/'.join((registered[0]['entity'], registered[0]['project'])) != session.project:
            raise ValueError('Register this model in the participant project before training.')
        if not request.get('training_data_url', '').startswith('wandb-artifact:///' + session.project + '/'):
            raise ValueError('Use reviewed training data from this participant project.')
        return submit_once(session, 'serverless-sft', request, forecast=forecast,
            approved_usd=approved_usd, submit=lambda body: self.request('POST', '/v1/preview/sft-training-jobs', body))

    def poll(self, session, job_key):
        return poll_job(session, job_key, fetch=lambda identity:
            self.request('GET', '/v1/preview/training-jobs/' + quote(identity, safe='')))

    def checkpoints(self, model_id):
        if not isinstance(model_id, str) or not model_id.strip():
            raise ValueError('Provide the registered model ID.')
        # Latest first: the API otherwise defaults to the oldest 20 checkpoints.
        return self.request('GET', '/v1/preview/models/' + quote(model_id, safe='')
                            + '/checkpoints?order=desc&limit=100')


def sft_examples(reviewed, cases, system_prompt=None, *, intents=None):
    """No teacher-only or test labels can enter the accepted-label training artifact."""
    intents = intents or sorted({case['label'] for case in cases.values() if 'label' in case})
    if not intents:
        raise ValueError('Provide the complete allowed intent list before preparing training data.')
    prompt = system_prompt or route_messages('', intents)[0]['content']
    examples, seen = [], set()
    for review in reviewed['rows']:
        if not review.get('verified') or review['split'] not in ('train', 'review', 'development'):
            raise ValueError('SFT requires reviewed training/development labels.')
        case = cases[review['case_id']]
        if case.get('split') not in ('train', 'review', 'development'):
            raise ValueError('The case must belong to a recorded training/development split.')
        if review['case_id'] in seen:
            raise ValueError('A case appears more than once in the accepted-label dataset.')
        seen.add(review['case_id'])
        answer = validate_route({'intent': review['accepted_label'], 'needs_review': False,
                                 'reason': review.get('evidence', {}).get('reason')
                                 or 'Route to ' + str(review['accepted_label']) + '.'}, intents)
        examples.append({'messages': [{'role': 'system', 'content': prompt},
            {'role': 'user', 'content': case['text']},
            {'role': 'assistant', 'content': json.dumps(answer)}]})
    if not examples:
        raise ValueError('Accept at least one reviewed example before preparing SFT.')
    return examples


def publish_sft_data(session, examples):
    import wandb
    fingerprint = digest(examples)
    with session.stage('advanced/sft-data', inputs={'examples': fingerprint}) as stage:
        if stage.needs_run:
            path = stage.output_dir / 'train.jsonl'
            path.write_text(''.join(json.dumps(row) + '\n' for row in examples))
            stage.record({'path': str(path.relative_to(session.root)), 'count': len(examples)}, files=[path])
    key = 'sft-data/' + fingerprint
    saved = session.read()['publications'].get(key)
    if saved:
        return saved
    pub = session.connect()
    with pub.run(digest([session.workspace_id, key])[:32], 'Reviewed routing examples', 'sft-data') as run:
        artifact = wandb.Artifact('reviewed-routing-' + fingerprint[:12], type='dataset',
            metadata={'format': 'jsonl', 'num_trajectories': len(examples)})
        artifact.add_file(str(session.file(stage.result['path'])), name='train.jsonl')
        logged = run.log_artifact(artifact).wait(timeout=120)
        result = {'url': 'wandb-artifact:///' + logged.qualified_name, 'artifact': logged.qualified_name,
                  'count': len(examples), 'run': run.url}
    with session.transaction() as state:
        state['publications'][key] = result
    return result


def sft_request(model_id, training_data_url, count, *, epochs=1, batch_size=8, learning_rate=5e-5):
    if (any(type(value) is not int for value in (count, epochs, batch_size))
            or not 1 <= batch_size <= 32 or not 1 <= epochs <= 3 or count < 1):
        raise ValueError('Use 1–32 examples per batch, 1–3 epochs, and a nonempty reviewed dataset.')
    if (type(learning_rate) not in (float, int) or not math.isfinite(learning_rate)
            or learning_rate <= 0):
        raise ValueError('Use a positive finite learning rate.')
    if not model_id or not re.fullmatch(r'wandb-artifact:///[^/]+/[^/]+/[^:]+:v\d+', training_data_url):
        raise ValueError('Use the registered model ID and an exact :vN training-data artifact.')
    steps = math.ceil(count * epochs / batch_size)
    return {'model_id': model_id, 'training_data_url': training_data_url,
            'config': {'batch_size': batch_size, 'learning_rate': [learning_rate] * steps, 'assistant_turns': 'last'}}


def aria_prompt(project, run_url, artifact, evaluation_url, queue):
    return (f'In {project}, inspect {run_url} and {evaluation_url}. Reproduce artifact {artifact}. '
            'Explain one observed failure using the saved inputs and outputs. Propose one change and '
            f'estimate its cost. Check that Launch queue {queue} has an active worker. '
            'Do not submit an experiment until I approve its code, data split, budget and run count. '
            'Keep final-test examples out of development. Return links for every claim.')
