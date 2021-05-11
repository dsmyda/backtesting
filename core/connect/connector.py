from core.connect import SourceTask, SinkTask


class Connector:

    def __init__(self, source: SourceTask, sink: SinkTask):
        self.source = source
        self.sink = sink

    async def open(self):
        # TODO - parallelize this
        async for record in self.source.poll():
            await self.sink.push(record)
