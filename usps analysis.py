# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 12:02:22 2020

@author: roses
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale=2.5)
#sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':10,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':15,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1,
                     'legend.facecolor':'w'})

file = r'C:\Users\roses\Desktop\Rose Random\data visualization projects\usps analysis\usps raw data.csv'
data = pd.read_csv(file)
data['Non-Marketing Mail Volume (Billions)'] = data['Mail Volume (Billions)'] \
    - data['Marketing Mail Volume (Billions)']
keys = list(data.keys())

def create_plot(dname,title):
    fig, ax = plt.subplots()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized() 
    plt.plot(data['Year'],data[dname],'.-')
    plt.title(title,bbox=dict(fc="0.9"))
    plt.xlabel('Year')
    plt.ylabel(dname)
    
create_plot('Mail Volume (Billions)','USPS Mail Volume')
create_plot('Marketing Mail Volume (Billions)','USPS Marketing Mail Volume')
create_plot('Shipping/Package Volume (Billions)','USPS Shipping/Package Volume')

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
graph_keys = []
cols = [7,19]
for i in cols:
    graph_keys.append(keys[i])
plt.stackplot(data['Year'],data[graph_keys].T,labels=graph_keys,alpha=.9)
plt.legend()
plt.ylim(0,200)
plt.title('USPS Mail Volume',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('Mail Volume (Billions)')

create_plot('Career Employees','USPS Career Employees')
create_plot('Vehicles','USPS Vehicles')
create_plot('Delivery Routes','USPS Delivery Routes')

create_plot('Total Retail Revenue (Billions of $)','USPS Total Retail Revenue')
create_plot('Annual Operating Revenue (Billions of $)','USPS Annual Operating Revenue')

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
graph_keys = []
cols = [1,13]
for i in cols:
    graph_keys.append(keys[i])
plt.plot(data['Year'],data[graph_keys],'.-')
plt.legend(graph_keys)
plt.ylim(0,100)
plt.title('USPS Revenue',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('Revenue (Billions of $)')

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
graph_keys = []
cols = [14,15]
for i in cols:
    graph_keys.append(keys[i])
plt.stackplot(data['Year'],data[graph_keys].T,labels=graph_keys,alpha=.9)
plt.legend()
plt.ylim(0,25)
plt.title('USPS Retail Revenue',bbox=dict(fc="0.9"))
plt.ylabel('Retail Revenue (Billions of $)')
plt.xlabel('Year')
