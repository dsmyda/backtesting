import asyncio
from abc import ABC

from core import SourceNode, SinkNode
from asyncio import Event


class IntermediateNode(ABC, SourceNode, SinkNode):

    def __init__(self, config):
        super().__init__(config)
        self.event = Event()
