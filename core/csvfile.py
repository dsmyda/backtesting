from core import Producer
import csv
from os import path
from datetime import datetime


def cast(datatype: str, value):
    if datatype == 'number':
        return float(value)
    elif datatype == 'dateiso':
        return datetime.fromisoformat(value).timestamp() * 1000  #convert to epoch ms for downstream consumers


class CsvFile(Producer):

    def __init__(self, config):
        super().__init__(config)

    def validate_config(self):
        if 'path' not in self.config:
            raise Exception('Add a path to your cvsfile configuration. For example,\n'
                            'csvfile:\n'
                            '   path: C:/Users/Danny/csv/btcusd.csv')
        if not path.exists(self.config['path']):
            raise Exception('The file in your csvfile configuration does not exist.\n'
                            'Did you typo?')
        if 'schema' not in self.config:
            raise Exception('Add a schema to your cvsfile configuration. For example,\n'
                            'csvfile:\n'
                            '   schema:\n'
                            '       Date: datetime - ISO\n'
                            '       Open: number\n'
                            '       etc...')

    async def produce(self):
        with open(self.config['path']) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                yield {k: [cast(self.config['schema'][k], val)] for k, val in row.items()}

        yield None
