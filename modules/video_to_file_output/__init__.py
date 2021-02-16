from os import mkdir

import cv2
import ffmpeg
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from modulebase import ModuleBase


class VideoToFileOutputModule(ModuleBase):
    dir = 'video_output'
    counter = 0

    def __init__(self, frame_provider: ModuleBase[VideoFrame]):
        try:
            mkdir(self.dir)
        except FileExistsError:
            pass  # dir already exists

        frame_provider.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        path = self.dir + '/' + str(self.counter) + '.png'
        cv2.imwrite(path, frame.frame)
        self.counter += 1

    def get_data_stream(self) -> Observable:
        return Subject()

    def start(self):
        pass

    def stop(self):
        pass
