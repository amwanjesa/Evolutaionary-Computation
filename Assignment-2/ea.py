import random
import numpy as np
from scipy.spatial.distance import hamming
from graph import *

random.seed(673)


class GLS:
    def __init__(self, population_size):
        self.population = self.generate_population(
            length=500, size=population_size)

    def generate_population(self, length=500, size=50):
        def get_graph_partition(length):
            ones = [1] * (length / 2)
            zeroes = [0] * (length / 2)
            individual = np.random.choice(ones +zeroes, length, replace=False)
            return individual
        return [get_graph_partition(length) for i in range(size)]

    def crossover(self, length=500):
        # Uniform crossover
        child = []
        index_free_bits = []
        random.shuffle(self.population)
        index = random.sample(list(range(len(self.population))), 2)
        self.parents = [self.population[index[0]], self.population[index[1]]]
        # Compute hamming distance
        parents_distance = hamming(self.parents[0], self.parents[1])
        # If hamming distance higher than l/2 change bits of one parent
        if parents_distance > 0.5:
            new_parent = [1 if number ==
                          0 else 0 for number in self.parents[0]]
        else:
            new_parent = self.parents[0]
        # Create offspring
        for i in range(len(new_parent)):
            if new_parent[i] == self.parents[1][i]:
                child.append(new_parent[i])
            else:
                child.append(random.randint(0, 1))
                index_free_bits.append(i)
        
        if self.parents[1] == new_parent:
            return child
        else:
            return self.check_equality(length, index_free_bits, child)

    def check_equality(self, length, possible_indeces, individual):
        if sum(individual) != (length/2):
            number_changes = int(abs((length/2) - sum(individual)))
            change = random.sample(possible_indeces, number_changes)
            for i in change:
                if individual[i] == 1:
                    individual[i] = 0
                else:
                    individual[i] = 1
        return individual

    def create_new_population(self, new_child, child_cutstate, ranked_population):
        new_population = []
        # Get worse individual
        worst_cutstate = max(ranked_population.keys())
        contestant = ranked_population[worst_cutstate]
        if len(ranked_population[worst_cutstate]) > 1:
            contestant = contestant[random.randint(0, (len(ranked_population[worst_cutstate])-1))]
        if len(ranked_population[worst_cutstate]) == 1:
            contestant = contestant[0]
        # Make it compete with the child
        if child_cutstate <= worst_cutstate:
            for i in range(len(self.population)):
                if self.population[i] != contestant:
                    new_population.append(self.population[i])
                if self.population[i] == contestant:
                    new_population.append(new_child)
        else:
            new_population = self.population

        self.population = new_population

    def transform_person(self, person):
        return {i+1 : person[i] for i in range(len(person))}
