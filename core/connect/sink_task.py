from abc import ABCMeta, abstractmethod


class SinkTask(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, connect_config):
        pass

    @abstractmethod
    async def push(self, data: dict):
        pass