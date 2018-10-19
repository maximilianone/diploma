from random import *
import numpy as np


class Individual:
    def __init__(self, state, medical_state, age):
        self.state = state
        self.medical_state = medical_state
        self.age = age
        self.last_examination_count = [0, 0]
        self.lifespan = [0, 0]

    def __repr__(self):
        return 'State :' + str(self.state) + ' Medical state :' + str(self.medical_state) + ' Age:' + str(self.age)

    def __str__(self):
        return 'State :' + str(self.state) + ' Medical state :' + str(self.medical_state) + ' Age:' + str(self.age)

    def set_age(self):
        year = randint(0, self.lifespan[0] - 1) if self.lifespan[0] > 1 else 1
        self.age = [year, randint(0, 11)]

    def get_examination_probability(self, probability):
        return probability * np.exp(
            probability * (self.last_examination_count[0] * 12 + self.last_examination_count[1]))

    def set_lifespan(self, life_expectancy):
        self.lifespan = [int(np.round(life_expectancy * (-np.log(random())) ** 0.3)), randint(0, 11)]
