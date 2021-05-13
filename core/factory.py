from core import BackTest, CsvFile
from core.exchanges import BinanceHistoricalAPI, BinanceLiveAPI

node_factory = {
    BinanceHistoricalAPI.name(): BinanceHistoricalAPI,
    BinanceLiveAPI.name(): BinanceLiveAPI,
    BackTest.name(): BackTest,
    CsvFile.name(): CsvFile
}


def create(name: str):
    return node_factory[name]
