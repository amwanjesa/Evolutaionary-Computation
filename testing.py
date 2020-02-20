import pandas as pd

from genetic_algorithm import GA

if __name__ == "__main__":
    experiment_data = pd.DataFrame()
    not_found = 0
    found = 0
    gens = []
    for i in range(25):
        ga = GA(130)

        while not ga.global_optimum_found() and not ga.failed_generation:
            ga.create_new_population()

        gens.append(ga.generation + 1)

        if not ga.global_optimum_found():
            print('No global minimum :(')
            not_found += 1
        else:
            print('Found global minimum!')
            found += 1
        experiment_data[i] = ga.population_stats()

exp_data = experiment_data.T
print(experiment_data)
print(not_found)
print(found)
print(gens)
