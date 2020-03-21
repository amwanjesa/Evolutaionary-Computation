import pprint

import pandas as pd
from tqdm import tqdm

from graph import *


def read_graph_data(filename):
    connections = []
    graph = Graph()
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                graph.add_connection(l[3:])
                graph.add_node(l[0], int(l[2]))
                for node in l[3:]:
                    graph.add_edge(l[0], node)

    return graph


if __name__ == '__main__':
    
    fm_solutions = pd.DataFrame()
    for i in tqdm(range(10000), desc='Fiducca Mattheyses experiments'):
        graph = read_graph_data('Graph500.txt')
        graph.create_network()
        graph.init_partition()
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        fm_solutions = fm_solutions.append(result, ignore_index=True)
        del graph
    fm_solutions.to_csv('fm_result.csv')
