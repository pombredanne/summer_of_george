import re
import numpy as np
from ..AbstractFitness import AbstractFitness


class Fitness(AbstractFitness):
    to_regex = None
    expected_match = None
    static_ending = None
    
    def __init__(self, to_regex, static_ending, expected_match, text):
        self.to_regex = to_regex
        self.static_ending = static_ending
        self.expected_match = expected_match
        self.text = text
        
        super()

    previous_length = -1
    previous_fitness = -1
    
    def evaluate_genes(self, individual, display_logging = False):
        regex = ''
        fitness = 0
        length_of_individual = len(individual)
        reverse = np.flip(self.to_regex.transform_to_array(individual))
        for i, regex_item in enumerate(reverse):
            temp_regex = regex_item + regex
            
            ## encourage individual regex correctness,
            pattern = re.compile(temp_regex + self.static_ending, re.IGNORECASE)
            matches = pattern.findall(self.text)
            converted_matches = list(map(lambda n: float(n), matches))
            if len(matches) > 0 and self.expected_match in converted_matches:
                fitness += (( 1 - (i / length_of_individual) ) / length_of_individual)
            else:
                ## when item is wrong,
                temp_regex = '(?:.|\s)' + regex
            
            regex = temp_regex
            
        perfect_score = np.array([ 
            (( 1 - (i / length_of_individual) ) / length_of_individual)
            for i 
            in range(length_of_individual) ]
        ).sum()
        
        return fitness / perfect_score
    
    def evaluate_individual(self, individual, display_logging = False):
        regex = self.to_regex.transform(individual) + self.static_ending
        pattern = re.compile(regex, re.IGNORECASE)
        
        fitness = 0
        
        # encourage matches, but less is better.
        matches = pattern.findall(self.text)
        converted_matches = list(map(lambda n: float(n), matches))
        if len(converted_matches) > 0 and self.expected_match in converted_matches:
            ## punish if the matches arent even the expected match...
            fitness += ( 1 / len(converted_matches) )
            
        return fitness
      
    def evaluate(self, individual, display_logging = False):
        new_fitness = 0.0
        
        new_fitness += self.evaluate_genes(individual, display_logging)
        new_fitness += self.evaluate_individual(individual, display_logging)
        
        new_length = len(individual)
        previous_fitness = self.previous_fitness
        self.previous_fitness = new_fitness
        
        if previous_fitness == new_fitness:
            if self.previous_length <= new_length:
                new_fitness += 1 # encourage growth over shrinking,
        
        self.previous_length = new_length
        
        return new_fitness / 3


class Mutator():
    
    gene_factory = None
    
    def __init__(self, gene_factory):
        self.gene_factory = gene_factory

    def gene_mutator(self, gene, display_logging = False):
        precentage = np.random.rand()
        if precentage < .08:
            new_gene = self.gene_factory.create()
            gene = new_gene

        return gene

    def individual_height_mutator(self, individual, display_logging = False):
        precentage = np.random.rand()
        if precentage < .10:
            gene = self.gene_factory.create()
            individual = [gene] + individual # grow to the left,

        length = len(individual)
        if precentage > .90 and length > 0:
            individual = individual[1:] # remove from the left,

        return individual