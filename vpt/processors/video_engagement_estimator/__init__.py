from rx import Observable
from rx.subject import Subject

from vpt.capabilities import OutputCapable
from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase

import numpy as np


class VideoEngagementEstimator(ProcessorBase):
    """Returns:
        - none if no face was detected in the video frame
        - true if face was detected and it is looking at the camera
        - false if face was detected but it looks sideways
    """

    _subj: Subject

    def __init__(self, head_rotation_source: OutputCapable[np.ndarray]):
        self._subj = Subject()
        head_rotation_source.output.subscribe(self.process_rotation)
        self.boundary = 1

    def process_rotation(self, rot: np.ndarray):
        if rot is None:
            self._subj.on_next(None)
        else:
            self._subj.on_next(np.linalg.norm(rot) < self.boundary)

    @property
    def output(self) -> Observable:
        return self._subj
