import pandas as pd
import numpy as np

df = pd.read_excel('BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                   names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])

VPL = df['ВПЛ'].replace('так', 1).replace('ні', 0)
vpl = VPL.tolist()
CIN = df[['CIN1', 'CIN2', 'CIN3']].replace('так', 1).fillna(0)
cin = CIN.values

AGE = df['ВІК']
age = AGE.tolist()

clusters = []
counter = 0
for i in range(len(age)):
    if counter < 10 or age[i] == age[i-1]:
        counter += 1
    else:
        clusters.append(i)
        counter = 0
clusters[len(clusters) - 1] = len(age)

vpl_clusters_parts = []
for i in range(len(clusters)):
    if i == 0:
        vpl_part = np.sum(vpl[0: clusters[i]]) / clusters[i]
    else:
        vpl_part = np.sum(vpl[clusters[i - 1]: clusters[i]]) / (clusters[i] - clusters[i - 1])
    vpl_clusters_parts.append([1 - vpl_part, vpl_part])

print(vpl_clusters_parts)
parameter_matrix = []
target_matrix = []
for i in range(len(vpl_clusters_parts) - 1):
    parameter_matrix.append(vpl_clusters_parts[i])
    target_matrix.append(vpl_clusters_parts[i + 1])
parameter_matrix = np.matrix(parameter_matrix)
target_matrix = np.matrix(target_matrix)
transport_matrix = np.linalg.lstsq(parameter_matrix, target_matrix, rcond=None)[0]
print(transport_matrix)
deviation = 0
for i in range(len(vpl_clusters_parts) - 1):
    test = np.matrix(vpl_clusters_parts[i]) * transport_matrix
    print(np.sqrt(np.sum([a**2 for a in (np.asarray(test) - np.array(vpl_clusters_parts[i+1]))]) / 2), vpl_clusters_parts[i+1], test)
    deviation += np.sqrt(np.sum([a**2 for a in (np.asarray(test) - np.array(vpl_clusters_parts[i+1]))]) / 2)
print(deviation / (len(vpl_clusters_parts) - 1))
