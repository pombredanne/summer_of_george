from abc import ABC, abstractmethod


class AbstractFitness(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, individual, iterations = 1000, display_logging = False):
        pass
