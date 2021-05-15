import asyncio
from asyncio.log import logger

from core import Producer, Consumer
import csv
from os import path
from datetime import datetime


def cast(datatype: str, value):
    if datatype == 'number':
        return float(value)
    elif datatype == 'dateiso':
        return float(datetime.fromisoformat(value).timestamp() * 1000)  #convert to epoch ms for downstream consumers
    else:
        return value


class CsvFile(Producer, Consumer):

    def __init__(self, config, role):
        super().__init__(config, role)

        if role == 'SINK' or role == 'INTERMEDIATE':
            self.csvfile = open(self.config['path'], 'w')
            self.queue = asyncio.Queue()
            self.writer = None

    def validate_config(self):
        if 'path' not in self.config:
            raise Exception('Add a path to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   path: C:/Users/Danny/csv/btcusd.csv')
        if not path.exists(self.config['path']) and self.role == 'SOURCE':
            raise Exception('The file in your ' + str(self) + ' configuration does not exist (' + self.config['path'] + ')\n'
                            'Did you typo?')
        if 'schema' not in self.config and self.role == 'SOURCE':
            raise Exception('Add a schema to your ' + str(self) + ' configuration. For example,\n'
                            + str(self) + ':\n'
                            '   schema:\n'
                            '       Date: datetime - ISO\n'
                            '       Open: number\n'
                            '       etc...')

    async def produce(self):
        if self.role == 'INTERMEDIATE':
            value = True
            while value:
                value = await self.queue.get()
                yield value
        elif self.role == 'SINK':
            pass
        else:  # Must be a source
            with open(self.config['path']) as csvfile:
                logger.debug(str(self) + '| opened csv file')
                reader = csv.DictReader(csvfile, delimiter=',')
                logger.debug(str(self) + '| preparing to read csv file')
                for row in reader:
                    yield {k: cast(self.config['schema'][k], val) for k, val in row.items()}
                logger.debug(str(self) + '| finished reading csv file')

            yield None

    async def consume(self, data):
        if data is None:
            self.csvfile.close()
            await self.queue.put(None)
        else:
            if not self.writer:
                self.writer = csv.DictWriter(self.csvfile, delimiter=',', fieldnames=data.keys())
                self.writer.writeheader()

            self.writer.writerow(data)

            if self.role == 'INTERMEDIATE':
                # Optimization, don't stream from file just write directly
                await self.queue.put(data)


    @staticmethod
    def name():
        return 'csvfile'

    def __str__(self):
        return CsvFile.name()
