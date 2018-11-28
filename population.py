from individual import Individual
import copy
import numpy as np


class Population:
    def __init__(self, state_distribution):
        self.state_distribution = state_distribution
        self.transition_matrix = []
        self.transition_treated_matrix = []
        self.transition_medical_matrix = []
        self.members = []
        self.population_death_rate = 0
        self.wrong_examination = 0
        self.average_infected_vector = []
        self.infected_dead = 0

    def __len__(self):
        return len(self.members)

    def populate(self):
        state_distribution = copy.deepcopy(self.state_distribution)
        for i in range(len(state_distribution)):
            for j in range(1, len(state_distribution[i])):
                state_distribution[i][0] -= state_distribution[i][j]

        for i in range(len(state_distribution)):
            for j in range(len(state_distribution[i])):
                for k in range(state_distribution[i][j]):
                    individual = Individual(i, j)
                    self.members.append(individual)
