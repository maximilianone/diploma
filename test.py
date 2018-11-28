import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter
import numpy as np

df = pd.read_excel('BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                   names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])

HPV = df[['ВІК', 'ВПЛ']]
HPV = HPV[HPV['ВПЛ'] != 'ні']
CIN1 = df[['ВІК', 'CIN1']].dropna()
CIN2 = df[['ВІК', 'CIN2']].dropna()
CIN3 = df[['ВІК', 'CIN3']].dropna()
CC = df[['ВІК', 'CC']].dropna()
labels = 'ВПЛ', 'CIN1', 'CIN1',  'Вразливі', 'CC'

fig1, ax1 = plt.subplots()
ax1.hist(HPV['ВІК'].tolist(), 20, weights=np.ones(len(HPV['ВІК'].tolist())) / len(HPV['ВІК'].tolist()))

plt.xlabel('Вік')
plt.ylabel('Люди %')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

fig1, ax1 = plt.subplots()
ax1.hist(CIN1['ВІК'].tolist(), 20, weights=np.ones(len(CIN1['ВІК'].tolist())) / len(CIN1['ВІК'].tolist()))

plt.xlabel('Вік')
plt.ylabel('Люди %')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

fig1, ax1 = plt.subplots()
ax1.hist(CIN2['ВІК'].tolist(), 20, weights=np.ones(len(CIN2['ВІК'].tolist())) / len(CIN2['ВІК'].tolist()))

plt.xlabel('Вік')
plt.ylabel('Люди %')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

fig1, ax1 = plt.subplots()
ax1.hist(CIN3['ВІК'].tolist(), 20, weights=np.ones(len(CIN3['ВІК'].tolist())) / len(CIN3['ВІК'].tolist()))

plt.xlabel('Вік')
plt.ylabel('Люди %')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

fig1, ax1 = plt.subplots()
ax1.hist(CC['ВІК'].tolist(), 20, weights=np.ones(len(CC['ВІК'].tolist())) / len(CC['ВІК'].tolist()))

plt.xlabel('Вік')
plt.ylabel('Люди %')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()
