import matplotlib.pyplot as plt
from random import *
import numpy as np

time = 70
x = list([i for i in range(time)])


def gaussian(a, b, x):
    return a * np.exp(-((x - b) ** 2) / (2 * 10 ** 2))


y = []
for i in range(time):
    y.append(gaussian(2, 35, i))

count = 0

for moment in range(time):
    count += np.random.poisson(2 / 12)

plt.plot(x, y)
plt.show()
