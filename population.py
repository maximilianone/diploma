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
        self.population_birth_rate = 0
        self.population_death_rate = 0
        self.wrong_examination = 0
        self.infection_vector = []

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
                    individual = Individual(i, j, 0)
                    individual.set_lifespan(int(np.round(1 / self.population_death_rate)))
                    individual.set_age()
                    self.members.append(individual)

    def get_infection_probability(self):
        # infected_people = 0
        # infected_treated_people = 0
        # for i in range(1, len(self.state_distribution)):
        #     infected_people += self.state_distribution[i][0]
        #     infected_treated_people += self.state_distribution[i][3]
        # beta_1 = self.find_quantifier(self.infection_vector[0], infected_treated_people / infected_people)
        # beta_2 = self.find_quantifier(self.infection_vector[1], infected_treated_people / infected_people)
        # return beta_1 * (((infected_people - infected_treated_people) / len(self)) + beta_2 * (
        #             infected_treated_people / len(self)))
        return self.infection_vector[0][0]

    @staticmethod
    def find_quantifier(vector, r):
        val = vector[len(vector) - 2] * np.exp(-vector[len(vector) - 1] * r)
        vector.append(val)
        return vector[len(vector) - 1]
