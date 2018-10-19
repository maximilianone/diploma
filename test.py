from individual import Individual
from random import *
import numpy as np

deviation = 0
simulation_result = np.array([[[1, 2, 3], [0, 1, 2], [7, 3, 1]], [[1, 2, 3], [0, 1, 2], [7, 3, 1]]])
statistic = np.array([[[2, 3, 4], [1, 2, 3], [8, 4, 2]], [[2, 3, 4], [1, 2, 3], [8, 4, 2]]])
for i in range(len(simulation_result)):
    print(np.sum([a ** 2 for a in (a_row for a_row in (simulation_result[i] - statistic[i]))])/ (len(simulation_result[i][0]) * len(simulation_result[i]) * len(simulation_result)))
    deviation += np.sum(
        [a ** 2 for a in (a_row for a_row in (simulation_result[i] - statistic[i]))]) / (len(simulation_result[i][0]) * len(simulation_result[i]) * len(simulation_result))
print(np.sqrt(deviation))