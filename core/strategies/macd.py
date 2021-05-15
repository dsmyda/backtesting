from backtesting import Strategy
from backtesting.lib import crossover
import talib


def macd(arr):
    macd, _, _ = talib.MACD(arr, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd


def macd_signal(arr):
    _, macd_signal, _ = talib.MACD(arr, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd_signal


class MACD(Strategy):
    """ Test BUY/SELL signals on MACD crossovers """

    def init(self):
        self.macd = self.I(macd, self.data.Close, overlay=True)
        self.macd_signal = self.I(macd_signal, self.data.Close, overlay=True)

    def next(self):
        if self.position and crossover(self.macd_signal, self.macd):
            self.position.close()  # exit the position
        elif not self.position and crossover(self.macd, self.macd_signal):
            self.buy()  # go long

