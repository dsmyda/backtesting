from core import Producer, Consumer


class Postgres(Producer, Consumer):
    def __init__(self, config):
        pass

    def validate_config(self):
        pass

    async def produce(self):
        pass

    async def consume(self, data):
        pass
