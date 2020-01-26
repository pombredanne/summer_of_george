import luigi
import json
import re
import os
from pathlib import Path

from package.ga import BinaryGeneFactory, AbstractFitness, SimpleHillClimber
from package.transformers import IntegerToBinaryString, StringToMapping, KeyArrayToRegex
from package.ga.setups import DynamicWithStaticEnding

from split_text_task import SplitTextTask


class GenerateRegexTask(luigi.Task):

  is_complete = False
  input_directory = luigi.Parameter('input_directory')

  def requires(self):
    return SplitTextTask(self.input_directory)

  def run(self):
    static_ending = r'\W([\d.]*\d[.\d]*)\W'
    consts = 'abcdefghijklmnopqrstuvwxyz'
    regexes = [
        r'\s',
        r'\d',
        r'[a-z]',
        r'[:=]',
        r'[!?.]',
        r'\W'
    ]

    complete_set = [ c for c in consts ] + regexes

    binary_start = 0
    binary_end = len(complete_set) -1 # hard end, values < binary_end

    integer_to_binary_transformer = IntegerToBinaryString(5)
    gene_factory = BinaryGeneFactory(binary_start, binary_end, 5)

    binary_to_regex = {}
    for i in range(binary_end):
        key = integer_to_binary_transformer.transform(i)
        binary_to_regex[key] = complete_set[i]

    string_mapper = StringToMapping(binary_to_regex)
    to_regex = KeyArrayToRegex(string_mapper)

    mutator = DynamicWithStaticEnding.Mutator(gene_factory)

    output = {}
    number_of_iterations = 10000

    files_to_process = [
      file
      for file in os.listdir(self.input_directory)
      if len(re.findall(r'_section_\d+\.txt', file)) > 0
    ]

    for file_to_process in files_to_process:
      path = '{}/{}'.format(
        self.input_directory,
        file_to_process
      )

      stem = Path(path).stem

      section = luigi.LocalTarget(path).open('r').read()
      output_file = luigi.LocalTarget(
        '{}/{}_regex.csv'.format(self.input_directory, stem)
      )

      output = []
      expected_numbers = list(map(lambda n: float(n), re.compile(static_ending).findall(section)))
      for expected_number in expected_numbers:
        individual = gene_factory.create_many(10)

        fitness_evaluator = DynamicWithStaticEnding.Fitness(to_regex, static_ending, expected_number, section)
        hill_climber = SimpleHillClimber(fitness_evaluator, [ mutator.gene_mutator ], [ mutator.individual_height_mutator ])

        result = hill_climber.run(individual, number_of_iterations, False)

        output.append(to_regex.transform_and_compress(result[0]) + static_ending + ',' + str(result[1]) + ',' + str(result[2]))

      with output_file.open('w') as outfile:
        outfile.write('\n'.join(output))

    self.is_complete = True

  def complete(self):
    return self.is_complete

if __name__ == '__main__':
  luigi.run()
