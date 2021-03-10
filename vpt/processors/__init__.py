'''A collection of the processor node that operate on the data.'''
from .gaze_detector import GazeDetector
from .speech_detector import SpeechDetector
from .engagement_estimator import EngagementEstimator
from .mouse_compressor import MouseCompressor

__all__ = (
    'GazeDetector',
    'SpeechDetector',
    'EngagementEstimator',
    'MouseCompressor',
)
