from simulate import simulate
from population import Population
import pandas as pd


df = pd.read_excel('data_studied.xlsx', usecols=[16, 19, 25, 27, 28, 30], skiprows=[0],
                   names=['hiv', 'aids', 'population', 'examined', 'examined%', 'ph. intervention%'])

# print(df['hiv'].values.tolist())

time = 165
step = [0, 1]

susceptible = 10000
hiv = 200
aids = 14


healthy_child_hiv_parent = 0.75

birth_rate = 0.015 * (step[0] + (step[1] / 12))

birth_state_matrix = [[1, 0, 0],
                      [healthy_child_hiv_parent, 1 - healthy_child_hiv_parent, 0],
                      [healthy_child_hiv_parent, 1 - healthy_child_hiv_parent, 0]]

hiv_to_aids = 0.0203 * (step[0] + (step[1] / 12))
hiv_infection = 0.01513 * (step[0] + (step[1] / 12))
aids_death = 0.0223 * (step[0] + (step[1] / 12))
hiv_death = 0.01376 * (step[0] + (step[1] / 12))

transition_matrix = [[1 - hiv_infection, hiv_infection, 0, 0],
                     [0, 1 - hiv_to_aids - hiv_death, hiv_to_aids, hiv_death],
                     [0, 0, 1 - aids_death, aids_death]]

population_distribution = [susceptible, hiv, aids]
statuses_names = ['susceptible', 'hiv', 'aids']
population = Population(population_distribution, statuses_names, transition_matrix, [], birth_rate, birth_state_matrix)

simulate(time, step, population)
