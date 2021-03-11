"""The module responsible for estimating the engagement of the user."""
from typing import Tuple

import numpy as np
from rx import Observable, operators
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.data_structures import Engagement, Gaze
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
        self.subscriptions = None

    def start(self):
        if not self.stopped:
            return
        super().start()
        head_rotation_vector, voice_present = self.sources

        # Observable with all data channels merged into one stream
        obs = head_rotation_vector.output.pipe(operators.combine_latest(voice_present.output))
        self.subscriptions = [
            obs.subscribe(self.process_state),
        ]

    def process_state(self, state: Tuple[Gaze, bool]):
        '''Convert the state pair into an engagement code.'''
        video_eng, voice = state

        if video_eng == Gaze.WORKSPACE and not voice:
            self._subj.on_next(Engagement.ENGAGEMENT)
        elif video_eng == Gaze.WORKSPACE and voice:
            self._subj.on_next(Engagement.CONFERENCING)
        elif video_eng == Gaze.ELSEWHERE and not voice:
            self._subj.on_next(Engagement.IDLING)
        elif video_eng == Gaze.ELSEWHERE and voice:
            self._subj.on_next(Engagement.DISTRACTION)
        elif video_eng == Gaze.ABSENT:
            self._subj.on_next(Engagement.ABSENCE)

    @property
    def output(self) -> Observable:
        '''The getter for the engagement codes observable.'''
        return self._subj
