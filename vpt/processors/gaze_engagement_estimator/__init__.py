'''Transforms the gaze estimation to engagement estimation.'''
from typing import List

import numpy as np
from rx import Observable
from rx.subject import Subject

from vpt.processors.base import ProcessorBase
from vpt.capabilities import OutputCapable


class GazeEngagementEstimator(ProcessorBase[np.ndarray]):
    '''Transforms the gaze estimation to engagement estimation.'''
    _subj: Subject
    sources: List[OutputCapable]

    def __init__(self, rotation_vector_source: OutputCapable[np.ndarray]):
        self._subj = Subject()
        self.stopped = True
        self.sources = [rotation_vector_source]
        rotation_vector_source.output.subscribe(
            lambda v: self._subj.on_next(np.linalg.norm(v))
        )

    @property
    def output(self) -> Observable:
        '''The getter for the engagement codes observable.'''
        return self._subj
