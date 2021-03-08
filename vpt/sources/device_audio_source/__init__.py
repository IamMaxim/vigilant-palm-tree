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
    _subj: Subject
    device: Union[str, int]
    channels: int
    sample_rate: float

    def __init__(self, channels: int, sample_rate: float, device: Union[str, int] = None):
        self.stopped = True
        self._subj = Subject()
        self.device = device
        self.channels = channels
        self.sample_rate = sample_rate

    @property
    def output(self) -> Observable:
        '''The getter for the audio chunks observable.'''
        return self._subj

    def run(self):
        '''Records the audio into a stream.'''
        sample_duration = 1
        while not self.stopped:
            rec = sd.rec(int(sample_duration * self.sample_rate),
                         samplerate=self.sample_rate,
                         channels=self.channels,
                         device=self.device,
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
