# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 08:47:49 2019

@author: usrsolo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import linregress
import numpy as np

sns.set(font_scale=2.1)
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':15,
                     'legend.frameon':True,'legend.framealpha':1,
                     'legend.facecolor':'w'})

file_T10Y2Y = r'C:\Users\usrsolo\Documents\Rose Random\T10Y2Y yield spread data.csv'
file_T10Y3M = r'C:\Users\usrsolo\Documents\Rose Random\T10Y3M yield spread data.csv'
file_recession = r'C:\Users\usrsolo\Documents\Rose Random\recession data.csv'

data_T10Y2Y = pd.read_csv(file_T10Y2Y,parse_dates=['observation_date'])
data_T10Y3M = pd.read_csv(file_T10Y3M,parse_dates=['observation_date'])
data_recession = pd.read_csv(file_recession)

#convert all dates to datetime type
for key in data_recession:
    for i in range(len(data_recession)):
        data_recession[key][i] = datetime.strptime(data_recession[key][i],
                      '%Y-%m-%d')

#plot yield spread over time with recession years highlighted
def plot_data(data):
    keys = list(data.keys())
    name = keys[1]
    plt.plot(data['observation_date'],data[name])

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()    
plot_data(data_T10Y2Y)
plot_data(data_T10Y3M)
#vertical band for each recession from/to
for i in range(len(data_recession)):
    plt.axvspan(data_recession['From'][i],data_recession['To'][i],
                color='k',alpha=.1)
plt.xlabel('Date')
plt.ylabel('Yield Spread')
plt.title('US Yield Spread as Predictor of Recession',bbox=dict(fc="0.9"))
plt.legend(['T10Y2Y Spread','T10Y3M Spread'])
plt.text(.835,.025,'Vertical Bands\nIndicate Recessions',
         bbox=dict(facecolor='w'),transform=ax.transAxes)

#determine by how long a yield curve inversion predated the start of a recession
def analyze_data(data,r):
    keys = list(data.keys())
    name = keys[1]
    predate = [] #list of timelengths inversion predated next recession
    #loop through yield spread data
    i = 0
    while i < len(data) and r < 5:
        #if spread falls below 0 record inversion date
        if data[name][i] < 0:
            inversion = data['observation_date'][i] #inversion date
            recession = data_recession['From'][r] #recession date
            time_length = recession - inversion
            time_length = time_length.days/30 #convert to ~months
            predate.append(time_length)
            text = f'The {name} spread inversion predated the ' + \
            f'{data_recession["From"][r].year} recession by ' + \
            f'{int(np.round(time_length))} months'
            print(text)
            #go through the rest of yield spread data that was recorded during
            #the recession to ignore the inverted datapoints after the initial
            #inversion
            for j in range(i,len(data)):
                if data['observation_date'][j] > data_recession['To'][r]:
                    r+=1
                    i = j
                    break
        i+=1
    return predate

predate_T10Y2Y = analyze_data(data_T10Y2Y,0)
predate_T10Y3M = analyze_data(data_T10Y3M,1)

def daily_yield_curve_analysis():

    yield_curve_file = r'C:\Users\usrsolo\Documents\Rose Random\yield curve rates data.csv'
    yield_curve_data = pd.read_csv(yield_curve_file)
    
    #only want to show so many ylabels on plot otherwise too crowded
    keys = list(yield_curve_data.keys())
    ylabels = []
    #create labels only for years (ignore m/d/)
    for i in range(len(yield_curve_data['Date'])):
        date = yield_curve_data['Date'][i]
        year = int(date[len(date)-4:len(date)])
        ylabels.append(year)
    #get rid of redundant years and slim down labels by mod 2
    for y in range(len(ylabels)-1,1,-1):
        if ylabels[y] == ylabels[y-1] or ylabels[y] % 2 != 0:
            ylabels[y] = ''
        
    #convert dates to datetime type
    dates = []
    for date in yield_curve_data['Date']:
        dates.append(datetime.strptime(date,'%m/%d/%Y'))
    yield_curve_data['Date'] = dates
    
    #determine position of date for start and end of recession along yaxis
    #used to then plot start and end recession lines to indicate recession on
    #plot
    recession_lines = [[],[]]     
    for r in range(2,len(data_recession)):
        for i in range(len(yield_curve_data)):
            time_length = yield_curve_data['Date'][i] - data_recession['From'][r]
            time_length = time_length.days
            if time_length >= 0:
                recession_lines[0].append(len(yield_curve_data)-i)
                break
        for i in range(len(yield_curve_data)):
            time_length = yield_curve_data['Date'][i] - data_recession['To'][r]
            time_length = time_length.days
            if time_length >=0:
                recession_lines[1].append(len(yield_curve_data)-i)
                break
            
    #plot a heatmap of the yield curve over time
    #color = sns.palplot(sns.light_palette("navy", reverse=True))
    fig, ax = plt.subplots()  
    hm = sns.heatmap(yield_curve_data[keys[1:]],yticklabels=ylabels,
                     cmap="YlGnBu",cbar_kws={'label': '%Yield'})
    plt.yticks(rotation=0)
    hm.hlines(recession_lines[0],*hm.get_xlim(),color='r')
    hm.hlines(recession_lines[1],*hm.get_xlim(),color='purple')
    plt.title('US Daily Yield Curve Over Time',bbox=dict(fc="0.9"))
    plt.xlabel('Treasury Note')
    plt.ylabel('Date')
    plt.legend(['Recession Start','Recession End'])#bbox_to_anchor=(1.2,1))
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    
    #determine the slope of a yield curve at each date
    yield_curve_slopes = []
    for i in range(len(yield_curve_data)):
        treasury_bills = [.25,.5,1,2,3,5,7,10,20,30] #time for tbills in years
        yields = []
        for key in keys[1:]:
            yields.append(yield_curve_data[key][i])
        #get rid of nans that will throw off linreg calc
        shift_yields = []
        shift_tbills = []
        for j in range(len(yields)):
            if not np.isnan(yields[j]):
                shift_yields.append(yields[j])
                shift_tbills.append(treasury_bills[j])
            
        lin_reg = linregress(shift_tbills,shift_yields)
        yield_curve_slopes.append(lin_reg.slope)
        
    #plot slope v time
    fig, ax = plt.subplots()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.plot(yield_curve_data['Date'],yield_curve_slopes)
    for i in range(2,len(data_recession)):
        plt.axvspan(data_recession['From'][i],data_recession['To'][i],
                    color='k',alpha=.1)
    #plt.xticks(rotation=70)
    plt.title('US Daily Yield Curve Linear Regression Slope Over Time',
              bbox=dict(fc="0.9"))
    plt.xlabel('Date')
    plt.ylabel('Slope (%yield/maturity years)')
    plt.text(.835,.025,'Vertical Bands\nIndicate Recessions',
             bbox=dict(facecolor='w'),transform=ax.transAxes)

def yearly_yield_curve_analysis():
    
    yield_curve_file = r'C:/Users/usrsolo/Documents/Rose Random/US treasury bill yield curve rates data yearly averages.csv'
    yield_curve_data = pd.read_csv(yield_curve_file)
    keys = list(yield_curve_data.keys())
    years = list(yield_curve_data['Year'])
    #only want to show so many ylabels on plot otherwise too crowded
    for y in range(len(years)):
        if years[y] % 5 != 0:
            years[y] = ''
            
    #set up plot loc for recession years
    recession_years = [1953,1958,1960,1970,1973,1980,1981,1990,2001,2008]
    r_lines = []
    for year in recession_years:
        r_lines.append(2011-year)
        
    spread10Y3M = yield_curve_data['10-year'] - yield_curve_data['3-month']
    spread10Y3Y = yield_curve_data['10-year'] - yield_curve_data['3-year']
    #plot spread v time
    fig, ax = plt.subplots()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.plot(yield_curve_data['Year'],spread10Y3Y)
    plt.plot(yield_curve_data['Year'],spread10Y3M)
    for r in recession_years:
        rec = plt.axvline(x=r,color='r')
    plt.title('US Yearly Average Yield Spread Over Time',bbox=dict(fc="0.9"))
    plt.xlabel('Date')
    plt.ylabel('Yield Spread')
    plt.legend(['T10Y3Y Spread','T10Y3M Spread','Recession'],loc='upper left')
    
    #plot a heatmap of the yield curve over time
    fig, ax = plt.subplots()    
    hm2 = sns.heatmap(yield_curve_data[keys[1:]],yticklabels=years,
                      cmap="YlGnBu",cbar_kws={'label': '%Yield'})
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.yticks(rotation=0)
    hm2.hlines(r_lines,*hm2.get_xlim(),color='r')
    plt.title('US Yearly Average Yield Curve Over Time',bbox=dict(fc="0.9"))
    plt.xlabel('Treasury Note')
    plt.ylabel('Date')
    plt.legend(['Recession'])
    
    #determine the slope of a yield curve at each date
    yield_curve_slopes = []
    for i in range(len(yield_curve_data)):
        treasury_bills = [.25,.5,3,10,30]
        yields = []
        for key in keys[1:]:
            yields.append(yield_curve_data[key][i])
        shift_yields = []
        shift_tbills = []
        for j in range(len(yields)):
            if not np.isnan(yields[j]):
                shift_yields.append(yields[j])
                shift_tbills.append(treasury_bills[j])
            
        lin_reg = linregress(shift_tbills,shift_yields)
        yield_curve_slopes.append(lin_reg.slope)
    
    #plot slope v time
    fig, ax = plt.subplots()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.plot(yield_curve_data['Year'],yield_curve_slopes)
    for r in recession_years:
        rec = plt.axvline(x=r,color='r')
    plt.title('US Yearly Average Yield Curve Linear Regression Slope Over Time',
              bbox=dict(fc="0.9"))
    plt.xlabel('Date')
    plt.ylabel('Slope (%yield/maturity years)')
    plt.legend([rec],['Recession'])
    
daily_yield_curve_analysis()
yearly_yield_curve_analysis()
  