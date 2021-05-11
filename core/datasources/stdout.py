from core.data_source import DataSource
from core.exchange import Exchange


class StdoutDataSource(DataSource):
    """ Print to stdout for testing """

    def save(self, exchange: Exchange, pair, timeframe, data: dict):
        print('Exchange: %s, pair: %s, timeframe: %s, data: %s' % (exchange.value, pair, timeframe, data))

    def get_latest_timestamp(self, exchange: Exchange, pair, timeframe):
        pass

    def to_pd_date_frame(self, exchange: Exchange, pair, timeframe, start=None, end=None):
        pass