class Node:

    def __init__(self, coordinates, degree):
        self.degree = degree
        self.coordinaters = coordinates

class Edge: 
    def __init__(self, source, target):
        self.source = source 
        self.target = target

class Graph: 
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    
    def add_node(self, source, target):
        pass