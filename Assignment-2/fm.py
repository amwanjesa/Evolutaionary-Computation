import numpy as np
import pandas as pd
from tqdm import tqdm
from random import shuffle
from graph import *


def read_graph_data(filename):

    graph = Graph()
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                graph.add_node(l[0], l[2])
                for node in l[3:]:
                    graph.add_edge(l[0], node)
    return graph

if __name__ == '__main__':

    np.random.seed(352)

    graph = read_graph_data('Graph500.txt')
    graph.init_partition()