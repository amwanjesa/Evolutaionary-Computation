import numpy as np
import random
from os.path import join
from time import perf_counter

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
                node, degree, neighbours = int(l[0]), int(l[2]), [
                    int(x) for x in l[3:]]
                connections[node] = neighbours
                freedoms[node] = True
                nodes.append(node)
                degrees[node] = degree

    return nodes, connections, degrees, freedoms


def mutation(solution, perturbation=0.01):
    def mutate(current_solution, perturbation):
        new_solution = {}
        for node, block in current_solution.items():
            if random.random() <= perturbation:
                if block == 1:
                    new_solution[node] = 0
                else:
                    new_solution[node] = 1
            else:
                new_solution[node] = block
        return new_solution

    new_solution = mutate(solution, perturbation)
    new_solution = {i + 1: i for i in GLS.check_equality(500,
                                          list(range(500)), list(new_solution.values()))}
    return new_solution


def transform_results(results_dict):
    new_child = []
    cutstate = results_dict['cutstate']
    solution_dict = results_dict['solution']
    for i in sorted(solution_dict.keys()):
        new_child.append(solution_dict[i])
    return cutstate, new_child


if __name__ == '__main__':

    nodes, connections, degrees, freedoms = read_graph_data('Graph500.txt')
    data_storage = join('data', 'gls')
    performance_stats = pd.DataFrame()
    solutions = pd.DataFrame(columns=['Cutstate'])

    for j in range(25):
        tic = perf_counter()
        best_solution = {}
        # Create gls and graph object
        gls = GLS(population_size=50)
        graph = Graph(nodes=nodes, connections=connections,
                      freedoms=freedoms, degrees=degrees)

        # Improve population by running the FM on each individual once
        ranked_population = {}
        improved_population = []
        for individual in tqdm(gls.population, desc='Population improvement'):
            graph.init_partition(gls.transform_person(individual))
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

            # Mutate child
            child = mutation(gls.transform_person(child))

            # Compute FM
            graph.init_partition(child)
            graph.setup_gains()
            result = graph.fiduccia_mattheyses()
            child_cutstate, new_child = transform_results(result)
            # Create new population
            ranked_population = gls.create_new_population(
                500, new_child, child_cutstate, ranked_population)
        solutions = solutions.append(
            {'Cutstate': sorted(ranked_population.keys())}, ignore_index=True)
        toc = perf_counter()
        performance_stats = performance_stats.append(
            {'Execution Time': toc - tic}, ignore_index=True)

        # Delete gls and graph
        del gls
        del graph

    solutions.to_csv(join(data_storage, f'gls_with_fm.csv'))
    performance_stats.to_csv(
        join(data_storage, f'gls_with_fm_performance.csv'))
