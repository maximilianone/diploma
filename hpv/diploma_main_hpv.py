import pandas as pd
from hpv.statistic_processor import get_transition_matrices
import numpy as np
import copy
from simulate import *
from population import Population
from individual import Individual


def main():
    df = pd.read_excel('../BD2.xlsx', usecols=[1, 6, 27, 28, 29, 30], skiprows=[0, 1],
                       names=['ВІК', 'ВПЛ', 'CIN1', 'CIN2', 'CIN3', 'CC'])
    get_transition_matrices(df)

    age_all = df['ВІК'].values
    hpv_all = df['ВПЛ'].replace('так', 1).replace('ні', 0).values
    cin_hard = df[['CIN2', 'CIN3']].replace('так', 2).fillna(0).sum(axis=1)
    cin_light = df['CIN1'].replace('так', 1).fillna(0)
    cin_all = pd.concat([cin_light, cin_hard], axis=1, sort=False).sum(axis=1).values

    hpv_transition_matrix = [[0.72686798, 0.27313202], [0.46668473, 0.53331527]]
    cin_hpv_transition_matrix = [[0.37306533, 0.56736636, 0.05956831],
                                 [0.49543228, 0.40456772, 0.1],
                                 [0.0, 0.0, 1.0]]
    cin_no_hpv_transition_matrix = [[0.87526995, 0.11552851, 0.00920153],
                                    [0.31512487, 0.66512231, 0.01975282],
                                    [0.0, 0.0, 1.0]]

    population = Population([])
    for i in range(len(hpv_all)):
        population.members.append(Individual(int(hpv_all[i]), 0, int(cin_all[i]), int(age_all[i])))
    population.state_distribution = [[len(hpv_all) - np.sum(hpv_all), 0], [np.sum(hpv_all), 0]]

    monte_carlo_iterations = 5000
    time = 30
    monte_carlo_hpv(hpv_transition_matrix, cin_hpv_transition_matrix, cin_no_hpv_transition_matrix,
                    population, monte_carlo_iterations, time)


def monte_carlo_hpv(hpv_transition_matrix, cin_hpv_transition_matrix, cin_no_hpv_transition_matrix,
                    population, monte_carlo_iterations, time):
    optimum = 0
    time_in_cin23_default = 0
    time_in_cin23_optimum = 0
    examined_count_optimum = 0
    examination_period_optimum = 0
    examination_period_hpv_optimum = 0
    examination_period_cin_optimum = 0

    for m in range(monte_carlo_iterations):
        population_copy = copy.deepcopy(population)

        examination_period = randint(3, 6)
        examination_period_hpv = randint(0, int(np.floor(examination_period / 2)))
        if examination_period_hpv == 0:
            examination_period_hpv = 1
        examination_period_cin = randint(0, int(np.floor(examination_period / 2)))
        if examination_period_cin == 0:
            examination_period_cin = 1
        if examination_period_cin == examination_period / 2 and examination_period_hpv == examination_period / 2:
            examination_period_hpv -= 1
        examined_count = 0
        time_in_cin23 = 0

        for individual in population_copy.members:
            individual.last_examination_count = [randint(1, examination_period), 0]

        for i in range(time):
            for individual in population_copy.members:

                if individual.age > 65:
                    population_copy.members.remove(individual)
                    continue

                change_state_with_matrix(population_copy, individual, hpv_transition_matrix, 'state', False)

                if individual.state == 0:
                    change_state_with_matrix(population_copy, individual, cin_no_hpv_transition_matrix,
                                             'additional_state', False)
                else:
                    change_state_with_matrix(population_copy, individual, cin_hpv_transition_matrix, 'additional_state',
                                             False)

                if not m < 50:
                    individual.last_examination_count[0] -= 1
                    if individual.last_examination_count[0] == 0:
                        examined_count += 1
                        individual.last_examination_count = [examination_period, 0]
                        # if individual.state == 1:
                        #     individual.last_examination_count[0] -= examination_period_hpv
                        #     if individual.additional_state == 2:
                        #         population_copy.members.remove(individual)
                        #         continue
                        #     elif individual.additional_state == 1:
                        #         individual.last_examination_count[0] -= examination_period_cin
                        if individual.additional_state == 2:
                            population_copy.members.remove(individual)
                            continue
                        elif individual.additional_state == 1:
                            individual.last_examination_count[0] -= examination_period_cin
                            # if individual.state == 1:
                            #     individual.last_examination_count[0] -= examination_period_hpv

                if individual.additional_state == 2:
                    time_in_cin23 += 1

                individual.age += 1
        if m < 50:
            time_in_cin23_default += time_in_cin23 / 50
        else:
            step_effectiveness = (time_in_cin23_default - time_in_cin23) / examined_count
            if step_effectiveness > optimum:
                optimum = step_effectiveness
                time_in_cin23_optimum = time_in_cin23
                examined_count_optimum = examined_count
                examination_period_optimum = examination_period
                examination_period_hpv_optimum = examination_period_hpv
                examination_period_cin_optimum = examination_period_cin
    print(time_in_cin23_optimum, examined_count_optimum, optimum)
    print(examination_period_optimum, examination_period_cin_optimum, examination_period_hpv_optimum)
    print(time_in_cin23_default)


main()
