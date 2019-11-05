# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:24:16 2019

@author: usrsolo
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
import scipy
from sklearn.linear_model import LinearRegression

sns.set(font_scale=2)
sns.set_style("whitegrid")
plt.rcParams.update({'font.size':25,'axes.titlepad':35,'axes.labelpad':12})

#read in the raw data as a dataframe
file = r'C:\Users\usrsolo\Documents\Rose Random\USA SP Return and Inflation Raw Data.csv'
df = pd.read_csv(file)
#holding periods (timelengths in years of holding SP500)
periods = [1,5,10,20,30,40]
colnames = []
for p in periods:
    colnames.append(str(p) + ' yr')

#calculate annualized returns adjusted for inflation for each period and save
#to new dataframe with each period per column
data = pd.DataFrame(columns=colnames) 
for p in periods:
    period_data = []
    for i in range(len(df)):
        if i < p-1:
            period_data.append(np.nan)
        else:
            #compounded return of previous p years at given year
            r = np.prod(df['SP Return'][i-p+1:i+1]/100+1)
            #compounded inflation of previous p years at given year
            inf = np.prod(df['Inflation'][i-p+1:i+1]/100+1)
            #adjust return for inflation and annualize it
            adj_r = (r/inf-1)*100/p
            period_data.append(adj_r)
    key = str(p) + ' yr'
    data[key] = period_data
    
fignum = 0

#plot adjusted returns for each holding period over time
fignum+=1
plt.figure(fignum)
plt.title('S&P Returns over Time (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('% Return, Annualized')
plt.plot(df['Year'],data)
plt.legend(colnames,frameon=True,title='Periods')
mng = plt.get_current_fig_manager()
mng.window.showMaximized()   

#boxplot returns for each holding period
fignum+=1
plt.figure(fignum)
plt.title('S&P Returns Distribution per Period (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
plt.xlabel('Periods')
plt.ylabel('% Return, Annualized')
bp = sns.boxplot(data = data)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#violinplot returns for each holding period
fignum+=1
plt.figure(fignum)
plt.title('S&P Returns Distribution per Period (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
plt.xlabel('Periods')
plt.ylabel('% Return, Annualized')
vp = sns.violinplot(data = data)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#plot histogram of returns for each holding period
fignum+=1
plt.figure(fignum)
i = 0
for key in data:
    #create subplots in figure for each period
    i = i + 1
    sub = plt.subplot(2,3,i)
    #determine starting numerical datapoint loc
    a = 0
    while math.isnan(data[key][a]) == True:
        a = a + 1
    #create histogram plot with kde distribution
    histogram = sns.distplot(data[key][a:],kde=True)
    title = key + ' Period'
    plt.title(title,fontsize = 15)
    plt.xlabel('% Return, Annualized',fontsize = 15)
    plt.ylabel('Density',fontsize = 15)
    plt.ylim(0,.05)
    plt.xlim(-45,80)
plt.suptitle('S&P Returns Distribution per Period (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
#adjust padding between subplots
plt.subplots_adjust(hspace = .5, wspace = .3)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#plot histogram of returns for each holding period
fignum+=1
plt.figure(fignum)
i = 0
for key in data:
    i = i + 1
    sub = plt.subplot(2,3,i)
    a = 0
    while math.isnan(data[key][a]) == True:
        a = a + 1
    #create histogram plot without kde distribution
    histogram = sns.distplot(data[key][a:],kde=False)
    title = key + ' Period'
    plt.title(title,fontsize = 15)
    plt.xlabel('% Return, Annualized',fontsize = 15)
    plt.ylabel('Count',fontsize = 15)
    plt.ylim(0,30)
    plt.xlim(-45,80)
plt.suptitle('S&P Returns Distribution per Period (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
plt.subplots_adjust(hspace = .5, wspace = .3)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#determine chance of returns of a given range for each period
returns = [[-100,0],
           [0,10],
           [10,100],
           [5,15],
           ]
for key in data:
    a = 0
    while math.isnan(data[key][a]) == True:
        a = a + 1
    #kernel density estimation (kde) way to estimate probability density
    #function of a random variable
    kde = scipy.stats.gaussian_kde(data[key][a:])
    #for each range in returns determine the probability of returns falling
    #in this range by integrating kde between the two limits
    for r in returns:
        r.append(100*kde.integrate_box_1d(r[0],r[1]))

#write the likelihoods of returns to csv file        
likelihoods = pd.DataFrame(data=returns)
likelihoods.columns = ['From','To'] + colnames
likelihoods_file = r'C:\Users\usrsolo\Documents\Rose Random\annualized returns likelihoods.csv'
likelihoods.to_csv(likelihoods_file)

#plot chance of returns of a given range for each period
fignum+=1
plt.figure(fignum)
plt.title('S&P Returns Likelihood of Occuring (Adjusted for Inflation, Annualized)',bbox=dict(fc="0.9"))
plt.xlabel('Periods')
plt.ylabel('Likelihood (%)')
labels = []
for r in returns:
    labels.append(f'Returns between {r[0]}% and {r[1]}%')
    plt.plot(r[2:],'.-',markersize=25)
plt.legend(labels,frameon=True)
#rename xticks to period labels
ticks = range(len(colnames))
plt.xticks(ticks,colnames)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#plot P/E for SP over time
fignum+=1
plt.figure(fignum)
plt.title('S&P P/E over Time',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('P/E')
plt.plot(df['Year'],df['P/E'])
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

#plot returns v P/E for each period
fignum+=1
plt.figure(fignum)
i = 0
for p in periods:
    #create subplots in figure for each period
    i+=1
    sub = plt.subplot(2,3,i)
    #read in the p/e for the initial year of the periods
    x = df['P/E'][:len(df)-(p-1)]
    y = data[str(p) + ' yr'][(p-1):]
    plt.plot(x,y,'.')
    
    #ignore all datapoints with P/E greater than outlier
    outlier = 40
    index = x[x>outlier].index.tolist()
    if index is not []:
        x = x.drop(index)
        y = y.drop(index)
        
    #apply linear regression on data
    x = x.values.reshape(-1,1)
    lin_reg = LinearRegression().fit(x,y)
    plt.plot([min(x),max(x)],
              [lin_reg.coef_*min(x)+lin_reg.intercept_,
               lin_reg.coef_*max(x)+lin_reg.intercept_])
    plt.ylim(-50,100)
    plt.xlim(0,80)
    plt.xlabel('P/E of Intitial Year in Period',fontsize=15)
    plt.ylabel('% Return, Annualized',fontsize=15)
    plt.title(str(p) + ' yr Period',fontsize=15)
    
    r_sq = round(lin_reg.score(x,y)*100,1)
    slope = round(lin_reg.coef_[0],2)
    intercept = round(lin_reg.intercept_,2)
    plt.legend(['Returns',
                f'Regression: {slope}*[P/E] + {intercept}; R_sq = {r_sq}%'],
    fontsize=10,frameon=True)
    
plt.suptitle('S&P Returns vs. P/E (Adjusted for Inflation, Annualized)',fontsize=30,bbox=dict(fc="0.9"))
plt.subplots_adjust(hspace = .5, wspace = .3)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()



