import logging
import pprint
import traceback
from collections import Counter

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
                node, degree, neighbours = int(l[0]), int(l[2]), [int(x) for x in l[3:]]
                connections[node] = neighbours
                freedoms[node] = True
                nodes.append(node)
                degrees[node] = degree

    return  nodes, connections, degrees, freedoms


if __name__ == '__main__':

    fm_solutions = pd.DataFrame()
    previous_solution = {}
    nodes, connections, degrees, freedoms = read_graph_data('Graph500.txt')
    
    for i in tqdm(range(2500), desc='Fiducca Mattheyses experiments'):
        graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
        if previous_solution:
            graph.init_partition(previous_solution)
        else:
            graph.init_partition()
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        previous_solution = result['solution']
        #print(previous_solution)
        fm_solutions = fm_solutions.append(result, ignore_index=True)
        graph.reset()
        del graph
        if i == 50:
            fm_solutions.to_csv('fm_result_no_nets_50.csv')
