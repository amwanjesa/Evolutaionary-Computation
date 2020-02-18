from genetic_algorithm import GA

if __name__ == "__main__":
    ga = GA(10)
    stats = {ga.generation: ga.population_stats()}


    while not ga.global_optimum_found():
        ga.create_new_population()
        stats[ga.generation] = ga.population_stats()
    print(f'Found global minimum!')
    