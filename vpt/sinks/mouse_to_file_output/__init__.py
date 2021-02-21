import mouse

from vpt.sources.base import SourceBase
from vpt.sinks.base import SinkBase


class MouseToFileOutputProcessor(SinkBase):
    def __init__(self, mouse_source: SourceBase):
        self.file = open('mouse_output.txt', 'w+')
        mouse_source.get_data_stream().subscribe(self.process_mouse)

    def process_mouse(self, event):
        if isinstance(event, mouse.ButtonEvent):
            self.file.write('button %s %s %s\n' % (event.button, event.event_type, event.time))
        elif isinstance(event, mouse.WheelEvent):
            self.file.write('wheel %s %s\n' % (event.delta, event.time))
        elif isinstance(event, mouse.MoveEvent):
            self.file.write('move %s %s %s\n' % (event.x, event.y, event.time))
        self.file.flush()
