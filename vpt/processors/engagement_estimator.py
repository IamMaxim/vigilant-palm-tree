"""The module responsible for estimating the engagement of the user."""

import numpy as np
from rx import Observable, operators
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.data_structures import Engagement
from vpt.capabilities import OutputCapable
from vpt.processors.base import ProcessorBase


class EngagementEstimator(ProcessorBase[Engagement]):
    """Given gaze and speech data, estimates the user's engagement level."""
    _subj: Subject

    def __init__(self,
                 head_rotation_vector: OutputCapable[np.ndarray],
                 voice_present: OutputCapable[bool]):
        self._subj = Subject()
        self.stopped = True
        self.sources = [head_rotation_vector, voice_present]


    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        head_rotation_vector, voice_present = self.sources

        # Observable with all data channels merged into one stream
        obs = head_rotation_vector.output.pipe(operators.combine_latest(voice_present.output))
        obs.subscribe(self.process_state, scheduler=scheduler)

    def process_state(self, state):
        '''Convert the state pair into an engagement code.'''
        video_eng, voice = state

        if video_eng is True and voice is False:
            self._subj.on_next(Engagement.ENGAGEMENT)
        elif video_eng is True and voice is True:
            self._subj.on_next(Engagement.CONFERENCING)
        elif video_eng is False and voice is False:
            self._subj.on_next(Engagement.IDLING)
        elif video_eng is False and voice is True:
            self._subj.on_next(Engagement.DISTRACTION)
        elif video_eng is None:
            self._subj.on_next(Engagement.ABSENCE)
        else:
            raise Exception('Invalid engagement state machine state detected')

    @property
    def output(self) -> Observable:
        '''The getter for the engagement codes observable.'''
        return self._subj
