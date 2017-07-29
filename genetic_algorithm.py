import random

class GeneticAlgorithm(object):

    def __init__(self, population_size, mutation_rate, crossover_rate, elitism_count):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count

    def init_population(self, chromosome_length):
        p = Population(self.population_size, chromosome_length)
        return p

    def calc_fitness(self, individual):
        correct_genes = 0
        for i in range(len(individual.chromosome)):
            if individual.chromosome[i] == 1:
                correct_genes += 1
        fitness = correct_genes / len(individual.chromosome)
        individual.fitness = fitness
        return fitness

    def eval_population(self, population):
        population_fitness = 0

        for individual in population.population:
            population_fitness += self.calc_fitness(individual)
        population.fitness = population_fitness


class Individual(object):

    def __init__(self, chromosome, fitness=-1):
        if chromosome is int:
            self.chromosome = [0] * chromosome
            for i in range(chromosome):
                if 0.5 < random.random():
                    self.chromosome[i] = 1
        else:
            self.chromosome = chromosome
        self.fitness = fitness

    @property
    def __str__(self):
        return ", ".join(self.chromosome)


class Population(object):

    def __init__(self, population_size, chromosome_length=None, fitness=0):
        self.population = [None] * population_size
        self.fitness = fitness
        if chromosome_length is not None:
            for i in range(len(self.population)):
                self.population[i] = Individual(chromosome_length)

    def getfittest(self, offset):
        s = sorted(self.population, key=lambda individual: individual.fitness)
        return s[offset]

    def __len__(self):
        return len(self.population)

    def set_individual(self, offset, individual):
        self.population[offset] = individual

    def get_individual(self, offset):
        return self.population[offset]

    def shuffle(self):
        random.shuffle(self.population)




