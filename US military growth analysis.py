# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:18:52 2019

@author: usrsolo
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':20,'axes.titlepad':30,'axes.labelpad':20})

file = r'C:\Users\usrsolo\Documents\Rose Random\growth of us military over time raw data.csv'
data = pd.read_csv(file)
war_dates = [1814,1847,1864,1898,1918,1945,1952,1968,1982]
war_labels = ['War of 1812','Mexican War','Civil War','Spanish War','WWI','WWII','Korean War','Vietnam War','Cold War']

fig, ax = plt.subplots()
plt.grid()
ax.set_axisbelow(True) #sets grid and axes behind chart elements, can also use zorder

#setup major/minor axis gridlines
ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
plt.grid(b=True, which='minor', color='k', linewidth=0.1)

plt.bar(data['Year'],data['Military/Pop'])
plt.title('Percentage of Total US Population in Military Over Time',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('Percentage of Total US Pop. in Military (%)')

#set labels for major wars in US history
for i in range(len(war_dates)):
    loc = war_dates[i] - data['Year'][0]
    plt.annotate(war_labels[i],
                 xy=(war_dates[i],data['Military/Pop'][loc]),
                 xytext=(war_dates[i]-4,data['Military/Pop'][loc]+.15),
                 backgroundcolor='w',
                 bbox=dict(fc="0.99"),
                 fontsize=14.5)
    
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

fig, ax = plt.subplots()
plt.grid()
ax.set_axisbelow(True) #sets grid and axes behind chart elements, can also use zorder

#setup major/minor axis gridlines
ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
plt.grid(b=True, which='minor', color='k', linewidth=0.1)
#set y axis ticks as multiples of 1mil
tick_format = mpl.ticker.FuncFormatter(lambda x, pos: x/1000000)
ax.yaxis.set_major_formatter(tick_format)

plt.bar(data['Year'],data['Total Military'])
plt.title('Size of US Military Over Time',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('No. of US Military Members (in Millions)')

#set labels for major wars in US history
for i in range(len(war_dates)):
    loc = war_dates[i] - data['Year'][0]
    plt.annotate(war_labels[i],
                 xy=(war_dates[i],data['Total Military'][loc]),
                 xytext=(war_dates[i]-4,data['Total Military'][loc]+250000),
                 backgroundcolor='w',
                 bbox=dict(fc="0.99"),
                 fontsize=14.5)
    
mng = plt.get_current_fig_manager()
mng.window.showMaximized()