"""Plot saved v0.3.0 observations and predictions. No fitting or inference."""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from forge_workshop_kit import solar
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--state',type=Path,default=root.parents[1]/'.workshop/solar-v030-rehearsal')
parser.add_argument('--data',type=Path,default=root.parents[1]/'data/solar-v1')
a=parser.parse_args(); j=json.loads((a.state/'journal.json').read_text()); by={s['name']:s for s in j['stages'].values()}
images,_=solar.load_aia(a.data); goes,_=solar.load_goes(a.data)
out=root/'public/images';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#f6f2e7','axes.facecolor':'#f6f2e7','text.color':'#163c43','axes.labelcolor':'#163c43','xtick.color':'#163c43','ytick.color':'#163c43'})
records=[]
def save(fig,name,desc,stages=()):
 fig.savefig(out/name,dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor());plt.close(fig)
 records.append({'file':name,'description':desc,'stage_ids':[by[n]['id'] for n in stages],'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest()})
def pred(name):return np.load(a.state/'outputs'/by[name]['id']/'predictions.npy')
# Opening uses training observations, not results or selected final examples.
fig,ax=plt.subplots(1,2,figsize=(12,3.5),gridspec_kw={'width_ratios':[1.7,1]})
x=goes['train'];take=min(720,len(x['ids']));t=x['ids'][:take].astype('datetime64[m]')
ax[0].plot(t,x['persistence'][:take,0],color='#2b7a78',lw=1.6);ax[0].set_title('GOES-15 · February 1, 2014',loc='left');ax[0].set_ylabel('log₁₀ XRS-B flux (W/m²)');ax[0].set_xlabel('Observation time (UTC)');ax[0].xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
i=images['train'];ax[1].imshow(i['x'][0,1],cmap='sdoaia171' if 'sdoaia171' in plt.colormaps() else 'inferno',vmin=-2,vmax=3);ax[1].set_title('AIA 171 Å · '+i['ids'][0]+' UTC',loc='left',fontsize=12);ax[1].axis('off')
fig.tight_layout();save(fig,'v030-observations.png','Training observations from immutable solar-v1 data. AIA shows normalized log1p intensity at 64 × 64.')
# Three actual training observations make image channel and horizon concrete.
fig,axes=plt.subplots(1,3,figsize=(11,3.4));origin=np.datetime64(i['ids'][0]);times=[origin-np.timedelta64(60,'m'),origin,origin+np.timedelta64(60,'m')]
for ax,z,label,ts in zip(axes,[i['x'][0,0],i['x'][0,1],i['y'][0,0]],['Input channel 0 · −60 min','Input channel 1 · now','Target · +60 min'],times):
 ax.imshow(z,cmap='inferno',vmin=-2,vmax=3);ax.set_title(label,fontsize=14);ax.set_xlabel(str(ts)+' UTC',fontsize=11);ax.set_xticks([]);ax.set_yticks([])
fig.tight_layout();save(fig,'v030-image-window.png','First accepted training image window; common intensity scale; observations, not model output.')
# Actual selected GOES training loss. Avoid cross-loss scale comparison.
s=by['goes/search-2'];fig,ax=plt.subplots(figsize=(10.5,3.7));loss=s['result']['losses'];ax.plot(np.arange(1,len(loss)+1),loss,color='#2b7a78',lw=2);ax.set_xlabel('Training step');ax.set_ylabel('Masked squared training loss');ax.set_title('The selected GOES model at its 60-step limit',loc='left');ax.scatter([60],[loss[-1]],color='#b76738');ax.annotate('Training stops here',xy=(60,loss[-1]),xytext=(36,max(loss)*.4),arrowprops={'arrowstyle':'->','color':'#b76738'});fig.tight_layout();save(fig,'v030-goes-loss.png','Saved training losses; no new training. A falling training loss does not establish final quality.',['goes/search-2'])
# Matched validation and final image comparisons with identical scale and first-case selection.
for split,names,filename in [('validation',['images/manual-conv','images/manual-residual'],'v030-validation-predictions.png'),('test',['images/final-manual','images/final-agent'],'v030-final-predictions.png')]:
 d=images[split];fig,axes=plt.subplots(len(names),4,figsize=(12,5.0));labels=['Convolutional','Residual'] if split=='validation' else ['Manual','Agent-selected'];target=d['y'][0,0];mask=d['mask'][0,0]
 for row,(name,label) in enumerate(zip(names,labels)):
  prediction=pred(name)[0,0];err=np.abs(prediction-target)*mask
  vals=[d['x'][0,1],prediction,target,err]
  for col,(val,title) in enumerate(zip(vals,['Current image','Forecast +60 min','Observed +60 min','Absolute on-disk error'])):
   axes[row,col].imshow(val,cmap='magma' if col==3 else 'inferno',vmin=0 if col==3 else -2,vmax=1 if col==3 else 3);axes[row,col].set_xticks([]);axes[row,col].set_yticks([])
   if row==0:axes[row,col].set_title(title,fontsize=12)
  axes[row,0].set_ylabel(label,fontsize=14)
 fig.suptitle('Forecast origin '+d['ids'][0]+' UTC · same scales in both rows',fontsize=13);fig.tight_layout();save(fig,filename,'First accepted '+split+' case, not the largest improvement. Intensity scale −2 to 3; absolute error scale 0 to 1; training-normalized log1p intensity.',names)
# Final GOES comparison from saved predictions and the fixed test split.
d=goes['test'];forecast=pred('goes/final')[:,0];fig,ax=plt.subplots(figsize=(11.5,3.7));times=d['ids'].astype('datetime64[m]')+np.timedelta64(30,'m')
ax.plot(times,d['y'][:,0],label='Observed future',color='#163c43',lw=1.6);ax.plot(times,d['persistence'][:,0],label='Persistence',color='#b76738',lw=1,alpha=.8);ax.plot(times,forecast,label='Selected model',color='#4382a6',lw=1.5);ax.legend(loc='upper right',ncol=3,frameon=False);ax.set_xlabel('Target time (UTC)');ax.set_ylabel('log₁₀ XRS-B flux (W/m²)');ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b %d\n%H:%M'));fig.tight_layout();save(fig,'v030-goes-final.png','All 2,694 accepted final GOES windows, saved selected-model predictions.',['goes/final'])
(root/'notes/visual-v030-figures.json').write_text(json.dumps({'source_workspace':'6e768bbe071648e094cb296a0a57c21e','dataset':solar.verify_data(a.data),'training_calls':0,'provider_calls':0,'figures':records},indent=2)+'\n')
print(json.dumps({'plots':len(records),'training_calls':0,'provider_calls':0}))
