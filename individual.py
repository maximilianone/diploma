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
        self.age = [randint(0, self.lifespan[0] - 1), randint(0, 11)]
    # def get_death_probability(self, step, death_rate):
    #     return (1 - np.exp(-(self.age[0] * death_rate) ** 4)) * (step[0] + step[1] / 12)

    def get_examination_probability(self, probability):
        return probability * np.exp(
            probability * (self.last_examination_count[0] * 12 + self.last_examination_count[1]))

    def set_lifespan(self, life_expectancy):
        self.lifespan = [int(np.round(life_expectancy * (-np.log(random())) ** 0.3)), randint(0, 11)]
