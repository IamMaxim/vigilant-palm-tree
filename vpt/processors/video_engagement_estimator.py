from typing import Union

import numpy as np
from rx import Observable
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.capabilities import OutputCapable
from vpt.processors.base import ProcessorBase


class VideoEngagementEstimator(ProcessorBase[Union[None, bool]]):
    """Returns:
        - none if no face was detected in the video frame
        - true if face was detected and it is looking at the camera
        - false if face was detected but it looks sideways
    """

    _subj: Subject

    def __init__(self, head_rotation_source: OutputCapable[np.ndarray]):
        self._subj = Subject()
        self.stopped = True
        self.sources = [head_rotation_source]
        self.boundary = 1


    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        head_rotation_source, = self.sources

        head_rotation_source.output.subscribe(self.process_rotation, scheduler=scheduler)

    def process_rotation(self, rot: Union[np.ndarray, None]):
        '''Compute the gaze code based on the rotation vector.'''
        if rot is None:
            self._subj.on_next(None)
        else:
            self._subj.on_next(np.linalg.norm(rot) < self.boundary)

    @property
    def output(self) -> Observable:
        '''The getter for the gaze codes observable.'''
        return self._subj
