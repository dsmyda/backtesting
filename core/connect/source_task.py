from abc import ABCMeta, abstractmethod


class SourceTask(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, connect_config):
        pass

    @abstractmethod
    async def poll(self):
        pass