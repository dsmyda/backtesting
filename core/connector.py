from abc import ABCMeta, abstractmethod

from core.data_source import DataSource


class Connector(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, data_source: DataSource):
        pass

    @abstractmethod
    async def replicate(self, pair, timeframe, start=None, end=None):
        pass
