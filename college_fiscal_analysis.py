# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 12:03:19 2019

@author: usrsolo
"""

import pandas as pd
import matplotlib.pyplot as plt

#set plot properties
plt.rcParams.update({'axes.titlepad':35,'axes.labelpad':15,
                     'axes.grid':True,
                     'font.size':25,'font.weight':'bold',
                     'lines.markersize':30,'lines.linewidth':3,
                     'legend.frameon':True,'legend.framealpha':1})

file = r'C:\Users\usrsolo\Documents\Rose Random\Tuitions\college fiscal data.xlsx'
xls = pd.ExcelFile(file)

h = ['','/','.','+','*','\\','-', '|', 'O', 'x','o']
pie = 'Private and affiliated gifts, grants, contracts, investment returns, and endowment income (PIE) '

def plot_by_inst_type(inst_type,data_type,ykey,allother):
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    #determine all the institution types to group by
    groups = []
    for sheet in xls.sheet_names:
        if inst_type in sheet:
            groups.append(sheet)
    for g in range(len(groups)):
        #read each sheet as dataframe from excel file
        #set the index to year and then transpose for more readable dataframe
        df = xls.parse(groups[g]).set_index('Year').T
        df = df.loc[:,~df.columns.duplicated()] #get rid of duplicated cols
        df['Year'] = df.index 
        df.reset_index(inplace=True,drop=True)
        df['Profit'] = df['Total operating revenue '] - \
        df['Total operating expenditures ']
        width = .8 / len(groups) #width of bars for chart
        years = list(df['Year'])
        #determine xtick shift for grouped bars
        shift = -len(groups)*width/2 + g*width + width/2
        x = [y + shift for y in years]
        bottom = 0 #bottom y vals for stacked bars
        for d in range(len(data_type)):
            dtype = data_type[d]
            #if multiple data types want to stack
            if d > 0:
                bottom = bottom + df[data_type[d-1]]
            if dtype == pie:
                label = 'PIE'
            else:
                label = dtype
            plt.bar(x,df[dtype],width,bottom,label=groups[g] + ' ' + label,
                    color = f'C{d}',hatch=h[g],
                    edgecolor='k')
            last_recorded = df[dtype] + bottom
        #if want to plot all other rev/exp to have total
        if allother:
            df['All Other ' + ykey] = df[f'Total operating {ykey.lower()} '] \
            - last_recorded
            plt.bar(x,df['All Other ' + ykey],width,last_recorded,
                    label=groups[g] + ' All Other ' + ykey, color = f'C{d+1}',
                    hatch=h[g],edgecolor='k')   

    plt.title(f'US College Fiscal Data {inst_type} Institution {ykey}',
              bbox=dict(fc="0.9"))
    plt.xlabel('Years')
    plt.ylabel(f'Average {ykey} per FTE Student (in 2013 dollars)')
    plt.legend()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    ymax = max(ax.get_ylim())
    ymin = min(ax.get_ylim())
    plt.ylim(ymin,ymax+ymax/10*len(groups)*(len(data_type)+1))
    
plot_by_inst_type('Bachelor',
                  ['Net tuition '],
                  'Revenue',False)

plot_by_inst_type('Master',
                  ['Net tuition '],
                  'Revenue',False)

plot_by_inst_type('Research',
                  ['Net tuition '],
                  'Revenue',False)

plot_by_inst_type('Inst',
                  ['Net tuition '],
                  'Revenue',False)

plot_by_inst_type('Bachelor',
                  [pie],
                  'Revenue',False)

plot_by_inst_type('Bachelor',
                  ['State and local appropriations '],
                  'Revenue',False)

plot_by_inst_type('Bachelor',
                  ['Instruction '],
                  'Expenditures',False)

plot_by_inst_type('Master',
                  [pie],
                  'Revenue',False)

plot_by_inst_type('Research',
                  [pie],
                  'Revenue',False)

plot_by_inst_type('Bachelor',
                  ['Net tuition ','State and local appropriations ',pie],
                  'Revenue',True)

plot_by_inst_type('Bachelor',
                  ['Instruction ','Student services ','Institutional support '],
                  'Expenditures',True)

plot_by_inst_type('Master',
                  ['Net tuition ','State and local appropriations ',pie],
                  'Revenue',True)

plot_by_inst_type('Master',
                  ['Instruction ','Student services ','Institutional support '],
                  'Expenditures',True)

plot_by_inst_type('Research',
                  ['Net tuition ','State and local appropriations ',pie],
                  'Revenue',True)

plot_by_inst_type('Research',
                  ['Instruction ','Research '],
                  'Expenditures',True)

plot_by_inst_type('Bachelor',['Profit'],'Profit',False)
plot_by_inst_type('Bachelor',['Net tuition ','Profit'],'',False)

def plot_rev_v_exp(inst_type,rev_type,exp_type,ymax,allother):
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    #determine all the institution types to group by
    for sheet in xls.sheet_names:
        if inst_type in sheet:
            #read each sheet as dataframe from excel file
            #set the index to year and then transpose for more readable dataframe
            df = xls.parse(sheet).set_index('Year').T
            df = df.loc[:,~df.columns.duplicated()] #get rid of duplicated cols
            df['Year'] = df.index 
            df.reset_index(inplace=True,drop=True)
            df['Profit'] = df['Total operating revenue '] - \
            df['Total operating expenditures ']
            width = .8 / 2 #width of bars for chart
            years = list(df['Year'])
            
            #plot revenues, stacked
            #xtick shift for grouped bars
            shift = -width/2
            x = [y + shift for y in years]
            bottom = 0 #bottom y vals for stacked bars
            for r in range(len(rev_type)):
                rtype = rev_type[r]
                #if multiple data types want to stack
                if r > 0:
                    bottom = bottom + df[rev_type[r-1]]
                if rtype == pie:
                    label = 'PIE'
                else:
                    label = rtype
                plt.bar(x,df[rtype],width,bottom,label=sheet + ' ' + label,
                        edgecolor='k')
                last_recorded = df[rtype] + bottom
            if allother:
                df['All Other Revenue'] = df[f'Total operating revenue '] \
                - last_recorded
                plt.bar(x,df['All Other Revenue'],width,last_recorded,
                        label=sheet + ' All Other Revenue', edgecolor='k')
            
            #plot expenditures, stacked
            shift = width/2
            x = [y + shift for y in years]
            bottom = 0
            for e in range(len(exp_type)):
                etype = exp_type[e]
                label = etype
                if e > 0:
                    bottom = bottom + df[exp_type[e-1]]
                plt.bar(x,df[etype],width,bottom,label=sheet + ' ' + label,
                        edgecolor='k',hatch='/')
                last_recorded = df[etype] + bottom
            if allother:
                df['All Other Expenditures'] = df[f'Total operating expenditures '] \
                - last_recorded
                plt.bar(x,df['All Other Expenditures'],width,last_recorded,
                        label=sheet + ' All Other Expenditures',
                        edgecolor='k',hatch='/')   

    plt.title(f'US College Fiscal Data {inst_type} Institution Revenue v Expenditures',
              bbox=dict(fc="0.9"))
    plt.xlabel('Years')
    plt.ylabel(f'Average $ per FTE Student (in 2013 dollars)')
    plt.legend()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.ylim(0,ymax)
    
plot_rev_v_exp('Public Bachelor',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Student services '],75000,True)
plot_rev_v_exp('Private Bachelor',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Student services '],75000,True)

plot_rev_v_exp('Public Master',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Student services '],50000,True)
plot_rev_v_exp('Private Master',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Student services '],50000,True)

plot_rev_v_exp('Public Research',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Research '],200000,True)
plot_rev_v_exp('Private Research',
               ['Net tuition ','State and local appropriations ',pie],
               ['Instruction ','Research '],200000,True)

plot_rev_v_exp('Public Bachelor',['Net tuition '],['Profit'],20000,False)
plot_rev_v_exp('Private Bachelor',['Net tuition '],['Profit'],20000,False)
plot_rev_v_exp('Public Master',['Net tuition '],['Profit'],20000,False)
plot_rev_v_exp('Private Master',['Net tuition '],['Profit'],20000,False)
plot_rev_v_exp('Public Research',['Net tuition '],['Profit'],50000,False)
plot_rev_v_exp('Private Research',['Net tuition '],['Profit'],50000,False)
