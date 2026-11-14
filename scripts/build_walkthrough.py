"""Make a read-only walkthrough from completed rehearsal receipts. No execution."""
import argparse
import html
import json
import shutil
from pathlib import Path

from forge_workshop_kit import WorkshopSession

parser = argparse.ArgumentParser()
parser.add_argument('--state', default='.workshop/solar-rehearsal')
parser.add_argument('--project', required=True)
args = parser.parse_args()
session = WorkshopSession(args.project, 'solar-autoresearch', state_dir=args.state)
journal = session.read()
result = json.loads(Path('evidence/solar-rehearsal.json').read_text())
out = Path('evidence')

def latest(name):
    return [r for r in session.completed() if r['name'] == name][-1]

def figure(name, destination):
    row = latest(name)
    shutil.copy(session.file('outputs/' + row['id'] + '/predictions.png'), out / destination)
    return destination

manual = figure('images/manual-residual', 'solar-validation.png')
final = figure('images/final-agent', 'solar-final.png')
goes = figure('goes/final', 'goes-final.png')
escape = html.escape
table = '<table><tr><th>Frozen image version</th><th>Final error ↓</th><th>Skill vs persistence ↑</th></tr>'
for label, metrics in result['results'].items():
    table += f'<tr><td>{escape(label)}</td><td>{metrics["error"]:.6f}</td><td>{metrics["skill_vs_persistence"]:.1%}</td></tr>'
table += '</table>'
first = latest('images/round-1/compose')['result']['decision']
second = latest('images/round-2/compose')['result']['decision']
trace = 'https://forge.coreweave.com/agent-lens/' + args.project + '/conversations/' + latest('images/round-2/propose')['id']
public_rows = [{k: r[k] for k in ('id','name','status','sources','source_fingerprint','config','inputs','result','started_at','ended_at') if k in r} for r in journal['stages'].values()]
(out / 'solar-executions.json').write_text(json.dumps(public_rows, indent=2))
chapters = [
    ('Your project. Your experiment.', '<p>Recorded rehearsal · November 13, 2026. These are saved executions, not results from an edit you make while watching.</p><p>Copy a notebook → authenticate in Forge → write code → publish evidence. The facilitator reads progress runs. There is no workshop gateway.</p><img src="chapter-1.png" alt="The notebook connection exercise">', 'Start by copying the notebook into your project. The first exercise instruments a small operation. No host token is involved.'),
    ('First, predict nothing changes.', '<p>GOES-15 measurements and AIA 171 Å images from February 1–14, 2014. Training: days 1–10. Validation: 11–12. Final evaluation: 13–14.</p><p>Persistence predicts the latest observation. Data windows never cross a gap or a partition. The download includes checksums and quality exclusions.</p><img src="goes-final.png" alt="Observed and predicted GOES flux">', 'The data and timestamps matter before the model does. This measurement model is undertrained at the short teaching budget. Persistence wins. That result is retained.'),
    ('Change settings, then change architectures.', '<p>Six configurations compare an MLP and temporal CNN. Images introduce a plain convolutional predictor and a residual predictor. Training code remains editable; W&B records settings, source, losses and predictions.</p><img src="solar-validation.png" alt="Five panels comparing image inputs, prediction, observation and error">', 'A configuration search changes settings in existing programs. Architecture comparison chooses an implemented model. Neither is an agent writing new research code.'),
    ('Now let an agent edit the program.', '<p>Round one proposed competing changes. The selected change replaced squared loss with absolute loss. Its validation error fell from 0.122116 to 0.120553. A dilated-convolution candidate regressed.</p><pre>' + escape(first['diff']) + '</pre><p>Round two tried learning-rate decay. Validation worsened, so composition retained the previous code.</p><p><a href="' + trace + '">Open the actual research-agent conversation ↗</a></p><img src="hosted-agent-lens.png" alt="Native Agent Lens inspection from the copied notebook">', 'Review the exact diff before execution. The agent’s rationale is a hypothesis. Probe it, compare the result, and keep the rejected branch. KEEP preserves the code fingerprint.'),
    ('Freeze. Then open the reserved dates.', table + '<p>Disk-masked image error is separate from log-flux error. These 199 image windows overlap and come from two test days; they are not 199 independent solar events.</p><img src="solar-final.png" alt="Final image prediction and error">', 'The final comparison loads saved weights and predicts. It does not train again. Look at the delivered prediction, not only the average score.'),
    ('A result you can reopen.', '<p>Code, model weights, predictions, stage receipts, traces and conclusions belong to the participant’s project. A new runtime restores completed work from an artifact.</p><p>Native EvalTables returned HTTP 500 in this rehearsal. Weave evaluations and notebook comparisons are saved; publication can be retried without another training or model request.</p><p><a href="solar-rehearsal.json">Results and costs</a> · <a href="solar-executions.json">Full executed code and decisions</a> · <a href="https://github.com/ash0ts/forge-workshop-kit">Source and setup</a></p>', 'The point is to build a research loop you can inspect and reproduce. Small validation gains may not transfer. The saved evidence lets you explain either outcome.'),
]
sections = ''.join(f'<section data-step="{i}" hidden><small>RECORDED EXAMPLE · {i+1} / 6</small><h1>{title}</h1>{body}<aside>{caption}</aside></section>' for i,(title,body,caption) in enumerate(chapters))
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Solar Autoresearch · recorded walkthrough</title><style>
body{margin:0;background:#f3f1e9;color:#182930;font:18px/1.5 system-ui}main{max-width:1100px;margin:auto;padding:32px}h1{font-size:38px;line-height:1.15}small{color:#77501d;letter-spacing:.08em}section[hidden]{display:none}img{width:100%;max-height:420px;object-fit:contain}pre{padding:16px;background:#172b35;color:#f5f0df;overflow:auto;font-size:16px}aside{background:#dfe9e7;padding:18px;border-left:4px solid #477e77;margin-top:20px}nav{position:sticky;top:0;background:#172b35;padding:16px;display:flex;gap:10px;z-index:1}button{padding:10px 15px;cursor:pointer;font-size:16px;border:1px solid #b0c5c7;background:transparent;color:white;border-radius:5px}button[aria-current=true]{background:#d99542;color:#172b35}table{width:100%;border-collapse:collapse}th,td{padding:12px;border-bottom:1px solid #bbc4c2;text-align:left}a{color:#216a76}@media(max-width:600px){main{padding:16px}h1{font-size:29px}nav{flex-wrap:wrap}button{padding:8px}pre{font-size:12px}}</style><nav aria-label="Walkthrough chapters">''' + ''.join(f'<button data-select="{i}">{i+1}. {label}</button>' for i,label in enumerate(('Copy','Baseline','Compare','Improve','Evaluate','Resume'))) + '</nav><main>' + sections + '''</main><script>
function show(i){document.querySelectorAll('section').forEach((e,n)=>e.hidden=n!==i);document.querySelectorAll('button').forEach((e,n)=>e.setAttribute('aria-current',n===i));history.replaceState(null,'','#'+(i+1));window.scrollTo(0,0)}document.querySelectorAll('button').forEach(b=>b.onclick=()=>show(+b.dataset.select));show(Math.max(0,Math.min(5,Number(location.hash.slice(1)||1)-1)));
</script></html>'''
(out / 'walkthrough.html').write_text(page)
(out / 'walkthrough-transcript.txt').write_text('\n\n'.join(title+'\n'+caption for title,_,caption in chapters))
print(out / 'walkthrough.html')
