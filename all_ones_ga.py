from genetic_algorithm import GeneticAlgorithm

def main():
    ga = GeneticAlgorithm(100, 0.01, 0.95, 50)
    population = ga.init_population(50)

    ga.eval_population(population)
    generation = 1

    while not ga.is_termination_condition_met(population):
        print("Best solution " + str(population.getfittest(0)))

        # Apply croosover
        population = ga.crossover_population(population)

        # Apply mutation
        population = ga.mutate_population(population)
        # Evaluate poulation
        ga.eval_population(population)

        generation += 1

    print("Found solution in " + str(generation) + " generations")
    print("Best solution " + str(population.getfittest(0)))

if __name__ == "__main__":
    main()