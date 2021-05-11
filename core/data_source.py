from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    def add(self, json: str):
        pass

    @abstractmethod
    def get_latest_timestamp(self, exchange, pair, timeframe):
        pass

    @abstractmethod
    def to_pd_date_frame(self, exchange, pair, timeframe, start=None, end=None):
        pass