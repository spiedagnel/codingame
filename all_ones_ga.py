from genetic_algorithm import GeneticAlgorithm

def main():
    ga = GeneticAlgorithm(100, 0.01, 0.95, 0)
    population = ga.init_population(50)

if __name__ == "__main__":
    main()