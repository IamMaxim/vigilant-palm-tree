'''The 'record' CLI command.'''

import sys
from datetime import datetime
from typing import Union

import sounddevice as sd
from rx.scheduler.mainloop import QtScheduler
from matplotlib.backends.backend_qt5 import QtCore, QtWidgets

from vpt.processors import EngagementEstimator, GazeDetector, SpeechDetector, MouseCompressor
from vpt.sinks import GraphView, CSVStore
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource


def record(audio_source: Union[str, int], video_source_id: int):
    """Runs all of the recorders to check that everything works correctly."""
    audio_device = sd.query_devices(kind='input', device=audio_source)

    # Create capture nodes
    video_source = DeviceVideoSource(video_source_id)
    audio_source = DeviceAudioSource(audio_device['max_input_channels'],
                                     audio_device['default_samplerate'],
                                     audio_source)
    keyboard_source = KeyboardSource()
    mouse_source = MouseSource()

    gaze_detector = GazeDetector(video_source)
    speech_detector = SpeechDetector(audio_source)
    mouse_compressor = MouseCompressor(mouse_source)
    engagement_estimator = EngagementEstimator(gaze_detector,
                                               speech_detector)

    store = CSVStore(f'data/session-{datetime.now().strftime("%m-%d-%H-%M")}',
                     mouse_compressor,
                     keyboard_source,
                     engagement_estimator)
    graph_view = GraphView(mouse_compressor,
                           keyboard_source,
                           engagement_estimator)

    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    store.start()
    graph_view.start()

    exit_code = qapp.exec_()

    graph_view.stop()
    store.stop()

    sys.exit(exit_code)
