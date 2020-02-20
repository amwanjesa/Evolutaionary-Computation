import pandas as pd
import time

from genetic_algorithm import GA

if __name__ == "__main__":
    run_experiment()


def run_experiment():
    generation_fitness = pd.DataFrame()
    successful_generations = pd.DataFrame(columns=['n_generations', 'success'])

    tic = time.perf_counter()
    population_size = 130
    fitness_function = 'ones'
    for i in range(25):
        ga = GA(population_size, fitness_function=fitness_function)

        while not ga.global_optimum_found() and not ga.failed_generation:
            ga.create_new_population()

        successful_generations = successful_generations.append({'n_generations': ga.generation + 1,
                                                                'success': ga.global_optimum_found()}, ignore_index=True)
        generation_fitness[f'Run {i + 1}'] = ga.population_stats()

    toc = time.perf_counter()
    print(f" in {toc - tic:0.4f} seconds")

    generation_fitness.to_csv(
        f'generation_fitness_n_{population_size}_{fitness_function}.csv')
    successful_generations.to_csv(
        f'successful_generations_n_{population_size}_{fitness_function}.csv')
