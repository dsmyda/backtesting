import asyncio
import logging

from core.factory import create
from core import Pipeline

import yaml
import sys

#asyncio.get_event_loop().set_debug(enabled=True)
#logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) < 2: # the first arg is the script name
    print('Please specify the path to your pipeline configuration file.\n'
          'For example: $ python runner.py C:/home/pipelines/google_pipeline.yaml\n'
          'The path can be either relative or absolute.')
else:
    pipeline_config_path = sys.argv[1]

    with open(pipeline_config_path) as file:
        configuration = yaml.load(file, Loader=yaml.FullLoader)

        pipeline = Pipeline()
        for name, config in configuration['pipeline'].items():
            pipeline.add(create(name)(config))

    pipeline.run()
