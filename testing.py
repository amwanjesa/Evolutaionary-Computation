from genetic_algorithm import GA
import pandas as pd

if __name__ == "__main__":
    experiment_data = pd.DataFrame()
    not_found = 0
    found = 0
    gens = []
    for i in range(25):
        ga = GA(120)
        stats = {ga.generation: ga.population_stats()}

        while not ga.global_optimum_found() and ga.generation < 1000:
            ga.create_new_population()
            stats[ga.generation] = ga.population_stats()
        
        gens.append(ga.generation)

        if not ga.global_optimum_found():
            print(f'No global minimum :(')
            not_found += 1
        else:
            print(f'Found global minimum!')
            found += 1

        #print(stats[ga.generation])
        # I will fix this later
        experiment_data = experiment_data.append(stats[ga.generation])


#print(experiment_data)
print(not_found)
print(found)
print(gens)