from abc import ABC
from typing import TypeVar, Generic


T = TypeVar('T')


# Should be used for GUI, writing to datastore, etc.
class SinkBase(Generic[T], ABC):
    pass
