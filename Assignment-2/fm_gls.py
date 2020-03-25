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

    fm_solutions = pd.DataFrame(columns = ['Cutstate', 'Solution'])
    previous_solution = {}
    nodes, connections, degrees, freedoms = read_graph_data('Graph500.txt')
    graph = Graph(nodes=nodes, connections=connections, freedoms=freedoms, degrees=degrees)
    gls = GLS(population_size = 50)
    ranked_population = {}
    for person in gls.population:
        new_person = gls.transform_person(person)
        cutstate = graph.population_cutstate(new_person)
        if cutstate in ranked_population:
            ranked_population[cutstate].append(person)
        else:
            ranked_population[cutstate] = [person]

    for i in tqdm(range(2500), desc='Fiducca Mattheyses experiments'):
        child = gls.crossover()
        graph.init_partition(gls.transform_person(child))
        graph.setup_gains()
        result = graph.fiduccia_mattheyses()
        child_cutstate, new_child = transform_results(result)
        print(f'Child: {child_cutstate}')
        cc_test = graph.population_cutstate(new_child)
        print(f'Test: {cc_test}')
        gls.create_new_population(500, new_child, child_cutstate, ranked_population)
        # Get new ranked population
        ranked_population = {}
        for person in gls.population:
            transformed_person = gls.transform_person(person)
            cutstate = graph.population_cutstate(transformed_person)
            if cutstate in ranked_population:
                ranked_population[cutstate].append(person)
            else:
                ranked_population[cutstate] = [person]

        best_cutstate = min(ranked_population.keys())
        print(f'Cutstates {sorted(ranked_population.keys())}')
        best_solution = ranked_population[best_cutstate]

        fm_solutions = fm_solutions.append({'Cutstate': best_cutstate, 'Solution': best_solution}, ignore_index=True)
        #del graph
        #if i == 50:
        #    fm_solutions.to_csv('fm_result_gls_200.csv')
    fm_solutions.to_csv('gls_with_fm.csv')
