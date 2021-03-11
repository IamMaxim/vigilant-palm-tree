"""Registers mouse events to a data stream."""
from typing import Union

import mouse
from rx import Observable
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.sources.base import SourceBase


class MouseSource(SourceBase[Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]]):
    """A source node for mouse events."""
    _subj: Subject

    def __init__(self):
        self._subj = Subject()
        self.stopped = True

    @property
    def output(self) -> Observable:
        '''The getter for the mouse events observable.'''
        return self._subj

    def emit_event(self, event):
        """Sends the event to the stream."""
        self._subj.on_next(event)

    def start(self):
        '''Attach an event listener.'''
        if not self.stopped:
            return
        self.stopped = False
        mouse.hook(self.emit_event)

    def stop(self):
        '''Detach the event listener.'''
        if self.stopped:
            return
        self.stopped = True
        mouse.unhook(self.emit_event)
