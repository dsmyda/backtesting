from asyncio.log import logger

from backtesting import Backtest
from core.strategies import SmaCross

from core import SinkNode


class BackTestSinkNode(SinkNode):
    def __init__(self, config):
        self.config = config

    async def consume(self, data):
        logger.debug(str(self) + ' data frame received')
        bt = Backtest(data, SmaCross, exclusive_orders=True)
        stats = bt.run()
        logger.debug(str(self) + ' backtesting completed')
        print(stats)

    def __str__(self):
        return '[' + self.__class__.__name__ + ']'
