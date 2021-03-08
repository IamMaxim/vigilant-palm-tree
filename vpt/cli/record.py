import time

from vpt.processors import EngagementEstimator, GazeDetector, SpeechDetector, MouseCompressor
from vpt.processors.video_engagement_estimator import VideoEngagementEstimator
from vpt.sinks import GraphView, SQLiteStore
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource


def record():
    """Runs all of the recorders to check that everything works correctly."""
    print('Recording...')

    # Create capture nodes
    video_source = DeviceVideoSource()
    audio_source = DeviceAudioSource()
    keyboard_source = KeyboardSource()
    __mouse_source = MouseSource()

    gaze_detector = GazeDetector(video_source)
    video_estimator = VideoEngagementEstimator(gaze_detector)

    speech_detector = SpeechDetector(audio_source)

    mouse_throttler = MouseCompressor(__mouse_source)

    engagement_estimator = EngagementEstimator(
        video_estimator, speech_detector)

    store = SQLiteStore(f'session-{int(time.time())}.db',
                        mouse_throttler, keyboard_source, engagement_estimator)
    graph_display = GraphView(
        mouse_throttler, keyboard_source, engagement_estimator)

    # Start capture on all types of sources
    video_source.start()
    audio_source.start()
    keyboard_source.start()
    __mouse_source.start()

    # while True:
    #     store.update()
    #     graph_display.update()
    graph_display.qapp.exec_()

    # Stop capture on all types of sources
    video_source.stop()
    audio_source.stop()
    keyboard_source.stop()
    __mouse_source.stop()

    print('Done')
