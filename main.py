import asyncio
import logging

from core import Exchange
from core.exchanges import BinanceHistoricalProducer
from core.intermediates import PandasDataFrameNode
from core import BackTestConsumer, Pipeline

#asyncio.get_event_loop().set_debug(enabled=True)
#logging.basicConfig(level=logging.DEBUG)

config = {
    'timeframe': '1d',
    'exchange': Exchange.BINANCE,
    'pair': 'ETHUSDT',
    'start': '2020-11-01 00:00:00'
}

pipeline = Pipeline(config).chain(
    BinanceHistoricalProducer,
    PandasDataFrameNode,
    BackTestConsumer
)
pipeline.run()
