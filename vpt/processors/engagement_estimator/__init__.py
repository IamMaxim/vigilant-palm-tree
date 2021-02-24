'''The module responsible for estimating the engagement of the user.'''
from vpt.processors.base import ProcessorBase


class EngagementEstimator(ProcessorBase):
    '''Given gaze and speech data, estimates the user's engagement level.'''
