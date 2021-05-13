import asyncio
from asyncio.log import logger
from core import Producer, Consumer


class Pipeline:

    def __init__(self):
        self.nodes = []

    def _chain(self):
        assert len(self.nodes) >= 2
        logger.debug(str(self) + ' constructing pipeline')
        edges = []
        for i in range(len(self.nodes) - 1):
            edges.append(Edge(self.nodes[i], self.nodes[i + 1]))
        logger.debug(str(self) + ' finished constructing pipeline')
        return edges

    def add(self, node):
        self.nodes.append(node)

    def run(self):
        """ Start dataflow in the pipeline and wait for it to complete """

        loop = asyncio.get_event_loop()
        logger.debug(str(self) + ' starting all edge coroutines')
        loop.run_until_complete(asyncio.gather(*[edge.open() for edge in self._chain()]))
        logger.debug(str(self) + ' all coroutines exited')

    def __str__(self):
        return '[' + self.__class__.__name__ + ']'


class Edge:

    def __init__(self, source: Producer, sink: Consumer):
        self.source: Producer = source
        self.sink: Consumer = sink

    async def open(self):
        logger.debug(str(self) + ' opened')
        async for record in self.source.produce():
            await self.sink.consume(record)
        logger.debug(str(self) + ' closed')

    def __str__(self):
        return '[' + self.__class__.__name__ + '=' \
               + self.source.__class__.__name__ + ', '\
               + self.sink.__class__.__name__ + ']'
