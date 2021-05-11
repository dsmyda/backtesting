from core.connect import SinkTask


class StdoutSinkTask(SinkTask):
    """ Print to stdout for testing """

    def __init__(self, connect_config):
        self.config = connect_config

    async def push(self, data: dict):
        print('Exchange: %s, pair: %s, timeframe: %s, data: %s' % (self.config['exchange'].value,
                                                                   self.config['pair'], self.config['timeframe'], data))


