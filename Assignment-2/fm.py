import numpy as np
import pandas as pd
from tqdm import tqdm
from random import shuffle


def read_graph_data(filename):

    graph_data = {}
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                graph_data[l[0]] = {'coordinates': l[1],
                                    'degree': l[2], 'ID_connections': l[3:]}
    return graph_data


def random_initial_partitioning(graph_data):

    nodes = list(graph_data.keys())
    shuffle(nodes)

    partition_a = { node: graph_data[node] for node in nodes[:len(nodes) // 2]}
    partition_b = { node: graph_data[node] for node in nodes[len(nodes) // 2:]}

    return partition_a, partition_b


if __name__ == '__main__':

    np.random.seed(352)

    graph = read_graph_data('Graph500.txt')
    partitions = random_initial_partitioning(graph)