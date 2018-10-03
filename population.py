from individual import Individual


class Population:
    def __init__(self, state_distribution, members, birth_rate, birth_state_matrix):
        self.state_distribution = state_distribution
        self.transition_matrix = []
        self.transition_treated_matrix = []
        self.members = members
        self.birth_rate = birth_rate
        self.birth_state_matrix = birth_state_matrix
        self.populate(state_distribution)

    def __len__(self):
        population_length = 0
        for status_count in self.state_distribution:
            population_length += status_count
        return population_length

    def populate(self, state_distribution):
        for i in range(len(state_distribution)):
            for j in range(state_distribution[i]):
                individual = Individual(i, 0)
                individual.set_age()
                self.members.append(individual)
