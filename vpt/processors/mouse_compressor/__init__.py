'''Compress mouse events.'''
from vpt.processors.base import ProcessorBase


class MouseCompressor(ProcessorBase):
    '''Compresses a stream of mouse events to reduce redundancy.'''
