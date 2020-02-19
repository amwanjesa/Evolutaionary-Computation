from genetic_algorithm import GA

if __name__ == "__main__":
    ga = GA(70)
    stats = {ga.generation: ga.population_stats()}

    i = 0
    iterations = 1000
    while not ga.global_optimum_found() and i < iterations:
        i += 1
        ga.create_new_population()
        stats[ga.generation] = ga.population_stats()
        #print(i)

    if i == iterations:
        print(f'No global minimum :(')
    else:
        print(f'Found global minimum!')
    print(stats)
    