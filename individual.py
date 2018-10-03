from random import *
import numpy as np

life_expectancy = 70


class Individual:
    def __init__(self, state, medical_state, age):
        self.state = state
        self.medical_state = medical_state
        self.age = age

    def __repr__(self):
        return 'State :' + str(self.state) + ' Medical state :' + str(self.medical_state) + ' Age:' + str(self.age)

    def __str__(self):
        return 'State :' + str(self.state) + ' Medical state :' + str(self.medical_state) + ' Age:' + str(self.age)

    def set_age(self):
        self.age = [randint(0, life_expectancy - 1), randint(0, 11)]

    def get_death_probability(self, probability):
        probability = probability * (16729699.82 + ((1.180329 - 16729700) / (1 + (self.age[0] / 553.2562) ** 7.453266)))
        return probability if probability <= 1 else 1

    def get_birth_probability(self, probability):
        return probability * (1.098933 * np.exp(-(self.age[0] - 39.0966) ** 2 / (2 * 15.4054) ** 2))

# def get_lifespan():
#     return [int(np.round(life_expectancy *(-np.log(random()))**0.3)), randint(0, 11)]
