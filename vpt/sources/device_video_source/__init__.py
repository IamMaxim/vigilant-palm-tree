'''Gets the video from the device.'''
import threading

import cv2
from rx import Observable
from rx.subject import Subject

from data_structures import VideoFrame
from vpt.sources.base import SourceBase


class DeviceVideoSource(SourceBase[VideoFrame]):
    '''A data source for the video stream from the device.'''
    _subj: Subject
    video_capture: cv2.VideoCapture
    device = 0

    def start(self):
        '''Starts the video recording stream in a separate thread.'''
        if not self.stopped:
            return

        self.stopped = False
        threading.Thread(target=self.capture_loop).start()

    def stop(self):
        '''Stops recording video.'''
        self.stopped = True

    def capture_loop(self):
        '''Captures frames from the video and sends them to the stream.'''
        video_capture = cv2.VideoCapture(self.device)
        while not self.stopped:
            _ret, frame = video_capture.read()
            self._subj.on_next(VideoFrame(frame))

    def __init__(self, device_id: int = 0):
        self._subj = Subject()
        self.device = device_id
        self.stopped = True

    @property
    def output(self) -> Observable:
        '''The getter for the video frames observable.'''
        return self._subj
