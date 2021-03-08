'''The base interfaces for the processor nodes.'''
from typing import TypeVar
from abc import ABC

from ..capabilities import InputCapable, OutputCapable, Initiatable

T = TypeVar('T')


class ProcessorBase(InputCapable, OutputCapable[T], Initiatable, ABC):
    '''Should be used for intermediary processing nodes.'''
