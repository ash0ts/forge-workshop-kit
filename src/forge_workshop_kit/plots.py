"""Plots of saved predictions; these functions never train or call a provider."""
import numpy as np
import matplotlib.pyplot as plt


def forecast(prediction, split, *, index=0, title='Saved prediction'):
    if prediction.ndim<=2:
        figure,ax=plt.subplots(figsize=(10,3.6),layout='constrained')
        stride=max(1,len(prediction)//500)
        times=split['ids'][::stride].astype('datetime64[m]')
        ax.plot(times,split['y'][::stride,0],label='Observed future',color='#222')
        ax.plot(times,prediction[::stride,0],label='Prediction',color='#c47721',alpha=.8)
        ax.set(ylabel='log10 XRS-B flux (W/m²)',title=title)
        ax.legend(); figure.autofmt_xdate()
        return figure
    i=min(index,len(prediction)-1)
    figure,axes=plt.subplots(1,5,figsize=(13,3),layout='constrained')
    arrays=[split['x'][i,0],split['x'][i,1],prediction[i,0],split['y'][i,0],
            np.abs(prediction[i,0]-split['y'][i,0])*split['mask'][i,0]]
    labels=['One hour ago','Now','Predicted +1 hour','Observed +1 hour','Absolute error (disk)']
    lo,hi=np.percentile(split['y'][i,0],[1,99])
    for axis,array,label in zip(axes,arrays,labels):
        axis.imshow(array,origin='lower',cmap='magma',vmin=0 if label.startswith('Absolute') else lo,
                    vmax=None if label.startswith('Absolute') else hi)
        axis.set_title(label,fontsize=10);axis.set_axis_off()
    figure.suptitle(title+' · '+str(split['ids'][i])+' UTC',fontsize=12)
    return figure
