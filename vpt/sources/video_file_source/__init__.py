import threading

import cv2
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from vpt.sources.base import SourceBase


class VideoFileSource(SourceBase[VideoFrame]):
    need_to_run: bool
    __subject: Subject

    def __init__(self, filename: str):
        self.__subject = Subject()
        self.lock = threading.Lock()

        self.video_capture = cv2.VideoCapture(filename)
        if not self.video_capture.isOpened():
            raise ValueError('could not open video stream for file {}'.format(filename))

    def start(self):
        self.need_to_run = True
        thread = threading.Thread(target=self.capture_loop)
        thread.start()

    def stop(self):
        self.need_to_run = False

    def wait(self):
        self.lock.acquire()
        self.lock.release()

    def capture_loop(self):
        with self.lock:
            while self.need_to_run:
                ret, frame = self.video_capture.read()

                if not ret:
                    break

                self.__subject.on_next(VideoFrame(frame))

    def get_data_stream(self) -> Observable:
        return self.__subject
