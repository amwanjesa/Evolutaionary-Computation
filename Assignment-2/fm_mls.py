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


if __name__ == '__main__':

    nodes, connections, degrees, freedoms = read_graph_data(
        'Assignment-2\Graph500.txt')
    data_storage = join('Assignment-2', 'data', 'mls')
    performance_stats = pd.DataFrame()
    graph = Graph(nodes=nodes, connections=connections,
                  freedoms=freedoms, degrees=degrees)
    solutions = pd.DataFrame()
    for j in range(3):
        tic = perf_counter()
        best_solution = {}
        for i in tqdm(range(10), desc='Fiducca Mattheyses experiments'):
            if best_solution:
                graph.init_partition(best_solution['solution'])
            else:
                graph.init_partition()

            graph.setup_gains()
            result = graph.fiduccia_mattheyses()


        solution = result['solution']
        solution['cutstate'] = result['cutstate']

        solutions = solutions.append(
            solution, ignore_index=True)
        toc = perf_counter()
        performance_stats = performance_stats.append(
            {'Execution Time': toc - tic}, ignore_index=True)
    solutions.to_csv(join(data_storage, f'mls_with_fm_run{j + 1}.csv'))
    performance_stats.to_csv(
        join(data_storage, f'mls_with_fm_performance.csv'))
