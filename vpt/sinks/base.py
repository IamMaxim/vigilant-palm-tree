'''Base interfaces for sink nodes.'''
from abc import ABC

from ..capabilities import InputCapable


class SinkBase(InputCapable, ABC):
    '''Base class for data sinks.'''
