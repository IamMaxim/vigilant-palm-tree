'''Processes an audio stream to detect speech.'''

import numpy as np
from rx.subject import Subject
from scipy import fft

from vpt.sources.base import SourceBase
from vpt.processors.base import ProcessorBase

# The frequency range of human voice in Hz.
VOICE_RANGE = range(80, 1100 + 1)
# The threshold which the amplitude needs to overcome to be considered present (in undefined units).
NOISE_THRESHOLD = .5


class SpeechDetector(ProcessorBase[bool]):
    '''Detects speech in an audio stream and outputs a signal stream for that.'''
    subj = Subject()

    def __init__(self, audio_source: SourceBase[np.ndarray]):
        '''Wire up the detector to an arbitrary audio source.'''
        audio_source.get_data_stream().subscribe(self.detect_speech)

    def get_data_stream(self):
        return self.subj

    def detect_speech(self, frame: np.ndarray):
        '''Detect sound in speech frequencies in a given audio frame.'''
        if frame.ndim == 1:
            frame = frame.reshape(len(frame), 1)
        self.subj.on_next(np.any(self.fft(frame.mean(axis=1))[VOICE_RANGE] >= NOISE_THRESHOLD))

    @staticmethod
    def fft(frame):
        '''Convert the audio signal from the time domain to the frequency domain.'''
        frame -= np.average(frame)
        fft_normal = fft.fft(frame) / len(frame)

        result = abs(fft_normal[range(len(frame) // 2)]).astype(np.float64)
        result *= 1 / result.max(axis=0)
        return result

    def start(self):
        pass

    def stop(self):
        pass
