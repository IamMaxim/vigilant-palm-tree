'''The base interfaces for the processor nodes.'''
from typing import TypeVar
from abc import abstractmethod, ABC

from rx import Observable

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase

T = TypeVar('T')


class ProcessorBase(SinkBase[T], SourceBase[T], ABC):
    '''Should be used for intermediary processing nodes'''
    @abstractmethod
    def get_data_stream(self) -> Observable:
        pass
