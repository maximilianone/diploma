import numpy as np
from random import *


def simulate(time, step, population):
    status_distribution_sequences = [[[population.state_distribution[i][j]] for j in
                                      range(len(population.state_distribution[i]))] for i in
                                     range(len(population.state_distribution))]
    population_sequence = [len(population)]

    for i in range(time):
        death(population)

        for individual in population.members:
            infect(population, individual, step)

            if individual.medical_state == 1:
                individual.last_examination_count = increment_time(individual.last_examination_count, step)

            change_medical_state(population, individual, population.transition_medical_matrix)
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


def death(population):
    dead = prepare_population_count(len(population) * population.population_death_rate)
    for i in range(dead):
        individual = population.members[randint(0, len(population) - 1)]
        population.state_distribution[individual.state][individual.medical_state] -= 1
        if not individual.medical_state == 0:
            population.state_distribution[individual.state][0] -= 1
        if individual.medical_state == 3:
            population.state_distribution[individual.state][2] -= 1
        population.members.remove(individual)


def infect(population, individual, step):
    if not individual.state == 0:
        inf, inf_tr = population.average_infected_vector[0], population.average_infected_vector[1]
        average = inf if not individual.medical_state == 3 else inf_tr
        infected_people = np.random.poisson(average / (12 / (step[1] + 12 * step[0])))
        for agent in population.members:
            if infected_people == 0:
                break
            if agent.state == 0:
                agent.state = 1
                population.state_distribution[0][agent.medical_state] -= 1
                if not agent.medical_state == 0:
                    population.state_distribution[0][0] -= 1
                population.state_distribution[1][agent.medical_state] += 1
                if not agent.medical_state == 0:
                    population.state_distribution[1][0] += 1
                infected_people -= 1


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
            if individual.medical_state == 3:
                population.state_distribution[individual.state][2] -= 1
            if i == len(transition_matrix[individual.state]) - 1:
                population.members.remove(individual)
                population.infected_dead += 1
            else:
                individual.state = i
                population.state_distribution[individual.state][individual.medical_state] += 1
                if not individual.medical_state == 0:
                    population.state_distribution[individual.state][0] += 1
                if individual.medical_state == 3:
                    population.state_distribution[individual.state][2] += 1


def change_medical_state(population, individual, transition_matrix):
    rand = uniform(0, 1)
    if individual.medical_state <= 1:
        if individual.get_examination_probability(transition_matrix[0][0]) >= uniform(0, 1):
            individual.last_examination_count = [0, 0]
            if individual.medical_state == 0:
                individual.medical_state = 1
                population.state_distribution[individual.state][individual.medical_state] += 1
            if population.wrong_examination <= uniform(0, 1) and not individual.state == 0:
                population.state_distribution[individual.state][individual.medical_state] -= 1
                individual.medical_state = 2
                population.state_distribution[individual.state][individual.medical_state] += 1
    elif individual.medical_state == 2:
        if (individual.state == 1 and transition_matrix[1][0] >= rand) or (
                individual.state == 2 and transition_matrix[1][1] >= rand):
            individual.medical_state = 3
            population.state_distribution[individual.state][individual.medical_state] += 1


def markov_transition(rand, transition_probability_vector, transition_number):
    left = 0
    for i in range(transition_number):
        left += transition_probability_vector[i]

    right = left + transition_probability_vector[transition_number]
    return left <= rand <= right
