import threading

import cv2
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from nodes import SourceBase


class DeviceVideoSource(SourceBase[VideoFrame]):
    need_to_run: bool
    __subject: Subject
    video_capture: cv2.VideoCapture
    video_filename: str

    def start(self):
        self.need_to_run = True
        thread = threading.Thread(target=self.capture_loop)
        thread.start()

    def stop(self):
        self.need_to_run = False

    def capture_loop(self):
        video_capture = cv2.VideoCapture(self.video_filename)
        while self.need_to_run:
            ret, frame = video_capture.read()
            self.__subject.on_next(VideoFrame(frame))

    def __init__(self, filename: str):
        self.__subject = Subject()
        self.video_filename = filename

    def get_data_stream(self) -> Observable:
        return self.__subject
