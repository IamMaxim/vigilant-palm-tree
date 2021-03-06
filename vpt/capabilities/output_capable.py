'''The base mixin for the output-capable nodes.'''
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from rx import Observable

from .initiatable import Initiatable

T = TypeVar('T')


class OutputCapable(Generic[T], Initiatable, ABC):
    '''Base class for output-capable nodes.
       Should be used for sources and processors.'''

    @property
    @abstractmethod
    def output(self) -> Observable:
        '''The getter for the output observable.'''
