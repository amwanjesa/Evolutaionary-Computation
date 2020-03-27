import logging
import pprint
import traceback
from collections import Counter

import pandas as pd
from tqdm import tqdm

from ea import *
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

def transform_results(results_dict):
    new_child = []
    cutstate = results_dict['cutstate']
    solution_dict = results_dict['solution']
    for i in sorted(solution_dict.keys()):
        new_child.append(solution_dict[i])
    return cutstate, new_child

if __name__ == '__main__':

    fm_solutions = pd.DataFrame(columns = ['Cutstate'])#, 'Solution'])
    previous_solution = {}
    nodes, connections, degrees, freedoms = read_graph_data('Graph500.txt')
    # Create gls and graph object
    gls = GLS(population_size = 50)
    graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
    
    # Improve population by running the FM on each individual once
    ranked_population = {}
    improved_population = []
    for person in tqdm(gls.population, desc='Population improvement'):
        graph.init_partition(gls.transform_person(person))
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        cutstate, solution = transform_results(result)
        improved_population.append(solution)
        if cutstate in ranked_population:
            ranked_population[cutstate].append(solution)
        else:
            ranked_population[cutstate] = [solution]
    # Update the population with the improved one
    gls.population = improved_population

    # Create children
    for i in tqdm(range(2450), desc='Fiducca Mattheyses experiments'):
        # Create child
        child = gls.crossover()
        # Compute FM
        graph.init_partition(gls.transform_person(child))
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        child_cutstate, new_child = transform_results(result)
        print(f'Child cutstate {child_cutstate}')
        #Create new population
        ranked_population = gls.create_new_population(500, new_child, child_cutstate, ranked_population)
        print(f'Cutstates {sorted(ranked_population.keys())}')
        fm_solutions = fm_solutions.append({'Cutstate': sorted(ranked_population.keys())}, ignore_index=True)
    fm_solutions.to_csv('gls_with_fm.csv')
