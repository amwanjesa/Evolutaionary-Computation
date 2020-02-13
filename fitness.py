class Fitness:

    def __init__(self):
        pass

    def count_ones(self, solution):
        return solution.count('1')
    
    def trap_function(self, solution, k, d):
        fitness = 0
        scalar = (k - d) / (k - 1)
        for subsolution in zip(*(iter(solution),) * k):
            if self.count_ones(subsolution) == k:
                fitness += k
            elif self.count_ones(subsolution) < k:
                fitness += k - d - scalar * self.count_ones(solution)
        return fitness