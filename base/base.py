from abc import ABCMeta, abstractmethod


class BaseFetcher(metaclass=ABCMeta):
    @abstractmethod
    def fetch_data(self):
        pass
