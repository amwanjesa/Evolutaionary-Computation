class Fitness:

    def __init__(self):
        pass

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
                fitness += k - d - scalar * Fitness.count_ones(solution)
        return fitness
    
    @staticmethod
    def trap_function_not_tight(solution, k, d):
        fitness = 0
        scalar = (k - d) / (k - 1)
        spread = len(solution) / k
        for start_point in spread:

            subsolution = [solution[i] for  in range(start_point, start_point + len(solution), spread)]
            if Fitness.count_ones(subsolution) == k:
                fitness += k
            elif Fitness.count_ones(subsolution) < k:
                fitness += k - d - scalar * Fitness.count_ones(solution)
        return fitness