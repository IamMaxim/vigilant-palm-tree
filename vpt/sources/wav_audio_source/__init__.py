'''Gets the audio from the device.'''

import math

import numpy as np
from rx import Observable
from rx.subject import Subject
from scipy.io import wavfile

from vpt.sources.base import SourceBase


from scipy.fft import fft
import numpy as np
from numpy import arange
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

def frequency_sepectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft(x) / n  # fft computing and normalization
    x = abs(x[range(n // 2)]).astype(np.float64)
    x *= 1 / x.max(axis=0)


    return frqarr, x


class WavAudioSource(SourceBase[np.ndarray]):
    '''A data source for the audio stream from the device.'''
    subj = Subject()
    filename: str
    sample_rate: int

    def __init__(self, filename):
        '''Select the WAV file to read from.'''
        self.filename = filename

    def get_data_stream(self) -> Observable:
        return self.subj

    def start(self):
        '''Outputs the entire file into the stream in 1-second chunks.'''
        sf, data = wavfile.read(self.filename)
        print(sf)
        if data.ndim == 1:
            data = data.reshape(len(data), 1)
        self.sample_rate = sf
        for chunk in np.array_split(data, math.ceil(len(data) / sf)):
            self.subj.on_next(chunk)

            y = chunk[:, 0]  # use the first channel (or take their average, alternatively)
            t = np.arange(len(y)) / float(sf)

            plt.figure()
            plt.subplot(2, 1, 1)
            plt.plot(t, y)
            plt.xlabel('t')
            plt.ylabel('y')

            frq, X = frequency_sepectrum(y, sf)

            plt.subplot(2, 1, 2)
            plt.plot(frq, X, 'b')
            plt.xlabel('Freq (Hz)')
            plt.ylabel('|X(freq)|')
            plt.tight_layout()

            plt.show()

    def stop(self):
        pass
