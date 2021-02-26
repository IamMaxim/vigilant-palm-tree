'''Gets the audio from the device.'''

import math

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from rx import Observable
from rx.subject import Subject
from scipy.fft import fft

from vpt.sources.base import SourceBase


def freq_decompose(signal, sample_rate):
    signal -= np.average(signal)
    fft_norm = fft(signal)
    return abs(fft_norm[:len(fft_norm) // 2]).astype(np.float64)


class WavAudioSource(SourceBase[np.ndarray]):
    '''A data source for the audio stream from the device.'''
    subj = Subject()
    filename: str
    sample_rate: int
    debug: bool

    def __init__(self, filename, debug=False):
        '''Select the WAV file to read from.'''
        self.filename = filename
        self.debug = debug

    def get_data_stream(self) -> Observable:
        return self.subj

    def start(self):
        '''Outputs the entire file into the stream in 1-second chunks.'''
        data, sample_rate = sf.read(self.filename)
        if data.ndim == 1:
            data = data.reshape(len(data), 1)
        self.sample_rate = sample_rate

        if self.debug:
            print(f'Sample rate: {self.sample_rate}')
            print(f'Total samples: {data.shape}')

        for chunk in np.array_split(data, math.ceil(len(data) / sample_rate)):
            self.subj.on_next(chunk)
            if self.debug:
                sd.play(chunk, self.sample_rate)
                sd.wait()
                self.plot_chunk(chunk)
                plt.show()

    def plot_chunk(self, chunk):
        mono = chunk.mean(axis=1)
        time = np.arange(len(mono)) / float(self.sample_rate)

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(time, mono)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        amplitudes = freq_decompose(mono, self.sample_rate)

        plt.subplot(2, 1, 2)
        plt.plot(np.arange(len(amplitudes)), amplitudes, 'b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel(f'Amplitude')
        plt.tight_layout()

    def stop(self):
        pass
