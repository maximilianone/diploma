from simulate import simulate
import numpy as np
import copy
from population import Population
import matplotlib.pyplot as plt

time = 300
step = [0, 1]

quantifier = 5
agents = 1000 * quantifier

susceptible = 976 * quantifier
hiv = 22 * quantifier
aids = 2 * quantifier
susceptible_examined = 46 * quantifier
hiv_examined = 1 * quantifier
hiv_wrong_examined = 0
hiv_treated = 0
aids_examined = 0
aids_wrong_examined = 0
aids_treated = 0

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

population = Population(population_distribution)
population.transition_matrix = [[1.0, 0.0, 0.0, 0.0],
                                [0.0, 0.99697924031886779226, 0.002900325949233125, 0.00012043373189908274],
                                [0.0, 0.0, 0.997982954514390556, 0.002017045485609444]]
population.transition_treated_matrix = [[1], [0.0, 0.9999265919813641, 7.196470280814807e-05, 1.443315827697732e-06],
                                        [0.0, 0.0, 0.9999977350989598, 2.2649010401869064e-06]]
population.transition_medical_matrix = [[0.00083601937167775734], [0.00186468954542118, 0.0263742426647091]]
population.population_death_rate = 0.0004219560712723398
population.average_infected_vector = [0.14162747716319577, 0.017622648234252702]
population.wrong_examination = 0
population.populate()


def optimize(time, step, population):
    optimization_vector = []
    optimize_default = 0
    optimize_delimiter_default = 0
    for i in range(10):
        optimization_value = 0
        optimization_delimiter = 0
        for j in range(20):
            population_copy = copy.deepcopy(population)
            population_copy.transition_medical_matrix[1][0] += 0.01 * i
            simulate(time, step, population_copy)
            optimization_value += population_copy.infected_dead
            optimization_delimiter += population_copy.state_distribution[1][3]
        optimization_value /= 20
        optimization_delimiter /= 20
        print(optimization_value)
        if i == 0:
            optimize_default = optimization_value
            optimize_delimiter_default = optimization_delimiter
            optimization_vector.append(0)
        else:
            optimization_vector.append((optimize_default - optimization_value) / (
                    optimization_delimiter - optimize_delimiter_default))
        print(optimization_delimiter)
    time_vector = list([0.00186468954542118 + 0.01 * i for i in range(10)])
    plt.grid(True)
    plt.plot(time_vector, optimization_vector)
    plt.xlabel('Параметр керування, P(th)')
    plt.ylabel('Δd/E')
    plt.show()


optimize(time, step, population)
