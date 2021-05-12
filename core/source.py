from abc import abstractmethod
from core import Node


class SourceNode(Node):

    @abstractmethod
    async def produce(self):
        pass
