import os

import soundfile as sf

from nodes import SinkBase, ProcessorBase


class AudioToFileOutputProcessor(SinkBase):

    def __init__(self, rec_source: ProcessorBase):
        rec_source.get_data_stream().subscribe(self.process_audio_rec)
        try:
            os.remove('audio.wav')
        except FileNotFoundError:
            pass  # No file created yet

        self.file = sf.SoundFile('audio.wav', mode='w', samplerate=44100, channels=1)

    def process_audio_rec(self, rec):
        self.file.write(rec)
