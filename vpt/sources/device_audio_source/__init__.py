'''Gets the audio from the device.'''
import threading
from typing import Union

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

    def __init__(self, device: Union[str, int] = None):
        super().__init__()
        if device is not None:
            sd.default.device = device

    def get_data_stream(self) -> Observable:
        return self._subj

    def run(self):
        '''Records the audio into a stream.'''
        while not self.stopped:
            rec = sd.rec(int(self.sample_duration * self.sample_rate),
                         samplerate=self.sample_rate,
                         channels=2,
                         blocking=True)

            rec = self.trim_corruption_lol(rec)
            self._subj.on_next(rec)

    def trim_corruption_lol(self, chunk):
        eps = 1e-4
        for sample_idx in range(len(chunk)):
            if np.any(chunk[sample_idx] > eps):
                break
        return chunk[int(sample_idx * 1.1):, :]

    def start(self):
        self.stopped = False
        threading.Thread(target=self.run).start()

    def stop(self):
        pass
