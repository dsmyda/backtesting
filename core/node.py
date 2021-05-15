from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, config, role):
        self.config = config
        self.role = role
        self.validate_config()

    @abstractmethod
    def validate_config(self):
        pass
