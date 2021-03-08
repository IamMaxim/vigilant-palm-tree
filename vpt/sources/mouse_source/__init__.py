'''Registers mouse events to a data stream.'''
import mouse
from rx import Observable
from rx.subject import Subject

from vpt.sources.base import SourceBase


class MouseSource(SourceBase):
    '''A source node for mouse events.'''
    _subj: Subject

    def __init__(self):
        self._subj = Subject()
        self.stopped = True

    @property
    def output(self) -> Observable:
        '''The getter for the mouse events observable.'''
        return self._subj

    def callback(self, event):
        '''Sends the event to the stream.'''
        self._subj.on_next(event)

    def start(self):
        if not self.stopped:
            return
        self.stopped = False
        mouse.hook(self.callback)

    def stop(self):
        self.stopped = True
        mouse.unhook_all()
