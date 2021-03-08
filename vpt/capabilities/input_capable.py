'''The base mixin for the input-capable nodes.'''
from abc import ABC
from typing import List

from .output_capable import OutputCapable


class InputCapable(ABC):
    '''Base class for input-capable nodes.
       Should be used for processors and sinks.'''
    sources: List[OutputCapable]
