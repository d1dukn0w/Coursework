# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:13:47 2023

@author: Conra
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import norm
x=np.load('londonIncidents.npz')
d={'xdata':x['all'][:,0],'ydata':x['all'][:,1]}
data=pd.DataFrame(d)
N=15
xmax=46.0
xmin=-0.25
xstep=(xmax-xmin)/N
xlst=np.arange(xmin,xmax+xstep,step=xstep)

ymax=0
ymin=-17.5
ystep=(ymax-ymin)/N
ylst=np.arange(ymin,ymax+ystep,step=ystep)

#plt.scatter(data[['xdata']],data[['ydata']],marker='.')
#plt.grid(visible=True,which='both',axis='both', color='r',linestyle='-')
#plt.xticks(ticks=xlst, rotation=30)
#plt.yticks(ticks=ylst)
#plt.xlim(xmin,xmax)
#plt.ylim(ymin,ymax)
ntotal=0
nlst=[]
for i in range(N):
    xlimlst=xlst
    xliml=xlimlst[i]
    xlimu=xlimlst[i+1]
    #print('i:{}, ({},{})'.format(i,xliml,xlimu))
    for k in range(N):
        ylimlst=ylst
        #print(ylimlst)
        yliml=ylimlst[k]
        ylimu=ylimlst[k+1]
        #print('k:{}, ({},{})'.format(k,yliml,ylimu))
        trudfxl=(data.where(data[['xdata']]>xliml)).notnull()
        trudfxu=(data.where(data[['xdata']]<xlimu)).notnull()
        trudfyl=(data.where(data[['ydata']]>yliml)).notnull()
        trudfyu=(data.where(data[['ydata']]<ylimu)).notnull()
        n=0
        for i in range(len(data)):
            if ((trudfxl['xdata'][i]==True) and (trudfxu['xdata'][i]==True) and (trudfyl['ydata'][i]==True) and (trudfyu['ydata'][i]==True)):
                n+=1
                ntotal+=1
                #plt.scatter(data['xdata'][i],data['ydata'][i],color='k',marker='.')
        nlst.append(n)

density=np.array(nlst)
avgdens = np.average(density)
stddev = np.std(density)
print((density))
print("The average density is {} per box".format(avgdens))

fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)
unidata=np.random.uniform(0,15, 1000)
ax1.hist(unidata, bins=15, density=True,label='True Uniform Distribution')
ax1.set_xlabel(xlabel='Density (Counts/Box)')
ax2.set_xlabel(xlabel='Density (Counts/Box)')
ax2.hist(density, bins=15, color='r', label='Data', density=True)
ax1.set_ylabel(ylabel='Probability')
fig.legend()
print('{}% of datapoints were excluded by the bounds'.format(round((((len(data)-ntotal)/len(data))*100),2)))
