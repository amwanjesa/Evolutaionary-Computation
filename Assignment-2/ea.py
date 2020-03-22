import random
import numpy as np
from scipy.spatial.distance import hamming

class GLS:
    def __init__(self, population_size):
        self.population = self.generate_population(length=500, size=population_size)

    def crossover(self):
        # Uniform crossover
        child = []
        index_free_bits = []
        # Compute hamming distance
        parents_distance = hamming(self.parents[0], self.parents[1])
        # If hamming distance higher than l/2 change bits of one parent
        if parents_distance > 0.5:
            new_parent = [1 if number == 0 else 0 for number in self.parents[0]]
        else:
            new_parent = self.parents[0]
        # Create offspring
        for i in range(len(new_parent)):
            if new_parent[i] == self.parents[1][i]:
                child.append(new_parent[i])
            else:
                child.append(random.randint(0,1))
                index_free_bits.append(i)
        return check_equality(length, index_free_bits, child)

    def generate_population(self, length=500, size=50):
        def get_binary_string(length):
            for i in range(length):
                person = [].append(random.randint(0,1))
            return check_equality(length, (length-1), person)
    return [get_binary_string(length) for i in range(size)]

    def check_equality(self, length=500, possible_indeces, individual):
        if sum(individual) != (length/2):
            number_changes = int(abs((length/2) - sum(individual)))
            change = random.sample(possible_indeces, number_changes)
            for i in change:
                if individual[i] == 1:
                    individual[i] = 0
                else:
                    individual[i] = 1
        return individual