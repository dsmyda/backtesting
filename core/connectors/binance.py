from os import getenv
from binance import AsyncClient

from core import Connector, DataSource, Exchange


class BinanceConnector(Connector):
    """ Pulls historical Kline data from the Binance API and feeds it into a data source """

    KLINE_COLUMNS = ["Open_Time", "Open", "High", "Low", "Close", "Volume", "Close_Time", "Quote_Asset_Volume",
                     "Number_of_Trades", "Taker_Buy_Base_Asset_Volume", "Taker_Buy_Quote_Asset_Volume"]

    API_KEY = getenv('BINANCE_API_KEY')
    API_SECRET = getenv('BINANCE_API_SECRET')

    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    async def replicate(self, pair: str, timeframe: str, start: str, end=None):
        client = await AsyncClient.create(BinanceConnector.API_KEY, BinanceConnector.API_SECRET, tld='us')
        try:
            for kline in await client.get_historical_klines(pair, timeframe, start, limit=1000):
                kline.pop()  # Pop off legacy field, which we can ignore

                self.data_source.save(
                    Exchange.BINANCE,
                    pair,
                    timeframe,
                    dict(zip(BinanceConnector.KLINE_COLUMNS, kline))
                )
        finally:
            await client.close_connection()
