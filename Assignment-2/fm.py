from graph import *
import pandas as pd
import pprint

def read_graph_data(filename):
    connections = []
    net = []
    counter = 0
    graph = Graph()
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                connections.append(l[3:])
                graph.add_node(l[0], l[2])
                for node in l[3:]:
                    graph.add_edge(l[0], node)
                
        for i in connections:
            counter += 1 
            for j in i:
                #intersection of i and connections[j]
                inters = list(set(i).intersection(set(connections[int(j)-1])))
                if len(inters) > 0: 
                    inters.extend([str(counter), j])
                    inters.sort()
                else:
                    inters.extend([str(counter), j])
                    inters.sort()
                if inters not in net:
                    net.append(inters) 

    return graph, net


if __name__ == '__main__':
    graph, net = read_graph_data('Graph500.txt')
    pp = pprint.PrettyPrinter()
    pp.pprint(net)
    print(len(net))
    graph.init_partition()
