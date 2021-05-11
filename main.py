import asyncio

from binance import AsyncClient

from core.connectors import BinanceConnector
from core.datasources import StdoutDataSource

stdout_sink = StdoutDataSource()
loop = asyncio.get_event_loop()
binance_connector = BinanceConnector(stdout_sink)
loop.run_until_complete(binance_connector.replicate("ETHBTC", AsyncClient.KLINE_INTERVAL_4HOUR, start="2021-01-01 00:00:00"))