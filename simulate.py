import numpy as np
from random import *
from individual import Individual


def simulate(time, step, population):
    status_distribution_sequences = [[population.state_distribution[i]] for i in
                                     range(len(population.state_distribution))]
    status_distribution_sequences.append([len(population)])

    for i in range(time):
        change_population_number(population)

        for individual in population.members:
            individual.age = np.sum([individual.age, step], axis=0)
            if individual.age[1] == 12:
                individual.age[0] += 1
                individual.age[1] = 0

            change_state(population, individual)

        for j in range(len(status_distribution_sequences) - 1):
            status_distribution_sequences[j].append(population.state_distribution[j])
        status_distribution_sequences[len(population.state_distribution)].append(len(population))
    return [status_distribution_sequences, population.transition_matrix]


def change_population_number(population):
    if population.population_change_rate > 0:
        born(population)
    elif population.population_change_rate < 0:
        death(population)


def born(population):
    population_len = len(population)
    for i in range(population_len):
        rand = uniform(0, 1)
        probability = population.members[i].get_birth_probability(population.population_change_rate)
        if probability >= rand:
            population.members.append(Individual(0, 0, 0))


def death(population):
    for individual in population.members:
        rand = uniform(0, 1)
        probability = individual.get_death_probability(np.absolute(population.population_change_rate))
        if probability >= rand:
            population.members.remove(individual)


def prepare_population_count(count):
    return int(np.round(count))


def change_state(population, individual):
    rand = uniform(0, 1)
    for i in range(len(population.transition_matrix[individual.state])):
        if markov_transition(rand, population.transition_matrix[individual.state], i):
            population.state_distribution[individual.state] -= 1
            if i == len(population.transition_matrix[individual.state]) - 1:
                population.members.remove(individual)
            else:
                individual.state = i
                population.state_distribution[individual.state] += 1


def markov_transition(rand, transition_probability_vector, transition_number):
    left = 0
    for i in range(transition_number):
        left += transition_probability_vector[i]

    right = left + transition_probability_vector[transition_number]
    return left <= rand <= right
