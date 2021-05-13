from core import BackTestConsumer, CsvFile
from core.exchanges import BinanceHistoricalProducer

node_factory = {
    'binance': BinanceHistoricalProducer,
    'backtest': BackTestConsumer,
    'csvfile': CsvFile
}


def create(name: str):
    return node_factory[name]
