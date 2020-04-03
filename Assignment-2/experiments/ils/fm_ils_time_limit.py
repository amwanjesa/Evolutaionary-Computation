import random
from os.path import join
from time import perf_counter

import pandas as pd
from tqdm import tqdm

from graph import *
from time_limit import time_limit, TimeoutException


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
    new_solution = GLS.check_equality(500,
                                          list(range(500)), list(new_solution.values()))
    new_solution = {i + 1: new_solution[i] for i in range(len(new_solution))}
    return new_solution


if __name__ == '__main__':

    nodes, connections, degrees, freedoms = read_graph_data(
        'Graph500.txt')
    mutation_rates = [0.01, 0.03, 0.05]  # , 0.1, 0.2]
    data_storage = join('data', 'ils')
    solutions = pd.DataFrame()
    limit_in_seconds = 40
    for mutation_rate in mutation_rates:
        for j in range(25):
            graph = Graph(nodes=nodes, connections=connections,
                          freedoms=freedoms, degrees=degrees)
            cutstates = pd.DataFrame()
            found_same_cutstate = 0
            tic = perf_counter()
            best_solution = {}
            try:
                with(time_limit(limit_in_seconds, 'MLS')):
                    while True:
                        if best_solution:
                            graph.init_partition(
                                mutation(best_solution['solution'], perturbation=mutation_rate))
                        else:
                            graph.init_partition()

                        graph.setup_gains()
                        result = graph.fiduccia_mattheyses()

                        if not best_solution:
                            best_solution = result
                        elif result['cutstate'] < best_solution['cutstate']:
                            best_solution = result
                        elif result['cutstate'] == best_solution['cutstate']:
                            found_same_cutstate += 1
            except TimeoutException:
                pass
            del graph
            solution = best_solution['solution']
            solution['cutstate'] = best_solution['cutstate']
            solutions = solutions.append(
                solution, ignore_index=True)
            toc = perf_counter()
        solutions.to_csv(
            join(data_storage, f'ils_with_fm_{str(mutation_rate)}_limit_{limit_in_seconds}.csv'))
