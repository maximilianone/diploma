import matplotlib.pyplot as plt
from random import *
import numpy as np

time = 12
x = list([i for i in range(time)])


def poisson(k, l):
    return np.exp(-l) * (l ** k) / np.math.factorial(k)


y = []
for i in range(time):
    y.append(poisson(i, 4))

count = 0

for moment in range(time):
    count += np.random.poisson(2/12)

print(count)
