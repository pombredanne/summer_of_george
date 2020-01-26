import re
import numpy as np


class BasicDocumentToMatrix():
  r"""
    Convert /[=:~-]/ to .95, \w\s\w to .90
  """

  document = ''
  lines_in_document = []

  def __init__(self, document: str):
    self.document = document
    self.lines_in_document = list(filter(lambda x: x != '', document.split('\n')))

  def transform(self):
    length = len(self.lines_in_document)
    width = np.max(
        [
            len(line)
            for line
            in self.lines_in_document
        ]
    )

    document_as_matrix = np.zeros((length, width))

    pipeline = [
      self._fill_in_matrix,
      self._apply_filters,
    ]

    for method in pipeline:
      document_as_matrix = method(document_as_matrix)

    return document_as_matrix

  def _fill_in_matrix(self, document_as_matrix):
    for r, line in enumerate(self.lines_in_document):
      for c, char in enumerate(line.replace(r'\s', ' ')):
        if char == ' ':
          pass
        elif re.match(r'[=:~-]', char):
          document_as_matrix[r, c] = .95
        else:
          document_as_matrix[r, c] = 1

    return document_as_matrix

  def _apply_filters(self, document_as_matrix):
    length, width = document_as_matrix.shape
    for row in range(length):
      row_values = document_as_matrix[row, :]
      for col in range(1, width-1):
        pv = row_values[col-1]
        cv = row_values[col]
        nv = row_values[col+1]

        if pv > 0 and nv > 0 and cv == 0:
          document_as_matrix[row, col] = .90

    return document_as_matrix
