"""Repair one concrete retry error before the open-ended harness comparison."""

import copy
import time

from .cases import CASES
from .simulator import execute
from .teaching import compile_code


STARTER = '''def recover_access(arguments, call_tool):
    # The first call timed out. It may already have added the member.
    # Repair this retry, then read onboarding_status to confirm the account.
    retry = dict(arguments, operation_id=arguments["operation_id"] + "-retry")
    return call_tool("provision_member", retry)
'''

ANSWER = '''def recover_access(arguments, call_tool):
    # Reuse the operation identity for the same write.
    receipt = call_tool("provision_member", dict(arguments))
    return call_tool("onboarding_status", {"account_id": arguments["account_id"]})
'''


def run_recovery(source):
    """Execute the learner's function against a fresh public development incident."""
    fn = compile_code(source)['recover_access']
    case = next(c for c in CASES if c.id == 'missing-seat')
    world = copy.deepcopy(case.initial)
    events = []
    def call_tool(name, arguments):
        nonlocal world
        started = time.time()
        world, result = execute(world, name, copy.deepcopy(arguments), fault='provision_timeout_after_commit')
        events.append({'id': 'recovery-tool-' + str(len(events)), 'name': name,
                       'arguments': copy.deepcopy(arguments), 'result': copy.deepcopy(result),
                       'started_at': started, 'ended_at': time.time(),
                       'error': result.get('error')})
        return result
    arguments = {'account_id': 'fern', 'email': 'alex@example.test', 'role': 'member', 'operation_id': 'join-alex'}
    first = call_tool('provision_member', arguments)
    if first.get('error') != 'timeout':
        raise AssertionError('The practice case no longer produces a committed-write timeout.')
    error = None
    try:
        result = fn(copy.deepcopy(arguments), call_tool)
    except Exception as exception:
        result, error = None, str(exception)
    members = world['accounts']['fern']['members']
    single = members == [{'email': 'alex@example.test', 'role': 'member'}]
    verified = any(e['name'] == 'onboarding_status' and not e.get('error') for e in events[1:])
    return {'case_id': case.id, 'world': world, 'events': events, 'result': result,
            'error': error, 'membership_count': len(members), 'duplicates': max(0, len(members)-1),
            'single_membership': single, 'verified_account': verified,
            'passed': single and verified and error is None}


def comparison_rows(before, after):
    return {label: [{'case_id': run['case_id'], 'input': {'incident': 'write committed before timeout'},
                     'prediction': run['world']['accounts']['fern']['members'],
                     'target': [{'email': 'alex@example.test', 'role': 'member'}],
                     'error': 0 if run['single_membership'] else 1,
                     'scores': {'duplicates': run['duplicates'], 'verified_account': run['verified_account']},
                     'evidence': {'events': run['events'], 'function_error': run['error']}}]
            for label, run in [('new-id-retry', before), ('your-recovery', after)]}
