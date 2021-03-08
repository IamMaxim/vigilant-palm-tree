'''A collection of data source nodes.'''
from .device_audio_source import DeviceAudioSource
from .wav_audio_source import WavAudioSource
from .device_video_source import DeviceVideoSource
from .keyboard_source import KeyboardSource
from .mouse_source import MouseSource

__all__ = (
    'DeviceAudioSource',
    'WavAudioSource',
    'DeviceVideoSource',
    'KeyboardSource',
    'MouseSource',
)
