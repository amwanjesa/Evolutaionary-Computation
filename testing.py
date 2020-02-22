import pandas as pd
import time
import numpy as np

from genetic_algorithm import GA

def run_experiment():
    generation_fitness = pd.DataFrame()
    successful_generations = pd.DataFrame(columns=['n_generations', 'success'])
    time_per_run = []
    tic = time.perf_counter()
    population_size = 250
    fitness_function = 'ones'
    for i in range(25):
        tic_per_run = time.perf_counter()
        ga = GA(population_size, fitness_function=fitness_function)

        while not ga.global_optimum_found() and not ga.failed_generation:
            ga.create_new_population()

        successful_generations = successful_generations.append({'n_generations': ga.generation + 1,
                                                                'success': ga.global_optimum_found()}, ignore_index=True)
        generation_fitness[f'Run {i + 1}'] = ga.population_stats()
        toc_per_run = time.perf_counter()
        time_per_run.append(toc_per_run - tic_per_run)

    toc = time.perf_counter()
    print(f" in {toc - tic:0.4f} seconds")
    #print(successful_generations.success.value_counts())

    #generation_fitness.to_csv(
    #    f'generation_fitness_n_{population_size}_{fitness_function}.csv')
    #successful_generations.to_csv(
    #    f'successful_generations_n_{population_size}_{fitness_function}.csv')

    # table stats
    average_generations = successful_generations.mean(axis = 0, skipna = True)[0]
    sd_generations = successful_generations.std(axis = 0, skipna = True)[0]
    row_average_fitness = generation_fitness.mean(axis = 1, skipna = True)
    row_sd_fitness = generation_fitness.std(axis = 1, skipna = True)
    average_fitness = row_average_fitness.mean(axis = 0, skipna = True)
    sd_fitness = row_sd_fitness.std(axis = 0, skipna = True)
    cpu_time = toc-tic
    average_cpu_time = np.mean(time_per_run)
    sd_cpu_time = np.std(time_per_run)

    table_data = pd.DataFrame({'Population size': [population_size], 
        'Average generations': [average_generations],
        'SD generations': [sd_generations], 
        'Average fitness': [average_fitness], 'SD fitness': [sd_fitness],
        'CPU time': [cpu_time], 'Average CPU time': [average_cpu_time], 
        'SD CPU time': [sd_cpu_time]})

    table_data.to_csv(
       f'table_data_{population_size}_{fitness_function}_singletrial.csv')

if __name__ == "__main__":
    run_experiment()