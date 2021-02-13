import threading

import cv2
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from modulebase import ModuleBase


class WebcamCaptureModule(ModuleBase[VideoFrame]):
    need_to_run: bool
    __subject: Subject
    video_capture: cv2.VideoCapture

    def start(self):
        self.need_to_run = True
        thread = threading.Thread(target=self.capture_loop)
        thread.start()

    def stop(self):
        self.need_to_run = False

    def capture_loop(self):
        video_capture = cv2.VideoCapture(0)
        while self.need_to_run:
            ret, frame = video_capture.read()
            self.__subject.on_next(VideoFrame(frame))

    def __init__(self):
        self.__subject = Subject()

    def get_data_stream(self) -> Observable:
        return self.__subject
