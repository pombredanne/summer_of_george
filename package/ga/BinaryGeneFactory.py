import numpy as np
from ..transformers.IntegerToBinaryString import IntegerToBinaryString


class BinaryGeneFactory():

    transformer = None
    binary_start = -1
    binary_end = -1

    def __init__(self, binary_start, binary_end, max_binary_length):
        self.binary_start = binary_start
        self.binary_end = binary_end
        self.transformer = IntegerToBinaryString(max_binary_length)

    def create(self):
        random_integer = np.random.randint(self.binary_start, self.binary_end)
        return self.transformer.transform(random_integer)

    def create_many(self, total):
        return [ self.create() for _ in range(total) ]
