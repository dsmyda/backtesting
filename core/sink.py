from abc import abstractmethod
from core import Node


class SinkNode(Node):

    @abstractmethod
    async def consume(self, data):
        pass
