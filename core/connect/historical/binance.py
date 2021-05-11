from os import getenv
from binance import AsyncClient
from core.connect import SourceTask


class BinanceSourceTask(SourceTask):
    """ Pulls historical Kline data from the Binance API and feeds it into a data source """

    KLINE_COLUMNS = ["Open_Time", "Open", "High", "Low", "Close", "Volume", "Close_Time", "Quote_Asset_Volume",
                     "Number_of_Trades", "Taker_Buy_Base_Asset_Volume", "Taker_Buy_Quote_Asset_Volume"]

    def __init__(self, connect_config):
        self.config = connect_config

    async def poll(self):
        client = await AsyncClient.create(getenv('BINANCE_API_KEY'), getenv('BINANCE_API_SECRET'), tld='us')
        try:
            for kline in await client.get_historical_klines(self.config['pair'], self.config['timeframe'],
                                                            self.config['start'], limit=1000):
                kline.pop()  # Pop off legacy field, which we can ignore

                yield dict(zip(BinanceSourceTask.KLINE_COLUMNS, kline))
        finally:
            await client.close_connection()
