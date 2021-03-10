'''The base mixin for the input-capable nodes.'''
from abc import ABC
from typing import List

from rx.scheduler.mainloop import QtScheduler
from rx.core.typing import Disposable

from .output_capable import OutputCapable, Initiatable


class InputCapable(Initiatable, ABC):
    '''Base class for input-capable nodes.
       Should be used for processors and sinks.'''
    sources: List[OutputCapable]
    subscriptions: List[Disposable]

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
        if self.subscriptions is not None:
            for subcription in self.subscriptions:
                subcription.dispose()
