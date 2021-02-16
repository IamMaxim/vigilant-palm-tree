import abc
from typing import TypeVar, Generic

from rx import Observable

T = TypeVar('T')


class ModuleBase(Generic[T]):
    @abc.abstractmethod
    def get_data_stream(self) -> Observable:
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
