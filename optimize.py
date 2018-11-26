from simulate import simulate
import pandas as pd
import numpy as np
from plot_builder import build_plot
from population import Population


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

time = 144
step = [0, 1]

population_statistic = np.array(df['population'].values.tolist()[12:157])
susceptible_statistic = np.array(df['susceptible'].values.tolist()[12:157])
treated_statistic = np.array(df['treated%'].values.tolist()[12:157])
population_treated = df['treated%'].values.tolist()[:12]
hiv_statistic = np.array(df['hiv'].values.tolist()[12:157])
aids_statistic = np.array(df['aids'].values.tolist()[12:157])
quantifier = 20
agents = 1000 * quantifier
delimiter = population_statistic[0] / agents

treated_statistic = np.array([int(np.round(i)) for i in (treated_statistic * (hiv_statistic + aids_statistic))])

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
aids_examined = 2
aids_wrong_examined = 0
aids_treated = 0

population_distribution = [[susceptible, susceptible_examined], [hiv, hiv_wrong_examined, hiv_examined, hiv_treated],
                           [aids, aids_wrong_examined, aids_examined, aids_treated]]

population = Population(population_distribution)
population.population_treated = population_treated
population.transition_matrix = [[1.0, 0.0, 0.0, 0.0],
                                [0.0, 0.993127610306856, 0.005793699432760308, 0.0010786902603837061],
                                [0.0, 0.0, 0.9941233226771411, 0.005876677322858956]]
population.transition_treated_matrix = [[1], [0.0, 0.9998330154088951, 0.00016361910077234633, 3.3654903324941644e-06],
                                        [0.0, 0.0, 0.9999740079580219, 2.5992041978020294e-05]]
population.transition_medical_matrix = [[0.00309876971845901], [0.0022893188245755166, 0.03803177478377469]]
population.population_death_rate = 0.0004818770463706198
population.average_infected_vector = [0.03088048550225484, 0.001477381928906738]
population.wrong_examination = 0
population.populate()

names = ['susceptible', 'hiv', 'aids', 'treated']
time_sequence = list([i for i in range(time + 1)])


def optimize(time, step, population):
    distribution_sequences, population_sequence = simulate(time, step, population)
    return values_to_statistic(distribution_sequences)


build_plot(optimize(time, step, population), statistic_values, time_sequence, names)