import asyncio
import logging

from core import Exchange
from core.integrations.historical import BinanceHistoricalSourceNode
from core.intermediates import PdDataFrameIntermediateNode
from core import BackTestSinkNode, Pipeline

asyncio.get_event_loop().set_debug(enabled=True)
logging.basicConfig(level=logging.DEBUG)

config = {
    'timeframe': '4h',
    'exchange': Exchange.BINANCE,
    'pair': 'ETHBTC',
    'start': '2021-05-01 00:00:00',
    'sql': {
        # TODO, implement this for postgres
        'table': 'exchanges.historical.binance.4h.ethbtc',
        'ddl': ''
    }
}

Pipeline(
    config,
    BinanceHistoricalSourceNode,
    PdDataFrameIntermediateNode,
    BackTestSinkNode
).run()
