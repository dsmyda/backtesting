from backtesting import Strategy
from backtesting.lib import crossover
import talib


def rsi(series, timeperiod):
    return talib.RSI(series, timeperiod=timeperiod)


class RSI(Strategy):
    """ Test BUY/SELL signals on RSI overbought, oversold """

    overbought = 70
    oversold = 30
    timeperiod = 14

    def init(self):
        self.rsi_indicator = self.I(rsi, self.data.Close, self.timeperiod)

    def next(self):
        if self.position and crossover(self.rsi_indicator, self.overbought):
            self.position.close()
        elif not self.position and crossover(self.oversold, self.rsi_indicator):
            self.buy()  # go long

