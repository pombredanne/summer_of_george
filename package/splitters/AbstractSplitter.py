from abc import ABC, abstractmethod


class AbstractSplitter(ABC):
    @abstractmethod
    def split_document(self):
        pass
