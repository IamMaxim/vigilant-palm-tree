'''The base mixin for the input-capable nodes.'''
from abc import ABC
from typing import List

from rx.scheduler.mainloop import QtScheduler

from .output_capable import OutputCapable, Initiatable


class InputCapable(Initiatable, ABC):
    '''Base class for input-capable nodes.
       Should be used for processors and sinks.'''
    sources: List[OutputCapable]

    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        self.stopped = False
        for source in self.sources:
            source.start(scheduler)

    def stop(self):
        if self.stopped:
            return
        self.stopped = True
        for source in self.sources:
            source.stop()
