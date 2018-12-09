import pandas as pd
import numpy as np
import copy
from random import uniform


def get_transition_matrices(df):
    hpv_all = df['ВПЛ'].replace('так', 1).replace('ні', 0)
    hpv = [hpv_all.tolist()]
    cin_hard = df[['CIN2', 'CIN3']].replace('так', 1).fillna(0).sum(axis=1)
    cin_light = df['CIN1'].replace('так', 1).fillna(0)
    cin_all = pd.concat([cin_light, cin_hard], axis=1, sort=False)
    hpv_and_cin = pd.concat([hpv_all, cin_all], axis=1, sort=False)
    cin_hpv = hpv_and_cin.loc[hpv_and_cin['ВПЛ'] == 1].drop(['ВПЛ'], axis=1).values.T.tolist()
    cin_no_hpv = hpv_and_cin.loc[hpv_and_cin['ВПЛ'] == 0].drop(['ВПЛ'], axis=1).values.T.tolist()

    age_all = df['ВІК']
    age = age_all.tolist()

    clusters = []
    counter = 0
    for i in range(len(age)):
        if counter < 15 or age[i] == age[i - 1]:
            counter += 1
        else:
            clusters.append(i)
            counter = 0
    clusters[len(clusters) - 1] = len(age)

    clusters_parts_hpv = find_cluster_parts(clusters, hpv)
    hpv_clusters = [a[1] for a in clusters_parts_hpv]
    hpv_clusters_incremental = [int(hpv_clusters[a] + np.sum(hpv_clusters[:a])) for a in range(len(hpv_clusters))]
    no_hpv_clusters = [a[0] for a in clusters_parts_hpv]
    no_hpv_clusters_incremental = [int(no_hpv_clusters[a] + np.sum(no_hpv_clusters[:a])) for a in
                                   range(len(no_hpv_clusters))]
    clusters_parts_hpv = [[a / np.sum(part) for a in part] for part in clusters_parts_hpv]
    clusters_parts_cin_hpv = find_cluster_parts(hpv_clusters_incremental, cin_hpv)
    clusters_parts_cin_hpv = [[a / np.sum(part) for a in part] for part in clusters_parts_cin_hpv]
    clusters_parts_cin_no_hpv = find_cluster_parts(no_hpv_clusters_incremental, cin_no_hpv)
    clusters_parts_cin_no_hpv = [[a / np.sum(part) for a in part] for part in clusters_parts_cin_no_hpv]

    transition_matrix_hpv, deviation_hpv = find_transition_matrix(clusters_parts_hpv, False)
    transition_matrix_cin_hpv, deviation_cin_hpv = find_transition_matrix(clusters_parts_cin_hpv, True)
    transition_matrix_cin_no_hpv, deviation_cin_no_hpv = find_transition_matrix(clusters_parts_cin_no_hpv, True, True)
    print(deviation_hpv, deviation_cin_hpv, deviation_cin_no_hpv)
    print(transition_matrix_hpv, '\n', transition_matrix_cin_hpv, '\n', transition_matrix_cin_no_hpv)


def find_transition_matrix(clusters_parts, last_is_screen, minimize_to_last=False):
    parameter_matrix = []
    target_matrix = []
    for i in range(len(clusters_parts) - 1):
        parameter_matrix.append(clusters_parts[i])
        target_matrix.append(clusters_parts[i + 1])
    parameter_matrix = np.matrix(parameter_matrix)
    target_matrix = np.matrix(target_matrix)
    transport_matrix = np.asarray(np.linalg.lstsq(parameter_matrix, target_matrix, rcond=1)[0])

    rows, columns = np.where(transport_matrix <= 0)
    for i in range(len(rows)):
        transport_matrix[rows[i]][columns[i]] = 0

    rows, columns = np.where(transport_matrix >= 1)
    for i in range(len(rows)):
        transport_matrix[rows[i]][columns[i]] = 0.9

    if last_is_screen:
        transport_matrix[len(transport_matrix) - 1] = np.zeros(len(transport_matrix))
        transport_matrix[len(transport_matrix) - 1][len(transport_matrix) - 1] = 1
    transport_matrix = optimize(clusters_parts, transport_matrix, last_is_screen, minimize_to_last)

    deviation = find_deviation(clusters_parts, transport_matrix, True)

    return transport_matrix, deviation


def find_cluster_parts(clusters, data):
    clusters_parts = []
    for i in range(len(clusters)):
        if i == 0:
            part = np.array([np.sum(a) for a in [column[0: clusters[i]] for column in data]])
        else:
            part = np.array([np.sum(a) for a in [column[clusters[i - 1]: clusters[i]] for column in data]])
        cluster_elements = clusters[i] - clusters[i - 1] if i > 0 else clusters[i]
        clusters_parts.append([*[cluster_elements - np.sum(part)], *part.tolist()])
    return clusters_parts


def find_deviation(expected, transport_matrix, to_print):
    deviation = 0
    for i in range(len(expected) - 1):
        test = np.matrix(transport_matrix) * np.matrix(expected[i]).T
        if to_print:
            print(np.sqrt(np.sum([a ** 2 for a in (np.asarray(test.T) - np.array(expected[i + 1]))]) / 2),
                  expected[i + 1], test.T)
        deviation += np.sqrt(np.sum([a ** 2 for a in (np.asarray(test.T) - np.array(expected[i + 1]))]) / 2)
    return deviation / (len(expected) - 1)


def optimize(expected, transport_matrix, last_is_screen, minimize_to_last):
    border = len(transport_matrix) if not last_is_screen else len(transport_matrix) - 1
    result = transport_matrix
    deviation = find_deviation(expected, transport_matrix, False)

    for i in range(10000):
        transport_matrix_copy = copy.deepcopy(transport_matrix)
        for j in range(border):
            for k in range(len(transport_matrix_copy[0])):
                if not k == j:
                    rand = uniform(-0.2, 0.2)
                    transport_matrix_copy[j][k] += rand
                    if transport_matrix_copy[j][k] < 0:
                        transport_matrix_copy[j][k] = 0
            min_value = 0.005 if minimize_to_last else 0.05
            if last_is_screen and transport_matrix_copy[j][len(transport_matrix_copy) - 1] < min_value:
                transport_matrix_copy[j][len(transport_matrix_copy) - 1] += min_value
                transport_matrix_copy[j][j] -= min_value
            max_value = 0.01 if minimize_to_last else 0.06
            while last_is_screen and transport_matrix_copy[j][len(transport_matrix_copy) - 1] > max_value:
                transport_matrix_copy[j][len(transport_matrix_copy) - 1] -= max_value
                transport_matrix_copy[j][j] += max_value
            transport_matrix_copy[j][j] = 1 - np.sum(transport_matrix_copy[j, :j]) - np.sum(
                transport_matrix_copy[j, j + 1:])
        new_deviation = find_deviation(expected, transport_matrix_copy, False)
        if new_deviation < deviation:
            result = transport_matrix_copy
            deviation = new_deviation
    return result
