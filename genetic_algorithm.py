import random


class GA:
    def __init__(self, population_size):
        self.population = self.generate_population(length=)

    def crossover(self):
        pass

    def mutate(self):
        pass

    def family_competition(self, k=2):
        pass

    def generate_population(self, length=100, size=10):
        def get_binary_string(length):
            return ''.join((random.choice('01') for i in range(length)))

        return [get_binary_string(length) for i in range(size)]
