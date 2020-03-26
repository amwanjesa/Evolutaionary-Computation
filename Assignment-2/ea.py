import random
import numpy as np
from scipy.spatial.distance import hamming
from graph import *

random.seed(673)


class GLS:
    def __init__(self, population_size):
        self.population = self.generate_population(length=500, size=population_size)

    def generate_population(self, length=500, size=50):
        def get_binary_string(length):
            person = []
            for i in range(length):
                person.append(random.randint(0,1))
            return self.check_equality(length, list(range(length)), person)
        return [get_binary_string(length) for i in range(size)]

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
            new_parent = [1 if number == 0 else 0 for number in self.parents[0]]
        else:
            new_parent = self.parents[0]
        # Create offspring
        if self.parents[1] == new_parent:
            return new_parent
        else:
            for i in range(len(new_parent)):
                if new_parent[i] == self.parents[1][i]:
                    child.append(new_parent[i])
                else:
                    child.append(random.randint(0,1))
                    index_free_bits.append(i)
        
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

    def create_new_population(self, length, new_child, child_cutstate, ranked_population):
        new_population = self.population
        k = 0
        # Get worse individual
        worst_cutstate = max(ranked_population.keys())
        contestant = ranked_population[worst_cutstate]
        if len(ranked_population[worst_cutstate]) > 1:
            contestant = contestant[random.randint(0, (len(ranked_population[worst_cutstate])-1))]
        if len(ranked_population[worst_cutstate]) == 1:
            contestant = contestant[0]
        # Make it compete with the child
        if child_cutstate <= worst_cutstate:
            idx = new_population.index(contestant)
            new_population[idx] = new_child
            if child_cutstate in ranked_population:
                ranked_population[child_cutstate].append(new_child)
            else:
                ranked_population[child_cutstate] = [new_child]
            # Delete worst contestant
            if len(ranked_population[worst_cutstate]) == 1:
                ranked_population.pop(worst_cutstate)
            else:
                idx_contestant = ranked_population[worst_cutstate].index(contestant)
                del ranked_population[worst_cutstate][idx_contestant]

        self.population = new_population
        return ranked_population

    def transform_person(self, person):
        new_person = {}
        for i in range(len(person)):
            new_person[i] = person[i]
        return new_person
