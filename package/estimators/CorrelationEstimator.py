import math
import numpy as np
from .AbstractEstimator import AbstractEstimator


class CorrelationEstimator(AbstractEstimator):

    def __init__(self, document_transformer):
        super().__init__(document_transformer)

    def evaluate(self):
        y = []
        document_as_matrix = self.document_transformer.transform()
        length, _ = document_as_matrix.shape
        for row in range(1, length):
            a_orig = document_as_matrix[row-1, :]
            b_orig = document_as_matrix[row, :]

            a = self._strip_array(a_orig)
            b = self._strip_array(b_orig)

            a_len = len(a)
            b_len = len(b)

            value = 0
            if a_len != 0 and b_len != 0:
                if a_len > b_len:
                    a = a[:b_len]
                if b_len > a_len:
                    b = b[:a_len]

                m = np.array([a, b])
                value = np.corrcoef(m)[0, 1]
                if math.isnan(value):
                    value = 0

            y.append([abs(value)])

        return y

    def _strip_array(self, array):
        for col in np.flip(range(len(array))):
            if array[col] != 0.0:
                break

        return array[:col]