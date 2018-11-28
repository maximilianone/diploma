from simulate import simulate
import numpy as np
import copy
from population import Population


time = 144
step = [0, 1]

quantifier = 20
agents = 1000 * quantifier

susceptible = 976 * quantifier
hiv = 22 * quantifier
aids = 2 * quantifier
susceptible_examined = 46 * quantifier
hiv_examined = 1 * quantifier
hiv_wrong_examined = 0
hiv_treated = 0
aids_examined = 1
aids_wrong_examined = 0
aids_treated = 0

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

population = Population(population_distribution)
population.transition_matrix = [[1.0, 0.0, 0.0, 0.0],
                                [0.0, 0.993895336731776, 0.004900325949233125, 0.0012043373189908274],
                                [0.0, 0.0, 0.9949829545143906, 0.005017045485609444]]
population.transition_treated_matrix = [[1], [0.0, 0.9999265919813641, 7.196470280814807e-05, 1.443315827697732e-06],
                                        [0.0, 0.0, 0.9999977350989598, 2.2649010401869064e-06]]
population.transition_medical_matrix = [[0.0023601937167775734], [0.00186468954542118, 0.0263742426647091]]
population.population_death_rate = 0.0004619560712723398
population.average_infected_vector = [0.018162747716319577, 0.0017622648234252702]
population.wrong_examination = 0
population.populate()


def optimize(time, step, population):
    for i in range(10):
        population_copy = copy.deepcopy(population)
        simulate(time, step, population_copy)
        print(population_copy.infected_dead)


optimize(time, step, population)
