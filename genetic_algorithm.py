import random, heapq

seed(23)

class GA:
    def __init__(self, population_size):
        self.population = self.generate_population(length=100, size=population_size)

    def pair_matching(self):
        # shuffle the population
        random.shuffle(self.population)
        # create the pairs

        # create the children

        # make them compete

        # return the new population

    def crossover(self, length=100, crossover_type="2X"):
        # choose crossover type (two point or uniform)
        # receive two parents and compute the children
        child = []
        if crossover_type == "2X":
            # two point crossover (2X)
            cross_point = [random.randint(0, length), random.randint(0, length)]
            while cross_point[0] == cross_point[1]:
                cross_point[1] == random.randint(0, length)
            cross_point.sort()
            child.append(parent[0][0:cross_point[0]] + parent[1][cross_point[0]:cross_point[1]] + parent[0][cross_point[1]:length])
            child.append(parent[1][0:cross_point[0]] + parent[0][cross_point[0]:cross_point[1]] + parent[1][cross_point[1]:length])
            return child
        else:
            # uniform crossover (UX)
            child_1 = ''
            child_2 = ''
            for i in range(length):
                prop = random.random()
                if prop > 0.5:
                    child_1 += parent[1][i]
                    child_2 += parent[0][i]
                else:
                    child_1 += parent[0][i]
                    child_2 += parent[1][i]
            child = [child_1, child_2]
            return child

    def family_competition(self, k=2):
        #family = [parents, children]          
        # call fitness function for the family
        #family_fitness = fitness(family)
        total_fitness = [parent_fitness, children_fitness]
        best_solution = heapq.nlargest(2, total_fitness)
        best_solution_index = [total_fitness.index(best_solution[0]), total_fitness.index(best_solution[1])]
        
        return [family[best_solution_index[0], family[best_solution_index[1]]]

    def generate_population(self, length=100, size=10):
        def get_binary_string(length):
            return ''.join((random.choice('01') for i in range(length)))

        return [get_binary_string(length) for i in range(size)]
