import random
from fitness import Fitness
random.seed(42)

class GA:
    def __init__(self, population_size):
        self.population = self.generate_population(length=100, size=population_size)
        self.generation = 0

    def create_new_population(self):
        # shuffle the population
        random.shuffle(self.population)
        new_population = []
        # create the pairs
        for i in range(int(len(self.population)/2)):
            self.parent = [self.population[2*i], self.population[2*i+1]]
        # create the children
            self.children = self.crossover(length=100, crossover_type='2X')
        # make them compete
            selection = self.family_competition(k=2)
        # return the new population
            new_population += selection
        self.population = new_population
        self.generation += 1

    def crossover(self, length=100, crossover_type='2X'):
        # choose crossover type (two point or uniform)
        # receive two parents and compute the children
        children = []
        if crossover_type == '2X':
            # two point crossover (2X)
            cross_point = [random.randint(0, length), random.randint(0, length)]
            while cross_point[0] == cross_point[1]:
                cross_point[1] = random.randint(0, length)
            cross_point.sort()
            children.append(self.parent[0][0:cross_point[0]] + self.parent[1][cross_point[0]:cross_point[1]] + self.parent[0][cross_point[1]:length])
            children.append(self.parent[1][0:cross_point[0]] + self.parent[0][cross_point[0]:cross_point[1]] + self.parent[1][cross_point[1]:length])
            return children
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
            children = [child_1, child_2]
            return children

    def family_competition(self, k=2):
        family = self.parent + self.children
        
        family_fitness = [(solution, Fitness.count_ones(solution)) for solution in family]          
        sorted_family = sorted(family_fitness, key = lambda x: x[1], reverse=True)
        kth_best, kth1_best = sorted_family[k - 1], sorted_family[k]

        if kth_best[1] == kth_best[1]:
            if kth1_best[0] in self.parent and not kth_best in self.parent:
                sorted_family[k - 1] = kth1_best
                sorted_family[k] = kth_best
        
        return [solution[0] for solution in sorted_family[:k]]
    
    def global_optimum_found(self, length=100):
        global_optimum = '1' * length
        return global_optimum in self.population
        
    def generate_population(self, length=100, size=10):
        def get_binary_string(length):
            return ''.join((random.choice('01') for i in range(length)))

        return [get_binary_string(length) for i in range(size)]

    def population_stats(self):
        return [Fitness.count_ones(solution) for solution in self.population]
            