"""Select and reproduce exact artifacts. Registry linking does not deploy a model."""

import re
import time

from filelock import FileLock

from .session import digest


def record_release(session, *, artifact, evaluation, decision, metrics, checks,
                   previous=None, reason, actor='participant'):
    if not re.fullmatch(r'[^/]+/[^/]+/[^:]+:v\d+', artifact):
        raise ValueError('Use an exact artifact version, such as entity/project/model:v2.')
    if previous is not None and not re.fullmatch(r'[^/]+/[^/]+/[^:]+:v\d+', previous):
        raise ValueError('Pin the previous artifact to an exact :vN version too.')
    if decision not in ('release', 'reject', 'rollback'):
        raise ValueError('Choose release, reject, or rollback.')
    if not evaluation or not reason.strip():
        raise ValueError('Link the evaluation and explain your decision.')
    if decision != 'reject' and (not checks or any(v is not True for v in checks.values())):
        raise ValueError('All release checks must pass before selecting this artifact.')
    if decision == 'rollback' and not previous:
        raise ValueError('Identify the version being replaced by the rollback.')
    record = {'artifact': artifact, 'evaluation': evaluation, 'decision': decision,
                  'metrics': metrics, 'checks': checks, 'previous': previous, 'reason': reason, 'actor': actor}
    record['id'] = digest(record)[:32]
    with session.transaction() as state:
        records = state.setdefault('releases', {})
        if record['id'] in records:
            return records[record['id']]
        record['created_at'] = time.time()
        records[record['id']] = record
    return record


def reproduce(artifact, *, root, api=None):
    if not re.fullmatch(r'[^/]+/[^/]+/[^:]+:v\d+', artifact):
        raise ValueError('Reproduction requires a pinned :vN artifact, not latest.')
    if api is None:
        import wandb
        api = wandb.Api()
    return api.artifact(artifact).download(root=str(root))


def link_registry(session, release_id, target):
    if not re.fullmatch(r'(?:[^/]+/)?wandb-registry-[^/]+/[^/]+', target):
        raise ValueError('Choose a Registry collection, for example wandb-registry-Models/routing.')
    identity = digest([session.workspace_id, release_id, target])[:32]
    with FileLock(str(session.root / ('.registry-' + identity + '.lock'))):
        release = session.read().get('releases', {}).get(release_id)
        if not release or release['decision'] == 'reject':
            raise ValueError('Choose an accepted, evaluated release first.')
        saved = release.get('registry', {}).get(target)
        if saved:
            return saved
        pub = session.connect()
        with pub.run(identity, 'Link evaluated version', 'workshop-release') as run:
            artifact = run.use_artifact(release['artifact'])
            linked = run.link_artifact(artifact, target_path=target)
            receipt = {'artifact': release['artifact'], 'target': target,
                       'url': getattr(linked, 'url', None), 'run': run.url}
            # A run-close failure must not discard a completed link and cause a repeat.
            with session.transaction() as state:
                state['releases'][release_id].setdefault('registry', {})[target] = receipt
        return receipt
