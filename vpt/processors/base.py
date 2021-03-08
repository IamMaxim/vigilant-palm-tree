'''The base interfaces for the processor nodes.'''
from abc import ABC
from typing import TypeVar, List

from ..capabilities import InputCapable, OutputCapable

T = TypeVar('T')


class ProcessorBase(OutputCapable[T], InputCapable, ABC):
    '''Should be used for intermediary processing nodes.'''
    sources: List[OutputCapable]

    def start(self):
        if not self.stopped:
            return
        self.stopped = False
        for source in self.sources:
            source.start()

    def stop(self):
        if self.stopped:
            return
        self.stopped = True
        for source in self.sources:
            source.stop()
