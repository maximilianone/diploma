from random import *
import numpy as np


class Individual:
    def __init__(self, state, medical_state, additional_state=0, age=0):
        self.state = state
        self.medical_state = medical_state
        self.additional_state = additional_state
        self.last_examination_count = [0, 0]
        self.age = age

    def __repr__(self):
        return 'Age:' + str(self.age) + ' State :' + str(self.state) + ' Additional state:' + str(
            self.additional_state) + ' Medical state :' + str(self.medical_state)

    def __str__(self):
        return 'Age:' + str(self.age) + ' State :' + str(self.state) + ' Additional state:' + str(
            self.additional_state) + ' Medical state :' + str(self.medical_state)

    def get_examination_probability(self, probability):
        return probability * np.exp(
            probability * (self.last_examination_count[0] * 12 + self.last_examination_count[1]))
