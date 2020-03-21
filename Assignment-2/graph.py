from random import shuffle


class Node:

    def __init__(self, id, degree):
        self.id = id
        self.degree = degree
        self.free = True


class Edge:
    def __init__(self, source, target):
        self.pair = set([source, target])


class Graph:
    def __init__(self, nodes=[], edges=[], connections=[]):
        self.nodes = nodes
        self.edges = edges
        self.connections = connections
        self.block_a = None
        self.block_b = None
        self.current_solution = []
        self.current_cutstate = None

    def add_node(self, id, degree):
        new_node = Node(id, degree)
        self.nodes.append(new_node)

    def add_edge(self, source, target):
        new_edge = Edge(source, target)
        if not new_edge in self.edges:
            self.edges.append(new_edge)
        
    def remove_node(self, node):
        self.nodes.remove(node)

    def add_connection(self, connections):
        self.connections.append(connections)

    def init_partition(self):
        shuffle(self.nodes)

        self.block_a = Block(self.nodes[:len(self.nodes) // 2], self.edges)
        self.block_b = Block(self.nodes[:len(self.nodes) // 2], self.edges)

    def contains_node(self, node):
        return node in self.nodes

    def contains_node_id(self, node_id):
        return node_id in [node.id for node in self.nodes]

    def contains_edge(self, edge):
        return edge in self.edges

    def setup_gains(self):
        self.block_a.gain_storage = Gains(max([node.degree for node in self.nodes]))
        self.block_b.gain_storage = Gains(max([node.degree for node in self.nodes]))
        for node in self.nodes:
            gain = self.calculate_gain(node)
            if self.block_a.contains_node(node):
                self.block_a.gain_storage.save_node_at_gain(node, gain)
            else:
                self.block_b.gain_storage.save_node_at_gain(node, gain)

    def calculate_gain(self, node):
        gain = 0
        node_block = self.block_a if self.block_a.contains_node(
            node) else self.block_b
        for net in self.critical_network(node.id):
            if all([node_block.contains_node_id(cell) for cell in net]):
                gain += 1
            else:
                gain -= 1
        return gain

    def associated_edges(self, node):
        for edge in self.edges:
            if node.id in edge.pair:
                yield edge

    def create_network(self):
        nets = []
        counter = 0
        for i in self.connections:
            counter += 1
            for j in i:
                # intersection of i and connections[j]
                inters = list(set(i).intersection(
                    set(self.connections[int(j)-1])))
                if len(inters) > 0:
                    inters.extend([str(counter), j])
                    inters.sort()
                else:
                    inters.extend([str(counter), j])
                    inters.sort()
                if inters not in nets:
                    nets.append(inters)
        self.nets = nets

    def critical_network(self, base_cell):
        critical_network = []
        for network in self.nets:
            if str(base_cell) in network and len(network) < 4:
                critical_network.append(network)
        return critical_network

    def possible_nodes(self):
        gains = []
        possible_gains = []
        for node in self.nodes:
            gains.append([self.calculate_gain(node), node.id])
        for gain in gains:
            if gain[0] == max(gains)[0]:
                possible_gains.append(gain)
        print(possible_gains)

    def get_solution(self):
        solution = []
        for node in self.nodes:
            if self.block_a.nodes.contains_node(node):
                solution.append(1)
            else:
                solution.append(0)
        return solution

    def get_cutstate(self):
        cutstate = 0
        for node in self.block_a.nodes:
            for net in self.nets:
                if node.id in net:
                    if not all([self.block_a.contains_node_id(cell) for cell in net]):
                        cutstate += 1
        return cutstate

    def update_solution(self):
        new_cutstate = self.get_cutstate()
        if self.current_cutstate is not None:
            if new_cutstate < self.current_cutstate:
                self.initial_solution = self.get_solution()
                self.current_cutstate = new_cutstate
   
    def bipartitioning(self):
        largest_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b
        node = largest_block.gain_storage.get_node_with_highest_gain()

        # Remove node from current block and move it to the other one
        largest_block.remove_node(node)
        other_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b
        other_block.nodes.append(node)
        # Mark moved node as not free
        node.free = False
        # Updated gains using self.setup_gains
        self.setup_gains()

        # Select new node
        node = other_block.gain_storage.get_node_with_highest_gain()
        # Remove node from current block
        other_block.remove_node(node)
        # Move it to the other block
        largest_block.nodes.append(node)
        # Set node to false
        node.free = False
        # Gains update
        self.setup_gains()

        # Calculate new solution
        self.update_solution()


class Block(Graph):
    def __init__(self, nodes=[], edges=[]):
        super().__init__(nodes=nodes, edges=edges)
        self.gain_storage = None

    @property
    def size(self):
        return len(self.nodes)

    def remove_node(self, node):
        self.nodes.remove(node)
        self.gain_storage.remove_node(node)


class Gains:
    def __init__(self, max_degree):
        self.max_degree = max_degree
        self.records = {i: set() for i in range(-max_degree, max_degree + 1)}
        self.highest_gain = 0

    def get_nodes_at_gain(self, gain_value):
        return self.records[gain_value]

    def save_node_at_gain(self, node, gain_value):
        self.records[gain_value].add(node)
        self.update_highest_gain()

    def get_node_with_highest_gain(self):
        return self.records[self.highest_gain]

    def update_highest_gain(self):
        for i in self.records.keys():
            if self.records[i]:
                self.highest_gain = i
                break
    
    def remove_node(self, node):
        for gain, nodes in self.records.items():
            if node in nodes:
                self.records[gain].remove(node)
                break
