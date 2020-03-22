import random
import numpy as np
from scipy.spatial.distance import hamming

class EA:
    def __init__(self):
        self.parents = np.random.choice(2, (2, 10))
        child = self.crossover()

    def crossover(self):
        # Uniform crossover
        child = []
        index_free_bits = []
        # Compute hamming distance
        parents_distance = hamming(self.parents[0], self.parents[1])
        print(f'These are the parents: {self.parents}')
        print(f'This is the distance: {parents_distance}')
        # If hamming distance higher than l/2 change bits of one parent
        if parents_distance > 0.5:
            new_parent = [1 if number == 0 else 0 for number in self.parents[0]]
        else:
            new_parent = self.parents[0]
        print(f'This is the new parent: {new_parent}')
        # Create offspring
        for i in range(len(new_parent)):
            if new_parent[i] == self.parents[1][i]:
                child.append(new_parent[i])
            else:
                child.append(random.randint(0, 1))
                index_free_bits.append(i)
        print(f'This is the child: {child}')
        # Number of ones and zeros
        equality = sum(child)
        print(f'This is the equality: {equality}')
        print(f'These are the free spots: {index_free_bits}')
        if equality != (len(new_parent)/2):
            number_bits = int(abs(equality - (len(new_parent)/2)))
            print(f'Number of bits: {number_bits}')
            bits_change = random.sample(index_free_bits, number_bits)
            for i in bits_change:
                if child[i] == 1:
                    child[i] = 0
                else:
                    child[i] = 1
        print(f'This is the final child: {child}')
        return child
