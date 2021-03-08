'''The base mixin for the nodes that can be started and stopped.'''
from abc import ABC, abstractmethod


class Initiatable(ABC):
    '''Base class for nodes that can be started and stopped.
       Should be used for sources and processors.'''

    @abstractmethod
    def start(self):
        '''Start the node's data stream.'''

    @abstractmethod
    def stop(self):
        '''Start the node's data stream.'''
