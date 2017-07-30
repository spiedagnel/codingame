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

    @staticmethod
    def calc_fitness(individual):
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

    @staticmethod
    def is_termination_condition_met(population):
        for i in population.population:
            if i.fitness == 1:
                return True
        return False

    @staticmethod
    def select_parent(population):
        individuals = population.population
        population_fitness = population.fitness
        roulette_wheel_position = random.random()*population_fitness
        spin_wheel = 0
        for individual in individuals:
            spin_wheel += individual.fitness
            if spin_wheel >= roulette_wheel_position:
                return individual
        return individuals[len(population) - 1]

    def crossover_population(self, population):
        new_population = Population(len(population))
        for i in range(len(population)):
            parent1 = population.getfittest(i)
            if self.crossover_rate > random.random() and i > self.elitism_count:
                offspring = Individual(len(parent1.chromosome))
                parent2 = self.select_parent(population)
                for gene_idx in range(len(parent1.chromosome)):
                    if 0.5 > random.random():
                        offspring.chromosome[gene_idx] = parent1.chromosome[gene_idx]
                    else:
                        offspring.chromosome[gene_idx] = parent2.chromosome[gene_idx]
                new_population.population[i] = offspring
            else:
                new_population.population[i] = parent1
        return new_population

    def mutate_population(self, population):
        new_population = Population(len(population))
        for population_idx in range(len(population)):
            individual = population.getfittest(population_idx)
            for gene_idx in range(len(individual.chromosome)):
                if population_idx >= self.elitism_count:
                    if self.mutation_rate > random.random():
                        new_gene = 1
                        if individual.chromosome[gene_idx] == 1:
                            new_gene = 0
                        individual.chromosome[gene_idx] = new_gene
            new_population.population[population_idx] = individual
        return new_population


class Individual(object):

    def __init__(self, chromosome, fitness=-1):
        if isinstance(chromosome, int):
            self.chromosome = [0] * chromosome
            for i in range(chromosome):
                if 0.5 < random.random():
                    self.chromosome[i] = 1
        else:
            self.chromosome = chromosome
        self.fitness = fitness

    def __str__(self):
        return ', '.join(str(c) for c in self.chromosome)


class Population(object):

    def __init__(self, population_size, chromosome_length=None, fitness=0):
        self.population = [None] * population_size
        self.fitness = fitness
        if chromosome_length is not None:
            for i in range(len(self.population)):
                self.population[i] = Individual(chromosome_length)

    def getfittest(self, offset):
        s = sorted(self.population, key=lambda individual: individual.fitness, reverse=True)
        return s[offset]

    def __len__(self):
        return len(self.population)

    def set_individual(self, offset, individual):
        self.population[offset] = individual

    def get_individual(self, offset):
        return self.population[offset]

    def shuffle(self):
        random.shuffle(self.population)




