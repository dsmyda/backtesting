from abc import abstractmethod
from core import Node


class Consumer(Node):

    @abstractmethod
    async def consume(self, data):
        pass
