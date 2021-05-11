from core.connect import SourceTask


class BinanceLiveSourceTask(SourceTask):
    """ Tracks live trading data from binance """

    def __init__(self, config):
        self.config = config

    async def poll(self):
        pass