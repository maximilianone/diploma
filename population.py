from individual import Individual
import copy


class Population:
    def __init__(self, state_distribution, transition_medical_matrix):
        self.state_distribution = state_distribution
        self.transition_matrix = []
        self.transition_treated_matrix = []
        self.transition_medical_matrix = transition_medical_matrix
        self.members = []
        self.population_change_rate = 0
        self.populate()

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
                    individual.set_age()
                    self.members.append(individual)

    def get_infection_quantifier(self):
        return self.state_distribution[1][0] + self.state_distribution[2][0]
