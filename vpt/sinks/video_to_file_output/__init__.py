from os import makedirs

import cv2

from data_structures import VideoFrame
from vpt.sources.base import SourceBase
from vpt.sinks.base import SinkBase


class VideoToFileOutputProcessor(SinkBase):
    dir = 'video_output'
    counter = 0

    def __init__(self, frame_provider: SourceBase[VideoFrame]):
        makedirs(self.dir, exist_ok=True)

        frame_provider.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        path = self.dir + '/' + str(self.counter) + '.png'
        cv2.imwrite(path, frame.frame)
        self.counter += 1
