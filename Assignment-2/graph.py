from random import shuffle, randint, seed
from tqdm import tqdm
from block import Block
from operator import itemgetter

#seed(21)


class Node:

    def __init__(self, id, degree):
        self.id = id
        self.degree = degree
        self.free = True


class Edge:
    def __init__(self, endpoint_1, endpoint_2):
        self.pair = set([endpoint_1, endpoint_2])


class Graph:
    def __init__(self, nodes=[], degrees=[], connections={}, freedoms={}):
        self.nodes = nodes
        self.degrees = degrees
        self.connections = connections
        self.freedoms = freedoms
        self.block_a = None
        self.block_b = None
        self.bucket_list = nodes
        self.best_solution = []
        self.best_cutstate = None

        self.current_solution = []
        self.current_cutstate = None

        self.fm_limit = 10000

    def add_node(self, new_node_id, degree):
        self.nodes.append(new_node_id)
        self.degrees.append(degree)
        self.freedoms[new_node_id] = True

    def remove_node(self, node):
        self.nodes.remove(node)

    def add_connection(self, node, connections):
        self.connections[node] = connections

    def init_partition(self, previous_solution={}):
        count_b_block = 0
        if previous_solution:
            nodes_1 = []
            nodes_2 = []
            freedoms_1 = {}
            freedoms_2 = {}
            count = 0
            for i, (node, in_a) in enumerate(previous_solution.items()):
                if in_a:
                    nodes_1.append(node)
                    freedoms_1[node] = True
                else:
                    count_b_block += 1
                    nodes_2.append(node)
                    freedoms_2[node] = True
            self.block_a = Block(
                nodes=nodes_1, freedoms=freedoms_1, max_degree=max(self.degrees))
            self.block_b = Block(
                nodes=nodes_2, freedoms=freedoms_2, max_degree=max(self.degrees))
        else:
            shuffle(self.nodes)
            halfway = len(self.nodes) // 2
            nodes_1 = self.nodes[:halfway]
            nodes_2 = self.nodes[halfway:]

            freedoms_1 = {k: v for k, v in self.freedoms.items()
                          if k in nodes_1}
            freedoms_2 = {k: v for k, v in self.freedoms.items()
                          if k in nodes_2}

            self.block_a = Block(
                nodes=nodes_1, freedoms=freedoms_1, max_degree=max(self.degrees))
            self.block_b = Block(
                nodes=nodes_2, freedoms=freedoms_2, max_degree=max(self.degrees))

    def setup_gains(self):
        for node in self.bucket_list:#self.nodes:
            if self.block_a.contains_node(node): #and self.block_a.freedoms[node]:
                gain = self.calculate_gain(node)
                self.block_a.save_node_at_gain(node, gain)
            elif self.block_b.contains_node(node): #and self.block_b.freedoms[node]:
                gain = self.calculate_gain(node)
                self.block_b.save_node_at_gain(node, gain)

    def calculate_gain(self, node):
        gain = 0

        #!!! This might be wrong
        node_block = self.block_a if self.block_a.contains_node(
            node) else self.block_b
        for neighbour in self.connections[node]:
            if node_block.contains_node(neighbour):
                gain -= 1
            else:
                gain += 1
        return gain

    def get_solution(self):
        solution = {}
        for node in self.nodes:
            if self.block_a.contains_node(node):
                solution[node] = 1
            else:
                solution[node] = 0
        return solution

    def get_cutstate(self):
        cutstate = 0
        seen = []
        for node in self.nodes:
            connections = self.connections[node]
            for neighbour in connections:
                if frozenset((node, neighbour)) in seen:
                    continue
                node_block = self.block_a if self.block_a.contains_node(
                    node) else self.block_b
                if not all([node_block.contains_node(cell) for cell in (node, neighbour)]):
                    cutstate += 1
                seen.append(frozenset((node, neighbour)))
        return cutstate

    def update_solution(self):
        new_cutstate = self.get_cutstate()
        if self.current_cutstate is not None:
            if new_cutstate < self.current_cutstate:
                self.current_solution = self.get_solution()
                self.current_cutstate = new_cutstate
        else:
            self.current_solution = self.get_solution()
            self.current_cutstate = new_cutstate

    def swap(self):
        largest_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b
        possible_nodes = largest_block.get_free_node_with_highest_gain()
        node_index = randint(0, (len(possible_nodes)-1))
        node = possible_nodes[node_index]

        # Remove node from current block and move it to the other one
        largest_block.remove_node(node)
        other_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b

        # Mark moved node as not free
        other_block.add_node(node, False)
        other_block.lock_node(node)

        # Updated gains using self.setup_gains
        self.bucket_list.pop(self.bucket_list.index(node))
        self.setup_gains()

        # Select new node
        possible_nodes = other_block.get_free_node_with_highest_gain()
        node_index = randint(0, (len(possible_nodes)-1))
        node = possible_nodes[node_index]

        # Remove node from current block
        other_block.remove_node(node)

        # Move it to the other block and Set node to false
        largest_block.add_node(node, False)
        largest_block.lock_node(node)

        # Gains update
        self.bucket_list.pop(self.bucket_list.index(node))
        self.setup_gains()

        # Calculate new solution
        self.update_solution()

    def fiduccia_mattheyses(self):
        keep_searching = True
        while keep_searching and self.fm_limit:
            while self.block_a.has_free_nodes() and self.block_b.has_free_nodes() and len(self.bucket_list) != 0:
                self.swap()

            if self.best_cutstate is not None:
                if self.best_cutstate > self.current_cutstate:
                    self.best_solution = self.current_solution
                    self.best_cutstate = self.current_cutstate
                else:
                    break
            else:
                self.best_cutstate = self.current_cutstate
                self.best_solution = self.current_solution
            self.block_a.free_all_nodes()
            self.block_b.free_all_nodes()
            self.bucket_list = self.nodes
            self.setup_gains()
            self.fm_limit -= 1 

        return {'solution': self.current_solution, 'cutstate': self.current_cutstate}
