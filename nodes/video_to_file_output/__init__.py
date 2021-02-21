from os import mkdir

import cv2

from data_structures import VideoFrame
from processorbase import ProcessorBase, SinkBase


class VideoToFileOutputProcessor(SinkBase):
    dir = 'video_output'
    counter = 0

    def __init__(self, frame_provider: ProcessorBase[VideoFrame]):
        try:
            mkdir(self.dir)
        except FileExistsError:
            pass  # dir already exists

        frame_provider.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        path = self.dir + '/' + str(self.counter) + '.png'
        cv2.imwrite(path, frame.frame)
        self.counter += 1

