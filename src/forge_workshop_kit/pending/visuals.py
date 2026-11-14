"""Saved-record views and free office practice. No model or publication calls."""

import copy
import json
from html import escape

from .cases import CASES
from .simulator import execute


STYLE = """<style>
.pending-visual{color:inherit;font-family:inherit;line-height:1.5;margin:16px 0}
.pending-visual h3{font-size:1.15rem;margin:0 0 12px}.pending-visual h4{font-size:1rem;margin:0 0 8px}
.pending-visual .pv-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:16px}
.pending-visual .pv-cell{border:1px solid var(--wk-line,#9baca6);border-radius:7px;padding:16px;min-width:0}
.pending-visual p{margin:8px 0}.pending-visual .pv-kicker{font-size:.8rem;letter-spacing:.035em;text-transform:uppercase}
.pending-visual code{overflow-wrap:anywhere}.pending-visual pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.85rem;line-height:1.5;margin:8px 0;padding:12px;border:1px solid var(--wk-line,#9baca6);border-radius:5px}
.pending-visual .pv-highlight{border-left:4px solid #d2a43c;padding-left:12px}.pending-visual .pv-muted{font-size:.9rem}
.pending-visual table{border-collapse:collapse;width:100%;font-size:.92rem}.pending-visual td,.pending-visual th{border-bottom:1px solid var(--wk-line,#9baca6);padding:10px;text-align:left;vertical-align:top}
.pending-visual a:focus-visible{outline:3px solid #d2a43c;outline-offset:3px}.pending-visual summary{cursor:pointer}
@media(max-width:600px){.pending-visual .pv-table{overflow-x:auto}.pending-visual .pv-cell{padding:12px}}
</style>"""


def _text(value):
    return escape(str(value))


def _json(value):
    return "<pre>" + escape(json.dumps(value, indent=2, ensure_ascii=False)) + "</pre>"


def _section(title, content):
    return STYLE + '<section class="pending-visual"><h3>' + escape(title) + "</h3>" + content + "</section>"


def _cell(title, content):
    return '<div class="pv-cell"><h4>' + escape(title) + "</h4>" + content + "</div>"


def _link(url, label):
    if not isinstance(url, str) or not url.startswith("https://"):
        return "<p>Conversation link not available yet.</p>"
    return '<p><a href="' + escape(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + escape(label) + " ↗</a></p>"


def office_brief():
    """The two public development tickets, before their implementation lessons."""
    return _section("Two tickets for our new colleague", '<div class="pv-grid">' + _cell(
        "Billing · Acme", "<p>Two captured payments of $49 share invoice inv-1.</p><p><strong>Required outcome:</strong> refund pay-2 once, keep pay-1 and other accounts unchanged.</p>"
    ) + _cell(
        "Account access · Fern", "<p>Add alex@example.test with the member role. The write can succeed before its response times out.</p><p><strong>Required outcome:</strong> one membership, with an explanation supported by the account.</p>"
    ) + '</div><p class="pv-muted">Fictional accounts, executable Python tools. The model chooses an action; Python changes the account; independent checks assess the result.</p>')


def handoff_frames(check):
    """Render the learner's saved local check, never a fabricated model response."""
    if not all(key in check for key in ("action", "result", "next_request")):
        return {}
    action = check["action"]
    request = check["next_request"]
    name, arguments = action.get("action"), action.get("arguments", {})
    frames = {
        "1 · Selected action": _section("Read the action fields", '<p>The free check supplies this action. It is not a model response.</p>' + _json(action) + '<p class="pv-highlight">The dispatcher reads <code>action</code> as the tool name and passes <code>arguments</code> to the function.</p>'),
        "2 · Python call": _section("Your dispatcher routes the arguments", _json({"name": name, "arguments": arguments}) + '<pre>my_dispatch(name, arguments, world, my_invoice_tool, call_tool)\n\n# lookup_invoice takes this branch:\nworld, my_invoice_tool(world, **arguments)</pre><p>Both dispatcher paths return the account state and the tool result. A lookup leaves state unchanged.</p>'),
        "3 · Returned records": _section("The tool returns these records", _json(check["result"]) + '<p>These are the actual records returned by your function in the saved check.</p>'),
        "4 · Next request": _section("Your observation function appends two messages", '<p>The earlier messages stay intact. The action and its result become the last two messages:</p>' + _json(request[-2:]) + '<p class="pv-highlight">This workshop uses a JSON action protocol in ordinary chat messages. The assistant message records the chosen action; the user message supplies tool data. It is not a new customer instruction or the provider-native tool role.</p><details><summary>Complete checked request</summary>' + _json(request) + '</details>'),
    }
    return frames


def skill_inspection(run, requests=()):
    """Distinguish installed files, observed reads, and observed request handoff."""
    events = run.get("events", [])
    reads = []
    for index, item in enumerate(events):
        if item.get("name") != "read_skill" or item.get("arguments", {}).get("name") != "verify-operation":
            continue
        result = item.get("result") or {}
        text = result.get("text")
        if not isinstance(text, str) or not text or item.get("error"):
            reads.append({"event": item, "read": False, "request": None, "following": []})
            continue
        matching = next((request for request in requests
                         if request.get("started_at", 0) >= item.get("ended_at", float("inf"))
                         and any(text in str(message.get("content", ""))
                                 or json.dumps(text)[1:-1] in str(message.get("content", ""))
                                 for message in request.get("request", {}).get("messages", []))), None)
        reads.append({"event": item, "read": True, "request": matching,
                      "following": [event.get("name", "unknown") for event in events[index + 1:]]})
    return reads


def skill_view(run, requests=()):
    reads = skill_inspection(run, requests)
    observed = [read for read in reads if read["read"]]
    content = '<p>Saving the skill makes its name available through <code>read_skill</code>. The model must request it before the text enters its context.</p>'
    if not observed:
        content += '<p class="pv-highlight"><strong>No successful verification-skill read is recorded in this run.</strong> The file exists, but these events do not establish that the model used its contents.</p>'
    for read in reads:
        item = read["event"]
        content += '<div class="pv-grid">' + _cell("1 · Read request", _json(item.get("arguments", {})) + '<p>Event: <code>' + _text(item.get("id", "unavailable")) + '</code></p>')
        content += _cell("2 · Returned skill", _json(item.get("result")))
        request = read["request"]
        detail = '<p>Saved model request <code>' + _text(request["id"]) + '</code> contains this returned text.</p>' if request else '<p>No matching saved next request was found. The skill read alone does not prove the handoff.</p>'
        content += _cell("3 · Next model input", detail) + '</div><p><strong>Subsequent tools:</strong> ' + _text(" → ".join(read["following"]) or "None recorded") + '</p>'
    content += '<p>Loading a skill shows access to its instructions. Compare later actions to determine whether the behavior changed.</p>'
    content += _link(run.get("trace", {}).get("url"), "Inspect this execution in Agent Lens")
    return _section(run.get("case_id", "Ticket") + " · was the skill read?", content)


def new_timeout_practice():
    """Create a separate public practice state; no saved experiment is touched."""
    case = next(case for case in CASES if case.id == "missing-seat")
    return {"world": copy.deepcopy(case.initial), "events": []}


PRACTICE_ACTIONS = {
    "commit": ("provision_member", {"account_id": "fern", "email": "alex@example.test", "role": "member", "operation_id": "join-alex"}),
    "inspect": ("onboarding_status", {"account_id": "fern"}),
    "same": ("provision_member", {"account_id": "fern", "email": "alex@example.test", "role": "member", "operation_id": "join-alex"}),
    "new": ("provision_member", {"account_id": "fern", "email": "alex@example.test", "role": "member", "operation_id": "join-alex-2"}),
}


def timeout_action(practice, action):
    if action not in PRACTICE_ACTIONS:
        raise ValueError("Choose a listed practice action")
    if not practice.get("events") and action != "commit":
        raise ValueError("Send the first request before trying a recovery action")
    name, arguments = PRACTICE_ACTIONS[action]
    world, result = execute(practice["world"], name, copy.deepcopy(arguments), fault="provision_timeout_after_commit")
    record = {"action": name, "arguments": copy.deepcopy(arguments), "result": result,
              "members": copy.deepcopy(world["accounts"]["fern"]["members"])}
    return {"world": world, "events": [*practice["events"], record]}


def timeout_view(practice):
    events = practice.get("events", [])
    if not events:
        return _section("Try the timeout without a model call", '<p>Predict what will happen if a write commits but its response is lost. Click <strong>Send the request and trigger a timeout</strong>, then choose how to recover.</p><p>Free local practice uses the same simulator. It does not run MCP, export a trace, or change your saved employee executions.</p>')
    item = events[-1]
    content = '<p class="pv-muted">Free local practice. This view reveals simulator state so you can check your prediction; the employee can only see tool responses.</p><div class="pv-grid">'
    content += _cell("What the caller received", _json({"tool": item["action"], "arguments": item["arguments"], "result": item["result"]}))
    content += _cell("What exists in the account", '<p><strong>' + str(len(item["members"])) + ' membership(s)</strong> for Fern</p>' + _json(item["members"])) + '</div>'
    if item["result"].get("error") == "timeout":
        content += '<p class="pv-highlight">The response timed out after the membership was saved. A red tool result does not establish that the write failed.</p>'
    elif item["result"].get("replayed"):
        content += '<p class="pv-highlight">The same operation ID and arguments returned the saved receipt. No second write occurred.</p>'
    elif len(item["members"]) > 1:
        content += '<p class="pv-highlight">A new operation ID created a second membership. The API accepted the operation; the task is now wrong.</p>'
    else:
        content += '<p class="pv-highlight">The status response shows that access already exists. The employee has evidence to stop writing and explain the result.</p>'
    return _section("Compare the response with the account", content)


def checks_view():
    rows = [
        ("Agent feedback", "check_work", "Current case state; matching refund or membership count", "The employee sees this tool result. A completion rule may require it."),
        ("Your development scorer", "my_state_check", "Saved account state; four free refund examples", "You implement and test this check. It does not define the final benchmark."),
        ("Independent final grader", "grade(case, run)", "All expected accounts and the required resolution", "Determines task success, including unrelated state and clarification."),
        ("Explanation judge", "judge_explanation", "Mission, recorded actions, reply and your rubric", "Returns grounded, complete and reason. It does not receive expected accounts."),
    ]
    body = '<div class="pv-table"><table><thead><tr><th>Check</th><th>Function</th><th>Reads</th><th>Use</th></tr></thead><tbody>'
    for row in rows:
        body += "<tr>" + "".join("<td>" + escape(value) + "</td>" for value in row) + "</tr>"
    body += '</tbody></table></div><p><code>my_judge_validation</code> checks response types and a nonempty reason. It does not decide whether the judge is correct. An unavailable judgment stays missing.</p>'
    return _section("Four checks, with different jobs", body)


def aligned_cases(runs_by_version):
    """Case identities from saved executions only, including partial comparisons."""
    return list(dict.fromkeys(run["case_id"] for runs in runs_by_version.values() for run in runs))


def _score(value):
    return "Unavailable" if value is None else "Pass" if value is True or value == 1 else "Fail"


def _accounts_summary(accounts):
    body = ""
    for identity, account in accounts.items():
        if identity == "other-account":
            continue
        refunds = account.get("refunds", [])
        members = account.get("members", [])
        body += '<p><strong>' + _text(identity) + '</strong><br>Refunds: '
        body += _text("; ".join(str(row.get("payment_id", "payment")) + ": $" + format(row.get("amount_cents", 0) / 100, ".2f") for row in refunds) or "none")
        body += '<br>Members: ' + _text("; ".join(str(row.get("email", "unknown")) + " (" + str(row.get("role", "unknown")) + ")" for row in members) or "none")
        body += '</p>'
    return body or "<p>No saved account state.</p>"


def comparison_view(runs_by_version, case_id):
    names = {"starting": "Starting instructions", "manual": "Your revision", "agent": "Agent-selected revision"}
    content = '<p>These columns show saved executions of the same fresh ticket. Selecting a ticket does not run it again.</p><div class="pv-grid">'
    for version, label in names.items():
        run = next((run for run in runs_by_version.get(version, []) if run.get("case_id") == case_id), None)
        if run is None:
            content += _cell(label, "<p>No saved execution for this case and version.</p>")
            continue
        judgment = run.get("explanation_judgment") or {}
        scores = run.get("scores") or {}
        body = '<p><strong>Task success:</strong> ' + _score(scores.get("task_success")) + '<br><strong>Explanation grounded:</strong> ' + _score(judgment.get("grounded")) + '<br><strong>Explanation complete:</strong> ' + _score(judgment.get("complete")) + '</p>'
        events = run.get("events", [])
        body += '<p><strong>Tool calls:</strong> ' + str(len(events)) + '<br>' + _text(" → ".join(e.get("name", "unknown") for e in events)) + '</p>'
        draft = run.get("draft") or {}
        body += '<p><strong>Employee explanation</strong><br>' + _text(draft.get("summary", "No saved explanation")) + '</p>'
        body += '<p><strong>Resolution:</strong> ' + _text(draft.get("resolution", "Unavailable")) + '</p>'
        body += '<details><summary>Read the judge’s reason</summary><p>' + _text(judgment.get("reason") or judgment.get("error") or "No saved judgment") + '</p></details>'
        accounts = run.get("world", {}).get("accounts", {})
        body += '<p><strong>Resulting account</strong></p>' + _accounts_summary(accounts)
        body += '<details><summary>Exact account state and harness version</summary>' + _json(accounts) + '<p><code>' + _text(run.get("harness_fingerprint", "Unavailable")) + '</code></p></details>'
        body += _link(run.get("trace", {}).get("url"), "Inspect this execution in Agent Lens")
        content += _cell(label, body)
    return _section(case_id + " · compare the same ticket", content + '</div><p>A changed sequence can still produce the same correct account. Compare the checks, explanation and work performed separately.</p>')
