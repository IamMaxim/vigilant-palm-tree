'''Processes an audio stream to detect speech.'''
from vpt.processors.base import ProcessorBase


class SpeechDetector(ProcessorBase):
    '''Detects speech in an audio stream and outputs a signal stream for that.'''
