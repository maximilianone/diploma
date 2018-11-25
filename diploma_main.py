from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot


def values_to_statistic(status_distribution_sequences):
    infected = np.array(status_distribution_sequences[1][0]) + np.array(status_distribution_sequences[2][0])
    examined = np.array(status_distribution_sequences[1][2]) + np.array(status_distribution_sequences[2][2])
    treated = np.array(status_distribution_sequences[1][3]) + np.array(status_distribution_sequences[2][3])
    result = [np.array(status_distribution_sequences[0][0]) + infected - examined,
              np.array(status_distribution_sequences[1][2]),
              np.array(status_distribution_sequences[2][2]),
              np.array(treated)]
    return result


df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'treated%'])

monte_carlo_iterations = 500

time = 144
step = [0, 1]

population_statistic = np.array(df['population'].values.tolist()[12:157])
susceptible_statistic = np.array(df['susceptible'].values.tolist()[12:157])
treated_statistic = np.array(df['treated%'].values.tolist()[12:157])
population_treated = df['treated%'].values.tolist()[:12]
hiv_statistic = np.array(df['hiv'].values.tolist()[12:157])
aids_statistic = np.array(df['aids'].values.tolist()[12:157])

treated_statistic = np.array([int(np.round(i)) for i in (treated_statistic * (hiv_statistic + aids_statistic))])

quantifier = 5
agents = 1000 * quantifier
delimiter = population_statistic[0] / agents

statistic_values = [np.array([int(np.round(i / delimiter)) for i in susceptible_statistic]),
                    np.array([int(np.round(i / delimiter)) for i in hiv_statistic]),
                    np.array([int(np.round(i / delimiter)) for i in aids_statistic]),
                    np.array([int(np.round(i / delimiter)) for i in treated_statistic])]


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

population_death_rate = [0.0000005, 0.000005]

wrong_examination = [0, 0]

average_infected = [0.15, 0.35]
average_treated_infected = [0.01, 0.04]

average_infected_vector = [average_infected, average_treated_infected]

hiv_to_aids = [0.021, 0.025]
aids_death = 0.03
hiv_death = 0.01
hiv_treated_to_aids = 0.003
hiv_treated_death = 0.001
aids_treated_death = 0.004

transition_matrix_min_max = [[1, [0, 0], [0, 0], [0, 0]],
                             [[0, 0], 1, hiv_to_aids, [0, hiv_death]],
                             [[0, 0], [0, 0], 1, [0, aids_death]]]

transition_treated_matrix_min_max = [[[0]],
                                     [[0, 0], 1, [0, hiv_treated_to_aids], [0, hiv_treated_death]],
                                     [[0, 0], [0, 0], 1, [0, aids_treated_death]]]

examination = [0.001, 0.01]
treating_hiv = [0.002, 0.005]
treating_aids = [0.02, 0.05]
transition_medical_matrix = [[examination], [treating_hiv, treating_aids]]

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

names = ['susceptible', 'hiv', 'aids', 'treated']

population = Population(population_distribution)
population.population_treated = population_treated

optimum_results = monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                                    transition_medical_matrix, population_death_rate,
                                    average_infected_vector, wrong_examination, statistic_values,
                                    time, step, monte_carlo_iterations, values_to_statistic)

time_sequence = list([i for i in range(time + 1)])
print(optimum_results[1], optimum_results[2], optimum_results[3],
      optimum_results[4], optimum_results[5])
build_plot(optimum_results[0], statistic_values, time_sequence, names)
