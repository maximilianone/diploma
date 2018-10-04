from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot

df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'treated%'])

monte_carlo_iterations = 1

time = 164
step = [0, 1]

examined_statistic = np.array(df['examined'].values.tolist())
treated_statistic = np.array(df['treated%'].values.tolist())
examined_statistic_percent = np.array(df['examined%'].values.tolist())
population_statistic = np.array(df['population'].values.tolist())

hiv_statistic = np.array(df['hiv'].values.tolist()) / examined_statistic
aids_statistic = np.array(df['aids'].values.tolist()) / examined_statistic
susceptible_statistic = 1 - hiv_statistic - aids_statistic

hiv_treated_to_all = (hiv_statistic/(hiv_statistic + aids_statistic))
aids_treated_to_all = 1 - (hiv_statistic/(hiv_statistic + aids_statistic))

susceptible_examined_statistic = susceptible_statistic * examined_statistic_percent
hiv_examined_statistic = hiv_statistic * examined_statistic_percent
hiv_treated_statistic = hiv_treated_to_all * treated_statistic
aids_examined_statistic = aids_statistic * examined_statistic_percent
aids_treated_statistic = aids_treated_to_all * treated_statistic

statistic_values = np.array([[susceptible_statistic.tolist()], [hiv_statistic.tolist()], [aids_statistic.tolist()]])

susceptible = 10000
hiv = 200
aids = 14
susceptible_examined = 200
hiv_examined = 50
hiv_wrong_examined = 0
hiv_treated = 0
aids_examined = 5
aids_wrong_examined = 0
aids_treated = 0

population_birth_rate = [0, 0.0105]
population_death_rate = [0, 0.015]

wrong_examination = [0, 0.1]

hiv_to_aids = 0.0203
hiv_infection = 0.01513
aids_death = 0.0223
hiv_death = 0.01376
hiv_treated_to_aids = 0.00203
hiv_treated_death = 0.001376
aids_treated_death = 0.005

transition_matrix_min_max = [[1, [0, hiv_infection], [0, 0], [0, 0]],
                             [[0, 0], 1, [0, hiv_to_aids], [0, hiv_death]],
                             [[0, 0], [0, 0], 1, [0, aids_death]]]

transition_treated_matrix_min_max = [[[0]],
                                     [[0, 0], 1, [0, hiv_treated_to_aids], [0, hiv_treated_death]],
                                     [[0, 0], [0, 0], 1, [0, aids_treated_death]]]

transition_medical_matrix = np.array([np.array(df['examined%'].values.tolist()),
                                      np.array(df['treated%'].values.tolist())])

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

statuses_names = ['susceptible', 'hiv', 'aids']
medical_statuses_names = ['', 'examined', 'diagnosed', 'treated']

population = Population(population_distribution, transition_medical_matrix)

result_sequences = monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                                     population_birth_rate, population_death_rate, wrong_examination, statistic_values,
                                     time, step, monte_carlo_iterations)

time_sequence = list([i for i in range(time + 1)])
build_plot(result_sequences[0], statistic_values, time_sequence, statuses_names)
