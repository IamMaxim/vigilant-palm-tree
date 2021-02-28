'''Transforms the gaze estimation to engagement estimation.'''
import numpy as np
from rx import Observable
from rx.subject import Subject

from vpt.processors.base import ProcessorBase


class GazeEngagementEstimator(ProcessorBase[np.ndarray]):
    '''Transforms the gaze estimation to engagement estimation.'''
    _subj: Subject

    def __init__(self, rotation_vector_source: ProcessorBase[np.ndarray]):
        self._subj = Subject()
        rotation_vector_source.get_data_stream().subscribe(
            lambda v: self._subj.on_next(np.linalg.norm(v))
        )

    def get_data_stream(self) -> Observable:
        return self._subj
