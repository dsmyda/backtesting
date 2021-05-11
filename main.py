import asyncio

from core import Exchange
from core.connect import Connector
from core.connect.historical import BinanceSourceTask
from core.connect.datasinks import StdoutSinkTask

config = {
    'timeframe': '4h',
    'exchange': Exchange.BINANCE,
    'pair': 'ETHBTC',
    'start': '2021-01-01 00:00:00',
    'sql': {
        # TODO, implement this for postgres
        'table': 'exchanges.historical.binance.4h.ethbtc',
        'ddl': ''
    }
}
binance_source = BinanceSourceTask(config)
stdout_sink = StdoutSinkTask(config)
binance_connector = Connector(binance_source, stdout_sink)

loop = asyncio.get_event_loop()
loop.run_until_complete(binance_connector.open())