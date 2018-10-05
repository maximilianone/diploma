from simulate import simulate
from random import *
import numpy as np
import copy


def monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                      population_birth_rate, population_death_rate, infection_vector,
                      wrong_examination, statistic_values,
                      time, step, count):
    optimum_results = []
    deviation = 0

    for i in range(count):
        population_copy = copy.deepcopy(population)
        population_copy.transition_matrix = get_transition_matrix(transition_matrix_min_max)
        population_copy.transition_treated_matrix = get_transition_matrix(transition_treated_matrix_min_max)
        population_copy.population_birth_rate = uniform(population_birth_rate[0], population_birth_rate[1])
        population_copy.population_death_rate = uniform(population_death_rate[0], population_death_rate[1])
        population_copy.infection_vector = get_transition_vector(infection_vector)
        population_copy.wrong_examination = uniform(wrong_examination[0], wrong_examination[1])
        population_copy.populate()

        distribution_sequences, population_sequence = simulate(time, step, population_copy)
        print(distribution_sequences)
        state_distribution = np.array(distribution_sequences)
        state_indexes = [i for i in range(len(state_distribution) - 1)]
        iteration_results = np.array(
            state_distribution[state_indexes, :] / state_distribution[len(state_distribution) - 1, :])
        if i == 0:
            optimum_results.append(iteration_results)
            optimum_results.append(population_copy.transition_matrix)
            deviation = np.sqrt(np.sum(
                [a ** 2 for a in (a_row for a_row in (iteration_results - statistic_values))]) / iteration_results.size)
            print(deviation)
        else:
            iteration_deviation = np.sqrt(np.sum(
                [a ** 2 for a in (a_row for a_row in (iteration_results - statistic_values))]) / iteration_results.size)
            if iteration_deviation < deviation:
                deviation = iteration_deviation
                optimum_results[0] = iteration_results
                optimum_results[1] = population_copy.transition_matrix
                print(deviation)
            print(iteration_deviation)
        print(i)
    optimum_results.append(deviation)
    return optimum_results


def get_transition_matrix(transition_matrix_min_max):
    transition_matrix = []
    for i in range(len(transition_matrix_min_max)):
        transition_matrix.append([])
        for j in range(len(transition_matrix_min_max[i])):
            if i == j:
                transition_matrix[i].append(1)
            else:
                transition_matrix[i].append(
                    uniform(transition_matrix_min_max[i][j][0], transition_matrix_min_max[i][j][1]))
    return prepare_transition_matrix(transition_matrix)


def prepare_transition_matrix(transition_matrix):
    for i in range(len(transition_matrix)):
        sum_row = 0
        for j in range(len(transition_matrix[i])):
            if not i == j:
                sum_row += transition_matrix[i][j]
        transition_matrix[i][i] -= sum_row
    return transition_matrix


def get_transition_vector(transition_vector_min_max):
    transition_vector = []
    for i in range(len(transition_vector_min_max)):
        transition_vector.append(uniform(transition_vector_min_max[i][0], transition_vector_min_max[i][1]))
    return transition_vector
