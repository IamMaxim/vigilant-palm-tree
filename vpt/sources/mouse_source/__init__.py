"""Registers mouse events to a data stream."""
import mouse
from rx import Observable
from rx.subject import Subject

from vpt.sources.base import SourceBase


class MouseSource(SourceBase):
    """A source node for mouse events."""
    _subj: Subject

    def __init__(self):
        self._subj = Subject()

    def get_data_stream(self) -> Observable:
        return self._subj

    def callback(self, event):
        """Sends the event to the stream."""
        self._subj.on_next(event)

    def start(self):
        mouse.hook(self.callback)

    def stop(self):
        mouse.unhook_all()
