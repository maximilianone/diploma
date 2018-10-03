from random import *
import numpy as np

life_expectancy = 70


class Individual:
    def __init__(self, state, medical_state, age):
        self.state = state
        self.medical_state = medical_state
        self.age = age
        self.lifespan = get_lifespan()

    def __repr__(self):
        return 'State :' + str(self.state) + ' Age:' + str(self.age) + ' Lifespan:' + str(self.lifespan)

    def __str__(self):
        return 'State :' + str(self.state) + ' Age:' + str(self.age) + ' Lifespan:' + str(self.lifespan)

    def set_age(self):
        self.age = [randint(0, self.lifespan[0] -1), randint(0, 11)]


def get_lifespan():
    return [int(np.round(life_expectancy *(-np.log(random()))**0.3)), randint(0, 11)]
