from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot


def values_to_statistic(status_distribution_sequences, population_sequence):
    infected = np.array(status_distribution_sequences[1][0]) + np.array(status_distribution_sequences[2][0])
    examined = np.array(status_distribution_sequences[1][2]) + np.array(status_distribution_sequences[2][2])
    treated = np.array(status_distribution_sequences[1][3]) + np.array(status_distribution_sequences[2][3])
    treated_percent = []
    for i in range(len(examined)):
        treated_percent.append(treated[i] / examined[i] if not examined[i] == 0 else 0)
    result = [(np.array(status_distribution_sequences[0][0]) + infected - examined) / np.array(population_sequence),
              (np.array(status_distribution_sequences[1][2])) / np.array(population_sequence),
              (np.array(status_distribution_sequences[2][2])) / np.array(population_sequence),
              np.array(treated_percent)]
    return result


df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'treated%'])

monte_carlo_iterations = 10

time = 152
step = [0, 1]

population_statistic = df['population'].values.tolist()[12:]
susceptible_statistic = df['susceptible'].values.tolist()[12:]
treated_statistic = df['treated%'].values.tolist()[12:]
population_treated = df['treated%'].values.tolist()[:12]
hiv_statistic = df['hiv'].values.tolist()[12:]
aids_statistic = df['aids'].values.tolist()[12:]

statistic_values = [np.array(susceptible_statistic) / np.array(population_statistic),
                    np.array(hiv_statistic) / np.array(population_statistic),
                    np.array(aids_statistic) / np.array(population_statistic),
                    np.array(treated_statistic)]

population_count = 1000
susceptible = 976
hiv = 22
aids = 2
susceptible_examined = 46
hiv_examined = 1
hiv_wrong_examined = 0
hiv_treated = 0
aids_examined = 0
aids_wrong_examined = 0
aids_treated = 0

# birth rate considering step duration
population_birth_rate = [0.0005, 0.000875]
# year death rate
population_death_rate = [0.012, 0.015]

wrong_examination = [0, 0.2]

average_infected = [0, 2]
average_treated_infected = [0, 1]

average_infected_vector = [average_infected, average_treated_infected]

hiv_to_aids = 0.03
aids_death = 0.03
hiv_death = 0.01
hiv_treated_to_aids = 0.003
hiv_treated_death = 0.001
aids_treated_death = 0.004

transition_matrix_min_max = [[1, [0, 0], [0, 0], [0, 0]],
                             [[0, 0], 1, [0, hiv_to_aids], [0, hiv_death]],
                             [[0, 0], [0, 0], 1, [0, aids_death]]]

transition_treated_matrix_min_max = [[[0]],
                                     [[0, 0], 1, [0, hiv_treated_to_aids], [0, hiv_treated_death]],
                                     [[0, 0], [0, 0], 1, [0, aids_treated_death]]]

examination = [0, 0.01]
treating = [0, 0.01]
transition_medical_matrix = [examination, treating]

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

names = ['susceptible', 'hiv', 'aids', 'examined']

population = Population(population_distribution)
population.population_treated = population_treated

optimum_results = monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                                    transition_medical_matrix, population_birth_rate, population_death_rate,
                                    average_infected_vector, wrong_examination, statistic_values,
                                    time, step, monte_carlo_iterations, values_to_statistic)

time_sequence = list([i for i in range(time + 1)])
print(optimum_results[1], optimum_results[2], optimum_results[3],
      optimum_results[4], optimum_results[5], optimum_results[6])
build_plot(optimum_results[0], statistic_values, time_sequence, names)
