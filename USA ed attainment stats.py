# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:34:50 2019

@author: usrsolo
"""

import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
import seaborn as sns

#set plot properties
sns.set(font_scale=3)
sns.set_style("whitegrid")
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':15,
                     'font.weight':'bold',
                     'axes.titleweight':'bold','axes.labelweight':'bold',
                     'grid.color':'k','axes.edgecolor':'k',
                     'lines.markersize':30,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1})

folder = r'C:\Users\usrsolo\Documents\Rose Random\education attainment stats'

#create a plot for a given education attainment level and age group
def create_plot(ed_attainment,age,fignum):
    time = [] #year for each data point
    stats = [] #percentage of us pop with inputted ed attainment at inputted age group
    #loop through all the files with education attainment data in folder
    files = listdir(folder)
    for f in files:
        if f[:20] == 'education attainment':
            file = folder + '\\' + f
            year = int(f[20:25])
            # read in data (make sure a df has been created)
            df = pd.read_excel(io = file, header=5).iloc[:21]
            #the raw data is not consistently structured year to year so
            #need to adjust how reading in the data depending on year
            if year > 2002:
                #read in data from excel file skipping header lines
                #and only reading the next 21 lines
                df = pd.read_excel(io = file, header=5).iloc[:21]
                df = df.reset_index()
            else:
                #need to concatenate two tables of data from excel file
                a = pd.read_excel(io = file, header=5).iloc[:21]
                a = a.reset_index()
                b = pd.read_excel(io = file, header=38).iloc[:21]
                b = b.reset_index()
                frames = [a,b]
                df = pd.concat(frames)
                df = df.reset_index()
                
            #find the correct key label for the inputted age grop
            age_label= ''
            for row in range(len(df['index'])):
                name = str(df['index'][row])
                if age.lower() in name.lower():
                    age_label = row
            total = df['Total'][age_label] #total us pop in age group
            #find the correct key label for the inputted ed attainment
            ed_label = ''
            for key in df:
                if ed_attainment.lower() in key.lower():
                    ed_label = key
            data = df[ed_label][age_label]
            time.append(year)
            stats.append(data/total*100)
        
    plt.figure(fignum)
    plt.xlabel('Year')
    plt.ylabel('% of US Pop. Aged ' + age)
    plt.title(ed_attainment + ' Level Education for People Aged ' + age, bbox=dict(fc="0.9"))
    plt.plot(time,stats,'.-')
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()  

#create a plot for a given age group showing breakdown of ed attainment ranges
def degree_check(age,fignum):
    time = [] #year for each data point
    stats = [[],[],[]] #series of stats for each ed attainment range
    files = listdir(folder)
    #loop through all the files with education attainment data in folder
    for f in files:
        if f[:20] == 'education attainment':
            file = folder + '\\' + f
            year = int(f[20:25])
            # read in data (make sure a df has been created)
            df = pd.read_excel(io = file, header=5).iloc[:21]
            #the raw data is not consistently structured year to year so
            #need to adjust how reading in the data depending on year
            if year > 2002:
                #read in data from excel file skipping header lines
                #and only reading the next 21 lines
                df = pd.read_excel(io = file, header=5).iloc[:21]
                df = df.reset_index()
            else:
                #need to concatenate two tables of data from excel file
                a = pd.read_excel(io = file, header=5).iloc[:21]
                a = a.reset_index()
                b = pd.read_excel(io = file, header=38).iloc[:21]
                b = b.reset_index()
                frames = [a,b]
                df = pd.concat(frames)
                df = df.reset_index()
                
            #find the correct key label for the inputted age grop
            age_label= ''
            for row in range(len(df['index'])):
                name = str(df['index'][row])
                if age.lower() in name.lower():
                    age_label = row
            total = df['Total'][age_label] #total us pop in age group
            some_college = 0 #us pop with some college but no degree
            post_secondary = [] #us pop with any post-secondary degree
            bmd = [] #us pop with a bachelor, masters, or doctorate degree
            for key in df:
                if 'degree' in key.lower() and 'some college' not in key.lower():
                    post_secondary.append(df[key][age_label])
                    if 'bachelor' in key.lower() or \
                        'master' in key.lower() or \
                        'doctor' in key.lower():
                        bmd.append(df[key][age_label])
                if 'some college' in key.lower():
                    some_college = df[key][age_label]
                    
            all_degree = sum(post_secondary)
            bmd_degree = sum(bmd)
            atleast_sc = some_college + all_degree
            time.append(year)
            stats[0].append(atleast_sc/total*100)
            stats[1].append(all_degree/total*100)
            stats[2].append(bmd_degree/total*100)
        
    plt.figure(fignum)
    plt.xlabel('Year')
    plt.ylabel('% of US Pop. Aged ' + age)
    plt.title('Post-Secondary Education for People Aged ' + age, bbox=dict(fc="0.9"))
    plt.plot(time,stats[0],'.-')
    plt.plot(time,stats[1],'.-')
    plt.plot(time,stats[2],'.-')
    plt.ylim(20,80)
    plt.legend(['At least some college',
                'All post-secondary degrees',
                'Bachelor, master, doctorate degrees'])
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()   
    
ed_attainment = 'Some College'
age = '25 Years and Over'
create_plot(ed_attainment,age,1)
age = '25 to 29 Years'
create_plot(ed_attainment,age,2)
ed_attainment = 'Bachelor'
age = '25 Years and Over'
create_plot(ed_attainment,age,3)
age = '25 to 29 Years'
create_plot(ed_attainment,age,4)
    
age = '25 Years and Over'
degree_check(age,5)
age = '25 to 29 Years'
degree_check(age,6)