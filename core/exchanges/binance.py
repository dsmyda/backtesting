from asyncio.log import logger
from os import getenv
from binance import AsyncClient
from core import Producer
from core.exchanges import Exchange


class BinanceHistoricalProducer(Producer):
    """ Pulls historical Kline data from the Binance API """

    def __init__(self, config):
        super().__init__(config)

    def validate_config(self):
        if 'pair' not in self.config:
            raise Exception('Add a pair to your binance configuration. For example,\n'
                            'binance:\n'
                            '   pair: ETHUSDT')
        if 'timeframe' not in self.config:
            raise Exception('Add a timeframe to your binance configuration. For example,\n'
                            'binance:\n'
                            '   timeframe: 4h')
        if 'start' not in self.config:
            raise Exception('Add a start time to your binance configuration. For example,\n'
                            'binance:\n'
                            '   start: "2020-11-01 00:00:00"')

    async def produce(self):
        logger.debug(str(self) + ' preparing to initialize client')
        client = await AsyncClient.create(getenv('BINANCE_API_KEY'), getenv('BINANCE_API_SECRET'), tld='us')
        logger.debug(str(self) + ' finished initializing client')

        try:
            logger.debug(str(self) + ' preparing to fetch kline data')
            for kline in await client.get_historical_klines(self.config['pair'], self.config['timeframe'],
                                                            self.config['start'], limit=1000):
                logger.debug(str(self) + ' kline data received')
                kline.pop()  # Pop off legacy field, which we can ignore
                yield dict(zip(Exchange.BINANCE.value['columns'], [[float(v) if i > 0 else v] for i, v in enumerate(kline)]))

            logger.debug(str(self) + ' finished fetching kline data')
        finally:
            logger.debug(str(self) + ' preparing to close connection')
            await client.close_connection()
            logger.debug(str(self) + ' finishing closing connection')

        yield None

    def __str__(self):
        return '[' + self.__class__.__name__ + ']'


class BinanceLiveProducer(Producer):
    """ Tracks live trading data from binance """

    def __init__(self, config):
        self.config = config

    def validate_config(self):
        pass

    async def produce(self):
        pass