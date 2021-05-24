# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 16:23:59 2021

@author: roses
"""

from os import listdir, getcwd, path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams.update({'axes.titlepad':30,'axes.labelpad':10,
                     'font.weight':'bold','font.size':20,
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k','axes.grid':True,
                     'lines.markersize':12,'legend.frameon':True,
                     'legend.framealpha':1})

#open file from cwd and parse data into dataframe
cwd = getcwd()
files = listdir(cwd)
file = ''
for f in files:
    ext = path.splitext(f)[1]
    if ext == '.csv':
        file = path.join(cwd,f)
        dtypes = {'date':'str'}
        data = pd.read_csv(file,dtype=dtypes,parse_dates=['date'])
        break

#adjust data to more usable form (takes a long time to run code for adjustment)
constituents = []
start_date = []
end_date = []
#for each ticker set in data pull out individual tickers into constituent list
for j in range(0,len(data['tickers'])):
    ticker_set_str = data['tickers'][j] + ','
    name_start = -1
    #go through each char in ticker_set_str and find each ticker name
    #as separated by comma delimiter
    for i in range(0,len(ticker_set_str)):
        if ticker_set_str[i] == ',':
            name = ticker_set_str[name_start+1:i]
            #add the ticker name to constituent list if new ticker
            if name not in constituents:
                constituents.append(name)
                #add start date for new ticker
                start_date.append(data['date'][j])
                #add date to end date for ticker, but add start date as
                #placeholder until actual end date found
                end_date.append(data['date'][j])
            #if ticker already exists in constituent list set that date
            #as the end date, this will continue to update the end date
            #until the loop finishes going thorugh the data
            else:
                #determine the location of the existing ticker name
                loc = constituents.index(name)
                #input the date as the end date
                end_date[loc] = data['date'][j]
            name_start = i

#determine time spent as constituent for each ticker    
time_alive = []        
for i in range(0,len(constituents)):
    delta = end_date[i] - start_date[i]
    time_alive.append(delta.days)

#reformat adjusted data as df and sort values by time_alive
data_adj = pd.DataFrame(columns = ['tickers','start_date','end_date','time_alive'])
data_adj['tickers'] = constituents
data_adj['start_date'] = start_date
data_adj['end_date'] = end_date
data_adj['time_alive'] = time_alive
data_adj['time_alive'] = list(data_adj['time_alive']/365)
good_data = data_adj.sort_values(by=['time_alive'])

avg_time_alive = np.average(good_data['time_alive'])

#bar plot of all constituents by time spent as member
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.plot([0,len(good_data)-1],[avg_time_alive,avg_time_alive],'r--')
plt.bar(good_data['tickers'],good_data['time_alive'],snap=False,color='b')
plt.xticks([])
plt.title('How Many Years Has Each Historical Constituent of the S&P500 \n'+
          'Spent as a Member of the Index')
plt.xlabel('All Historical Constituents of the S&P500 (1996-2020)')
plt.ylabel('Time Spent as Consituent \n of the S&P500 \n (Years)')
#plt.grid(True,which='minor',linewidth=.5,color='k')
plt.legend([f'Average Time Spent as Member = {int(avg_time_alive)} years',
            f'Total Number of Constituents = {len(good_data)}'])

#boxplot of distribution of time spent as member across constituency
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
bp = sns.boxplot(data = good_data)
bp.set_xticklabels(['Constituency of the S&P500'])
plt.ylabel('Time Spent as Consituent \n of the S&P500 \n (Years)')
plt.title('Distribution of Time Spent as Constituent of S&P500 (1996-2020)')

#histogram of distribution of time spent as member across constituency
fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
histogram = sns.histplot(good_data['time_alive'],kde=True)
plt.xlabel('Time Spent as Consituent of the S&P500 (Years)')
plt.ylabel('No. of Consituents')
plt.title('How Many Years Do Constituent Companies Last as \n'+
          'Members of the S&P500 (1996-2020)')
plt.legend(['Kernel Density Estimate','Count of Constituents'])


# #this is a scary graph
# fig, ax = plt.subplots()
# mng = plt.get_current_fig_manager()
# mng.window.showMaximized()
# for i in range(0,len(constituents)):
#     plt.plot([start_date[i],end_date[i]],[i,i])