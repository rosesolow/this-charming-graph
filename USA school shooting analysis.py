# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=2.5)
sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':15,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':15,'lines.linewidth':2,
                     'legend.frameon':True,'legend.framealpha':1})

file = r'C:\Users\roses\Desktop\Rose Random\data visualization projects\USA school shootings analysis\USA school shootings stats.csv'
data = pd.read_csv(file)

#print(data.keys())

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
plt.plot(data['Year'],data['Number of Incidents'],'.-')
plt.title('USA School Shootings',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('Number of Incidents')

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
plt.plot(data['Year'],data['Killed (includes shooter)'],'.-')
plt.plot(data['Year'],data['Injured Victims (not killed)'],'.-')
plt.plot(data['Year'],data['Total Injured/Killed Victims'],'.-')
plt.title('USA School Shootings',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.legend(['Number of Fatalities','Number of Injured','Number of Victims'])

fig, ax = plt.subplots()
mng = plt.get_current_fig_manager()
mng.window.showMaximized() 
plt.plot(data['Year'],data['Fatalities/Incident'],'.-')
plt.plot(data['Year'],data['Injured Victims/Incident'],'.-')
plt.plot(data['Year'],data['Victims/Incident'],'.-')
plt.title('USA School Shootings',bbox=dict(fc="0.9"))
plt.xlabel('Year')
plt.ylabel('')
plt.legend(['Fatalities/Incident','Injured Victims/Incident',
            'Victims/Incident'])
