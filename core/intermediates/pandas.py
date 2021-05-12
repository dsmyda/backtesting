import asyncio
from asyncio.log import logger

import pandas as pd
from core import Producer, Consumer


def _add_datetime_index(data_frame):
    datetime_series = pd.to_datetime(data_frame['Open_Time'], unit="ms")
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    return data_frame.set_index(datetime_index)


class PandasDataFrameNode(Producer, Consumer):
    def __init__(self, config):
        super().__init__(config)
        self.latest = pd.DataFrame()
        self.event = asyncio.Event()

    async def produce(self):
        logger.debug(str(self) + ' waiting for data frame')
        await self.event.wait()
        logger.debug(str(self) + ' finished waiting, data frame received')

        self.latest = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _add_datetime_index(self.latest))

        yield self.latest

    async def consume(self, data):
        if data is None:
            logger.debug(str(self) + ' poison pill detected, notifying the produce API')
            self.event.set()
        else:
            logger.debug(str(self) + ' updating data frame')
            self.latest = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.latest.append(pd.DataFrame.from_dict(data)))

    def __str__(self):
        return '[' + self.__class__.__name__ + ']'
