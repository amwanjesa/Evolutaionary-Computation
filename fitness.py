class Fitness:

    def __init__(self):
        pass

    @staticmethod
    def get_fitness(solution, function='ones', k=4, d=2):
        if function == 'ones':
            return Fitness.count_ones(solution)
        elif function == 'trap tight':
            if k is not None and d is not None:
                return Fitness.trap_function(solution, k, d)
            else:
                raise TypeError(
                    f'k and d have to be set to use the tightly linked trap function')
        elif function == 'trap not tight':
            if k is not None and d is not None:
                return Fitness.trap_function_not_tight(solution, k, d)
            else:
                raise TypeError(
                    f'k and d have to be set to use the not-tightly linked trap function')

    @staticmethod
    def count_ones(solution):
        return solution.count('1')

    @staticmethod
    def trap_function(solution, k, d):
        fitness = 0
        scalar = (k - d) / (k - 1)
        for subsolution in zip(*(iter(solution),) * k):
            if Fitness.count_ones(subsolution) == k:
                fitness += k
            elif Fitness.count_ones(subsolution) < k:
                fitness += k - d - scalar * Fitness.count_ones(subsolution)
        return fitness

    @staticmethod
    def trap_function_not_tight(solution, k, d):
        fitness = 0
        scalar = (k - d) / (k - 1)
        spread = int(len(solution) / k)
        for start_point in range(spread):

            subsolution = [solution[i] for i in range(
                start_point, start_point + len(solution), spread)]
            print(subsolution)
            if Fitness.count_ones(subsolution) == k:
                fitness += k
            elif Fitness.count_ones(subsolution) < k:
                fitness += k - d - scalar * Fitness.count_ones(subsolution)
        return fitness
