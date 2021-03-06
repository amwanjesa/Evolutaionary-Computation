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
    limit_in_seconds = 15
    for j in range(25):
        tic2 = perf_counter()
        graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
        previous_solution = {}
        try:
            with(time_limit(limit_in_seconds, 'MLS')):
                while True:
                    if previous_solution:
                        graph.init_partition(previous_solution['solution'])
                    else:
                        graph.init_partition()

                    graph.setup_gains()
                    result = graph.fiduccia_mattheyses()
                    previous_solution = result



        except TimeoutException:
            pass
        solution = previous_solution['solution']
        solution['cutstate'] = previous_solution['cutstate']
        solution = previous_solution['solution']
        solutions = solutions.append(
            solution, ignore_index=True)
        del graph
    solutions.to_csv(join(data_storage, f'mls_with_fm_time_limit_{limit_in_seconds}.csv'))
