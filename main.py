import asyncio
import logging

from core.exchanges import BinanceHistoricalProducer, Exchange
from core.strategies import MacdCross
from core.intermediates import PandasDataFrameNode
from core import BackTestConsumer, Pipeline

#asyncio.get_event_loop().set_debug(enabled=True)
#logging.basicConfig(level=logging.DEBUG)

config = {
    'timeframe': '1d',
    'exchange': Exchange.BINANCE,
    'pair': 'ETHUSDT',
    'start': '2020-11-01 00:00:00',
    'strategy': MacdCross,
    'persist': True  # Todo - write any data frames to SQL as part of the pipeline process
}

pipeline = Pipeline(config).chain(
    BinanceHistoricalProducer,
    PandasDataFrameNode,
    BackTestConsumer
)
pipeline.run()
