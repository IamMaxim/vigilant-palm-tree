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

    def callback(self, event):
        """Sends the event to the stream."""
        self._subj.on_next(event)

    def start(self, _scheduler: QtScheduler):
        '''Attach an event listener.'''
        if not self.stopped:
            return
        self.stopped = False
        mouse.hook(self.callback)

    def stop(self):
        '''Detach the event listener.'''
        if self.stopped:
            return
        self.stopped = True
        mouse.unhook_all()
