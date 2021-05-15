from asyncio.log import logger

from backtesting import Backtest
import pandas as pd
from backtesting.lib import plot_heatmaps
import re
from core import Consumer
from core.strategies.factory import create


class BackTest(Consumer):

    def __init__(self, config, role):
        super().__init__(config, role)
        self.data_frame = pd.DataFrame()

    def validate_config(self):
        if 'strategy' not in self.config:
            raise Exception('Add a strategy to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   strategy: macd')

        # transform optimize statements into python code
        if 'optimize' in self.config:
            range_pattern = re.compile('\d+-\d+')

            for k, v in self.config['optimize'].items():
                if range_pattern.match(v):
                    nums = v.split('-')
                    self.config['optimize'][k] = range(int(nums[0]), int(nums[-1]))

            if 'constraint' in self.config['optimize']:
                text_expression = self.config['optimize']['constraint']


    def _add_datetime_index(self):
        datetime_series = pd.to_datetime(self.data_frame[self.data_frame.columns[0]], unit="ms")
        datetime_index = pd.DatetimeIndex(datetime_series.values)
        self.data_frame = self.data_frame.set_index(datetime_index)

    async def consume(self, data):
        if data is None:
            logger.debug(str(self) + '| poison pill detected, starting the backtest')
            self._add_datetime_index()
            bt = Backtest(self.data_frame, create(self.config['strategy']),
                          cash=self.config['cash'] if 'cash' in self.config else 10000,
                          exclusive_orders=True,
                          trade_on_close=True,
                          commission=0.01)

            if 'optimize' in self.config:
                stats, heatmap = bt.optimize(**self.config['optimize'], return_heatmap=True)
                print(stats)
                bt.plot()
                plot_heatmaps(heatmap, agg='mean')
            else:
                stats = bt.run()
                print(stats)
                bt.plot()
        else:
            logger.debug(str(self) + '| updating data frame')
            self.data_frame = self.data_frame.append(pd.DataFrame.from_dict({k: [v] for k, v in data.items()}))

    @staticmethod
    def name():
        return 'backtest'

    def __str__(self):
        return BackTest.name()
