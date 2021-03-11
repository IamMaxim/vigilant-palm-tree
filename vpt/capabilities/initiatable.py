'''The base mixin for the nodes that can be started and stopped.'''
from abc import ABC, abstractmethod

from rx.scheduler.mainloop import QtScheduler


class Initiatable(ABC):
    '''Base class for nodes that can be started and stopped.
       Should be used for sources and processors.'''
    stopped: bool

    @abstractmethod
    def start(self, scheduler: QtScheduler):
        '''Start the node's data stream.'''

    @abstractmethod
    def stop(self):
        '''Start the node's data stream.'''
