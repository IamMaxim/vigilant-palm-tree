'''A collection of the processor node that operate on the data.'''
from .engagement_estimator import EngagementEstimator
from .gaze_detector import GazeDetector
from .gaze_engagement_estimator import GazeEngagementEstimator
from .mouse_compressor import MouseCompressor
from .speech_detector import SpeechDetector

__all__ = (
    'EngagementEstimator',
    'GazeDetector',
    'GazeEngagementEstimator',
    'MouseCompressor',
    'SpeechDetector',
)
