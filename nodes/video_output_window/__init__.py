from time import sleep

import cv2

from data_structures import VideoFrame
from processorbase import ProcessorBase, SinkBase


class VideoOutputWindowProcessor(SinkBase):
    frame: VideoFrame = None
    stopped: bool

    def __init__(self, video_frame_source: ProcessorBase[VideoFrame]):
        self.stopped = False
        video_frame_source.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        self.frame = frame

    # Note: this is a blocking method. It returns as soon as user presses the ESC key
    def run(self):
        print('run')

        while not self.stopped:
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
