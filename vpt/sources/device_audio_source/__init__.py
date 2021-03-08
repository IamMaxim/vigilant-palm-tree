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

    def __init__(self, device: Union[str, int] = None):
        self.stopped = True
        self._subj = Subject()
        if device is not None:
            sd.default.device = device

    @property
    def output(self) -> Observable:
        '''The getter for the audio chunks observable.'''
        return self._subj

    def run(self):
        '''Records the audio into a stream.'''
        while not self.stopped:
            rec = sd.rec(int(self.sample_duration * self.sample_rate),
                         samplerate=self.sample_rate,
                         channels=2,
                         blocking=True)

            rec = self.trim_corruption(rec)
            self._subj.on_next(rec)

    @staticmethod
    def trim_corruption(chunk):
        '''Trim the flat signal that comes in the beginning of the waveform
           recorded with `sounddevice`.'''
        eps = 1e-4
        idx = None
        for idx, sample in enumerate(chunk):
            if np.any(sample > eps):
                break
        return chunk[int(idx * 1.1):, :]

    def start(self):
        '''Start sending out audio frames.'''
        if not self.stopped:
            return

        self.stopped = False
        threading.Thread(target=self.run).start()

    def stop(self):
        '''Stop the data generating thread.'''
        self.stopped = True
