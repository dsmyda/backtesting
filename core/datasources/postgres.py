from os import getenv
from core import DataSource
from sqlalchemy import create_engine


class PostgresDataSource(DataSource):

    WRITER_CONNECTION_STRING = getenv('POSTGRES_CONNECTION_WRITER')

    def __init__(self):
        self.database = create_engine(PostgresDataSource.WRITER_CONNECTION_STRING)

    def save(self, exchange, pair, timeframe, key_values: dict):
        pass

    def get_latest_timestamp(self, exchange, pair, timeframe):
        pass

    def to_pd_date_frame(self, exchange, pair, timeframe, start=None, end=None):
        pass