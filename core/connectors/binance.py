import os

from binance.client import Client
from ..connector import Connector
from ..data_source import DataSource


class BinanceConnector(Connector):
    genesis_trade = ""

    API_KEY = os.getenv('BINANCE_API_KEY')
    API_SECRET = os.getenv('BINANCE_API_SECRET')

    def __init__(self, data_source: DataSource):
        self.client = Client(BinanceConnector.API_KEY, BinanceConnector.API_SECRET)
        self.data_source = data_source

    async def replicate(self, exchange, pair, timeframe, start=None, end=None):
        pass