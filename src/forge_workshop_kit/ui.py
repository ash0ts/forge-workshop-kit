"""Shared notebook views. These functions render receipts; they never execute a task."""
from __future__ import annotations

import difflib
import base64
import json
import textwrap
from functools import cache
from html import escape
from importlib.resources import files
from urllib.parse import quote, urlparse

from . import visuals
from .session import digest

STYLE = '''<style>
:root{--wk-ink:var(--text-primary,#163c43);--wk-muted:var(--text-secondary,#526b66);--wk-paper:var(--background,#fbfaf5);--wk-line:var(--border,#b7c7c0);--wk-accent:#237a6c;--wk-gold:#f1ca70}
.dark,.dark-theme,[data-theme="dark"]{--wk-ink:#e8efea;--wk-muted:#bbcec4;--wk-paper:#152a30;--wk-line:#5c766f;--wk-accent:#79cfb7}
.workshop-head,.workshop-step,.workshop-result,.workshop-context,.workshop-branch{color:var(--wk-ink);font-family:'IBM Plex Sans',system-ui,sans-serif;box-sizing:border-box}
.workshop-head{padding:28px 30px;background:#163c43;color:#f6f2e7;border-radius:10px;margin:12px 0 22px;border-top:5px solid #f1ca70}
.workshop-head h1{font-size:clamp(26px,3vw,38px);line-height:1.16;letter-spacing:-.7px;margin:10px 0}.workshop-head p{max-width:78ch;line-height:1.6;color:#d6e5da;margin-bottom:4px}
.workshop-head[data-theme="lab"]{display:flex;align-items:center;gap:24px}.workshop-head-copy{flex:1;min-width:0}.workshop-lab-art{width:210px;height:auto;flex:none;border-radius:6px}
.workshop-label{font:12px/1.4 'IBM Plex Mono',monospace;letter-spacing:.11em;text-transform:uppercase;color:#f1ca70}
.workshop-step{padding:20px 0 14px;border-bottom:1px solid var(--wk-line);margin:8px 0 16px}.workshop-step h2{font-size:25px;line-height:1.25;margin:0 0 12px}.workshop-step p{max-width:85ch;line-height:1.6;margin:8px 0}
.workshop-context{font-size:13px;display:flex;gap:12px 24px;flex-wrap:wrap;padding:12px 0;margin:0 0 12px;border-bottom:1px solid var(--wk-line);color:var(--wk-muted)}
.workshop-result{border-left:4px solid var(--wk-accent);padding:16px 20px;margin:14px 0;background:var(--wk-paper);border-radius:0 8px 8px 0}.workshop-result[data-status="unavailable"],.workshop-result[data-status="failed"]{border-left-color:#bf7551}.workshop-result h3{margin:0 0 12px;font-size:19px}.workshop-result dl{display:grid;grid-template-columns:minmax(120px,1fr) 3fr;gap:8px 18px;margin:0}.workshop-result dt{color:var(--wk-muted)}.workshop-result dd{margin:0;overflow-wrap:anywhere}.workshop-result pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:350px;overflow:auto;font-size:12px}
.workshop-evidence{display:flex;flex-wrap:wrap;gap:9px;margin:12px 0}.workshop-evidence a{border:1px solid var(--wk-line);padding:9px 13px;border-radius:6px;color:var(--wk-accent);font-size:14px;line-height:1.4;text-decoration:none}.workshop-evidence a:hover{border-color:var(--wk-accent);text-decoration:underline}
.workshop-evidence a:focus-visible,.workshop-branch a:focus-visible,.workshop-branch summary:focus-visible{outline:3px solid #b88a28;outline-offset:3px}
.workshop-diff{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.65 'IBM Plex Mono',monospace;border:1px solid var(--wk-line);border-radius:6px;padding:12px;max-height:420px;overflow:auto;color:var(--wk-ink)}.workshop-diff .add{background:#237a6c20;display:block}.workshop-diff .del{background:#c17b4025;display:block}
.workshop-branch{margin:16px 0;border:1px solid var(--wk-line);border-radius:8px;padding:18px;scroll-margin-top:20px}.workshop-branch:target{outline:3px solid #c99e39}.workshop-branch h3{font-size:19px;margin:0 0 8px}.workshop-branch p{line-height:1.55}.workshop-branch summary{cursor:pointer;font-size:15px}.workshop-branch svg{width:100%;display:block}.workshop-branch code{overflow-wrap:anywhere}.workshop-branch dl{margin:12px 0}.workshop-branch dt{font-size:12px;color:var(--wk-muted)}.workshop-branch dd{margin:0 0 10px;overflow-wrap:anywhere}
.workshop-workbench{color:var(--wk-ink);font-family:'IBM Plex Sans',system-ui,sans-serif;min-width:0;margin:18px 0}.workshop-workbench fieldset{border:1px solid var(--wk-line);border-radius:9px;padding:16px;min-width:0}.workshop-workbench legend{font-weight:600;font-size:20px;padding:0 8px}.workshop-workbench .wk-grid{display:grid;grid-template-columns:minmax(220px,30%) minmax(0,1fr);gap:20px;align-items:start}.workshop-workbench .wk-options{display:grid;gap:7px;max-height:650px;overflow:auto;padding:4px}.workshop-workbench .wk-choice{display:block;border:1px solid var(--wk-line);border-left:5px solid var(--wk-role);padding:9px 11px;border-radius:5px;cursor:pointer;line-height:1.35;background:var(--wk-paper)}.workshop-workbench .wk-choice strong{display:block;font-size:14px;overflow-wrap:anywhere}.workshop-workbench .wk-choice small{display:block;color:var(--wk-muted);font-size:12px;margin:4px 0}.workshop-workbench .wk-radio{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}.workshop-workbench .wk-panel{display:none;min-width:0;border-left:4px solid var(--wk-role);padding-left:18px}.workshop-workbench .wk-panel h3{font-size:22px;line-height:1.3;margin:0 0 10px}.workshop-workbench .wk-panel h4{font-size:16px;margin:18px 0 8px}.workshop-workbench .wk-panel p{line-height:1.6}.workshop-workbench .wk-panel code{overflow-wrap:anywhere}.workshop-workbench details{margin:12px 0}.workshop-workbench summary{cursor:pointer;line-height:1.5}.workshop-workbench .wk-status{font-size:13px;color:var(--wk-muted)}.workshop-workbench .wk-round{font-size:14px;margin:12px 0 3px}.workshop-workbench .wk-role{font-size:12px;text-transform:uppercase;letter-spacing:.05em}.workshop-workbench .wk-warning{border-left:3px solid #c17b40;padding:10px;background:#c17b4015}.workshop-workbench .workshop-result{padding:12px;margin:12px 0}.workshop-workbench .wk-legend{font-size:13px;color:var(--wk-muted);line-height:1.6}.workshop-workbench .wk-neighbors{display:flex;gap:12px;margin-top:20px;flex-wrap:wrap}.workshop-workbench .wk-neighbors label{cursor:pointer;text-decoration:underline;font-size:14px}.workshop-workbench :is(a,summary):focus-visible{outline:3px solid #b88a28;outline-offset:3px}
@media(max-width:760px){.workshop-workbench .wk-grid{grid-template-columns:1fr}.workshop-workbench .wk-options{max-height:230px;grid-template-columns:repeat(2,minmax(0,1fr))}.workshop-workbench .wk-round{grid-column:1/-1}.workshop-workbench .wk-panel{padding-left:12px}.workshop-workbench fieldset{padding:12px}.workshop-workbench .wk-choice strong{font-size:13px}}
@media(max-width:650px){.workshop-head{padding:20px}.workshop-head[data-theme="lab"]{flex-direction:column;align-items:flex-start;gap:12px}.workshop-lab-art{width:150px}.workshop-result dl{grid-template-columns:1fr}.workshop-result dd{margin-bottom:8px}.workshop-evidence a{width:100%}}
@media(prefers-reduced-motion:reduce){.workshop-branch{scroll-behavior:auto}}
</style>'''


@cache
def _fonts():
    rules = []
    for family, weight in [('sans', 400), ('sans', 600), ('mono', 400)]:
        asset = files('forge_workshop_kit').joinpath('assets', 'fonts',
            f'ibm-plex-{family}-latin-{weight}-normal.woff2')
        encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
        rules.append(f"@font-face{{font-family:'IBM Plex {family.title()}';font-style:normal;"
                     f"font-weight:{weight};font-display:swap;src:url(data:font/woff2;base64,{encoded}) format('woff2')}}")
    return '<style>' + ''.join(rules) + '</style>'


def heading(title, description, *, theme='office', eyebrow=None):
    labels = {'neutral': 'Forge workshop', 'office': 'Pending, Inc. · Forge workshop',
              'lab': 'Solar Forecasting Lab · Forge workshop',
              'routing': 'Customer support · Forge workshop',
              'inspection': 'PCB inspection · Forge workshop'}
    if theme not in labels:
        raise ValueError('Unknown workshop theme.')
    content = (f'<div class="workshop-label">{escape(eyebrow or labels[theme])}</div>'
               f'<h1>{escape(title)}</h1><p>{escape(description)}</p>')
    if theme == 'lab':
        asset = files('forge_workshop_kit').joinpath('assets', 'solar-lab.svg')
        encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
        content = (f'<div class="workshop-head-copy">{content}</div>'
                   f'<img class="workshop-lab-art" src="data:image/svg+xml;base64,{encoded}"'
                   ' alt="Pixel research workstation with solar imagery, experiment plots, and a notebook"'
                   ' width="680" height="450">')
    return _fonts() + STYLE + f'<header class="workshop-head" data-theme="{theme}">{content}</header>'


def step(title, task, expected):
    return f'<section class="workshop-step"><h2>{escape(title)}</h2><p>{escape(task)}</p><p><strong>Before you continue:</strong> {escape(expected)}</p></section>'


def links(values):
    return '<nav class="workshop-evidence" aria-label="Evidence links">' + ''.join(
        f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(str(label))} ↗</a>'
        for label, url in values.items()
        if isinstance(url, str) and urlparse(url).scheme == 'https' and urlparse(url).netloc
    ) + '</nav>'


def navigation(mo, steps, current, on_select, completed=(), *, label='Your workday'):
    completed = set(completed)
    buttons = {}
    for index, (key, step_label) in enumerate(steps, 1):
        marker = '✓ ' if key in completed else ''
        buttons[f'step{index}'] = mo.ui.button(
            label=f'{marker}{index} · {step_label}',
            on_click=lambda _, target=key: on_select(target),
            kind='success' if key == current else 'neutral',
            tooltip='Current step' if key == current else 'Open this step; no work will run',
        )
    # The caller binds this composite to a notebook global so callbacks stay active.
    template = f'<p><strong>{escape(label)}</strong> · Choose a step to open it. Use its run button when you’re ready.</p>'
    template += '<div style="display:flex;flex-wrap:wrap;gap:8px">' + ''.join(
        '{' + name + '}' for name in buttons) + '</div>'
    return mo.Html(template).batch(**buttons)


def next_step(mo, label, target, on_select):
    label = label.removeprefix('Next: ')
    return mo.ui.button(label=f'Continue: {label} →', kind='success',
                        on_click=lambda _: on_select(target), full_width=True)


def prerequisite(mo, message, target, on_select):
    return mo.Html('<aside style="border-left:3px solid #b88a28;padding:12px">'
                   + escape(message) + '<br>{go}</aside>').batch(
        go=mo.ui.button(label='Go to the required step →', on_click=lambda _: on_select(target)))


def _display(value):
    if value is None:
        return 'Unavailable'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if isinstance(value, float):
        return f'{value:.6g}'
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def result(title, fields, status='complete', detail=None):
    rows = ''.join(f'<dt>{escape(str(k))}</dt><dd>{escape(_display(v))}</dd>' for k, v in fields.items())
    more = '' if detail is None else '<details><summary>Execution details</summary><pre>' + escape(json.dumps(detail, indent=2, default=str)) + '</pre></details>'
    return f'<section class="workshop-result" data-status="{escape(status, quote=True)}" aria-label="{escape(title, quote=True)}"><h3>{escape(title)}</h3><dl>{rows}</dl>{more}</section>'


def context(session):
    if session is None:
        return ''
    state = session.read()
    requests = state.get('requests', {}).values()
    observed = sum(float(r.get('observed_usd') or 0) for r in requests)
    unknown = sum(float(r.get('unknown_usd') or 0) for r in requests)
    return '<div class="workshop-context">' + ''.join(f'<span>{escape(v)}</span>' for v in (
        f'Project: {session.project}', 'Tools and training: this notebook runtime',
        f'Inference allowance: ${session.budget_usd:.2f}',
        f'Measured inference: ${observed:.4f} · bounded unknown: ${unknown:.4f}',
        'Notebook compute is billed separately',
    )) + '</div>'


def diff(before, after):
    content = list(difflib.unified_diff(before.splitlines(), after.splitlines(),
                                      fromfile='previous', tofile='proposed', lineterm=''))
    if not content:
        return '<p><strong>Retain this version.</strong> The executable files are unchanged.</p>'
    lines = []
    for line in content:
        kind = 'add' if line.startswith('+') and not line.startswith('+++') else 'del' if line.startswith('-') and not line.startswith('---') else ''
        lines.append(f'<span class="{kind}">{escape(line)}</span>')
    return '<pre class="workshop-diff">' + '\n'.join(lines) + '</pre>'


def stage_links(session, stage_ids=()):
    state = session.read()
    found = {}
    for identity in stage_ids:
        record = state['stages'].get(identity, {})
        label = record.get('name', 'Execution').replace('/', ' / ').replace('-', ' ')
        trace = state['publications'].get('trace/' + identity, record.get('result', {}).get('trace', {}))
        if trace.get('url'):
            found[f'{label} · Agent Lens' + ('' if trace.get('verified') else ' · upload not yet verified')] = trace['url']
        if record.get('published'):
            found[f'{label} · run'] = record['published']
        if record.get('artifact_url'):
            found[f'{label} · files'] = record['artifact_url']
    return found


def span_links(session, identity):
    state = session.read()
    row = state['stages'].get(identity, {})
    trace = state['publications'].get('trace/' + identity, {})
    if not trace.get('verified') or not trace.get('url') or not trace.get('trace_id'):
        return {}
    found = {}
    for index, event in enumerate(row.get('result', {}).get('events', []), 1):
        span = trace.get('span_ids', {}).get(event.get('id'))
        if span:
            found[f"{index} · {event['name']}" + (' · error' if event.get('error') else '')] = (
                trace['url'] + '/spans/turns/' + trace['trace_id'] + '/spans/' + span)
    return found


def evidence(mo, session, stage_ids=(), question='', extra=None):
    values = stage_links(session, stage_ids) if session else {}
    values.update(extra or {})
    elements = [mo.md('**Inspect in Forge**')]
    if question:
        elements.append(mo.md(question))
    if len(values) > 9:
        elements.append(mo.accordion({f'Open all {len(values)} runs and saved files': mo.Html(links(values))}))
    else:
        elements.append(mo.Html(links(values)) if values else mo.md('Links to this run and its files will appear here after upload.'))
    if session:
        state = session.read()
        exact = {}
        for identity in stage_ids:
            name = state['stages'].get(identity, {}).get('name', identity)
            exact.update({name + ' / ' + label: url for label, url in span_links(session, identity).items()})
            receipt = state['publications'].get('trace/' + identity, {})
            if receipt.get('status') == 'unavailable' or receipt.get('error'):
                elements.append(mo.callout(mo.md('The execution is saved. Trace publication needs a retry: '
                                               + str(receipt.get('error', 'the uploaded trace has not yet been verified'))), kind='warn'))
        if exact:
            elements.append(mo.accordion({'Open a specific recorded tool span': mo.Html(links(exact))}))
    return mo.vstack(elements)


def _weave_url(reference):
    if not isinstance(reference, str) or not reference.startswith('weave:///'):
        return None
    parts = reference.removeprefix('weave:///').split('/')
    if len(parts) != 4 or parts[2] != 'object' or ':' not in parts[3]:
        return None
    name, version = parts[3].rsplit(':', 1)
    return 'https://wandb.ai/' + '/'.join(quote(p, safe='') for p in parts[:2]) + '/weave/objects/' + quote(name, safe='') + '/versions/' + quote(version, safe='')


def _comparison_label(record, ordinal):
    """Name a saved comparison from its published object, including legacy receipts."""
    for label, version in record.items():
        if version.get('comparison_name'):
            name = version['comparison_name']
            return {'solar-images-final': 'Solar images · final',
                    'solar-measurements-final': 'GOES measurements · final',
                    'pending-final': 'Office cases · final'}.get(name, name.replace('-', ' ').capitalize())
        for field, suffix in (('evaluation', 'evaluation'), ('dataset', 'cases')):
            reference = version.get(field, '')
            if not isinstance(reference, str) or not reference.startswith('weave:///'):
                continue
            parts = reference.removeprefix('weave:///').split('/')
            if len(parts) != 4 or parts[2] != 'object':
                continue
            name = parts[3].rsplit(':', 1)[0]
            ending = f'-{label}-{suffix}'
            if name.endswith(ending):
                name = name[:-len(ending)]
                return {'solar-images-final': 'Solar images · final',
                        'solar-measurements-final': 'GOES measurements · final',
                        'pending-final': 'Office cases · final'}.get(
                            name, name.replace('-', ' ').capitalize())
    return f'Saved comparison {ordinal}'


def comparison_links(receipt, *, suffix=''):
    """Name image and measurement comparisons separately, including persistence."""
    found = {}
    for label, row in receipt.items():
        if not isinstance(row, dict):
            continue
        prefix = _comparison_label(receipt, suffix or 1) + " / " + label
        if suffix:
            prefix += ' · ' + suffix
        if row.get('run'):
            found[prefix + ' · run'] = row['run']
        for key, title in (('dataset', 'cases'), ('evaluation', 'Weave evaluation')):
            url = _weave_url(row.get(key, ''))
            if url:
                found[prefix + ' · ' + title] = url
    return found


def publication(mo, session):
    rows = []
    destinations = {}
    errors = []
    comparison_names = {}
    comparison_number = 0
    if session is None:
        return mo.md('Connect to your project to publish evidence.')
    for key, record in session.read()['publications'].items():
        if key.startswith('comparison/'):
            comparison_number += 1
            comparison = _comparison_label(record, comparison_number)
            comparison_names[comparison] = comparison_names.get(comparison, 0) + 1
            if comparison_names[comparison] > 1:
                comparison += f' · saved set {comparison_names[comparison]}'
            for label, version in record.items():
                destination_label = comparison + ' / ' + label
                rows.append({'Comparison': comparison, 'Version': label, 'Weave': version.get('weave_status', 'not published'),
                             'Native EvalTables': version.get('native_status', 'not published'),
                             'Result run': version.get('run', '')})
                if version.get('run'):
                    destinations[destination_label + ' · comparison run'] = version['run']
                for field in ('evaluation', 'dataset'):
                    url = _weave_url(version.get(field))
                    if url:
                        destinations[destination_label + ' · Weave ' + field] = url
                for field in ('weave_error', 'native_error'):
                    if version.get(field):
                        errors.append(destination_label + ': ' + version[field])
    if not rows:
        return mo.md('Comparisons have not been published yet. Saved executions remain available locally.')
    partial = any(r['Native EvalTables'] != 'published' or r['Weave'] != 'published' for r in rows)
    elements = [mo.md('**Publication status**'), mo.Html(links(destinations)),
                mo.ui.table(rows, selection=None, show_column_summaries=False)]
    if partial:
        elements.append(mo.callout(mo.md('Some comparisons could not be uploaded. You can still use the notebook results and the links above. Retry the upload from saved work without running the experiment again.'), kind='warn'))
        if errors:
            elements.append(mo.accordion({'Publication error details': mo.md('\n\n'.join(errors))}))
    return mo.vstack(elements)


def _source(value):
    if isinstance(value.get('source'), str):
        return value['source']
    if isinstance(value.get('harness'), dict):
        return '\n\n'.join(f'{k}\n{v}' for k, v in value['harness'].items())
    return ''


def _retained_selection(row, rows):
    saved = row.get('result', {})
    if saved.get('retained_parent'):
        return True
    if not row['name'].endswith('/adopted'):
        return False
    prefix = row['name'].rsplit('/', 1)[0]
    compositions = [r for r in rows if r['name'] == prefix + '/compose' and r['status'] == 'complete']
    for composition in reversed(compositions):
        decision = composition['result']
        if isinstance(decision.get('decision'), dict):
            decision = decision['decision']
        if (decision.get('decision') == 'KEEP' and decision.get('fingerprint')
                and saved.get('fingerprint') == decision['fingerprint']):
            return True
    return False


def _branch_detail(session, row):
    saved = row.get('result', {})
    decision = saved.get('decision', saved)
    decision = decision if isinstance(decision, dict) else saved
    title = decision.get('title') or row['name'].split('/')[-1].replace('-', ' ')
    if decision.get('decision') == 'KEEP' or _retained_selection(row, session.read()['stages'].values()):
        title = 'Retain this version · ' + title
    content = [f'<article class="workshop-branch" id="branch-{escape(row["id"])}"><h3>{escape(title)}</h3>',
               f'<p>{escape(row["name"])} · {escape(row["status"])}</p>']
    if decision.get('rationale'):
        content.append('<p><strong>The agent’s rationale:</strong> ' + escape(decision['rationale']) + '</p>')
    for candidate in saved.get('candidates', []):
        content.append('<h4>' + escape(candidate.get('title', 'Proposed change')) + '</h4>')
        content.append('<p>' + escape(candidate.get('rationale', 'No rationale recorded.')) + '</p>')
        change = candidate.get('diff')
        if change:
            content.append('<pre class="workshop-diff">' + escape(change) + '</pre>')
        elif candidate.get('decision') == 'KEEP':
            content.append('<p>Retain this version. The code is unchanged.</p>')
    if decision.get('diff'):
        content.append('<pre class="workshop-diff">' + escape(decision['diff']) + '</pre>')
    execution = saved.get('run', saved.get('adopted', saved))
    execution_id = saved.get('execution')
    if isinstance(execution_id, str):
        executed_row = session.read()['stages'].get(execution_id, {})
        execution = {**executed_row.get('result', {}), 'stage_id': execution_id}
    if isinstance(execution, dict):
        metrics = execution.get('metrics', execution.get('scores', {}))
        if metrics:
            content.append(result('Observed result', metrics))
        executed = (execution.get('harness_fingerprint') or execution.get('fingerprint')
                    or execution.get('source_fingerprint'))
        if not executed and execution.get('stage_id'):
            executed = session.read()['stages'].get(execution['stage_id'], {}).get('source_fingerprint')
        if executed:
            content.append('<p>Executed version: <code>' + escape(executed) + '</code></p>')
    labels = {'lesson': 'Agent’s proposed lesson', 'limits': 'Stated limits',
              'error': 'Error', 'execution_error': 'Execution error'}
    for key, label in labels.items():
        value = saved.get(key) or decision.get(key)
        if value:
            content.append('<p><strong>' + label + ':</strong> ' + escape(_display(value)) + '</p>')
    content.append('<details><summary>Code and version details</summary><p>Source fingerprint: <code>' + escape(row.get('source_fingerprint', 'unavailable')) + '</code></p>')
    sources = row.get('sources', {})
    for name, source in sources.items():
        content.append('<p>' + escape(name) + '</p><pre class="workshop-diff">' + escape(str(source)) + '</pre>')
    content.append('</details>')
    ids = [row['id']]
    if isinstance(execution, dict) and execution.get('stage_id'):
        ids.append(execution['stage_id'])
    content.append(links(stage_links(session, ids)))
    exact = {}
    for identity in ids:
        exact.update(span_links(session, identity))
    if exact:
        content.append('<details><summary>Supporting tool spans</summary>' + links(exact) + '</details>')
    content.append('</article>')
    return ''.join(content)


def branches(session):
    rows = [r for r in session.read()['stages'].values() if '/round-' in r['name']]
    rows.sort(key=lambda row: row.get('started_at', 0))
    return ''.join(_branch_detail(session, row) for row in rows) or '<p>The branches will appear here after the agent proposes changes and you test them.</p>'


def _branch_status(node):
    labels = {'not_run': 'Not run', 'proposed': 'Proposed · not an execution',
              'complete': 'Completed', 'failed': 'Failed', 'running': 'Interrupted or in progress',
              'unavailable': 'Unavailable'}
    text = labels.get(node['status'], node['status'].replace('_', ' ').capitalize())
    if node['selected']:
        text = 'Selected · retained files' if node['retained'] else 'Selected version saved'
    elif node['execution']:
        execution = node['execution']
        text = 'Execution: ' + labels.get(execution['status'], execution['status'])
        agent_status = execution['result'].get('status')
        if agent_status and agent_status != 'complete':
            text += ' · agent: ' + str(agent_status)
    return text


def _branch_quote(label, value):
    text = str(value)
    if len(text) <= 280:
        return '<p><strong>' + label + ':</strong> ' + escape(text) + '</p>'
    excerpt = text[:260].rsplit(' ', 1)[0] + '…'
    return ('<p><strong>' + label + ':</strong> ' + escape(excerpt) + '</p>'
            + '<details><summary>Read the full saved explanation</summary><p>'
            + escape(text) + '</p></details>')


def _branch_panel(session, node):
    decision, saved = node['decision'], node['result']
    content = [f'<div class="wk-role">Round {node["round"]} · '
               + escape(node['key'].replace('-', ' ')) + '</div>',
               '<h3>' + escape(node['title']) + '</h3>',
               '<p class="wk-status">' + escape(_branch_status(node)) + '</p>']
    if node['status'] == 'not_run':
        content.append('<p>This step has no saved result yet. Use the exercise’s run control to do the work; choosing a branch here only changes what you see.</p>')
        return ''.join(content)
    rationale = decision.get('rationale')
    if rationale and not node['selected']:
        content.append(_branch_quote('The agent’s reason for this change', rationale))
    if node['key'] == 'proposal':
        content.append('<p>The agent returned two proposals. Open Candidate A and Candidate B to compare their intended changes, then open each test to see what executed.</p>')
    if node['selected']:
        if node['retained']:
            content.append('<p><strong>Retain this version.</strong> The saved selection keeps the previous files. This decision is separate from any test execution.</p>')
        else:
            content.append('<p>The saved decision selects these files for the next task. It does not establish a quality gain by itself.</p>')
        if saved.get('failure_fallback'):
            content.append('<p class="wk-warning">The composed run did not complete. The selection falls back to the previous valid harness.</p>')
        recommendation = node.get('composition_recommendation', {})
        if recommendation.get('rationale'):
            content.append(_branch_quote('The agent’s composition recommendation', recommendation['rationale']))
    elif decision.get('decision') == 'KEEP':
        content.append('<p><strong>Retain this version.</strong> The proposal keeps the executable files unchanged. A later test is still a separate execution.</p>')
    content.append('<h4>Inspect in Forge</h4>')
    evidence_links = stage_links(session, node['record_ids'])
    content.append(links(evidence_links) if evidence_links else
                   '<p>No Forge link is saved for this step. The local decision and files remain available below.</p>')
    if node['diff']:
        content.append('<h4>What changed</h4><pre class="workshop-diff">' + escape(str(node['diff'])) + '</pre>')
    elif node['files'] and decision.get('decision') != 'KEEP' and not node['selected']:
        content.append('<p>The saved files are available below. A before/after diff was not recorded.</p>')
    execution = node['execution']
    if execution:
        if node.get('selection_execution_mismatch'):
            content.append('<p class="wk-warning">The attempted execution used different files from the selected version. Its result is shown as the attempted test, not as a test of the selected files.</p>')
        elif node['fingerprint_match'] is False:
            content.append('<p class="wk-warning">The executed fingerprint does not match this proposal. Do not attribute its result to the proposed edit.</p>')
        elif node['fingerprint_match'] is True:
            content.append('<p>The executed files match this version.</p>')
        if execution['metrics']:
            metric_labels = {'task_success': 'Task completed correctly',
                'state_correct': 'Account state correct', 'completion_correct': 'Resolution correct',
                'reason': 'State check', 'expected_resolution': 'Expected resolution',
                'validation_error': 'Validation error', 'error': 'Mean absolute error',
                'persistence_error': 'Persistence error', 'seconds': 'Execution seconds',
                'skill_vs_persistence': 'Improvement over persistence (fraction)',
                'examples': 'Examples', 'learner_metric': 'Learner scorer error',
                'learner_metric_matches': 'Learner scorer agrees'}
            metrics = {metric_labels.get(k, k.replace('_', ' ').capitalize()): v
                       for k, v in execution['metrics'].items()}
            content.append(result('Observed execution result', metrics,
                                  status=execution['status']))
        else:
            content.append('<p>No score is saved for this execution.</p>')
        if execution['result'].get('errors'):
            content.append('<p class="wk-warning">' + escape(_display(execution['result']['errors'])) + '</p>')
        if execution['record'].get('error'):
            content.append('<p class="wk-warning">' + escape(_display(execution['record']['error'])) + '</p>')
    for key, label in [('lesson', 'Agent’s proposed lesson'), ('limits', 'Stated limits'),
                       ('error', 'Error'), ('execution_error', 'Execution error')]:
        value = saved.get(key) or decision.get(key)
        if value:
            content.append(_branch_quote(label, _display(value)))
    exact = {}
    for identity in node['record_ids']:
        exact.update(span_links(session, identity))
    if exact:
        content.append('<details><summary>Open a recorded tool or model span</summary>' + links(exact) + '</details>')
    content.append('<details><summary>Files, fingerprints, and saved attempts</summary>')
    if node['fingerprint']:
        content.append('<p>Version fingerprint: <code>' + escape(node['fingerprint']) + '</code></p>')
    if execution and execution['fingerprint']:
        content.append('<p>Executed fingerprint: <code>' + escape(execution['fingerprint']) + '</code></p>')
    for name, source in (node['files'] or node['sources']).items():
        content.append('<h4>' + escape(name) + '</h4><pre class="workshop-diff">' + escape(str(source)) + '</pre>')
    for attempt in node['attempts']:
        content.append('<p><code>' + escape(attempt['id']) + '</code> · '
                       + escape(attempt['status']) + '</p>')
        if attempt.get('error'):
            content.append('<pre class="workshop-diff">' + escape(str(attempt['error'])) + '</pre>')
    content.append('</details>')
    return ''.join(content)


def branch_workbench_html(session, *, key='improvement'):
    """HTML-only branch selection: no callback can rerun an exercise or write a receipt."""
    groups = visuals.branch_records(session.read())
    nodes = [node for group in groups for node in group['nodes']]
    if not nodes:
        return STYLE + '<section class="workshop-workbench"><h3>Your improvement history</h3><p>Run the first proposal to create two branches. Their files, tests, and selection will appear here.</p></section>'
    vocabulary = visuals.contract()
    namespace = 'wk-' + digest([key, session.project, session.workspace_id])[:14]
    default = next((index for index, node in enumerate(nodes) if node['status'] != 'not_run'), 0)
    selectors, inputs, choices, panels = [], [], [], []
    last_round = None
    for index, node in enumerate(nodes):
        identity = namespace + '-' + str(index)
        color = vocabulary['colors'][node['role']]
        selectors.append(f'#{identity}:checked~.wk-grid .wk-panel[data-choice="{index}"]{{display:block}}')
        selectors.append(f'#{identity}:checked~.wk-grid label[for="{identity}"]{{outline:2px solid var(--wk-accent);outline-offset:1px;font-weight:600}}')
        selectors.append(f'#{identity}:focus-visible~.wk-grid label[for="{identity}"]{{outline:3px solid #b88a28;outline-offset:2px}}')
        accessible = f'Round {node["round"]}, {node["key"].replace("-", " ")}: {node["title"]}. {_branch_status(node)}'
        inputs.append(f'<input class="wk-radio" type="radio" name="{namespace}" id="{identity}"'
                      f' aria-label="{escape(accessible, quote=True)}" aria-controls="{identity}-panel"'
                      + (' checked' if index == default else '') + '>')
        if node['id'].rsplit('/', 1)[0] != last_round:
            last_round = node['id'].rsplit('/', 1)[0]
            choices.append(f'<h3 class="wk-round">Round {node["round"]}</h3>')
        choices.append(f'<label class="wk-choice" for="{identity}" style="--wk-role:{color}">'
                       f'<small>{escape(node["key"].replace("-", " "))}</small><strong>{escape(node["title"])}</strong>'
                       f'<small>{escape(_branch_status(node))}</small></label>')
        neighbors = []
        for offset, label in [(-1, '← Previous step'), (1, 'Next step →')]:
            target = index + offset
            if 0 <= target < len(nodes):
                neighbors.append(f'<label for="{namespace}-{target}">{label}</label>')
        relations = []
        names = {n['id']: n['title'] for n in nodes}
        for group in groups:
            for edge in group['edges']:
                if node['id'] in (edge['from'], edge['to']):
                    relations.append('<li>' + escape(names[edge['from']]) + ' → '
                                     + escape(names[edge['to']]) + ': '
                                     + escape(vocabulary['edges'][edge['kind']]['label']) + '.</li>')
        relationships = ('<details><summary>Recorded connections</summary><ul>'
                         + ''.join(relations) + '</ul></details>') if relations else ''
        panels.append(f'<article class="wk-panel" data-choice="{index}" id="{identity}-panel"'
                      f' aria-label="{escape(node["title"], quote=True)}" style="--wk-role:{color}">'
                      + _branch_panel(session, node) + relationships + '<nav class="wk-neighbors" aria-label="Explore steps">'
                      + ''.join(neighbors) + '</nav></article>')
    other = [r for group in groups for r in group['other_records']]
    extra = ('<details><summary>Reviews and other saved events</summary>'
             + ''.join(_branch_detail(session, row) for row in other) + '</details>') if other else ''
    return (STYLE + '<style>' + ''.join(selectors) + '</style>'
            + '<section class="workshop-workbench"><fieldset><legend>Your improvement history</legend>'
            + '<p>Choose a step to read its files, result, and Forge links. Use the arrow keys within the choices to move between steps. No work runs when you select a step.</p>'
            + '<p class="wk-legend">Gray: starting version · blue: A · orange: B · neutral: composition. '
            + 'A saved selection is labeled explicitly. Color does not represent quality.</p>'
            + ''.join(inputs) + '<div class="wk-grid"><div class="wk-options" aria-label="Saved steps">'
            + ''.join(choices) + '</div><div>' + ''.join(panels) + '</div></div></fieldset>' + extra + '</section>')


def branch_workbench(mo, session, *, key='improvement'):
    return mo.Html(branch_workbench_html(session, key=key))










def branch_graph(session):
    """Static compatibility view using the same saved relationships as the workbench."""
    groups = visuals.branch_records(session.read())
    colors = visuals.contract()['colors']
    diagrams = []
    for group in groups:
        positions = {'parent': (85, 90), 'proposal': (85, 230),
                     'candidate-a': (300, 90), 'probe-a': (510, 90),
                     'candidate-b': (300, 230), 'probe-b': (510, 230),
                     'compose': (725, 160), 'composition-test': (930, 160),
                     'selection': (930, 335), 'reflection': (725, 335)}
        by_id = {node['id']: node for node in group['nodes']}
        marker = 'arrow-' + digest(group['id'])[:10]
        svg = [f'<section class="workshop-branch"><h3>Round {group["round"]}</h3>',
               '<svg viewBox="0 0 1060 415" role="img" aria-label="Saved proposal, execution, evidence, and selection relationships">',
               '<title>Saved improvement branches</title><desc>Blue identifies candidate A and orange candidate B. Solid arrows pass files to an execution. Dashed arrows mean the composition reviewed an execution. Selection is labeled separately. Missing work has no invented connection.</desc>',
               f'<defs><marker id="{marker}" markerWidth="7" markerHeight="7" refX="7" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="var(--wk-muted)"/></marker></defs>']
        for edge in group['edges']:
            a, b = by_id[edge['from']], by_id[edge['to']]
            x1, y1 = positions[a['key']]; x2, y2 = positions[b['key']]
            dashed = ' stroke-dasharray="6 5"' if edge['kind'] == 'evidence' else ''
            svg.append(f'<path d="M{x1},{y1} C{(x1+x2)/2},{y1} {(x1+x2)/2},{y2} {x2},{y2}" fill="none" stroke="var(--wk-muted)" stroke-width="2" marker-end="url(#{marker})"{dashed}><title>{escape(visuals.contract()["edges"][edge["kind"]]["label"])}</title></path>')
        for node in group['nodes']:
            x, y = positions[node['key']]
            if node['record_id']:
                svg.append(f'<a href="#branch-{escape(node["record_id"])}" aria-label="{escape(node["title"], quote=True)}">')
            svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{colors[node["role"]]}"/>')
            label = node['title']
            lines = textwrap.wrap(label, 24)
            if len(lines) > 3:
                lines = lines[:3]; lines[-1] = lines[-1].rstrip('., ') + '…'
            svg.append(f'<text x="{x}" y="{y+24}" text-anchor="middle" fill="var(--wk-ink)" style="font-size:13px">')
            for index, line in enumerate(lines):
                svg.append(f'<tspan x="{x}" dy="{0 if index == 0 else 16}">{escape(line)}</tspan>')
            svg.append(f'</text><text x="{x}" y="{y-17}" text-anchor="middle" fill="var(--wk-muted)" style="font-size:11px">{escape(_branch_status(node))}</text>')
            if node['record_id']:
                svg.append('</a>')
        svg.append('</svg><p>Solid: files passed to an execution. Dashed: execution evidence reviewed. Selection is explicit; color does not represent quality.</p></section>')
        diagrams.append(''.join(svg))
    return STYLE + ''.join(diagrams) + branches(session)
