"""Draw original airline teaching diagrams from the current figure specifications."""
from __future__ import annotations
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT/'skills/teenage-engineering-visualizations/assets/tokens.json').read_text(encoding='utf-8'))
COLORS = TOKENS['colors']
PAPER, INK, MUTED, LINE, PANEL, ORANGE, BLUE = (COLORS[k] for k in ('paper','ink','muted','line','panel','accent','candidate_a'))

class Drawing:
    def __init__(self, title, eyebrow, note, index=0, total=1):
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img"><title>{escape(title)}</title><desc>{escape(note)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="{INK}" stroke-width="1.4"/></marker></defs>']
        self.rect(0,0,1200,675,PAPER,stroke='none')
        self.text(40,28,eyebrow,16,fill=MUTED)
        self.text(40,66,title,30,weight=600)
        self.text(1160,28,f'{index+1:02}/{total:02}',16,anchor='end',mono=True)
        self.line(40,82,1160,82)
        self.text(40,650,note,17,fill=MUTED)
        self.drawing_start = len(self.parts)
    def add(self,s):self.parts.append(s)
    def text(self,x,y,s,size=20,weight=400,fill=INK,anchor='start',mono=False):
        family = 'IBM Plex Mono' if mono else 'IBM Plex Sans'
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" font-family="{family}" text-anchor="{anchor}">'+escape(str(s))+'</text>')
    def lines(self,x,y,rows,size=20,gap=26,**kw):
        for i,row in enumerate(rows):self.text(x,y+i*gap,row,size,**kw)
    def rect(self,x,y,w,h,fill='none',stroke=LINE,sw=1.5,rx=0,dash=None):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def line(self,x1,y1,x2,y2,stroke=LINE,sw=1.5,dash=None,arrow=False):
        self.add(f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def path(self,d,stroke=INK,fill='none',sw=2,dash=None,arrow=False):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def circle(self,x,y,r=5,fill=INK,stroke='none'):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
    def callout(self,n,x,y,label,tx,ty,active=True):
        self.path(f'M{x},{y+12}V{ty}H{tx}',LINE,sw=1.5)
        self.circle(tx,ty,3,INK)
        self.circle(x,y,13,ORANGE if active else INK)
        self.text(x,y+7,n,19,600,INK if active else PAPER,'middle')
        self.text(x+22,y+7,label,19,600)
    def code(self,rows,effect):
        self.drawing_end = len(self.parts)
        self.line(40,548,1160,548)
        self.text(40,574,'CODE',16,600,fill=MUTED)
        for i,row in enumerate(rows[:3]):self.text(130,574+i*23,row,17,mono=True)
        self.text(750,574,'OBSERVE',16,600,fill=MUTED)
        for i,row in enumerate(effect[:3]):self.text(750,599+i*23,row,19)
    def svg(self):return ''.join(self.parts)+'</svg>'

def ticket(d,x,y,w,label,sub='2024-05-20',accent=False,missing=False):
    # Ticket perforation, cut corners and stub make itinerary records recognizable.
    c=ORANGE if accent else INK
    d.path(f'M{x+10},{y}H{x+w-10}L{x+w},{y+10}V{y+74}L{x+w-10},{y+84}H{x+10}L{x},{y+74}V{y+10}Z',c,PAPER,2,dash='6 4' if missing else None)
    d.line(x+w-58,y+8,x+w-58,y+76,LINE,1.5,'3 4')
    d.text(x+17,y+31,label,22,600,fill=c)
    d.text(x+17,y+61,sub,16,mono=True,fill=MUTED)
    for k in range(9):d.line(x+w-45+k*3,y+19,x+w-45+k*3,y+64,INK,1 if k%3 else 2)
    if missing:
        d.line(x+8,y+7,x+w-8,y+77,ORANGE,2.5)
        d.line(x+8,y+77,x+w-8,y+7,ORANGE,2.5)

def strip(d,x,y,names,width=220,gap=18,active=None):
    for i,name in enumerate(names):ticket(d,x+i*(width+gap),y,width,name,accent=name==active)

def figure_itinerary(d,i):
    d.text(40,116,'Passenger request: replace the two outbound legs; keep the return.',22,600)
    d.text(40,158,'BEFORE',18,600,fill=MUTED)
    strip(d,235,136,['OUT-1','OUT-2','RETURN'],240,24)
    d.path('M235,231V241H739V231',ORANGE,sw=2)
    d.text(487,267,'replace_start = 0      replace_stop = 2',18,anchor='middle',mono=True)
    d.callout(1,930,259,'Untouched suffix',885,220,i==0)
    d.text(40,315,'SEND THE WHOLE FLIGHT LIST',18,600,fill=MUTED)
    # Both results are always positioned identically; each reveal adds operation detail.
    d.text(55,355,'Omission drill',21,600)
    d.text(640,355,'Complete replacement',21,600)
    if i>=1:
        ticket(d,55,376,225,'NONSTOP',accent=True)
        ticket(d,305,376,225,'RETURN',missing=True)
        ticket(d,640,376,225,'NONSTOP',accent=True)
        ticket(d,890,376,225,'RETURN')
        d.text(55,493,'[NONSTOP]',18,mono=True)
        d.text(640,493,'[NONSTOP, RETURN]',18,mono=True)
    else:
        d.text(55,425,'Payload not yet assembled',21)
        d.text(640,425,'Payload not yet assembled',21)
    d.line(602,345,602,525,LINE,1.5)
    if i>=1:
        d.text(55,525,'API succeeds; return flight is removed.',20)
        d.text(640,525,'Requested change + unchanged return.',20)
    if i>=2:
        d.callout(2,920,311,'Read the returned booking',1000,376,True)
    d.code(['current[:start] + replacement + current[stop:]'],['The API replaces the entire list.','Check the return in its response.'])


def emit(slug, functions):
    base=ROOT/'visual-guides'/slug
    for fid,fn in functions.items():
        p=base/f'{fid}.json';spec=json.loads(p.read_text(encoding='utf-8'));out=base/'art'/fid;out.mkdir(parents=True,exist_ok=True)
        for i,state in enumerate(spec['states']):
            note='Simulated booking • illustrative local drill' if fid=='itinerary' else 'Illustrative counterexamples • native status from recorded qualification' if fid=='alignment' else f'{spec["provenance"].capitalize()} teaching view • see linked source records'
            d=Drawing(spec['title'],spec['eyebrow'],note,i,len(spec['states']))
            fn(d,i)
            f=out/f'{state["id"]}.svg';f.write_text(d.svg(),encoding='utf-8')
            state['artwork']=f.relative_to(base).as_posix()
        p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(f'{slug}/{fid}: {len(spec["states"])} frames')

def flight_line(d,x,y,labels,w=420):
    step=w/max(1,len(labels)-1)
    d.line(x,y,x+w,y,INK,2)
    for j,label in enumerate(labels):
        xx=x+j*step;d.circle(xx,y,6,PAPER,INK);d.text(xx,y+31,label,18,anchor='middle',mono=True)

def figure_overview(d,i):
    d.text(40,117,'“Change the outbound flight. Keep my return.”',25,600)
    d.text(40,150,'Simulated booking • one request, four places to investigate',19,fill=MUTED)
    strip(d,40,185,['OUT-1','OUT-2','RETURN'],210,16)
    d.path('M40,280V290H476V280',ORANGE,sw=2);d.text(40,318,'Requested range [0:2]',18,mono=True)
    d.callout(1,790,182,'Booking state',597,269,i==0)
    d.text(792,221,'Original flights + passenger request',19)
    # Trace anatomy retains one booking record instead of treating it as an abstract box.
    d.line(90,343,90,476,INK,2)
    for n,(y,label) in enumerate([(351,'request_confirmation'),(396,'update_reservation_flights'),(441,'get_reservation_details')]):
        d.circle(90,y,6,ORANGE if i>=1 and n==1 else PAPER,INK)
        d.text(111,y+6,label,18,mono=True)
    d.callout(2,790,285,'Agent Lens',424,396,i==1)
    d.lines(792,324,['Arguments → returned booking','Follow errors and later recovery.'],19)
    if i>=2:
        d.text(580,412,'REVIEW',18,600);d.text(580,445,'Return preserved?',20)
        d.rect(580,461,22,22,PAPER,INK);d.path('M584,471L590,477L600,465',INK,sw=2)
        d.text(614,480,'Human label + source turn',18)
        d.line(430,443,558,443,INK,1.5,'5 4',True)
    if i>=3:
        d.path('M945,380H1110L1135,405V507H945Z',INK,PAPER,2)
        d.path('M1110,380V405H1135',INK,sw=1.5)
        d.lines(960,432,['case.json','initial_state','expected flights'],17,25,mono=True)
        d.line(855,471,927,471,INK,1.5,'5 4',True)
        d.text(945,532,'Artifact + regression test',18)
    d.code(['case = case_from_reviewed_turn(review, run)'],['Review the outcome, then the rule.','EvalTables compares repaired bookings.'])

def figure_traces(d,i):
    d.text(40,119,'One conversation, one booking, several operations',23,600)
    d.text(40,152,'Illustrative trace anatomy • duration comes from stored timestamps',18,fill=MUTED)
    d.line(65,188,65,490,INK,2)
    rows=[(202,'PASSENGER','Keep the return flight.'),(280,'TOOL','update_reservation_flights'),(393,'OBSERVATION','saved: True'),(487,'CHECK','Is RETURN still in flights?')]
    for j,(y,kind,label) in enumerate(rows):
        d.circle(65,y,7,ORANGE if j==min(i,3) else PAPER,INK)
        d.text(90,y-5,kind,16,600,fill=MUTED);d.text(90,y+22,label,20,mono=j in [1,2])
    d.line(585,177,585,521,LINE)
    d.text(625,204,'arguments.flights',20,600,mono=True)
    d.lines(625,238,['[NONSTOP, RETURN]'],20,mono=True)
    d.callout(1,988,207,'Write payload',876,238,i==1)
    ticket(d,625,291,220,'NONSTOP',accent=i>=1)
    ticket(d,869,291,220,'RETURN')
    d.text(625,411,'result.reservation.flights',19,600,mono=True)
    d.text(625,449,'[NONSTOP, RETURN]',20,mono=True)
    if i>=2:
        d.path('M625,470V486H1089V470',INK,sw=2)
        d.text(625,518,'Check RETURN against the original booking.',21)
    d.code(['Tool(arguments=args, result=result,', '     started_at=start, ended_at=end)'],['Find the payload and returned flights.','A saved write is not a correctness check.'])

def figure_alignment(d,i):
    d.text(40,117,'A shorter itinerary is not always a mistake.',24,600)
    cols=[40,575,820,1040]
    for x,s in zip(cols,['REVIEWED REQUEST','BEFORE → AFTER','HUMAN','NATIVE']):d.text(x,158,s,17,600,fill=MUTED)
    d.line(40,173,1160,173)
    data=[('Keep return; agent omits it','OUT + RETURN → OUT','Issue'),('Requested one-way trip','OUT → OUT','No issue'),('Replace connection with nonstop','A + B + RETURN → N + RETURN','No issue'),('Explicit full-itinerary change','OUT + RETURN → NEW + NEW','No issue'),('Still waiting for confirmation','Booking has not changed','Unresolved')]
    for j,(request,change,label) in enumerate(data):
        y=209+j*57
        d.text(40,y,request,19)
        # Mini literal flight-chain segments reveal the distinction visually.
        if j<4:
            names=[('O','R'),('O',),('A','B','R'),('O','R')][j]
            after=[('O',),('O',),('N','R'),('N','N')][j]
            xx=580
            for k,name in enumerate(names):d.rect(xx+k*28,y-19,23,26,PANEL,INK);d.text(xx+11+k*28,y+1,name,16,anchor='middle',mono=True)
            d.line(665,y-6,690,y-6,INK,1.5,arrow=True)
            for k,name in enumerate(after):d.rect(705+k*28,y-19,23,26,PAPER,INK);d.text(716+k*28,y+1,name,16,anchor='middle',mono=True)
        else:d.text(580,y,'No write yet',17,mono=True)
        d.text(820,y,label if i>=0 else '—',19,600 if j==0 else 400)
        d.text(1040,y,'Not run here',18,fill=MUTED)
        d.line(40,y+20,1160,y+20)

    if i>=1:
        d.text(40,485,'Separate native qualification: six HTTP 500 responses' if i>=3 else 'Rule: unrequested change to preserved flights',20,600)
    d.text(40,516,'O / OUT = outbound    R = return    N = replacement',18,mono=True,fill=MUTED)
    d.code(['criteria = "Flag unrequested itinerary changes."'],['Six recorded native tests: HTTP 500.','A missing judgment is not “no issue”.'])

def figure_coverage(d,i):
    d.text(40,116,'Illustrative arithmetic: 8 eligible turns, 6 completed judgments',24,600)
    d.text(40,157,'TURN',17,600,fill=MUTED)
    statuses=['flag','flag','flag','clear','clear','clear','pending','unavailable']
    human=['issue','issue','no issue','issue','no issue','no issue','—','—']
    for j,s in enumerate(statuses):
        x=100+j*130
        d.text(x,157,f'{j+1:02}',18,mono=True)
        d.path(f'M{x-20},183H{x+82}L{x+96},197V303H{x-20}Z',INK,PAPER,1.5)
        d.path(f'M{x+82},183V197H{x+96}',INK,sw=1)
        if j<6:
            d.circle(x+35,223,17,ORANGE if s=='flag' else PANEL)
            d.text(x+35,230,'!' if s=='flag' else '–',22,600,anchor='middle')
        else:
            d.circle(x+35,223,17,PAPER,LINE);d.text(x+35,230,'?' if j==6 else '×',22,anchor='middle')
        d.text(x+35,279,s,16,anchor='middle',mono=True)
        d.text(x+35,336,human[j] if i>=2 else 'review',17,anchor='middle')
    d.text(40,336,'HUMAN',16,600,fill=MUTED)
    d.path('M87,355V367H834V355',INK,sw=2)
    d.text(87,398,'6 completed judgments / 8 eligible turns',22,600)
    if i>=1:d.text(917,397,'75% coverage',22,600)
    if i>=2:
        d.line(40,425,1160,425)
        d.text(40,465,'Precision = 2 / 3',25,600);d.text(40,501,'Actual issues among 3 flagged turns',19)
        d.text(640,465,'Recall = 2 / 3',25,600);d.text(640,501,'Flagged issues among 3 reviewed issues',19)
    d.code(['coverage = len(completed) / len(eligible)', 'precision = TP / (TP + FP)', 'recall = TP / (TP + FN)'],['Keep pending and unavailable visible.','Agreement uses reviewed turns only.'])

def document(d,x,y,w,title,rows,accent=False):
    d.path(f'M{x},{y}H{x+w-24}L{x+w},{y+24}V{y+160}H{x}Z',ORANGE if accent else INK,PAPER,2)
    d.path(f'M{x+w-24},{y}V{y+24}H{x+w}',INK,sw=1)
    d.text(x+15,y+42,title,20,600)
    d.lines(x+15,y+76,rows,17,26,mono=True)

def figure_regression(d,i):
    d.text(40,116,'Keep the original booking. Replaying the final state changes the test.',23,600)
    d.text(40,157,'ORIGINAL BOOKING',18,600,fill=MUTED)
    for k,name in enumerate(['OUT-1','OUT-2','RETURN']):ticket(d,40,177+k*86,235,name)
    d.text(400,157,'FAULTY WRITE',18,600,fill=MUTED)
    d.text(400,211,'update_reservation_flights',18,mono=True)
    d.text(400,252,'flights = [NONSTOP]',22,600,mono=True)
    d.text(400,293,'Whole-list replacement',20)
    d.text(400,325,'saved: True',20,mono=True)
    d.line(290,264,380,264,INK,2,arrow=True)
    d.line(725,264,807,264,INK,2,arrow=True)
    d.text(830,157,'RETURNED BOOKING',18,600,fill=MUTED)
    ticket(d,830,177,280,'NONSTOP',accent=True)
    ticket(d,830,290,280,'RETURN',missing=True)
    if i>=1:
        d.path('M970,389V470H158V439',BLUE,sw=2.5,dash='6 4',arrow=True)
        d.text(330,454,'Restore the original booking, then test the repair.',21,600,fill=BLUE)
    if i>=2:
        d.text(40,520,'case.json: request + initial_state + policy',19,mono=True)
        d.text(655,520,'Expected: [NONSTOP, RETURN]',19,600,mono=True)
    d.code(['case["initial_state"] = deepcopy(run["initial_state"])'],['Replay starts before the faulty write.','Keep review and source links with it.'])

def figure_comparison(d,i):
    d.text(40,118,'Agent correctness and monitor availability are different outcomes.',23,600)
    d.text(40,166,'ILLUSTRATIVE MATCHED BOOKING',18,600,fill=MUTED)
    flight_line(d,110,211,['OUT-1','OUT-2','RETURN'],410)
    d.path('M310,252V302H120V315',INK,sw=1.5,arrow=True);d.path('M310,302H715V315',INK,sw=1.5,arrow=True)
    d.text(40,338,'Original agent',22,600);d.text(640,338,'Repaired agent',22,600)
    if i>=1:
        strip(d,40,359,['NONSTOP','RETURN'],220,20)
        strip(d,640,359,['NONSTOP','RETURN'],220,20)
    else:
        d.text(40,401,'Inspect the matched execution next.',21)
        d.text(640,401,'Use an isolated copy of the same booking.',21)
    d.text(40,477,'All 40 recorded live conversations passed booking checks.' if i>=3 else 'Compare requested changes and untouched flights.',23,600)
    d.text(40,511,'Use the labeled omission drill to study the failure mechanism.',20)
    d.text(680,178,'MONITOR',18,600,fill=MUTED)
    d.text(680,217,'Frozen criteria',23,600)
    d.line(680,238,1110,238)
    d.text(680,260,'6 native tests: HTTP 500' if i>=2 else 'Judging not yet inspected',21,mono=True)
    d.text(680,289,'Judgments unavailable' if i>=2 else 'Keep criteria fixed.',19)
    d.code(['before = run["initial_state"]["reservation"]','after = run["world"]["reservation"]'],['Preserve successful live traffic.','Monitoring failures stay separate.'])

def write_hero(slug, fn):
    spec=json.loads((ROOT/'visual-guides'/slug/'overview.json').read_text(encoding='utf-8'))
    d=Drawing(spec['title'],spec['eyebrow'],'',len(spec['states'])-1,len(spec['states']))
    fn(d,len(spec['states'])-1)
    opening=d.parts[0].replace('height="675" viewBox="0 0 1200 675"','height="455" viewBox="0 0 1200 455"')
    art=opening+f'<rect width="1200" height="455" fill="{PAPER}"/><g transform="translate(0,-90)">'+''.join(d.parts[d.drawing_start:d.drawing_end])+'</g></svg>'
    (ROOT/'visual-guides'/slug/'hero.svg').write_text(art,encoding='utf-8')

if __name__=='__main__':
    emit('airline_monitoring', {'overview':figure_overview,'itinerary':figure_itinerary,'traces':figure_traces,'alignment':figure_alignment,'coverage':figure_coverage,'regression':figure_regression,'comparison':figure_comparison})
    # The poster uses the same itinerary anatomy, without inventing a second system.
    write_hero('airline_monitoring',figure_overview)
