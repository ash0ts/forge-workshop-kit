"""Original operational illustrations for the Transit teaching guides."""
from pathlib import Path
import json
from illustrate_pending import Drawing,PosterDrawing,ROOT,P,I,M,L,A,BLUE

def board(d,x,y,w=550):
    d.rect(x,y,w,235,fill='#fff',width=2)
    d.rect(x,y,w,51,fill=I)
    d.text(x+18,y+34,'PARK STREET / historical schedule',21,color=P,weight=600)
    d.text(x+18,y+90,'trip         departure          service day',16,mono=True,color=M)
    d.line(x+14,y+105,x+w-14,y+105,color=L)
    d.text(x+18,y+142,'63926435     00:08 Nov 29        Nov 28',16,mono=True)
    d.line(x+14,y+161,x+w-14,y+161,color=L)
    d.text(x+18,y+196,'GTFS 24:08:00  /  America/New_York',16,mono=True)
    d.text(x+18,y+220,'Frozen 2024 feed; not live arrivals',16,color=M)

def overview(d,k):
    d.text(45,124,'MBTA GTFS / frozen source',18,weight=600)
    for y,label in [(148,'stop_times'),(194,'trips'),(240,'calendar + exceptions')]:
        d.path(f'M45 {y} H300 V{y+34} H45 Z',fill='#fff')
        d.text(58,y+24,label,17,mono=True)
    d.path('M170 274 V314 H343',arrow=True)
    d.group(k>=1)
    d.text(45,363,'Two owned source files',20,weight=600)
    for x,y,file,color in [(45,389,'query.py',BLUE),(45,472,'presentation.py',A)]:
        d.rect(x,y,262,56,fill='#fff',stroke=color,width=2)
        d.text(x+16,y+24,file,20,mono=True)
        for n in range(3):d.line(x+17+n*75,y+42,x+67+n*75,y+42,color=color)
    d.path('M307 418 H348 V317 H396',arrow=True)
    d.path('M307 500 H368 V336 H396',arrow=True)
    d.text(316,293,'join',18)
    d.end()
    d.group(k>=2)
    board(d,396,150,752)
    d.call(1,1080,433,1080,290)
    d.lines(712,432,['After midnight, the civil date changes.','The GTFS service date stays November 28.'],18,leading=29)
    d.end()
    d.group(k>=3)
    d.path('M560 385 V507 H812',arrow=True,dash='6 5')
    d.text(416,532,'Save the checked lesson',18)
    d.path('M812 483 H1148 V546 H812 Z',fill='#e8e9e3')
    d.text(830,510,'Next build: with / without memory',18)
    d.text(830,536,'same task + allowance',16,mono=True)
    d.end()
    d.footer('query.departures(stop_id, at) → presentation.render_board(departures)','Coordinate ownership, test the assembled board, then measure whether a checked lesson helps.')

def service_time(d,k):
    d.text(46,120,'FOLLOW ONE DEPARTURE',16,mono=True)
    for x,w,title,values in [(46,290,'stop_times',['trip_id: 63926435','stop_id: 70076','departure: 24:08:00']),(426,280,'trips',['trip_id: 63926435','route_id → route','service_id → calendar']),(790,362,'service calendar',['service_date: 2024-11-28','active service + exceptions'])]:
        d.sheet(x,140,w,163,title,k==0)
        d.lines(x+16,213,values,16,leading=31,mono=True)
    d.path('M336 212 H426',arrow=True)
    d.path('M706 274 H747 V212 H790',arrow=True)
    d.group(k>=1)
    d.text(46,350,'GTFS hours are elapsed time from service-day midnight',22,weight=600)
    d.line(70,427,824,427,width=2);d.path('M824 419 L834 435 L844 419 L854 435',width=2);d.line(854,427,1115,427,width=2)
    for x,label in [(70,'Nov 28 / 00:00'),(890,'Nov 29 / 00:00'),(1115,'00:08')]:
        d.line(x,414,x,441,width=2);d.text(x,465,label,18,anchor='middle' if x==890 else ('end' if x==1115 else 'start'))
    d.path('M70 405 V389 H812 V405 M890 405 V389 H1115 V405',color=A,width=2)
    d.text(450,382,'24 hours',24,weight=600,anchor='middle');d.text(1000,382,'8 minutes',21,weight=600,anchor='middle')
    d.dot(1115,427,7,A)
    d.text(450,466,'compressed day',16,color=M,anchor='middle')
    d.end()
    d.group(k>=2)
    d.text(46,523,'service_date',16,mono=True,color=M);d.text(201,523,'2024-11-28',20,mono=True)
    d.text(533,523,'departure_time',16,mono=True,color=M);d.text(706,523,'2024-11-29T00:08:00-05:00',18,mono=True)
    d.end()
    d.footer('departure = midnight + timedelta(hours=h, minutes=m, seconds=s)','At 00:05 on November 29, this 00:08 train still belongs to November 28 service.')

def worker(d,k):
    d.text(44,122,'ASSIGNED SOURCE / query.py',18,weight=600)
    d.path('M44 146 H414 V361 H44 Z',fill='#fff')
    for n,(label,text) in enumerate([('01','task: implement query'),('02','contract: departures(...)'),('03','source: current query.py'),('04','lessons: selected records')]):
        d.text(58,186+n*43,label,16,mono=True,color=M);d.text(97,186+n*43,text,16,mono=True)
    d.group(k>=1)
    d.text(480,122,'ALLOWED TOOL SLOTS',16,mono=True)
    for n,name in enumerate(['read_file','write_file','run_tests','read_memory','send_message','finish']):
        y=143+n*45;d.rect(479,y,230,38,fill='#fff',stroke=A if n==0 else L,width=2 if n==0 else 1)
        d.dot(491,y+19,4,A if n==0 else L);d.text(508,y+26,name,18,mono=True)
    d.path('M414 216 H450 V162 H479',arrow=True)
    d.text(50,402,'selected read_file action',18)
    d.text(50,435,'path: "query.py"',19,mono=True)
    d.path('M414 435 H450 V162 H479',arrow=True)
    d.end()
    d.group(k>=2)
    d.text(765,122,'NEXT REQUEST / turn history',18,weight=600)
    d.rect(763,143,390,294,fill='#fff')
    for y,role,value in [(180,'system','assigned feature only'),(234,'user','task + source + lessons'),(288,'assistant','read_file(query.py)'),(342,'user','actual source + hash')]:
        d.text(781,y,role,16,mono=True,color=M);d.text(781,y+26,value,18,mono=True);d.line(764,y+39,1152,y+39,color=L)
    d.path('M709 163 H741 V364 H763',arrow=True)
    d.end()
    d.group(k>=3)
    d.path('M950 437 V477 H724',arrow=True)
    d.text(48,512,'PATCH',18,mono=True);d.text(145,512,'changed source + tests + worker identity',20)
    d.text(778,512,'submitted ≠ integrated',22,weight=600)
    d.end()
    d.footer('name = action["action"]; return tools[name](action)','Return each tool observation to the worker; review and integrate its patch separately.')

def claims(d,k):
    d.text(47,121,'CONTROLLED CLAIM DRILL',16,mono=True)
    for x,label in [(130,'Worker 1'),(600,'Task board'),(1070,'Worker 2')]:
        d.text(x,163,label,22,weight=600,anchor='middle');d.line(x,181,x,433,color=L,width=2)
    d.path('M130 217 H584',arrow=True);d.text(230,204,'read: owner=None',18,mono=True)
    d.path('M1070 247 H616',arrow=True);d.text(740,234,'read: owner=None',18,mono=True)
    d.text(452,283,'Both reads can see an unclaimed task.',18)
    d.group(k>=1)
    d.rect(565,304,70,100,fill='#e8e9e3',stroke=A,width=2)
    d.path('M130 325 H565',arrow=True);d.text(207,315,'claim(query, worker-1)',16,mono=True)
    d.path('M1070 383 H635',arrow=True);d.text(747,372,'claim(query, worker-2)',16,mono=True)
    d.text(157,369,'owner = worker-1',19,mono=True)
    d.text(760,423,'cannot acquire same claim',18)
    d.text(484,454,'atomic ownership update',18,weight=600)
    d.end()
    d.group(k>=2)
    d.text(47,508,'Dependencies',20,weight=600)
    d.text(241,508,'submitted',18,mono=True,color=M)
    d.path('M367 502 H480',dash='5 5');d.line(442,489,442,515,color=A,width=4)
    d.text(498,508,'integrated',18,mono=True)
    d.path('M636 502 H768',arrow=True)
    d.text(787,508,'dependent task becomes ready',18)
    d.end()
    d.footer('return board.claim(task_id, worker_id)','Read-then-write can race. Claim atomically; unblock dependencies only after integration.')

def integration(d,k):
    d.text(47,112,'contract.md / both copies share the same interface',19,weight=600)
    for x,w,file,owner,color in [(47,510,'query.py','Query worker owns this file',BLUE),(645,507,'presentation.py','Presentation worker owns this file',A)]:
        d.rect(x,147,w,210,fill='#fff',stroke=color,width=2)
        d.rect(x,147,52,210,fill='#e8e9e3',stroke=L)
        d.text(x+68,178,file,22,mono=True)
        d.text(x+68,208,owner,18)
        d.line(x+52,222,x+w,222,color=L)
        for n,y in enumerate([251,284,317]):d.text(x+13,y,f'{n+1:02d}',16,mono=True,color=M)
    d.group(k>=1)
    d.lines(114,251,['def departures(...):','  for shift in (-1, 0, 1):','    # inspect service days'],16,leading=33,mono=True)
    d.lines(712,251,['def render_board(rows, ...):','  escape(str(row["headsign"]))','  # render escaped HTML'],16,leading=33,mono=True)
    d.text(47,137,'Abbreviated source; returned patch and tests remain attached to the submission.',16)
    d.end()
    d.group(k>=2)
    d.path('M300 357 V422',arrow=True)
    d.rect(47,428,609,118,fill='#fff')
    d.text(65,458,'Interface record / one departure',18,weight=600)
    d.text(65,492,'trip_id       service_date    departure_time',16,mono=True,color=M)
    d.text(65,524,'63926435      2024-11-28      Nov 29 00:08 -05:00',16,mono=True)
    d.path('M656 474 H695 V407 H900 V357',arrow=True)
    d.path('M1152 310 H1171 V485 H1147',arrow=True)
    d.rect(740,428,407,118,fill='#e8e9e3',width=2)
    d.text(761,461,'PARK STREET',20,weight=600)
    d.text(761,498,'00:08 / November 29',23,mono=True)
    d.text(761,532,'Check dates, order and interface.',18)
    d.end()
    d.footer('status="integrated", reviewer=reviewer, reviewed_patch=expected_patch_digest','Review the submitted patch, test the combined application, and record the exact integrated source.')

def memory(d,k):
    d.text(47,120,'THREE COLLECTIONS / different responsibilities',18,weight=600)
    for y,title,body in [(149,'tasks','owner / status / dependencies'),(236,'contracts','interfaces / allowed paths'),(323,'lessons','checked experience + evidence')]:
        d.path(f'M47 {y+12} H65 V{y} H169 L183 {y+12} H410 V{y+71} H47 Z',fill='#e8e9e3')
        d.text(66,y+37,title,22,weight=600);d.text(66,y+60,body,16,mono=True)
    d.group(k>=1)
    d.path('M410 365 H455',arrow=True)
    d.text(466,141,'LESSON INDEX / practice fixture',18,weight=600)
    d.text(466,181,'id         status    version   tag',16,mono=True,color=M)
    for n,(name,status,version,tag) in enumerate([('checked','accepted','r1','time'),('guess','proposed','r1','time'),('stale','accepted','r0','time'),('unrelated','accepted','r1','colors')]):
        y=218+n*49
        d.rect(455,y-25,695,41,fill='#fff',stroke=A if n==0 else L,width=2 if n==0 else 1)
        d.text(471,y,f'{name:10} {status:9} {version:8} {tag}',16,mono=True,color=I if n==0 else M)
        d.text(1005,y,'select' if n==0 else 'exclude',18,weight=600 if n==0 else 400)
        if n>0:d.line(981,y-12,995,y+2,color=M)
    d.text(468,429,'required: accepted · transit · r1 · matching tag',18)
    d.end()
    d.group(k>=2)
    d.path('M1150 218 H1170 V455 H748 V466',arrow=True)
    d.rect(455,473,695,70,fill='#fff',stroke=A,width=2)
    d.text(473,500,'NEXT WORKER REQUEST / selected lesson',16,mono=True)
    d.text(473,529,'“Keep hours above 24” + its checked source record',20)
    d.end()
    d.footer('accepted and scope == "transit" and version == "r1" and set(tags) & {"time"}','Retrieval proves the worker read the lesson. Application results establish whether it helped.')

def marks(d,x,y,total,passed,visible,color=I):
    for i in range(total):
        xx=x+(i%9)*36;yy=y+(i//9)*36
        d.rect(xx,yy,23,23,fill=color if visible and i<passed else '#fff',stroke=I)
        if visible and i>=passed:d.path(f'M{xx+5} {yy+5} L{xx+18} {yy+18} M{xx+18} {yy+5} L{xx+5} {yy+18}',width=1.5)

def comparison(d,k):
    d.text(47,125,'Match task · data · model · cases · total request allowance',22,weight=600)
    d.text(47,163,'Include planning, integration and retries in the allowance.',18)
    d.line(47,186,1153,186,color=L)
    d.text(47,225,'RECORDED BUILD',16,mono=True)
    d.text(47,266,'Solo',22);marks(d,240,244,10,10,k>=1)
    d.text(623,266,'10 / 10' if k>=1 else 'results hidden',24,mono=True)
    d.text(47,345,'Team',22);marks(d,240,323,10,8,k>=1)
    d.text(623,345,'8 / 10' if k>=1 else 'results hidden',24,mono=True)
    if k>=1:
        d.path('M545 335 H583 V291 H851',arrow=True,dash='6 5')
        d.lines(866,282,['Two failing checks.','One UTC defect.'],20,leading=29)
    d.line(47,393,1153,393,color=L)
    d.text(47,428,'FOLLOW-UP BUILD',16,mono=True)
    d.text(47,467,'Without memory',20);marks(d,240,444,18,12,k>=2)
    d.text(47,541,'With memory',20);marks(d,240,508,18,12,k>=2)
    d.text(623,470,'12 / 18' if k>=2 else 'results hidden',24,mono=True)
    d.text(623,544,'12 / 18' if k>=2 else 'results hidden',24,mono=True)
    if k>=3:
        d.text(866,455,'RELEASE GATE',16,mono=True)
        d.lines(866,488,['Available results?','All passed?', 'Otherwise retain.'],20,leading=28)
    if k == 0:
        caption = 'Compare solo and team builds, then compare the follow-up builds with and without memory.'
    elif k == 1:
        caption = 'The solo build passed 10/10 checks; the team passed 8/10. Inspect the two failed checks.'
    else:
        caption = 'Team 8/10 versus solo 10/10; both follow-up builds scored 12/18.'
    d.footer('bool(rows) and all(row.get("passed") is True for row in rows)', caption)


def poster_hero():
    d=PosterDrawing('A GTFS departure crosses two owned files into one board',
        'Frozen historical MBTA record: trip 63926435 at stop 70076 departs at GTFS time 24:08:00. The query worker resolves the service day, and the presentation worker renders the shared departure record. Park Street shows 00:08 on November 29, 2024 while service_date remains November 28, 2024 in America/New_York.')
    # Exact GTFS fields, with the service date resolved by the query implementation.
    d.path('M22 58H306L330 82V367H22Z',fill='#fff',width=2)
    d.path('M306 58V82H330',color=L)
    d.text(42,103,'stop_times.txt',27,mono=True,weight=600)
    d.line(22,123,330,123,color=L)
    d.text(42,162,'trip 63926435',26,mono=True)
    d.text(42,207,'stop 70076',26,mono=True)
    d.text(42,261,'departure',24,color=M)
    d.text(42,308,'24:08:00',38,mono=True,weight=600)
    d.text(42,348,'GTFS elapsed hours',24)
    d.text(22,409,'Frozen MBTA feed',26,weight=600)
    # These are source documents with separate owners, joined by the shared row contract.
    for y,file,owner,behavior,color in [(40,'query.py','Query worker','Resolve service day',BLUE),(251,'presentation.py','Display worker','Escape + render rows',A)]:
        d.path(f'M391 {y}H706L730 {y+24}V{y+160}H391Z',fill='#fff',color=color,width=2)
        d.path(f'M706 {y}V{y+24}H730',color=color)
        d.text(410,y+41,file,27,mono=True,weight=600)
        d.line(391,y+58,730,y+58,color=L)
        d.text(410,y+96,owner,24,color=M)
        d.text(410,y+137,behavior,26,weight=600)
    d.path('M330 173H360V119H389',arrow=True,width=2)
    d.path('M560 200V249',arrow=True,width=2)
    d.text(580,235,'shared row',24)
    d.path('M730 330H758V217H786',arrow=True,width=2)
    # The assembled output exposes civil time and the distinct service date together.
    d.rect(788,58,390,353,fill='#fff',width=2)
    d.rect(788,58,390,64,fill=I)
    d.text(809,102,'PARK STREET',30,color=P,weight=600)
    d.text(809,163,'Civil departure',24,color=M)
    d.text(809,220,'00:08',48,mono=True,weight=600)
    d.text(809,265,'Nov 29, 2024',29,mono=True)
    d.line(802,285,1164,285,color=L)
    d.text(809,323,'Service: Nov 28, 2024',26,weight=600)
    d.text(809,371,'America/New_York',24,mono=True)
    d.save(ROOT/'visual-guides/transit/hero.svg')


def build():
    folder=ROOT/'visual-guides/transit'
    functions={'overview':overview,'service-time':service_time,'worker':worker,'claims':claims,'integration':integration,'memory':memory,'comparison':comparison}
    for name,fn in functions.items():
        path=folder/(name+'.json');spec=json.loads(path.read_text(encoding='utf-8'))
        for index,state in enumerate(spec['states']):
            d=Drawing(spec['title'],'Transit / '+name,state,index,len(spec['states']))
            if name=='comparison':d.evidence='Recorded scores'
            elif name=='service-time':d.evidence='Public data'
            elif name in ('claims','memory'):d.evidence='Controlled drill'
            fn(d,index)
            art=Path('art')/name/(state['id']+'.svg');d.save(folder/art);state['artwork']=art.as_posix()
        path.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        if name=='overview':poster_hero()

if __name__=='__main__':build()
