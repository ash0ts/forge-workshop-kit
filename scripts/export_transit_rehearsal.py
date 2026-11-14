"""Export public transit rehearsal evidence without credentials or transport headers."""

import argparse
import json
from pathlib import Path

from forge_workshop_kit import transit
from forge_workshop_kit.session import digest


def export(folder):
    state = json.loads((folder / 'journal.json').read_text())
    workspace_identity = json.loads((folder / 'identity.json').read_text())
    requests = []
    for identity, row in state['requests'].items():
        response = row.get('response') or {}
        choice = (response.get('choices') or [{}])[0]
        requests.append({
            'identity': identity,
            **{key: row.get(key) for key in (
                'status', 'request_fingerprint', 'started_at', 'ended_at',
                'observed_usd', 'unknown_usd', 'reserved_usd', 'error')},
            'request': row['request'],
            'response_id': response.get('id'),
            'returned_model': response.get('model'),
            'usage': response.get('usage'),
            'finish_reason': choice.get('finish_reason'),
            'content': choice.get('message', {}).get('content'),
        })
    stages = [{key: row.get(key) for key in (
        'id', 'name', 'status', 'config', 'inputs', 'sources', 'source_fingerprint',
        'started_at', 'ended_at', 'result', 'events', 'error')}
        for row in state['stages'].values()]
    costs = {
        'observed_usd': sum(row.get('observed_usd') or 0 for row in requests),
        'bounded_unknown_usd': sum(row.get('unknown_usd') or 0 for row in requests),
        'inflight_usd': sum(row.get('reserved_usd') or 0 for row in requests
                           if row['status'] in ('pending', 'reserved')),
    }
    public = {
        'rehearsal': folder.name,
        'workshop': workspace_identity['workshop'],
        'workspace_id': workspace_identity['workspace_id'],
        'project': workspace_identity['project'],
        'dataset': transit.data_manifest(),
        'stages': stages,
        'requests': requests,
        'costs': costs,
        'builds': state.get('factory_boards', {}),
        'workshop_state': state.get('factory_workshop', {}),
        'publications': state.get('publications', {}),
        'export_note': 'Transport headers, local credentials, and model reasoning are omitted; local board paths are relative. '
                       'Returned actions, requested settings, usage and provider response IDs are retained.',
    }
    for build in public['workshop_state'].get('builds', {}).values():
        result = build.get('result', {})
        if result.get('board_path'):
            result['board_path'] = str(Path(result['board_path']).relative_to(folder.resolve()))
    # Release receipts also contain local app paths. Keep their relationship to
    # this workspace without publishing the maintainer's filesystem location.
    prefix = str(folder.resolve()) + '/'
    def local_paths(value):
        if isinstance(value, dict):
            return {key: local_paths(item) for key, item in value.items()}
        if isinstance(value, list):
            return [local_paths(item) for item in value]
        if isinstance(value, str) and value.startswith(prefix):
            return value[len(prefix):]
        return value
    return local_paths(public)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = [export(folder) for folder in args.state]
    payload = {'schema_version': 1, 'rehearsals': rows,
               'total_inference_usd': sum(row['costs']['observed_usd'] for row in rows),
               'bounded_unknown_usd': sum(row['costs']['bounded_unknown_usd'] for row in rows),
               'inflight_usd': sum(row['costs']['inflight_usd'] for row in rows)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps({'file': str(args.output), 'sha256': digest(payload),
                      'rehearsals': len(rows), 'inference_usd': payload['total_inference_usd']}))


if __name__ == '__main__':
    main()
