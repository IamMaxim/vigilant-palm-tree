'''The base interfaces for the source nodes.'''
from typing import TypeVar
from abc import ABC

from ..capabilities import OutputCapable, Initiatable

T = TypeVar('T')


class SourceBase(OutputCapable[T], Initiatable, ABC):
    '''Base class for data sources.
       Should be used for capturers.'''
