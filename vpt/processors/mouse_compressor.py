"""Compress mouse events."""
from typing import Union

import mouse
from rx import Observable, operators
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase


class MouseCompressor(ProcessorBase[Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]]):
    """Compresses a stream of mouse events to reduce redundancy."""
    _subj: Subject
    window_duration: float

    def __init__(self, mouse_source: SourceBase, window_duration=0.1):
        self._subj = Subject()
        self.stopped = True
        self.sources = [mouse_source]
        self.window_duration = window_duration
        self.subscriptions = None

    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        mouse_source, = self.sources

        self.subscriptions = [
            mouse_source.output
                .pipe(operators.debounce(self.window_duration))
                .subscribe(self._subj.on_next, scheduler=scheduler),
        ]

    @property
    def output(self) -> Observable:
        '''The getter for the compressed mouse events observable.'''
        return self._subj
