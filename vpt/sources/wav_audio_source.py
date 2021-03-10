'''Gets the audio from a WAV file.'''

import math
import threading

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from rx import Observable
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler
from scipy.fft import fft

from vpt.sources.base import SourceBase


def freq_decompose(signal):
    '''Decompose a signal into frequencies using the FFT.'''
    signal -= np.average(signal)
    fft_norm = fft(signal)
    return abs(fft_norm[:len(fft_norm) // 2]).astype(np.float64)


class WavAudioSource(SourceBase[np.ndarray]):
    '''A data source for the audio stream from a WAV file.'''
    _subj: Subject
    filename: str
    sample_rate: int
    debug: bool
    _thread: threading.Thread

    def __init__(self, filename, debug=False):
        '''Select the WAV file to read from.'''
        self._subj = Subject()
        self.stopped = True
        self.filename = filename
        self.debug = debug

    @property
    def output(self) -> Observable:
        '''The getter for the audio chunks observable.'''
        return self._subj

    def start(self):
        '''Outputs the entire file into the stream in 1-second chunks.'''
        if not self.stopped:
            return
        self.stopped = False
        self._thread = threading.Thread(target=self.run_threaded)
        self._thread.start()

    def run_threaded(self):
        '''The thread's routine to read a file and output it into the observable.'''
        data, sample_rate = sf.read(self.filename)
        if data.ndim == 1:
            data = data.reshape(len(data), 1)
        self.sample_rate = sample_rate

        if self.debug:
            print(f'Sample rate: {self.sample_rate}')
            print(f'Total samples: {data.shape}')

        for chunk in np.array_split(data, math.ceil(len(data) / sample_rate)):
            if self.stopped:
                return

            self._subj.on_next(chunk)
            if self.debug:
                sd.play(chunk, self.sample_rate)
                sd.wait()
                self.plot_chunk(chunk)
                plt.show()
        self.stopped = True

    def plot_chunk(self, chunk):
        '''Plot a chunk of audio as a waveform and as a spectrum.'''
        mono = chunk.mean(axis=1)
        time = np.arange(len(mono)) / float(self.sample_rate)

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(time, mono)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        amplitudes = freq_decompose(mono)

        plt.subplot(2, 1, 2)
        plt.plot(np.arange(len(amplitudes)), amplitudes, 'b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('Amplitude')
        plt.tight_layout()

    def stop(self):
        '''Stops the thread from outputting any more chunks, unless it's done.'''
        if self.stopped:
            return
        self.stopped = True
        self._thread.join()
