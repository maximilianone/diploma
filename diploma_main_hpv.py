import pandas as pd
import numpy as np
import copy
from random import uniform


def main():
    df = pd.read_excel('BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                       names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])

    VPL = df['ВПЛ'].replace('так', 1).replace('ні', 0)
    vpl = [VPL.tolist()]
    CIN = df[['CIN1', 'CIN2', 'CIN3']].replace('так', 1).fillna(0)
    cin = np.transpose(np.array(CIN.values.tolist())).tolist()

    AGE = df['ВІК']
    age = AGE.tolist()

    clusters = []
    counter = 0
    for i in range(len(age)):
        if counter < 10 or age[i] == age[i - 1]:
            counter += 1
        else:
            clusters.append(i)
            counter = 0
    clusters[len(clusters) - 1] = len(age)

    transition_matrix_hpv, deviation_hpv = find_transition_matrix(clusters, vpl, False)
    transition_matrix_cin, deviation_cin = find_transition_matrix(clusters, cin, True)
    print(deviation_hpv, deviation_cin)
    print(transition_matrix_hpv, transition_matrix_cin)


def find_transition_matrix(clusters, data, last_is_screen):
    clusters_parts = []
    for i in range(len(clusters)):
        if i == 0:
            part = np.array([np.sum(a) for a in [column[0: clusters[i]] for column in data]]) / clusters[i]
        else:
            part = np.array([np.sum(a) for a in [column[clusters[i - 1]: clusters[i]] for column in data]]) / (
                    clusters[i] - clusters[i - 1])
        clusters_parts.append([*[1 - np.sum(part)], *part.tolist()])

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

    if last_is_screen:
        transport_matrix[len(transport_matrix) - 1] = np.zeros(len(transport_matrix))
        transport_matrix[len(transport_matrix) - 1][len(transport_matrix) - 1] = 1

    transport_matrix = optimize(clusters_parts, transport_matrix, last_is_screen)

    deviation = find_deviation(clusters_parts, transport_matrix, True)

    return transport_matrix, deviation


def find_deviation(expected, transport_matrix, to_print):
    deviation = 0
    for i in range(len(expected) - 1):
        test = np.matrix(expected[i]) * np.matrix(transport_matrix)
        if to_print:
            print(np.sqrt(np.sum([a ** 2 for a in (np.asarray(test) - np.array(expected[i + 1]))]) / 2),
                  expected[i + 1], test)
        deviation += np.sqrt(np.sum([a ** 2 for a in (np.asarray(test) - np.array(expected[i + 1]))]) / 2)
    return deviation / (len(expected) - 1)


def optimize(expected, transport_matrix, last_is_screen):
    border = len(transport_matrix) if not last_is_screen else len(transport_matrix) - 1
    result = transport_matrix
    deviation = find_deviation(expected, transport_matrix, False)

    for i in range(1000):
        transport_matrix_copy = copy.deepcopy(transport_matrix)
        for j in range(border):
            for k in range(len(transport_matrix_copy[0])):
                if not k == j:
                    rand = uniform(-0.2, 0.2)
                    transport_matrix_copy[j][k] += rand
                    if transport_matrix_copy[j][k] < 0:
                        transport_matrix_copy[j][k] = 0
            transport_matrix_copy[j][j] = 1 - np.sum(transport_matrix_copy[j, :j]) - np.sum(
                transport_matrix_copy[j, j + 1:])
        new_deviation = find_deviation(expected, transport_matrix_copy, False)
        if new_deviation < deviation:
            result = transport_matrix_copy
            deviation = new_deviation
    return result


main()
