import abc
from typing import TypeVar, Generic

from rx import Observable

T = TypeVar('T')


# Should be used for GUI, writing to datastore, etc.
class SinkBase(Generic[T]):
    pass


# Should be used for intermediary processing nodes
class ProcessorBase(SinkBase[T]):
    def get_data_stream(self) -> Observable:
        raise NotImplementedError


# Should be used for capturers
class SourceBase(ProcessorBase[T]):
    def get_data_stream(self) -> Observable:
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
