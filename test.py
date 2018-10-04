from individual import Individual
from random import *
import numpy as np

individual = Individual(0, 0, 0)

individual.set_age()

print(individual.age, individual.get_death_probability(0.15), individual.get_birth_probability(0.105))

print(randint(0, 0))
print(np.subtract([0, 2], [0, 1]))