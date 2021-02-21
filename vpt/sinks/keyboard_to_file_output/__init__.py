from vpt.sources.base import SourceBase
from vpt.sinks.base import SinkBase


class KeyboardToFileOutputProcessor(SinkBase):

    def __init__(self, keyboard_source: SourceBase):
        keyboard_source.get_data_stream().subscribe(self.process_event)
        self.file = open('keyboard_output.txt', 'w+')

    def process_event(self, event):
        self.file.write('%s %s %s\n' % (event.name, event.scan_code, event.time))
        self.file.flush()
