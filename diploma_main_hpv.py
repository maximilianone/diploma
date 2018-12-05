import pandas as pd

df = pd.read_excel('BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                   names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])

VPL = df[['ВІК', 'ВПЛ']]
CIN = df[['ВІК', 'CIN1', 'CIN2', 'CIN3', 'CC']]
