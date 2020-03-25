import logging
import pprint
import traceback
from collections import Counter

import pandas as pd
from tqdm import tqdm

from graph import *


def read_graph_data(filename):
    connections = {}
    nodes = []
    degrees = {}
    freedoms = {}
    with open(filename) as f:
        for line in f:
            l = line.split()
            if len(l) > 0:
                node, degree, neighbours = int(l[0]), int(l[2]), [int(x) for x in l[3:]]
                connections[node] = neighbours
                freedoms[node] = True
                nodes.append(node)
                degrees[node] = degree

    return  nodes, connections, degrees, freedoms

def mutation(solution, perturbation=0.01):
    new_solution = []
    while new_solution.count(1) != new_solution.count(0):
        for number in solution:
            if random.random() <= perturbation:
                if number == 1:
                    new_solution.append(0)
                else:
                    new_solution.append(1)
            else:
                new_solution.append(number)


if __name__ == '__main__':

    fm_solutions = pd.DataFrame()
    previous_solution = {}
    nodes, connections, degrees, freedoms = read_graph_data('Assignment-2\Graph500.txt')
    found_same_cutstate = 0
    
    for i in tqdm(range(2500), desc='Fiducca Mattheyses experiments'):
        graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
        if len(fm_solutions) > 0:
            best_solution = fm_solutions['cutstate'].iloc[-1]
            graph.init_partition(mutation(best_solution, perturbation=0.05))
        else:
            graph.init_partition()
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        previous_solution = result['solution']
        
        if len(fm_solutions) < 1:
            fm_solutions = fm_solutions.append(result, ignore_index=True)
        else:
            best_cutstate = fm_solutions['cutstate'].iloc[-1]
            if result['cutstate'] < best_cutstate:
                fm_solutions = fm_solutions.append(result, ignore_index=True)
            elif result['cutstate'] == best_cutstate:
                found_same_cutstate += 1


        #print(previous_solution)
        del graph
        if i == 200:
            fm_solutions.to_csv('ils_with_fm_200.csv')
    fm_solutions.to_csv('ils_with_fm.csv')
