from abc import ABC, abstractmethod


class AbstractEstimator(ABC):
    document_transformer = None

    def __init__(self, document_transformer):
        assert document_transformer is not None
        self.document_transformer = document_transformer

    @abstractmethod
    def evaluate(self):
        pass
