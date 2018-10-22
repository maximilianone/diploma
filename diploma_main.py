from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot

df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'treated%'])

monte_carlo_iterations = 300

time = 164
step = [0, 1]

examined_statistic = np.array(df['examined'].values.tolist())
treated_statistic = np.array(df['treated%'].values.tolist())
examined_statistic_percent = np.array(df['examined%'].values.tolist())
population_statistic = np.array(df['population'].values.tolist())

hiv_statistic = np.array(df['hiv'].values.tolist()) / examined_statistic
aids_statistic = np.array(df['aids'].values.tolist()) / examined_statistic
susceptible_statistic = 1 - hiv_statistic - aids_statistic

hiv_treated_to_all = (hiv_statistic / (hiv_statistic + aids_statistic))
aids_treated_to_all = 1 - (hiv_statistic / (hiv_statistic + aids_statistic))

susceptible_examined_statistic = susceptible_statistic * examined_statistic_percent
hiv_examined_statistic = hiv_statistic * examined_statistic_percent
hiv_treated_statistic = hiv_treated_to_all * treated_statistic
aids_examined_statistic = aids_statistic * examined_statistic_percent
aids_treated_statistic = aids_treated_to_all * treated_statistic

empty_list_hiv = np.array([0 for i in range(time + 1)])
empty_list_aids = np.array([0 for j in range(time + 1)])


statistic_values = [np.array([susceptible_statistic.tolist(), susceptible_examined_statistic.tolist()]),
                    np.array([hiv_statistic.tolist(), empty_list_hiv.tolist(), hiv_examined_statistic.tolist(),
                              hiv_treated_statistic.tolist()]),
                    np.array(
                        [aids_statistic.tolist(), empty_list_aids.tolist(), aids_examined_statistic.tolist(),
                         aids_treated_statistic.tolist()])]

susceptible = 9993
hiv = 207
aids = 14
susceptible_examined = 439
hiv_examined = 9
hiv_wrong_examined = 0
hiv_treated = 0
aids_examined = 1
aids_wrong_examined = 0
aids_treated = 0

# birth rate considering step duration
population_birth_rate = [0.0005, 0.000875]
# year death rate
population_death_rate = [0.012, 0.015]

wrong_examination = [0, 0.1]

hiv_infection_quantifier = [0.1, 0.5]
hiv_treated_infection_quantifier = [0.01, 0.1]

infection_vector = [hiv_infection_quantifier, hiv_treated_infection_quantifier]

hiv_to_aids = 0.015
aids_death = 0.015
hiv_death = 0.01
hiv_treated_to_aids = 0.0015
hiv_treated_death = 0.001
aids_treated_death = 0.002

transition_matrix_min_max = [[1, [0, 0], [0, 0], [0, 0]],
                             [[0, 0], 1, [0, hiv_to_aids], [0, hiv_death]],
                             [[0, 0], [0, 0], 1, [0, aids_death]]]

transition_treated_matrix_min_max = [[[0]],
                                     [[0, 0], 1, [0, hiv_treated_to_aids], [0, hiv_treated_death]],
                                     [[0, 0], [0, 0], 1, [0, aids_treated_death]]]

examination = [0, 0.001]
treating = [0, 0.1]
transition_medical_matrix = [examination, treating]

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

statuses_names = ['susceptible', 'hiv', 'aids']
medical_statuses_names = ['', 'examined', 'diagnosed', 'treated']

population = Population(population_distribution)

optimum_results = monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                                     transition_medical_matrix, population_birth_rate, population_death_rate,
                                     infection_vector, wrong_examination, statistic_values,
                                     time, step, monte_carlo_iterations)

time_sequence = list([i for i in range(time + 1)])
print(optimum_results[1], optimum_results[2], optimum_results[3],
      optimum_results[4], optimum_results[5], optimum_results[6])
build_plot(optimum_results[0], statistic_values, time_sequence, statuses_names, medical_statuses_names)
