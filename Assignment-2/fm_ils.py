import random
from os.path import join
from time import perf_counter

import pandas as pd
from tqdm import tqdm

from graph import *


def read_graph_data(filename):
    connections = {}
    nodes = []
    degrees = {}
    freedoms = {}
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                node, degree, neighbours = int(l[0]), int(l[2]), [
                    int(x) for x in l[3:]]
                connections[node] = neighbours
                freedoms[node] = True
                nodes.append(node)
                degrees[node] = degree

    return nodes, connections, degrees, freedoms


def mutation(solution, perturbation=0.01):
    def mutate(current_solution, perturbation):
        new_solution = {}
        for node, block in current_solution.items():
            if random.random() <= perturbation:
                if block == 1:
                    new_solution[node] = 0
                else:
                    new_solution[node] = 1
            else:
                new_solution[node] = block
        return new_solution

    new_solution = mutate(solution, perturbation)
    while list(new_solution.values()).count(1) != list(new_solution.values()).count(0):
        new_solution = mutate(solution, perturbation)
    return new_solution


if __name__ == '__main__':

    nodes, connections, degrees, freedoms = read_graph_data(
        'Assignment-2\Graph500.txt')
    mutation_rate = 0.01
    performance_stats = pd.DataFrame()
    data_storage = join('Assignment-2', 'data', 'ils')
    for j in range(25):
        solutions = pd.DataFrame()
        cutstates = pd.DataFrame()
        found_same_cutstate = 0
        tic = perf_counter()
        for i in tqdm(range(2500), desc='Fiducca Mattheyses experiments'):
            graph = Graph(nodes=nodes, connections=connections,
                          freedoms=freedoms, degrees=degrees)
            if not solutions.empty:
                best_solution = solutions.loc[:,
                                              solutions.columns != 'cutstate'].iloc[-1].to_dict()
                graph.init_partition(
                    mutation(best_solution, perturbation=mutation_rate))
            else:
                graph.init_partition()
            graph.setup_gains()
            result = graph.fiduccia_mattheyses()

            # print(f'Local search found cutstate {result["cutstate"]}')

            solution = result['solution']
            solution['cutstate'] = result['cutstate']
            if solutions.empty:
                solutions = solutions.append(
                    solution, ignore_index=True)
            else:
                best_cutstate = solutions['cutstate'].iloc[-1]
                if result['cutstate'] < best_cutstate:
                    solutions = solutions.append(solution, ignore_index=True)
                elif result['cutstate'] == best_cutstate:
                    found_same_cutstate += 1
            del graph

        toc = perf_counter()
        performance_stats = performance_stats.append(
            {'Execution Time': toc - tic, 'No Change': found_same_cutstate}, ignore_index=True)
        solutions.to_csv(join(data_storage, f'ils_with_fm_run{j + 1}.csv'))
    performance_stats.to_csv(
        join(data_storage, f'ils_with_fm_{int(mutation_rate * 100)}_performance.csv'))
