"""Portable visual vocabulary and read-only views of saved improvement records."""
from __future__ import annotations

import difflib
import json
import re
from copy import deepcopy
from importlib.resources import files

from .session import digest


def contract():
    """Return a fresh copy so a notebook cannot alter another view's vocabulary."""
    return json.loads(files('forge_workshop_kit').joinpath('assets', 'visuals.json').read_text())


def _result(row):
    value = (row or {}).get('result', {})
    return value if isinstance(value, dict) else {}


def _decision(row):
    value = _result(row)
    return value['decision'] if isinstance(value.get('decision'), dict) else value


def _fingerprint(value, row=None):
    for key in ('harness_fingerprint', 'fingerprint', 'source_fingerprint'):
        if value.get(key):
            return value[key]
    if isinstance(value.get('source'), str):
        return digest({'candidate.py': value['source']})
    return (row or {}).get('source_fingerprint')


def _files(value):
    if isinstance(value.get('source'), str):
        return {'candidate.py': value['source']}
    harness = value.get('harness')
    if isinstance(harness, dict):
        mapping = {'instructions': 'instructions.md', 'verification_skill': 'skills/verify-operation.md',
                   'tool_skill': 'skills/office-tools.md'}
        result = {mapping[k]: v for k, v in harness.items() if k in mapping}
        workflow = {k: v for k, v in harness.items() if k not in mapping}
        if workflow:
            result['workflow.json'] = json.dumps(workflow, sort_keys=True, indent=2)
        return result
    return {}


def _diff(before, after):
    if not before or not after:
        return None
    return '\n'.join(line for name in sorted(set(before) | set(after))
                     for line in difflib.unified_diff(str(before.get(name, '')).splitlines(),
                         str(after.get(name, '')).splitlines(), fromfile='previous/' + name,
                         tofile='proposed/' + name, lineterm=''))


def _references(value):
    """Read explicit execution references; do not interpret filenames as evidence reads."""
    found = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ('stage_id', 'execution', 'tested') and isinstance(item, str):
                found.add(item)
            elif isinstance(item, (dict, list)):
                found.update(_references(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_references(item))
    return found


def _execution(row, stages):
    """Resolve wrapper receipts to the actual stage, including interrupted executions."""
    saved = _result(row)
    value = saved.get('run', saved.get('adopted', saved))
    value = value if isinstance(value, dict) else {}
    identity = saved.get('execution') or value.get('stage_id')
    actual = stages.get(identity, {}) if identity else {}
    if not actual and row and any(k in value for k in ('metrics', 'scores', 'world')):
        actual = row
        identity = row['id']
    result = {**_result(actual), **value}
    return {'id': identity, 'record': actual, 'result': result,
            'status': actual.get('status', 'unavailable'),
            'fingerprint': _fingerprint(result, actual),
            'metrics': result.get('metrics', result.get('scores', {}))}


def branch_records(state):
    """Adapt Pending and Solar journals without changing records or contacting services.

    Proposal contents, tested files, and the selection are separate nodes. A shared
    fingerprint establishes identical files, not that a particular proposal was adopted.
    """
    state = deepcopy(state)
    stages = state.get('stages', {})
    rows = sorted(stages.values(), key=lambda r: (r.get('started_at', 0), r.get('id', '')))
    groups = {}
    for row in rows:
        match = re.match(r'(.*/round-(\d+))/([^/].*)', row.get('name', ''))
        if match:
            groups.setdefault((match[1], int(match[2])), []).append(row)
    output = []
    for (prefix, number), group in groups.items():
        def find(*names, group=group, prefix=prefix):
            candidates = [r for r in group if r['name'] in [prefix + '/' + n for n in names]]
            # A successful saved retry is usable even if an earlier request failed.
            return next((r for r in reversed(candidates) if r.get('status') == 'complete'),
                        candidates[-1] if candidates else None)

        proposal, composition = find('propose'), find('compose')
        selected = find('adopt', 'adopted')
        parent = ((proposal or {}).get('inputs', {}).get('evidence', {}).get('parent'))
        parent_files = (_files({'harness': parent}) if isinstance(parent, dict)
                        else {k: v for k, v in (proposal or {}).get('sources', {}).items()
                              if k == 'candidate.py'})
        nodes = []

        def add(key, title, role, row=None, *, decision=None, execution_row=None,
                group=group, prefix=prefix, number=number, nodes=nodes, parent_files=parent_files):
            decision = decision or {}
            execution = _execution(execution_row, stages) if execution_row else None
            proposed_fp = _fingerprint(decision) if decision else None
            match = (execution['fingerprint'] == proposed_fp
                     if execution and execution['fingerprint'] and proposed_fp else None)
            sources = _files(decision)
            change = decision.get('diff')
            if change is None:
                change = _diff(parent_files, sources)
            status = (row or {}).get('status', 'not_run')
            if key.startswith('candidate-'):
                status = 'proposed' if decision else 'not_run'
            ids = [r['id'] for r in (row, execution_row) if r]
            if execution and execution['id']:
                ids.append(execution['id'])
            if key == 'selection' and row:
                tested = row.get('inputs', {}).get('tested') or _result(row).get('execution')
                if tested in stages:
                    ids.append(tested)
            node = {'id': prefix + '/' + key, 'key': key, 'round': number, 'title': title,
                    'role': role, 'status': status, 'record_id': (row or {}).get('id'),
                    'record_ids': list(dict.fromkeys(ids)), 'decision': decision,
                    'fingerprint': proposed_fp, 'diff': change, 'files': sources,
                    'execution': execution, 'fingerprint_match': match,
                    'selected': key == 'selection' and status == 'complete',
                    'retained': bool(_result(row).get('retained_parent')),
                    'result': _result(row), 'sources': (row or {}).get('sources', {}),
                    'attempts': [r for r in group if row and r['name'] == row['name']]}
            nodes.append(node)
            return node

        starting = next((r for r in reversed(group) if '/starting/' in r['name']), None)
        if starting:
            add('parent', 'Starting version on this case', 'parent', starting, execution_row=starting)
        add('proposal', 'Propose two changes', 'parent', proposal)
        candidates = _result(proposal).get('candidates', [])
        for index, letter in enumerate(('a', 'b')):
            candidate = candidates[index] if len(candidates) > index else {}
            role = 'candidate_' + letter
            add('candidate-' + letter, candidate.get('title', 'Candidate ' + letter.upper()),
                role, proposal if candidate else None, decision=candidate)
            probe = find('probe-' + letter, 'probe-result-' + str(index), 'probe-' + str(index))
            if not probe:
                probe = next((r for r in reversed(group)
                              if r['name'].startswith(prefix + '/probe-' + letter + '-execution/')), None)
            add('probe-' + letter, 'Test candidate ' + letter.upper(), role, probe,
                decision=candidate, execution_row=probe)
        composed = _decision(composition)
        add('compose', composed.get('title', 'Choose changes for a combined version'),
            'composition', composition, decision=composed)
        tested = find('composition-result', 'composition-test', 'composition')
        if not tested:
            tested = next((r for r in reversed(group)
                           if r['name'].startswith(prefix + '/composition-test-execution/')), None)
        add('composition-test', 'Test the composition', 'composition', tested,
            decision=composed, execution_row=tested)
        saved = _result(selected)
        retained = saved.get('retained_parent') or (composed.get('decision') == 'KEEP'
            and saved.get('fingerprint') and saved.get('fingerprint') == composed.get('fingerprint'))
        selected_value = saved.get('adopted', saved)
        selected_node = add('selection', 'Retain this version' if retained else 'Save selected version',
                            'selection', selected, decision=selected_value, execution_row=selected)
        selected_node['retained'] = bool(retained)
        if selected and composition:
            selected_node['composition_recommendation'] = composed
            selected_node['record_ids'].append(composition['id'])
        # A failed composition can point to the tested files while selecting the parent.
        # Keep that attempted execution visible without claiming the parent ran here.
        if selected_node['execution'] and selected_node['fingerprint_match'] is False:
            selected_node['selection_execution_mismatch'] = True
        reflection = find('reflection')
        if reflection:
            add('reflection', 'Save what this execution taught us', 'composition', reflection)
            if selected:
                selected_node['record_ids'].append(reflection['id'])
        edges = []
        by_key = {node['key']: node for node in nodes}
        for origin, target in (('candidate-a', 'probe-a'), ('candidate-b', 'probe-b'),
                               ('compose', 'composition-test')):
            node = by_key[target]
            if node['execution'] and node['fingerprint_match'] is True:
                edges.append({'from': by_key[origin]['id'], 'to': node['id'], 'kind': 'code'})
        reviewed = _references((composition or {}).get('inputs', {}))
        for key in ('probe-a', 'probe-b'):
            node = by_key[key]
            if node['execution'] and node['execution']['id'] in reviewed:
                edges.append({'from': node['id'], 'to': by_key['compose']['id'], 'kind': 'evidence'})
        selected_execution = selected_node['execution']
        if (selected_node['selected'] and selected_execution
                and selected_node['fingerprint_match'] is True):
            for node in nodes:
                if (node['key'] != 'selection' and node['execution']
                        and node['execution']['id'] == selected_execution['id']):
                    edges.append({'from': node['id'], 'to': selected_node['id'], 'kind': 'selection'})
                    break
        represented = {identity for n in nodes for identity in n['record_ids']}
        order = ['parent', 'proposal', 'candidate-a', 'probe-a', 'candidate-b', 'probe-b',
                 'compose', 'composition-test', 'selection', 'reflection']
        nodes.sort(key=lambda n: order.index(n['key']))
        output.append({'id': prefix, 'round': number, 'nodes': nodes, 'edges': edges,
                       'other_records': [r for r in group if r['id'] not in represented]})
    return output
