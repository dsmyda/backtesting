from asyncio.log import logger

from backtesting import Backtest
import pandas as pd

from core import Consumer
from core.strategies.factory import create


class BackTest(Consumer):

    def __init__(self, config):
        self.config = config
        self.data_frame = pd.DataFrame()

    def validate_config(self):
        if 'strategy' not in self.config:
            raise Exception('Add a strategy to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   strategy: macdcross')

    def _add_datetime_index(self):
        datetime_series = pd.to_datetime(self.data_frame[self.data_frame.columns[0]], unit="ms")
        datetime_index = pd.DatetimeIndex(datetime_series.values)
        self.data_frame = self.data_frame.set_index(datetime_index)

    async def consume(self, data):
        if data is None:
            logger.debug(str(self) + '| poison pill detected, starting the backtest')
            self._add_datetime_index()
            bt = Backtest(self.data_frame, create(self.config['strategy']),
                          exclusive_orders=True,
                          trade_on_close=True,
                          commission=0.01)
            print(bt.run())
            bt.plot()
        else:
            logger.debug(str(self) + '| updating data frame')
            self.data_frame = self.data_frame.append(pd.DataFrame.from_dict(data))

    @staticmethod
    def name():
        return 'backtest'

    def __str__(self):
        return BackTest.name()
