from graph import *
import pandas as pd
import pprint

def read_graph_data(filename):
    connections = []
    graph = Graph()
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                connections.append(l[3:])
                graph.add_node(l[0], l[2])
                for node in l[3:]:
                    graph.add_edge(l[0], node)
        net = graph.create_network(connections)

    return graph, net


if __name__ == '__main__':
    graph, net = read_graph_data('Graph500.txt')
    print(net)
    graph.init_partition()
