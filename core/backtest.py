from asyncio.log import logger

from backtesting import Backtest
from core.strategies import MacdCross

from core import Consumer


class BackTestConsumer(Consumer):
    def __init__(self, config):
        self.config = config

    async def consume(self, data):
        logger.debug(str(self) + ' historical data frame received')
        bt = Backtest(data, MacdCross,
                      exclusive_orders=True,
                      trade_on_close=True,
                      commission=self.config['exchange'].value['commission'])
        bt.run()
        bt.plot()

    def __str__(self):
        return '[' + self.__class__.__name__ + ']'
