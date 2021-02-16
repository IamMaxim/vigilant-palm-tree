import os

import sounddevice
from rx import Observable
from rx.subject import Subject

import soundfile as sf

from modulebase import ModuleBase


class AudioToFileOutputModule(ModuleBase):

    def __init__(self, rec_source: ModuleBase):
        rec_source.get_data_stream().subscribe(self.process_audio_rec)
        try:
            os.remove('audio.wav')
        except FileNotFoundError:
            pass  # No file created yet

        self.file = sf.SoundFile('audio.wav', mode='w', samplerate=44100, channels=1)

    def process_audio_rec(self, rec):
        self.file.write(rec)

    def get_data_stream(self) -> Observable:
        return Subject()

    def start(self):
        pass

    def stop(self):
        pass
