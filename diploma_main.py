from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot

df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'ph. intervention%'])

# print(df['hiv'].values.tolist())

monte_carlo_iterations = 100

time = 164
step = [0, 1]

examined_statistic = np.array(df['examined'].values.tolist())
hiv_statistic = np.array(df['hiv'].values.tolist()) / examined_statistic
aids_statistic = np.array(df['aids'].values.tolist()) / examined_statistic
susceptible_statistic = 1 - hiv_statistic - aids_statistic

statistic_values = np.array([susceptible_statistic.tolist(), hiv_statistic.tolist(), aids_statistic.tolist()])

susceptible = 10000
hiv = 200
aids = 14

healthy_child_hiv_parent = 0.75

birth_rate = 0.015 * (step[0] + (step[1] / 12))

birth_state_matrix = [[1, 0, 0],
                      [healthy_child_hiv_parent, 1 - healthy_child_hiv_parent, 0],
                      [healthy_child_hiv_parent, 1 - healthy_child_hiv_parent, 0]]

hiv_to_aids = 0.0203
hiv_infection = 0.01513 * (step[0] + (step[1] / 12))
aids_death = 0.0223 * (step[0] + (step[1] / 12))
hiv_death = 0.01376 * (step[0] + (step[1] / 12))

transition_matrix_min_max = [[1, [0, hiv_infection], [0, 0], [0, 0]],
                             [[0, 0], 1, [0, hiv_to_aids], [0, hiv_death]],
                             [[0, 0], [0, 0], 1, [0, aids_death]]]

population_distribution = [susceptible, hiv, aids]
statuses_names = ['susceptible', 'hiv', 'aids']
population = Population(population_distribution, [], [], birth_rate, birth_state_matrix)

result_sequences = monte_carlo_apply(population, monte_carlo_iterations, transition_matrix_min_max, time, step,
                                     statistic_values)

time_sequence = list([i for i in range(time + 1)])
build_plot(result_sequences[0], statistic_values, time_sequence, statuses_names)
