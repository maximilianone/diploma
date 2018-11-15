from monte_carlo import monte_carlo_apply
import numpy as np
from population import Population
import pandas as pd
from plot_builder import build_plot


def find_people_count(val, len_pop):
    return int(np.round(val * len_pop))


df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 26, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'susceptible', 'examined', 'examined%', 'treated%'])

monte_carlo_iterations = 1000

time = 152
step = [0, 1]

examined_statistic = np.array(df['examined'].values.tolist()[12:])
treated_statistic = np.array(df['treated%'].values.tolist()[12:])
population_treated = df['treated%'].values.tolist()[:12]
examined_statistic_percent = np.array(df['examined%'].values.tolist()[12:])
population_statistic = np.array(df['population'].values.tolist()[12:])

hiv_statistic = np.array(df['hiv'].values.tolist()[12:]) / examined_statistic
aids_statistic = np.array(df['aids'].values.tolist()[12:]) / examined_statistic
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

population_count = 1024
susceptible = find_people_count(susceptible_statistic[0], population_count)
hiv = find_people_count(hiv_statistic[0], population_count)
aids = find_people_count(aids_statistic[0], population_count)
susceptible_examined = find_people_count(susceptible_examined_statistic[0], population_count)
hiv_examined = find_people_count(hiv_examined_statistic[0], population_count)
hiv_wrong_examined = 0
hiv_treated = find_people_count(hiv_treated_statistic[0], hiv)
aids_examined = find_people_count(aids_examined_statistic[0], population_count)
aids_wrong_examined = 0
aids_treated = find_people_count(aids_treated_statistic[0], aids)

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

examination = [0, 0.001]
treating = [0, 0.3]
transition_medical_matrix = [examination, treating]

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

statuses_names = ['susceptible', 'hiv', 'aids']
medical_statuses_names = ['', 'examined', 'diagnosed', 'treated']

population = Population(population_distribution)
population.population_treated = population_treated

optimum_results = monte_carlo_apply(population, transition_matrix_min_max, transition_treated_matrix_min_max,
                                    transition_medical_matrix, population_birth_rate, population_death_rate,
                                    average_infected_vector, wrong_examination, statistic_values,
                                    time, step, monte_carlo_iterations)

time_sequence = list([i for i in range(time + 1)])
print(optimum_results[1], optimum_results[2], optimum_results[3],
      optimum_results[4], optimum_results[5], optimum_results[6])
build_plot(optimum_results[0], statistic_values, time_sequence, statuses_names, medical_statuses_names)
