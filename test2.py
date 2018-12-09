from simulate import simulate
import pandas as pd
import numpy as np
from plot_builder import build_plot
from population import Population
from monte_carlo import find_deviation


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
quantifier = 10
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
aids_examined = 1
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

names = ['Здорові (вразливі)', 'ВІЛ-інфіковані', 'Хворі на СПІД', 'Отримуючі АРТ']
time_sequence = list([i for i in range(time + 1)])


def optimize(time, step, population):
    distribution_sequences, population_sequence = simulate(time, step, population)
    print(population.infected_dead)
    print(population.state_distribution[0][1] + population.state_distribution[1][1] + \
          population.state_distribution[2][1] + population.state_distribution[1][2] + \
          population.state_distribution[2][2])
    return values_to_statistic(distribution_sequences)


simulation = optimize(time, step, population)
print(find_deviation(statistic_values, simulation))
build_plot(simulation, statistic_values, time_sequence, names)