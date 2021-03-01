import time

import numpy as np

from vpt.sources.base import SourceBase
from vpt.processors import EngagementEstimator, GazeDetector, engagement_estimator
from vpt.sinks import VideoDisplay, FileStore, GraphView
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource

from rx import create


class Dummy(SourceBase[float]):
    def __init__(self):
        self.running = True

        def something(observer, scheduler):
            while self.running:
                observer.on_next(np.random.randint(0, 2))
                time.sleep(0.1)
            observer.on_completed()

        self.subj = create(something)

    def get_data_stream(self):
        '''Returns the stream of data that can be listened to.'''
        return self.subj

    def start(self):
        '''Starts the data stream.'''
        self.running = True

    def stop(self):
        '''Stops the data stream.'''
        self.running = False


def record():
    '''Runs all of the recorders to check that everything works correctly.'''
    print('Recording...')

    # Create capture nodes
    engagement_source = Dummy()
    keyboard_source = KeyboardSource()
    mouse_source = MouseSource()

    graph_display = GraphView(mouse_source, keyboard_source, engagement_source)

    # Start capture on all types of sources
    engagement_source.start()
    keyboard_source.start()
    mouse_source.start()

    graph_display.run()

    # Stop capture on all types of sources
    engagement_source.stop()
    keyboard_source.stop()
    mouse_source.stop()

    print('Done')
