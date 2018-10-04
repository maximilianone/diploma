from individual import Individual
from random import *
import numpy as np
import scipy.stats as s

individual = Individual(0, 0, 0)
ast = np.random.randint(0,70,100)
hist, bin_edges = np.histogram(ast)
print(s.exponweib.sf(10, 1, 2, loc=0, scale=1))