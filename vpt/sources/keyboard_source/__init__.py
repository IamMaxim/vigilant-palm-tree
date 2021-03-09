'''Registers keyboard events to a data stream.'''
import keyboard
from rx import Observable
from rx.subject import Subject

from vpt.sources.base import SourceBase


class KeyboardSource(SourceBase[keyboard.KeyboardEvent]):
    '''A source node for keyboard events.'''
    _subj: Subject

    def __init__(self):
        self._subj = Subject()
        self.stopped = True

    def start(self):
        '''Attach an event listener.'''
        if not self.stopped:
            return
        self.stopped = False
        keyboard.hook(self.callback)

    def stop(self):
        '''Detach the event listener.'''
        if self.stopped:
            return
        self.stopped = True
        keyboard.unhook_all()

    def callback(self, event: keyboard.KeyboardEvent):
        '''Sends the event to the stream.'''
        self._subj.on_next(event)

    @property
    def output(self) -> Observable:
        '''The getter for the keyboard events observable.'''
        return self._subj
