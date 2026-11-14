"""Editable exercises and display helpers for the transit software factory."""
from __future__ import annotations

import html
import json
from copy import deepcopy
from pathlib import Path

from .manifest import get_workshop
from .session import digest

STEPS = get_workshop('transit-factory')['steps']

ACCEPTANCE_STARTER = '''def check_departures(rows):
    # At 00:05 on Nov 29, this real Park Street train must still appear.
    # Its GTFS service day is Nov 28, while its departure is on Nov 29.
    raise NotImplementedError("Find trip 63926435 with the correct dates")
'''
ACCEPTANCE_SOLUTION = '''def check_departures(rows):
    return any(row["trip_id"] == "63926435"
               and row["service_date"] == "2024-11-28"
               and row["departure_time"] == "2024-11-29T00:08:00-05:00"
               for row in rows)
'''


def check_public_scenario(source, rows):
    """Run the learner's public acceptance condition on actual build output."""
    passed = functions(source)['check_departures'](rows)
    if not isinstance(passed, bool):
        raise ValueError('Return True or False from check_departures.')
    return {'passed': passed, 'status': 'passed' if passed else 'failed',
            'scenario': 'Park Street after midnight', 'source_fingerprint': digest(source), 'paid_calls': 0}


def check_acceptance(source):
    """Check one public scenario and two deliberate mutations, without a model."""
    from . import transit
    rows = transit.reference_departures(transit.load_data(), '70076', '2024-11-29T00:05:00-05:00')
    assert check_public_scenario(source, rows)['passed'], 'The real 00:08 departure should pass.'
    missing = [row for row in rows if row['trip_id'] != '63926435']
    assert not check_public_scenario(source, missing)['passed'], 'Reject a board that omits this departure.'
    wrong_day = [{**row, 'service_date': '2024-11-29'} if row['trip_id'] == '63926435' else row for row in rows]
    assert not check_public_scenario(source, wrong_day)['passed'], 'The service day is still November 28.'
    return {**check_public_scenario(source, rows), 'checks': ['Real departure accepted', 'Missing departure rejected', 'Wrong service day rejected']}

EXERCISES = {
    'worker': {
        'function': 'build_worker_request',
        'task': 'Give the builder its task, interface contract, source, and selected lessons. Then complete dispatch_action: route each returned action to its allowed tool and return the tool result. Keep acceptance answers out of the model request.',
        'hint': 'build_worker_request returns system and user messages. In dispatch_action, read action["action"], look that name up in tools, and call exactly that function with the action dictionary.',
        'starter': '''def build_worker_request(task, sources, lessons):
    import json
    # Include the task, current files, and the lessons in the user message.
    raise NotImplementedError("Build the two messages this worker will receive")

def dispatch_action(action, tools):
    # tools contains the six allowed operations, each accepting the action dict.
    # Return the selected tool's result so it can enter the next model request.
    raise NotImplementedError("Run the operation selected by the builder")
''',
        'solution': '''def build_worker_request(task, sources, lessons):
    import json
    return [
        {"role": "system", "content": "Implement only your assigned transit feature. Read the contract, inspect the source, and test your changes before submitting."},
        {"role": "user", "content": json.dumps({"task": task, "sources": sources, "lessons": lessons})},
    ]

def dispatch_action(action, tools):
    name = action["action"]
    if name not in tools:
        raise ValueError("Unknown builder operation: " + name)
    return tools[name](action)
''',
    },
    'tasks': {
        'function': 'ready_tasks',
        'task': 'Return only pending tasks whose dependencies have been integrated. A builder saying it is finished does not unblock another task.',
        'hint': 'Inspect each task’s status, then look up every dependency in the same task dictionary.',
        'starter': '''def ready_tasks(tasks):
    # tasks maps task IDs to records. Only integrated dependencies are ready.
    raise NotImplementedError("Return the IDs that can start")

def claim_task(board, task_id, worker_id):
    # The board performs the short, atomic ownership update.
    raise NotImplementedError("Claim the task before starting work")
''',
        'solution': '''def ready_tasks(tasks):
    return [key for key, task in tasks.items()
            if task["status"] == "pending"
            and all(tasks[parent]["status"] == "integrated"
                    for parent in task.get("depends_on", []))]

def claim_task(board, task_id, worker_id):
    return board.claim(task_id, worker_id)
''',
    },
    'memory': {
        'function': 'select_memories',
        'task': 'Retrieve accepted lessons for this project revision and task. Exclude proposed notes, unrelated topics, and lessons written for an older interface.',
        'hint': 'Require accepted status, matching scope and revision, and at least one matching tag.',
        'starter': '''def select_memories(entries, tags, scope, revision):
    # A useful-looking note may still be unverified or out of date.
    raise NotImplementedError("Select the lessons this worker may read")
''',
        'solution': '''def select_memories(entries, tags, scope, revision):
    return [entry for entry in entries
            if entry["status"] == "accepted"
            and entry["scope"] == scope
            and entry["version"] == revision
            and set(entry["tags"]) & set(tags)]
''',
    },
    'evaluate': {
        'function': 'score_scenario',
        'task': 'Compare the departure IDs and order returned by the app with the expected list. Test an omitted departure and a false completion claim. This is your development check; the final comparison also uses the independent supplied scorer.',
        'hint': 'A status message is not a departure. Compare the lists, including their order.',
        'starter': '''def score_scenario(actual, expected):
    # Inputs are lists of departure identifiers, in displayed order.
    raise NotImplementedError("Return whether the lists match")
''',
        'solution': '''def score_scenario(actual, expected):
    return actual == expected
''',
    },
    'release': {
        'function': 'release_decision',
        'task': 'Allow a release only when every reserved scenario has an available, passing result. Explain a blocked release instead of treating missing checks as success.',
        'hint': 'Require at least one row and every passed value to be exactly True.',
        'starter': '''def release_decision(rows):
    # A missing result is None, not a passing test.
    raise NotImplementedError("Choose release or retain the previous version")
''',
        'solution': '''def release_decision(rows):
    return bool(rows) and all(row.get("passed") is True for row in rows)
''',
    },
}


def functions(source):
    namespace = {}
    exec(compile(source, '<participant exercise>', 'exec'), namespace)
    return namespace


def check_exercise(name, source):
    """Free checks run the actual submitted functions. No provider is imported."""
    scope = functions(source)
    details = {}
    if name == 'worker':
        output = scope['build_worker_request']({'id': 'query', 'instructions': 'Use service time'},
                                              {'query.py': '# source'}, [{'text': 'Preserve 25:10'}])
        assert isinstance(output, list) and len(output) >= 2, 'Return system and user messages.'
        joined = json.dumps(output)
        assert all(word in joined for word in ('query.py', 'Use service time', 'Preserve 25:10')), 'The request lost source, instructions, or selected memory.'
        calls = []
        def read_file(action):
            calls.append(action)
            return {'content': '# actual tool observation'}
        action = {'action': 'read_file', 'path': 'query.py'}
        observation = scope['dispatch_action'](action, {'read_file': read_file})
        assert calls == [action], 'Dispatch exactly the requested tool once, with its arguments.'
        assert observation == {'content': '# actual tool observation'}, 'Return the tool observation for the next model request.'
        try:
            scope['dispatch_action']({'action': 'shell'}, {'read_file': read_file})
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError('Reject operations that are absent from the allowed tools.')
    elif name == 'tasks':
        tasks = {'query': {'status': 'pending', 'depends_on': []},
                 'view': {'status': 'submitted', 'depends_on': []},
                 'integrate': {'status': 'pending', 'depends_on': ['query', 'view']}}
        assert scope['ready_tasks'](tasks) == ['query'], 'Submitted work is not integrated.'
        tasks['query']['status'] = tasks['view']['status'] = 'integrated'
        assert scope['ready_tasks'](tasks) == ['integrate'], 'Integrated dependencies should unblock the task.'
        class Board:
            def claim(self, task_id, worker_id):
                return {'task_id': task_id, 'worker_id': worker_id}
        assert scope['claim_task'](Board(), 'query', 'builder-1') == {'task_id':'query','worker_id':'builder-1'}, 'Use the board’s atomic claim.'
        from . import transit
        details['coordination_repair'] = transit.qualify_coordination_repair()
        assert details['coordination_repair']['improved'], 'The repaired board must permit exactly one owner.'
    elif name == 'memory':
        valid = {'id':'checked','status':'accepted','scope':'transit','version':'r1','source_revision':'provenance-hash','tags':['time'],'text':'Keep hours above 24'}
        examples = [valid, {**valid,'id':'guess','status':'proposed'}, {**valid,'id':'stale','version':'r0'}, {**valid,'id':'unrelated','tags':['colors']}]
        assert scope['select_memories'](examples, ['time'], 'transit', 'r1') == [valid], 'Exclude unaccepted, stale, and unrelated notes.'
    elif name == 'evaluate':
        check = scope['score_scenario']
        assert check(['trip-1','trip-2'], ['trip-1','trip-2']) is True
        assert check(['trip-1'], ['trip-1','trip-2']) is False, 'A missing departure must fail.'
        assert check(['trip-2','trip-1'], ['trip-1','trip-2']) is False, 'The displayed order matters.'
    elif name == 'release':
        check = scope['release_decision']
        assert check([{'passed': True}]) is True
        for rows in ([], [{'passed':None}], [{'passed':False}], [{'passed':True},{'passed':None}]):
            assert check(rows) is False, 'Empty, failed, or unavailable checks cannot authorize a release.'
    return {'status':'passed','function':EXERCISES[name]['function'], 'source_fingerprint':digest(source), 'paid_calls':0, **details}


def saved(session, name):
    if session is None:
        return None
    rows = [row for row in session.read()['stages'].values()
            if row['name'] == name and row['status'] == 'complete']
    return max(rows, key=lambda row: row.get('ended_at',0), default=None)


def complete_steps(session):
    return session.read()['progress'].get('completed', []) if session else []


def stages_for_step(session, step):
    """Select saved executions relevant to the current exercise, without publishing."""
    prefixes = {
        'setup': ('factory/setup',),
        'worker': ('factory/build/solo/',),
        'tasks': ('factory/build/solo/',),
        'team': ('factory/build/team/',),
        'integrate': ('factory/integration/solo', 'factory/integration/team', 'factory/build/solo/', 'factory/build/team/'),
        'memory': ('factory/memory/', 'factory/integration/solo', 'factory/integration/team', 'factory/prepared-reference'),
        'followup': ('factory/build/without-memory/', 'factory/build/with-memory/', 'factory/integration/without-memory', 'factory/integration/with-memory'),
        'evaluate': ('factory/evaluate/',),
        'release': ('factory/release/', 'factory/evaluate/'),
    }.get(step, ())
    return [key for key, row in session.read()['stages'].items()
            if row['name'].startswith(prefixes)] if session else []


def with_evidence(snapshot, state):
    """Attach verified publication identities to a display copy of a saved board."""
    board = deepcopy(snapshot)
    events = {event['id']: event for event in board.get('events', [])}
    for key, receipt in state.get('publications', {}).items():
        if not key.startswith('trace/') or not receipt.get('verified') or not receipt.get('url'):
            continue
        stage = state.get('stages', {}).get(key.split('/', 1)[1], {})
        for event_id, span_id in receipt.get('span_ids', {}).items():
            event = events.get(event_id)
            if event is None:
                continue
            expected_stage = f"factory/build/{event.get('build_id')}/worker/{event.get('task_id')}"
            if stage.get('name') != expected_stage:
                continue
            links = {'Agent Lens conversation': receipt['url']}
            if receipt.get('trace_id') and span_id:
                links['Open this tool span'] = receipt['url'] + '/spans/turns/' + receipt['trace_id'] + '/spans/' + span_id
            event['evidence'] = links
            task = board.get('tasks', {}).get(event.get('task_id'))
            if task is not None:
                task.setdefault('evidence', {})['Builder conversation'] = receipt['url']
    return board


def safe(value):
    return html.escape(str(value))


VIEW_STYLE = '''<style>
.factory-view{font-family:inherit;margin:12px 0}.factory-view table{width:100%;border-collapse:collapse}
.factory-view td,.factory-view th{padding:10px;text-align:left;border-bottom:1px solid #8885;vertical-align:top}
.factory-view details{border:1px solid #8885;border-radius:8px;padding:12px;margin:8px 0}
.factory-view summary{cursor:pointer;font-weight:600}.factory-view pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:360px;overflow:auto}
.factory-view a{color:inherit;text-decoration:underline;text-underline-offset:3px}.factory-view a:focus-visible,.factory-view summary:focus-visible{outline:3px solid #29a8a0;outline-offset:3px}
.factory-view .factory-status{display:inline-block;border:1px solid #8887;border-radius:12px;padding:2px 8px;font-size:.85em}
.factory-view .factory-detail:target{outline:3px solid #29a8a0;outline-offset:4px}
@media(max-width:640px){.factory-view .factory-table-wrap{overflow-x:auto}.factory-view td,.factory-view th{padding:8px}}
</style>'''


def _anchor(kind, identity):
    return 'factory-' + kind + '-' + digest(str(identity))[:16]


def _details(label, value):
    return '<details><summary>' + safe(label) + '</summary><pre>' + safe(json.dumps(value, indent=2, default=str)) + '</pre></details>'


def _links(value):
    """Render only recorded absolute HTTPS links; never derive trace destinations."""
    links = value.get('evidence', value.get('links', {}))
    if not isinstance(links, dict):
        return ''
    return ' · '.join('<a href="' + safe(url) + '" target="_blank" rel="noopener noreferrer">' + safe(label) + '</a>'
                      for label, url in links.items() if isinstance(url, str) and url.startswith('https://'))


def task_board(snapshot):
    tasks = snapshot.get('tasks', {})
    if isinstance(tasks, list):
        tasks = {task['id']:task for task in tasks}
    prefix = snapshot.get('identity', 'example')
    body, detail = [], []
    for key, row in tasks.items():
        spec = row.get('spec', row)
        anchor = _anchor('task', str(prefix) + key)
        events = [event for event in snapshot.get('events', []) if event.get('task_id', event.get('arguments', {}).get('task_id')) == key]
        event_links = ' · '.join('<a href="#' + _anchor('event', event.get('id', digest(event))) + '">' + safe(event.get('name', 'Operation')) + '</a>' for event in events)
        title = spec.get('title', row.get('title', key))
        body.append(f'<tr><th><a href="#{anchor}">{safe(title)}</a></th><td><span class="factory-status">{safe(row.get("status","pending"))}</span></td><td>{safe(row.get("owner") or row.get("worker_id") or "Unclaimed")}</td><td>{safe(", ".join(spec.get("depends_on", [])) or "None")}</td></tr>')
        change = row.get('diff') or ('No changed files. This record may retain the starting version.' if row.get('decision') == 'KEEP' else 'No submitted diff yet.')
        detail.append('<details class="factory-detail" id="' + anchor + '"><summary>' + safe(title) + ': files, checks, and decision</summary>'
                      + '<p>' + safe(spec.get('instructions', '')) + '</p><p><strong>Editable files:</strong> ' + safe(', '.join(spec.get('editable_files', [])) or 'Not recorded') + '</p>'
                      + '<p><strong>Decision:</strong> ' + safe(row.get('decision', 'No submitted decision')) + '. ' + safe(row.get('rationale', '')) + '</p>'
                      + '<pre>' + safe(change) + '</pre>' + _details('Development test receipt', row.get('test_receipt', {}))
                      + '<p><strong>Recorded operations:</strong> ' + (event_links or 'None yet') + '</p>' + _links(row) + '</details>')
    return VIEW_STYLE + '<section class="factory-view"><p>Select a task to read its actual diff and tests. Follow an operation to its timeline entry.</p><div class="factory-table-wrap"><table><thead><tr><th>Task</th><th>Status</th><th>Owner</th><th>Waits for</th></tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>' + ''.join(detail) + '</section>'


def timeline(events):
    if not events:
        return '<p>No worker operations have been recorded for this build.</p>'
    ordered = sorted(events, key=lambda row:row.get('started_at',0))
    first = ordered[0].get('started_at',0)
    body, detail = [], []
    for row in ordered:
        anchor = _anchor('event', row.get('id', digest(row)))
        task = row.get('task_id', row.get('arguments', {}).get('task_id'))
        task_link = '<a href="#' + _anchor('task', str(row.get('board_fingerprint', 'example')) + task) + '">Back to task</a>' if task else ''
        body.append(f'<tr><td>{row.get("started_at",first)-first:.2f}s</td><td>{safe(row.get("worker_id") or row.get("arguments",{}).get("worker_id", "coordinator"))}</td><td><a href="#{anchor}">{safe(row.get("name","operation"))}</a></td><td>{safe(row.get("status","complete"))}</td><td>{max(0,row.get("ended_at",0)-row.get("started_at",0)):.2f}s</td></tr>')
        detail.append('<details class="factory-detail" id="' + anchor + '"><summary>' + safe(row.get('name', 'Operation')) + ' · ' + safe(row.get('worker_id', 'coordinator')) + '</summary><p>' + task_link + '</p>'
                      + _details('Arguments', row.get('arguments', {})) + _details('Returned result', row.get('result'))
                      + (_details('Recorded error', row['error']) if row.get('error') else '') + _links(row) + '</details>')
    return VIEW_STYLE + '<section class="factory-view"><p>Times are relative to the first recorded operation in this build. Select an operation to inspect its arguments and result.</p><div class="factory-table-wrap"><table><thead><tr><th>Start</th><th>Worker</th><th>Operation</th><th>Status</th><th>Duration</th></tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>' + ''.join(detail) + '</section>'


def release_history(records):
    """Show saved releases and explicit retain decisions, without inventing lineage."""
    if not records:
        return '<p>No release decision is saved yet. A passing development check does not release the app.</p>'
    cards = []
    for row in records:
        revision = row.get('source_fingerprint') or row.get('fingerprint')
        previous = row.get('previous_release')
        parent = '<a href="#' + _anchor('release', previous) + '">Previous saved version</a>' if previous and any(previous in (other.get('source_fingerprint'), other.get('fingerprint')) for other in records) else safe(previous or 'No preceding release recorded')
        cards.append('<details class="factory-detail" id="' + _anchor('release', revision or digest(row)) + '"><summary>' + safe(row.get('title') or row.get('label') or row.get('decision') or 'Saved release') + '</summary><p><strong>Decision:</strong> ' + safe(row.get('decision', 'Release')) + '</p><p><strong>Executed source:</strong> ' + safe(revision or 'No newly released source') + '</p><p>' + parent + '</p><p>' + safe(row.get('conclusion', row.get('reason', ''))) + '</p>' + _links(row) + _details('Saved release record', row) + '</details>')
    return VIEW_STYLE + '<section class="factory-view">' + ''.join(cards) + '</section>'


def capture_sources(session, names):
    return {name:session.get_draft('factory/'+name, EXERCISES[name]['starter']) for name in names}
