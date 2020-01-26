class SimpleHillClimber():
    fitness = None
    gene_mutators = []
    individual_mutators = []

    def __init__(self, fitness, gene_mutators = [], individual_mutators = []):
        self.fitness = fitness
        self.gene_mutators = gene_mutators
        self.individual_mutators = individual_mutators

    def run(self, individual, iterations = 1000, display_logging = False):
        for iteration in range(iterations):
            fitness = self.fitness.evaluate(individual)
            if (fitness >= 1):
                ## finished early,
                break

            if display_logging:
                print('iteration:', iteration, '=', fitness)

            new_individual = []
            for gene in individual:
                for gene_mutator in self.gene_mutators:
                    gene = gene_mutator(gene, display_logging)

                new_individual.append(gene)

            for individual_mutator in self.individual_mutators:
                new_individual = individual_mutator(new_individual, display_logging)

            if self.fitness.evaluate(new_individual, display_logging) > fitness:
                individual = new_individual

        return (individual, self.fitness.evaluate(individual), iteration)
