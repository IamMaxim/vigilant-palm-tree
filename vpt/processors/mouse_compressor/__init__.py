"""Compress mouse events."""
from rx import Observable
from rx import operators
from rx.subject import Subject

from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase


class MouseCompressor(ProcessorBase):
    """Compresses a stream of mouse events to reduce redundancy."""

    def __init__(self, mouse_source: SourceBase, window_duration=0.016):
        self.subj = Subject()
        mouse_source \
            .get_data_stream() \
            .pipe(operators.throttle_first(window_duration)) \
            .subscribe(lambda x: self.subj.on_next(x))

    def get_data_stream(self) -> Observable:
        return self.subj

    def start(self):
        pass

    def stop(self):
        pass
