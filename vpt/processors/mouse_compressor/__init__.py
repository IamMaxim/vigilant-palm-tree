"""Compress mouse events."""
from typing import Union

import mouse
from rx import Observable
from rx import operators
from rx.subject import Subject

from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase


class MouseCompressor(ProcessorBase[Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]]):
    """Compresses a stream of mouse events to reduce redundancy."""
    _subj: Subject

    def __init__(self, mouse_source: SourceBase, window_duration=0.016):
        self._subj = Subject()
        self.stopped = True
        self.sources = [mouse_source]
        mouse_source \
            .output \
            .pipe(operators.throttle_first(window_duration)) \
            .subscribe(self._subj.on_next)

    @property
    def output(self) -> Observable:
        '''The getter for the compressed mouse events observable.'''
        return self._subj
