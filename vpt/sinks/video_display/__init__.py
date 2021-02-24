import time
from time import sleep

import cv2

from data_structures import VideoFrame
from vpt.sources.base import SourceBase
from vpt.sinks.base import SinkBase


class VideoDisplay(SinkBase):
    frame: VideoFrame = None
    stopped: bool
    start_time: float
    duration: float

    def __init__(self, video_frame_source: SourceBase[VideoFrame], duration=-1):
        """
        :param video_frame_source: the source of video frames. May be a processor or source node.
        :param duration: max duration after which the display will automatically close. -1 means the window will never
        close. Given in seconds.
        """
        self.stopped = False
        self.duration = duration
        self.start_time = time.time()
        video_frame_source.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        self.frame = frame

    # Note: this is a blocking method. It returns as soon as user presses the ESC key
    def run(self):
        print('run')

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
        cv2.destroyWindow('Video')
        self.stopped = True
        cv2.waitKey(1)
