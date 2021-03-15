'''Processes an audio stream to detect speech.'''

import numpy as np
from rx import Observable
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler
from scipy import fft

from vpt.sources.base import SourceBase
from vpt.processors.base import ProcessorBase

# The frequency range of human voice in Hz.
VOICE_RANGE = range(80, 1100 + 1)


class SpeechDetector(ProcessorBase[bool]):
    '''Detects speech in an audio stream and outputs a signal stream for that.'''
    _subj: Subject
    mean_loudness: np.float64
    '''The threshold which the amplitude needs to overcome
       to be considered present (in undefined units).'''
    noise_threshold: float
    '''The fraction of the current mean loudness that
       the signal needs to overcome to not be disregarded as silence.'''
    silence_threshold: float
    _samples: int

    def __init__(self,
                 audio_source: SourceBase[np.ndarray],
                 noise_threshold: float = .5,
                 silence_threshold: float = .3):
        '''Wire up the detector to an arbitrary audio source.'''
        self._subj = Subject()
        self.stopped = True
        self.sources = [audio_source]
        self.mean_loudness = None
        self._samples = 0
        self.noise_threshold = noise_threshold
        self.silence_threshold = silence_threshold
        self.subscriptions = None

    def start(self):
        if not self.stopped:
            return
        super().start()
        audio_source, = self.sources

        self.subscriptions = [
            audio_source.output.subscribe(self.detect_speech),
        ]

    @property
    def output(self) -> Observable:
        '''The getter for the speech codes observable.'''
        return self._subj

    def detect_speech(self, frame: np.ndarray):
        '''Detect sound in speech frequencies in a given audio frame.'''
        if frame.shape[-1] == 0:
            # Empty audio frames should not be processed
            return

        if frame.ndim == 1:
            frame = frame.reshape(len(frame), 1)

        try:
            freqs = self.fft(frame.mean(axis=1))
        except ValueError:
            return
        this_loudness = freqs.max(axis=0)

        if self.is_silence(this_loudness):
            self._subj.on_next(False)
        else:
            freqs_norm = self.normalize_frequencies(freqs)
            self._subj.on_next(
                np.any(freqs_norm[VOICE_RANGE] >= self.noise_threshold))
        self.update_mean(this_loudness)

    def update_mean(self, new_loudness):
        '''Updates the internal mean relative loudness level with a new sample.'''
        if self.mean_loudness is None:
            self.mean_loudness = new_loudness
        else:
            self.mean_loudness *= self._samples / (self._samples + 1)
            self.mean_loudness += new_loudness / (self._samples + 1)
        self._samples += 1

    def is_silence(self, new_loudness):
        '''Tests if a given relative loudness level is quiet enough to be disregarded.'''
        if self.mean_loudness is None:
            return False
        try:
            return new_loudness / self.mean_loudness < self.silence_threshold
        except ZeroDivisionError:
            return True

    @staticmethod
    def fft(frame):
        '''Convert the audio signal from the time domain to the frequency domain.'''
        frame -= np.average(frame)
        fft_normal = fft.fft(frame)

        return abs(fft_normal[:len(frame) // 2])

    @staticmethod
    def normalize_frequencies(frequencies):
        '''Normalize an array of frequency amplitudes, scaling them from 0 to 1.'''
        # Multiplication is used instead of division for performance
        return frequencies * (1 / frequencies.max(axis=0))
