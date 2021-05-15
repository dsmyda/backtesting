from asyncio.log import logger
from os import getenv
from binance import AsyncClient, BinanceSocketManager
from core import Producer
from core.exchanges import Exchange


class BinanceHistoricalAPI(Producer):
    """ Pulls historical Kline data from the Binance API """

    def __init__(self, config, role):
        super().__init__(config, role)

    def validate_config(self):
        if 'pair' not in self.config:
            raise Exception('Add a pair to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   pair: ETHUSDT')
        if 'timeframe' not in self.config:
            raise Exception('Add a timeframe to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   timeframe: 4h')
        if 'start' not in self.config:
            raise Exception('Add a start time to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   start: "2020-11-01 00:00:00"')

    async def produce(self):
        logger.debug(str(self) + '| preparing to initialize client')
        client = await AsyncClient.create(getenv('BINANCE_API_KEY'), getenv('BINANCE_API_SECRET'), tld='us')
        logger.debug(str(self) + '| finished initializing client')

        try:
            logger.debug(str(self) + '| preparing to fetch kline data')
            for kline in await client.get_historical_klines(self.config['pair'], self.config['timeframe'],
                                                            self.config['start'], limit=1000):
                logger.debug(str(self) + '| kline data received')
                kline.pop()  # Pop off legacy field, which we can ignore
                yield dict(zip(Exchange.BINANCE.value['columns'], [float(v) if i > 0 else v for i, v in enumerate(kline)]))

            logger.debug(str(self) + '| finished fetching kline data')
        finally:
            logger.debug(str(self) + '| preparing to close connection')
            await client.close_connection()
            logger.debug(str(self) + '| finishing closing connection')

        yield None

    @staticmethod
    def name():
        return 'binance'

    def __str__(self):
        return BinanceHistoricalAPI.name()


def cast(datatype, value):
    if datatype == 'number':
        return float(value)


class BinanceLiveAPI(Producer):
    """ Tracks live trading data from binance """

    columns = {
        't': 'Open_Time',
        'T': 'Close_Time',
        'o': 'Open',
        'c': 'Close',
        'h': 'High',
        'l': 'Low',
        'v': 'Volume',
        'n': 'Number_of_Trades',
        'x': 'Is_Closed',
        'q': 'Quote_Asset_Volume',
        'V': 'Taker_Buy_Base_Asset_Volume',
        'Q': 'Taker_Buy_Quote_Asset_Volume'
    }

    datatypes = {
        'o': 'number',
        'c': 'number',
        'h': 'number',
        'l': 'number',
        'v': 'number',
        'a': 'number',
        'V': 'number',
        'Q': 'number'
    }

    def __init__(self, config, role):
        super().__init__(config, role)

    def validate_config(self):
        if 'pair' not in self.config:
            raise Exception('Add a pair to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   pair: ETHUSDT')
        if 'timeframe' not in self.config:
            raise Exception('Add a timeframe to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   timeframe: 4h')

    async def produce(self):
        logger.debug(str(self) + '| preparing to initialize client and socket manager')
        client = await AsyncClient.create(getenv('BINANCE_API_KEY'), getenv('BINANCE_API_SECRET'), tld='us')
        socket_manager = BinanceSocketManager(client)
        logger.debug(str(self) + '| finished initializing client and socket manager')

        try:
            logger.debug(str(self) + '| preparing to open kline socket')
            kline_socket = socket_manager.kline_socket(self.config['pair'], interval=self.config['timeframe'])
            async with kline_socket:
                while True:
                    logger.debug(str(self) + '| kline data received')
                    event = await kline_socket.recv()
                    data = {}
                    for k, v in event['k'].items():
                        if k in BinanceLiveAPI.columns:
                            data[BinanceLiveAPI.columns[k]] = v if k not in BinanceLiveAPI.datatypes else cast(BinanceLiveAPI.datatypes[k], v)
                    yield data
        finally:
            logger.debug(str(self) + '| preparing to close connection')
            await client.close_connection()
            logger.debug(str(self) + '| finishing closing connection')

    @staticmethod
    def name():
        return 'binancelive'

    def __str__(self):
        return BinanceLiveAPI.name()
