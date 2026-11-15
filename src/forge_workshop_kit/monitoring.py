"""Read participant progress. This module has no lesson-runtime dependencies."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlparse

from .manifest import get_workshop


def project_name(value):
    value = value.strip()
    if value.startswith('https://'):
        parsed = urlparse(value)
        if parsed.hostname not in ('forge.coreweave.com', 'wandb.ai'):
            raise ValueError('Use a Forge or W&B project link, or entity/project.')
        parts = parsed.path.strip('/').split('/')
        if parsed.hostname == 'forge.coreweave.com' and parts[0] in ('wandb', 'agent-lens', 'weave'):
            parts = parts[1:]
        value = '/'.join(parts[:2])
    parts = value.split('/')
    if len(parts) != 2 or not all(part and all(c.isalnum() or c in '-_.' for c in part) for part in parts):
        raise ValueError('A project has two parts: entity/project.')
    return value


def load_roster(path):
    path = Path(path)
    if not path.is_file():
        return {'projects': [], 'workshop': 'solar-autoresearch', 'since': '', 'until': '', 'workspace': '', 'session': ''}
    return json.loads(path.read_text(encoding="utf-8"))


def save_roster(path, settings):
    """Save public project links and filters on the facilitator's own runtime."""
    result = {key: str(settings.get(key, '')).strip() for key in ('workshop', 'since', 'until', 'workspace', 'session')}
    result['projects'] = list(dict.fromkeys(project_name(p) for p in settings.get('projects', []) if p.strip()))
    lower, upper = _timestamp(result['since']), _timestamp(result['until'])
    if lower is not None and upper is not None and upper < lower:
        raise ValueError('The end time must be after the start time.')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(result, indent=2), encoding="utf-8", newline="\n")
    temporary.replace(path)
    return result


def _timestamp(value):
    if value in ('', None):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).timestamp()


def _label(workshop_id, checkpoint):
    try:
        manifest = get_workshop(workshop_id)
    except ValueError:
        return checkpoint or 'Not started'
    key = next((target for prefix, target in manifest['checkpoint_prefixes'] if (checkpoint or '').startswith(prefix)), checkpoint)
    return dict(manifest['steps']).get(key, checkpoint or 'Not started')


def monitor(projects, workshop_id, *, api=None, since=None, until=None, workspace='', session='', max_workers=6):
    """Read progress concurrently; no response means unknown, never a failed exercise.

    Dates filter last published activity (UTC); workspace and session are exact IDs.
    Session uses notebook_identity when a publisher supplies it. Older runs without
    that field remain unknown instead of being assigned to the selected session.
    """
    lower, upper = _timestamp(since), _timestamp(until)
    if lower is not None and upper is not None and upper < lower:
        raise ValueError('The end time must be after the start time.')
    names = list(dict.fromkeys(project_name(p) for p in projects if p.strip()))
    def fetch(project):
        try:
            if api is None:
                import wandb
                client = wandb.Api(timeout=20)
            else:
                client = api
            filters = {'jobType': 'workshop-progress', 'config.workshop_id': workshop_id}
            if workspace:
                filters['config.workspace_id'] = workspace
            if session:
                filters['config.notebook_identity'] = session
            rows = []
            for run in client.runs(project, filters=filters):
                summary = dict(getattr(run.summary, '_json_dict', run.summary))
                updated = _timestamp(summary.get('updated_at'))
                config = dict(run.config)
                if workspace and config.get('workspace_id') != workspace:
                    continue
                if session and config.get('notebook_identity') != session:
                    continue
                if lower is not None and (updated is None or updated < lower):
                    continue
                if upper is not None and (updated is None or updated > upper):
                    continue
                rows.append(dict(project=project, workspace=config.get('workspace_id'), session=config.get('notebook_identity') or 'Not recorded',
                    step=_label(workshop_id, summary.get('step')), checkpoint=summary.get('step'),
                    status=summary.get('status', 'unknown'), completed=len(summary.get('completed', [])),
                    failed=summary.get('failed_executions', []), help=summary.get('help_request', ''),
                    updated_at=updated, last_update=datetime.fromtimestamp(updated, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') if updated else 'Unknown',
                    evidence=summary.get('evidence', {}), aria_investigations=summary.get('aria_investigations', {}), url=run.url))
            return rows or [dict(project=project, status='unknown', step='No matching progress update', last_update='Unknown')]
        except Exception as error:
            return [dict(project=project, status='unavailable', error=str(error)[:300], last_update='Unknown')]
    if not names:
        return []
    with ThreadPoolExecutor(max_workers=max(1, min(int(max_workers), len(names), 8))) as pool:
        return [row for rows in pool.map(fetch, names) for row in rows]
