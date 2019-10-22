# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:42:58 2019

@author: usrsolo
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib as mpl
import numpy as np

plt.rcParams.update({'font.size':25,'axes.titlepad':35,'axes.labelpad':20})

file = r'C:\Users\usrsolo\Documents\Rose Random\US poltical party affiliation over time raw data.csv'
data = pd.read_csv(file)

#convert dates in dataframe from strings to datetime types
dates = []
for i in range(len(data)):
    for j in range(len(data['Date'][i])):
        #use the first day of the survey set by reading only up to hyphen
        if data['Date'][i][j] == '-' :
            break
    dates.append(datetime.strptime(data['Date'][i][:j],'%Y %b %d'))
data['Date'] = dates

#the dates are in descending order, would use below function to resort however
#the moving calculation is crafted to work with descending order dates
#data = data.sort_values(by=['Date'])

#from the raw data calculate out the leanings of independents
r_leaning = data['Republicans + Republican leaners'] - data['Republicans']
d_leaning = data['Democrats + Democratic leaners'] - data['Democrats']  
data['Republican Leaning Independents'] = r_leaning
data['Democratic Leaning Independents'] = d_leaning

#associate a color with each key of the dataset for graphing
keys = list(data.keys())
colors = ['','r','g','b','r','b','tab:pink','c']

#calculate the moving average of the data to smooth out the data to be easier
#to distinguish trends
moving_avg_data = pd.DataFrame(columns = keys)
moving_avg_data['Date'] = data['Date']
span = 90 #days average to be calculated over
for key in keys:
    if key != 'Date':
        smoothdata = []
        for i in range(len(data[key])):
            #find the date closest to the span days away from datapoint being
            #calculated (not all averages is over exact no. of span days)
            j = i
            while (data['Date'][i] - data['Date'][j]).days < span:
                j+=1
                #if reach end of dataset break to avoid error
                if j == len(data[key]):
                    break
            #if can calculate span days away without reaching end of dataset
            #calculate average over span, else append nan
            if j < len(data[key]):
                x = list(data[key][i:j])
                smoothdata.append(np.average(x))
            else:
                smoothdata.append(np.nan)
        moving_avg_data[key] = smoothdata

#create_plot function, creates plot of given set of columns of data
generic_title = 'US Political Party Affiliations Over Time'
def create_line_plot(title=generic_title,df=data,cols=[1,2,3]):

    fig, ax = plt.subplots()
    plt.grid()
    #set grid and axes behind chart elements, can also use zorder
    ax.set_axisbelow(True)
    
    #setup minor axes gridlines
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    plt.grid(b=True, which='minor', color='k', linewidth=0.1)
    
    plt.title(title,bbox=dict(fc="0.9"))
    plt.xlabel('Date')
    plt.ylabel('Affiliated Citizens (%)')
    
    mxm = 0
    for i in cols:
        plt.plot(df['Date'],df[keys[i]],color=colors[i])
        if max(df[keys[i]]) > mxm:
            mxm = max(df[keys[i]])
    plt.legend()
    plt.ylim(top=mxm+10)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    
#create plots using raw data
create_line_plot(cols=[1,2,3])
create_line_plot(cols=[4,5])  
create_line_plot(cols=[6,7])
create_line_plot(cols=[1,3,6,7])

#create plots using moving average data
moving_avg_title = generic_title + f' ({span} day moving average)'
create_line_plot(title=moving_avg_title,df=moving_avg_data,cols=[1,2,3])
create_line_plot(title=moving_avg_title,df=moving_avg_data,cols=[4,5])  
create_line_plot(title=moving_avg_title,df=moving_avg_data,cols=[6,7])
create_line_plot(title=moving_avg_title,df=moving_avg_data,cols=[1,3,6,7])

#create_plot function, creates plot of given set of columns of data
def create_stacked_plot(title=generic_title,df=data,cols=[1,2,3]):

    fig, ax = plt.subplots()
    plt.grid()
    #set grid and axes behind on top of chart elements, can also use zorder
    ax.set_axisbelow(False)
    
    #setup minor axes gridlines
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    plt.grid(b=True, which='minor', color='k', linewidth=0.1)
    plt.grid(b=True, which='major', color='k', linewidth=0.2)
    
    plt.title(title,bbox=dict(fc="0.9"))
    plt.xlabel('Date')
    plt.ylabel('Affiliated Citizens (%)')
    
    graph_keys = []
    graph_colors = []
    for i in cols:
        graph_keys.append(keys[i])
        graph_colors.append(colors[i])
    plt.stackplot(df['Date'].values,df[graph_keys].T,colors=graph_colors,labels=graph_keys)
    plt.legend()
    plt.ylim(0,130)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    
#create plots using raw data
create_stacked_plot(cols=[1,2,3])
create_stacked_plot(cols=[4,5])  
create_stacked_plot(cols=[6,7])
create_stacked_plot(cols=[1,6,7,3])

r_indep = []
d_indep = []
for i in range(len(data)):
    num = data['Republican Leaning Independents'][i] + data['Democratic Leaning Independents'][i]
    r_indep.append((data['Republican Leaning Independents'][i] / num) * 100)
    d_indep.append((data['Democratic Leaning Independents'][i] / num) * 100)

fig, ax = plt.subplots()
plt.grid()
#set grid and axes behind on top of chart elements, can also use zorder
ax.set_axisbelow(False)

#setup minor axes gridlines
ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
plt.grid(b=True, which='minor', color='k', linewidth=0.1)
plt.grid(b=True, which='major', color='k', linewidth=0.2)

plt.title('Political Leanings of Independents',bbox=dict(fc="0.9"))
plt.xlabel('Date')
plt.ylabel('Percentage of Independents (%)')
plt.stackplot(data['Date'].values,[r_indep,d_indep],colors=colors[6:],labels=keys[6:])
#plt.plot(data['Date'],r_indep,color=colors[6])
#plt.plot(data['Date'],d_indep,color=colors[7])
plt.legend()
#plt.ylim(0,130)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
    

    


