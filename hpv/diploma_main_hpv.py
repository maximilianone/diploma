import pandas as pd
from hpv.statistic_processor import get_transition_matrices
import numpy as np
import copy
from random import uniform

df = pd.read_excel('../BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                   names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])
# get_transition_matrices(df)

hpv_all = df['ВПЛ'].replace('так', 1).replace('ні', 0).values
cin_hard = df[['CIN2', 'CIN3']].replace('так', 2).fillna(0).sum(axis=1)
cin_light = df['CIN1'].replace('так', 1).fillna(0)
cin_all = pd.concat([cin_light, cin_hard], axis=1, sort=False).sum(axis=1).values

hpv_transition_matrix = [[0.72686798, 0.27313202], [0.46668473, 0.53331527]]
cin_hpv_transition_matrix = [[0.34725057, 0.55318269, 0.09956675],
                             [0.8750524, 0.06654774, 0.05839987],
                             [0.0, 0.0, 1.0]]
cin_no_hpv_transition_matrix = [[0.81262258, 0.1305708, 0.05680661],
                                [0.21128755, 0.52144082, 0.26727163],
                                [0.0, 0.0, 1.0]]


