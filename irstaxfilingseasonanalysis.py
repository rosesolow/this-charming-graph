# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 13:12:28 2021

@author: roses
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#import scipy

#set plotting params
sns.set(font_scale=2)
#sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':25,'axes.labelpad':10,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':15,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1,
                     'legend.facecolor':'w'})

#import data
file = r'C:\Users\roses\Desktop\Rose Random\data visualization projects\tax filing season analysis\irstaxfilingseasondata.csv'
dtypes = {'Week Ending Date':'str'}
data = pd.read_csv(file,dtype=dtypes,parse_dates=['Week Ending Date'])
data['Returns'] = [x/1000000 for x in data['Returns']]

#create list of all years from filing week dates and list of indexes for
#each new year of filing data
loc = 0
newyearlocs = [loc] #index for each new year of filing data
years = [data['Week Ending Date'][loc].year]
for i in range(len(data)):
    if data['Week Ending Date'][i].year != data['Week Ending Date'][loc].year:
        loc = i
        newyearlocs.append(loc)
        years.append(data['Week Ending Date'][loc].year)
newyearlocs.append(len(data)-1)

#create data for weekly returns from cumulative returns col
returns = []
for r in range(len(data['Returns'])-1):
    delta = data['Week Ending Date'][r] - data['Week Ending Date'][r+1]
    week_delta = delta.days/7
    if week_delta > 1:
        returns.append(np.nan)
    else:
        returns.append(data['Returns'][r] - data['Returns'][r+1])

#calculate average returns for each filing week (week 0 is week of filing
#deadline and each filing week is number of weeks before or after week 0)
df = pd.DataFrame(columns=years)
fweeks = list(range(min(data['Filing Week']),max(data['Filing Week']+1)))
df['Filing Week'] = fweeks
fweekavgs = []
for i in range(len(returns)):
    week = data['Filing Week'][i]
    year = data['Week Ending Date'][i].year
    index = week + 11
    df[year][index] = returns[i]
for w in range(len(fweeks)):
    returnsperfweek = []
    for y in years:
        returnsperfweek.append(df[y][w])
    fweekavgs.append(np.nanmean(returnsperfweek))
    
#plot returns per filing week for each year and average returns per filing
#week for weeks -10 to 4
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
for y in years:
    color = (years[0] - y + 5)/15
    plt.plot(fweeks[1:16],df[y][1:16],'.',c=[color,color,color])
plt.plot(fweeks[1:16],fweekavgs[1:16],'.-')
labels = years.copy()
labels.append('Average')
plt.legend(labels)
plt.xlabel('Filing Week (No. of Weeks Before or After Deadline)')
plt.ylabel('Returns Received per Week (in millions)')
plt.title('When Do We File Our Taxes?\n(IRS Data 2012-2020)',
          bbox=dict(fc="0.9"))
plt.text(.025,.825,'Week 0 Denotes Week of \nFiling Deadline (Apr 15)',
             bbox=dict(facecolor='w'),transform=ax.transAxes)

#because data >4 filing weeks after deadline is sporadic this graph looks
#funny so not including
#plot returns per filing week for each year and average returns per filing wk
# fig, ax = plt.subplots()
# mng = plt.get_current_fig_manager()
# mng.window.showMaximized() 
# for y in years:
#     color = (years[0] - y + 5)/15
#     plt.plot(fweeks,df[y],'.',c=[color,color,color])
# plt.plot(fweeks,fweekavgs,'.-')
# labels = years.copy()
# labels.append('Average')
# plt.legend(labels)
# plt.xlabel('Filing Week')
# plt.ylabel('Returns Received')
# plt.title('IRS Received Tax Returns by Filing Week',bbox=dict(fc="0.9"))
# plt.text(.025,.825,'Week 0 Denotes Week of \nFiling Deadline (Apr 15)',
#              bbox=dict(facecolor='w'),transform=ax.transAxes)

#plot cumulative returns per filing week over each year
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
for j in range(len(newyearlocs)-1):
    color = (years[0] - years[j] + 5)/15
    plt.plot(data['Filing Week'][newyearlocs[j]:newyearlocs[j+1]],
             data['Returns'][newyearlocs[j]:newyearlocs[j+1]],
             '.',c=[0,0,color])
plt.legend(years)
plt.xlabel('Filing Week (No. of Weeks Before or After Deadline)')
plt.ylabel('Cumulative Returns Received (in millions)')
plt.title('Cumulative IRS Received Tax Returns by Filing Week per Year',
          bbox=dict(fc="0.9"))
plt.text(.7,.05,'Week 0 Denotes Week of \nFiling Deadline (Apr 15)',
             bbox=dict(facecolor='w'),transform=ax.transAxes)

#plot cumulative returns over time
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
for j in range(len(newyearlocs)-1):
    color = (years[0] - years[j] + 5)/15
    plt.plot(data['Week Ending Date'][newyearlocs[j]:newyearlocs[j+1]],
             data['Returns'][newyearlocs[j]:newyearlocs[j+1]],
             '.-',c=[0,0,color])
plt.xlabel('Date')
plt.ylabel('Cumulative Returns Received (in millions)')
plt.title('IRS Tax Filing Seasons 2012-2020',bbox=dict(fc="0.9"))
