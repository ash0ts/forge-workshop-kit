"""Native Agent Lens readback and explicit Alignment tests. No work runs on import."""
from __future__ import annotations

import time
from urllib.parse import quote

import httpx

from .publication import credentials
from .session import digest


class LensClient:
    """Project-scoped API used by the native Tags and Insights screens."""

    def __init__(self, project, *, transport=None, api_key=None):
        pieces = project.split('/')
        if len(pieces) != 2 or not all(pieces):
            raise ValueError('Use an entity/project destination.')
        self.project = project
        self.http = httpx.Client(base_url='https://forge.coreweave.com/api/pulse/',
            headers={'Authorization': 'Bearer ' + (api_key or credentials()),
                     'x-wandb-entity': pieces[0], 'x-wandb-project': pieces[1]},
            transport=transport, timeout=60)

    def close(self):
        self.http.close()

    def _request(self, method, path, **kwargs):
        response = self.http.request(method, path, **kwargs)
        if response.status_code in (401, 403):
            raise PermissionError(f'Agent Lens access denied ({response.status_code}) for {self.project}. Check the account and project permissions.')
        response.raise_for_status()
        body = response.json()
        if 'data' not in body:
            raise ValueError('Agent Lens returned an unrecognized response. Keep results unavailable.')
        return body['data']

    def tags(self):
        return self._request('GET', 'tags') or []

    def tag(self, tag_id):
        return self._request('GET', 'tags/' + quote(tag_id, safe=''))

    def alignment(self, tag_id):
        return self._request('GET', 'tags/' + quote(tag_id, safe='') + '/alignment_examples') or []

    def outcomes(self, conversation_ids, agent_name=None):
        ids = list(dict.fromkeys(conversation_ids))
        if not ids:
            return []
        if len(ids) > 5000:
            raise ValueError('Select at most 5,000 conversations per read.')
        rows = self._request('POST', 'conversation-tags/query', json={'conversation_ids': ids}) or []
        return [row for row in rows if row['conversation_id'] in ids
                and (agent_name is None or row['agent_name'] == agent_name)]

    def insights_status(self):
        return {'weeks': self._request('GET', 'insights/latest-week'),
                'clustering': self._request('GET', 'insights/clustering-status')}

    def test(self, tag_id, example_id, criteria):
        return self._request('POST', 'tags/' + quote(tag_id, safe='') + '/test',
            params={'example_id': example_id}, json={'criteria': criteria})


def tag_definition(row):
    return {key: row.get(key) for key in ('id', 'name', 'criteria', 'agent_name_filter')}


def save_tag_snapshot(session, tag_id, agent_name, require_enabled=False, *, client=None):
    lens = client or LensClient(session.project)
    try:
        row = lens.tag(tag_id)
        if row.get('agent_name_filter') != [agent_name]:
            raise ValueError('Scope this tag to the exact workshop agent shown in the notebook. An empty filter applies more broadly.')
        if not row.get('criteria'):
            raise ValueError('Save the tag criteria in Agent Lens first.')
        if require_enabled and row.get('llm_judge_enabled') is not True:
            raise ValueError('Enable Apply with AI for this workshop agent before sending the monitoring batch.')
        snapshot = {**row, 'definition_fingerprint': digest(tag_definition(row)),
            'read_at': time.time(), 'project': session.project,
            'url': f'https://forge.coreweave.com/agent-lens/{session.project}/tags/{quote(tag_id, safe="")}'}
        with session.transaction() as state:
            snapshots = state.setdefault('native_tag_snapshots', {})
            frozen = snapshots.get('frozen')
            if require_enabled and frozen and frozen['definition_fingerprint'] != snapshot['definition_fingerprint']:
                raise ValueError('The tag definition changed after monitoring was frozen. Restore the frozen criteria before comparing versions.')
            snapshots[snapshot['definition_fingerprint']] = snapshot
            snapshots['current'] = snapshot
            if require_enabled:
                snapshots['frozen'] = snapshot
        return snapshot
    finally:
        if client is None:
            lens.close()


def read_monitoring(session, tag_id, conversation_ids, agent_name, *, client=None):
    """A missing positive assignment does not establish a completed negative judgment."""
    conversation_ids = list(dict.fromkeys(conversation_ids))
    lens = client or LensClient(session.project)
    try:
        native = lens.tag(tag_id)
        frozen = session.read().get('native_tag_snapshots', {}).get('frozen')
        if frozen and digest(tag_definition(native)) != frozen['definition_fingerprint']:
            raise ValueError('Native tag criteria differ from the frozen monitoring rule.')
        assignments = [row for row in lens.outcomes(conversation_ids, agent_name)
                       if row.get('tag_id') == tag_id and row.get('source') == 'judge']
        rows = []
        for conversation_id in dict.fromkeys(conversation_ids):
            matches = [row for row in assignments if row['conversation_id'] == conversation_id]
            rows.append({'conversation_id': conversation_id,
                'status': 'tagged' if matches else 'unobserved',
                'prediction': True if matches else None,
                'explanation': 'Native AI assignment observed.' if matches else
                    'No AI assignment observed. It may be pending or a completed no-match; this API does not distinguish them.',
                'assignments': matches,
                'url': f'https://forge.coreweave.com/agent-lens/{session.project}/conversations/{conversation_id}'})
        result = {'rows': rows, 'tag_id': tag_id, 'read_at': time.time(),
            'processing_coverage': None, 'cost_usd': None,
            'native_billing': 'Native tag judging is outside the notebook inference allowance.'}
        with session.transaction() as state:
            state.setdefault('native_monitoring', {})[digest([tag_id, list(conversation_ids)])] = result
        return result
    finally:
        if client is None:
            lens.close()


def test_alignment(session, tag_id, example_id, criteria, *, client=None):
    """Explicit billed native test; a saved completed test is reused without another call."""
    if not criteria.strip() or len(criteria) > 1600:
        raise ValueError('Native criteria must contain 1–1,600 characters.')
    key = digest([session.project, tag_id, example_id, criteria])
    prior = session.read().get('native_alignment', {}).get(key)
    if prior:
        if prior['status'] == 'complete':
            return prior
        raise RuntimeError('The native judge test has an unavailable or uncertain outcome. Inspect its saved receipt; it will not be automatically resent.')
    lens = client or LensClient(session.project)
    try:
        examples = {row['id']: row for row in lens.alignment(tag_id)}
        if example_id not in examples:
            raise ValueError('Choose an Alignment example from this tag and project.')
        example = examples[example_id]
        name = lens.tag(tag_id)['name']
        receipt = {'id': key, 'tag_id': tag_id, 'example': example, 'criteria': criteria,
            'criteria_fingerprint': digest(criteria), 'status': 'pending',
            'started_at': time.time(), 'cost_usd': None, 'billing': 'native_tag_judge'}
        with session.transaction() as state:
            state.setdefault('native_alignment', {})[key] = receipt
        try:
            rows = lens.test(tag_id, example_id, criteria)
            if not isinstance(rows, list) or any(not isinstance(row, dict) or 'tag' not in row or 'reason' not in row for row in rows):
                raise ValueError('Native test did not return its documented result list.')
            receipt.update(status='complete', prediction=any(row['tag'] == name for row in rows), results=rows)
        except Exception as error:
            receipt.update(status='unavailable', prediction=None, error=str(error)[:500])
        receipt['ended_at'] = time.time()
        with session.transaction() as state:
            state['native_alignment'][key] = receipt
        return receipt
    finally:
        if client is None:
            lens.close()
