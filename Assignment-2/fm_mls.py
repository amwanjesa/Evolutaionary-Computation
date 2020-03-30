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


if __name__ == '__main__':

    nodes, connections, degrees, freedoms = read_graph_data(
        'Graph500.txt')
    data_storage = join('data', 'mls')
    solutions = pd.DataFrame()
    limit_in_seconds = 60
    for j in range(2):
        tic2 = perf_counter()
        try:
            graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
            previous_solution = {}
            with(time_limit(limit_in_seconds, 'MLS')):
                while True:
                    if previous_solution:
                        graph.init_partition(previous_solution['solution'])
                    else:
                        graph.init_partition()

                    graph.setup_gains()
                    result = graph.fiduccia_mattheyses()
                    previous_solution = result



                solution['cutstate'] = previous_solution['cutstate']
                solution = previous_solution['solution']

                solutions = solutions.append(
                    solution, ignore_index=True)
                del graph
        except TimeoutException:
            toc2 = perf_counter()
            print(f'MLS timed out after {toc2 - tic2}')
            solutions.to_csv(join(data_storage, f'mls_with_fm_time_limited_{limit_in_seconds}.csv'))
    solutions.to_csv(join(data_storage, f'mls_with_fm_time_limited_{limit_in_seconds}.csv'))
