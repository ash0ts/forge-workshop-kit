from forge_workshop_kit.factory_teaching import with_evidence


def test_trace_links_require_the_same_build_and_task_without_changing_records():
    board = {'tasks': {'query': {'id': 'query'}}, 'events': [
        {'id': 'shared-claim-id', 'build_id': 'team', 'task_id': 'query'},
        {'id': 'unpublished', 'build_id': 'team', 'task_id': 'query'},
    ]}
    state = {
        'stages': {
            'team-stage': {'name': 'factory/build/team/worker/query'},
            'solo-stage': {'name': 'factory/build/solo/worker/query'},
        },
        'publications': {
            'trace/team-stage': {'verified': True, 'url': 'https://example.com/team',
                                 'trace_id': 'team-trace', 'span_ids': {'shared-claim-id': 'team-span'}},
            'trace/solo-stage': {'verified': True, 'url': 'https://example.com/solo',
                                 'trace_id': 'solo-trace', 'span_ids': {'shared-claim-id': 'solo-span'}},
        },
    }
    display = with_evidence(board, state)
    assert display['events'][0]['evidence'] == {
        'Agent Lens conversation': 'https://example.com/team',
        'Open this tool span': 'https://example.com/team/spans/turns/team-trace/spans/team-span',
    }
    assert display['tasks']['query']['evidence']['Builder conversation'] == 'https://example.com/team'
    assert 'evidence' not in display['events'][1]
    assert all('evidence' not in row for row in board['events'])
    assert 'evidence' not in board['tasks']['query']

    state['publications']['trace/team-stage']['verified'] = False
    assert 'evidence' not in with_evidence(board, state)['events'][0]
