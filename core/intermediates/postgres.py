from os import getenv
from core import IntermediateNode
from sqlalchemy import create_engine


class PostgresIntermediateNode(IntermediateNode):
    """ Stores any financial records in """

    def __init__(self, connect_config):
        self.config = connect_config
        self.database = create_engine(getenv('POSTGRES_CONNECTION_WRITER'))

    async def produce(self, data: dict):
        pass

    async def consume(self):
        pass
