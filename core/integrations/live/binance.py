from core.integrations import SourceNode


class BinanceLiveSourceNode(SourceNode):
    """ Tracks live trading data from binance """

    def __init__(self, config):
        self.config = config

    async def poll(self):
        pass