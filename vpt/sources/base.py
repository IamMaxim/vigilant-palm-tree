'''The base interfaces for the source nodes.'''
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from rx import Observable

T = TypeVar('T')


class SourceBase(Generic[T], ABC):
    '''Base class for data sources.
       Should be used for capturers.'''
    @abstractmethod
    def get_data_stream(self) -> Observable:
        '''Returns the stream of data that can be listened to.'''

    @abstractmethod
    def start(self):
        '''Starts the data stream.'''

    @abstractmethod
    def stop(self):
        '''Stops the data stream.'''
