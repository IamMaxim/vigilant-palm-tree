from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from rx import Observable

T = TypeVar('T')


# Should be used for capturers
class SourceBase(Generic[T], ABC):
    @abstractmethod
    def get_data_stream(self) -> Observable:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
