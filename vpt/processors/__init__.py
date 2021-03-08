'''A collection of the processor node that operate on the data.'''
from .gaze_detector import GazeDetector
from .gaze_engagement_estimator import GazeEngagementEstimator
from .mouse_compressor import MouseCompressor
from .speech_detector import SpeechDetector

__all__ = (
    'GazeDetector',
    'GazeEngagementEstimator',
    'MouseCompressor',
    'SpeechDetector',
)
