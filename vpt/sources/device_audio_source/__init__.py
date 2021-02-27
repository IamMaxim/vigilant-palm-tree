'''Gets the audio from the device.'''
import threading

import numpy as np
import sounddevice as sd
from rx import Observable
from rx.subject import Subject

from vpt.sources.base import SourceBase


class DeviceAudioSource(SourceBase[np.ndarray]):
    '''A data source for the audio stream from the device.'''
    stopped = False
    sample_duration = 1
    sample_rate = 44100
    _subj: Subject

    def __init__(self):
        self._subj = Subject()

    def get_data_stream(self) -> Observable:
        return self._subj

    def run(self):
        '''Records the audio into a stream.'''
        while not self.stopped:
            rec = sd.rec(int(self.sample_duration * self.sample_rate),
                         samplerate=self.sample_rate,
                         channels=1)
            sd.wait()
            self._subj.on_next(rec)

    def start(self):
        self.stopped = False
        threading.Thread(target=self.run).start()

    def stop(self):
        pass
