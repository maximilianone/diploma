import matplotlib.pyplot as plt
from random import *
import numpy as np
import pandas as pd

df = pd.read_excel('HPV.xlsx', usecols=[42, 43, 44, 45],
                   names=['ВПЛ', 'CIN1', 'CIN2/3', 'CC'])

HPV = np.sum(df['ВПЛ'].values.tolist())
CIN1 = np.sum(df['CIN1'].values.tolist())
CIN2 = np.sum(df['CIN1'].values.tolist())
CC = np.sum(df['CC'].values.tolist())

labels = 'ВПЛ', 'CIN1', 'CIN1',  'Вразливі', 'CC'
sizes = [HPV - 2, CIN1, CIN2, len(df['ВПЛ'].values.tolist()) - HPV - CIN1 - CIN2 - CC, CC]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
