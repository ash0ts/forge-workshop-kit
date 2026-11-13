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


def heading(title, description, *, theme='office'):
    labels = {'neutral': 'Forge workshop', 'office': 'Pending, Inc. · Forge workshop',
              'lab': 'Solar Forecasting Lab · Forge workshop'}
    if theme not in labels:
        raise ValueError('Workshop theme must be neutral, office, or lab.')
    content = (f'<div class="workshop-label">{labels[theme]}</div>'
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


def branch_graph(session):
    """Two explicit proposal branches. Edges show workflow, not code adoption."""
    rows = list(session.read()['stages'].values())
    rows.sort(key=lambda row: row.get('started_at', 0))
    svg = ['<section class="workshop-branch"><p><strong>Improvement history</strong> · Select a step to see the proposed edit, its test result, and the agent’s explanation. The last step in each round shows which version was kept.</p><svg viewBox="0 0 1020 670" role="img" aria-label="Two rounds with separate candidate A and B probes, composition, test, and selection">']
    for number in (1, 2):
        group = [r for r in rows if f'/round-{number}/' in r['name']]
        def find(*suffixes):
            return next((r for r in reversed(group) if any(r['name'].endswith('/' + suffix) for suffix in suffixes)), None)
        proposal = find('propose')
        candidates = (proposal or {}).get('result', {}).get('candidates', [])
        adopt = find('adopt', 'adopted')
        y = 55 + (number-1)*325
        svg.append(f'<text x="20" y="{y}" fill="var(--wk-ink)" font-size="20">Round {number}</text>')
        nodes = [
            (105, y+125, 'Propose two changes', proposal, 'proposal'),
            (315, y+60, candidates[0].get('title','Candidate A') if candidates else 'Candidate A', find('probe-a','probe-0','candidate-0','probe-result-0') or proposal, 'candidate'),
            (315, y+200, candidates[1].get('title','Candidate B') if len(candidates)>1 else 'Candidate B', find('probe-b','probe-1','candidate-1','probe-result-1') or proposal, 'candidate'),
            (540, y+125, 'Compose a version', find('compose'), 'decision'),
            (750, y+125, 'Test the composition', find('composition-test','composition','composition-result'), 'execution'),
            (940, y+125, 'Retain this version' if adopt and _retained_selection(adopt, rows) else 'Save selected version', adopt, 'adoption'),
        ]
        edges = [(0,1),(0,2),(1,3),(2,3),(3,4),(4,5)]
        for a,b in edges:
            x1,y1,_,r1,_=nodes[a];x2,y2,_,r2,_=nodes[b]
            dash = '' if r1 and r2 else ' stroke-dasharray="5 5"'
            svg.append(f'<path d="M{x1+9},{y1} C{(x1+x2)/2},{y1} {(x1+x2)/2},{y2} {x2-9},{y2}" fill="none" stroke="#96aaa2" stroke-width="2"{dash}/>')
        for x,yy,label,record,kind in nodes:
            status = (record or {}).get('status','not run')
            if kind=='candidate' and record is proposal and proposal:
                status = 'proposed; not tested'
            color = '#4382a6' if kind=='candidate' else '#c17b40' if kind=='decision' else '#237a6c'
            if not record or status != 'complete': color='#7c8985'
            if record:
                svg.append(f'<a href="#branch-{escape(record["id"])}" aria-label="Round {number}: {escape(label,quote=True)}; {escape(status)}">')
            svg.append(f'<circle cx="{x}" cy="{yy}" r="8" fill="{color}"/><text x="{x}" y="{yy+25}" text-anchor="middle" fill="var(--wk-ink)" font-size="14">')
            for j,line in enumerate(textwrap.wrap(label, 23)[:3]):
                svg.append(f'<tspan x="{x}" dy="{0 if j==0 else 17}">{escape(line)}</tspan>')
            svg.append(f'</text><text x="{x}" y="{yy-18}" text-anchor="middle" fill="var(--wk-muted)" font-size="11">{escape(status)}</text>')
            if record: svg.append('</a>')
    svg.append('</svg><p>Blue: candidate · orange: composition decision · dashed line: work not yet recorded. Position and color do not represent quality.</p></section>')
    return ''.join(svg) + branches(session)
