"""Add source-linked ARIA investigations to the six authored storyboards.

The three static frames retain their geometry in PDF and in the browser. This
module reads recorded responses; it never requests an answer or invents one.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
import json
import os
from pathlib import Path
import re
import shutil

KIT = Path(__file__).resolve().parents[1]
SLUGS = {'pending':'pending_inc','solar':'solar_autoresearch','routing':'request_routing',
         'inspection':'visual_inspection','transit':'transit_factory','airline_monitoring':'airline_monitoring'}
PLACEMENTS = {
 'pending': [('investigate','manual',117),('conclusion','report',230)],
 'solar': [('investigate','images-window',147),('conclusion','conclusion-turn',348)],
 'routing': [('investigate','embeddings',51),('conclusion','report-exercise',318)],
 'inspection': [('investigate','patch-grid',64),('conclusion','reproduce',230)],
 'transit': [('investigate','Shared memory needs something worth sharing',200),('conclusion','Publish the version you can reproduce',335)],
 'airline_monitoring': [('investigate','tag-definition',110),('conclusion','conclusion',345)],
}
QUESTIONS = {
 'pending': ('Did the employee verify the account before claiming completion?', 'Did the harness change account correctness, tool behavior, or both?'),
 'solar': ('What can this validation forecast and loss curve tell us?', 'Which forecast improved, and what does this comparison leave uncertain?'),
 'routing': ('What in this validation request might explain its predicted queue?', 'Did we improve the classifier, repair its loader, or both?'),
 'inspection': ('Is this validation error about features, the threshold, or missing evidence?', 'Which defects were recovered, and which mistakes remain?'),
 'transit': ('Which development observation could support a useful project lesson?', 'Did coordination or the accepted lesson improve the delivered application?'),
 'airline_monitoring': ('Does this turn establish an unrequested itinerary change?', 'What changed in booking correctness, monitoring agreement, and coverage?'),
}
RECORDS = {
 'pending': [('Ticket and checked account','Selected starting execution','Tool result and read_skill event'),('Same fresh ticket','Three frozen harnesses','Account checks and tool events')],
 'solar': [('Forecast timestamp and units','Selected validation run','Loss curve, settings, persistence'),('Matching forecast timestamps','Frozen source and weights','Separate GOES and AIA errors')],
 'routing': [('Validation message','TF–IDF probabilities','Vectorizer and intent order'),('Same regression request','Healthy, faulty, repaired loader','Probability-column label order')],
 'inspection': [('Validation board photograph','Whole-image score and cutoff','Frozen features and reference label'),('Same final boards','Frozen detectors and cutoffs','Misses, false alarms, review volume')],
 'transit': [('Approved feature and contracts','Both integrated builds','Public checks and worker events'),('Matching acceptance scenarios','Frozen builds and memory inputs','Outputs, time, total cost')],
 'airline_monitoring': [('Passenger request','Original and returned itinerary','Reviewed turn and recovery events'),('Matching reserved bookings','Original and repaired versions','Agent checks, monitor coverage')],
}

def _key(row):
    return row.get('key') or row.get('name') or row['title']

def _safe_url(value):
    return str(value) if str(value).startswith(('https://','http://')) else ''

def _definition(deck, stop):
    manifest=json.loads((KIT/'src/forge_workshop_kit/workshops.json').read_text())
    workshop=next(item for item in manifest['templates'] if item['slug']==SLUGS[deck])
    return next(item for item in workshop['aria_investigations'] if item['id']==stop)


def _pack(deck, stop):
    path=KIT/'src/forge_workshop_kit/assets/aria'/SLUGS[deck]/f'{stop}.json'
    if not path.exists():
        return {'status':'unavailable','response':'','records':[], 'captures':[]},path
    return json.loads(path.read_text()),path

def _asset_url(path):
    return os.environ.get('DECK_BASE','').rstrip('/')+'/'+path.lstrip('/')

def _inline(value):
    value=re.sub(r'`([^`]+)`',r'<code>\1</code>',escape(value))
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)

def _record_link(url, label):
    return f'<a href="{escape(url,quote=True)}" target="_blank" rel="noopener">{escape(label)} ↗</a>' if _safe_url(url) else escape(label)

def _assets(deck_root, pack, pack_path, stop):
    dest=deck_root/'public/aria'/stop
    dest.mkdir(parents=True,exist_ok=True)
    if pack_path.exists():
        shutil.copy2(pack_path,dest/'investigation.json')
    supporting=list((pack.get('transcript_paths') or {}).values())
    supporting.extend(pack[key] for key in ('excerpt_path','excerpt_html') if pack.get(key))
    supporting.extend(item['path'] for item in pack.get('attachments',[]))
    for name in supporting:
        origin=(pack_path.parent/name).resolve()
        if not origin.is_relative_to(pack_path.parent.resolve()):
            raise ValueError('ARIA supporting files must stay inside the recorded pack directory')
        target=dest/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(origin,target)
    captures=[]
    for cap in pack.get('captures',[]):
        relative=Path(cap['path'])
        origin=(pack_path.parent/relative).resolve()
        if relative.is_absolute() or not origin.is_relative_to(pack_path.parent.resolve()):
            raise ValueError('ARIA capture must stay inside its recorded pack directory')
        if not origin.is_file():
            raise FileNotFoundError(origin)
        target=dest/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(origin,target)
        captures.append({**cap,'url':f'/aria/{stop}/{relative.as_posix()}'})
    return captures

def _graphic(deck, stop, phase):
    # This is an instructional diagram. It makes no assertion about an actual result.
    labels=RECORDS[deck][0 if stop=='investigate' else 1]
    words=['Your interpretation','ARIA response','Checked source record']
    cards=[]
    for index,(word,detail) in enumerate(zip(words,labels)):
        fill='#d9e9e1' if index==phase else '#f0eee4'
        cards.append(f'<g><rect x="{index*370}" y="18" width="340" height="116" rx="8" fill="{fill}" stroke="#48675d"/><text x="{index*370+18}" y="54" fill="#183b31" style="font-size:23px">{escape(word)}</text><text x="{index*370+18}" y="91" fill="#42584f" style="font-size:17px">{escape(detail)}</text></g>')
        if index<2: cards.append(f'<path d="M{index*370+345} 75h20" fill="none" stroke="#48675d" stroke-width="2"/><path d="M{index*370+360} 70l5 5-5 5" fill="none" stroke="#48675d" stroke-width="2"/>')
    return '<div class="aria-sequence-wrap"><svg class="aria-sequence" viewBox="0 0 1110 154" role="img" aria-label="Explain your interpretation, read ARIA’s answer, and check its cited source.">'+''.join(cards)+'</svg></div>'

def _capture(shot):
    """Outline observed fields without changing or covering the original image."""
    if not shot:
        return ''
    marks=[]
    labels=[]
    for number, item in enumerate(shot.get('annotations', []), 1):
        x,y,width,height=(float(item[key]) for key in ('x','y','width','height'))
        if not (0<=x<1 and 0<=y<1 and 0<width<=1-x and 0<height<=1-y):
            raise ValueError('ARIA annotations use normalized coordinates inside the capture')
        label=escape(item['label'])
        # The numbered marker sits just outside the outline, not on its value.
        left=max(11,x*1280-14)
        top=y*720+13
        marks.append(f'<rect x="{x*1280}" y="{y*720}" width="{width*1280}" height="{height*720}" rx="5" fill="none" stroke="#f7bd59" stroke-width="3"/><circle cx="{left}" cy="{top}" r="12" fill="#f7bd59" stroke="#182820" stroke-width="1.5"/><text x="{left}" y="{top+4}" fill="#182820" text-anchor="middle" style="font-size:14px;font-weight:600">{number}</text>')
        labels.append(f'<span><b>{number}</b> {label}</span>')
    overlay='<svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true">'+''.join(marks)+'</svg>' if marks else ''
    return (f'<figure class="aria-screen"><a href="{_asset_url(shot["url"])}" target="_blank"><img src="{shot["url"]}" alt="{escape(shot.get("caption","Recorded source"),quote=True)}">{overlay}</a>'
            +('<figcaption>'+''.join(labels)+'</figcaption>' if labels else '')+'</figure>')

def _frame(deck,stop,phase,pack,captures):
    graphic=_graphic(deck,stop,phase)
    question=_definition(deck,stop)['question']
    recorded=pack.get('status')=='recorded' and isinstance(pack.get('response'),str) and bool(pack['response'].strip())
    if phase==0:
        scope='Use only the selected development or validation records.' if stop=='investigate' else 'Keep the compared versions frozen. Suggest a future experiment without running it.'
        records=pack.get('records',[])[:3]
        links=''.join('<li>'+_record_link(r.get('url',''),r.get('label',r.get('identity','Selected record')))+'</li>' for r in records)
        selected=('<ul class="aria-records">'+links+'</ul>') if links else '<p>Select the saved records shown beside your notebook result.</p>'
        return graphic+f'<div class="aria-question">{escape(question)}</div><div class="aria-two"><div><b>Start with your explanation</b><p>What do you think happened? Which observation supports it?</p><p>Copy the notebook’s prompt and add native context in Forge.</p></div><div><b>Selected instructor records</b>{selected}</div></div><p class="aria-foot">{scope} Check ARIA’s selected project. Use exact record URLs; add native context where this surface offers it.</p>'
    if phase==1:
        if not recorded:
            return graphic+'<div class="aria-unavailable"><b>No usable recorded ARIA response is available for this stop.</b><p>Keep the original question. Inspect its selected records directly and record what you can establish. Do not present an invented answer as ARIA output.</p></div>'
        claim=pack.get('claim_excerpt') or (pack.get('citation_check') or {}).get('claim')
        # Only an explicitly selected excerpt is projected; the full response stays accessible.
        verbatim=bool(pack.get('claim_excerpt') and pack['claim_excerpt'] in pack['response'])
        claim_block=(f'<blockquote>{_inline(claim)}</blockquote>' if verbatim else f'<p><strong>Claim selected for checking:</strong> {_inline(claim)}</p>') if claim else '<p>Open the full recorded response and choose one claim to check.</p>'
        shot=next((c for c in captures if c.get('role')=='response'),captures[0] if captures else None)
        image=_capture(shot)
        transcript=(pack.get('transcript_paths') or {}).get('html')
        offline=f'<p><a href="{_asset_url(f"aria/{stop}/{escape(transcript,quote=True)}")}" target="_blank">Read the full transcript without sign-in ↗</a></p>' if transcript else ''
        return graphic+'<div class="aria-response">'+image+'<div><b>Recorded instructor investigation</b>'+claim_block+'<p>Does this statement follow from the records, or is it a possible explanation?</p>'+offline+_record_link(pack.get('conversation_url',''),'Open the recorded conversation')+'</div></div><p class="aria-foot">The recording uses instructor results. It does not describe your unexecuted edits.</p>'
    check=pack.get('citation_check') or {}
    if not recorded or not check:
        return graphic+'<div class="aria-unavailable"><b>Check a source before accepting a claim.</b><p>Open one selected record. Name its exact value, event, prediction, or changed line. Mark the interpretation supported, disputed, or unresolved.</p></div>'
    reason=check.get('reason','')
    # The full transcript retains precision; projected arithmetic needs readable values.
    reason=re.sub(r'\b\d+\.\d{8,}\b',lambda match:format(float(match.group()),'.6g'),reason)
    shot=next((c for c in captures if c.get('role')=='verification'),None)
    image=_capture(shot)
    excerpt=pack.get('excerpt_html')
    offline=f'<p><a href="{_asset_url(f"aria/{stop}/{escape(excerpt,quote=True)}")}" target="_blank">Check the supplied source values offline ↗</a></p>' if excerpt else ''
    return graphic+'<div class="aria-response">'+image+f'<div><b>Citation check: {escape(check.get("assessment","unresolved"))}</b><p>{escape(reason)}</p>'+_record_link(check.get('record_url',''),'Open the checked source')+offline+'</div></div><p class="aria-foot">Save your own citation check. ARIA’s answer does not become a label, score, approved lesson, or release decision.</p>'

def enrich(slides, deck_root, deck):
    """Insert two three-frame investigations, preserving existing slide schemas."""
    slides[:]=[s for s in slides if _key(s)!='aria']
    for row in slides:
        row['body']=re.sub(r'<p class="caption">Optional(?: ARIA investigation|: ask ARIA).*?</p>','',row['body'],flags=re.S)
        if deck=='routing' and _key(row)=='release':
            row['body']='<p>Link the exact evaluated artifact to Registry if your project has permission. Keep the checks, previous version, and release decision alongside it.</p><p class="caption">Registry manages selected versions. Your batch predictor and Artifact-based rollback already work without it.</p>'
    # Reserve the activities within existing discussion windows, including the
    # worked-example diagrams that immediately follow them. Breaks never move.
    adjusted = {'routing': {'embeddings':59,'sentence-vector':61,'construct-head':63,'fit-head':65},
                'inspection': {'regression':229,'reproduce':237,'reload-detector':238,'release':238},
                'transit': {'Shared memory needs something worth sharing':208,
                            'Check the lesson before another agent relies on it':209,
                            'Write a rule with a test attached':210,
                            'A saved note is not automatically accepted':211,
                            'First exclude the unchecked interpretation':212,
                            'Publish the version you can reproduce':342},
                'airline_monitoring': {'tag-definition':118,'counterexample-nonstop':119,'conclusion':352,'report':353}}
    for row in slides:
        adjusted_minute=adjusted.get(deck,{}).get(_key(row),adjusted.get(deck,{}).get(row['title']))
        if adjusted_minute is not None:
            row.update(time=f'{adjusted_minute//60}:{adjusted_minute%60:02d}',start_minute=adjusted_minute,elapsed_minutes=adjusted_minute)
    for stop,anchor,minute in PLACEMENTS[deck]:
        index=next(i for i,row in enumerate(slides) if _key(row)==anchor or row['title']==anchor)
        template=slides[index]
        pack,path=_pack(deck,stop)
        captures=_assets(deck_root,pack,path,stop)
        definition=_definition(deck,stop)
        duration=definition['minutes']
        purpose=definition['title']
        notes=(f'Allocate {duration} minutes within the existing discussion time. Ask for the participant’s interpretation before showing the response. '
               'The notebook agent still produces the measured changes. ARIA only investigates saved records. '
               'Use Copy investigation prompt and Open the selected Forge record. Verify the project selected inside ARIA; expanding to a full-page chat can reset it. Use exact record URLs. Add native attachments when this surface offers them. Typing @ did not open a run picker in this release check. Pasting an @ name or a URL does not prove that ARIA read a record. Excerpt-only analysis must stay labeled. '
               'ARIA requires a team project with Smart features; a successful write check does not establish that access. ARIA usage is outside the notebook’s $8 allowance. '
               'If unavailable or slow, choose Use the recorded investigation. Check one cited event, value, prediction, or code line, then Save citation check. '
               'Do not launch work, modify criteria, accept a label, or reopen the frozen comparison from this activity. '
               'If ARIA brings reserved results into a development answer, exclude that answer from development decisions and explain why. '
               f'Recording: src/forge_workshop_kit/assets/aria/{SLUGS[deck]}/{stop}.json. '
               'Native context guidance: https://docs.coreweave.com/products/aria/chat#add-context-to-a-conversation. '
               'Do not confuse plausible causes with observed evidence, tool success with task success, or fewer alerts with better monitoring.')
        extras=[]
        for phase,label in enumerate(('question','response','verify')):
            row=deepcopy(template)
            key=definition['deck_anchor'] if phase==0 else f'aria-{stop}-{label}'
            row.update(key=key,name=key,title=(purpose if phase==0 else 'Read one claim in the recorded response' if phase==1 else 'Open the source and check that claim'),
                       body=_frame(deck,stop,phase,pack,captures),notes=notes,kind='aria-investigation',cls='aria-investigation',answer=None,
                       concept=definition['question'],
                       source=['scripts/aria_storyboard.py',str(path.relative_to(KIT))],evidence=[r.get('url') for r in pack.get('records',[]) if r.get('url')],
                       exercise={'step':definition['step'],'function':None,'check':'Check one cited record','run':'Copy investigation prompt'},
                       time=f'{minute//60}:{minute%60:02d} · {duration} minutes across these three frames',
                       start_minute=minute,elapsed_minutes=minute,clicks=None,
                       aria={'stop_id':stop,'phase':label,'duration_minutes':duration,'recorded_status':pack.get('status','unavailable')})
            if 'timing' in row: row['timing']={'section':purpose,'start_minute':minute,'duration_minutes':duration}
            extras.append(row)
        slides[index:index]=extras
    return slides
