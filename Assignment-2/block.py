class Block:
    def __init__(self, nodes=[], freedoms={}, max_degree=0):
        self.nodes = nodes
        self.freedoms = freedoms
        self.max_degree = max_degree
        self.gains_storage = {i: set()
                              for i in range(-max_degree, max_degree + 1)}
        self.highest_gain = 0

    @property
    def size(self):
        return len(self.nodes)

    def add_node(self, node, freedom):
        self.nodes.append(node)
        self.freedoms[node] = freedom

    def get_nodes_at_gain(self, gain_value):
        return self.gains_storage[gain_value]

    def save_node_at_gain(self, node, gain_value):
        self.gains_storage[gain_value].add(node)
        self.update_highest_gain()

    def get_free_node_with_highest_gain(self):
        # print(f'Highest gain: {self.highest_gain}')
        nodes = [node for node in self.gains_storage[self.highest_gain] if self.freedoms[node]]
        if not nodes:
            self.highest_gain -= 1
            return self.get_free_node_with_highest_gain()
        else:
            return nodes


    def lock_node(self, node):
        self.freedoms[node] = False

    def update_highest_gain(self):
        for i in self.gains_storage.keys():
            if self.gains_storage[i]:
                self.highest_gain = i

    def remove_node(self, node):
        self.nodes.remove(node)
        del self.freedoms[node]
        for gain, nodes in self.gains_storage.items():
            if node in nodes:
                self.gains_storage[gain].remove(node)
        self.update_highest_gain()
                #break
        

    def contains_node(self, node):
        return node in self.nodes
    
    def has_free_nodes(self):
        return any(x for x in self.freedoms.values())
