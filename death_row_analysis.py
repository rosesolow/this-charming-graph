# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:50:00 2020

@author: roses

death_row_analysis

analysis of people in US sentenced to death since 1976

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale=2.5)
sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':10,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':15,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1})

file = r'C:\Users\roses\Desktop\Rose Random\data visualization projects\death row stats\the-condemned-data-master\the-condemed-data.csv'
data = pd.read_csv(file)
#fill all nan values with 'No Data' text (makes easier to search/sort)
df = data.fillna('No Data')

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
df.groupby('gender')['full_name'].nunique().plot(kind='bar',rot=0)
plt.title('Number of People Sentenced to Death in US by Gender since 1976',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
#clean up data by replacing duplicate values with ' ' on end 
#by truncating last char (ie 'White' and 'White ')
for i in range(len(df['race'])):
    if df['race'][i][len(df['race'][i])-1] == ' ':
        df['race'][i] = df['race'][i][:len(df['race'][i])-1]
df.groupby('race')['full_name'].nunique().plot(kind='bar',rot=0)
#need to wrap xtick labels because they are too long and smash into each other
#unfortunately there is no autowrap for tick labels so need to do manually
labels = ax.get_xticklabels()
wrapped_labels = [ l.get_text().replace(' ', '\n') for l in labels ]
ax.set_xticklabels(wrapped_labels)
#add some whitespace below the plot to fit all the newly wrapped labels
fig.subplots_adjust(bottom=0.2)
plt.title('Number of People Sentenced to Death in US by Race since 1976',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
#clean up data (duplicate 'Y' and 'Y ' vals) by re-entering more descriptive
#values for No Data and Y within resentenced column
for i in range(len(df['resentenced'])):
    if df['resentenced'][i] != 'No Data':
        df['resentenced'][i] = 'Resentenced'
    else:
        df['resentenced'][i] = 'Not Resentenced'
df.groupby('resentenced')['full_name'].nunique().plot(kind='bar',rot=0)
plt.title('Number of People Sentenced to Death in US and Later Resentenced ' +
          'since 1976',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
#clean up data (duplicate 'On' vs 'on')
for i in range(len(df['Status'])):
    if df['Status'][i] == 'Not Currently On Death Row':
        df['Status'][i] = 'Not Currently on Death Row'
df.groupby('Status')['full_name'].nunique().plot(kind='bar',rot=0)
plt.title('Number of People Sentenced to Death in US by Current Status ' +
          'since 1976',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
bytime = df.groupby('sentencing_year')['full_name'].nunique()
#get rid of last data point as this is the No Data count with no year
bytime = bytime[:len(bytime)-1]
bytime.plot(kind='line')
plt.title('Number of People Sentenced to Death in US each Year since 1976',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
#calculate the running total of death sentencing
running_total = []
total = 0
for count in bytime:
    total+=count
    running_total.append(total)
plt.plot(bytime.index,running_total)
plt.xlabel('Year')
plt.title('Number of People Sentenced to Death in US over Time since 1976 ' +
          '(Running Total)',
          bbox=dict(fc="0.9"))

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
#sort values so bar chart goes from low to high, more readable
bystate = df.groupby('state')['full_name'].nunique().sort_values()
bystate.plot(kind='bar')
fig.subplots_adjust(bottom=0.25)
plt.title('Total Number of People Sentenced to Death in US by State ' +
          'since 1976',
          bbox=dict(fc="0.9"))
