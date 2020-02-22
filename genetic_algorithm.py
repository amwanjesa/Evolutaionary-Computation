import random
from operator import itemgetter

from fitness import Fitness

random.seed(40)


class GA:
    def __init__(self, population_size, fitness_function='ones'):
        self.population = self.generate_population(
            length=100, size=population_size)
        self.generation = 0
        self.failed_generation = False
        self.fitness_function = fitness_function

    def create_new_population(self):
        # shuffle the population
        random.shuffle(self.population)
        new_population = []
        failed_offspring = []
        # create the pairs
        selection_errors = 0
        parent_disagreements = 0
        for i in range(int(len(self.population)/2)):
            self.parent = [self.population[2*i], self.population[2*i+1]]
            # create the children
            self.children = self.crossover(length=100, crossover_type='2X')
            # make them compete
            selection, failed_reproduction = self.family_competition(k=2)
            errors, disagreements = self.selection_error(selection)
            selection_errors += errors
            parent_disagreements += disagreements

            failed_offspring += failed_reproduction
            # return the new population
            new_population += selection

        print(f'Number of selection errors: {selection_errors}')
        print(f'Number of parent disagreements: {parent_disagreements}')
        self.failed_generation = all(failed_offspring)
        self.population = new_population
        self.generation += 1
        return selection_errors, parent_disagreements

    def crossover(self, length=100, crossover_type='2X'):
        # choose crossover type (two point or uniform)
        # receive two parents and compute the children
        children = []
        if crossover_type == '2X':
            # two point crossover (2X)
            cross_point = [random.randint(
                0, length), random.randint(0, length)]
            while cross_point[0] == cross_point[1]:
                cross_point[1] = random.randint(0, length)
            cross_point.sort()
            children.append(self.parent[0][0:cross_point[0]] + self.parent[1]
                            [cross_point[0]:cross_point[1]] + self.parent[0][cross_point[1]:length])
            children.append(self.parent[1][0:cross_point[0]] + self.parent[0]
                            [cross_point[0]:cross_point[1]] + self.parent[1][cross_point[1]:length])
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

    def selection_error(self, selection):
        diffs = [int(x) & int(y) for x, y in zip(*self.parent)]
        number_of_errors = 0
        number_of_disagreements = len([x for x in diffs if not x])
        for i, x in enumerate(diffs):
            number_of_errors += int(not x and not (
                int(selection[0][i]) & int(selection[1][i])))
        return number_of_errors, number_of_disagreements

    def family_competition(self, k=2):

        parent_fitness = [(solution, Fitness.get_fitness(
            solution, function=self.fitness_function)) for solution in self.parent]
        child_fitness = [(solution, Fitness.get_fitness(
            solution, function=self.fitness_function)) for solution in self.children]
        failed_reproduction = [baby_fitness[1] <= max(parent_fitness, key=itemgetter(1))[
            1] for baby_fitness in child_fitness]

        family_fitness = parent_fitness + child_fitness
        sorted_family = sorted(
            family_fitness, key=lambda x: x[1], reverse=True)
        kth_best, kth1_best = sorted_family[k - 1], sorted_family[k]

        if kth_best[1] == kth_best[1]:
            if kth1_best[0] in self.parent and not kth_best in self.parent:
                sorted_family[k - 1] = kth1_best
                sorted_family[k] = kth_best

        return [solution[0] for solution in sorted_family[:k]], failed_reproduction

    def global_optimum_found(self, length=100):
        global_optimum = '1' * length
        return global_optimum in self.population

    def generate_population(self, length=100, size=10):
        def get_binary_string(length):
            return ''.join((random.choice('01') for i in range(length)))

        return [get_binary_string(length) for i in range(size)]

    def population_stats(self):
        return [Fitness.get_fitness(solution, function=self.fitness_function) for solution in self.population]
