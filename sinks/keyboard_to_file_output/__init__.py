from processorbase import ProcessorBase, SinkBase


class KeyboardToFileOutputProcessor(SinkBase):

    def __init__(self, keyboard_source: ProcessorBase):
        keyboard_source.get_data_stream().subscribe(self.process_event)
        self.file = open('keyboard_output.txt', 'w+')

    def process_event(self, event):
        self.file.write('%s %s %s\n' % (event.name, event.scan_code, event.time))
        self.file.flush()
