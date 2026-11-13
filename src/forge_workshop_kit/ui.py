"""Small notebook presentation helpers. Execution always needs an explicit button."""
from html import escape
import json

STYLE='''<style>
.workshop-head{padding:24px;border-left:5px solid #e89b49;background:#14252e;color:#f4f0e7;border-radius:8px;margin:12px 0}
.workshop-head h1{font-size:32px;line-height:1.15;margin:8px 0}.workshop-head p{max-width:75ch;line-height:1.6}
.workshop-label{letter-spacing:.08em;text-transform:uppercase;font-size:12px;color:#f5b869}
.workshop-step{padding:18px;border:1px solid #647885;border-radius:8px;margin:12px 0}
.workshop-step h2{margin:0 0 10px}.workshop-step p{line-height:1.6}
.workshop-evidence{display:flex;flex-wrap:wrap;gap:12px;margin:12px 0}.workshop-evidence a{padding:10px 14px;border:1px solid #78909c;border-radius:6px}
</style>'''


def heading(title,description):
    return STYLE+f'<div class="workshop-head"><div class="workshop-label">Forge · Build, measure, improve</div><h1>{escape(title)}</h1><p>{escape(description)}</p></div>'


def step(title,task,expected):
    return f'<div class="workshop-step"><h2>{escape(title)}</h2><p>{escape(task)}</p><p><strong>Check:</strong> {escape(expected)}</p></div>'


def links(values):
    return '<div class="workshop-evidence">'+''.join(f'<a href="{escape(url,quote=True)}" target="_blank" rel="noopener">{escape(label)}</a>' for label,url in values.items() if isinstance(url,str) and url.startswith('https://'))+'</div>'


def branches(session):
    rows=[r for r in session.read()['stages'].values() if '/round-' in r['name']]
    items=[]
    for row in rows:
        result=row.get('result',{})
        titles=[c.get('title','Proposed code change') for c in result.get('candidates',[])]
        if isinstance(result.get('decision'),dict):
            titles=[result['decision'].get('title','Composition decision')]
        elif result.get('decision'):
            titles=[result.get('title','Retain this harness' if result['decision']=='KEEP' else 'Revise the harness')]
        label='; '.join(titles) or row['name'].split('/')[-1].replace('-',' ')
        items.append(f'<details class="workshop-step"><summary>{escape(row["name"])} · {escape(row["status"])} · {escape(label)}</summary><pre>{escape(json.dumps(result,indent=2)[:20000])}</pre></details>')
    return ''.join(items) or '<p>Branches appear after proposals and their executions are saved.</p>'


def branch_graph(session):
    """All edges come from saved round stages; vertical position does not encode quality."""
    rows=session.read()['stages'].values()
    pieces=['<svg viewBox="0 0 760 420" role="img" aria-label="Two research rounds: proposals, probes, composition and adoption" style="width:100%;max-width:900px;background:#14252e;border-radius:8px">']
    for number in (1,2):
        group=list(reversed([r for r in rows if f'/round-{number}/' in r['name']]))
        y=30+(number-1)*205
        pieces.append(f'<text x="20" y="{y}" fill="#f5b869" font-size="15">Round {number}</text>')
        if not group:
            pieces.append(f'<text x="20" y="{y+40}" fill="#a5b6bf">Not run</text>')
            continue
        proposal=next((r for r in group if r['name'].endswith('/propose')),None)
        candidates=(proposal or {}).get('result',{}).get('candidates',[])
        for i,candidate in enumerate(candidates):
            yy=y+50+i*55
            title=candidate.get('title','Proposed change')
            pieces.append(f'<path d="M40,{y+80} C100,{y+80} 100,{yy} 160,{yy}" fill="none" stroke="#6baae8" stroke-width="2"/>')
            pieces.append(f'<circle cx="160" cy="{yy}" r="5" fill="#6baae8"/><text x="175" y="{yy+5}" fill="#f4f0e7" font-size="12">{escape(title[:48])}</text>')
        for index,label in enumerate(('Probes','Composition','Adoption')):
            suffix=('/probe-done','/probed') if index==0 else ('/compose',) if index==1 else ('/adopt','/adopted')
            record=next((r for r in group if r['name'].endswith(suffix)),None)
            x=480+index*90
            status=(record or {}).get('status','not run')
            color='#e89b49' if status=='complete' else '#77848c'
            pieces.append(f'<path d="M{x-75},{y+80} L{x},{y+80}" stroke="{color}"/><circle cx="{x}" cy="{y+80}" r="6" fill="{color}"/><text x="{x-30}" y="{y+110}" fill="#f4f0e7" font-size="11">{label}</text><text x="{x-30}" y="{y+128}" fill="#a5b6bf" font-size="10">{status}</text>')
    pieces.append('</svg>')
    return ''.join(pieces)+branches(session)
