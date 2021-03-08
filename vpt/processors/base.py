'''The base interfaces for the processor nodes.'''
from abc import ABC
from typing import TypeVar

from ..capabilities import InputCapable, OutputCapable

T = TypeVar('T')


class ProcessorBase(OutputCapable[T], InputCapable, ABC):
    '''Should be used for intermediary processing nodes.'''
