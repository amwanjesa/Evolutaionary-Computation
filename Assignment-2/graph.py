from random import shuffle


class Node:

    def __init__(self, id, degree):
        self.id = id
        self.degree = degree


class Edge:
    def __init__(self, source, target):
        self.pair = set([source, target])


class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges
        self.block_a = None
        self.block_b = None

    def add_node(self, id, degree):
        new_node = Node(id, degree)
        self.nodes.append(new_node)

    def add_edge(self, source, target):
        new_edge = Edge(source, target)
        if not new_edge in self.edges:
            self.edges.append(new_edge)

    def init_partition(self):
        shuffle(self.nodes)

        self.block_a = self.nodes[:len(self.nodes) // 2]
        self.block_b = self.nodes[:len(self.nodes) // 2]
