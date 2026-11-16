#!/usr/bin/env python3
"""Draw the solar mechanisms from the versioned, measured illustration snapshot."""
from pathlib import Path
import json,math,argparse
from illustrate_inspection import SVG,C,tensor
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'visual-guides/solar'
def curve(s,x,y,w,h,values,color=None,lo=None,hi=None,width=2):
 lo=min(values) if lo is None else lo;hi=max(values) if hi is None else hi
 points=[(x+i*w/max(1,len(values)-1),y+h-(v-lo)/(hi-lo or 1)*h) for i,v in enumerate(values)];s.path('M'+' L'.join(f'{a:.2f} {b:.2f}' for a,b in points),color,width);return points

def mask_outline(s,x,y,w,values):
 d=[];cell=w/64
 for row in range(64):
  for col in range(64):
   if not values[(63-row)*64+col]:continue
   px,py=x+col*cell,y+row*cell
   for dr,dc,edge in [(-1,0,(px,py,px+cell,py)),(1,0,(px,py+cell,px+cell,py+cell)),(0,-1,(px,py,px,py+cell)),(0,1,(px+cell,py,px+cell,py+cell))]:
    rr,cc=row+dr,col+dc
    if not (0<=rr<64 and 0<=cc<64) or not values[(63-rr)*64+cc]:d.append('M%g %gL%g %g'%edge)
 s.path(' '.join(d),C['accent'],1.4)

def window(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Cut a forecast window at the observation time','60 observed one-minute samples enter; the XRS-B reading 30 minutes later stays outside.',f'{min(k+1,3):02}/03','Measured GOES-15 / 2014-02-01 • plotted values from the bundled observation snapshot')
 vals=e['history'][1]+e['future'];lo,hi=-5.8,-4.8;x0,y0,w,h=82,145,1000,260;s.line(x0,y0+h,x0+w,y0+h,arrow=True);s.line(x0,y0,x0,y0+h)
 for v in [-5.8,-5.4,-5.0]:
  y=y0+h-(v-lo)/(hi-lo)*h;s.line(x0,y,1100,y,C['line'],dash=True);s.text(68,y+6,str(v),18,mono=True,anchor='end')
 points=curve(s,x0,y0,w,h,vals,C['ink'],lo,hi);cut=x0+59/89*w;s.rect(x0,y0,cut-x0,h,'none',C['accent'],2);s.line(cut,125,cut,440,C['accent'],2,dash=True);s.text(82,121,'log10 XRS-B flux (W/m²)',20);s.text(cut,470,'t = 01:00',20,anchor='middle',weight=600);s.text(82,440,'00:01',18);s.text(1082,440,'01:30',18,anchor='end');s.text(250,470,'60 actual samples',22,weight=600)
 s.group(k>=1);last=e['preview']['latest_log10'];target=e['preview']['target_log10'];py=lambda v:y0+h-(v-lo)/(hi-lo)*h;s.line(cut,py(last),1082,py(last),C['blue'],2,dash=True);s.circle(1082,py(last),7,C['paper'],C['blue']);s.circle(1082,py(target),8,C['accent'],C['accent']);s.text(804,155,'Observed target −4.941',18,color=C['accent']);s.text(804,358,'Persistence −5.534',18,color=C['blue']);s.line(1130,py(last),1130,py(target),C['accent'],2);s.text(805,501,'Future target never enters the input.',20);s.end()
 s.group(k>=2);s.text(82,520,'Training-only scale:',20,weight=600);s.text(310,520,'(−5.534 − (−5.470)) / 0.276 = −0.233',19,mono=True);s.end()
 codes=['x = log10(flux[t-59:t+1])','persistence = log10_xrsb[t]; target = log10_xrsb[t+30]','x = (x - training_mean) / training_std'];s.strip(codes[min(k,2)],'A missing minute invalidates the window; no interpolated observation is inserted.');return s

def overview(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Follow one observation into a forecast experiment','A dated input, a baseline, an executed model, and the files that make the result recoverable.',f'{min(k+1,4):02}/04','Actual GOES window and AIA 171 Å frame • mechanism overview')
 s.image(32,139,270,270,e['aia_uris'][1]);s.text(32,449,'AIA 171 Å / 01:00',22,weight=600);s.text(32,479,'2014-02-01',18,mono=True);s.text(32,509,'64 × 64 measured image',18)
 s.text(350,125,'GOES: observation → future',22,weight=600);pts=curve(s,350,155,790,210,e['history'][1]+e['future'],C['ink']);s.line(350,375,1140,375);s.line(874,150,874,390,C['accent'],2,dash=True);s.text(874,421,'forecast origin',18,anchor='middle')
 s.group(k>=1);s.path(f'M874 {pts[59][1]} L1140 {pts[59][1]}',C['blue'],2);s.text(930,pts[59][1]-16,'copy current',18,color=C['blue']);s.end()
 s.group(k>=2);s.text(350,464,'Save one execution',22,weight=600)
 for j,name in enumerate(['candidate.py','weights.pt','predictions.npy']):
  x=350+j*267;s.path(f'M{x} 483 L{x+213} 483 L{x+231} 501 L{x+231} 537 L{x} 537 Z');s.path(f'M{x+213} 483 L{x+213} 501 L{x+231} 501');s.text(x+10,519,name,18,mono=True)
 s.end();s.group(k>=3);s.text(775,464,'Test each proposed source change',20,color=C['accent']);s.end();s.strip('same data + same scorer + recorded execution','Compare the model with persistence; retain failures and every tested seed.');return s

def shapes(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Two models receive the same 2 × 60 window','The MLP flattens time; the convolution reuses one width-five kernel at each time position.',f'{min(k+1,3):02}/03','Actual observed window • tensor geometry follows solar_candidate.py')
 s.text(32,123,'One example',22,weight=600)
 for j,name in enumerate(['XRS-A','XRS-B']):curve(s,32,158+j*90,330,64,e['history'][j],C['ink']);s.text(32,246+j*90,name,18)
 s.text(32,397,'2 channels × 60 minutes',20,mono=True);s.path('M363 230 L402 230 L402 166 L450 166',arrow=True);s.path('M402 230 L402 406 L450 406',arrow=True)
 s.group(k>=1);s.text(450,123,'MLP: learn separate weights',22,weight=600);tensor(s,450,145,495,60,e['history'][0]+e['history'][1],120);s.text(450,237,'flatten → 120 entries',18,mono=True);s.line(960,178,1010,178,arrow=True);tensor(s,1020,143,126,64,e['weights']['1.weight']['first64'],8);s.text(1020,239,'W: 16 × 120',18,mono=True);s.text(1020,277,'→ 1 value',20);s.text(450,277,'Every time position has its own input coefficient.',20);s.end()
 s.group(k>=2);s.text(450,353,'CNN: slide a shared kernel',22,weight=600)
 for j in range(2):
  for i in range(20):s.rect(450+i*24,382+j*27,24,25,C['panel'],C['line'],.7)
 s.rect(450+6*24,378,120,59,'none',C['accent'],3);s.path('M614 456 L854 456',C['accent'],2,arrow=True);s.text(450,496,'width 5; same learned kernel at every position',20);s.text(450,530,'20 of 60 time positions shown',18,color=C['muted']);s.text(1020,402,'pool time',20);s.line(966,407,1007,407,arrow=True);s.text(1020,439,'→ 1 value',20);s.end()
 s.strip(['x.shape == (batch, 2, 60)','Flatten → Linear(120, width) → Linear(width, 1)','Conv1d(2, width, 5, padding=2) → mean over time → Linear(width, 1)'][min(k,2)],'Both branches predict one XRS-B value per example; they are alternative implementations.');return s

def images(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Predict a correction to the current solar image','The same current image bypasses the network and is added to its predicted correction.',f'{min(k+1,3):02}/03','Actual AIA 171 Å frames / 2014-02-01 • shared log1p display scale')
 for x,i,label in [(32,0,'00:00 / t − 1 h'),(280,1,'01:00 / t'),(916,2,'02:00 / target')]:s.image(x,150,224,224,e['aia_uris'][i]);s.text(x,409,label,20,weight=600)
 s.text(32,120,'Observed pair: 2 × 64 × 64',22,weight=600);s.text(916,120,'Held-out future',22,weight=600)
 s.group(k>=1);s.path('M506 260 L550 260',arrow=True);s.text(557,218,'net(pair)',20,mono=True);s.rect(557,235,132,90,'none',C['ink']);s.lines(568,266,['Predicted','correction'],18);s.line(690,280,750,280,arrow=True);s.circle(782,280,28,C['paper']);s.text(782,289,'+',30,anchor='middle');s.path('M392 376 L392 463 L782 463 L782 310',C['accent'],2,arrow=True);s.text(485,492,'Unchanged current image',20,color=C['accent']);s.text(705,180,'Prediction',22,weight=600);s.text(719,356,'1 × 64 × 64',18,mono=True);s.end()
 s.group(k>=2);s.line(811,280,886,280,C['ink'],2,dash=True);s.text(834,250,'compare',18,anchor='middle');mask_outline(s,916,150,224,e['aia_mask']);s.text(916,459,'Mask keeps on-disk pixels',18);s.text(916,493,'MAE per image, then mean',18);s.end()
 s.strip(['pair = stack([image[t-1h], image[t]])','prediction = net(pair) + pair[:, 1:2]','error = (abs(prediction - target) * disk_mask).sum() / disk_mask.sum()'][min(k,2)],'The future target is scored after prediction; it is never an input frame.');return s

def learning(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('A falling training loss can still produce a bad forecast','Only the forecasting model is updated; the research agent’s weights remain fixed.',f'{min(k+1,4):02}/04','Recorded GOES / matched training and final weights • blue < 0, orange > 0')
 s.text(32,127,'Prediction − target',22,weight=600);s.lines(32,173,['squared error','× valid mask','÷ valid count'],24);s.path('M252 211 L315 211',arrow=True)
 s.group(k>=1);s.text(340,127,'Forecast weight array',22,weight=600);tensor(s,340,147,280,224,e['weights']['1.weight']['first64'],8);s.text(340,407,'64 saved coefficients shown',18);s.text(340,438,'from W[16, 120]',18,mono=True);s.path('M390 473 C300 473 300 305 330 305',C['accent'],2,arrow=True);s.text(32,461,'loss.backward()',20,mono=True);s.text(32,493,'optimizer.step()',20,mono=True);s.end()
 s.group(k>=2);s.text(686,127,'Training loss / 60 steps',22,weight=600);loss=e['losses'];loss=loss.get('losses',[]) if isinstance(loss,dict) else loss;curve(s,686,158,450,175,loss,C['ink']);s.line(686,333,1136,333);s.text(686,365,'1',18);s.text(1136,365,'60',18,anchor='end');s.end()
 s.group(k>=3);s.text(686,415,'Final error / lower is better',22,weight=600)
 for y,label,value,color in [(450,'Historical',2.468975,C['accent']),(496,'Persistence',.192706,C['blue'])]:
  s.text(686,y+14,label,18);s.rect(816,y,240*value/2.5,22,color,color);s.text(1158,y+18,f'{value:.6f}',18,mono=True,anchor='end')
 s.end();s.strip(['loss = ((prediction - target).square() * mask).sum() / mask.sum()','optimizer.zero_grad(); loss.backward(); optimizer.step()','model.eval(); score(validation_predictions, unchanged_validation_target)','historical_error = 2.468975; persistence_error = 0.192706'][min(k,3)],'The historical final forecast lost to persistence; training loss does not establish useful prediction.');return s

def research(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Test the proposed source, then select one branch','Round two keeps data, 40 training steps, and seed 17 fixed. Lower validation error is better.',f'{min(k+1,4):02}/04','Recorded research candidates • separate fixed-recipe seed outcomes retained below')
 s.text(32,124,'Parent: masked L1 loss',22,weight=600);s.path('M32 145 L270 145 L290 165 L290 280 L32 280 Z');s.text(48,190,'abs(pred − target)',18,mono=True);s.text(48,222,'× disk_mask',18,mono=True);s.text(48,257,'0.120553',24,mono=True);s.path('M290 210 L328 210 L328 168 L365 168',C['blue'],arrow=True);s.path('M328 210 L328 360 L365 360',C['accent'],arrow=True)
 s.group(k>=1);s.text(365,124,'A  Zero final convolution',22,weight=600,color=C['blue'])
 for j in range(3):
  for i in range(3):s.rect(365+i*43,145+j*43,43,43,'#ffffff',C['line']);s.text(386+i*43,173+j*43,'0',18,mono=True,anchor='middle')
 s.lines(523,175,['weight = 0; bias = 0','Starts at persistence','then learns a correction'],20);s.text(365,300,'one 3 × 3 kernel',18);s.text(1000,205,'0.110916',27,mono=True,color=C['blue']);s.end()
 s.group(k>=2);s.text(365,326,'B  Sample without replacement',22,weight=600,color=C['accent'])
 for i in range(8):s.rect(365+i*41,352,34,48,C['panel'],C['line']);s.text(382+i*41,383,['e','b','h','a','f','c','g','d'][i],18,mono=True,anchor='middle')
 s.text(365,438,'Illustrative order: no case is drawn twice.',20);s.text(1000,382,'0.120557',27,mono=True,color=C['accent']);s.end()
 s.group(k>=3);s.path('M1000 228 L1000 273 L1150 273',C['blue'],2,arrow=True);s.text(1148,304,'Select A',22,anchor='end',weight=600,color=C['blue']);s.text(1148,436,'A + B was not tested',20,anchor='end');s.end()
 s.line(32,470,1168,470);s.text(32,503,'Fixed zero-residual recipe, final seeds:',20,weight=600)
 rows=[r for r in e['qualification']['rows'] if r['task']=='images' and r['recipe']=='zero_residual']
 for i,r in enumerate(rows):s.text(580+i*195,503,f'{r["seed"]}: {r["error"]:.6f}',18,mono=True)
 s.strip('nn.init.zeros_(net[-1].weight); nn.init.zeros_(net[-1].bias)','A branch is a tested source change. A selection does not claim an unexecuted combination.');return s

def run_record(spec,state,e):
 k=[a['id'] for a in spec['states']].index(state['id']);s=SVG('Recover the files from the same executed experiment','Source, settings, data identity, weights, and predictions must refer to one execution.',f'{min(k+1,3):02}/03','Recorded source fingerprint and saved weight samples • local illustration snapshot')
 s.text(32,126,'Inputs',22,weight=600)
 for i,label in enumerate(['candidate.py','config.json','dataset ID']):
  x=32+i*180;s.path(f'M{x} 148 L{x+130} 148 L{x+149} 167 L{x+149} 292 L{x} 292 Z');s.path(f'M{x+130} 148 L{x+130} 167 L{x+149} 167');s.text(x+8,205,label,16,mono=True)
  for j in range(3):s.line(x+12,232+j*15,x+127,232+j*15,C['line'])
 s.lines(32,343,['source fingerprint',e['weight_source_fingerprint'][:24]+'…'],18,mono=True);s.text(32,414,'seed 17 · 60 steps · width 16',20)
 s.group(k>=1);s.line(557,220,625,220,arrow=True);s.text(654,126,'Outputs from that execution',22,weight=600);tensor(s,654,150,185,147,e['weights']['1.weight']['first64'],8);s.text(654,334,'weights.pt',20,mono=True);curve(s,900,151,236,146,e['losses'],C['ink']);s.text(900,334,'losses.json',20,mono=True);s.text(654,414,'predictions.npy',20,mono=True);s.text(654,446,'Same model, same split, preserved order',20);s.end()
 s.group(k>=2);s.path('M654 476 L654 522 L1135 522 L1135 476');s.text(896,514,'one execution artifact',20,anchor='middle',weight=600);s.end()
 s.strip('save(source, config, dataset_id, weights, predictions, losses)','A later notebook variable does not replace the outputs of the recorded execution.');return s
DRAW={'overview':overview,'window':window,'model-shapes':shapes,'images':images,'learning':learning,'research':research,'run-record':run_record}
def hero(e):
 s=SVG('Observe, forecast, and recover the experiment','Actual AIA and GOES observations from 2014-02-01.');s.a=s.a[:1]
 s.text(32,45,'1  Observe',30,weight=600);s.image(32,90,280,280,e['aia_uris'][1]);s.text(32,421,'AIA 171 Å / 01:00',26);s.text(32,459,'2014-02-01',23,mono=True)
 s.text(350,45,'2  Forecast',30,weight=600);pts=curve(s,350,115,470,240,e['history'][1]+e['future'],C['ink']);cut=350+470*59/89;s.line(350,369,820,369);s.line(cut,88,cut,385,C['accent'],2,dash=True);s.line(cut,pts[59][1],820,pts[59][1],C['blue'],2,dash=True);s.circle(820,pts[-1][1],8,C['accent'],C['accent']);s.text(350,421,'60 samples',26);s.text(820,421,'+30 min',26,anchor='end');s.text(350,459,'Keep the target outside the input.',24)
 s.text(894,45,'3  Recover',30,weight=600)
 for off in [24,12,0]:s.path(f'M{894+off} {112-off} L{1109+off} {112-off} L{1135+off} {138-off} L{1135+off} {370-off} L{894+off} {370-off} Z')
 s.lines(914,170,['Source / data','Settings','Weights','Predictions'],26);s.text(894,421,'One execution',26);s.text(894,459,'Linked files',24)
 s.text(32,527,'Keep the dated observations, source, weights, and predictions together.',28)
 return s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only');args=ap.parse_args();e=json.loads((OUT/'art/evidence.json').read_text(encoding='utf-8'))
 if not args.only:
  h=hero(e);h.save(OUT/'hero.svg');hp=OUT/'hero.svg';hp.write_text(hp.read_text(encoding='utf-8').replace('viewBox="0 0 1200 675"','viewBox="0 0 1200 560"'),encoding='utf-8')
 for p in OUT.glob('*.json'):
  if p.stem not in DRAW or (args.only and args.only!=p.stem):continue
  spec=json.loads(p.read_text(encoding='utf-8'))
  for state in spec['states']:
   rel=f'art/{p.stem}/{state["id"]}.svg';DRAW[p.stem](spec,state,e).save(OUT/rel);state['artwork']=rel
  p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
