from rx import Observable
from rx.subject import Subject

from modulebase import ModuleBase


class KeyboardToFileOutputModule(ModuleBase):

    def __init__(self, keyboard_source: ModuleBase):
        keyboard_source.get_data_stream().subscribe(self.process_event)
        self.file = open('keyboard_output.txt', 'w+')

    def process_event(self, event):
        self.file.write('%s %s %s\n' % (event.name, event.scan_code, event.time))
        self.file.flush()

    def get_data_stream(self) -> Observable:
        return Subject()

    def start(self):
        pass

    def stop(self):
        pass
