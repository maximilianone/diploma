import numpy as np
from random import *
from individual import Individual


def simulate(time, step, population):
    status_distribution_sequences = [[[population.state_distribution[i][j]] for j in
                                      range(len(population.state_distribution[i]))] for i in
                                     range(len(population.state_distribution))]
    population_sequence = [len(population)]

    for i in range(time):
        born(population)

        for individual in population.members:
            if death(individual, population):
                continue

            individual.age = increment_time(individual.age, step)
            if individual.medical_state == 1:
                individual.last_examination_count = increment_time(individual.last_examination_count, step)

            change_medical_state(population, individual, [population.transition_medical_matrix[0][i + 1],
                                                          population.transition_medical_matrix[1][i + 1]])
            change_state(population, individual)

        for j in range(len(status_distribution_sequences)):
            for k in range(len(status_distribution_sequences[j])):
                status_distribution_sequences[j][k].append(population.state_distribution[j][k])
        population_sequence.append(len(population))
    return status_distribution_sequences, population_sequence


def increment_time(time, step):
    time = np.sum([time, step], axis=0)
    if time[1] == 12:
        time[0] += 1
        time[1] = 0
    return time


def born(population):
    new_individuals_count = prepare_population_count(uniform(0, 2) *
                                                     len(population) * population.population_birth_rate)
    for i in range(new_individuals_count):
        individual = Individual(0, 0, [0, 0])
        individual.set_lifespan(prepare_population_count(1/population.population_death_rate))
        population.members.append(individual)
        population.state_distribution[0][0] += 1


def death(individual, population):
    is_dead = False
    if individual.age[0] > individual.lifespan[0] or (
            individual.age[0] == individual.lifespan[0] and individual.age[1] > individual.lifespan[1]):
        population.state_distribution[individual.state][individual.medical_state] -= 1
        if not individual.medical_state == 0:
            population.state_distribution[individual.state][0] -= 1
        population.members.remove(individual)
        is_dead = True
    return is_dead


def prepare_population_count(count):
    return int(np.round(count))


def change_state(population, individual):
    if individual.medical_state == 3:
        change_state_with_matrix(population, individual, population.transition_treated_matrix)
    else:
        change_state_with_matrix(population, individual, population.transition_matrix)


def change_state_with_matrix(population, individual, transition_matrix):
    rand = uniform(0, 1)
    for i in range(len(transition_matrix[individual.state])):
        if markov_transition(rand, transition_matrix[individual.state], i):
            population.state_distribution[individual.state][individual.medical_state] -= 1
            if not individual.medical_state == 0:
                population.state_distribution[individual.state][0] -= 1
            if i == len(transition_matrix[individual.state]) - 1:
                population.members.remove(individual)
            else:
                individual.state = i
                population.state_distribution[individual.state][individual.medical_state] += 1
                if not individual.medical_state == 0:
                    population.state_distribution[individual.state][0] += 1


def change_medical_state(population, individual, transition_matrix):
    if individual.medical_state <= 1:
        if individual.get_examination_probability(transition_matrix[0]) >= uniform(0, 1):
            individual.last_examination_count = [0, 0]
            if individual.medical_state == 0:
                individual.medical_state = 1
                population.state_distribution[individual.state][individual.medical_state] += 1
            if population.wrong_examination <= uniform(0, 1) and not individual.state == 0:
                population.state_distribution[individual.state][individual.medical_state] -= 1
                individual.medical_state = 2
                population.state_distribution[individual.state][individual.medical_state] += 1
    elif individual.medical_state == 2 and transition_matrix[1] >= uniform(0, 1):
        population.state_distribution[individual.state][individual.medical_state] -= 1
        individual.medical_state = 3
        population.state_distribution[individual.state][individual.medical_state] += 1


def markov_transition(rand, transition_probability_vector, transition_number):
    left = 0
    for i in range(transition_number):
        left += transition_probability_vector[i]

    right = left + transition_probability_vector[transition_number]
    return left <= rand <= right
