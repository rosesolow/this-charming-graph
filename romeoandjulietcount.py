# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 12:18:13 2024

@author: roses
"""

import pandas as pd
import matplotlib.pyplot as plt

filename = r'C:\Users\roses\Documents\Python Scripts\romeoandjulietcount.xlsx'

romeoandjuliet = pd.read_excel(filename)
romeoandjuliet = romeoandjuliet.astype(str)

love = [[],[],[]]
death = [[],[],[]]
lines = [[],[]]

for i in romeoandjuliet.index:
    line = romeoandjuliet['Romeo and Juliet'][i]
    if 'love' in line or 'Love' in line:
        love[0].append(i)
        love[1].append(line)
        love[2].append(1)
        
        lines[0].append(i)
        lines[1].append(line)
    if 'death' in line or 'Death' in line:
        death[0].append(i+.5)
        death[1].append(line)
        death[2].append(1)
        
        lines[0].append(i+.5)
        lines[1].append(line)
        
fig, ax = plt.subplots()
ax.bar(love[0],love[2],facecolor='r',width=5)
ax.bar(death[0],death[2],facecolor='k',width=5)

ax.set_xticklabels(lines[1])
plt.xticks(lines[0],rotation=90)
for j in range(len(lines[0])):
    if 'love' in lines[1][j] or 'Love' in lines[1][j]:
        ax.get_xticklabels()[j].set_color("red")

plt.subplots_adjust(left=0.01, right=0.99, 
                    top=.9, bottom=.5)
plt.tick_params(labelleft=False, left=False)

ax.set_title('Mentions of love and death throughout the progression of Romeo and Juliet')
