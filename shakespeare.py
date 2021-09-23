# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 13:19:34 2021

@author: roses

Shakespeare Play Analysis
"""

from os import listdir, getcwd, path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':10,
                      'font.weight':'bold','font.size':20,
                      'axes.titleweight':'bold','axes.labelweight':'bold',
                      'grid.color':'w','axes.edgecolor':'w','axes.grid':True,
                      'axes.facecolor':[.75,.75,.75],
                      'lines.markersize':12,'legend.frameon':True,
                      'legend.framealpha':1})

#open file from cwd and parse data into dataframe
cwd = getcwd()
files = listdir(cwd)
for f in files:
    ext = path.splitext(f)[1]
    if ext == '.xlsx':
        file = path.join(cwd,f)
        df = pd.read_excel(file)
        break

#plot number of plays grouped by country setting    
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
df.groupby('Country (modern)')['Title'].nunique().plot(kind='bar',rot=45)
labels = ax.get_xticklabels()
labels[4].set_text('Fictional \n country')
ax.set_xticklabels(labels,fontsize=14)
ax.set_axisbelow(True)
plt.title('Where Did Shakespeare Set His Plays?',bbox=dict(fc="0.9"))
plt.ylabel('Number of Shakespeare Plays \n per Country Setting')
    

    