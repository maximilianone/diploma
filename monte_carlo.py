from simulate import simulate
from random import *
import numpy as np
import copy


def monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                      transition_medical_matrix, population_death_rate, average_infected_vector,
                      wrong_examination, statistic_values,
                      time, step, count, values_to_statistic):
    optimum_results = []
    deviation = 0

    for i in range(count):
        population_copy = copy.deepcopy(population)
        population_copy.transition_matrix = get_transition_matrix(transition_matrix_min_max)
        population_copy.transition_treated_matrix = get_transition_matrix(transition_treated_matrix_min_max)
        population_copy.transition_medical_matrix = get_transition_vector(transition_medical_matrix)
        population_copy.population_death_rate = uniform(population_death_rate[0], population_death_rate[1])
        population_copy.average_infected_vector = get_int_vector(average_infected_vector)
        population_copy.wrong_examination = uniform(wrong_examination[0], wrong_examination[1])
        population_copy.populate()

        distribution_sequences, population_sequence = simulate(time, step, population_copy)
        simulation_results = values_to_statistic(distribution_sequences)

        if i == 0:
            optimum_results.append(simulation_results)
            optimum_results.append(population_copy.transition_matrix)
            optimum_results.append(population_copy.transition_medical_matrix)
            optimum_results.append(population_copy.transition_treated_matrix)
            optimum_results.append(population_copy.average_infected_vector)
            optimum_results.append(population_copy.population_death_rate)
            optimum_results.append(population_copy.population_birth_rate)
            deviation = find_deviation(statistic_values, simulation_results)

            print(deviation)
        else:
            iteration_deviation = find_deviation(statistic_values, simulation_results)
            if iteration_deviation < deviation:
                deviation = iteration_deviation
                optimum_results[0] = simulation_results
                optimum_results[1] = population_copy.transition_matrix
                optimum_results[2] = population_copy.transition_medical_matrix
                optimum_results[3] = population_copy.transition_treated_matrix
                optimum_results[4] = population_copy.average_infected_vector
                optimum_results[5] = population_copy.population_death_rate
                optimum_results[6] = population_copy.population_birth_rate
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


def get_int_vector(vector_min_max):
    transition_vector = []
    for i in range(len(vector_min_max)):
        transition_vector.append(randint(vector_min_max[i][0], vector_min_max[i][1]))
    return transition_vector


def find_deviation(statistic, simulation_result):
    deviation = 0
    for i in range(len(simulation_result)):
        deviation += np.sum([a ** 2 for a in (simulation_result[i] - statistic[i])]) / (len(simulation_result[i]))
    return np.sqrt(deviation)
