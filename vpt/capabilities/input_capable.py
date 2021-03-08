'''The base mixin for the input-capable nodes.'''
from abc import ABC


class InputCapable(ABC):
    '''Base class for input-capable nodes.
       Should be used for processors and sinks.'''
