import asyncio
import logging

from core.factory import create
from core import Pipeline

import yaml

#asyncio.get_event_loop().set_debug(enabled=True)
#logging.basicConfig(level=logging.DEBUG)

with open("pipeline.yaml") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)

    pipeline = Pipeline()
    for name, config in configuration['pipeline'].items():
        pipeline.add(create(name)(config))

pipeline.run()
