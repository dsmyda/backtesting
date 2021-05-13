from asyncio.log import logger

from core import Producer
import csv
from os import path
from datetime import datetime


def cast(datatype: str, value):
    if datatype == 'number':
        return float(value)
    elif datatype == 'dateiso':
        return datetime.fromisoformat(value).timestamp() * 1000  #convert to epoch ms for downstream consumers
    else:
        return value


class CsvFile(Producer):

    def __init__(self, config):
        super().__init__(config)

    def validate_config(self):
        if 'path' not in self.config:
            raise Exception('Add a path to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   path: C:/Users/Danny/csv/btcusd.csv')
        if not path.exists(self.config['path']):
            raise Exception('The file in your ' + str(self) + ' configuration does not exist.\n'
                            'Did you typo?')
        if 'schema' not in self.config:
            raise Exception('Add a schema to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   schema:\n'
                            '       Date: datetime - ISO\n'
                            '       Open: number\n'
                            '       etc...')

    async def produce(self):
        with open(self.config['path']) as csvfile:
            logger.debug(str(self) + '| opened csv file')
            reader = csv.DictReader(csvfile, delimiter=',')
            logger.debug(str(self) + '| preparing to read csv file')
            for row in reader:
                yield {k: [cast(self.config['schema'][k], val)] for k, val in row.items()}
            logger.debug(str(self) + '| finished reading csv file')

        yield None

    @staticmethod
    def name():
        return 'csvfile'

    def __str__(self):
        return CsvFile.name()
