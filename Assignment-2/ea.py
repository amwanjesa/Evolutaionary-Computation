import random
import numpy as np
from scipy.spatial.distance import hamming
from graph import *

random.seed(673)


class GLS:
    def __init__(self, population_size):
        # Create population
        self.population = self.generate_population(length=500, size=population_size)

    def generate_population(self, length=500, size=50):
        # !!! Try mixing two lists
        def get_binary_string(length):
            person = []
            for i in range(length):
                # Create the person
                person.append(random.randint(0,1))
            # Check if the individuals have 250 1's and 250 0's and correct them
            return self.check_equality(length, list(range(length)), person)
        return [get_binary_string(length) for i in range(size)]

    def crossover(self, length=500):
        # Uniform crossover
        child = []
        index_free_bits = []

        # Get the indeces for the parents
        self.parents = random.sample(self.population, 2)

        # Compute hamming distance
        parents_distance = hamming(self.parents[0], self.parents[1])

        # If hamming distance higher than l/2 change all the bits of one parent
        if parents_distance > 0.5:
            new_parent = [1 if number == 0 else 0 for number in self.parents[0]]
        else:
            new_parent = self.parents[0]
        # Check whether both parents are equal
        if self.parents[1] == new_parent:
            return new_parent
        else:
            # If they are not create the new child
            # If the parents bit is the same append that one if not choose one randomly
            for i in range(len(new_parent)):
                if new_parent[i] == self.parents[1][i]:
                    child.append(new_parent[i])
                else:
                    child.append(random.randint(0,1))
                    index_free_bits.append(i)
            # Check that the child does not break the equality criterion
            return self.check_equality(length, index_free_bits, child)

    def check_equality(self, length, possible_indeces, individual):
        # Check the number of ones
        if sum(individual) != (length/2):
            # Calculate the number of changes to fix the kid
            number_changes = int(abs((length/2) - sum(individual)))
            # Check which bits can be changed
            # Bits selected randomly can be changed, the other bits are fixed
            change = random.sample(possible_indeces, number_changes)
            for i in change:
                if individual[i] == 1:
                    individual[i] = 0
                else:
                    individual[i] = 1
        return individual

    def create_new_population(self, length, new_child, child_cutstate, ranked_population):
        new_population = self.population
        # k is a variable to avoid copying the kid more than once if there are duplicates
        k = 0
        # Get worst cutstate
        worst_cutstate = max(ranked_population.keys())
        # Get the worst individual
        contestant = ranked_population[worst_cutstate]
        # Check if there are more than one individual with the worse cutstate
        # if so choose one of them
        if len(ranked_population[worst_cutstate]) > 1:
            contestant = contestant[random.randint(0, (len(ranked_population[worst_cutstate])-1))]
        if len(ranked_population[worst_cutstate]) == 1:
            contestant = contestant[0]
        # Make the worst contestant compete with the child
        if child_cutstate <= worst_cutstate:
            # Get the index of the worst contestant
            idx = new_population.index(contestant)
            # Change the worst contestant for the child in the population
            new_population[idx] = new_child
            # Append the new child to the cutstates dictionary
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
        # Update the population
        self.population = new_population
        return ranked_population

    def transform_person(self, person):
        # Change from list to dictionary to use the person as input for the FM
        return  {i + 1: person[i] for i in range(len(person))}
