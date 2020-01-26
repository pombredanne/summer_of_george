import luigi
import json
import numpy as np
import os
from pathlib import Path

from package.transformers import DocumentToMatrix
from package.estimators import CorrelationEstimator
from package.splitters import SingleThresholdSplitter

class SplitTextTask(luigi.Task):

  is_complete = False
  input_directory = luigi.Parameter('input-directory')

  def requires(self):
    return None

  def run(self):
    files_to_process = [
      file
      for file in os.listdir(self.input_directory)
      if '_' not in file and file.endswith('.txt')
    ]

    for file_to_process in files_to_process:
      path = '{}/{}'.format(
        self.input_directory,
        file_to_process
      )

      stem = Path(path).stem

      document = luigi.LocalTarget(path).open('r').read()
      document_transformer = DocumentToMatrix.BasicDocumentToMatrix(document)
      estimator = CorrelationEstimator(document_transformer)
      y = np.array(estimator.evaluate()).flatten().tolist()

      splitter = SingleThresholdSplitter(y, .35)
      sections = splitter.split_document(document_transformer.lines_in_document)

      for index, section in enumerate(sections):
        output_file_path = '{}/{}_section_{}.txt'.format(self.input_directory, stem, index)
        output_target = luigi.LocalTarget(output_file_path)
        with output_target.open('w') as outfile:
          outfile.write(section)

      self.is_complete = True

  def complete(self):
    return self.is_complete

if __name__ == '__main__':
  luigi.run()
