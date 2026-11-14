"""Explicit managed-job submission, with durable IDs and conservative recovery."""

import math
import time

from filelock import FileLock

from .session import digest


class SubmissionNeedsReview(RuntimeError):
    pass


def validate_approval(forecast, approved_usd):
    """Check a recorded spending bound before any service allocates resources."""
    maximum = forecast.get('maximum_usd')
    if (not isinstance(approved_usd, (float, int)) or isinstance(approved_usd, bool)
            or not math.isfinite(approved_usd) or approved_usd < 0
            or not isinstance(maximum, (float, int)) or isinstance(maximum, bool)
            or not math.isfinite(maximum) or maximum < 0 or maximum > approved_usd
            or not forecast.get('basis') or not forecast.get('checked_at')):
        raise ValueError('Record a current cost bound and approve it before launching a job.')
    return maximum


def submit_once(session, name, request, *, forecast, approved_usd, submit):
    """The caller provides the service operation; this helper never retries a POST."""
    validate_approval(forecast, approved_usd)
    key = digest([name, request])[:32]
    with FileLock(str(session.root / ('.job-' + key + '.lock'))):
        saved = session.read().get('managed_jobs', {}).get(key)
        if saved and saved.get('job_id'):
            return saved
        if saved:
            raise SubmissionNeedsReview('Submission may have reached the provider. Find its job ID; do not submit again.')
        with session.transaction() as state:
            state.setdefault('managed_jobs', {})[key] = {
                'name': name, 'request': request, 'request_fingerprint': digest(request),
                'status': 'submitting', 'forecast': forecast, 'approved_usd': approved_usd,
                'submitted_at': time.time()}
        try:
            response = submit(request)
            job_id = response.get('job_id') or response.get('id')
            if not isinstance(job_id, str) or not job_id.strip():
                raise ValueError('The service returned no job ID. Check the provider before retrying.')
            with session.transaction() as state:
                state['managed_jobs'][key].update(job_id=job_id, status='submitted', response=response)
        except BaseException as error:
            with session.transaction() as state:
                state['managed_jobs'][key].update(status='submission_unknown', error=str(error)[:500])
            raise
        return session.read()['managed_jobs'][key]


def recover_job(session, key, job_id, *, lookup):
    """Attach an observed job only when its request identity matches the saved submission."""
    if not isinstance(job_id, str) or not job_id.strip():
        raise ValueError('Provide the observed provider job ID.')
    with FileLock(str(session.root / ('.job-' + key + '.lock'))):
        saved = session.read()['managed_jobs'][key]
        if saved.get('job_id'):
            if saved['job_id'] != job_id:
                raise ValueError('This submission already has a different job ID.')
            return saved
        observed = lookup(job_id)
        if (observed.get('request_fingerprint') != saved['request_fingerprint']
                or (observed.get('id') or observed.get('job_id')) != job_id):
            raise ValueError('The observed job does not match this submission. Inspect it with the provider.')
        with session.transaction() as state:
            state['managed_jobs'][key].update(job_id=job_id, status='submitted', recovery=observed)
        return session.read()['managed_jobs'][key]


def poll_job(session, key, *, fetch):
    saved = session.read()['managed_jobs'][key]
    if not saved.get('job_id'):
        raise SubmissionNeedsReview('Find the submitted job before monitoring it.')
    result = fetch(saved['job_id'])
    if (result.get('id') or result.get('job_id')) != saved['job_id']:
        raise ValueError('The service returned a different job. Saved monitoring was not changed.')
    with session.transaction() as state:
        state['managed_jobs'][key].update(last_status=result, last_checked_at=time.time())
    return result
