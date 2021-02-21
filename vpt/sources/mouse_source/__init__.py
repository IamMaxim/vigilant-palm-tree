import mouse
from rx import Observable
from rx.subject import Subject

from nodes import SourceBase


class MouseSource(SourceBase):
    subj = Subject()

    def get_data_stream(self) -> Observable:
        return self.subj

    def callback(self, event):
        self.subj.on_next(event)

    def start(self):
        mouse.hook(self.callback)

    def stop(self):
        mouse.unhook_all()
