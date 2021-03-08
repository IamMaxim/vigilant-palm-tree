'''Display the incoming video stream directly to the user on the screen.'''
import time
from time import sleep

import cv2

from data_structures import VideoFrame
from vpt.sources.base import SourceBase
from vpt.sinks.base import SinkBase


class VideoDisplay(SinkBase):
    '''A sink node to display the stream as video feed.'''
    frame: VideoFrame = None
    start_time: float
    duration: float

    def __init__(self, video_frame_source: SourceBase[VideoFrame], duration=-1):
        """
        :param video_frame_source: the source of video frames. May be a processor or source node.
        :param duration: max duration after which the display will automatically close.
            -1 means the window will never close. Given in seconds.
        """
        self.stopped = True
        self.sources = [video_frame_source]
        self.duration = duration
        video_frame_source.output.subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        '''Updates the currently displayed frame.'''
        self.frame = frame

    def start(self):
        '''Starts the video display.
           Note: this is a blocking method. It returns as soon as user presses the ESC key.'''
        super().start()
        self.start_time = time.time()
        while not self.stopped:
            # If we have a time on max time and we exceeded the duration, break the loop
            if self.duration != -1 and time.time() > self.start_time + self.duration:
                self.stop()
                break

            try:
                # Skip displaying frame for second time
                if self.frame is None:
                    sleep(0.001)
                    continue

                cv2.imshow('Video', self.frame.frame)
                self.frame = None
                if cv2.waitKey(1) == 27:
                    self.stop()  # esc to quit
            except AttributeError:
                # If this is thrown, no frames arrived yet
                sleep(0.01)
                continue

    def stop(self):
        '''Stops displaying the video stream.'''
        super().stop()
        cv2.destroyWindow('Video')
        cv2.waitKey(1)
