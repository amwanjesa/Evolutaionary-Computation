import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

from genetic_algorithm import GA

def run_experiment():
    generation_fitness = pd.DataFrame()
    population_members = pd.DataFrame()
    population_division = pd.DataFrame()
    population_fitness = pd.DataFrame()
    selection_error_corect = pd.DataFrame()
    
    successful_generations = pd.DataFrame(columns=['n_generations', 'success'])
    i = 0
    tic = time.perf_counter()
    population_size = 250
    fitness_function = 'ones'
    

    ga = GA(population_size, fitness_function=fitness_function)

    while not ga.global_optimum_found() and not ga.failed_generation:
        errors, disagreements = ga.create_new_population()
        generation_fitness[f'{i+1}'] = ga.population_stats()
        population_members[f'{i+1}'] = ga.population
        i += 1
        selection_error_corect[f'{i}'] = [errors, (disagreements - errors)]

    toc = time.perf_counter()
    print(f" in {toc - tic:0.4f} seconds")

    # Proportion
    proport = generation_fitness.mean(axis = 0, skipna = True)

    #plt.plot(proport)
    #plt.xlabel('Generation')
    #plt.ylabel('Proportion of ones')
    #plt.show()

    # Selection errors
    selection_transposed = selection_error_corect.T

    plt.plot(selection_transposed[0], label = 'Errors') #errors
    plt.plot(selection_transposed[1], label = 'Correct') #correct
    plt.xlabel('Generation')
    plt.ylabel('Selection')
    plt.legend()
    plt.show()

    # Schemata 1... vs. 0...
    zeros_fitness = []
    ones_fitness = []

    for m in range(i):
        zeros = 0
        ones = 0
        for j in range(population_size):
            if population_members[f'{m+1}'][j][0] == '0':
                zeros += 1
                zeros_fitness.append(generation_fitness[f'{m+1}'][j])
            else:
                ones += 1
                ones_fitness.append(generation_fitness[f'{m+1}'][j])

        population_division[f'{m+1}'] = [zeros, ones]
        population_fitness[f'{m+1}'] = [np.mean(zeros_fitness), np.mean(ones_fitness), 
        np.std(zeros_fitness), np.std(ones_fitness)]
    
    population_transposed = population_division.T

    #plt.plot(population_transposed[0], 'bo', label = 'Zeros') #zeros
    #plt.plot(population_transposed[1], 'ro', label = 'Ones') #ones
    #plt.xlabel('Generation')
    #plt.ylabel('Members')
    #plt.legend()
    #plt.show()

    population_fitness_transposed = population_fitness.T

    #plt.errorbar((np.arange(i)+1), population_fitness_transposed[0], population_fitness_transposed[2], fmt = 'bo', label = 'Zeros')
    #plt.errorbar((np.arange(i)+1), population_fitness_transposed[1], population_fitness_transposed[3], fmt = 'ro', label = 'Ones') #ones
    #plt.xlabel('Generation')
    #plt.ylabel('Fitness')
    #plt.legend()
    #plt.show()

    #generation_fitness.to_csv(f'generation_fitness.csv')
    #population_members.to_csv(f'population_members.csv')
    #population_transposed.to_csv(f'population_division.csv')
    #population_fitness.to_csv(f'population_fitness.csv')
    #selection_errors_correct.to_csv(f'selection_errors_correct.csv')


if __name__ == "__main__":
    run_experiment()