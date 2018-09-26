import numpy as np
from random import *
from individual import Individual


def simulate(time, step, population):
    status_distribution_sequences = [[] for i in range(len(population.state_distribution) + 1)]

    for i in range(time):
        delete_dead(population)
        born(population)

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


def delete_dead(population):
    for individual in population.members:
        if individual.age[0] > individual.lifespan[0] or (
                individual.age[0] == individual.age[0] and individual.age[1] > individual.age[1]):
            population.state_distribution[individual.state] -= 1
            population.members.remove(individual)


def born(population):
    population_replenishment = np.ceil(uniform(0, 2) * population.birth_rate * len(population))
    count = prepare_population_count(population_replenishment)
    children_distribution = []

    for state_population in population.state_distribution:
        children_distribution.append(count * state_population / len(population))

    children_distribution = prepare_children_distribution(children_distribution, count)
    add_born(population, children_distribution)


def add_born(population, children_distribution):
    for i in range(len(children_distribution)):
        for j in range(children_distribution[i]):
            rand = uniform(0, 1)
            individual = Individual(0, [0, 0])
            for k in range(len(population.birth_state_matrix[i])):
                if markov_transition(rand, population.birth_state_matrix[i], k):
                    individual.state = k
                    population.members.append(individual)
                    population.state_distribution[k] += 1


def prepare_population_count(count):
    return int(np.round(count))


def prepare_children_distribution(children_distribution, count):
    prepared_distribution = []
    counter = len(children_distribution)
    for i in range(counter):
        if not count > 0:
            prepared_distribution.append(0)
            continue
        max_distribution = np.max(children_distribution)
        children_distribution.remove(max_distribution)
        children_distribution_count = np.round(max_distribution)
        if count - children_distribution_count >= 0:
            if children_distribution_count == 0:
                children_distribution_count += 1
        else:
            children_distribution_count = count
        count -= children_distribution_count
        prepared_distribution.append(int(children_distribution_count))
    return prepared_distribution


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
