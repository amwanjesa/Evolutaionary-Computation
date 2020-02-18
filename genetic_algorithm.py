import random, heapq
from fitness import Fitness
seed(23)

class GA:
    def __init__(self, population_size):
        self.population = self.generate_population(length=100, size=population_size)
        self.new_population = create_new_population()

    def create_new_population(self):
        # shuffle the population
        random.shuffle(self.population)
        new_population = []
        # create the pairs
        for i in range(len(self.population)/2):
            self.parent = [self.population[2*i], self.population[2*i+1]]
        # create the children
            self.children = self.crossover(length=100, crossover_type='2X')
        # make them compete
            selection = self.family_competition(k=2)
        # return the new population
            new_population.append(selection)
        return new_population

    def crossover(self, length=100, crossover_type='2X'):
        # choose crossover type (two point or uniform)
        # receive two parents and compute the children
        child = []
        if crossover_type == '2X':
            # two point crossover (2X)
            cross_point = [random.randint(0, length), random.randint(0, length)]
            while cross_point[0] == cross_point[1]:
                cross_point[1] == random.randint(0, length)
            cross_point.sort()
            child.append(self.parent[0][0:cross_point[0]] + self.parent[1][cross_point[0]:cross_point[1]] + self.parent[0][cross_point[1]:length])
            child.append(self.parent[1][0:cross_point[0]] + self.parent[0][cross_point[0]:cross_point[1]] + self.parent[1][cross_point[1]:length])
            return child
        else:
            # uniform crossover (UX)
            child_1 = ''
            child_2 = ''
            for i in range(length):
                prop = random.random()
                if prop > 0.5:
                    child_1 += self.parent[1][i]
                    child_2 += self.parent[0][i]
                else:
                    child_1 += self.parent[0][i]
                    child_2 += self.parent[1][i]
            child = [child_1, child_2]
            return child

    def family_competition(self, k=2):
        family = self.parent + self.children

        family_fitness = {solution:Fitness.count_ones(solution) for solution in family}          
        sorted_family = sorted(family_fitness.items(), key = lambda x: x[1])
        
        return [sorted_family[len(sorted_family)-1][0], sorted_family[len(sorted_family)-2][0]]

    def generate_population(self, length=100, size=10):
        def get_binary_string(length):
            return ''.join((random.choice('01') for i in range(length)))

        return [get_binary_string(length) for i in range(size)]
