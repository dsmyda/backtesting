from abc import ABC, abstractmethod
from core.exchange import Exchange


class DataSource(ABC):

    @abstractmethod
    def save(self, exchange: Exchange, pair, timeframe, key_values: dict):
        pass

    @abstractmethod
    def get_latest_timestamp(self, exchange: Exchange, pair, timeframe):
        pass

    @abstractmethod
    def to_pd_date_frame(self, exchange: Exchange, pair, timeframe, start=None, end=None):
        pass