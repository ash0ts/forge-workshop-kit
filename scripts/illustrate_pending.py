"""Original state illustrations for the Pending teaching guides. No workshop execution."""
from pathlib import Path
import html
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/teenage-engineering-visualizations'
TOKENS = json.loads((SKILL / 'assets/tokens.json').read_text(encoding='utf-8'))['colors']
P, I, M, L, A, BLUE = [TOKENS[k] for k in ('paper', 'ink', 'muted', 'line', 'accent', 'candidate_a')]
FONT = ''  # The renderer supplies the bundled Plex fonts to inlined artwork.

class Drawing:
    def __init__(self, title, chapter, state, index, total):
        self.evidence = 'Illustrative'
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-label="{html.escape(title,quote=True)}"><style>{FONT}text{{font-family:"IBM Plex Sans";fill:{I}}}.mono{{font-family:"IBM Plex Mono"}}</style><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{I}" stroke-width="1.3"/></marker></defs><rect width="1200" height="675" fill="{P}"/>']
        self.text(38,29,chapter.upper(),16,mono=True)
        self.text(1162,29,f'{index+1:02d} / {total:02d}',16,mono=True,anchor='end')
        self.text(38,67,title,30,weight=600)
        self.line(38,84,1162,84,color=L)
    def add(self,s): self.parts.append(s)
    def text(self,x,y,value,size=18,color=None,mono=False,weight=400,anchor='start'):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" xml:space="preserve" class="{"mono" if mono else "sans"}" style="white-space:pre;fill:{color or I}">{html.escape(str(value))}</text>')
    def lines(self,x,y,values,size=18,leading=25,**kw):
        for n,v in enumerate(values): self.text(x,y+n*leading,v,size,**kw)
    def line(self,x1,y1,x2,y2,color=None,width=1.5,dash=None):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or I}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def path(self,d,color=None,width=1.8,arrow=False,dash=None,fill='none'):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{color or I}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def rect(self,x,y,w,h,fill=None,stroke=None,width=1.5):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or P}" stroke="{stroke or I}" stroke-width="{width}"/>')
    def dot(self,x,y,r=4,fill=None): self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or A}"/>')
    def call(self,n,x,y,tx,ty,label=None):
        self.path(f'M{x} {y} L{tx} {ty}',width=1)
        self.dot(tx,ty,3,I)
        self.add(f'<circle cx="{x}" cy="{y}" r="13" fill="{P}" stroke="{I}" stroke-width="1.5"/>')
        self.text(x,y+6,n,17,weight=600,anchor='middle')
        if label:self.text(x+23,y+6,label,18)
    def sheet(self,x,y,w,h,title,accent=False):
        self.path(f'M{x} {y} H{x+w-20} L{x+w} {y+20} V{y+h} H{x} Z',fill='#ffffff',color=A if accent else I,width=2 if accent else 1.5)
        self.path(f'M{x+w-20} {y} V{y+20} H{x+w}',color=L)
        self.text(x+16,y+30,title,19,weight=600)
        self.line(x,y+44,x+w,y+44,color=L)
    def group(self,shown=True):self.add(f'<g opacity="{1 if shown else .25}">')
    def end(self):self.add('</g>')
    def footer(self,code,effect):
        self.line(38,574,1162,574,color=L)
        self.text(38,602,code,16,mono=True)
        self.text(38,636,self.evidence,17,weight=600)
        for n,line in enumerate(textwrap.wrap(effect,width=94)):
            self.text(216,632+n*23,line,18,weight=600)
    def save(self,path):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(self.parts)+'</svg>',encoding='utf-8')

def dispatch(d,k):
    # One message stack, one real function registry, and a scoped account ledger.
    d.text(47,118,'REQUEST n / visible history',18,weight=600)
    for off in (12,6):d.rect(47+off,142-off,337,185,fill=P,stroke=L)
    d.rect(47,142,337,185,fill='#fff')
    for y,role,body in [(172,'system','rules + tool names'),(215,'user','acme / invoice inv-1')]:
        d.text(61,y,role,16,mono=True,color=M);d.text(153,y,body,16,mono=True)
        d.line(47,y+15,384,y+15,color=L)
    d.rect(47,244,337,83,fill='#e8e9e3',stroke=A,width=2)
    d.text(61,272,'assistant',16,mono=True)
    d.text(61,306,'action: lookup_invoice',18,mono=True)
    d.path('M384 283 H435 V187 H467',arrow=True)
    d.text(474,119,'FUNCTION REGISTRY',16,mono=True)
    d.group(k>=1)
    for y,name in [(150,'lookup_invoice'),(205,'get_account'),(260,'refund_payment')]:
        d.rect(470,y,269,43,fill='#fff',stroke=A if y==150 else L,width=2 if y==150 else 1)
        d.dot(482,y+22,4,A if y==150 else L)
        d.text(499,y+29,name,18,mono=True)
    d.text(476,335,'invoice_tool(world, **arguments)',16,mono=True)
    for y,label in [(377,'account_id = acme'),(416,'invoice_id = inv-1')]:
        d.dot(484,y-6,5,I);d.text(500,y,label,16,mono=True)
    d.path('M739 171 H778 V155 H806',arrow=True)
    d.path('M484 371 H463 V172 H470',color=A)
    d.path('M484 410 H452 V172 H470',color=A)
    d.text(819,119,'WORLD / accounts',18,weight=600)
    d.rect(806,139,348,263,fill='#fff')
    d.rect(806,139,348,42,fill='#e8e9e3',stroke=I)
    d.text(824,168,'acme',22,mono=True)
    d.text(824,212,'payment   invoice   cents',16,mono=True,color=M)
    for y,pay in [(250,'pay-1'),(291,'pay-2')]:
        d.rect(818,y-26,324,35,fill=P,stroke=A,width=2)
        d.text(827,y,f'{pay}     inv-1     4900',16,mono=True)
    d.line(806,319,1154,319,color=L)
    d.text(824,351,'other-account',18,mono=True,color=M)
    d.text(824,382,'same IDs / outside this lookup',16,color=M)
    d.path('M1142 275 H1170 V463 H746',arrow=True)
    d.end()
    d.text(47,365,'REQUEST n + 1 / enlarged appended turn',18,weight=600)
    d.group(k>=2)
    d.rect(47,389,337,155,fill='#fff')
    d.lines(64,421,['system  rules + tool names','user    acme / inv-1'],16,mono=True)
    d.text(64,504,'Previous turns retained',18)
    d.path('M68 327 V352 H34 V462 H47',dash='5 5')
    d.rect(395,444,749,100,fill='#fff',stroke=A,width=2)
    d.text(415,477,'assistant  action: lookup_invoice(acme, inv-1)',18,mono=True)
    d.line(395,492,1144,492,color=L)
    d.text(415,526,'user       observation: pay-1 + pay-2, 4900 cents each',16,mono=True)
    d.path('M384 462 H395',arrow=True)
    d.end()
    d.footer('next_messages = append(messages, action, result)', ['Select one action from the current request; its arguments identify the account and invoice.','The selected function reads only acme; matching IDs in another account are irrelevant.','The next request retains the old turns and appends the actual action and returned observation.'][min(k,2)])

def ledger(d,x,y,w=490,refund=False):
    d.sheet(x,y,w,238,'Account acme / invoice inv-1')
    d.text(x+18,y+78,'payment     charged    disposition',16,mono=True,color=M)
    d.line(x+12,y+91,x+w-12,y+91,color=L)
    d.text(x+18,y+122,'pay-1       $49.00     retained',18,mono=True)
    d.text(x+18,y+162,'pay-2       $49.00     '+('refunded' if refund else 'duplicate'),18,mono=True)
    d.line(x+12,y+180,x+w-12,y+180,color=L)
    d.text(x+18,y+215,'refunds: '+('[pay-2, 4900 cents]' if refund else '[]'),18,mono=True,color=A if refund else I)

def overview(d,k):
    d.sheet(48,142,290,255,'Customer ticket',k==0)
    d.lines(68,219,['Acme was charged twice.','Keep payment pay-1.','Refund the duplicate.'],21,leading=34)
    d.text(68,366,'Fictional development case',16,color=M)
    d.group(k>=1)
    d.text(405,135,'Your Python + instructions',18,weight=600)
    for y,label in [(191,'lookup'),(274,'choose'),(357,'act')]:
        d.add(f'<circle cx="480" cy="{y}" r="36" fill="{P}" stroke="{A if k==1 else I}" stroke-width="2"/>')
        d.text(480,y+6,label,18,anchor='middle')
    d.path('M338 234 H400 V191 H442',arrow=True)
    d.path('M480 227 V236',arrow=True)
    d.path('M480 310 V319',arrow=True)
    d.path('M516 357 H608 V230 H655',arrow=True)
    d.end()
    d.group(k>=2)
    ledger(d,655,142,490,refund=k>=2)
    d.call(1,1040,425,1050,302,'')
    d.text(645,428,'Read delivered state before claiming success.',18)
    d.path('M900 380 V452 H480 V395',arrow=True,dash='6 5')
    d.text(690,475,'observation returns to the loop',16,mono=True)
    d.end()
    d.group(k>=3)
    d.text(48,502,'Compare changes on matching fresh cases',20,weight=600)
    for x,label in [(48,'Starting'),(410,'Manual'),(772,'Agent-selected')]:
        d.text(x,543,label,18)
        for j in range(4):d.rect(x+160+j*26,524,18,18,fill=I)
        d.text(x+280,543,'4 / 4',18,mono=True)
    d.end()
    d.footer('Inspect the account → edit the harness → compare matching cases','Starting, manual and agent-selected versions each passed 4/4; correctness did not increase.' if k>=3 else 'The ticket asks for a state change. A completion message is only a claim.')

def harness(d,k):
    d.text(46,120,'HARNESS FILES / editable inputs',18,weight=600)
    d.path('M47 145 H379 V239 H47 Z M58 136 H390 V229',fill='#fff')
    d.text(65,174,'instructions.md',21,mono=True)
    d.lines(65,205,['Task + operating rules'],18)
    d.path('M379 190 H443 V174 H495',arrow=True)
    d.text(503,120,'build_messages() / request cutaway',18,weight=600)
    d.rect(495,143,655,284,fill='#fff',width=2)
    d.rect(495,143,116,219,fill='#e8e9e3',stroke=L)
    d.text(512,178,'system',19,mono=True)
    for y,label in [(175,'harness.instructions'),(222,'RULES: protect unrelated records'),(269,'TOOL_GUIDE: names + argument schema'),(316,'installed skill names')]:
        d.text(630,y,label,18,mono=True)
        d.line(612,y+17,1150,y+17,color=L)
    d.line(495,362,1150,362,color=I)
    d.text(512,400,'user',19,mono=True)
    d.text(630,400,'task["mission"] → the customer ticket',18,mono=True)
    d.group(k>=1)
    d.text(47,285,'TOOL ANATOMY',16,mono=True)
    d.text(47,321,'lookup_invoice',23,mono=True)
    for y,label in [(354,'account_id'),(387,'invoice_id')]:
        d.dot(66,y-6,5,I);d.text(83,y,label,18,mono=True)
    d.path('M199 351 H280 V269 H495',arrow=True)
    d.text(47,438,'Python implementation',18,weight=600)
    d.path('M47 454 H396 V541 H47 Z',fill='#fff')
    d.lines(64,483,['account = state["accounts"]','account = account[account_id]'],16,leading=29,mono=True)
    d.path('M1150 400 H1170 V553 H417 V498 H396',arrow=True)
    d.text(705,549,'fixed model → selected action → dispatch',16,mono=True)
    d.end()
    d.group(k>=2)
    d.path('M510 461 H1127 V516 H510 Z',fill='#e8e9e3',color=A,width=2)
    d.text(530,485,'read_skill("verify-operation")',18,mono=True)
    d.text(530,509,'returned file text becomes a later observation',18)
    d.path('M1018 316 H1136 V461',arrow=True,dash='5 5')
    d.end()
    d.footer('A tool schema exposes an action; the function determines its effect.','Skill names enter the first request; contents enter only after an actual read.')

def skills(d,k):
    d.sheet(47,145,330,340,'skills/verify-operation.md',k==0)
    d.lines(68,223,['Read the account.','Check the requested change.','Verify before reporting.'],20,leading=34)
    d.text(68,453,'Available on disk',18,color=M)
    d.text(430,121,'TRACE / ONE TURN',16,mono=True)
    d.line(462,153,462,506,color=L,width=3)
    d.dot(462,197,7,I);d.text(483,202,'selected action',18)
    d.group(k>=1)
    d.dot(462,285,8,A);d.text(483,269,'read_skill',22,mono=True)
    d.text(483,299,'name: verify-operation',16,mono=True)
    d.path('M377 285 H449',arrow=True)
    d.dot(462,386,7,I);d.text(483,391,'actual returned text',18)
    d.path('M462 394 V449 H744',arrow=True)
    d.end()
    d.group(k>=2)
    d.sheet(744,145,408,360,'Next model request',k==2)
    d.text(765,221,'system + customer + history',18)
    d.line(760,242,1135,242,color=L)
    d.lines(765,279,['assistant: read_skill','user: returned procedure'],18,mono=True)
    d.rect(764,345,367,135,fill='#e8e9e3',stroke=A,width=2)
    d.lines(781,379,['Read the account.','Check the requested change.','Verify before reporting.'],19,leading=31)
    d.end()
    d.footer('messages = append(messages, action, result)','Trace the edited text into the next request before attributing a behavior change to it.')

def retry(d,k):
    d.text(47,120,'FIRST ATTEMPT',16,mono=True)
    d.text(47,166,'join-alex',26,mono=True)
    d.path('M210 158 H340',arrow=True)
    d.text(245,138,'commit',18)
    d.sheet(340,119,310,128,'Account fern')
    d.text(360,201,'Alex / member / ×1',22,mono=True)
    d.path('M340 226 H220',dash='6 5')
    d.line(231,216,249,234,color=A,width=2);d.line(231,234,249,216,color=A,width=2)
    d.text(48,232,'timeout response',20,color=A)
    d.text(720,155,'The write happened.',25,weight=600)
    d.text(720,190,'The caller did not receive confirmation.',18)
    d.line(48,280,1150,280,color=L)
    for y,label,shown,count,key,color in [(336,'Change identity',k>=1,2,'join-alex-retry',A),(475,'Reuse identity',k>=2,1,'join-alex',BLUE)]:
        d.group(shown)
        d.text(48,y,label,22,weight=600)
        d.text(48,y+34,key,20,mono=True,color=color)
        d.path(f'M300 {y+10} H410',arrow=True)
        d.text(430,y-2,'operation ledger',16,mono=True,color=M)
        d.rect(424,y+10,230,43,fill='#fff',stroke=color,width=2)
        d.text(440,y+39,'new write' if count==2 else 'existing receipt',18)
        d.path(f'M654 {y+31} H760',arrow=True)
        for j in range(count):
            d.rect(786+j*174,y-5,157,63,fill='#fff')
            d.text(804+j*174,y+22,'Alex',23,weight=600)
            d.text(804+j*174,y+45,'member',16,mono=True)
        if count==1:
            d.text(971,y+11,'onboarding_status',16,mono=True)
            d.text(971,y+40,'verifies ×1',20,weight=600)
        d.end()
    d.footer('receipt = call_tool("provision_member", dict(arguments))','Controlled repair exercise: preserve operation_id, then verify the actual membership count.')

def checks(d,k):
    ledger(d,355,185,490,refund=True)
    d.text(380,143,'ONE DELIVERED ACCOUNT',16,mono=True)
    d.text(45,165,'1  Agent tool',22,weight=600)
    d.text(45,198,'check_work',18,mono=True)
    d.path('M355 264 H255 V211',arrow=True,dash='6 5')
    d.text(45,238,'Did the employee use it?',18)
    d.group(k>=1)
    d.text(45,368,'2  Your scorer',22,weight=600)
    d.lines(45,402,['Inspect refund count,','payment and amount.'],18)
    d.path('M355 386 H279',arrow=True,dash='6 5')
    d.end()
    d.group(k>=2)
    d.text(884,165,'3  Final grader',22,weight=600)
    d.lines(884,199,['Fresh tickets;','outside harness files.'],18)
    d.path('M845 264 H1013 V245',arrow=True,dash='6 5')
    d.end()
    d.group(k>=3)
    d.text(884,369,'4  Explanation judge',22,weight=600)
    d.lines(884,404,['Compare the message','with recorded work.'],18)
    d.path('M845 386 H875',arrow=True,dash='6 5')
    d.path('M382 478 H797 V544 H382 Z M405 544 L392 557 L430 544',fill='#fff')
    d.text(402,519,'“The duplicate payment was refunded.”',18)
    d.path('M797 511 H1027 V445',arrow=True,dash='6 5')
    d.end()
    d.footer('len(refunds) == 1 and refunds[0]["amount_cents"] == 4900','The state checks inspect the account; the judge evaluates the message about the work.')

def changes(d,k):
    d.sheet(47,237,248,160,'Starting harness',k==0)
    d.lines(65,307,['instructions.md','skills/*.md'],18,mono=True)
    d.text(65,371,'Original case snapshot',16)
    for y,name,visible,color in [(144,'Candidate A',k>=1,BLUE),(363,'Candidate B',k>=2,A)]:
        d.group(visible)
        d.path(f'M295 317 H345 V{y+85} H399',arrow=True,color=color)
        d.sheet(399,y,310,166,name,k==1 if name.endswith('A') else k==2)
        d.text(417,y+78,'reviewed file diff',18)
        for n,w in enumerate([223,170,205]):
            d.text(418,y+108+n*23,'+' if n==1 else '−',18,mono=True,color=color)
            d.line(447,y+102+n*23,447+w,y+102+n*23,color=color,width=2)
        d.path(f'M709 {y+83} H782',arrow=True)
        d.text(792,y+68,'Fresh copy of same case',18)
        d.text(792,y+100,'probe record: inspect result',16,mono=True)
        d.end()
    d.group(k>=3)
    d.path('M1094 255 H1140 V305 H1120',arrow=True,dash='6 5')
    d.path('M1094 460 H1140 V327 H1120',arrow=True,dash='6 5')
    d.text(789,321,'Select / combine / retain',22,weight=600)
    d.lines(789,354,['A new combination','needs its own test.'],18)
    d.end()
    d.footer('parent → independent proposals → probe records → adoption decision','Recorded final account correctness: starting 4/4 · manual 4/4 · agent-selected 4/4' if k>=4 else 'A proposal has no result until executed. Both branches begin from the same saved case.')


class PosterDrawing(Drawing):
    """An object-only poster inset; no slide title, counter or result strip."""
    def __init__(self, title, description):
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="455" viewBox="0 0 1200 455" role="img" aria-label="{html.escape(title,quote=True)}"><title>{html.escape(title)}</title><desc>{html.escape(description)}</desc><style>{FONT}text{{font-family:"IBM Plex Sans";fill:{I}}}.mono{{font-family:"IBM Plex Mono"}}</style><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{I}" stroke-width="1.3"/></marker></defs><rect width="1200" height="455" fill="{P}"/>']


def poster_hero():
    d=PosterDrawing('A customer ticket, agent tools, and the resulting account',
        'Illustrative acme invoice inv-1. The ticket asks to keep pay-1 and refund duplicate pay-2. The agent calls lookup_invoice and refund_payment, then reads the actual account. The ledger retains pay-1 and records the 4900-cent refund for pay-2.')
    # Customer paper ticket, with a perforated end and concrete requested record changes.
    d.path('M28 63H294V357L280 367L266 357L252 367L238 357L224 367L210 357L196 367L182 357L168 367L154 357L140 367L126 357L112 367L98 357L84 367L70 357L56 367L42 357L28 367Z',fill='#fff',width=2)
    d.text(48,103,'Customer ticket',28,weight=600)
    d.line(28,124,294,124,color=L)
    d.lines(48,163,['acme / inv-1','Charged twice.'],24,leading=42,mono=False)
    d.lines(48,259,['Keep pay-1.','Refund pay-2.'],26,leading=43,weight=600)
    d.line(43,330,278,330,color=L,dash='4 5')
    # The operative loop is a growing message sheet with real tool names.
    for off in (12,6):d.rect(364+off,82-off,279,264,fill=P,stroke=L)
    d.rect(364,82,279,264,fill='#fff',width=2)
    d.text(383,118,'Agent loop',28,weight=600)
    d.line(364,137,643,137,color=L)
    d.text(383,177,'lookup_invoice',24,mono=True)
    d.line(380,199,628,199,color=L)
    d.text(383,238,'refund_payment',24,mono=True)
    d.line(380,260,628,260,color=L)
    d.text(383,302,'read account',26,weight=600)
    d.path('M294 219H328V176H362',arrow=True,width=2)
    d.path('M643 238H666V188H689',arrow=True,width=2)
    # Delivered account anatomy; the selected payment changes, its neighbor is retained.
    d.rect(691,63,480,284,fill='#fff',width=2)
    d.rect(691,63,480,64,fill='#e8e9e3')
    d.text(713,106,'Account acme / inv-1',28,weight=600)
    d.text(713,164,'payment   cents   state',24,mono=True,color=M)
    d.line(704,182,1157,182,color=L)
    d.text(713,221,'pay-1     4900    kept',24,mono=True)
    d.rect(704,240,453,53,fill=P,stroke=A,width=2)
    d.text(713,276,'pay-2     4900    refunded',24,mono=True)
    d.text(713,329,'refunds: [pay-2]',26,mono=True,weight=600)
    d.path('M1100 347V407H502V346',arrow=True,width=2,dash='7 6')
    d.text(700,440,'Read back the changed record',26,weight=600)
    d.save(ROOT/'visual-guides/pending/hero.svg')


def build(only=None):
    folder=ROOT/'visual-guides/pending'
    functions={'dispatch':dispatch,'overview':overview,'harness':harness,'skills':skills,'retry':retry,'checks':checks,'changes':changes}
    for name,fn in functions.items():
        if only and name!=only:continue
        path=folder/(name+'.json');spec=json.loads(path.read_text(encoding='utf-8'))
        for index,state in enumerate(spec['states']):
            d=Drawing('A tool call becomes context' if name=='dispatch' else spec['title'],'Pending / '+name,state,index,len(spec['states']))
            if (name=='overview' and index>=3) or (name=='changes' and index>=4):d.evidence='Recorded scores'
            elif name=='retry':d.evidence='Controlled drill'
            elif name=='dispatch':d.evidence='Public fixture'
            fn(d,index)
            art=Path('art')/name/(state['id']+'.svg');d.save(folder/art);state['artwork']=art.as_posix()
        path.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        if name=='overview':poster_hero()

if __name__=='__main__':build()
