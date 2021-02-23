from rx import Observable
from rx.subject import Subject

from nodes import ProcessorBase
import numpy as np


class GazeEngagementEstimator(ProcessorBase[np.ndarray]):
    subj = Subject()

    def __init__(self, rotation_vector_source: ProcessorBase[np.ndarray]):
        rotation_vector_source.get_data_stream().subscribe(lambda v: self.subj.on_next(np.linalg.norm(v)))

    def get_data_stream(self) -> Observable:
        return self.subj
