from abc import abstractmethod
from core import Node


class Producer(Node):

    @abstractmethod
    async def produce(self):
        pass
