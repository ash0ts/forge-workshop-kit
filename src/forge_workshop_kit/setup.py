"""Read project context and saved access receipts without contacting a service."""
from __future__ import annotations

import os
import time


def project_context(environ=None):
    env = os.environ if environ is None else environ
    hosted = bool(env.get('WANDB_NOTEBOOK_ANCHOR_RUN') or env.get('WANDB_NOTEBOOK_COLLECTION'))
    detected = '/'.join((env['WANDB_ENTITY'], env['WANDB_PROJECT'])) if env.get('WANDB_ENTITY') and env.get('WANDB_PROJECT') else ''
    return {'project': detected if hosted else env.get('WORKSHOP_PROJECT') or detected,
            'hosted': hosted, 'detected': bool(detected),
            'source': 'Copied notebook project' if hosted and detected else 'Local project setting' if env.get('WORKSHOP_PROJECT') and not hosted else 'Runtime project' if detected else 'Enter your project'}


def save_access(session, result):
    """Save the result of the explicit, free project-write check."""
    with session.transaction() as state:
        state['publications']['setup/access'] = {**result, 'checked_at': time.time()}


def capabilities(session):
    """Describe what has actually been verified; never probe inference on setup."""
    if session is None:
        return []
    state = session.read()
    publications = state.get('publications', {})
    access = publications.get('setup/access', {})
    traces = [r for key, r in publications.items() if key.startswith('trace/')]
    requests = list(state.get('requests', {}).values())
    comparisons = [r for key, rows in publications.items() if key.startswith('comparison/') for r in rows.values() if isinstance(r, dict)]
    def status(rows, field, expected):
        if any(row.get(field) == expected for row in rows):
            return 'Verified from saved work'
        return 'Not yet verified' if not rows else 'Upload needs attention'
    successful = any(r.get('status') == 'complete' for r in requests)
    latest = max(requests, key=lambda r: r.get('ended_at') or r.get('started_at') or 0, default={})
    inference_status = 'Latest request denied access' if latest.get('http_status') in (401, 403) else 'Verified from a saved response' if successful else 'Request needs attention' if requests else 'Not yet called'
    return [
        {'Capability': 'Project writes', 'Status': 'Verified' if access.get('write_access') else 'Access needs attention' if access.get('error') else 'Not yet checked',
         'What this means': access.get('error') or session.project},
        {'Capability': 'Agent Lens', 'Status': status(traces, 'verified', True),
         'What this means': 'The trace exercise checks stored spans. Project access alone does not check tracing.'},
        {'Capability': 'Inference', 'Status': inference_status,
         'What this means': 'Your first explicit model run checks inference access and uses your allowance.'},
        {'Capability': 'Weave evaluations', 'Status': status(comparisons, 'weave_status', 'published'),
         'What this means': 'Checked when you publish an evaluation from saved results.'},
        {'Capability': 'Native EvalTables', 'Status': status(comparisons, 'native_status', 'published'),
         'What this means': 'Separate from execution and Weave. A failed upload does not erase your results.'},
    ]


def recovery_label(workshop, row):
    from .manifest import get_workshop
    metadata = get_workshop(workshop)
    labels = dict(metadata['steps'])
    name = row['name']
    step = next((target for prefix, target in metadata['checkpoint_prefixes'] if name.startswith(prefix)), None)
    title = labels.get(step, 'Execution')
    return f"{title} · {name.replace('/', ' / ')} · {row['status']} · attempt {row['next_attempt'] - 1}"
