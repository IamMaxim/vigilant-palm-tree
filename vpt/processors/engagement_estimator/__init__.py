"""The module responsible for estimating the engagement of the user."""
import time

import keyboard
import mouse
import numpy as np
from rx import Observable, operators
from rx.subject import Subject

from vpt.data_structures import Engagement
from vpt.capabilities import OutputCapable
from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase


class EngagementEstimator(ProcessorBase):
    """Given gaze and speech data, estimates the user's engagement level."""

    def __init__(self, head_rotation_vector: OutputCapable[np.ndarray], voice_present: OutputCapable[bool]):
        self.subj = Subject()

        # Current state
        self.rotation_accum = 0
        self.voice_accum = 0

        # Observable with all data channels merged into one stream
        obs = head_rotation_vector.output.pipe(operators.combine_latest(voice_present.output))

        obs.subscribe(self.process_state)

    def process_state(self, state):
        video_eng, voice = state

        # BE CAREFUL WITH =='s HERE! Remember we may have None as well.
        # is DOES NOT WORK HERE! DO NOT TRY TO "BEAUTIFY" THE CODE!
        if video_eng == True and voice == False:
            self.subj.on_next(Engagement.ENGAGEMENT)
        elif video_eng == True and voice == True:
            self.subj.on_next(Engagement.CONFERENCING)
        elif video_eng == False and voice == False:
            self.subj.on_next(Engagement.IDLING)
        elif video_eng == False and voice == True:
            self.subj.on_next(Engagement.DISTRACTION)
        elif video_eng == None:
            self.subj.on_next(Engagement.ABSENCE)
        else:
            raise Exception('Invalid engagement state machine state detected')

    @property
    def output(self) -> Observable:
        return self.subj
