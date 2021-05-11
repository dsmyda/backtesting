import os
from core.data_source import DataSource
from sqlalchemy import create_engine


class PostgresDataSource(DataSource):

    READER_CONNECTION = os.getenv('POSTGRES_CONNECTION_READER')
    WRITER_CONNECTION = os.getenv('POSTGRES_CONNECTION_WRITER')

    def __init__(self):
        self.pool = None

    def add(self, json: str):
        pass

    def get_latest_timestamp(self, exchange, pair, timeframe):
        pass

    def to_pd_date_frame(self, exchange, pair, timeframe, start=None, end=None):
        pass