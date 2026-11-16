#!/usr/bin/env python3
"""Generate original PCB mechanism drawings from versioned measured snapshots."""
from pathlib import Path
import base64,json,html,math,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'visual-guides/inspection'
C=json.loads((ROOT/'skills/teenage-engineering-visualizations/assets/tokens.json').read_text(encoding='utf-8'))['colors']
C['blue']=C['candidate_a']
def esc(v):return html.escape(str(v),quote=True)
class SVG:
 def __init__(self,title,subtitle='',state='',provenance='Illustrative mechanism'):
  self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675"><title>{esc(title)}</title><desc>{esc(subtitle)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="context-stroke" stroke-width="1.4"/></marker></defs><rect width="1200" height="675" fill="{C["paper"]}"/>']
  self.text(32,38,title,30,weight=600);self.text(32,70,subtitle,18,color=C['muted'])
  self.line(32,86,1168,86,color=C['ink']);self.text(32,657,provenance,18,color=C['muted'])
 def add(self,s):self.a.append(s)
 def text(self,x,y,s,size=18,color=None,weight=400,mono=False,anchor='start'):
  self.add(f'<text x="{x}" y="{y}" font-family="IBM Plex {"Mono" if mono else "Sans"}" font-size="{size}" font-weight="{weight}" fill="{color or C["ink"]}" text-anchor="{anchor}">{esc(s)}</text>')
 def lines(self,x,y,ss,size=18,**kw):
  for i,s in enumerate(ss):self.text(x,y+i*(size+6),s,size,**kw)
 def line(self,x,y,x2,y2,color=None,width=1.6,dash=False,arrow=False):self.add(f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{color or C["ink"]}" stroke-width="{width}"'+(' stroke-dasharray="5 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def path(self,d,color=None,width=1.6,arrow=False):self.add(f'<path d="{d}" fill="none" stroke="{color or C["ink"]}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def rect(self,x,y,w,h,fill='none',stroke=None,width=1.5):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke or C["ink"]}" stroke-width="{width}"/>')
 def circle(self,x,y,r,fill='none',stroke=None):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or C["ink"]}" stroke-width="1.6"/>')
 def image(self,x,y,w,h,uri,crop=None):
  if crop:
   self.add(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{crop}" preserveAspectRatio="none"><image width="1" height="1" href="{uri}" preserveAspectRatio="none"/></svg>')
  else:self.add(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri}" preserveAspectRatio="none"/>')
 def group(self,active=True):self.add(f'<g opacity="{1 if active else .18}">')
 def end(self):self.add('</g>')
 def grid(self,x,y,w,h,n=14,m=14,values=None,selected=None):
  for j in range(m):
   for i in range(n):
    v=values[j*n+i] if values is not None else None
    fill=('#%02x%02x%02x'%(244-int(v*8),243-int(v*152),239-int(v*199))) if v is not None else 'none'
    self.rect(x+i*w/n,y+j*h/m,w/n,h/m,fill,C['line'],.7)
  if selected is not None:self.rect(x+selected[1]*w/n,y+selected[0]*h/m,w/n,h/m,'none',C['accent'],3)
 def strip(self,code,effect):
  self.line(32,552,1168,552);self.rect(32,568,1136,54,C['panel'],C['panel']);self.text(48,591,code,16,mono=True);self.text(48,615,effect,18,weight=500)
 def save(self,path):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(self.a)+'</svg>',encoding='utf-8',newline='\n')
def uri(p):return 'data:image/'+('jpeg' if p.suffix.lower() in ('.jpg','.jpeg') else 'png')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def evidence():
 return json.loads((OUT/'art/evidence.json').read_text(encoding='utf-8'))

def patch(spec,state,e):
 ids=[s['id'] for s in spec['states']];k=ids.index(state['id']);r,c=e['position'];s=SVG('Measure a patch against normal boards','Same location, 64 channels; supplied defect masks never enter the calculation.',f'{min(k+1,4):02}/04','Actual PCB1 / extracted frozen features • geometry of one recorded board')
 s.text(32,120,'1  Locate the query',22,weight=600);s.image(32,140,280,280,e['query_uri']);s.grid(32,140,280,280,selected=(r,c));s.text(32,448,'PCB1 anomaly 048',20,weight=600);s.text(32,476,f'Patch [{r}, {c}] of 14 × 14',18,mono=True)
 px=32+(c+.5)*20;py=140+(r+.5)*20;s.path(f'M{px} {py} L332 {py} L348 206',C['accent'],2)
 s.image(348,145,132,132,e['query_uri'],f'{(c-1)/14} {(r-1)/14} {3/14} {3/14}');s.rect(348,145,132,132,'none',C['accent'],2);s.rect(392,189,44,44,'none',C['accent'],2);s.text(348,303,'Query: 3 × 3 context',18)
 s.group(k>=1);s.text(518,120,'2  Scale each channel',22,weight=600)
 s.text(520,164,'q',20,mono=True,color=C['accent']);s.text(520,211,'b',20,mono=True,color=C['blue']);s.text(520,258,'σ',20,mono=True)
 for j in range(4):
  x=550+j*96
  for row,key in enumerate(['query_vector','reference_vector','scale']):
   s.rect(x,140+row*47,90,36,'#ffffff',C['line']);s.text(x+45,164+row*47,f'{e[key][j]:.3f}',16,mono=True,anchor='middle')
 s.text(946,165,'… 64',18,mono=True);s.text(946,212,'… 64',18,mono=True);s.text(946,259,'… 64',18,mono=True)
 s.text(550,302,'σ = max(normal-bank std, 0.1)',18,mono=True);s.end()
 s.image(348,346,132,132,e['reference_uri'],f'{(c-1)/14} {(r-1)/14} {3/14} {3/14}');s.rect(348,346,132,132,'none',C['blue'],2);s.rect(392,390,44,44,'none',C['blue'],2);s.text(348,507,'Normal: same area',18)
 s.group(k>=2);s.text(520,350,'3  Compare; keep the nearest',22,weight=600);s.lines(550,388,['mean((q / σ − b / σ)²)',f'{e["normal_count"]} normal fitting references',f'nearest: {e["reference"]}'],18,mono=True);s.text(550,476,f'd = {e["distance"]:.4f}',28,weight=600,color=C['accent']);s.end()
 s.group(k>=3);s.text(1008,350,'4  Place back',20,weight=600);vals=e['distance_map'];mx=max(vals);s.text(1008,379,f'0 → {mx:.3f}',16,mono=True);s.grid(1008,390,128,128,values=[v/mx for v in vals],selected=(r,c));s.text(1008,542,'196 distances',18);s.end()
 codes=['q = patches[board, row, col]','scale = maximum(bank.std(axis=0), 0.1)','distance = mean((query / scale - reference / scale) ** 2)','features = log1p(distances).reshape(196)'];effects=['Enlarge the same spatial cell; each patch has 64 learned features.','Apply the same channel scale to the query and every normal reference.','Select the smallest distance at this location; exclude the query’s own bank row.','Repeat independently at every location and preserve the 14 × 14 spatial order.'];s.strip(codes[min(k,3)],effects[min(k,3)]);return s

def tensor(s,x,y,w,h,values,n=16,color=None):
 vals=list(values);rows=math.ceil(len(vals)/n);cellw=w/n;cellh=h/rows;mx=max(abs(v) for v in vals) or 1
 for j,v in enumerate(vals):
  amount=min(abs(v)/mx,1);base=(36,108,172) if v<0 else (236,91,40);rgb=tuple(round(244*(1-amount)+b*amount) for b in base);s.rect(x+(j%n)*cellw,y+(j//n)*cellh,cellw,cellh,'#%02x%02x%02x'%rgb,C['paper'],.4)
 s.rect(x,y,w,h,'none',C['ink'])
def score_axis(s,x,y,w,score,cutoff,title):
 lo,hi=-1.6,.1;px=lambda v:x+(v-lo)/(hi-lo)*w
 s.text(x,y-52,title,20,weight=600);s.line(x,y,x+w,y);s.line(px(cutoff),y-35,px(cutoff),y+35,C['ink'],2,dash=True);s.circle(px(score),y,8,C['accent'],C['accent']);s.text(px(score),y+58,f'{score:.3f}',18,mono=True,anchor='middle',color=C['accent']);s.text(px(cutoff)+14,y-15,f'cut {cutoff:.3f}',18,mono=True)
def representations(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('One photograph, two aligned feature sets','The enriched representation retains the original 512 values and appends 196 local distances.',f'{min(k+1,4):02}/04','Actual photograph and feature values • arrays shown with compressed dimensions')
 s.image(32,163,224,224,e['query_uri']);s.grid(32,163,224,224,selected=e['position']);s.text(32,419,'PCB1 anomaly 048',20,weight=600);s.lines(32,451,['One frozen encoder','Masks: inspection only'],18)
 s.path('M256 275 L302 275 L302 177 L350 177',arrow=True);s.path('M302 275 L302 414 L350 414',arrow=True);s.text(32,132,'Shared RGB image',18)
 s.group(k>=1);s.text(350,124,'Whole-image output',22,weight=600);tensor(s,350,149,500,72,e['whole'],64);s.text(350,251,'512 values',20,mono=True);s.text(880,177,'Baseline',22,weight=600);s.text(880,206,'uses all 512',20);s.line(850,185,866,185,arrow=True);s.end()
 s.group(k>=2);s.text(350,321,'Separate patch output',22,weight=600)
 for offset in [16,8,0]:s.grid(350+offset,347-offset,150,150)
 s.text(350,530,'14 × 14 × 64',20,mono=True);s.line(525,414,584,414,arrow=True);s.lines(598,280,['Normal bank','distances + log1p'],18);mx=max(e['distance_map']);s.grid(598,347,150,150,values=[v/mx for v in e['distance_map']]);s.text(598,530,'196 local',20,mono=True);s.end()
 s.group(k>=3);s.path('M820 222 L820 319 L894 319',arrow=True);s.path('M750 423 L820 423 L820 364 L894 364',C['accent'],arrow=True)
 tensor(s,896,295,272,48,e['whole'],64);tensor(s,896,349,272,55,e['distance_map'],28);s.text(896,443,'Enriched: 708',24,weight=600);s.lines(896,475,['512 unchanged','+ 196 local'],20);s.end()
 s.strip(['whole, patches = encoder(image)','baseline = whole','local = log1p(nearest_patch_distances)','enriched = concatenate([whole, local])'][min(k,3)],['Preserve the board identity across both arrays.','Keep the whole-image baseline as the comparison.','Use normal fitting references independently at each location.','Compare the same boards; the extra local values are the only representation change.'][min(k,3)]);return s

def overview(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('Inspect the board, then test the decision','Follow one PCB photograph through features, a frozen cutoff, and a reproducible detector.',f'{min(k+1,4):02}/04','Actual PCB1 anomaly 048 • conceptual operation view')
 s.image(32,142,320,320,e['query_uri']);s.text(32,504,'1  Photograph the board',22,weight=600)
 s.group(k>=1);s.grid(32,142,320,320,selected=e['position']);s.path('M204 383 L388 383 L388 195 L430 195',C['accent'],2);s.image(430,126,132,132,e['query_uri'],f'{6/14} {9/14} {3/14} {3/14}');s.rect(430,126,132,132,'none',C['accent'],2);s.rect(474,170,44,44,'none',C['accent'],2);s.text(430,296,'2  Keep local detail',22,weight=600);s.lines(430,326,['14 × 14 positions','64 channels each'],20);s.end()
 s.group(k>=2);s.text(700,126,'3  Apply the cutoff',22,weight=600);score_axis(s,700,222,450,-.887,-1.114,'Recorded patch-model score');s.text(700,310,'048: flagged by the patch model',20,weight=600);s.end()
 s.group(k>=3);s.text(700,386,'4  Recover the same detector',22,weight=600)
 for j,(label,sub) in enumerate([('Encoder','weights + input transform'),('Normal bank','normal case identities'),('Classifier','coefficients + cutoff')]):
  x=700+j*153;s.path(f'M{x} 415 L{x+115} 415 L{x+135} 435 L{x+135} 496 L{x} 496 Z');s.path(f'M{x+115} 415 L{x+115} 435 L{x+135} 435');s.text(x+8,465,label,18);s.text(x,526,['fixed features','same distances','same decisions'][j],18)
 s.end();s.strip('score >= frozen_threshold','Keep misses and false alarms visible; a recovered defect does not erase a new miss.');return s

def threshold(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('Move the cutoff, keep the scores fixed','Choose the largest validation cutoff that meets the requested defect recall.',f'{min(k+1,3):02}/03','Illustrative score positions • algorithm and recall target from inspection.py')
 x0,y0,w=110,320,980;s.line(x0,y0,x0+w,y0,arrow=True);s.text(110,365,'Lower score',20);s.text(1090,365,'Higher score',20,anchor='end');s.text(36,148,'Known validation defects',22,weight=600)
 defect=[.12,.25,.34,.46,.57,.64,.72,.81,.88,.95];normal=[.06,.10,.15,.22,.28,.31,.39,.43,.53,.76]
 for j,v in enumerate(defect):s.circle(x0+v*w,220,10,'#ffffff');s.text(x0+v*w,191,str(j+1),18,anchor='middle')
 for v in normal:s.rect(x0+v*w-9,410,18,18,C['panel'])
 s.text(700,390,'Normal validation boards',22,weight=600)
 s.group(k>=1);cut=x0+.25*w;s.line(cut,150,cut,470,C['accent'],3,dash=True);s.text(cut+16,275,'Cutoff for 9 of 10',22,weight=600,color=C['accent']);s.path(f'M{cut} 240 L{cut+40} 240',C['accent'],arrow=True);s.text(660,275,'Flag scores at or above the line',20);s.end()
 s.group(k>=2);s.circle(x0+.12*w,220,22,'none',C['accent']);s.text(100,525,'Miss: defect below cutoff',20,color=C['accent']);s.path(f'M{x0+.12*w} 242 L{x0+.12*w} 495',C['accent']);s.text(660,525,'False alarm: normal above cutoff',20,color=C['accent']);s.line(850,495,850,445,C['accent'],arrow=True);s.end()
 s.strip(['scores = score(validation_boards, frozen_model)','cutoff = sort(scores[labels == 1])[::-1][ceil(recall * count) - 1]','misses = defect & (score < cutoff); false_alarms = normal & (score >= cutoff)'][min(k,2)],'Illustrative 10-defect example: the same fixed scores support every cutoff comparison.');return s

def review(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('Spend the same 24 labels in each arm','Choose cases before revealing their labels. Use the same pool, model, and seed 17.',f'{min(k+1,3):02}/03','Illustrative placement of 24 selections per arm • fixed workshop review budget')
 s.text(32,124,'Active: nearest to the cutoff',22,weight=600);s.line(32,267,555,267);s.line(296,150,296,391,C['accent'],2,dash=True);s.text(296,422,'frozen cutoff',18,anchor='middle')
 for i in range(24):
  x=220+(i%6)*30;y=170+(i//6)*52;s.rect(x,y,23,30,'#ffffff',C['accent']);s.line(x+4,y+9,x+19,y+9,C['line']);s.line(x+4,y+17,x+19,y+17,C['line'])
 s.text(32,466,'24 case IDs, selected by |score − cutoff|',20);s.text(32,501,'Labels stay hidden during selection.',20)
 s.group(k>=1);s.text(645,124,'Random: sample from the same pool',22,weight=600)
 for i in range(24):
  x=656+(i%8)*62;y=168+(i//8)*77;s.rect(x,y,35,47,'#ffffff',C['blue']);s.line(x+6,y+14,x+28,y+14,C['line']);s.line(x+6,y+27,x+28,y+27,C['line'])
 s.text(645,466,'24 case IDs, without replacement',20);s.text(645,501,'The count of new labels is identical.',20);s.end()
 s.group(k>=2);s.path('M290 515 L290 538 L892 538 L892 515',C['ink'],2);s.text(590,532,'matched fitting and evaluation cases',18,anchor='middle');s.end()
 s.strip(['order = argsort(abs(scores - frozen_threshold))','random = rng(seed=17).permutation(pool)[:24]','compare(active_model, random_model, same_validation_cases)'][min(k,2)],'A larger labeled set alone does not establish that the selection rule helped.');return s

def cases(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('Keep the recovery beside the regression','Use each model’s own cutoff. These are recorded final examples, not validation choices.',f'{min(k+1,3):02}/03','Recorded PCB1 cases 048 and 015 • final teaching examples')
 s.image(32,130,240,240,e['query_uri']);s.text(32,406,'Board 048',24,weight=600);s.text(32,439,'Known defect',20)
 score_axis(s,320,200,350,-1.006,-.499,'Whole-image baseline');s.text(320,290,'Missed defect',22,color=C['accent'],weight=600)
 s.group(k>=1);score_axis(s,320,402,350,-.887,-1.114,'Patch-enriched model');s.text(320,492,'Defect flagged',22,weight=600);s.end()
 s.group(k>=2);s.image(868,130,280,280,e['regression_uri']);s.text(868,447,'Board 015',24,weight=600);s.lines(868,479,['Whole: flagged','Patch: missed'],20);s.end()
 s.strip('prediction = score >= model.threshold','048 is recovered; 015 becomes a miss. Compare both models across the full aligned case set.');return s

def reproduce(spec,state,e):
 k=[r['id'] for r in spec['states']].index(state['id']);s=SVG('Reassemble the detector from its saved parts','The photograph alone cannot reproduce a decision; the arrays and cutoff must match.',f'{min(k+1,3):02}/03','Array anatomy follows save_classifier / load_classifier • values from the recorded board')
 s.image(32,160,185,185,e['query_uri']);s.text(32,386,'Same RGB input',20,weight=600);s.line(217,255,258,255,arrow=True)
 s.text(280,126,'1  Encoder + preprocessing',22,weight=600)
 for off in [20,10,0]:s.grid(280+off,164-off,170,170,n=8,m=8)
 s.lines(280,381,['Frozen weights','Input size and normalization'],18);s.text(280,456,'whole[512]',20,mono=True);s.text(280,488,'patches[14,14,64]',18,mono=True)
 s.group(k>=1);s.text(590,126,'2  Normal bank',22,weight=600)
 for off in [20,10,0]:s.grid(590+off,164-off,170,170,n=8,m=8)
 s.lines(590,381,[f'{e["normal_count"]} normal fitting cases','Case IDs + channel scales'],18);s.text(590,456,'reference_bank',20,mono=True);s.text(590,488,'reference_cases',18,mono=True);s.end()
 s.group(k>=2);s.text(890,126,'3  Classifier',22,weight=600);tensor(s,890,164,260,80,e['classifier_coef'][:64],16);s.line(890,290,1150,290);s.line(1000,265,1000,315,C['accent'],2,dash=True);s.text(1016,282,'cutoff',18);s.lines(890,381,['mean + std + coefficients','intercept + frozen threshold'],18);s.text(890,456,'score → decision',20,mono=True);s.text(890,488,'match saved board IDs',18);s.end()
 s.strip('load_classifier(path); score(same_board, recovered_components)','Verify the resulting score and decision against the saved case identity.');return s

DRAW={'patch-distance':patch,'representations':representations,'overview':overview,'threshold':threshold,'review':review,'case-changes':cases,'reproduce':reproduce}

def hero(e):
 s=SVG('Inspect the photograph and the detector decision','Actual PCB1 anomaly 048 and its recorded patch-model score.');s.a=s.a[:1]
 s.text(32,45,'1  Inspect the board',30,weight=600);s.image(32,88,320,320,e['query_uri']);s.grid(32,88,320,320,selected=e['position']);s.text(32,449,'PCB1 anomaly 048',26)
 s.text(416,45,'2  Compare local features',30,weight=600)
 for x,key,label,color in [(416,'query_uri','Query patch',C['accent']),(620,'reference_uri','Normal reference',C['blue'])]:
  s.image(x,122,176,176,e[key],f'{6/14} {9/14} {3/14} {3/14}');s.rect(x,122,176,176,'none',color,2);s.rect(x+176/3,122+176/3,176/3,176/3,'none',color,2);s.text(x,342,label,24)
 s.path('M204 328 L382 328 L382 210 L408 210',C['accent'],2,arrow=True);s.text(416,397,'64 channels at one location',26);s.text(416,438,'Same location in normal boards',24)
 s.text(855,45,'3  Check the cutoff',28,weight=600);s.line(863,215,1166,215);s.line(960,156,960,276,C['ink'],2,dash=True);s.circle(1020,215,10,C['accent'],C['accent']);s.text(972,151,'cut −1.114',23,mono=True);s.text(1020,318,'−0.887',27,mono=True,anchor='middle',color=C['accent']);s.text(855,397,'048 is flagged.',26,weight=600);s.text(855,438,'Count other misses too.',24)
 s.text(32,527,'Masks support inspection; the detector’s features come from the photographs.',27)
 return s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only');args=ap.parse_args();e=evidence()
 if not args.only:
  h=hero(e);h.save(OUT/'hero.svg');hp=OUT/'hero.svg';hp.write_text(hp.read_text(encoding='utf-8').replace('viewBox="0 0 1200 675"','viewBox="0 0 1200 560"'),encoding='utf-8')
 for p in OUT.glob('*.json'):
  if p.stem not in DRAW:continue
  if args.only and p.stem!=args.only:continue
  spec=json.loads(p.read_text(encoding='utf-8'))
  for state in spec['states']:
   rel=f'art/{p.stem}/{state["id"]}.svg';DRAW[p.stem](spec,state,e).save(OUT/rel);state['artwork']=rel
  p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
