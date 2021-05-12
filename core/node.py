from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, config):
        self.config = config
