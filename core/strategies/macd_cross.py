from backtesting import Strategy
from backtesting.lib import crossover
import talib


def macd(arr):
    macd, _, _ = talib.MACD(arr, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd


def macd_signal(arr):
    _, macd_signal, _ = talib.MACD(arr, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd_signal


def crossed_between(a, b, candles = 3):
    for i in range(1, candles):
        if crossover(a[:-i], b[:-i]):
            return True


class MacdCross(Strategy):
    """ Test BUY/SELL signals on MACD crossovers """

    EPSILON = 10

    def init(self):
        self.macd = self.I(macd, self.data.Close, overlay=True)
        self.macd_signal = self.I(macd_signal, self.data.Close, overlay=True)

    def next(self):
        if crossed_between(self.macd, self.macd_signal) and self.macd[-1] - self.macd_signal[-1] >= MacdCross.EPSILON:
            self.buy()
        elif crossed_between(self.macd_signal, self.macd) and self.macd_signal[-1] - self.macd[-1] >= MacdCross.EPSILON:
            self.sell()

