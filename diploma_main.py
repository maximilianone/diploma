from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot

df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'ph. intervention%'])

monte_carlo_iterations = 1

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
hiv_examined = 50
susceptible_examined = 200
aids_examined = 5
hiv_treated = 0
aids_treated = 0

population_change_rate = [-0.12, 0.12]

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

transition_treated_matrix_min_max = [[1, [0, hiv_infection], [0, 0], [0, 0]],
                                     [[0, 0], 1, [0, hiv_treated_to_aids], [0, hiv_treated_death]],
                                     [[0, 0], [0, 0], 1, [0, aids_treated_death]]]

population_distribution = [susceptible, hiv, aids]
statuses_names = ['susceptible', 'hiv', 'aids']
population = Population(population_distribution, [], [], population_change_rate)

result_sequences = monte_carlo_apply(population, monte_carlo_iterations, transition_matrix_min_max, time, step,
                                     statistic_values)

time_sequence = list([i for i in range(time + 1)])
build_plot(result_sequences[0], statistic_values, time_sequence, statuses_names)
