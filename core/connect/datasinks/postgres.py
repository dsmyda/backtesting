from os import getenv
from core.connect import SinkTask
from sqlalchemy import create_engine


class PostgresSinkTask(SinkTask):
    """ Stores any financial records in """

    WRITER_CONNECTION_STRING = getenv('POSTGRES_CONNECTION_WRITER')

    def __init__(self, connect_config):
        self.config = connect_config
        self.database = create_engine(PostgresSinkTask.WRITER_CONNECTION_STRING)

    async def push(self, data: dict):
        pass