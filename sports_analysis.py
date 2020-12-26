# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:03:54 2020

@author: roses
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy

sns.set(font_scale=2)
#sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':10,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':15,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1,
                     'legend.facecolor':'w'})

file = r'C:\Users\roses\Desktop\Rose Random\data visualization projects\sports analysis\ballsportsdata.csv'
data = pd.read_csv(file)

#exponential regression
def exponential(x, a, k, b):
    return a*np.exp(x*k) + b

popt, pcov = scipy.optimize.curve_fit(exponential,data['PAD'],data['RATS'],p0=[1,-.5,1])

x = np.linspace(0,1000)
akb = list(popt)
y = []
for xval in x:
    y.append(exponential(xval,akb[0],akb[1],akb[2]))
    
#r2 value calculation
residuals = data['RATS'] - exponential(data['PAD'], *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((data['RATS']-np.mean(data['RATS']))**2)
r_squared = 1 - (ss_res / ss_tot)

#plot
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
plt.plot(data['PAD'],data['RATS'],'.')
plt.plot(x,y,'--')
plt.title('Scoring Rate vs Player Density in Professional Ball Sports',bbox=dict(fc="0.9"))
plt.ylabel('RATS (goals/hr)')
plt.xlabel('PAD ($m^2$/player)')
a = f'{akb[0]: .2f}'
kx = f'{akb[1]: .4f}'+'x'
b = f'{akb[2]: .2f}'
eqn = ('$y = {}*e^{{{}}}{}$').format(a,kx,b)
r2 = f'$r^2$ = {r_squared: .2f}'
plt.legend(['Raw Data',f'Fitted Curve:\n{eqn}\n{r2}'])
plt.text(.575,.6,'RATS = Rate of Average Total Scoring\nPAD = Player Area Density',
         bbox=dict(facecolor='w'),transform=ax.transAxes)