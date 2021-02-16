from time import sleep

import cv2
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from modulebase import ModuleBase


class VideoOutputWindowModule(ModuleBase):
    frame: VideoFrame = None
    stopped: bool

    def __init__(self, video_frame_source: ModuleBase[VideoFrame]):
        self.stopped = False
        video_frame_source.get_data_stream().subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        self.frame = frame

    def start(self):
        # threading.Thread(target=self.show).start()
        raise NotImplementedError('VideoOutputWindowModule does not support start() method, as it requires main thread.'
                                  ' Use !blocking! run() instead')

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

    def get_data_stream(self) -> Observable:
        return Subject()
